"""Chat sobre Neo4j con pipeline de tres agentes (CONTEXTO.md — sin RAG)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, timedelta
import re
import time
from typing import Any, Callable

from config import (
    MODEL_CONSULTANT,
    MODEL_INTERPRETER,
    MODEL_REDACTOR,
    OLLAMA_NUM_PREDICT_JSON,
    OLLAMA_NUM_PREDICT_TEXT,
)
from src.neo4j_graph import Neo4jGraphClient, QueryResult
from src.ollama_client import OllamaClient
from src.vigia_schema import GRAPH_SCHEMA_FOR_LLM


INTERPRETER_SYSTEM_PROMPT = """Eres el Agente 1 — Intérprete del sistema Vigía Cauca.

Tu tarea es analizar la pregunta del usuario en español y devolver UN SOLO objeto JSON válido
(sin markdown, sin texto adicional) con la forma exacta:

{
  "intencion": "<conteo|listado|resumen|comparacion|detalle|ranking>",
  "categoria": "<valor ENUM de NOVEDAD.categoria o null>",
  "ubicacion": { "nombre": "<texto o null>", "nivel": "<MUNICIPIO|CORREGIMIENTO|VEREDA|SECTOR|BARRIO|COMUNA|TERRITORIO_INDIGENA|null>" },
  "periodo": { "desde": "<YYYY-MM-DD|hoy|ayer|semana_pasada|este_mes|mes_pasado|null>", "hasta": "<YYYY-MM-DD|hoy|ayer|null>" },
  "perfil_usuario": "<tecnico|no_tecnico>",
  "filtros_adicionales": { },
  "consulta_mejorada": "<string o null>"
}

Reglas:
- Conoces el modelo de datos Neo4j (Vigía Cauca v2). Usa solo ENUMs y nombres del esquema provisto abajo.
- Si la intención es ambigua o falta el alcance geográfico cuando es necesario, NO hagas una pregunta de aclaración.
  En su lugar, devuelve `consulta_mejorada` con una versión mejorada y concreta de la consulta original.
  Ejemplo: usuario dice "¿Qué pasó?" → `consulta_mejorada`: "Dime los eventos de orden público ocurridos en los últimos 30 días en el departamento del Cauca."
  Ejemplo: usuario dice "Hostigamientos" → `consulta_mejorada`: "Dime los hostigamientos registrados en el último año en el Cauca."
  Si la consulta es clara y no es ambigua, `consulta_mejorada` debe ser null.
- **NO sugieras consulta mejorada** cuando la pregunta sea un ranking o listado de municipios
  (ej. "municipios con más...", "¿Cuáles son los municipios..."). En esos casos la consulta original es válida.
- **Ranking por mes sin año:** Si el usuario pide un ranking o comparación por mes (ej. "¿En qué mes hubo más...?") pero NO especifica un año, la consulta es ambigua. Devuelve `consulta_mejorada` pidiendo que especifique el año:
  Ejemplo: usuario dice "¿En qué mes se registraron más ataques con drones?" → `consulta_mejorada`: "¿De qué año te interesa consultar? Especifica el año para poder comparar los meses. Por ejemplo: 'ataques con drones en 2024'."
- Si la pregunta es saludo o no requiere datos del grafo, devuelve JSON válido con intencion "resumen",
  consulta_mejorada: null, y categoria null.
- perfil_usuario: si el usuario pide datos técnicos (veredas, cortes exactos), "tecnico"; si no, "no_tecnico".
- Para referencias temporales relativas ("hoy", "ayer", "esta semana", "semana pasada", "este mes", "mes pasado") usa los valores exactos: "hoy", "ayer", "semana_pasada", "este_mes", "mes_pasado". El sistema las resolverá automáticamente a la fecha real antes de consultar Neo4j.
- Conceptos cruzados: si el usuario pregunta por "cilindro bomba" o "cilindros bomba", esto puede aparecer en novedades de categoría "Atentado Terrorista" (los que explotaron) o "Hallazgo de Material" (los que no explotaron). Guarda el concepto en `filtros_adicionales: {"concepto": "cilindro_bomba"}` y deja `categoria` como null para que la consulta abarque ambas categorías.
""".strip()


CONSULTANT_SYSTEM_PROMPT = f"""Eres el Agente 2 — Consultor Cypher para Neo4j (Vigía Cauca).

