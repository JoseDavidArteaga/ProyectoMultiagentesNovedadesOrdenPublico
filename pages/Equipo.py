import streamlit as st

st.set_page_config(
    page_title="Equipo · Vigía Cauca",
    page_icon="👥",
    layout="centered",
    initial_sidebar_state="collapsed",
)

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

.stDeployButton { display: none !important; }
html { background: #0d1117; }
[data-testid="collapsedControl"] { display: none !important; }

:root {
  --bg: #0d1117; --s1: #161b22; --s2: #21262d;
  --border: #30363d; --text: #e6edf3; --muted: #8b949e; --accent: #58a6ff;
}
.stApp { background: var(--bg) !important; }
.main .block-container { max-width: 820px !important; padding: 0 1rem 3rem !important; }

.vg-topbar {
  position: sticky; top: 0; z-index: 100;
  background: rgba(13,17,23,0.92); backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border); padding: 0.65rem 0;
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 2rem;
}
.vg-brand { display: flex; align-items: center; gap: 0.5rem; color: var(--text); font-weight: 700; font-size: 0.92rem; letter-spacing: -0.02em; font-family: "Inter", sans-serif; }
.vg-nav a { color: var(--muted); text-decoration: none; font-size: 0.8rem; font-weight: 500; padding: 0.35rem 0.75rem; border-radius: 6px; border: 1px solid transparent; transition: 0.18s; font-family: "Inter", sans-serif; }
.vg-nav a:hover { color: var(--text); border-color: var(--border); background: var(--s2); }

.vg-header { padding: 1.5rem 0 2rem; }
.vg-header h1 { color: var(--text); font-size: 1.4rem; font-weight: 700; font-family: "Inter", sans-serif; letter-spacing: -0.025em; margin-bottom: 0.4rem; }
.vg-header p { color: var(--muted); font-size: 0.875rem; line-height: 1.7; font-family: "Inter", sans-serif; max-width: 560px; }

.team-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 2rem; }
.team-card {
  background: var(--s1); border: 1px solid var(--border);
  border-radius: 12px; padding: 1.5rem 1.25rem;
  display: flex; flex-direction: column; gap: 0.75rem;
  transition: border-color 0.2s, background 0.2s;
}
.team-card:hover { border-color: var(--accent); background: rgba(88,166,255,0.04); }

.team-avatar {
  width: 48px; height: 48px; border-radius: 50%;
  background: var(--s2); border: 2px solid var(--border);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.1rem; font-weight: 700; color: var(--accent);
  font-family: "Inter", sans-serif;
}
.team-name { font-size: 0.88rem; font-weight: 600; color: var(--text); font-family: "Inter", sans-serif; line-height: 1.3; }
.team-role { font-size: 0.75rem; color: var(--accent); font-family: "JetBrains Mono", monospace; }
.team-links { display: flex; gap: 0.4rem; flex-wrap: wrap; margin-top: auto; }
.team-link {
  display: inline-flex; align-items: center; gap: 0.3rem;
  font-size: 0.72rem; color: var(--muted); text-decoration: none;
  background: var(--s2); border: 1px solid var(--border);
  border-radius: 6px; padding: 0.25rem 0.55rem;
  font-family: "Inter", sans-serif; transition: 0.15s;
}
.team-link:hover { color: var(--text); border-color: var(--accent); }

.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 2rem; }
.info-card {
  background: var(--s1); border: 1px solid var(--border);
  border-radius: 10px; padding: 1.25rem;
}
.info-card-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); font-family: "JetBrains Mono", monospace; margin-bottom: 0.35rem; }
.info-card-value { font-size: 0.875rem; color: var(--text); font-family: "Inter", sans-serif; font-weight: 500; line-height: 1.4; }

.support-box {
  background: var(--s1); border: 1px solid var(--border);
  border-radius: 12px; padding: 1.5rem;
}
.support-box h3 { color: var(--text); font-size: 0.95rem; font-weight: 600; font-family: "Inter", sans-serif; margin-bottom: 0.5rem; }
.support-box p { color: var(--muted); font-size: 0.84rem; line-height: 1.65; font-family: "Inter", sans-serif; margin-bottom: 1rem; }
.support-steps { display: flex; flex-direction: column; gap: 0.5rem; }
.support-step {
  display: flex; align-items: flex-start; gap: 0.75rem;
  font-size: 0.82rem; color: var(--muted); font-family: "Inter", sans-serif;
}
.support-step-num {
  width: 20px; height: 20px; border-radius: 50%; flex-shrink: 0;
  background: rgba(88,166,255,0.15); border: 1px solid rgba(88,166,255,0.3);
  color: var(--accent); font-size: 0.68rem; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
}

