import streamlit as st
from src.config import (
    demonstrative_mode,
    set_llm_api_key,
    set_llm_model,
    get_llm_model,
    set_embedding_model,
    get_embedding_model,
    DEFAULT_LLM_MODEL,
    DEFAULT_EMBEDDING_MODEL
)
from src.services import get_service


def render_sidebar():
  services = get_service()

  with st.sidebar:
    st.markdown("### **λ Lambda Notebook**")
    st.caption("Docs Reviewer — Protótipo de Interface")
    st.divider()

    # Configuração de API e Modelos (Modo Demonstrativo)
    if demonstrative_mode():
      st.warning("⚠️ **Modo Demonstrativo Ativo**\n(Sem chave de API informada)")
      with st.expander("⚙️ **Configurar API & Modelos**", expanded=True):
        st.caption("Configure uma API Key e escolha os modelos para habilitar o modo real.")

        # Campo de API Key
        api_key_input = st.text_input(
            "🔑 Gemini API Key",
            type="password",
            placeholder="Insira sua Gemini API Key...",
            help="Obtenha sua chave no Google AI Studio (aistudio.google.com)",
            key="sidebar_api_key_input"
        )

        # Modelo de Chat (LLM)
        current_chat_model = get_llm_model() or DEFAULT_LLM_MODEL
        chat_options = [
            "gemini-3.8-flash",
            "gemini-3.1-flash-lite",
            "gemini-3.5-flash-lite",
            "gemini-3.1-pro-preview",
            "gemini-3-flash-preview",
            "gemini-4-argon",
        ]
        if current_chat_model not in chat_options:
          chat_options.insert(0, current_chat_model)
        chat_idx = chat_options.index(current_chat_model)

        chat_model_val = st.selectbox(
            "💬 Modelo de Chat (LLM)",
            options=chat_options,
            index=chat_idx,
            accept_new_options=True,
            key="sidebar_chat_model_select",
            help="Selecione um modelo da lista ou digite o nome de um modelo novo/customizado diretamente no campo."
        )

        # Modelo de Embeddings
        current_emb_model = get_embedding_model() or DEFAULT_EMBEDDING_MODEL
        emb_options = [
            "models/gemini-embedding-2",
            "models/gemini-embedding-001",
        ]
        if current_emb_model not in emb_options:
          emb_options.insert(0, current_emb_model)
        emb_idx = emb_options.index(current_emb_model)

        emb_model_val = st.selectbox(
            "🧩 Modelo de Embeddings",
            options=emb_options,
            index=emb_idx,
            accept_new_options=True,
            key="sidebar_emb_model_select",
            help="Selecione um modelo da lista ou digite o nome de um modelo novo/customizado diretamente no campo."
        )

        # Aplica os modelos selecionados no config
        if chat_model_val and chat_model_val.strip():
          set_llm_model(chat_model_val.strip())
        if emb_model_val and emb_model_val.strip():
          set_embedding_model(emb_model_val.strip())

        # Botão para ativar a API Key informada
        if st.button("🚀 Ativar Chave & Modelos", type="primary", use_container_width=True):
          if api_key_input and api_key_input.strip():
            key_clean = api_key_input.strip()
            set_llm_api_key(key_clean)
            st.session_state["llm_api_key"] = key_clean

            chat_final = chat_model_val.strip() if chat_model_val else DEFAULT_LLM_MODEL
            set_llm_model(chat_final)
            st.session_state["llm_model"] = chat_final

            emb_final = emb_model_val.strip() if emb_model_val else DEFAULT_EMBEDDING_MODEL
            set_embedding_model(emb_final)
            st.session_state["embedding_model"] = emb_final

            # Limpa estado de navegação do modo mockado para recarregar o banco real limpo
            st.session_state.pop("active_notebook_id", None)
            st.session_state.pop("notebooks", None)

            st.success("API Key e modelos configurados com sucesso!")
            st.rerun()
          else:
            st.error("Informe uma API Key válida.")

      st.divider()
    else:
      with st.expander("🔑 **API Conectada**", expanded=False):
        st.success("🟢 Modo Real Ativo")
        st.caption(f"**Chat:** `{get_llm_model()}`")
        st.caption(f"**Embeddings:** `{get_embedding_model()}`")
        if st.button("Desconectar Chave (Modo Demo)", use_container_width=True):
          set_llm_api_key("")
          st.session_state.pop("llm_api_key", None)
          st.session_state.pop("active_notebook_id", None)
          st.session_state.pop("notebooks", None)
          st.toast("Modo demonstrativo reativado.")
          st.rerun()
      st.divider()

    # Formulário para Criar Novo Notebook
    with st.expander("➕ **Novo Notebook**", expanded=False):
      with st.form("form_create_notebook", clear_on_submit=True):
        new_name = st.text_input("Nome do Notebook", placeholder="Ex: Pesquisa de Mercado")
        new_desc = st.text_area("Descrição (opcional)", placeholder="Breve resumo dos documentos e objetivos...")
        submitted = st.form_submit_button("Criar Notebook", use_container_width=True)
        if submitted:
          if new_name.strip():
            nb = services.create_notebook(name=new_name.strip(), description=new_desc.strip())
            st.success(f"Notebook '{new_name}' criado!")
            st.rerun()
          else:
            st.error("Informe um nome válido.")

    # Listagem de Notebooks
    st.markdown("#### :material/folder: **Pastas (Notebooks)**")
    notebooks = services.get_all_notebooks()

    if not notebooks:
      st.info("Nenhum notebook cadastrado.")
      if demonstrative_mode():
        if st.button("Carregar Dados de Exemplo"):
          services.reset_mock_state()
          st.rerun()
      return

    active_id = st.session_state.get("active_notebook_id")

    for nb in notebooks:
      docs = services.get_documents(nb.id)
      is_active = (nb.id == active_id)
      col1, col2 = st.columns([0.82, 0.18])

      with col1:
        btn_label = f"{':material/folder_open: ' if is_active else ':material/folder: '} {nb.name}"
        if st.button(
          btn_label,
          key=f"nb_btn_{nb.id}",
          use_container_width=True,
          type="primary" if is_active else "secondary"
        ):
          st.session_state["active_notebook_id"] = nb.id
          st.rerun()

      with col2:
        if st.button(":material/delete:", key=f"del_nb_{nb.id}", help="Excluir este notebook"):
          services.delete_notebook(nb.id)
          st.toast("Notebook excluído.")
          st.rerun()

    st.divider()

    if demonstrative_mode():
      # Botão para restaurar dados mockados
      if st.button("Restaurar Dados Demonstrativos", use_container_width=True):
        services.reset_mock_state()
        st.toast("Dados de demonstração restaurados!")
        st.rerun()
