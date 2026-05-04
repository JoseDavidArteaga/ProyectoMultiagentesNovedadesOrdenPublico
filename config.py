"""
config.py — Configuración centralizada del sistema multiagente.
Carga las variables de entorno desde un archivo .env (local) o desde los
Secrets de Google Colab.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # carga .env si existe (entorno local)


# ─── Proveedor LLM ────────────────────────────────────────────────────────────
# "ollama" (local) o "groq" (cloud)
LLM_PROVIDER: str = os.environ.get("LLM_PROVIDER", "ollama").strip().lower()

# ─── Ollama local (Vigía Cauca — pipeline de 3 agentes, ver CONTEXTO.md) ─────
OLLAMA_BASE_URL: str = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
# Retrocompatibilidad: si solo defines OLLAMA_CHAT_MODEL, los tres agentes lo usan (p. ej. RAM < 16 GB).
OLLAMA_CHAT_MODEL: str = os.environ.get("OLLAMA_CHAT_MODEL", "qwen3.5:9b")
OLLAMA_MODEL_INTERPRETER: str = os.environ.get("OLLAMA_MODEL_INTERPRETER", OLLAMA_CHAT_MODEL)
# Consultor es el más exigente (Cypher); por defecto 27b si no se define (CONTEXTO §9).
OLLAMA_MODEL_CONSULTANT: str = os.environ.get("OLLAMA_MODEL_CONSULTANT", "qwen3.5:27b")
OLLAMA_MODEL_REDACTOR: str = os.environ.get("OLLAMA_MODEL_REDACTOR", OLLAMA_CHAT_MODEL)
OLLAMA_TEMPERATURE: float = float(os.environ.get("OLLAMA_TEMPERATURE", "0.2"))
OLLAMA_TIMEOUT_SECONDS: int = int(os.environ.get("OLLAMA_TIMEOUT_SECONDS", "300"))
OLLAMA_NUM_PREDICT_JSON: int = int(os.environ.get("OLLAMA_NUM_PREDICT_JSON", "220"))
OLLAMA_NUM_PREDICT_TEXT: int = int(os.environ.get("OLLAMA_NUM_PREDICT_TEXT", "420"))

# ─── Groq (API compatible con OpenAI) ────────────────────────────────────────
GROQ_API_KEY: str = os.environ.get("GROQ_API_KEY", "")
GROQ_BASE_URL: str = os.environ.get("GROQ_BASE_URL", "https://api.groq.com/openai/v1")

# ─── Neo4j local ─────────────────────────────────────────────────────────────
NEO4J_URI: str = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME: str = os.environ.get("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD: str = os.environ.get("NEO4J_PASSWORD", "neo4j2026")
NEO4J_DATABASE: str = os.environ.get("NEO4J_DATABASE", "neo4j")
NEO4J_MAX_RESULTS: int = int(os.environ.get("NEO4J_MAX_RESULTS", "100"))

# ─── Datos ────────────────────────────────────────────────────────────────────
RAW_DATA_DIR: str = "data/raw"
NEO4J_SEED_FILE: str = os.environ.get("NEO4J_SEED_FILE", "data/raw/vigia_cauca_neo4j.cypher")

# ─── Municipios del Cauca (lista de referencia para Fuzzy Matching) ───────────
MUNICIPIOS_CAUCA: list[str] = [
    "Popayán", "Almaguer", "Argelia", "Balboa", "Bolívar", "Buenos Aires",
    "Cajibío", "Caldono", "Caloto", "Coconuco", "Corinto", "El Tambo",
    "Florencia", "Guachené", "Guapi", "Inzá", "Jambaló", "La Sierra",
    "La Vega", "López de Micay", "Mercaderes", "Miranda", "Morales",
    "Padilla", "Páez", "Patía", "Piamonte", "Piendamó", "Puerto Tejada",
    "Puracé", "Rosas", "San Sebastián", "Santa Rosa", "Santander de Quilichao",
    "Silvia", "Sotará", "Suárez", "Sucre", "Timbío", "Timbiquí", "Toribío",
    "Totoró", "Villa Rica",
]

# ─── Categorías HECHO en Neo4j (CONTEXTO §3.1 — valores en la propiedad categoria)
CATEGORIAS_HECHO_NEO4J: list[str] = [
    "Enfrentamiento",
    "Hostigamiento",
    "Atentado Terrorista",
    "Ataque con Dron",
    "Homicidio",
    "Secuestro",
    "Retén Ilegal",
    "Reclutamiento Ilícito",
    "Acción de Protesta",
    "Hallazgo de Material",
    "Otro",
]

# ─── Langfuse (Observabilidad y evaluación de agentes) ──────────────────────
LANGFUSE_ENABLED: bool = os.environ.get("LANGFUSE_ENABLED", "false").lower() == "true"
# IMPORTANT: Do not store Langfuse keys in the repository. Set these via environment variables or a local .env file.
LANGFUSE_PUBLIC_KEY: str = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
LANGFUSE_SECRET_KEY: str = os.environ.get("LANGFUSE_SECRET_KEY", "")
# Default host can point to cloud or a self-hosted instance. Leave empty to use SDK default.
LANGFUSE_HOST: str = os.environ.get("LANGFUSE_HOST", "https://us.cloud.langfuse.com")

# Configuración de evaluación
EVALUATION_ENABLED: bool = os.environ.get("EVALUATION_ENABLED", "true").lower() == "true"
EVALUATION_MODELS: dict[str, str] = {
    "faithfulness": "¿El informe está respaldado por los datos?",
    "coherence": "¿El informe es coherente y bien estructurado?",
    "completeness": "¿El informe cubre todos los aspectos de la pregunta?",
}