hr { border: none !important; border-top: 1px solid var(--border) !important; margin: 1.5rem 0 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="vg-topbar">
  <div class="vg-brand">
    <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#58a6ff" stroke-width="2.5">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
    </svg>
    Vigía Cauca
  </div>
  <nav class="vg-nav">
    <a href="/" target="_self">Chat</a>
    <a href="/Agentes" target="_self">Agentes</a>
    <a href="/Equipo" class="nav-active" target="_self">Equipo</a>
  </nav>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="vg-header">
  <h1>👥 Equipo de desarrollo</h1>
  <p>Proyecto académico de la Universidad del Cauca. Ante cualquier duda sobre el sistema,
  el funcionamiento de los agentes o errores en producción, contacta directamente al equipo.</p>
</div>
""", unsafe_allow_html=True)

# ── Team cards ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="team-grid">

  <div class="team-card">
    <div class="team-avatar">BG</div>
    <div>
      <div class="team-name">Brayan Steven Gomes Lasso</div>
      <div class="team-role">Interfaz · UX · Despliegue</div>
    </div>
    <div class="team-links">
      <a class="team-link" href="mailto:brayangomes@unicauca.edu.co">✉ Email</a>
      <a class="team-link" href="https://github.com/bratev-dev" target="_blank">⌥ GitHub</a>
    </div>
  </div>

  <div class="team-card">
    <div class="team-avatar">CU</div>
    <div>
      <div class="team-name">Cristhian Camilo Unas Ocaña</div>
      <div class="team-role">Agentes · Ollama</div>
    </div>
    <div class="team-links">
      <a class="team-link" href="mailto:cunas@unicauca.edu.co">✉ Email</a>
      <a class="team-link" href="https://github.com/CrisCamUO" target="_blank">⌥ GitHub</a>
    </div>
  </div>

  <div class="team-card">
    <div class="team-avatar">JA</div>
    <div>
      <div class="team-name">José David Arteaga Fernández</div>
      <div class="team-role">Backend · Neo4j · Pipeline</div>
    </div>
    <div class="team-links">
      <a class="team-link" href="mailto:josedavidart@unicauca.edu.co">✉ Email</a>
      <a class="team-link" href="https://github.com/JoseDavidArteaga" target="_blank">⌥ GitHub</a>
    </div>
  </div>

</div>
""", unsafe_allow_html=True)

# ── Project info ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="info-grid">
  <div class="info-card">
    <div class="info-card-label">Institución</div>
    <div class="info-card-value">Universidad del Cauca<br>Fac. Ingeniería Electrónica y Telecomunicaciones</div>
  </div>
  <div class="info-card">
    <div class="info-card-label">Asignatura</div>
    <div class="info-card-value">Aplicaciones de la IA Generativa<br>Semestre 2026-1</div>
  </div>
  <div class="info-card">
    <div class="info-card-label">Docente</div>
    <div class="info-card-value">Nestor Díaz</div>
  </div>
  <div class="info-card">
    <div class="info-card-label">Stack tecnológico</div>
    <div class="info-card-value">Ollama · Neo4j · Streamlit · Python</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Support guide ─────────────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div class="support-box">
  <h3>🛠 ¿Problemas con el sistema?</h3>
  <p>Antes de contactar al equipo, verifica los siguientes puntos. La mayoría de errores
  tienen solución local sin necesidad de soporte.</p>
  <div class="support-steps">
    <div class="support-step">
      <div class="support-step-num">1</div>
      <span>Confirma que <strong style="color:#e6edf3">Ollama</strong> está activo: abre <code style="background:#21262d;color:#58a6ff;padding:0.1rem 0.35rem;border-radius:4px;font-size:0.75rem">http://localhost:11434</code> — debe decir <em>Ollama is running</em>.</span>
    </div>
    <div class="support-step">
      <div class="support-step-num">2</div>
      <span>Confirma que <strong style="color:#e6edf3">Neo4j Desktop</strong> tiene la base de datos en estado <em>Started</em> (botón verde).</span>
    </div>
    <div class="support-step">
      <div class="support-step-num">3</div>
      <span>Verifica que el archivo <code style="background:#21262d;color:#58a6ff;padding:0.1rem 0.35rem;border-radius:4px;font-size:0.75rem">.env</code> tiene el nombre correcto de la base de datos en <code style="background:#21262d;color:#58a6ff;padding:0.1rem 0.35rem;border-radius:4px;font-size:0.75rem">NEO4J_DATABASE</code>.</span>
    </div>
    <div class="support-step">
      <div class="support-step-num">4</div>
      <span>Usa el botón <strong style="color:#e6edf3">↺</strong> en la pantalla principal para limpiar caché y reconectar.</span>
    </div>
    <div class="support-step">
      <div class="support-step-num">5</div>
      <span>Si el error persiste, expande <em>"Ver detalle del error de conexión"</em> en el chat y comparte el mensaje con el equipo.</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
