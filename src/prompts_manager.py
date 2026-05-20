"""Prompt management integration with Langfuse.

This module provides functions to fetch prompts from Langfuse with fallback to local definitions.
Prompts are managed via the Langfuse API for versioning, testing, and production deployment.
"""

from __future__ import annotations

import json
from typing import Any

from config import LANGFUSE_ENABLED, LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY


# ── Langfuse client (initialized lazily) ─────────────────────────────────────
_langfuse_client: Any = None


def _get_langfuse_client() -> Any:
    """Get or initialize Langfuse client for prompt management."""
    global _langfuse_client
    
    if _langfuse_client is not None:
        return _langfuse_client
    
    if not (LANGFUSE_ENABLED and LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY):
        return None
    
    try:
        from langfuse import get_client
        _langfuse_client = get_client()
        return _langfuse_client
    except Exception as e:
        print(f"⚠️  Failed to initialize Langfuse client for prompts: {e}")
        return None


def get_prompt_from_langfuse(prompt_name: str, prompt_type: str = "chat") -> Any:
    """Fetch a prompt from Langfuse by name.
    
    Args:
        prompt_name: Name of the prompt in Langfuse (e.g., 'vigia-interpreter', 'vigia-consultant')
        prompt_type: Type of prompt ('chat' or 'text'); defaults to 'chat'
    
    Returns:
        Langfuse prompt object if found, None otherwise.
    """
    client = _get_langfuse_client()
    if client is None:
        return None
    
    try:
        prompt = client.get_prompt(prompt_name, type=prompt_type)
        return prompt
    except Exception as e:
        print(f"⚠️  Failed to fetch prompt '{prompt_name}' from Langfuse: {e}")
        return None


def compile_prompt_template(prompt_obj: Any, **variables: Any) -> str | list[dict[str, str]]:
    """Compile a Langfuse prompt template with variables.
    
    Args:
        prompt_obj: Langfuse prompt object
        **variables: Variables to interpolate into the template
    
    Returns:
        Compiled prompt (string for text prompts, list of dicts for chat prompts)
    """
    if prompt_obj is None:
        return None
    
    try:
        compiled = prompt_obj.compile(**variables)
        return compiled
    except Exception as e:
        print(f"⚠️  Failed to compile prompt: {e}")
        return None


def get_interpreter_prompt(schema_block: str = "") -> str:
    """Get interpreter agent system prompt with fallback to local definition.
    
    Args:
        schema_block: Schema information to append to the prompt
    
    Returns:
        System prompt string
    """
    # Try to fetch from Langfuse
    prompt_obj = get_prompt_from_langfuse("vigia-interpreter", prompt_type="text")
    if prompt_obj is not None:
        try:
            compiled = prompt_obj.compile(schema_block=schema_block or "")
            return compiled
        except Exception:
            pass
    
    # Fallback to local definition
    return _LOCAL_INTERPRETER_PROMPT + ("\n\n" + schema_block if schema_block else "")


def get_consultant_prompt() -> str:
    """Get consultant agent system prompt with fallback to local definition.
    
    Returns:
        System prompt string (may include schema template)
    """
    # Try to fetch from Langfuse
    prompt_obj = get_prompt_from_langfuse("vigia-consultant", prompt_type="text")
    if prompt_obj is not None:
        try:
            # Note: schema_block is typically injected at call-time
            compiled = prompt_obj.compile(schema_block="")
            return compiled
        except Exception:
            pass
    
    # Fallback to local definition
    return _LOCAL_CONSULTANT_PROMPT


def get_redactor_prompt() -> str:
    """Get redactor agent system prompt with fallback to local definition.
    
    Returns:
        System prompt string
    """
    # Try to fetch from Langfuse
    prompt_obj = get_prompt_from_langfuse("vigia-redactor", prompt_type="text")
    if prompt_obj is not None:
        try:
            compiled = prompt_obj.compile()
            return compiled
        except Exception:
            pass
    
    # Fallback to local definition
    return _LOCAL_REDACTOR_PROMPT


# ── Local prompt definitions (fallback when Langfuse unavailable) ─────────────

