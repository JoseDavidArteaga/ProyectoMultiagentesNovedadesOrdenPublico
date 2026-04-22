"""
src/vector_store.py — Construcción e indexación del almacén vectorial.

Convierte cada registro del dataset procesado en un documento de texto
enriquecido, lo embebe con text-embedding-3-large (OpenAI) y lo almacena
en ChromaDB (opción por defecto) o FAISS.
"""

import os
import pandas as pd
from openai import OpenAI
from tqdm import tqdm

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    OPENAI_API_KEY,
    EMBEDDING_MODEL,
    VECTOR_STORE_BACKEND,
    CHROMA_PERSIST_DIR,
    PROCESSED_DATA_FILE,
)


# ─── Cliente OpenAI ───────────────────────────────────────────────────────────
_client = OpenAI(api_key=OPENAI_API_KEY)


# ─── Construcción del texto de cada documento ────────────────────────────────

def _row_a_documento(row: pd.Series) -> str:
    """
    Convierte una fila del dataset en texto legible para el embedding.
    El formato es deliberadamente narrativo para mejorar la recuperación
    semántica ante consultas en lenguaje natural.
    """
    flags = []
    if row.get("uso_drones"):     flags.append("uso de drones")
    if row.get("uso_explosivos"): flags.append("uso de explosivos")
    if row.get("hay_bloqueo"):    flags.append("bloqueo vial")
    flags_str = "; ".join(flags) if flags else "ninguno"

    return (
        f"Fecha: {row.get('fecha', 'desconocida')}. "
        f"Municipio: {row.get('municipio', 'desconocido')}. "
        f"Categoría del hecho: {row.get('categoria_hecho', 'OTRO')}. "
        f"Descripción: {row.get('hechos', '')}. "
        f"Afectaciones: {row.get('afectaciones', '')}. "
        f"Factores especiales: {flags_str}."
    )


# ─── Función de embedding ─────────────────────────────────────────────────────

def obtener_embedding(texto: str) -> list[float]:
    """Llama a la API de OpenAI y devuelve el vector de embedding."""
    respuesta = _client.embeddings.create(
        input=texto,
        model=EMBEDDING_MODEL,
    )
    return respuesta.data[0].embedding


# ─── ChromaDB ─────────────────────────────────────────────────────────────────

def construir_chroma(df: pd.DataFrame) -> "chromadb.Collection":
    """Indexa todos los documentos en una colección ChromaDB persistente."""
    import chromadb

    cliente_chroma = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    coleccion = cliente_chroma.get_or_create_collection(
        name="orden_publico_cauca",
        metadata={"hnsw:space": "cosine"},
    )

    # Solo indexar registros no presentes aún
    ids_existentes = set(coleccion.get(include=[])["ids"])

    ids, textos, embeddings, metadatos = [], [], [], []

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Indexando en ChromaDB"):
        doc_id = str(row["id"])
        if doc_id in ids_existentes:
            continue

        texto = _row_a_documento(row)
        emb   = obtener_embedding(texto)

        ids.append(doc_id)
        textos.append(texto)
        embeddings.append(emb)
        metadatos.append({
            "fecha":           str(row.get("fecha", "")),
            "municipio":       str(row.get("municipio", "")),
            "categoria_hecho": str(row.get("categoria_hecho", "")),
            "semestre":        str(row.get("semestre", "")),
            "trimestre":       str(row.get("trimestre", "")),
            "mes":             str(row.get("mes", "")),
        })

        # Upsert en lotes de 100 para no sobrepasar límites de la API
        if len(ids) == 100:
            coleccion.add(ids=ids, documents=textos, embeddings=embeddings, metadatas=metadatos)
            ids, textos, embeddings, metadatos = [], [], [], []

    if ids:
        coleccion.add(ids=ids, documents=textos, embeddings=embeddings, metadatas=metadatos)

    print(f"[VectorStore] ChromaDB lista — {coleccion.count():,} documentos indexados.")
    return coleccion


def cargar_chroma() -> "chromadb.Collection":
    """Carga una colección ChromaDB ya existente (sin reindexar)."""
    import chromadb
    cliente_chroma = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    return cliente_chroma.get_collection("orden_publico_cauca")


# ─── FAISS (alternativa) ──────────────────────────────────────────────────────

def construir_faiss(df: pd.DataFrame):
    """
    Construye un índice FAISS con los embeddings del dataset.
    Retorna (index, docs_list) donde docs_list[i] es el texto del documento i.
    """
    import faiss
    import numpy as np

    textos     = [_row_a_documento(row) for _, row in tqdm(df.iterrows(), total=len(df), desc="Generando embeddings")]
    embeddings = [obtener_embedding(t) for t in tqdm(textos, desc="Indexando en FAISS")]

    matrix = np.array(embeddings, dtype="float32")
    faiss.normalize_L2(matrix)

    dim   = matrix.shape[1]
    index = faiss.IndexFlatIP(dim)   # producto interno ≡ coseno con vectores normalizados
    index.add(matrix)

    print(f"[VectorStore] FAISS listo — {index.ntotal:,} documentos indexados.")
    return index, textos


# ─── Punto de entrada ─────────────────────────────────────────────────────────

def construir_vector_store(ruta_csv: str = PROCESSED_DATA_FILE):
    """
    Carga el dataset procesado y construye el vector store según
    VECTOR_STORE_BACKEND definido en config.py.
    """
    df = pd.read_csv(ruta_csv, dtype=str)
    print(f"[VectorStore] {len(df):,} registros cargados desde {ruta_csv}")

    if VECTOR_STORE_BACKEND == "chroma":
        return construir_chroma(df)
    elif VECTOR_STORE_BACKEND == "faiss":
        return construir_faiss(df)
    else:
        raise ValueError(f"Backend no soportado: {VECTOR_STORE_BACKEND}")
