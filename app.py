from __future__ import annotations

import streamlit as st

from config import NEO4J_DATABASE, NEO4J_PASSWORD, NEO4J_URI, NEO4J_USERNAME, OLLAMA_BASE_URL, OLLAMA_CHAT_MODEL
from src.local_chat import LocalGraphChat
from src.neo4j_graph import Neo4jGraphClient
from src.ollama_client import OllamaClient


st.set_page_config(page_title="Vigia Cauca Chat", page_icon="💬", layout="wide")


def build_chat(uri: str, username: str, password: str, database: str, ollama_url: str, model: str) -> LocalGraphChat:
    graph_client = Neo4jGraphClient(
        uri=uri,
        username=username,
        password=password,
        database=database,
    )
    ollama_client = OllamaClient(
        base_url=ollama_url,
        model=model,
    )
    return LocalGraphChat(graph_client=graph_client, ollama_client=ollama_client)


if "messages" not in st.session_state:
    st.session_state.messages = []

if "connection_ok" not in st.session_state:
    st.session_state.connection_ok = False


st.title("Vigia Cauca Chat")
st.caption("Chat local con Ollama y consultas sobre Neo4j")

with st.sidebar:
    st.subheader("Conexiones")
    neo4j_uri = st.text_input("Neo4j URI", value=NEO4J_URI)
    neo4j_username = st.text_input("Neo4j usuario", value=NEO4J_USERNAME)
    neo4j_password = st.text_input("Neo4j contraseña", value=NEO4J_PASSWORD, type="password")
    neo4j_database = st.text_input("Neo4j database", value=NEO4J_DATABASE)
    ollama_url = st.text_input("Ollama URL", value=OLLAMA_BASE_URL)
    ollama_model = st.text_input("Modelo Ollama", value=OLLAMA_CHAT_MODEL)

    if st.button("Probar conexiones", use_container_width=True):
        try:
            chat = build_chat(
                neo4j_uri,
                neo4j_username,
                neo4j_password,
                neo4j_database,
                ollama_url,
                ollama_model,
            )
            chat.check_connections()
            st.session_state.connection_ok = True
            st.success("Neo4j y Ollama responden correctamente.")
        except Exception as exc:
            st.session_state.connection_ok = False
            st.error(f"No se pudo conectar: {exc}")

    st.markdown("Consultas sugeridas:")
    st.code("Top 5 municipios con más novedades")
    st.code("¿Qué novedades hubo en Toribío?")
    st.code("¿Qué actores aparecen en ataques con dron?")


for item in st.session_state.messages:
    with st.chat_message(item["role"]):
        st.markdown(item["content"])
        if item.get("cypher"):
            with st.expander("Cypher ejecutado"):
                st.code(item["cypher"], language="cypher")
        if item.get("rows"):
            with st.expander("Filas devueltas"):
                st.json(item["rows"])


prompt = st.chat_input("Escribe tu consulta sobre novedades de orden público")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            chat = build_chat(
                neo4j_uri,
                neo4j_username,
                neo4j_password,
                neo4j_database,
                ollama_url,
                ollama_model,
            )
            turn = chat.ask(prompt)
            st.markdown(turn.answer)
            if turn.cypher:
                with st.expander("Cypher ejecutado"):
                    st.code(turn.cypher, language="cypher")
            if turn.rows:
                with st.expander("Filas devueltas"):
                    st.json(turn.rows)
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": turn.answer,
                    "cypher": turn.cypher,
                    "rows": turn.rows,
                }
            )
        except Exception as exc:
            message = f"Error al procesar la consulta: {exc}"
            st.error(message)
            st.session_state.messages.append({"role": "assistant", "content": message})