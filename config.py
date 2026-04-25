"""
config.py — Configuración centralizada del sistema multiagente.
Carga las variables de entorno desde un archivo .env (local) o desde los
Secrets de Google Colab.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # carga .env si existe (entorno local)


# ─── OpenAI ──────────────────────────────────────────────────────────────────
OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")

# ─── Ollama local ────────────────────────────────────────────────────────────
OLLAMA_BASE_URL: str = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_CHAT_MODEL: str = os.environ.get("OLLAMA_CHAT_MODEL", "llama3.1:8b")
OLLAMA_TEMPERATURE: float = float(os.environ.get("OLLAMA_TEMPERATURE", "0.2"))

# ─── Neo4j local ─────────────────────────────────────────────────────────────
NEO4J_URI: str = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME: str = os.environ.get("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD: str = os.environ.get("NEO4J_PASSWORD", "")
NEO4J_DATABASE: str = os.environ.get("NEO4J_DATABASE", "neo4j")
NEO4J_MAX_RESULTS: int = int(os.environ.get("NEO4J_MAX_RESULTS", "20"))

# Modelos
EMBEDDING_MODEL: str = "text-embedding-3-large"
GENERATOR_MODEL: str = "gpt-4.1"
VERIFIER_MODEL: str = "gpt-4o-mini"

# ─── Agente 1 — Recuperador ───────────────────────────────────────────────────
TOP_K: int = 5                          # documentos recuperados por consulta
VECTOR_STORE_BACKEND: str = "chroma"   # "chroma" | "faiss"
CHROMA_PERSIST_DIR: str = "data/chroma_db"

# ─── Agente 2 — Generador ─────────────────────────────────────────────────────
GENERATOR_MAX_TOKENS: int = 1500
GENERATOR_TEMPERATURE: float = 0.2     # bajo para reportes institucionales

# ─── Agente 3 — Verificador ───────────────────────────────────────────────────
VERIFIER_MAX_TOKENS: int = 800
VERIFIER_TEMPERATURE: float = 0.0      # determinista para validación
FAITHFULNESS_THRESHOLD: float = 0.85   # umbral mínimo aceptable

# ─── Datos ────────────────────────────────────────────────────────────────────
RAW_DATA_DIR: str = "data/raw"
PROCESSED_DATA_DIR: str = "data/processed"
PROCESSED_DATA_FILE: str = "data/processed/hechos_orden_publico_2024.csv"
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

# ─── Categorías de hechos ─────────────────────────────────────────────────────
CATEGORIAS_HECHO: list[str] = [
    "ENFRENTAMIENTO",
    "CONFRONTACION",
    "HOSTIGAMIENTO",
    "ATAQUE_CON_DRONES",
    "BLOQUEO_VIAL",
    "DESPLAZAMIENTO_FORZADO",
    "HOMICIDIO",
    "SECUESTRO",
    "RETEN_ILEGAL",
    "PROTESTA_SOCIAL",
    "OTRO",
]
