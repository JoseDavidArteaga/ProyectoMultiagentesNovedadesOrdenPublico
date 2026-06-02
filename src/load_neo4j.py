"""Carga un archivo .cypher en la base local de Neo4j."""

from __future__ import annotations

from pathlib import Path

from neo4j import GraphDatabase

from config import (
    NEO4J_DATABASE,
    NEO4J_PASSWORD,
    NEO4J_SEED_FILE,
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_DATA_FILE_1,
    NEO4J_DATA_FILE_2,
    NEO4J_DATA_FILE_3,
)


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
    # Mantener compatibilidad: esta función delega en load_cypher_file
    return load_cypher_file(seed_file)


def load_cypher_file(file_path: str) -> int:
    """Carga y ejecuta todas las sentencias Cypher en `file_path`.

    Devuelve el número de sentencias ejecutadas. Si el archivo no existe,
    devuelve 0 (sin levantar excepción) para permitir continuar con otros archivos.
    """
    path = Path(file_path)
    if not path.exists():
        print(f"Aviso: no existe el archivo Cypher: {path}")
        return 0

    text = path.read_text(encoding="utf-8")
    statements = split_cypher_statements(text)
    if not statements:
        print(f"Aviso: no se encontraron sentencias en {path}")
        return 0

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    try:
        with driver.session(database=NEO4J_DATABASE) as session:
            for statement in statements:
                session.run(statement).consume()
    finally:
        driver.close()

    return len(statements)


if __name__ == "__main__":
    total = 0

    # Ejecutar archivo seed principal
    total += load_seed_file()

    # Ejecutar archivos de datos adicionales definidos en config
    data_files = [NEO4J_DATA_FILE_1, NEO4J_DATA_FILE_2, NEO4J_DATA_FILE_3]
    for df in data_files:
        if not df:
            continue
        executed = load_cypher_file(df)
        total += executed

    print(f"Carga completada. Sentencias ejecutadas: {total}")