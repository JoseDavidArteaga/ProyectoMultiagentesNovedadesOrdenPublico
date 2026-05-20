"""Acceso read-only a Neo4j para consultas del chat local."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from neo4j import GraphDatabase

from config import NEO4J_DATABASE, NEO4J_MAX_RESULTS, NEO4J_PASSWORD, NEO4J_URI, NEO4J_USERNAME
from src.vigia_schema import GRAPH_SCHEMA_FOR_LLM


FORBIDDEN_KEYWORDS = {
    "CREATE",
    "MERGE",
    "DELETE",
    "DETACH",
    "SET",
    "REMOVE",
    "DROP",
    "LOAD CSV",
    "FOREACH",
    "CALL DBMS",
    "CALL APOC",
}


@dataclass
class QueryResult:
    cypher: str
    records: list[dict[str, Any]]


class Neo4jGraphClient:
    def __init__(
        self,
        uri: str = NEO4J_URI,
        username: str = NEO4J_USERNAME,
        password: str = NEO4J_PASSWORD,
        database: str = NEO4J_DATABASE,
        max_results: int = NEO4J_MAX_RESULTS,
    ) -> None:
        self.database = database
        self.max_results = max_results
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self) -> None:
        self.driver.close()

    def ping(self) -> None:
        with self.driver.session(database=self.database) as session:
            session.run("RETURN 1 AS ok").single()

    def execute_read_query(self, cypher: str, params: dict[str, Any] | None = None) -> QueryResult:
        normalized = self._validate_query(cypher)
        with self.driver.session(database=self.database) as session:
            result = session.run(normalized, params or {})
            records = [dict(record) for record in result][: self.max_results]
        return QueryResult(cypher=normalized, records=records)

    def schema_description(self) -> str:
        """Resumen canónico Vigía Cauca v2 (CONTEXTO.md)."""
        return GRAPH_SCHEMA_FOR_LLM

    def examples_description(self) -> str:
        return (
            "Ejemplo 1: MATCH (h:HECHO)-[:OCURRE_EN]->(cp:CentroPoblado {nombre_municipio: $municipio}) "
            "RETURN h.id AS id, h.fecha AS fecha, h.descripcion AS descripcion, cp.nombre AS lugar, cp.nombre_municipio AS municipio "
            "ORDER BY h.fecha DESC LIMIT 10\n"
            "Ejemplo 2: MATCH (h:HECHO)-[:ES_DE]->(cat:Categoria) "
            "RETURN cat.nombre AS categoria, count(h) AS total ORDER BY total DESC LIMIT 5\n"
            "Ejemplo 3: MATCH (h:HECHO)-[:GENERA]->(af:Afectacion) "
            "RETURN h.descripcion AS descripcion, af.nombre AS afectacion, count(*) AS cantidad "
            "ORDER BY cantidad DESC LIMIT 10"
        )

    @staticmethod
    def _validate_query(cypher: str) -> str:
        text = (cypher or "").strip().rstrip(";")
        if not text:
            raise ValueError("La consulta Cypher está vacía.")

        upper = text.upper()
        if "RETURN" not in upper:
            raise ValueError("La consulta debe ser de solo lectura y terminar en RETURN.")

        if "GROUP BY" in upper:
            raise ValueError("Cypher no usa GROUP BY; agrupa con WITH antes de ORDER BY y RETURN.")

        if "MATCH (CP:CENTROPOBLADO)-[:OCURRE_EN]->(H:HECHO)" in upper:
            raise ValueError(
                "La dirección de OCURRE_EN está invertida. Usa MATCH (h:HECHO)-[:OCURRE_EN]->(cp:CentroPoblado)."
            )

        for keyword in FORBIDDEN_KEYWORDS:
            if keyword in upper:
                raise ValueError(f"La consulta contiene una operación no permitida: {keyword}.")

        return text