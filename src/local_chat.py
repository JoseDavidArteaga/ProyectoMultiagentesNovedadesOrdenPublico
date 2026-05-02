"""Chat sobre Neo4j con pipeline de tres agentes (CONTEXTO.md — sin RAG)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from typing import Any

from config import (
    OLLAMA_MODEL_CONSULTANT,
    OLLAMA_MODEL_INTERPRETER,
    OLLAMA_MODEL_REDACTOR,
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
  "periodo": { "desde": "<YYYY-MM-DD o null>", "hasta": "<YYYY-MM-DD|hoy|null>" },
  "perfil_usuario": "<tecnico|no_tecnico>",
  "filtros_adicionales": { },
  "aclaracion_requerida": <true|false>,
  "pregunta_aclaracion": "<string o null>"
}

Reglas:
- Conoces el modelo de datos Neo4j (Vigía Cauca v2). Usa solo ENUMs y nombres del esquema provisto abajo.
- Si la intención es ambigua o falta el alcance geográfico cuando es necesario, pon aclaracion_requerida: true
  y una pregunta_aclaracion concreta en español. NO inventes municipios.
- Si la pregunta es saludo o no requiere datos del grafo, devuelve JSON válido con intencion "resumen",
  aclaracion_requerida: false, y categoria null.
- perfil_usuario: si el usuario pide datos técnicos (veredas, cortes exactos), "tecnico"; si no, "no_tecnico".
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
- Usa parámetros ($nombre, fechas como date('YYYY-MM-DD')) en params cuando corresponda.

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


class LocalGraphChat:
    """Pipeline: Intérprete → Consultor Cypher → Redactor (sin RAG)."""

    def __init__(
        self,
        graph_client: Neo4jGraphClient | None = None,
        ollama_client: OllamaClient | None = None,
    ) -> None:
        self.graph_client = graph_client or Neo4jGraphClient()
        self.ollama_client = ollama_client or OllamaClient()
        self.model_interpreter = OLLAMA_MODEL_INTERPRETER
        self.model_consultant = OLLAMA_MODEL_CONSULTANT
        self.model_redactor = OLLAMA_MODEL_REDACTOR

    def check_connections(self) -> None:
        self.graph_client.ping()
        self.ollama_client.ping()

    def ask(
        self,
        question: str,
        *,
        perfil_ui: str | None = None,
        rol_usuario: str = "Operador",
    ) -> ChatTurn:
        question = (question or "").strip()
        if not question:
            raise ValueError("La consulta no puede estar vacía.")

        schema_block = (
            f"{GRAPH_SCHEMA_FOR_LLM}\n\n"
            f"Ejemplos de patrones:\n{self.graph_client.examples_description()}"
        )

        intencion = self._agente1_interpretar(question, schema_block)

        # Unificar perfil: UI puede forzar; si no, el modelo propone en JSON
        perfil = (perfil_ui or intencion.get("perfil_usuario") or "no_tecnico").strip()
        if perfil not in ("tecnico", "no_tecnico"):
            perfil = "no_tecnico"
        intencion["perfil_usuario"] = perfil

        if intencion.get("aclaracion_requerida"):
            msg = intencion.get("pregunta_aclaracion") or (
                "¿Podrías precisar municipio o período de la consulta?"
            )
            return ChatTurn(
                user_message=question,
                answer=msg,
                cypher="",
                rows=[],
                intencion_json=intencion,
            )

        plan = self._agente2_cypher(question, intencion, rol_usuario)
        cypher = plan.get("cypher") or ""
        params = plan.get("params") or {}

        if not (cypher or "").strip():
            return ChatTurn(
                user_message=question,
                answer="No se pudo generar una consulta válida para tu pregunta. Reformula o reduce el alcance.",
                cypher="",
                rows=[],
                intencion_json=intencion,
            )

        try:
            query_result = self.graph_client.execute_read_query(cypher, params)
        except ValueError as exc:
            return ChatTurn(
                user_message=question,
                answer=f"No se pudo ejecutar la consulta de forma segura: {exc}",
                cypher=cypher,
                rows=[],
                intencion_json=intencion,
            )

        answer = self._agente3_redactar(question, intencion, query_result, rol_usuario)
        return ChatTurn(
            user_message=question,
            answer=answer,
            cypher=query_result.cypher,
            rows=query_result.records,
            intencion_json=intencion,
        )

    def _agente1_interpretar(self, question: str, schema_block: str) -> dict[str, Any]:
        messages = [
            {"role": "system", "content": INTERPRETER_SYSTEM_PROMPT + "\n\n" + schema_block},
            {"role": "user", "content": f"Pregunta del usuario:\n{question}"},
        ]
        raw = self.ollama_client.chat_json(messages, model=self.model_interpreter)
        return self._normalize_intencion(raw)

    @staticmethod
    def _normalize_intencion(data: dict[str, Any]) -> dict[str, Any]:
        out = dict(data)
        out.setdefault("intencion", "resumen")
        out.setdefault("categoria", None)
        out.setdefault("ubicacion", {"nombre": None, "nivel": None})
        out.setdefault("periodo", {"desde": None, "hasta": None})
        out.setdefault("perfil_usuario", "no_tecnico")
        out.setdefault("filtros_adicionales", {})
        out.setdefault("aclaracion_requerida", False)
        out.setdefault("pregunta_aclaracion", None)
        return out

    def _agente2_cypher(
        self,
        question: str,
        intencion: dict[str, Any],
        rol_usuario: str,
    ) -> dict[str, Any]:
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
        return self.ollama_client.chat_json(messages, model=self.model_consultant)

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
        return self.ollama_client.chat(messages, model=self.model_redactor)
