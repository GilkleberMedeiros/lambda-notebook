import streamlit as st
from src.config import CHAT_HISTORY_CONTEXT_WINDOW_SIZE
from src.services import get_service

services = get_service()

def render_chat(notebook_id: str):
    documents = services.get_documents(notebook_id)

    # Cabeçalho do Chat e Ações
    col_h1, col_h2 = st.columns([0.7, 0.3])
    with col_h1:
        st.markdown("### 💬 **Perguntas & Respostas**")
        st.caption("Converse e extraia insights com base nos documentos do seu notebook.")
    with col_h2:
        if st.button("🧹 Limpar Histórico", use_container_width=True, help="Zera as mensagens deste notebook"):
            services.clear_messages(notebook_id)
            st.toast("Histórico limpo!")
            st.rerun()

    # Filtro de Fontes Ativas
    selected_docs = []
    if documents:
        with st.expander("🎯 **Filtrar Fontes Ativas para a Pergunta** (Opcional)", expanded=False):
            selected_docs = st.multiselect(
                "Selecione quais documentos devem compor o contexto (deixe vazio para todos):",
                options=documents,
                format_func=lambda d: d.name,
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
    messages = services.get_messages(notebook_id)

    if not messages:
        st.info("👋 Nenhuma conversa iniciada neste notebook. Envie uma pergunta abaixo ou clique em uma das sugestões acima!")

    for msg in messages:
        with st.chat_message(msg.role):
            st.markdown(msg.content)
            sources = msg.sources or []
            if sources:
                with st.expander(f"🔍 Fontes consultadas ({len(sources)})", expanded=False):
                    for src in sources:
                        doc_name = src.get("name", "Documento")
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
        services.add_message(notebook_id=notebook_id, role="user", content=query_to_run)

        # Simula resposta do assistente via streaming
        with st.chat_message("assistant"):
            chat_history = messages[:CHAT_HISTORY_CONTEXT_WINDOW_SIZE+1]
            active_selection = selected_docs if selected_docs else documents
            active_selection_ids = [ doc.id for doc in active_selection ]
            contextualized_q = services.recontextualize_query(query_to_run, chat_history)
            llm_response = services.query_llm(contextualized_q, notebook_id, chat_history, active_selection_ids)
            stream_response = (char for char in llm_response["response"])
            
            full_response = st.write_stream(stream_response)
            retrieved_sources = llm_response["sources"]

            if retrieved_sources:
                with st.expander(f"🔍 Fontes consultadas ({len(retrieved_sources)})", expanded=True):
                    for src in retrieved_sources:
                        doc_name = src.get("name", "Documento")
                        page = src.get("page", "")
                        snippet = src.get("snippet", "")
                        st.markdown(f"**📄 {doc_name}** `({page})`")
                        if snippet:
                            st.caption(f"> \"{snippet}\"")
                        st.markdown("---")

        # Salva resposta do assistente no histórico mockado
        services.add_message(
            notebook_id=notebook_id,
            role="assistant",
            content=full_response,
            sources=retrieved_sources
        )

        st.rerun()
