import streamlit as st
from src.mock_data import init_mock_state, get_all_notebooks, reset_mock_state
from src.ui.styles import CUSTOM_CSS
from src.ui.sidebar import render_sidebar
from src.ui.gallery import render_gallery
from src.ui.chat import render_chat

from src.database.db import sqlite_engine   # Init DB!
from src.rag.vector_store import chroma_client  # Init ChromaDB!

# Configuração da página Streamlit
st.set_page_config(
    page_title="Gemini Notebook - Docs Reviewer",
    page_icon="📓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injeção de estilos visuais customizados
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Inicialização dos dados mockados no st.session_state
init_mock_state()

# Renderização da Barra Lateral (Navegação de Pastas / Notebooks)
render_sidebar()

# Recupera o Notebook Ativo
active_id = st.session_state.get("active_notebook_id")
notebooks = get_all_notebooks()

if not active_id and notebooks:
    active_id = notebooks[0]["id"]
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
    if st.button("Carregar Dados Demonstrativos", type="primary"):
        reset_mock_state()
        st.rerun()
