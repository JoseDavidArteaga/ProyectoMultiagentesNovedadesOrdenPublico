from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

from config import (
    LLM_PROVIDER,
    NEO4J_DATABASE, NEO4J_PASSWORD, NEO4J_URI,
    NEO4J_USERNAME, OLLAMA_BASE_URL, OLLAMA_CHAT_MODEL,
)
from src.local_chat import LocalGraphChat, PipelineStageError
from src.neo4j_graph import Neo4jGraphClient
from src.ollama_client import OllamaClient

sys.path.insert(0, str(Path(__file__).parent))

st.set_page_config(
    page_title="Vigía Cauca · Sistema Multiagente",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

#MainMenu,
footer,
header[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
section[data-testid="stSidebar"] {
  display: none !important;
  visibility: hidden !important;
}
.nav-active {
  color: var(--text) !important;
  background: var(--s2) !important;
  border-color: var(--border) !important;
}
/* Botón de reconexión ↺ */
[data-testid="stColumn"]:last-child .stBaseButton-secondary,
[data-testid="stColumn"]:last-child button {
  background: var(--s2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 6px !important;
  color: var(--muted) !important;
  font-size: 0.85rem !important;
  font-family: "JetBrains Mono", monospace !important;
  min-height: 32px !important;
  padding: 0 0.5rem !important;
  box-shadow: none !important;
  transition: color 0.18s, border-color 0.18s !important;
}
[data-testid="stColumn"]:last-child .stBaseButton-secondary:hover,
[data-testid="stColumn"]:last-child button:hover {
  color: var(--text) !important;
  border-color: var(--accent) !important;
  background: var(--s2) !important;
}
.stDeployButton { display: none !important; }
html { background: #0d1117; }
[data-testid="collapsedControl"] { display: none !important; }

:root {
  --bg:     #0d1117;
  --s1:     #161b22;
  --s2:     #21262d;
  --border: #30363d;
  --text:   #e6edf3;
  --muted:  #8b949e;
  --accent: #58a6ff;
  --green:  #3fb950;
  --red:    #f85149;
}

.stApp { background: var(--bg) !important; }
.main .block-container {
  max-width: 760px !important;
  padding: 0 1rem 5rem 1rem !important;
}

.vg-topbar {
  position: sticky; top: 0; z-index: 100;
  background: rgba(13,17,23,0.92);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
  padding: 0.65rem 0;
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 1.5rem;
}
.vg-brand {
  display: flex; align-items: center; gap: 0.5rem;
  color: var(--text); font-weight: 700; font-size: 0.92rem;
  letter-spacing: -0.02em; font-family: "Inter", sans-serif;
}
.vg-nav a {
  color: var(--muted); text-decoration: none; font-size: 0.8rem;
  font-weight: 500; padding: 0.35rem 0.75rem;
  border-radius: 6px; border: 1px solid transparent;
  transition: 0.18s ease; font-family: "Inter", sans-serif;
}
.vg-nav a:hover { color: var(--text); border-color: var(--border); background: var(--s2); }

.vg-welcome { text-align: center; padding: 2.5rem 1rem 1.5rem; }
.vg-welcome h1 {
  font-size: 1.55rem; font-weight: 700; color: var(--text);
  margin-bottom: 0.5rem; font-family: "Inter", sans-serif; letter-spacing: -0.03em;
}
.vg-welcome p {
  color: var(--muted); font-size: 0.875rem; line-height: 1.75;
  max-width: 440px; margin: 0 auto 1.75rem; font-family: "Inter", sans-serif;
}
.vg-chips { display: flex; flex-wrap: wrap; gap: 0.45rem; justify-content: center; }

/* Chips ahora son botones clicables */
.vg-chip {
  background: var(--s1); border: 1px solid var(--border); border-radius: 20px;
  padding: 0.4rem 0.9rem; font-size: 0.78rem; color: var(--muted);
  font-family: "Inter", sans-serif; transition: 0.18s;
  cursor: pointer; user-select: none;
}
.vg-chip:hover {
  color: var(--text); border-color: var(--accent);
  background: rgba(88,166,255,0.08);
}

.vg-status { display: flex; gap: 0.5rem; margin-bottom: 0.75rem; flex-wrap: wrap; }
.vg-pill {
  display: inline-flex; align-items: center; gap: 0.3rem;
  font-size: 0.71rem; font-family: "Inter", sans-serif;
  border-radius: 20px; padding: 0.18rem 0.65rem;
}
.vg-ok  { color: var(--green); background: rgba(63,185,80,0.1); border: 1px solid rgba(63,185,80,0.3); }
.vg-err { color: var(--red);   background: rgba(248,81,73,0.1);  border: 1px solid rgba(248,81,73,0.3); }

[data-testid="stChatMessage"] { background: transparent !important; padding: 0.25rem 0 !important; }
[data-testid="chatAvatarIcon-user"] > div,
[data-testid="chatAvatarIcon-assistant"] > div {
  background: var(--s2) !important; border: 1px solid var(--border) !important;
}

/* Input: borde neutral, focus en accent azul (nunca rojo) */
[data-testid="stChatInputContainer"] {
  background: var(--s1) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  box-shadow: none !important;
  outline: none !important;
}
[data-testid="stChatInputContainer"]:focus-within {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(88,166,255,0.12) !important;
}
[data-testid="stChatInputContainer"] textarea {
  color: var(--text) !important; background: transparent !important;
  font-family: "Inter", sans-serif !important; font-size: 0.9rem !important;
  caret-color: var(--accent) !important;
}
[data-testid="stChatInputContainer"] textarea:focus {
  outline: none !important;
  box-shadow: none !important;
}
/* Sobrescribe el rojo de Streamlit en focus a nivel global */
*:focus { outline: none !important; }
*:focus-visible { outline: none !important; }
textarea:focus, input:focus {
  border-color: var(--accent) !important;
  box-shadow: none !important;
  outline: none !important;
}
[data-testid="stChatInputContainer"],
[data-testid="stChatInputContainer"] *,
[data-testid="stChatInputContainer"]:focus-within {
  outline: none !important;
  box-shadow: none !important;
}
/* Luego aplica el tuyo */
[data-testid="stChatInputContainer"]:focus-within {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(88,166,255,0.12) !important;
}

details > summary {
  background: var(--s1) !important; border: 1px solid var(--border) !important;
  border-radius: 6px !important; color: var(--muted) !important;
  font-size: 0.77rem !important; font-family: "JetBrains Mono", monospace !important;
  padding: 0.4rem 0.75rem !important; cursor: pointer !important;
  list-style: none !important; margin-top: 0.5rem !important;
}
details[open] > summary { border-radius: 6px 6px 0 0 !important; }
details > div {
  background: var(--s1) !important; border: 1px solid var(--border) !important;
  border-top: none !important; border-radius: 0 0 6px 6px !important;
  padding: 0.75rem !important;
}

code {
  background: var(--bg) !important; color: var(--accent) !important;
  border: 1px solid var(--border) !important; border-radius: 4px !important;
  font-family: "JetBrains Mono", monospace !important; font-size: 0.78rem !important;
  padding: 0.1rem 0.35rem !important;
}
pre > code {
  display: block !important; padding: 0.85rem 1rem !important;
  overflow-x: auto !important; line-height: 1.65 !important;
  border: none !important; border-radius: 0 !important; background: transparent !important;
}
pre {
  background: #010409 !important; border: 1px solid var(--border) !important;
  border-radius: 8px !important; overflow: hidden !important; margin: 0.5rem 0 !important;
}

hr { border: none !important; border-top: 1px solid var(--border) !important; margin: 1.25rem 0 !important; }
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Topbar ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="vg-topbar">
  <div class="vg-brand">
    <svg width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="#58a6ff" stroke-width="2.5">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
    </svg>
    Vigía Cauca
  </div>
  <nav class="vg-nav">
    <a href="/" class="nav-active" target="_self">Chat</a>
    <a href="/Agentes" target="_self">Agentes</a>
    <a href="/Equipo" target="_self">Equipo</a>
  </nav>
</div>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def build_chat(uri, username, password, database, ollama_url, model):
    graph_client = Neo4jGraphClient(
        uri=uri, username=username, password=password, database=database,
    )
    ollama_client = OllamaClient(base_url=ollama_url, model=model)
    return LocalGraphChat(graph_client=graph_client, ollama_client=ollama_client)


@st.cache_resource(show_spinner=False)
def get_client():
    try:
        return build_chat(
            NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD,
            NEO4J_DATABASE, OLLAMA_BASE_URL, OLLAMA_CHAT_MODEL,
        ), None
    except Exception as e:
        return None, str(e)


# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# Estado para manejar el chip clicado
if "chip_query" not in st.session_state:
    st.session_state.chip_query = None

# Perfil / rol: valores por defecto (los selectbox usan la misma clave en session_state)
st.session_state.setdefault("perfil_ui", "no_tecnico")
st.session_state.setdefault("rol_usuario", "Operador")

# ── Connection check ──────────────────────────────────────────────────────────
client, init_err = get_client()
neo4j_ok, ollama_ok = False, False
conn_error = init_err or ""

if client:
    try:
        client.check_connections()
        neo4j_ok, ollama_ok = True, True
    except Exception as e:
        conn_error = str(e)
        err = conn_error.lower()
        neo4j_ok  = not any(k in err for k in ["neo4j", "bolt", "7687", "serviceunavailable", "authentication"])
        ollama_ok = not any(
            k in err
            for k in [
                "ollama",
                "11434",
                "connection refused",
                "connectionerror",
                "groq",
                "401",
                "403",
                "gsk_",
            ]
        )


def pill(label, ok):
    cls = "vg-ok" if ok else "vg-err"
    return f'<span class="vg-pill {cls}">● {label}</span>'


status_col, btn_col = st.columns([6, 1])
with status_col:
    llm_label = "Groq" if LLM_PROVIDER == "groq" else "Ollama"
    st.markdown(
        f'<div class="vg-status">{pill("Neo4j", neo4j_ok)}{pill(llm_label, ollama_ok)}</div>',
        unsafe_allow_html=True,
    )
with btn_col:
    if st.button("↺", help="Reconectar servicios", use_container_width=True):
        get_client.clear()
        st.rerun()

with st.expander("Perfil del informe y rol de usuario", expanded=False):
    st.selectbox(
        "Tono del informe",
        options=["no_tecnico", "tecnico"],
        format_func=lambda x: "No técnico (lenguaje claro)" if x == "no_tecnico" else "Técnico (detalle territorial)",
        key="perfil_ui",
        help="Definido en CONTEXTO.md como perfil_usuario para el Agente 3 (Redactor).",
    )
    st.selectbox(
        "Rol en la plataforma",
        options=["Visitante", "Operador", "Administrador"],
        key="rol_usuario",
        help="Si el rol es Visitante, el Agente 2 excluye novedades con visibilidad Privado.",
    )

if conn_error and not (neo4j_ok and ollama_ok):
    with st.expander("⬡ Ver detalle del error de conexión"):
        st.code(conn_error, language="text")

# ── Welcome + Chips clicables ─────────────────────────────────────────────────
EXAMPLES = [
    "¿Top 3 municipios con más hechos?",
    "¿Cuántos hostigamientos en 2024?",
    "¿Qué ocurrió en Toribío?",
    "¿Ataques con drones reportados?",
    "¿Municipios con más desplazamientos?",
]

if not st.session_state.messages:
    st.markdown("""
    <div class="vg-welcome">
      <h1>🛡️ Sistema de Análisis de Orden Público</h1>
      <p>Consulta en lenguaje natural sobre los hechos de seguridad del departamento del Cauca.
      Tres agentes (Intérprete, Consultor Cypher, Redactor) consultan Neo4j y redactan el informe.</p>
    </div>
    """, unsafe_allow_html=True)

    # Chips como botones Streamlit con estilo custom
    # Chips como botones Streamlit — 2 por fila para que no se aplasten
    st.markdown('<div class="vg-chips-wrap">', unsafe_allow_html=True)
    row1 = st.columns([1, 1])
    row2 = st.columns([1, 1])
    row3 = st.columns([1, 1, 1])

    chip_pairs = [(row1, EXAMPLES[0:2]), (row2, EXAMPLES[2:4]), (row3, EXAMPLES[4:5])]
    for row_cols, row_examples in chip_pairs:
        for j, example in enumerate(row_examples):
            with row_cols[j]:
                if st.button(example, key=f"chip_{EXAMPLES.index(example)}", use_container_width=True):
                    st.session_state.chip_query = example
    st.markdown('</div>', unsafe_allow_html=True)

    # Inyectar estilo sobre los botones de chips generados por Streamlit
    st.markdown("""
    <style>
    /* Chips */
    .vg-chips-wrap { margin-bottom: 1rem; }

    [data-testid="stHorizontalBlock"] .stBaseButton-secondary,
    [data-testid="stHorizontalBlock"] button[data-testid="stBaseButton-secondary"],
    [data-testid="stHorizontalBlock"] button {
      background: var(--s1) !important;
      border: 1px solid var(--border) !important;
      border-radius: 20px !important;
      padding: 0.35rem 0.85rem !important;
      font-size: 0.78rem !important;
      color: var(--muted) !important;
      font-family: "Inter", sans-serif !important;
      transition: 0.18s !important;
      box-shadow: none !important;
      min-height: 36px !important;
      line-height: 1.3 !important;
    }
    [data-testid="stHorizontalBlock"] button p,
    [data-testid="stHorizontalBlock"] .stBaseButton-secondary p {
      color: var(--muted) !important;
      font-size: 0.78rem !important;
      font-family: "Inter", sans-serif !important;
      margin: 0 !important;
    }
    [data-testid="stHorizontalBlock"] button:hover,
    [data-testid="stHorizontalBlock"] .stBaseButton-secondary:hover {
      color: var(--text) !important;
      border-color: var(--accent) !important;
      background: rgba(88,166,255,0.08) !important;
    }
    [data-testid="stHorizontalBlock"] button:hover p,
    [data-testid="stHorizontalBlock"] .stBaseButton-secondary:hover p {
      color: var(--text) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

# ── Historial ─────────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🛡️"):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            if msg.get("cypher"):
                with st.expander("⬡ Ver consulta Cypher ejecutada"):
                    st.code(msg["cypher"], language="cypher")
            if msg.get("rows"):
                with st.expander(f"⬡ Ver datos crudos · {len(msg['rows'])} registros"):
                    st.json(msg["rows"])
            if msg.get("intencion"):
                with st.expander("⬡ JSON de intención (Agente 1)"):
                    st.json(msg["intencion"])
            if msg.get("debug_trace"):
                with st.expander("⬡ Trazas de ejecución"):
                    st.code("\n".join(msg["debug_trace"]), language="text")


# ── Procesador central de consultas ──────────────────────────────────────────
def process_query(prompt: str):
    """Agrega el mensaje del usuario y genera la respuesta del asistente."""
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🛡️"):
        if not client or not (neo4j_ok and ollama_ok):
            resp = "⚠️ **Servicio no disponible.** Verifica que Neo4j y Ollama estén corriendo."
            st.markdown(resp)
            st.session_state.messages.append({"role": "assistant", "content": resp})
        else:
            with st.spinner("Analizando consulta…"):
                progress_box = st.empty()
                try:
                    def on_progress(msg: str) -> None:
                        progress_box.info(f"Estado: {msg}")

                    result = client.ask(
                        prompt,
                        perfil_ui=st.session_state.perfil_ui,
                        rol_usuario=st.session_state.rol_usuario,
                        progress_callback=on_progress,
                    )
                    progress_box.empty()
                    st.markdown(result.answer)
                    if result.cypher:
                        with st.expander("⬡ Ver consulta Cypher ejecutada"):
                            st.code(result.cypher, language="cypher")
                    if result.rows:
                        with st.expander(f"⬡ Ver datos crudos · {len(result.rows)} registros"):
                            st.json(result.rows)
                    if result.intencion_json:
                        with st.expander("⬡ JSON de intención (Agente 1)"):
                            st.json(result.intencion_json)
                    if result.debug_trace:
                        with st.expander("⬡ Trazas de ejecución"):
                            st.code("\n".join(result.debug_trace), language="text")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result.answer,
                        "cypher": result.cypher,
                        "rows": result.rows,
                        "intencion": result.intencion_json,
                        "debug_trace": result.debug_trace,
                    })
                except PipelineStageError as e:
                    progress_box.empty()
                    posibles = [
                        "Timeout en Ollama (consulta larga o modelo saturado en RAM/CPU).",
                        "Modelo no cargado o nombre incorrecto en .env (`OLLAMA_MODEL_*`).",
                        "Ollama no responde / desconexión local en `http://localhost:11434`.",
                        "Salida no-JSON del modelo en Agente 1 o Agente 2.",
                        "Cypher inválido o bloqueado por reglas de seguridad.",
                        "Error de ejecución en Neo4j (credenciales, base o consulta).",
                    ]
                    err_msg = f"❌ **Error en etapa:** `{e.stage}`\n\n**Detalle:** `{e}`"
                    st.markdown(err_msg)
                    with st.expander("⬡ Trazas de ejecución"):
                        st.code("\n".join(e.debug_trace), language="text")
                    with st.expander("⬡ Posibles excepciones a revisar"):
                        for item in posibles:
                            st.markdown(f"- {item}")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": err_msg,
                        "debug_trace": e.debug_trace,
                    })
                except Exception as e:
                    progress_box.empty()
                    err_msg = f"❌ **Error:** `{e}`"
                    st.markdown(err_msg)
                    st.session_state.messages.append({"role": "assistant", "content": err_msg})


# ── Ejecutar chip clicado (antes del chat_input para no colisionar) ────────────
if st.session_state.chip_query:
    query = st.session_state.chip_query
    st.session_state.chip_query = None
    process_query(query)
    st.rerun()

# ── Input ─────────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Escribe tu consulta sobre orden público del Cauca…"):
    process_query(prompt)
