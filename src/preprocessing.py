"""
src/preprocessing.py — Pipeline de limpieza y normalización del dataset Excel.

Resuelve los problemas documentados en CONTEXTO.md:
  - Fechas en múltiples formatos → ISO 8601
  - Inconsistencias en nombres de municipios → Fuzzy Matching
  - Errores ortográficos en campos narrativos → limpieza básica
  - Duplicados entre hojas generales y temáticas → deduplicación
  - Campos booleanos derivados (uso_drones, uso_explosivos, hay_bloqueo)
"""

import re
import hashlib
import pandas as pd
from dateutil import parser as date_parser
from thefuzz import process as fuzz_process

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import MUNICIPIOS_CAUCA, PROCESSED_DATA_FILE


# ─── Constantes internas ──────────────────────────────────────────────────────

_SHEET_MAP = {
    # nombre de hoja → categoría asignada
    "enero-junio":       None,   # hoja general; la categoría se infiere
    "julio-diciembre":   None,
    "ENFRENTAMIENTOS":   "ENFRENTAMIENTO",
    "CONFRONTACIONES":   "CONFRONTACION",
    "HOSTIGAMIENTOS":    "HOSTIGAMIENTO",
    "ATAQUE CON DRONES": "ATAQUE_CON_DRONES",
}

_KEYWORDS_DRONES     = ["dron", "drone", "uav", "vehículo aéreo"]
_KEYWORDS_EXPLOSIVOS = ["explosivo", "granada", "bomba", "mina", "cilindro"]
_KEYWORDS_BLOQUEO    = ["bloqueo", "bloqueó", "bloquearon", "cierre vial", "obstaculiz"]


# ─── Funciones auxiliares ─────────────────────────────────────────────────────

def _normalizar_fecha(valor) -> str | None:
    """Convierte cualquier representación de fecha a YYYY-MM-DD."""
    if pd.isna(valor):
        return None
    raw = str(valor).strip()
    # Eliminar artefactos comunes: "02/05/05/2024" → tomar primeros 10 chars
    raw = re.sub(r"(\d{2}/\d{2}/\d{2}/\d{4})", lambda m: m.group(0)[:10], raw)
    try:
        return date_parser.parse(raw, dayfirst=True).strftime("%Y-%m-%d")
    except Exception:
        return None


def _normalizar_municipio(nombre: str, score_minimo: int = 75) -> str:
    """Devuelve el nombre oficial del municipio usando Fuzzy Matching."""
    if not nombre or pd.isna(nombre):
        return "DESCONOCIDO"
    resultado, score = fuzz_process.extractOne(str(nombre).strip(), MUNICIPIOS_CAUCA)
    return resultado if score >= score_minimo else str(nombre).strip().title()


def _limpiar_texto(texto) -> str:
    """Limpieza básica de campos narrativos."""
    if pd.isna(texto):
        return ""
    t = str(texto).strip()
    # Colapsar espacios múltiples
    t = re.sub(r"\s+", " ", t)
    # Eliminar caracteres de control
    t = re.sub(r"[\x00-\x1f\x7f]", "", t)
    return t


def _detectar_booleano(texto: str, keywords: list[str]) -> bool:
    texto_lower = texto.lower()
    return any(kw in texto_lower for kw in keywords)


def _generar_id(row: pd.Series) -> str:
    """ID único basado en fecha + municipio + hash de los primeros 80 chars de hechos."""
    base = f"{row.get('fecha','')}-{row.get('municipio','')}-{str(row.get('hechos',''))[:80]}"
    return hashlib.md5(base.encode()).hexdigest()[:12]


# ─── Carga del Excel ──────────────────────────────────────────────────────────

def cargar_excel(ruta: str) -> pd.DataFrame:
    """
    Lee todas las hojas relevantes del Excel y las consolida en un único
    DataFrame. Asigna la categoría del hecho según la hoja de origen.
    """
    xl = pd.ExcelFile(ruta)
    frames = []

    for hoja in xl.sheet_names:
        # Intentar hacer coincidir el nombre de hoja con el mapa conocido
        categoria = None
        for clave, cat in _SHEET_MAP.items():
            if clave.lower() in hoja.lower():
                categoria = cat
                break

        try:
            df = pd.read_excel(xl, sheet_name=hoja, dtype=str)
        except Exception as e:
            print(f"[WARN] No se pudo leer la hoja '{hoja}': {e}")
            continue

        df["_hoja_origen"] = hoja
        df["_categoria_hoja"] = categoria
        frames.append(df)

    if not frames:
        raise ValueError(f"No se encontraron hojas legibles en {ruta}")

    return pd.concat(frames, ignore_index=True)


# ─── Normalización de columnas ────────────────────────────────────────────────

