import streamlit as st
from src.config import demonstrative_mode
from src.services import (
  get_all_notebooks,
  create_notebook,
  delete_notebook,
  get_documents,
)

if demonstrative_mode():
  from src.mock_data import (
    get_all_notebooks,
    create_notebook,
    delete_notebook,
    get_documents,
    reset_mock_state
)

def render_sidebar():
  with st.sidebar:
    st.markdown("### 📓 **Gemini Notebook**")
    st.caption("Docs Reviewer — Protótipo de Interface")
    st.divider()

    # Formulário para Criar Novo Notebook
    with st.expander("➕ **Novo Notebook**", expanded=False):
      with st.form("form_create_notebook", clear_on_submit=True):
        new_name = st.text_input("Nome do Notebook", placeholder="Ex: Pesquisa de Mercado")
        new_desc = st.text_area("Descrição (opcional)", placeholder="Breve resumo dos documentos e objetivos...")
        submitted = st.form_submit_button("Criar Notebook", use_container_width=True)
        if submitted:
          if new_name.strip():
            nb = create_notebook(name=new_name.strip(), description=new_desc.strip())
            st.success(f"Notebook '{new_name}' criado!")
            st.rerun()
          else:
            st.error("Informe um nome válido.")

    # Listagem de Notebooks
    st.markdown("#### 📁 **Pastas (Notebooks)**")
    notebooks = get_all_notebooks()

    if not notebooks:
      st.info("Nenhum notebook cadastrado.")
      if demonstrative_mode():
        if st.button("Carregar Dados de Exemplo"):
          reset_mock_state()
          st.rerun()
      return

    active_id = st.session_state.get("active_notebook_id")

    for nb in notebooks:
      docs = get_documents(nb["id"])
      is_active = (nb["id"] == active_id)
      col1, col2 = st.columns([0.82, 0.18])

      with col1:
        btn_label = f"{'🔹 ' if is_active else '📁 '} {nb['name']} ({len(docs)})"
        if st.button(
          btn_label,
          key=f"nb_btn_{nb['id']}",
          use_container_width=True,
          type="primary" if is_active else "secondary"
        ):
          st.session_state["active_notebook_id"] = nb["id"]
          st.rerun()

      with col2:
        if st.button("🗑️", key=f"del_nb_{nb['id']}", help="Excluir este notebook"):
          delete_notebook(nb["id"])
          st.toast("Notebook excluído.")
          st.rerun()

    st.divider()

    if demonstrative_mode():
      # Botão para restaurar dados mockados
      if st.button("🔄 Restaurar Dados Demonstrativos", use_container_width=True):
        reset_mock_state()
        st.toast("Dados de demonstração restaurados!")
        st.rerun()
