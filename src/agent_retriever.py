"""
src/agent_retriever.py — Agente 1: Recuperador (RAG).

Recibe una consulta en lenguaje natural, la convierte en un vector semántico
y recupera los top-K fragmentos más relevantes del vector store.
"""

import os
from dataclasses import dataclass

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TOP_K, VECTOR_STORE_BACKEND
from src.vector_store import obtener_embedding


@dataclass
class DocumentoRecuperado:
    id:       str
    texto:    str
    score:    float
    metadata: dict


# ─── Recuperación desde ChromaDB ─────────────────────────────────────────────

def _recuperar_chroma(
    consulta: str,
    coleccion,
    top_k: int,
    filtros: dict | None,
) -> list[DocumentoRecuperado]:
    """Consulta ChromaDB y devuelve los top_k documentos más similares."""
    vector = obtener_embedding(consulta)

    kwargs = dict(
        query_embeddings=[vector],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )
    if filtros:
        kwargs["where"] = filtros

    resultado = coleccion.query(**kwargs)

    documentos = []
    for i in range(len(resultado["ids"][0])):
        documentos.append(DocumentoRecuperado(
            id=resultado["ids"][0][i],
            texto=resultado["documents"][0][i],
            score=1 - resultado["distances"][0][i],  # distancia coseno → similitud
            metadata=resultado["metadatas"][0][i],
        ))
    return documentos


# ─── Recuperación desde FAISS ─────────────────────────────────────────────────

def _recuperar_faiss(
    consulta: str,
    index,
    textos: list[str],
    top_k: int,
) -> list[DocumentoRecuperado]:
    """Consulta FAISS y devuelve los top_k documentos más similares."""
    import numpy as np
    import faiss

    vector = obtener_embedding(consulta)
    arr    = np.array([vector], dtype="float32")
    faiss.normalize_L2(arr)

    scores, indices = index.search(arr, top_k)

    documentos = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        documentos.append(DocumentoRecuperado(
            id=str(idx),
            texto=textos[idx],
            score=float(score),
            metadata={},
        ))
    return documentos


# ─── Interfaz pública del Agente 1 ───────────────────────────────────────────

class AgenteRecuperador:
    """
    Agente 1 — Recuperador semántico.

    Uso:
        agente = AgenteRecuperador(coleccion=chroma_collection)
        docs   = agente.recuperar("Top 3 municipios con más hechos en 2024")
    """

    def __init__(self, coleccion=None, index=None, textos: list[str] | None = None):
        """
        Parámetros
        ----------
        coleccion : chromadb.Collection | None
            Colección ChromaDB (si VECTOR_STORE_BACKEND == "chroma").
        index : faiss.Index | None
            Índice FAISS (si VECTOR_STORE_BACKEND == "faiss").
        textos : list[str] | None
            Lista de textos correspondientes al índice FAISS.
        """
        self.coleccion = coleccion
        self.index     = index
        self.textos    = textos or []

    def recuperar(
        self,
        consulta: str,
        top_k: int = TOP_K,
        filtros: dict | None = None,
    ) -> list[DocumentoRecuperado]:
        """
        Recupera los documentos más relevantes para la consulta dada.

        Parámetros
        ----------
        consulta : str
            Pregunta o instrucción en lenguaje natural (español).
        top_k : int
            Número de documentos a recuperar.
        filtros : dict | None
            Filtros de metadatos (solo ChromaDB). Ejemplo:
            {"municipio": "Toribío"} o {"semestre": "1"}.

        Retorna
        -------
        list[DocumentoRecuperado] ordenada por score descendente.
        """
        if not consulta or not consulta.strip():
            raise ValueError("La consulta no puede estar vacía.")

        if VECTOR_STORE_BACKEND == "chroma":
            if self.coleccion is None:
                raise RuntimeError("Colección ChromaDB no inicializada.")
            docs = _recuperar_chroma(consulta, self.coleccion, top_k, filtros)
        elif VECTOR_STORE_BACKEND == "faiss":
            if self.index is None:
                raise RuntimeError("Índice FAISS no inicializado.")
            docs = _recuperar_faiss(consulta, self.index, self.textos, top_k)
        else:
            raise ValueError(f"Backend no soportado: {VECTOR_STORE_BACKEND}")

        return sorted(docs, key=lambda d: d.score, reverse=True)

    def contexto_para_generador(self, docs: list[DocumentoRecuperado]) -> str:
        """
        Formatea los documentos recuperados como bloque de contexto
        listo para incluir en el prompt del Agente 2.
        """
        partes = []
        for i, doc in enumerate(docs, start=1):
            meta = doc.metadata
            encabezado = (
                f"[Documento {i}] "
                f"Fecha: {meta.get('fecha','?')} | "
                f"Municipio: {meta.get('municipio','?')} | "
                f"Categoría: {meta.get('categoria_hecho','?')} | "
                f"Score: {doc.score:.3f}"
            )
            partes.append(f"{encabezado}\n{doc.texto}")
        return "\n\n---\n\n".join(partes)
