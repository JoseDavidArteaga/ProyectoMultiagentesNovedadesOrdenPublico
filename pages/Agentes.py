import streamlit as st

st.set_page_config(
    page_title="Agentes · Vigía Cauca",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
#MainMenu, footer, header[data-testid="stHeader"], [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"], section[data-testid="stSidebar"] {
  display: none !important;
}
.nav-active { color: #e6edf3 !important; background: #21262d !important; border-color: #30363d !important; }
.stDeployButton { display: none !important; }
html { background: #0d1117; }
:root { --bg: #0d1117; --text: #e6edf3; --muted: #8b949e; --accent: #58a6ff; --border: #30363d; }
.stApp { background: var(--bg) !important; }
.main .block-container { max-width: 760px !important; padding: 0 1rem 3rem !important; }
.vg-topbar {
  position: sticky; top: 0; z-index: 100;
  background: rgba(13,17,23,0.92); backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border); padding: 0.65rem 0;
  display: flex; align-items: center; justify-content: space-between; margin-bottom: 2rem;
}
.vg-brand { display: flex; align-items: center; gap: 0.5rem; color: var(--text); font-weight: 700;
  font-size: 0.92rem; font-family: "Segoe UI", sans-serif; }
.vg-nav a { color: var(--muted); text-decoration: none; font-size: 0.8rem; padding: 0.35rem 0.75rem;
  border-radius: 6px; border: 1px solid transparent; }
.vg-nav a:hover { color: var(--text); border-color: var(--border); background: #21262d; }
h1 { color: var(--text); font-size: 1.35rem; }
p, li { color: var(--muted); font-size: 0.9rem; line-height: 1.7; }
code { color: var(--accent); background: #161b22; padding: 0.1rem 0.35rem; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="vg-topbar">
  <div class="vg-brand">🛡️ Vigía Cauca</div>
  <nav class="vg-nav">
    <a href="/" target="_self">Chat</a>
    <a href="/Agentes" class="nav-active" target="_self">Agentes</a>
    <a href="/Equipo" target="_self">Equipo</a>
  </nav>
</div>
""", unsafe_allow_html=True)

st.title("Pipeline de tres agentes")

st.markdown("""
El sistema **no usa RAG**: los datos salen solo de **Neo4j** mediante Cypher de solo lectura
(`MATCH` / `OPTIONAL MATCH`, etc.). Los modelos locales corren en **Ollama** (por defecto Qwen 3.5,
según `CONTEXTO.md` y variables `OLLAMA_MODEL_*` en `.env`).

1. **Agente 1 — Intérprete** (`qwen3.5:9b` por defecto): convierte la pregunta en un JSON de intención
   (categoría, ubicación, período, `perfil_usuario`, etc.). Si falta alcance, devuelve una aclaración y **no** ejecuta consulta.

2. **Agente 2 — Consultor** (`qwen3.5:27b` por defecto): a partir del JSON genera Cypher válido con
   `[:CONTIENE*1..4]` para municipios, valida seguridad y ejecuta contra Neo4j (máximo 100 filas).
   Si el rol es **Visitante**, debe excluir novedades con `visibilidad = Privado`.

3. **Agente 3 — Redactor** (`qwen3.5:9b` por defecto): redacta el informe institucional usando **solo**
   los datos devueltos por Neo4j, reflejando `nivel_confianza` y el tono según `perfil_usuario`.

Documentación completa del modelo de datos y relaciones: **`CONTEXTO.md`** y el script
`data/raw/vigia_cauca_neo4j.cypher`.
""")