_LOCAL_INTERPRETER_PROMPT = """Eres el Agente 1 — Intérprete del sistema Vigía Cauca.

Tu tarea es analizar la pregunta del usuario en español y devolver UN SOLO objeto JSON válido
(sin markdown, sin texto adicional) con la forma exacta:

{
  "intencion": "<conteo|listado|resumen|comparacion|detalle|ranking>",
    "categoria": "<valor ENUM de Categoria.nombre o null>",
  "ubicacion": { "nombre": "<texto o null>", "nivel": "<MUNICIPIO|CORREGIMIENTO|VEREDA|SECTOR|BARRIO|COMUNA|TERRITORIO_INDIGENA|null>" },
  "periodo": { "desde": "<YYYY-MM-DD o null>", "hasta": "<YYYY-MM-DD|hoy|null>" },
  "perfil_usuario": "<tecnico|no_tecnico>",
  "filtros_adicionales": { },
  "aclaracion_requerida": <true|false>,
  "pregunta_aclaracion": "<string o null>"
}

Reglas:
- Conoces el modelo de datos Neo4j (Vigía Cauca v2). Usa solo ENUMs y nombres del esquema provisto abajo.
- Si la intención es ambigua o falta el alcance geográfico cuando es necesario, pon aclaracion_requerida: true
  y una pregunta_aclaracion concreta en español. NO inventes municipios.
- Si la pregunta es saludo o no requiere datos del grafo, devuelve JSON válido con intencion "resumen",
  aclaracion_requerida: false, y categoria null.
- perfil_usuario: si el usuario pide datos técnicos (veredas, cortes exactos), "tecnico"; si no, "no_tecnico".
""".strip()

_LOCAL_CONSULTANT_PROMPT = """Eres el Agente 2 — Consultor Cypher para Neo4j (Vigía Cauca).

Recibirás la pregunta original del usuario, un JSON de intención del Agente 1, el rol del usuario en la plataforma,
y la fecha de hoy (ISO) para interpretar "hoy" en filtros de fecha.

Debes responder con UN SOLO objeto JSON:
{
  "cypher": "<consulta Cypher de solo lectura>",
  "params": { }
}

Reglas de seguridad (obligatorias):
- Solo cláusulas: MATCH, OPTIONAL MATCH, RETURN, WHERE, WITH, ORDER BY, LIMIT, UNWIND, CASE.
- PROHIBIDO: CREATE, MERGE, DELETE, SET, REMOVE, DROP, LOAD CSV, FOREACH, CALL dbms.*, CALL apoc.*.
- Toda consulta debe tener LIMIT (máximo 100).
- No uses GROUP BY: en Cypher el agrupamiento se hace con WITH.
- Esquema canónico: (HECHO)-[:OCURRE_EN]->(CentroPoblado), (HECHO)-[:EN_MES]->(MES),
    (HECHO)-[:EN_AÑO]->(AÑO), (HECHO)-[:ES_DE]->(Categoria), (HECHO)-[:GENERA {cantidad}]->(Afectacion),
    (CentroPoblado)-[:PERTENECE_A]->(Municipio).
- Para filtrar por municipio usa la propiedad del centro poblado:
    MATCH (cp:CentroPoblado {nombre_municipio: $municipio})<-[:OCURRE_EN]-(h:HECHO)
- Si necesitas conteos por categoría o municipio, agrupa con WITH y luego usa ORDER BY y LIMIT.
- Usa parámetros ($municipio, $categoria, fechas como date('YYYY-MM-DD')) en params cuando corresponda.
""".strip()

_LOCAL_REDACTOR_PROMPT = """Eres el Agente 3 — Redactor de informes institucionales del sistema Vigía Cauca.

Entrada: resultados tabulares en JSON (datos devueltos por Neo4j) más el JSON de intención del Agente 1
(incluye perfil_usuario) y el rol del usuario en la plataforma.

Reglas obligatorias:
- Redacta solo con la información presente en los datos. No inventes cifras, fechas ni hechos.
- Si nivel_confianza en los datos es Preliminar o En verificación, dilo explícitamente; nunca presentes como confirmado.
- No reveles nombres de víctimas; si aparecen "Reservado" o "No identificado", respétalo.
- Si el usuario es Visitante y los datos no incluyen hechos privados (ya filtrados en consulta), no menciones fuentes internas.
- Tono: si perfil_usuario es "no_tecnico", lenguaje claro y cotidiano; si es "tecnico", puedes incluir nombres de lugares y datos precisos.
- Informe formal, sin mencionar IA, Cypher, agentes ni ingeniería.
- No hagas juicios de culpabilidad ni perfilés comunidades.
""".strip()


__all__ = [
    "get_prompt_from_langfuse",
    "compile_prompt_template",
    "get_interpreter_prompt",
    "get_consultant_prompt",
    "get_redactor_prompt",
]
