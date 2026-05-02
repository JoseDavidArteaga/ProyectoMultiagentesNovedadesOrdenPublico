"""
src/pipeline.py — Orquestador histórico basado en RAG + OpenAI (recuperador / generador / verificador).

La aplicación Streamlit y el flujo descrito en CONTEXTO.md usan **Neo4j + Ollama** sin embeddings:
ver `src/local_chat.py` (Intérprete → Consultor Cypher → Redactor).

Este módulo se mantiene por si necesitas experimentos con vector store y GPT; no es la ruta principal de Vigía Cauca.
"""

import os
import time
from dataclasses import dataclass

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import TOP_K
from src.agent_retriever import AgenteRecuperador, DocumentoRecuperado
from src.agent_generator import AgenteGenerador
from src.agent_verifier import AgenteVerificador, ResultadoVerificacion


# ─── Resultado del pipeline ───────────────────────────────────────────────────

@dataclass
class ResultadoPipeline:
    consulta:               str
    documentos_recuperados: list[DocumentoRecuperado]
    reporte_inicial:        str
    verificacion:           ResultadoVerificacion
    reporte_final:          str          # reporte corregido por el verificador
    tiempo_total_seg:       float


# ─── Pipeline ─────────────────────────────────────────────────────────────────

class Pipeline:
    """
    Orquestador del sistema RAG multiagente.

    Uso básico:
        pipeline = Pipeline(coleccion=chroma_collection)
        resultado = pipeline.ejecutar("¿Qué municipios tuvieron más hechos en 2024?")
        print(resultado.reporte_final)
    """

    def __init__(
        self,
        coleccion=None,
        index=None,
        textos: list[str] | None = None,
        top_k: int = TOP_K,
        verbose: bool = True,
    ):
        self.recuperador = AgenteRecuperador(
            coleccion=coleccion,
            index=index,
            textos=textos,
        )
        self.generador   = AgenteGenerador()
        self.verificador = AgenteVerificador()
        self.top_k       = top_k
        self.verbose     = verbose

    def ejecutar(
        self,
        consulta: str,
        filtros: dict | None = None,
    ) -> ResultadoPipeline:
        """
        Ejecuta el pipeline completo para una consulta.

        Parámetros
        ----------
        consulta : str
            Consulta en lenguaje natural (español).
        filtros : dict | None
            Filtros opcionales de metadatos para el recuperador (solo ChromaDB).
            Ejemplo: {"municipio": "Toribío"} o {"semestre": "1"}.

        Retorna
        -------
        ResultadoPipeline con todos los artefactos intermedios y el reporte final.
        """
        t0 = time.time()
        self._log(f"\n{'='*60}")
        self._log(f"CONSULTA: {consulta}")
        self._log(f"{'='*60}")

        # ── Agente 1: Recuperación ────────────────────────────────────────────
        self._log("\n[Agente 1 — Recuperador] Buscando documentos relevantes...")
        docs = self.recuperador.recuperar(consulta, top_k=self.top_k, filtros=filtros)
        self._log(f"  {len(docs)} documentos recuperados.")
        for d in docs:
            self._log(f"  • [{d.metadata.get('fecha','?')}] {d.metadata.get('municipio','?')} "
                      f"| {d.metadata.get('categoria_hecho','?')} | score={d.score:.3f}")

        contexto = self.recuperador.contexto_para_generador(docs)

        # ── Agente 2: Generación ──────────────────────────────────────────────
        self._log("\n[Agente 2 — Generador] Redactando reporte...")
        reporte_inicial = self.generador.generar(consulta=consulta, contexto=contexto)
        self._log("  Reporte generado.")

        # ── Agente 3: Verificación ────────────────────────────────────────────
        self._log("\n[Agente 3 — Verificador] Validando fidelidad del reporte...")
        verificacion = self.verificador.verificar(reporte=reporte_inicial, contexto=contexto)
        self._log(self.verificador.resumen(verificacion))

        reporte_final = verificacion.reporte_corregido or reporte_inicial
        t_total = time.time() - t0
        self._log(f"\nPipeline completado en {t_total:.1f} segundos.")

        return ResultadoPipeline(
            consulta=consulta,
            documentos_recuperados=docs,
            reporte_inicial=reporte_inicial,
            verificacion=verificacion,
            reporte_final=reporte_final,
            tiempo_total_seg=t_total,
        )

    def _log(self, mensaje: str) -> None:
        if self.verbose:
            print(mensaje)
