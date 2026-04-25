"""Servicio de chat local sobre Neo4j usando Ollama."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from src.neo4j_graph import Neo4jGraphClient, QueryResult
from src.ollama_client import OllamaClient


QUERY_SYSTEM_PROMPT = """
Eres un asistente que traduce preguntas en español a Cypher para Neo4j.

Debes responder SIEMPRE con JSON válido con esta forma:
{
  "needs_query": true,
  "cypher": "MATCH ... RETURN ... LIMIT 10",
  "params": {"municipio": "Toribío"},
  "reason": "breve explicación"
}

Si la pregunta no requiere consultar Neo4j, responde:
{
  "needs_query": false,
  "cypher": "",
  "params": {},
  "reason": "..."
}

Reglas:
- Genera solo consultas de lectura.
- Nunca uses CREATE, MERGE, DELETE, SET, REMOVE, DROP, LOAD CSV, FOREACH.
- Usa parámetros cuando filtres por nombre o categoría.
- Incluye LIMIT cuando la consulta pueda devolver muchos resultados.
- Si preguntas por un municipio, recorre la jerarquía con [:CONTIENE*1..4].
- Si preguntas por actores, usa (a:ACTOR)-[:PARTICIPA_EN]->(n:NOVEDAD).
- Si preguntas por ubicación, usa (n:NOVEDAD)-[:OCURRE_EN]->(lugar).
""".strip()


ANSWER_SYSTEM_PROMPT = """
Eres un analista de orden público del Cauca. Responde en español claro y directo.

Usa solo los resultados tabulares suministrados por el sistema. Si no hay datos,
indica que no se encontraron resultados. No inventes registros ni cifras.
""".strip()


@dataclass
class ChatTurn:
    user_message: str
    answer: str
    cypher: str
    rows: list[dict[str, Any]]


class LocalGraphChat:
    def __init__(self, graph_client: Neo4jGraphClient | None = None, ollama_client: OllamaClient | None = None) -> None:
        self.graph_client = graph_client or Neo4jGraphClient()
        self.ollama_client = ollama_client or OllamaClient()

    def check_connections(self) -> None:
        self.graph_client.ping()
        self.ollama_client.ping()

    def ask(self, question: str) -> ChatTurn:
        question = (question or "").strip()
        if not question:
            raise ValueError("La consulta no puede estar vacía.")

        query_plan = self._plan_query(question)
        if not query_plan.get("needs_query", True):
            answer = self._answer_without_query(question, query_plan.get("reason", ""))
            return ChatTurn(user_message=question, answer=answer, cypher="", rows=[])

        query_result = self.graph_client.execute_read_query(
            query_plan.get("cypher", ""),
            query_plan.get("params", {}),
        )
        answer = self._synthesize_answer(question, query_result)
        return ChatTurn(
            user_message=question,
            answer=answer,
            cypher=query_result.cypher,
            rows=query_result.records,
        )

    def _plan_query(self, question: str) -> dict[str, Any]:
        messages = [
            {"role": "system", "content": QUERY_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    "Esquema del grafo:\n"
                    f"{self.graph_client.schema_description()}\n\n"
                    "Patrones de consulta útiles:\n"
                    f"{self.graph_client.examples_description()}\n\n"
                    f"Pregunta del usuario: {question}"
                ),
            },
        ]
        return self.ollama_client.chat_json(messages)

    def _answer_without_query(self, question: str, reason: str) -> str:
        messages = [
            {"role": "system", "content": ANSWER_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Pregunta: {question}\n"
                    f"Contexto adicional: {reason}\n"
                    "Responde sin citar una consulta a la base, y aclara el alcance si aplica."
                ),
            },
        ]
        return self.ollama_client.chat(messages)

    def _synthesize_answer(self, question: str, query_result: QueryResult) -> str:
        rows_json = json.dumps(query_result.records, ensure_ascii=False, indent=2, default=str)
        messages = [
            {"role": "system", "content": ANSWER_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Pregunta: {question}\n\n"
                    f"Cypher ejecutado:\n{query_result.cypher}\n\n"
                    f"Resultados:\n{rows_json}\n\n"
                    "Resume la respuesta para un usuario no técnico. Si hay varias filas, organiza el resultado en viñetas."
                ),
            },
        ]
        return self.ollama_client.chat(messages)