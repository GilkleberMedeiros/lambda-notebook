import copy
import time
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional, Generator
import streamlit as st

INITIAL_NOTEBOOKS_DATA = [
    {
        "id": "nb-1",
        "name": "Pesquisa em Inteligência Artificial & RAG",
        "description": "Compilado de artigos técnicos e benchmarks sobre Retrieval-Augmented Generation e modelos multimodais.",
        "created_at": "2026-10-31 14:30",
        "documents": [
            {
                "id": "doc-101",
                "name": "Guia_Completo_RAG_Avancado.pdf",
                "file_type": "PDF",
                "chunk_count": 28,
                "file_size_kb": 420.5,
                "created_at": "2026-10-31 14:32"
            },
            {
                "id": "doc-102",
                "name": "Relatorio_Modelos_Gemini_2026.docx",
                "file_type": "DOCX",
                "chunk_count": 16,
                "file_size_kb": 185.0,
                "created_at": "2026-10-31 14:35"
            },
            {
                "id": "doc-103",
                "name": "Boas_Praticas_Chunking_Embeddings.md",
                "file_type": "MD",
                "chunk_count": 9,
                "file_size_kb": 45.2,
                "created_at": "2026-10-31 14:40"
            }
        ],
        "messages": [
            {
                "id": "msg-1",
                "role": "user",
                "content": "Quais são as principais recomendações para otimização de busca em arquiteturas RAG segundo os documentos?",
                "created_at": "2026-10-31 14:45",
                "sources": []
            },
            {
                "id": "msg-2",
                "role": "assistant",
                "content": "Com base nos documentos disponíveis neste notebook, as principais recomendações são:\n\n1. **Estratégia de Chunking Híbrido:** Recomenda-se utilizar blocos de 500 a 1000 tokens com sobreposição (*overlap*) de 10% a 20% para preservar o contexto semântico entre seções.\n2. **Reranking Semântico:** Aplicar uma etapa secundária de reordenação (ex: Cross-Encoders) após o resgate inicial vetorial reduz falsos positivos e eleva a precisão do contexto.\n3. **Isolamento de Metadados:** Filtrar por metadados de documento e seção antes da busca densa acelera a recuperação e garante isolamento entre domínios.",
                "created_at": "2026-10-31 14:46",
                "sources": [
                    {
                        "document_name": "Guia_Completo_RAG_Avancado.pdf",
                        "page": "Página 14",
                        "snippet": "A implementação de reranking após a consulta vetorial eleva em até 35% a acurácia das respostas finais."
                    },
                    {
                        "document_name": "Boas_Praticas_Chunking_Embeddings.md",
                        "page": "Seção 2.1",
                        "snippet": "Recomenda-se chunk_size entre 800 e 1000 tokens com 150 tokens de overlap para textos técnicos."
                    }
                ]
            }
        ]
    },
    {
        "id": "nb-2",
        "name": "Arquitetura de Software e Microsserviços",
        "description": "Documentação técnica sobre design patterns, comunicação assíncrona com RabbitMQ/Kafka e observabilidade.",
        "created_at": "2026-10-31 15:10",
        "documents": [
            {
                "id": "doc-201",
                "name": "Padroes_Microservicos_Resiliencia.pdf",
                "file_type": "PDF",
                "chunk_count": 34,
                "file_size_kb": 560.8,
                "created_at": "2026-10-31 15:12"
            },
            {
                "id": "doc-202",
                "name": "Manual_Arquitetura_Hexagonal.txt",
                "file_type": "TXT",
                "chunk_count": 12,
                "file_size_kb": 68.4,
                "created_at": "2026-10-31 15:15"
            }
        ],
        "messages": [
            {
                "id": "msg-201",
                "role": "user",
                "content": "Como implementar o padrão Circuit Breaker para evitar falhas em cascata?",
                "created_at": "2026-10-31 15:20",
                "sources": []
            },
            {
                "id": "msg-202",
                "role": "assistant",
                "content": "De acordo com o documento *Padroes_Microservicos_Resiliencia.pdf*, o padrão Circuit Breaker deve operar em três estados fundamentais:\n\n- **Closed (Fechado):** As requisições fluem normalmente até que a taxa de erros atinja o limiar configurado.\n- **Open (Aberto):** As requisições falham imediatamente (*fast-fail*), poupando o serviço dependente sobrecarregado.\n- **Half-Open (Semi-aberto):** Um número limitado de requisições de teste é permitido para verificar se o serviço se recuperou.",
                "created_at": "2026-10-31 15:21",
                "sources": [
                    {
                        "document_name": "Padroes_Microservicos_Resiliencia.pdf",
                        "page": "Capítulo 5, p. 42",
                        "snippet": "O Circuit Breaker monitora falhas de rede e timeouts; quando ultrapassa o limiar de 50%, transiciona para o estado Open."
                    }
                ]
            }
        ]
    },
    {
        "id": "nb-3",
        "name": "Planejamento Estratégico & OKRs 2026",
        "description": "Metas corporativas, análise SWOT e diretrizes de crescimento para o ano vigente.",
        "created_at": "2026-10-31 16:00",
        "documents": [],
        "messages": []
    }
]

