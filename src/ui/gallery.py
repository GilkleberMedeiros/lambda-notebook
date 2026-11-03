import streamlit as st

from src.config import demonstrative_mode
from src.services import (
    get_notebook, 
    get_documents, 
    add_document, 
    delete_document
)

if demonstrative_mode():
    from src.mock_data import (
        get_notebook,
        get_documents,
        add_document,
        delete_document
    )


def render_gallery(notebook_id: str):
    notebook = get_notebook(notebook_id)
    if not notebook:
        st.warning("Selecione um notebook na barra lateral.")
        return

    documents = get_documents(notebook_id)
    total_chunks = sum(doc.get("chunk_count", 0) for doc in documents)

    # Cabeçalho do Notebook Selecionado
    col_t1, col_t2 = st.columns([0.7, 0.3])
    with col_t1:
        st.markdown(f"## 📁 {notebook['name']}")
        if notebook.get("description"):
            st.caption(notebook["description"])
    with col_t2:
        m1, m2 = st.columns(2)
        m1.metric("Documentos", len(documents))
        m2.metric("Chunks Indexados", total_chunks)

    st.divider()

    # Seção de Upload / Adição de Fontes
    with st.expander("📤 **Adicionar Documentos / Fontes**", expanded=False):
        uploaded_files = st.file_uploader(
            "Selecione arquivos (.pdf, .docx, .txt, .md)",
            type=["pdf", "docx", "txt", "md"],
            accept_multiple_files=True
        )

        if uploaded_files:
            if st.button("Processar e Ingerir Fontes", type="primary"):
                progress_bar = st.progress(0, text="Processando documentos...")
                for idx, file in enumerate(uploaded_files):
                    

                    add_document(
                        notebook_id=notebook_id,
                        file=file
                    )
                    progress_bar.progress((idx + 1) / len(uploaded_files), text=f"Indexado: {file.name}")

                st.success(f"{len(uploaded_files)} fonte(s) adicionada(s) à galeria!")
                st.rerun()

    # Galeria de Fontes
    st.markdown("### 📚 **Galeria de Fontes no Notebook**")

    if not documents:
        st.info("Nenhuma fonte adicionada a este notebook ainda. Use a caixa de upload acima para enviar documentos.")
        return

    # Renderiza em cards (grid de 3 colunas)
    cols = st.columns(3)
    for idx, doc in enumerate(documents):
        col = cols[idx % 3]
        file_type = doc.get("file_type", "TXT").lower()
        badge_class = f"badge-{file_type}" if file_type in ["pdf", "docx", "txt", "md"] else "badge-txt"

        with col:
            with st.container(border=True):
                st.markdown(f"<span class='{badge_class}'>{doc.get('file_type', 'DOC')}</span>", unsafe_allow_html=True)
                st.markdown(f"**{doc['name']}**")
                st.caption(f"📅 {doc.get('created_at', '')} | 💾 {doc.get('file_size_kb', 0)} KB")
                st.caption(f"🧩 {doc.get('chunk_count', 0)} blocos indexados")

                c1, c2 = st.columns([0.6, 0.4])
                with c1:
                    with st.popover("Detalhes"):
                        st.markdown(f"**ID:** `{doc['id']}`")
                        st.markdown(f"**Nome:** `{doc['name']}`")
                        st.markdown(f"**Formato:** {doc.get('file_type')}")
                        st.markdown(f"**Chunks:** {doc.get('chunk_count')}")
                with c2:
                    if st.button("🗑️", key=f"del_doc_{doc['id']}", help="Excluir documento"):
                        delete_document(notebook_id, doc["id"])
                        st.toast(f"Documento '{doc['name']}' removido.")
                        st.rerun()