Recibirás la pregunta original del usuario, un JSON de intención del Agente 1, el rol del usuario en la plataforma,
y la fecha de hoy (ISO) para interpretar "hoy" en filtros de fecha.

Debes responder con UN SOLO objeto JSON:
{{
  "cypher": "<consulta Cypher de solo lectura>",
  "params": {{ }}
}}

Reglas de seguridad (obligatorias):
- Solo cláusulas: MATCH, OPTIONAL MATCH, RETURN, WHERE, WITH, ORDER BY, LIMIT, UNWIND, CASE.
- PROHIBIDO: CREATE, MERGE, DELETE, SET, REMOVE, DROP, LOAD CSV, FOREACH, CALL dbms.*, CALL apoc.*.
- Toda consulta debe tener LIMIT (máximo 100).
- Para filtrar por nombre de municipio y llegar a las novedades:
  MATCH (m:MUNICIPIO {{nombre: $municipio}})-[:CONTIENE*1..4]->(lugar)<-[:OCURRE_EN]-(n:NOVEDAD)
- Dirección de relaciones exacta: (ACTOR)-[:PARTICIPA_EN]->(NOVEDAD), (NOVEDAD)-[:OCURRE_EN]->(lugar),
  (NOVEDAD)-[:TIENE_VICTIMA]->(VICTIMA), (NOVEDAD)-[:GENERA]->(AFECTACION_HUMANA).
- La propiedad en NOVEDAD es visibilidad (no nivel_visibilidad).
- Si rol_usuario es "Visitante", excluye siempre filas con novedades privadas:
  añade en el MATCH de NOVEDAD la condición AND coalesce(n.visibilidad, 'Público') = 'Público'
  (o equivalente que excluya "Privado").
- Usa parámetros ($nombre, etc.) en el diccionario `params` cuando corresponda.
- **CRÍTICO — fechas:** La propiedad `n.fecha` es de tipo `DATE` en Neo4j.
  - En `params`, la fecha debe ser un STRING ISO: `"YYYY-MM-DD"` (ej. `"2024-01-01"`).
  - En la consulta Cypher, DEBES envolver el parámetro con la función `date()`:
    `WHERE n.fecha >= date($desde) AND n.fecha <= date($hasta)`.
  - NUNCA compares `n.fecha >= $desde` directamente, porque compara DATE contra STRING y retorna 0 resultados.
  - Para extraer componentes de una fecha DATE, usa notación de punto (propiedad), NO funciones:
    - Año: `n.fecha.year` (NO `year(n.fecha)`)
    - Mes: `n.fecha.month` (NO `month(n.fecha)`)
    - Día: `n.fecha.day` (NO `day(n.fecha)`)
- Si `filtros_adicionales` contiene `"concepto": "cilindro_bomba"`, la consulta debe buscar la palabra "cilindro" en la descripción de la novedad:
  `WHERE toLower(n.descripcion) CONTAINS "cilindro"`. No restrinjas por categoría en ese caso, porque el concepto aparece tanto en "Atentado Terrorista" (explosionaron) como en "Hallazgo de Material" (no explosionaron).
- Si la intención es un ranking/listado de municipios (ej. "municipios con más..."), usa el patrón:
  `MATCH (m:MUNICIPIO)-[:CONTIENE*1..4]->(lugar)<-[:OCURRE_EN]-(n:NOVEDAD)` y agrupa por `m.nombre`. No filtres por un municipio específico.
- **CRÍTICO — tipo de nodo:** Para obtener el tipo/label de un nodo en Neo4j, usa la función `labels(n)` que devuelve una lista de strings. El primer elemento es el tipo principal: `labels(n)[0]` (NO `tipo(n)`).

