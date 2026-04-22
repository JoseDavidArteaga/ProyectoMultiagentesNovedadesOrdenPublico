"""
src/agent_verifier.py — Agente 3: Verificador de fidelidad.

Evalúa el reporte generado por el Agente 2 contra los documentos recuperados.
Detecta afirmaciones no respaldadas (alucinaciones) y calcula un
Faithfulness Score.  Usa GPT-4o-mini por suficiencia y eficiencia de costo.
"""

import os
import json
import re
from dataclasses import dataclass, field

from openai import OpenAI

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    OPENAI_API_KEY,
    VERIFIER_MODEL,
    VERIFIER_MAX_TOKENS,
    VERIFIER_TEMPERATURE,
    FAITHFULNESS_THRESHOLD,
)


_client = OpenAI(api_key=OPENAI_API_KEY)


# ─── Estructura de resultado ──────────────────────────────────────────────────

@dataclass
class ResultadoVerificacion:
    faithfulness_score: float           # [0.0 – 1.0]
    aprobado: bool                      # score >= FAITHFULNESS_THRESHOLD
    afirmaciones_total: int
    afirmaciones_respaldadas: int
    alucinaciones: list[str]            # frases no respaldadas por el contexto
    reporte_corregido: str              # versión revisada con correcciones
    razonamiento: str = field(default="")


# ─── System prompt del verificador ───────────────────────────────────────────

_SYSTEM_PROMPT_VERIFICADOR = """Eres un auditor especializado en verificación de hechos para reportes de seguridad pública.

Tu tarea es evaluar si el reporte generado está completamente respaldado por los documentos
de contexto proporcionados. NUNCA uses conocimiento externo; juzga SOLO con base en los documentos.

PROCESO DE VERIFICACIÓN:
1. Identifica cada afirmación fáctica del reporte (fechas, municipios, cifras, eventos).
2. Para cada afirmación, determina si está respaldada explícitamente en el contexto.
3. Clasifica las afirmaciones no respaldadas como posibles alucinaciones.
4. Calcula el Faithfulness Score = afirmaciones_respaldadas / total_afirmaciones.
5. Proporciona una versión corregida del reporte donde las alucinaciones se eliminan
   o se marcan como "no verificado en los documentos consultados".

RESPONDE EXCLUSIVAMENTE con un objeto JSON válido con esta estructura:
{
  "afirmaciones_total": <int>,
  "afirmaciones_respaldadas": <int>,
  "faithfulness_score": <float entre 0.0 y 1.0>,
  "alucinaciones": ["<frase no respaldada 1>", ...],
  "reporte_corregido": "<texto completo del reporte corregido>",
  "razonamiento": "<explicación breve del proceso de verificación>"
}
"""


# ─── Agente Verificador ───────────────────────────────────────────────────────

class AgenteVerificador:
    """
    Agente 3 — Verificador de fidelidad.

    Uso:
        agente = AgenteVerificador()
        resultado = agente.verificar(reporte="...", contexto="...")
    """

    def verificar(self, reporte: str, contexto: str) -> ResultadoVerificacion:
        """
        Verifica que el reporte esté respaldado por el contexto.

        Parámetros
        ----------
        reporte : str
            Reporte generado por el Agente 2.
        contexto : str
            Bloque de documentos recuperados usados para generar el reporte.

        Retorna
        -------
        ResultadoVerificacion con el score, alucinaciones y reporte corregido.
        """
        if not reporte.strip() or not contexto.strip():
            raise ValueError("El reporte y el contexto no pueden estar vacíos.")

        user_message = (
            f"DOCUMENTOS DE CONTEXTO:\n{contexto}\n\n"
            f"REPORTE A VERIFICAR:\n{reporte}"
        )

        respuesta = _client.chat.completions.create(
            model=VERIFIER_MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT_VERIFICADOR},
                {"role": "user",   "content": user_message},
            ],
            max_tokens=VERIFIER_MAX_TOKENS,
            temperature=VERIFIER_TEMPERATURE,
            response_format={"type": "json_object"},
        )

        raw = respuesta.choices[0].message.content.strip()
        datos = self._parsear_respuesta(raw)

        score = float(datos.get("faithfulness_score", 0.0))
        score = max(0.0, min(1.0, score))   # clamping defensivo

        return ResultadoVerificacion(
            faithfulness_score=score,
            aprobado=score >= FAITHFULNESS_THRESHOLD,
            afirmaciones_total=int(datos.get("afirmaciones_total", 0)),
            afirmaciones_respaldadas=int(datos.get("afirmaciones_respaldadas", 0)),
            alucinaciones=datos.get("alucinaciones", []),
            reporte_corregido=datos.get("reporte_corregido", reporte),
            razonamiento=datos.get("razonamiento", ""),
        )

    @staticmethod
    def _parsear_respuesta(raw: str) -> dict:
        """Intenta parsear JSON; en caso de fallo extrae lo que pueda."""
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # Intento de rescate: buscar bloque JSON dentro del texto
            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except json.JSONDecodeError:
                    pass
            return {
                "afirmaciones_total": 0,
                "afirmaciones_respaldadas": 0,
                "faithfulness_score": 0.0,
                "alucinaciones": [],
                "reporte_corregido": "",
                "razonamiento": f"Error al parsear la respuesta del verificador: {raw[:200]}",
            }

    def resumen(self, resultado: ResultadoVerificacion) -> str:
        """Devuelve un resumen legible del resultado de la verificación."""
        estado = "APROBADO ✓" if resultado.aprobado else "REQUIERE REVISIÓN ✗"
        lineas = [
            f"─── Verificación de Fidelidad ───────────────────────",
            f"Estado:              {estado}",
            f"Faithfulness Score:  {resultado.faithfulness_score:.2f} (umbral: {FAITHFULNESS_THRESHOLD})",
            f"Afirmaciones total:  {resultado.afirmaciones_total}",
            f"Afirmaciones válidas:{resultado.afirmaciones_respaldadas}",
        ]
        if resultado.alucinaciones:
            lineas.append(f"Posibles alucinaciones ({len(resultado.alucinaciones)}):")
            for al in resultado.alucinaciones:
                lineas.append(f"  • {al}")
        lineas.append(f"─────────────────────────────────────────────────────")
        return "\n".join(lineas)
