# Cómo arrancar Vigía Cauca en tu máquina

Esta guía sirve para clonar el repositorio, instalar dependencias, configurar Neo4j y Ollama, y ejecutar la aplicación web (Streamlit).

## Requisitos previos

- **Python** 3.11 o superior (recomendado 3.11+).
- **Neo4j** (Desktop o Aura local) con una base de datos creada y en estado *Started*.
- **Ollama** instalado y en ejecución (por defecto escucha en `http://localhost:11434`).
- **Git** (para clonar el repositorio).

## 1. Clonar el repositorio y crear el entorno virtual

En la carpeta donde guardes el proyecto:

```powershell
git clone <url-del-repositorio>
cd ProyectoMultiagentesNovedadesOrdenPublico
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

En macOS o Linux:

```bash
git clone <url-del-repositorio>
cd ProyectoMultiagentesNovedadesOrdenPublico
python3 -m venv .venv
source .venv/bin/activate
```

## 2. Instalar dependencias de Python

Con el entorno virtual activado:

```powershell
pip install -r requirements.txt
```

## 3. Archivo `.env`

En la **raíz del proyecto** debe existir un archivo llamado `.env` (junto a `app.py` y `config.py`). Ahí se definen la conexión a Neo4j y los modelos de Ollama que usará la aplicación.

Variables que debes revisar como mínimo:

| Variable | Descripción |
|----------|-------------|
| `NEO4J_URI` | URI Bolt (por defecto `bolt://localhost:7687`). |
| `NEO4J_USERNAME` | Usuario de Neo4j (suele ser `neo4j`). |
| `NEO4J_PASSWORD` | Contraseña que configuraste al crear la base. |
| `NEO4J_DATABASE` | Nombre de la base de datos en Neo4j (por ejemplo `neo4j` o el nombre que hayas creado en Desktop). |
| `OLLAMA_BASE_URL` | URL del servicio Ollama (por defecto `http://localhost:11434`). |
| `OLLAMA_CHAT_MODEL` | Nombre del modelo en Ollama para uso general. |
| `OLLAMA_MODEL_INTERPRETER` | Modelo del Agente 1 (intención JSON). |
| `OLLAMA_MODEL_CONSULTANT` | Modelo del Agente 2 (generación de Cypher). |
| `OLLAMA_MODEL_REDACTOR` | Modelo del Agente 3 (redacción del informe). |

Puedes usar el mismo nombre de modelo en las cuatro variables si tu equipo tiene poca memoria RAM: así solo se carga un modelo a la vez en el flujo.

Descarga en Ollama los modelos que indiques en `.env` (el nombre debe coincidir con el que ves al ejecutar `ollama list`):

```bash
ollama pull <nombre-del-modelo>
```

## 4. Cargar el grafo de ejemplo en Neo4j

El script Cypher de demostración está en `data/raw/vigia_cauca_neo4j.cypher` (véase también `CONTEXTO.md`).

Con Neo4j en marcha y el `.env` apuntando a la base correcta:

```powershell
python -m src.load_neo4j
```

Esto ejecuta las sentencias del archivo configurado en `NEO4J_SEED_FILE` (por defecto el anterior). Si la base ya contenía datos de una prueba anterior y necesitas empezar de cero, vacía la base desde Neo4j Browser o Desktop antes de volver a cargar.

## 5. Arrancar Ollama y Neo4j

1. Inicia **Neo4j** y comprueba que la base indicada en `NEO4J_DATABASE` esté *Started*.
2. Inicia **Ollama** y comprueba en el navegador que responde `http://localhost:11434` (mensaje tipo *Ollama is running*).

## 6. Lanzar la aplicación Streamlit

Desde la raíz del proyecto, con el entorno virtual activo:

```powershell
streamlit run app.py
```

Streamlit abrirá la interfaz en el navegador (por defecto `http://localhost:8501`). Desde ahí puedes usar el chat, la página **Agentes** (descripción del pipeline) y **Equipo**.

## 7. Comprobar conexiones

En la pantalla principal del chat aparecen indicadores de estado para Neo4j y Ollama. Si algo falla:

- Usa el botón **↺** para limpiar la caché de conexión y reintentar.
- Abre el expander de detalle de error y revisa usuario, contraseña y nombre de base en `.env`.

## 8. Notas opcionales

- **Migración desde Excel** y otros scripts usan rutas bajo `data/`; no son necesarios solo para probar el chat si ya cargaste el Cypher de ejemplo.
- El módulo `src/pipeline.py` y dependencias como **OpenAI** o **Chroma** corresponden a un flujo auxiliar basado en RAG; la aplicación principal del chat usa **Neo4j + Ollama** según `CONTEXTO.md`.

Si tras seguir estos pasos algo no arranca, revisa que la versión de Python sea compatible y que no haya otro proceso ocupando el puerto de Streamlit, Neo4j u Ollama.
