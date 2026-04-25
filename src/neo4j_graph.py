"""Acceso read-only a Neo4j para consultas del chat local."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from neo4j import GraphDatabase

from config import NEO4J_DATABASE, NEO4J_MAX_RESULTS, NEO4J_PASSWORD, NEO4J_URI, NEO4J_USERNAME


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
        return (
            "Nodos principales: NOVEDAD, ACTOR, USUARIO, MUNICIPIO, COMUNA, BARRIO, "
            "CORREGIMIENTO, VEREDA, SECTOR, TERRITORIO_INDIGENA, VICTIMA, AFECTACION_HUMANA.\n"
            "Relaciones clave: (ACTOR)-[:PARTICIPA_EN]->(NOVEDAD), "
            "(USUARIO)-[:REPORTA]->(NOVEDAD), (NOVEDAD)-[:OCURRE_EN]->(ubicacion), "
            "(NOVEDAD)-[:GENERA]->(AFECTACION_HUMANA), (ubicacion_padre)-[:CONTIENE]->(ubicacion_hija).\n"
            "Propiedades frecuentes de NOVEDAD: id, categoria, descripcion, fecha, hora, "
            "nivel_confianza, visibilidad, fuente, creado_en.\n"
            "Propiedades frecuentes de ACTOR: id, nombre, tipo.\n"
            "Propiedades frecuentes de MUNICIPIO y nodos de lugar: id, nombre."
        )

    def examples_description(self) -> str:
        return (
            "Ejemplo 1: MATCH (m:MUNICIPIO {nombre: $municipio})-[:CONTIENE*1..4]->(lugar)<-[:OCURRE_EN]-(n:NOVEDAD) "
            "RETURN n.id AS id, n.categoria AS categoria, n.fecha AS fecha, labels(lugar)[0] AS nivel, lugar.nombre AS lugar "
            "ORDER BY n.fecha DESC LIMIT 10\n"
            "Ejemplo 2: MATCH (m:MUNICIPIO)-[:CONTIENE*1..4]->(lugar)<-[:OCURRE_EN]-(n:NOVEDAD) "
            "RETURN m.nombre AS municipio, count(DISTINCT n) AS total_novedades ORDER BY total_novedades DESC LIMIT 5\n"
            "Ejemplo 3: MATCH (a:ACTOR)-[:PARTICIPA_EN]->(n:NOVEDAD)-[:OCURRE_EN]->(lugar) "
            "RETURN a.nombre AS actor, n.categoria AS categoria, lugar.nombre AS lugar, n.fecha AS fecha "
            "ORDER BY n.fecha DESC LIMIT 10"
        )

    @staticmethod
    def _validate_query(cypher: str) -> str:
        text = (cypher or "").strip().rstrip(";")
        if not text:
            raise ValueError("La consulta Cypher está vacía.")

        upper = text.upper()
        if "RETURN" not in upper:
            raise ValueError("La consulta debe ser de solo lectura y terminar en RETURN.")

        for keyword in FORBIDDEN_KEYWORDS:
            if keyword in upper:
                raise ValueError(f"La consulta contiene una operación no permitida: {keyword}.")

        return text