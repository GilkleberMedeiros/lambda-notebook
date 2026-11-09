import streamlit as st
from src.config import (
    demonstrative_mode,
    set_llm_api_key,
    set_llm_model,
    set_embedding_model
)
from src.services import get_service
from src.mock_services import MockServices
from src.ui.styles import CUSTOM_CSS
from src.ui.sidebar import render_sidebar
from src.ui.gallery import render_gallery
from src.ui.chat import render_chat

from src.database.db import sqlite_engine   # Init DB!
from src.rag.vector_store import chroma_client  # Init ChromaDB!

# Sincroniza configurações da sessão caso tenham sido definidas pelo usuário
if "llm_api_key" in st.session_state:
    set_llm_api_key(st.session_state["llm_api_key"])
if "llm_model" in st.session_state:
    set_llm_model(st.session_state["llm_model"])
if "embedding_model" in st.session_state:
    set_embedding_model(st.session_state["embedding_model"])

services = get_service()

# Configuração da página Streamlit
st.set_page_config(
    page_title="Gemini Notebook - Docs Reviewer",
    page_icon="📓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injeção de estilos visuais customizados
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Inicialização dos dados mockados no st.session_state apenas se em modo demonstrativo
if demonstrative_mode():
    MockServices.init_mock_state()

# Renderização da Barra Lateral (Navegação de Pastas / Notebooks)
render_sidebar()

# Atualiza instância de serviços após renderização da sidebar
services = get_service()

# Recupera o Notebook Ativo
active_id = st.session_state.get("active_notebook_id")
notebooks = services.get_all_notebooks()

# Se o active_id guardado na sessão não pertencer aos notebooks disponíveis do modo atual, reseta
available_ids = [nb.id for nb in notebooks]
if active_id not in available_ids:
    active_id = available_ids[0] if available_ids else None
    st.session_state["active_notebook_id"] = active_id

# Área Principal da Aplicação
if active_id:
    tab_chat, tab_gallery = st.tabs(["💬 **Chat & Q&A**", "📚 **Galeria de Fontes**"])

    with tab_chat:
        render_chat(active_id)

    with tab_gallery:
        render_gallery(active_id)
else:
    st.markdown("## 👋 Bem-vindo ao **Gemini Notebook**")
    st.info("Para começar, crie um novo notebook na barra lateral à esquerda ou restaure os dados de exemplo.")
    if demonstrative_mode():
        if st.button("Carregar Dados Demonstrativos", type="primary"):
            MockServices.reset_mock_state()
            st.rerun()
