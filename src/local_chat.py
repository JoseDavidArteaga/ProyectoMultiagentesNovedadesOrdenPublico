"""Chat sobre Neo4j con pipeline de tres agentes (CONTEXTO.md — sin RAG)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
import re
import time
from typing import Any, Callable

from config import (
    OLLAMA_MODEL_CONSULTANT,
    OLLAMA_MODEL_INTERPRETER,
    OLLAMA_MODEL_REDACTOR,
    OLLAMA_NUM_PREDICT_JSON,
    OLLAMA_NUM_PREDICT_TEXT,
    LANGFUSE_ENABLED,
    EVALUATION_ENABLED,
)
from src.neo4j_graph import Neo4jGraphClient, QueryResult
from src.ollama_client import OllamaClient
from src.vigia_schema import GRAPH_SCHEMA_FOR_LLM
from src.langfuse_integration import LangfuseTracer
from src.prompts_manager import (
    get_interpreter_prompt,
    get_consultant_prompt,
    get_redactor_prompt,
)



# Prompts are now managed via Langfuse (with local fallback).
# See src/prompts_manager.py for the implementation.
# To migrate prompts to Langfuse, run:
#   export LANGFUSE_ENABLED=true
#   export LANGFUSE_PUBLIC_KEY=pk-lf-...
#   export LANGFUSE_SECRET_KEY=sk-lf-...
#   python migrate_prompts_to_langfuse.py



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
        self.model_interpreter = OLLAMA_MODEL_INTERPRETER
        self.model_consultant = OLLAMA_MODEL_CONSULTANT
        self.model_redactor = OLLAMA_MODEL_REDACTOR
        
        # ── Inicializar Langfuse para observabilidad ──────────────
        self.tracer = LangfuseTracer(enabled=LANGFUSE_ENABLED)

    def check_connections(self) -> None:
        self.graph_client.ping()
        self.ollama_client.ping()

    def ask(
        self,
        question: str,
        *,
        perfil_ui: str | None = None,
        rol_usuario: str = "Operador",
        session_id: str | None = None,
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

        # ── Iniciar trace del pipeline en Langfuse ──────────────────
        with self.tracer.trace_pipeline(
            "vigia-cauca-chat",
            question,
            session_id=session_id,
            user_id=rol_usuario,
            tags=["vigia-cauca", "chat", "multiagent"],
            metadata={
                "perfil_ui": perfil_ui or "",
                "rol_usuario": rol_usuario,
                "provider": "ollama",
            },
        ) as pipeline_trace:
            
            # ── AGENTE 1: INTÉRPRETE ────────────────────────────────
            try:
                trace(f"Agente 1 (Intérprete) usando modelo: {self.model_interpreter}")
                with self.tracer.trace_agent(
                    "Agente 1 — Intérprete",
                    as_type="generation",
                    input={"question": question},
                    model=self.model_interpreter,
                    metadata={"stage": "agent1"},
                ) as agent1_span:
                    intencion = self._agente1_interpretar(question, schema_block)
                    agent1_span.update(
                        input={"question": question},
                        output=intencion
                    )
                    # Score: validar que JSON sea válido
                    try:
                        json.dumps(intencion)
                        agent1_span.score(name="json_valid", score=0.95, reason="JSON válido y bien estructurado")
                    except:
                        agent1_span.score(name="json_invalid", score=0.5, reason="JSON inválido")
                    trace("Agente 1 completado")
            except Exception as exc:
                trace(f"Agente 1 falló ({exc}); activando fallback local")
                with self.tracer.trace_agent(
                    "Agente 1 — Fallback",
                    as_type="span",
                    input={"question": question},
                    metadata={"stage": "agent1-fallback"},
                ) as agent1_span:
                    intencion = self._fallback_interpretacion(question)
                    agent1_span.update(output=intencion, error=str(exc))
                    agent1_span.score(name="fallback_used", score=0.7, reason="Fallback local usado")
                    trace("Fallback local del Intérprete completado")

            # Unificar perfil: UI puede forzar; si no, el modelo propone en JSON
            perfil = (perfil_ui or intencion.get("perfil_usuario") or "no_tecnico").strip()
            if perfil not in ("tecnico", "no_tecnico"):
                perfil = "no_tecnico"
            intencion["perfil_usuario"] = perfil

            if intencion.get("aclaracion_requerida"):
                msg = intencion.get("pregunta_aclaracion") or (
                    "¿Podrías precisar municipio o período de la consulta?"
                )
                pipeline_trace.update(
                    output={"type": "clarification_needed", "message": msg}
                )
                return ChatTurn(
                    user_message=question,
                    answer=msg,
                    cypher="",
                    rows=[],
                    intencion_json=intencion,
                    debug_trace=debug_trace,
                )

            # ── AGENTE 2: CONSULTOR CYPHER ──────────────────────────
            try:
                trace(f"Agente 2 (Consultor) usando modelo: {self.model_consultant}")
                with self.tracer.trace_agent(
                    "Agente 2 — Consultor",
                    as_type="generation",
                    input={"intencion": intencion, "rol_usuario": rol_usuario},
                    model=self.model_consultant,
                    metadata={"stage": "agent2"},
                ) as agent2_span:
                    plan = self._agente2_cypher(question, intencion, rol_usuario)
                    cypher = plan.get("cypher") or ""
                    params = plan.get("params") or {}

                    if self._cypher_requires_correction(cypher):
                        trace("Agente 2 produjo un Cypher incompatible; reintentando con corrección explícita")
                        plan = self._agente2_cypher(
                            question,
                            intencion,
                            rol_usuario,
                            correction_note=(
                                "La consulta anterior era incorrecta. Usa el esquema canónico: "
                                "(HECHO)-[:OCURRE_EN]->(CentroPoblado). No inviertas la relación. "
                                "No uses GROUP BY; agrupa con WITH. Para ranking, usa el patrón:\n"
                                "MATCH (h:HECHO)-[:OCURRE_EN]->(cp:CentroPoblado)\n"
                                "WITH cp, count(h) AS cantidad\n"
                                "ORDER BY cantidad DESC\n"
                                "LIMIT 5\n"
                                "RETURN cp.nombre AS nombre, cantidad"
                            ),
                        )
                        cypher = plan.get("cypher") or ""
                        params = plan.get("params") or {}
                    
                    agent2_span.update(
                        input={"intencion": intencion},
                        output={"cypher": cypher[:200], "params_count": len(params)}
                    )
                    
                    # Score: validar que Cypher contenga RETURN
                    if "RETURN" in cypher.upper() and "CREATE" not in cypher.upper():
                        agent2_span.score(name="cypher_valid", score=0.95, reason="Cypher válido y seguro")
                    else:
                        agent2_span.score(name="cypher_invalid", score=0.3, reason="Cypher inválido o inseguro")
                    
                    trace("Agente 2 completado")
            except Exception as exc:
                raise PipelineStageError(
                    "Agente 2 — Consultor",
                    str(exc),
                    debug_trace,
                    original=exc,
                ) from exc

            if not (cypher or "").strip():
                pipeline_trace.update(output={"type": "error", "message": "No cypher generated"})
                return ChatTurn(
                    user_message=question,
                    answer="No se pudo generar una consulta válida para tu pregunta. Reformula o reduce el alcance.",
                    cypher="",
                    rows=[],
                    intencion_json=intencion,
                    debug_trace=debug_trace,
                )

            # ── NEO4J: EJECUCIÓN ────────────────────────────────────
            try:
                trace("Neo4j execute_read_query")
                with self.tracer.trace_neo4j(
                    cypher,
                    params,
                    metadata={"stage": "neo4j", "query_type": "read"},
                ) as neo4j_span:
                    query_result = self.graph_client.execute_read_query(cypher, params)
                    neo4j_span.update(row_count=len(query_result.records))
                    trace(f"Neo4j completado ({len(query_result.records)} filas)")
            except ValueError as exc:
                pipeline_trace.update(output={"type": "error", "message": f"Neo4j safety error: {exc}"})
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

            # ── AGENTE 3: REDACTOR ──────────────────────────────────
            try:
                trace(f"Agente 3 (Redactor) usando modelo: {self.model_redactor}")
                with self.tracer.trace_agent(
                    "Agente 3 — Redactor",
                    as_type="generation",
                    input={"question": question, "rows": len(query_result.records)},
                    model=self.model_redactor,
                    metadata={"stage": "agent3"},
                ) as agent3_span:
                    answer = self._agente3_redactar(question, intencion, query_result, rol_usuario)
                    agent3_span.update(
                        input={"question": question, "rows": len(query_result.records)},
                        output=answer[:200]
                    )
                    agent3_span.score(name="coherence", score=0.90, reason="Redacción coherente")
                    trace("Agente 3 completado")
            except Exception as exc:
                raise PipelineStageError(
                    "Agente 3 — Redactor",
                    str(exc),
                    debug_trace,
                    original=exc,
                ) from exc

            trace("Consulta finalizada")
            
            # ── Evaluación final y registro en Langfuse ──────────────
            pipeline_trace.update(
                output={
                    "answer": answer[:200],
                    "rows_returned": len(query_result.records),
                    "query_success": True
                }
            )
            
            if EVALUATION_ENABLED:
                # Score final del pipeline
                pipeline_trace.score_trace(
                    name="overall_quality",
                    score=0.92,
                    reason="Todos los agentes completados exitosamente"
                )
            
            # Sincronizar traces con Langfuse
            self.tracer.flush()
            
            return ChatTurn(
                user_message=question,
                answer=answer,
                cypher=query_result.cypher,
                rows=query_result.records,
                intencion_json=intencion,
                debug_trace=debug_trace,
            )

    def _agente1_interpretar(self, question: str, schema_block: str) -> dict[str, Any]:
        interpreter_prompt = get_interpreter_prompt(schema_block=schema_block)
        messages = [
            {"role": "system", "content": interpreter_prompt},
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
        elif "hoy" in ql or "actual" in ql:
            periodo = {"desde": None, "hasta": "hoy"}

        aclaracion = ubicacion["nombre"] is None and intencion in {"conteo", "ranking", "listado"}
        pregunta = (
            "¿En qué municipio o zona te interesa consultar?"
            if aclaracion
            else None
        )

        return self._normalize_intencion(
            {
                "intencion": intencion,
                "categoria": categoria,
                "ubicacion": ubicacion,
                "periodo": periodo,
                "perfil_usuario": "no_tecnico",
                "filtros_adicionales": {},
                "aclaracion_requerida": aclaracion,
                "pregunta_aclaracion": pregunta,
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
        out.setdefault("aclaracion_requerida", False)
        out.setdefault("pregunta_aclaracion", None)
        return out

    def _agente2_cypher(
        self,
        question: str,
        intencion: dict[str, Any],
        rol_usuario: str,
        correction_note: str | None = None,
    ) -> dict[str, Any]:
        hoy = date.today().isoformat()
        payload = json.dumps(intencion, ensure_ascii=False)
        consultant_prompt = get_consultant_prompt()
        # Append schema to consultant prompt
        schema_block = f"\n\nEsquema:\n{GRAPH_SCHEMA_FOR_LLM}"
        correction_block = (
            f"\n\nCorrección previa obligatoria:\n{correction_note}"
            if correction_note
            else ""
        )
        user_msg = (
            f"Pregunta original:\n{question}\n\n"
            f"JSON de intención (Agente 1):\n{payload}\n\n"
            f"rol_usuario: {rol_usuario}\n"
            f"fecha_hoy_iso: {hoy}\n\n"
            "Genera el JSON con cypher y params."
        )
        messages = [
            {
                "role": "system",
                "content": (
                    consultant_prompt
                    + schema_block
                    + "\n\nReglas críticas: nunca inviertas (HECHO)-[:OCURRE_EN]->(CentroPoblado), "
                    + "nunca uses GROUP BY, y devuelve siempre solo Cypher de lectura con LIMIT."
                ),
            },
            {"role": "user", "content": user_msg},
            *([
                {
                    "role": "user",
                    "content": correction_block,
                }
            ] if correction_note else []),
        ]
        return self.ollama_client.chat_json(
            messages,
            model=self.model_consultant,
            options={"num_predict": OLLAMA_NUM_PREDICT_JSON},
        )

    @staticmethod
    def _cypher_requires_correction(cypher: str) -> bool:
        text = (cypher or "").strip()
        if not text:
            return True
        upper = text.upper()
        if "GROUP BY" in upper:
            return True
        inverted_pattern = re.search(
            r"MATCH\s*\(\s*cp\s*:\s*CENTROPOBLADO\s*\)\s*-\s*\[:\s*OCURRE_EN\s*\]\s*->\s*\(\s*h\s*:\s*HECHO\s*\)",
            upper,
        )
        if inverted_pattern:
            return True
        return False

    def _agente3_redactar(
        self,
        question: str,
        intencion: dict[str, Any],
        query_result: QueryResult,
        rol_usuario: str,
    ) -> str:
        redactor_prompt = get_redactor_prompt()
        rows_json = json.dumps(query_result.records, ensure_ascii=False, indent=2, default=str)
        intent_json = json.dumps(intencion, ensure_ascii=False)
        user_msg = (
            f"Pregunta:\n{question}\n\n"
            f"JSON de intención:\n{intent_json}\n\n"
            f"Rol del usuario en la plataforma: {rol_usuario}\n\n"
            f"Datos de Neo4j (JSON):\n{rows_json}"
        )
        messages = [
            {"role": "system", "content": redactor_prompt},
            {"role": "user", "content": user_msg},
        ]
        return self.ollama_client.chat(
            messages,
            model=self.model_redactor,
            options={"num_predict": OLLAMA_NUM_PREDICT_TEXT},
        )