def _mapear_columnas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renombra las columnas del Excel a los nombres estandarizados del schema.
    Ajusta el mapeo si los encabezados reales del Excel difieren.
    """
    # Mapeo flexible: nombre en Excel (minúsculas) → nombre estándar
    mapeo = {
        "fecha":        "fecha_raw",
        "municipio":    "municipio_raw",
        "hechos":       "hechos_raw",
        "afectaciones": "afectaciones_raw",
    }
    columnas_lower = {c.lower().strip(): c for c in df.columns}
    renombrar = {}
    for clave, nombre_std in mapeo.items():
        if clave in columnas_lower:
            renombrar[columnas_lower[clave]] = nombre_std

    return df.rename(columns=renombrar)


# ─── Pipeline principal ───────────────────────────────────────────────────────

def preprocesar(ruta_excel: str, guardar: bool = True) -> pd.DataFrame:
    """
    Ejecuta el pipeline completo de limpieza sobre el archivo Excel.

    Parámetros
    ----------
    ruta_excel : str
        Ruta al archivo .xlsx original.
    guardar : bool
        Si True, exporta el resultado a PROCESSED_DATA_FILE (CSV).

    Retorna
    -------
    pd.DataFrame con el dataset limpio y enriquecido.
    """
    print(f"[1/6] Cargando Excel: {ruta_excel}")
    df = cargar_excel(ruta_excel)
    print(f"      {len(df):,} filas cargadas de {df['_hoja_origen'].nunique()} hojas.")

    print("[2/6] Mapeando columnas...")
    df = _mapear_columnas(df)

    # Verificar columnas mínimas requeridas
    requeridas = {"fecha_raw", "municipio_raw", "hechos_raw"}
    faltantes = requeridas - set(df.columns)
    if faltantes:
        raise ValueError(f"Columnas requeridas no encontradas: {faltantes}")

    print("[3/6] Normalizando fechas...")
    df["fecha"] = df["fecha_raw"].apply(_normalizar_fecha)

    print("[4/6] Normalizando municipios (Fuzzy Matching)...")
    df["municipio"] = df["municipio_raw"].apply(_normalizar_municipio)

    print("[5/6] Limpiando campos narrativos y derivando campos booleanos...")
    df["hechos"]       = df["hechos_raw"].apply(_limpiar_texto)
    df["afectaciones"] = df.get("afectaciones_raw", pd.Series([""] * len(df))).apply(_limpiar_texto)

    texto_combinado = df["hechos"] + " " + df["afectaciones"]
    df["uso_drones"]     = texto_combinado.apply(lambda t: _detectar_booleano(t, _KEYWORDS_DRONES))
    df["uso_explosivos"] = texto_combinado.apply(lambda t: _detectar_booleano(t, _KEYWORDS_EXPLOSIVOS))
    df["hay_bloqueo"]    = texto_combinado.apply(lambda t: _detectar_booleano(t, _KEYWORDS_BLOQUEO))

    # Derivar campos temporales
    fechas_dt = pd.to_datetime(df["fecha"], errors="coerce")
    df["mes"]       = fechas_dt.dt.month
    df["trimestre"] = fechas_dt.dt.quarter
    df["semestre"]  = fechas_dt.dt.month.apply(lambda m: 1 if m <= 6 else 2)

    # Categoría del hecho: prioridad a la hoja temática; si es hoja general se
    # intenta inferir desde el texto
    df["categoria_hecho"] = df["_categoria_hoja"].fillna(
        df["hechos"].apply(_inferir_categoria)
    )

    print("[6/6] Deduplicando registros entre hojas...")
    df["id"] = df.apply(_generar_id, axis=1)
    n_antes = len(df)
    df = df.drop_duplicates(subset=["id"])
    print(f"      {n_antes - len(df):,} duplicados eliminados. {len(df):,} filas únicas.")

    # Seleccionar y ordenar columnas finales
    columnas_finales = [
        "id", "fecha", "mes", "trimestre", "semestre",
        "municipio", "categoria_hecho",
        "hechos", "afectaciones",
        "uso_drones", "uso_explosivos", "hay_bloqueo",
        "_hoja_origen",
    ]
    columnas_presentes = [c for c in columnas_finales if c in df.columns]
    df = df[columnas_presentes].sort_values("fecha", na_position="last")

    if guardar:
        os.makedirs(os.path.dirname(PROCESSED_DATA_FILE), exist_ok=True)
        df.to_csv(PROCESSED_DATA_FILE, index=False, encoding="utf-8")
        print(f"\n Dataset guardado en: {PROCESSED_DATA_FILE}")

    return df


def _inferir_categoria(texto: str) -> str:
    """Heurística simple para asignar categoría desde el texto del hecho."""
    t = texto.lower()
    if any(k in t for k in ["enfrentamiento", "combate"]):
        return "ENFRENTAMIENTO"
    if "confrontaci" in t:
        return "CONFRONTACION"
    if "hostigami" in t or "hostigmiento" in t:
        return "HOSTIGAMIENTO"
    if any(k in t for k in _KEYWORDS_DRONES):
        return "ATAQUE_CON_DRONES"
    if any(k in t for k in _KEYWORDS_BLOQUEO):
        return "BLOQUEO_VIAL"
    if "desplazami" in t:
        return "DESPLAZAMIENTO_FORZADO"
    if "homicidio" in t or "asesinato" in t:
        return "HOMICIDIO"
    if "secuestro" in t or "plagio" in t:
        return "SECUESTRO"
    if "retén" in t or "reten" in t:
        return "RETEN_ILEGAL"
    if "protesta" in t or "marcha" in t or "paro" in t:
        return "PROTESTA_SOCIAL"
    return "OTRO"
