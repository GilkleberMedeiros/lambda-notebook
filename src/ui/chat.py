import streamlit as st
from typing import List
from src.mock_data import (
    get_messages,
    add_message,
    clear_messages,
    get_documents,
    simulate_mock_stream,
    generate_mock_sources
)

def render_chat(notebook_id: str):
    documents = get_documents(notebook_id)
    doc_names = [d["name"] for d in documents]

    # Cabeçalho do Chat e Ações
    col_h1, col_h2 = st.columns([0.7, 0.3])
    with col_h1:
        st.markdown("### 💬 **Perguntas & Respostas**")
        st.caption("Converse e extraia insights com base nos documentos do seu notebook.")
    with col_h2:
        if st.button("🧹 Limpar Histórico", use_container_width=True, help="Zera as mensagens deste notebook"):
            clear_messages(notebook_id)
            st.toast("Histórico limpo!")
            st.rerun()

    # Filtro de Fontes Ativas
    selected_doc_names = []
    if doc_names:
        with st.expander("🎯 **Filtrar Fontes Ativas para a Pergunta** (Opcional)", expanded=False):
            selected_doc_names = st.multiselect(
                "Selecione quais documentos devem compor o contexto (deixe vazio para todos):",
                options=doc_names,
                default=[]
            )

    # Sugestões de Perguntas Rápidas
    st.markdown("##### ⚡ Perguntas Sugeridas")
    col_p1, col_p2, col_p3 = st.columns(3)
    prompt_suggestion = None
    with col_p1:
        if st.button("📑 Resumir principais pontos", use_container_width=True):
            prompt_suggestion = "Faça um resumo executivo dos pontos principais abordados nos documentos."
    with col_p2:
        if st.button("⚖️ Comparar abordagens", use_container_width=True):
            prompt_suggestion = "Compare as diferentes abordagens e metodologias descritas nas fontes."
    with col_p3:
        if st.button("🎯 Principais conclusões", use_container_width=True):
            prompt_suggestion = "Quais são as conclusões mais relevantes apresentadas pelos autores?"

    st.divider()

    # Histórico de Mensagens
    messages = get_messages(notebook_id)

    if not messages:
        st.info("👋 Nenhuma conversa iniciada neste notebook. Envie uma pergunta abaixo ou clique em uma das sugestões acima!")

    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            sources = msg.get("sources", [])
            if sources:
                with st.expander(f"🔍 Fontes consultadas ({len(sources)})", expanded=False):
                    for src in sources:
                        doc_name = src.get("document_name", "Documento")
                        page = src.get("page", "")
                        snippet = src.get("snippet", "")
                        st.markdown(f"**📄 {doc_name}** `({page})`")
                        if snippet:
                            st.caption(f"> \"{snippet}\"")
                        st.markdown("---")

    # Tratamento de Entrada do Usuário
    user_query = st.chat_input("Pergunte algo sobre os documentos do notebook...")
    query_to_run = prompt_suggestion or user_query

    if query_to_run:
        # Exibe mensagem do usuário
        with st.chat_message("user"):
            st.markdown(query_to_run)

        # Salva pergunta do usuário nos dados mockados
        add_message(notebook_id=notebook_id, role="user", content=query_to_run)

        # Simula resposta do assistente via streaming
        with st.chat_message("assistant"):
            active_selection = selected_doc_names if selected_doc_names else doc_names
            stream_gen = simulate_mock_stream(query=query_to_run, active_doc_names=active_selection)
            
            full_response = st.write_stream(stream_gen)
            retrieved_sources = generate_mock_sources(active_selection)

            if retrieved_sources:
                with st.expander(f"🔍 Fontes consultadas ({len(retrieved_sources)})", expanded=True):
                    for src in retrieved_sources:
                        doc_name = src.get("document_name", "Documento")
                        page = src.get("page", "")
                        snippet = src.get("snippet", "")
                        st.markdown(f"**📄 {doc_name}** `({page})`")
                        if snippet:
                            st.caption(f"> \"{snippet}\"")
                        st.markdown("---")

        # Salva resposta do assistente no histórico mockado
        add_message(
            notebook_id=notebook_id,
            role="assistant",
            content=full_response,
            sources=retrieved_sources
        )

        st.rerun()