def init_mock_state():
    """Inicializa os dados mockados no st.session_state se ainda não existirem."""
    if "notebooks" not in st.session_state:
        st.session_state["notebooks"] = copy.deepcopy(INITIAL_NOTEBOOKS_DATA)
    if "active_notebook_id" not in st.session_state:
        st.session_state["active_notebook_id"] = "nb-1"

def reset_mock_state():
    """Restaura os dados mockados para o estado original."""
    st.session_state["notebooks"] = copy.deepcopy(INITIAL_NOTEBOOKS_DATA)
    st.session_state["active_notebook_id"] = "nb-1"

def get_all_notebooks() -> List[Dict[str, Any]]:
    init_mock_state()
    return st.session_state["notebooks"]

def get_notebook(notebook_id: str) -> Optional[Dict[str, Any]]:
    init_mock_state()
    for nb in st.session_state["notebooks"]:
        if nb["id"] == notebook_id:
            return nb
    return None

def create_notebook(name: str, description: str = "") -> Dict[str, Any]:
    init_mock_state()
    new_nb = {
        "id": f"nb-{uuid.uuid4().hex[:6]}",
        "name": name,
        "description": description,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "documents": [],
        "messages": []
    }
    st.session_state["notebooks"].insert(0, new_nb)
    st.session_state["active_notebook_id"] = new_nb["id"]
    return new_nb

def delete_notebook(notebook_id: str):
    init_mock_state()
    st.session_state["notebooks"] = [nb for nb in st.session_state["notebooks"] if nb["id"] != notebook_id]
    if st.session_state.get("active_notebook_id") == notebook_id:
        remaining = st.session_state["notebooks"]
        st.session_state["active_notebook_id"] = remaining[0]["id"] if remaining else None

def get_documents(notebook_id: str) -> List[Dict[str, Any]]:
    nb = get_notebook(notebook_id)
    return nb["documents"] if nb else []

def add_mock_document(notebook_id: str, name: str, file_type: str, file_size_kb: float, chunk_count: int = 15):
    nb = get_notebook(notebook_id)
    if not nb:
        return
    new_doc = {
        "id": f"doc-{uuid.uuid4().hex[:6]}",
        "name": name,
        "file_type": file_type.upper(),
        "chunk_count": chunk_count,
        "file_size_kb": file_size_kb,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    nb["documents"].insert(0, new_doc)

def delete_document(notebook_id: str, document_id: str):
    nb = get_notebook(notebook_id)
    if not nb:
        return
    nb["documents"] = [d for d in nb["documents"] if d["id"] != document_id]

def get_messages(notebook_id: str) -> List[Dict[str, Any]]:
    nb = get_notebook(notebook_id)
    return nb["messages"] if nb else []

def add_message(notebook_id: str, role: str, content: str, sources: Optional[List[Dict[str, Any]]] = None):
    nb = get_notebook(notebook_id)
    if not nb:
        return
    new_msg = {
        "id": f"msg-{uuid.uuid4().hex[:6]}",
        "role": role,
        "content": content,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "sources": sources or []
    }
    nb["messages"].append(new_msg)

def clear_messages(notebook_id: str):
    nb = get_notebook(notebook_id)
    if not nb:
        return
    nb["messages"] = []

def simulate_mock_stream(query: str, active_doc_names: Optional[List[str]] = None) -> Generator[str, None, None]:
    """Gera uma resposta simulada por streaming para a UI."""
    doc_ref = active_doc_names[0] if active_doc_names else "Documento_Referencia.pdf"
    
    response_text = (
        f"Com base na análise dos documentos contidos neste notebook:\n\n"
        f"📌 **Tópico Analisado:** Em relação à sua dúvida sobre *\"{query}\"*:\n\n"
        f"1. **Ponto Central:** As fontes indicam que a metodologia recomendada deve priorizar a consistência, estrutura e rastreabilidade dos dados.\n"
        f"2. **Aplicação Prática:** Recomenda-se validar as premissas estabelecidas no material de apoio antes de prosseguir com a implementação.\n"
        f"3. **Observação das Fontes:** Conforme abordado em **{doc_ref}**, as conclusões apontam ganhos de eficiência significativos quando os padrões propostos são seguidos."
    )
    
    words = response_text.split(" ")
    for word in words:
        yield word + " "
        time.sleep(0.03)

def generate_mock_sources(active_doc_names: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Retorna fontes citadas mockadas para exibição nos cartões expansíveis da UI."""
    if active_doc_names and len(active_doc_names) > 0:
        return [
            {
                "document_name": active_doc_names[0],
                "page": "Página 8, Seção 2",
                "snippet": "A consistência das informações apresentadas é essencial para a tomada de decisão estruturada."
            }
        ]
    return [
        {
            "document_name": "Guia_Completo_RAG_Avancado.pdf",
            "page": "Página 14",
            "snippet": "A implementação de reranking após a consulta vetorial eleva em até 35% a acurácia das respostas finais."
        },
        {
            "document_name": "Boas_Praticas_Chunking_Embeddings.md",
            "page": "Seção 2.1",
            "snippet": "Recomenda-se chunk_size entre 800 e 1000 tokens com 150 tokens de overlap para textos técnicos."
        }
    ]
