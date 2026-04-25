"""Carga un archivo .cypher en la base local de Neo4j."""

from __future__ import annotations

from pathlib import Path

from neo4j import GraphDatabase

from config import NEO4J_DATABASE, NEO4J_PASSWORD, NEO4J_SEED_FILE, NEO4J_URI, NEO4J_USERNAME


def split_cypher_statements(text: str) -> list[str]:
    statements: list[str] = []
    buffer: list[str] = []

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("//"):
            continue

        buffer.append(line)
        current = "\n".join(buffer).strip()
        if current.endswith(";"):
            statement = current[:-1].strip()
            if statement:
                statements.append(statement)
            buffer = []

    tail = "\n".join(buffer).strip()
    if tail:
        statements.append(tail)

    return statements


def load_seed_file(seed_file: str = NEO4J_SEED_FILE) -> int:
    path = Path(seed_file)
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo Cypher: {path}")

    statements = split_cypher_statements(path.read_text(encoding="utf-8"))
    if not statements:
        raise ValueError(f"No se encontraron sentencias en {path}")

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    try:
        with driver.session(database=NEO4J_DATABASE) as session:
            for statement in statements:
                session.run(statement).consume()
    finally:
        driver.close()

    return len(statements)


if __name__ == "__main__":
    total = load_seed_file()
    print(f"Carga completada. Sentencias ejecutadas: {total}")