Esquema:
{GRAPH_SCHEMA_FOR_LLM}
""".strip()


def _redactor_system_prompt() -> str:
    return """Eres el Agente 3 — Redactor de informes institucionales del sistema Vigía Cauca.

Entrada: resultados tabulares en JSON (datos devueltos por Neo4j) más el JSON de intención del Agente 1
(incluye perfil_usuario) y el rol del usuario en la plataforma.

Reglas obligatorias:
- Redacta solo con la información presente en los datos. No inventes cifras, fechas ni hechos.
- Si nivel_confianza en los datos es Preliminar o En verificación, dilo explícitamente; nunca presentes como confirmado.
- No reveles nombres de víctimas; si aparecen "Reservado" o "No identificado", respétalo.
- Si el usuario es Visitante y los datos no incluyen hechos privados (ya filtrados en consulta), no menciones fuentes internas.
- Tono: si perfil_usuario es "no_tecnico", lenguaje claro y cotidiano; si es "tecnico", puedes incluir nombres de lugares y datos precisos.
- Informe formal, sin mencionar IA, Cypher, agentes ni ingeniería.
- No hagas juicios de culpabilidad ni perfilés comunidades.
""".strip()


@dataclass
class ChatTurn:
    user_message: str
    answer: str
    cypher: str
    rows: list[dict[str, Any]]
    intencion_json: dict[str, Any] | None = None
    debug_trace: list[str] | None = None


class PipelineStageError(RuntimeError):
    """Error con contexto de etapa para depuración del pipeline."""

    def __init__(self, stage: str, message: str, debug_trace: list[str], original: Exception | None = None):
        super().__init__(f"[{stage}] {message}")
        self.stage = stage
        self.debug_trace = debug_trace
        self.original = original


class LocalGraphChat:
    """Pipeline: Intérprete → Consultor Cypher → Redactor (sin RAG)."""

    def __init__(
        self,
        graph_client: Neo4jGraphClient | None = None,
        ollama_client: OllamaClient | None = None,
    ) -> None:
        self.graph_client = graph_client or Neo4jGraphClient()
        self.ollama_client = ollama_client or OllamaClient()
        self.model_interpreter = MODEL_INTERPRETER
        self.model_consultant = MODEL_CONSULTANT
        self.model_redactor = MODEL_REDACTOR

    def check_connections(self) -> None:
        self.graph_client.ping()
        self.ollama_client.ping()

    def ask(
        self,
        question: str,
        *,
        perfil_ui: str | None = None,
        rol_usuario: str = "Operador",
        progress_callback: Callable[[str], None] | None = None,
    ) -> ChatTurn:
        debug_trace: list[str] = []
        t0 = time.perf_counter()

        def trace(msg: str) -> None:
            dt = time.perf_counter() - t0
            debug_trace.append(f"{dt:7.2f}s | {msg}")
            if progress_callback:
                progress_callback(msg)

        question = (question or "").strip()
        if not question:
            raise ValueError("La consulta no puede estar vacía.")

        trace("Inicio de consulta")
        schema_block = (
            f"{GRAPH_SCHEMA_FOR_LLM}\n\n"
            f"Ejemplos de patrones:\n{self.graph_client.examples_description()}"
        )

        try:
            trace(f"Agente 1 (Intérprete) usando modelo: {self.model_interpreter}")
            intencion = self._agente1_interpretar(question, schema_block)
            trace("Agente 1 completado")
        except Exception as exc:
            trace(f"Agente 1 falló ({exc}); activando fallback local")
            intencion = self._fallback_interpretacion(question)
            trace("Fallback local del Intérprete completado")

        # Unificar perfil: UI puede forzar; si no, el modelo propone en JSON
        perfil = (perfil_ui or intencion.get("perfil_usuario") or "no_tecnico").strip()
        if perfil not in ("tecnico", "no_tecnico"):
            perfil = "no_tecnico"
        intencion["perfil_usuario"] = perfil

        consulta_mejorada = intencion.get("consulta_mejorada")
        if consulta_mejorada:
            msg = (
                f"Tu consulta es un poco amplia. Prueba con esta versión más concreta:\n\n"
                f"**{consulta_mejorada}**\n\n"
                f"Si prefieres, escríbela en el chat y la ejecuto."
            )
            return ChatTurn(
                user_message=question,
                answer=msg,
                cypher="",
                rows=[],
                intencion_json=intencion,
                debug_trace=debug_trace,
            )

        try:
            trace(f"Agente 2 (Consultor) usando modelo: {self.model_consultant}")
            plan = self._agente2_cypher(question, intencion, rol_usuario)
            trace("Agente 2 completado")
        except Exception as exc:
            raise PipelineStageError(
                "Agente 2 — Consultor",
                str(exc),
                debug_trace,
                original=exc,
            ) from exc
        cypher = plan.get("cypher") or ""
        params = plan.get("params") or {}

        if not (cypher or "").strip():
            return ChatTurn(
                user_message=question,
                answer="No se pudo generar una consulta válida para tu pregunta. Reformula o reduce el alcance.",
                cypher="",
                rows=[],
                intencion_json=intencion,
                debug_trace=debug_trace,
            )

        try:
            trace("Neo4j execute_read_query")
            query_result = self.graph_client.execute_read_query(cypher, params)
            trace(f"Neo4j completado ({len(query_result.records)} filas)")
        except ValueError as exc:
            return ChatTurn(
                user_message=question,
                answer=f"No se pudo ejecutar la consulta de forma segura: {exc}",
                cypher=cypher,
                rows=[],
                intencion_json=intencion,
                debug_trace=debug_trace,
            )
        except Exception as exc:
            raise PipelineStageError(
                "Neo4j",
                str(exc),
                debug_trace,
                original=exc,
            ) from exc

        try:
            trace(f"Agente 3 (Redactor) usando modelo: {self.model_redactor}")
            answer = self._agente3_redactar(question, intencion, query_result, rol_usuario)
            trace("Agente 3 completado")
        except Exception as exc:
            raise PipelineStageError(
                "Agente 3 — Redactor",
                str(exc),
                debug_trace,
                original=exc,
            ) from exc

        trace("Consulta finalizada")
        return ChatTurn(
            user_message=question,
            answer=answer,
            cypher=query_result.cypher,
            rows=query_result.records,
            intencion_json=intencion,
            debug_trace=debug_trace,
        )

    def _agente1_interpretar(self, question: str, schema_block: str) -> dict[str, Any]:
        messages = [
            {"role": "system", "content": INTERPRETER_SYSTEM_PROMPT + "\n\n" + schema_block},
            {"role": "user", "content": f"Pregunta del usuario:\n{question}"},
        ]
        raw = self.ollama_client.chat_json(
            messages,
            model=self.model_interpreter,
            options={"num_predict": OLLAMA_NUM_PREDICT_JSON},
        )
        return self._normalize_intencion(raw)

    def _fallback_interpretacion(self, question: str) -> dict[str, Any]:
        """Fallback determinista para modelos que no entregan JSON en Agente 1."""
        q = question.strip()
        ql = q.lower()

        categoria = None
        if "homicid" in ql:
            categoria = "Homicidio"
        elif "hostig" in ql:
            categoria = "Hostigamiento"
        elif "dron" in ql:
            categoria = "Ataque con Dron"
        elif "secuest" in ql:
            categoria = "Secuestro"
        elif "protest" in ql or "bloqueo" in ql:
            categoria = "Acción de Protesta"
        elif "atentado" in ql:
            categoria = "Atentado Terrorista"
        elif "hallazgo" in ql:
            categoria = "Hallazgo de Material"

        # Filtros adicionales (conceptos cruzados que no son categorías exactas)
        filtros_adicionales: dict[str, Any] = {}
        if "cilindro" in ql or "cilindros" in ql:
            filtros_adicionales["concepto"] = "cilindro_bomba"

        if any(k in ql for k in ["cuánt", "cuanto", "cuantos", "total", "número", "numero"]):
            intencion = "conteo"
        elif any(k in ql for k in ["top", "ranking", "más", "mas"]):
            intencion = "ranking"
        elif any(k in ql for k in ["list", "muéstra", "muestra", "dame"]):
            intencion = "listado"
        else:
            intencion = "resumen"

        ubic_match = re.search(
            r"\b(popayán|popayan|toribío|toribio|corinto|buenos aires|jambaló|jambalo)\b",
            ql,
        )
        ubicacion = {"nombre": None, "nivel": None}
        if ubic_match:
            nombre = ubic_match.group(1)
            nombre = (
                nombre.replace("popayan", "Popayán")
                .replace("toribio", "Toribío")
                .replace("jambalo", "Jambaló")
            )
            ubicacion = {"nombre": nombre.title() if " " in nombre else nombre, "nivel": "MUNICIPIO"}

        periodo = {"desde": None, "hasta": None}
        year_match = re.search(r"\b(20\d{2})\b", ql)
        if year_match:
            yy = year_match.group(1)
            periodo = {"desde": f"{yy}-01-01", "hasta": f"{yy}-12-31"}
        elif "ayer" in ql:
            periodo = {"desde": None, "hasta": "ayer"}
        elif "hoy" in ql or "actual" in ql:
            periodo = {"desde": None, "hasta": "hoy"}
        elif "semana pasada" in ql:
            periodo = {"desde": "semana_pasada", "hasta": None}
        elif "este mes" in ql or "mes actual" in ql:
            periodo = {"desde": "este_mes", "hasta": None}
        elif "mes pasado" in ql:
            periodo = {"desde": "mes_pasado", "hasta": None}

        # No pedir aclaración de ubicación si la pregunta misma es sobre
        # listar/ranquear municipios (ej. "municipios con más...")
        es_consulta_de_municipios = bool(
            re.search(r"\b(municipios?\s+(con|de|en|que|donde)|top\s+\d+\s+municipios?)\b", ql)
        )
        # Detectar ranking por mes sin año específico
        es_ranking_por_mes_sin_ano = (
            intencion in {"ranking", "comparacion"}
            and ("mes" in ql or "month" in ql)
            and not year_match
        )

        # Una consulta es ambigua si:
        # 1. Es listado/ranking/conteo sin ubicación específica, o
        # 2. Es solo una categoría suelta sin intención clara (ej. "hostigamientos"), o
        # 3. Es una consulta muy genérica sin filtros (ej. "qué pasó", "novedades")
        es_ambigua = (
            (
                ubicacion["nombre"] is None
                and intencion in {"conteo", "ranking", "listado"}
            )
            or (
                intencion == "resumen"
                and categoria is not None
                and ubicacion["nombre"] is None
                and periodo["desde"] is None
                and periodo["hasta"] is None
            )
            or (
                intencion == "resumen"
                and categoria is None
                and any(k in ql for k in ["que paso", "novedades", "eventos", "sucedio", "paso"])
            )
        ) and not es_consulta_de_municipios

        consulta_mejorada = None
        if es_ranking_por_mes_sin_ano:
            consulta_mejorada = (
                f"¿De qué año te interesa consultar? Especifica el año para poder "
                f"comparar los meses. Por ejemplo: '{categoria.lower() if categoria else 'eventos'} en 2024'."
            )
        elif es_ambigua:
            # Construir sugerencia basada en la consulta original
            sugerencia = "Dime "
            if categoria:
                sugerencia += f"los {categoria.lower()}s"
            else:
                sugerencia += "los eventos de orden público"
            if year_match:
                sugerencia += f" de {year_match.group(1)}"
            else:
                sugerencia += " del último año"
            sugerencia += " en el departamento del Cauca."
            consulta_mejorada = sugerencia

        return self._normalize_intencion(
            {
                "intencion": intencion,
                "categoria": categoria,
                "ubicacion": ubicacion,
                "periodo": periodo,
                "perfil_usuario": "no_tecnico",
                "filtros_adicionales": filtros_adicionales,
                "consulta_mejorada": consulta_mejorada,
            }
        )

    @staticmethod
    def _normalize_intencion(data: dict[str, Any]) -> dict[str, Any]:
        out = dict(data)
        out.setdefault("intencion", "resumen")
        out.setdefault("categoria", None)
        out.setdefault("ubicacion", {"nombre": None, "nivel": None})
        out.setdefault("periodo", {"desde": None, "hasta": None})
        out.setdefault("perfil_usuario", "no_tecnico")
        out.setdefault("filtros_adicionales", {})
        out.setdefault("consulta_mejorada", None)
        # Retrocompatibilidad: eliminar campos antiguos si llegan de un LLM antiguo
        out.pop("aclaracion_requerida", None)
        out.pop("pregunta_aclaracion", None)
        return out

    @staticmethod
    def _resolve_temporal_references(intencion: dict[str, Any]) -> dict[str, Any]:
        """Resuelve referencias temporales relativas a fechas ISO concretas."""
        out = dict(intencion)
        periodo = dict(out.get("periodo") or {})
        hoy = date.today()

        def _resolve(val):
            if val == "hoy":
                return hoy.isoformat()
            if val == "ayer":
                return (hoy - timedelta(days=1)).isoformat()
            if val == "semana_pasada":
                # lunes de la semana pasada
                lunes_esta_semana = hoy - timedelta(days=hoy.weekday())
                return (lunes_esta_semana - timedelta(days=7)).isoformat()
            if val == "este_mes":
                return hoy.replace(day=1).isoformat()
            if val == "mes_pasado":
                if hoy.month == 1:
                    return hoy.replace(year=hoy.year - 1, month=12, day=1).isoformat()
                return hoy.replace(month=hoy.month - 1, day=1).isoformat()
            return val

        if periodo.get("desde"):
            periodo["desde"] = _resolve(periodo["desde"])
        if periodo.get("hasta"):
            periodo["hasta"] = _resolve(periodo["hasta"])

        out["periodo"] = periodo
        return out

    def _agente2_cypher(
        self,
        question: str,
        intencion: dict[str, Any],
        rol_usuario: str,
    ) -> dict[str, Any]:
        intencion = self._resolve_temporal_references(intencion)
        hoy = date.today().isoformat()
        payload = json.dumps(intencion, ensure_ascii=False)
        user_msg = (
            f"Pregunta original:\n{question}\n\n"
            f"JSON de intención (Agente 1):\n{payload}\n\n"
            f"rol_usuario: {rol_usuario}\n"
            f"fecha_hoy_iso: {hoy}\n\n"
            "Genera el JSON con cypher y params."
        )
        messages = [
            {"role": "system", "content": CONSULTANT_SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ]
        return self.ollama_client.chat_json(
            messages,
            model=self.model_consultant,
            options={"num_predict": OLLAMA_NUM_PREDICT_JSON},
        )

    def _agente3_redactar(
        self,
        question: str,
        intencion: dict[str, Any],
        query_result: QueryResult,
        rol_usuario: str,
    ) -> str:
        rows_json = json.dumps(query_result.records, ensure_ascii=False, indent=2, default=str)
        intent_json = json.dumps(intencion, ensure_ascii=False)
        user_msg = (
            f"Pregunta:\n{question}\n\n"
            f"JSON de intención:\n{intent_json}\n\n"
            f"Rol del usuario en la plataforma: {rol_usuario}\n\n"
            f"Datos de Neo4j (JSON):\n{rows_json}"
        )
        messages = [
            {"role": "system", "content": _redactor_system_prompt()},
            {"role": "user", "content": user_msg},
        ]
        return self.ollama_client.chat(
            messages,
            model=self.model_redactor,
            options={"num_predict": OLLAMA_NUM_PREDICT_TEXT},
        )
