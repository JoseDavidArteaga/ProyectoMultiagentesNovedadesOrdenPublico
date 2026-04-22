"""
src/agent_generator.py — Agente 2: Generador de reportes.

Recibe la consulta original + el contexto recuperado por el Agente 1 y
sintetiza un reporte institucional estructurado usando GPT-4.1.
Usa prompt engineering con instrucciones del sistema + ejemplos few-shot.
"""

import os
from openai import OpenAI

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OPENAI_API_KEY, GENERATOR_MODEL, GENERATOR_MAX_TOKENS, GENERATOR_TEMPERATURE


_client = OpenAI(api_key=OPENAI_API_KEY)


# ─── System prompt ────────────────────────────────────────────────────────────

_SYSTEM_PROMPT = """Eres un asistente especializado en análisis de seguridad y orden público para la
Secretaría de Gobierno del departamento del Cauca, Colombia.

Tu función es redactar reportes institucionales claros, precisos y bien estructurados para
el Gobernador del Cauca, basándote EXCLUSIVAMENTE en los documentos de contexto proporcionados.

REGLAS OBLIGATORIAS:
1. Responde siempre en español formal, con tono institucional y objetivo.
2. Utiliza ÚNICAMENTE la información presente en los documentos de contexto.
   No incorpores datos, cifras ni afirmaciones que no aparezcan en el contexto.
3. Si la información disponible es insuficiente para responder, indícalo explícitamente.
4. Estructura la respuesta con secciones claras: encabezado, desarrollo y conclusión o síntesis.
5. Trata con cuidado las expresiones de incertidumbre del dataset
   ("al parecer", "se presume", "según información sin verificar"):
   reprodúcelas sin presentarlas como hechos confirmados.
6. Los análisis deben orientarse a patrones territoriales y temporales agregados,
   nunca a señalar culpabilidad individual ni a perfilar comunidades específicas.
7. Cita al final los documentos fuente que respaldan cada sección del reporte
   (usa el número de documento indicado en el contexto).

FORMATO DEL REPORTE:
---
**REPORTE DE ORDEN PÚBLICO — DEPARTAMENTO DEL CAUCA**
**Consulta:** [consulta original]
**Fecha de generación:** [fecha actual]

**1. Resumen ejecutivo**
[2-3 oraciones con los hallazgos principales]

**2. Análisis detallado**
[desarrollo organizado por municipio, período o categoría según corresponda]

**3. Síntesis y observaciones**
[patrones identificados, consideraciones relevantes]

**Fuentes consultadas:** [lista de documentos referenciados]
---
"""


# ─── Ejemplos few-shot ────────────────────────────────────────────────────────

_FEW_SHOT = [
    {
        "role": "user",
        "content": (
            "CONSULTA: ¿Cuáles fueron los principales hechos de orden público en Toribío durante el primer semestre de 2024?\n\n"
            "CONTEXTO:\n"
            "[Documento 1] Fecha: 2024-03-15 | Municipio: Toribío | Categoría: HOSTIGAMIENTO | Score: 0.921\n"
            "Fecha: 2024-03-15. Municipio: Toribío. Categoría del hecho: HOSTIGAMIENTO. "
            "Descripción: Al parecer, integrantes de grupos armados hostigan puesto de policía. "
            "Afectaciones: Sin heridos reportados, afectación a la movilidad.\n\n"
            "[Documento 2] Fecha: 2024-05-22 | Municipio: Toribío | Categoría: ENFRENTAMIENTO | Score: 0.887\n"
            "Fecha: 2024-05-22. Municipio: Toribío. Categoría del hecho: ENFRENTAMIENTO. "
            "Descripción: Enfrentamiento armado en zona rural. "
            "Afectaciones: 2 heridos civiles, desplazamiento de 15 familias."
        ),
    },
    {
        "role": "assistant",
        "content": (
            "---\n"
            "**REPORTE DE ORDEN PÚBLICO — DEPARTAMENTO DEL CAUCA**\n"
            "**Consulta:** Principales hechos de orden público en Toribío, primer semestre 2024\n\n"
            "**1. Resumen ejecutivo**\n"
            "Durante el primer semestre de 2024 se registraron en el municipio de Toribío al menos dos eventos significativos de orden público: "
            "un hostigamiento a instalaciones policiales y un enfrentamiento armado en zona rural que afectó a población civil.\n\n"
            "**2. Análisis detallado**\n"
            "- *15 de marzo de 2024 — Hostigamiento:* Al parecer, integrantes de grupos armados no identificados hostigan el puesto de policía. "
            "No se reportaron heridos; sin embargo, se registró afectación a la movilidad en la zona.\n"
            "- *22 de mayo de 2024 — Enfrentamiento armado:* Se presentó un enfrentamiento en zona rural del municipio. "
            "El hecho dejó dos heridos civiles y generó el desplazamiento de aproximadamente 15 familias.\n\n"
            "**3. Síntesis y observaciones**\n"
            "Los eventos documentados muestran una presión sostenida sobre el municipio de Toribío durante el primer semestre, "
            "con impacto directo en la población civil (heridos y desplazamiento). "
            "Las expresiones de incertidumbre presentes en el registro del 15 de marzo requieren verificación adicional.\n\n"
            "**Fuentes consultadas:** Documento 1, Documento 2\n"
            "---"
        ),
    },
]


# ─── Agente Generador ─────────────────────────────────────────────────────────

class AgenteGenerador:
    """
    Agente 2 — Generador de reportes institucionales.

    Uso:
        agente = AgenteGenerador()
        reporte = agente.generar(consulta="...", contexto="...")
    """

    def generar(self, consulta: str, contexto: str) -> str:
        """
        Genera el reporte a partir de la consulta y el contexto recuperado.

        Parámetros
        ----------
        consulta : str
            Consulta original del usuario en lenguaje natural.
        contexto : str
            Bloque de texto con los documentos recuperados por el Agente 1.

        Retorna
        -------
        str : Reporte generado en formato institucional.
        """
        if not consulta.strip():
            raise ValueError("La consulta no puede estar vacía.")
        if not contexto.strip():
            raise ValueError("El contexto no puede estar vacío.")

        user_message = (
            f"CONSULTA: {consulta}\n\n"
            f"CONTEXTO:\n{contexto}"
        )

        mensajes = [
            {"role": "system",    "content": _SYSTEM_PROMPT},
            *_FEW_SHOT,
            {"role": "user",      "content": user_message},
        ]

        respuesta = _client.chat.completions.create(
            model=GENERATOR_MODEL,
            messages=mensajes,
            max_tokens=GENERATOR_MAX_TOKENS,
            temperature=GENERATOR_TEMPERATURE,
        )

        return respuesta.choices[0].message.content.strip()
