import copy
import time
from pathlib import Path
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Generator
import streamlit as st
from streamlit.typing import UploadedFile

from src.database.models import ChatMessage, Notebook, Document
from src.services import _BaseServices


# Permite acesso via colchetes e get aos modelos para manter compatibilidade com componentes legados
if not hasattr(Notebook, "__getitem__"):
    def _nb_getitem(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        raise KeyError(key)
    Notebook.__getitem__ = _nb_getitem

if not hasattr(Notebook, "__setitem__"):
    def _nb_setitem(self, key, value):
        setattr(self, key, value)
    Notebook.__setitem__ = _nb_setitem

if not hasattr(Notebook, "get"):
    def _nb_get(self, key, default=None):
        return getattr(self, key, default)
    Notebook.get = _nb_get

if not hasattr(Document, "__getitem__"):
    def _doc_getitem(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        raise KeyError(key)
    Document.__getitem__ = _doc_getitem

if not hasattr(Document, "__setitem__"):
    def _doc_setitem(self, key, value):
        setattr(self, key, value)
    Document.__setitem__ = _doc_setitem

if not hasattr(Document, "get"):
    def _doc_get(self, key, default=None):
        return getattr(self, key, default)
    Document.get = _doc_get


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


def create_initial_notebooks() -> List[Notebook]:
    notebooks = []
    for nb_data in INITIAL_NOTEBOOKS_DATA:
        raw_id = nb_data["id"]
        nb_id = int(raw_id.replace("nb-", "")) if isinstance(raw_id, str) and raw_id.startswith("nb-") else int(raw_id)
        
        try:
            created_at = datetime.strptime(nb_data["created_at"], "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
        except Exception:
            created_at = datetime.now(timezone.utc)

        nb = Notebook(
            id=nb_id,
            name=nb_data["name"],
            description=nb_data.get("description"),
            created_at=created_at,
            updated_at=created_at,
        )

        for doc_data in nb_data.get("documents", []):
            raw_doc_id = doc_data["id"]
            doc_id = int(raw_doc_id.replace("doc-", "")) if isinstance(raw_doc_id, str) and raw_doc_id.startswith("doc-") else int(raw_doc_id)
            try:
                doc_created_at = datetime.strptime(doc_data["created_at"], "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
            except Exception:
                doc_created_at = datetime.now(timezone.utc)

            doc = Document(
                id=doc_id,
                notebook_id=nb_id,
                name=doc_data["name"],
                file_type=doc_data["file_type"],
                file_path=doc_data["name"],
                chunk_count=doc_data.get("chunk_count", 0),
                created_at=doc_created_at,
            )
            doc.file_size_kb = doc_data.get("file_size_kb", 0.0)
            nb.documents.append(doc)

        nb.messages = copy.deepcopy(nb_data.get("messages", []))
        notebooks.append(nb)
    return notebooks


def _generate_notebook_id() -> int:
    MockServices.init_mock_state()
    all_nb_ids = [
        nb.id for nb in st.session_state["notebooks"]
        if isinstance(nb.id, int)
    ]
    return max(all_nb_ids, default=0) + 1


def _generate_document_id() -> int:
    MockServices.init_mock_state()
    all_doc_ids = [
        d.id for nb in st.session_state["notebooks"]
        for d in nb.documents
        if isinstance(d.id, int)
    ]
    return max(all_doc_ids, default=100) + 1

def _generate_message_id() -> int:
    MockServices.init_mock_state()
    all_messages_ids = [
        d.id for nb in st.session_state["notebooks"]
        for d in nb.messages
        if isinstance(d.id, int)
    ]
    return max(all_messages_ids, default=100) + 1


class MockServices(_BaseServices):
    uses_mock_services = True

    @staticmethod
    def init_mock_state():
        """Inicializa os dados mockados no st.session_state se ainda não existirem."""
        if "notebooks" not in st.session_state or (
            st.session_state["notebooks"] and isinstance(st.session_state["notebooks"][0], dict)
        ):
            st.session_state["notebooks"] = create_initial_notebooks()
        if "active_notebook_id" not in st.session_state or st.session_state["active_notebook_id"] == "nb-1":
            st.session_state["active_notebook_id"] = 1

    @staticmethod
    def reset_mock_state():
        """Restaura os dados mockados para o estado original."""
        st.session_state["notebooks"] = create_initial_notebooks()
        st.session_state["active_notebook_id"] = 1

    @staticmethod
    def get_all_notebooks() -> List[Notebook]:
        MockServices.init_mock_state()
        return st.session_state["notebooks"]

    @staticmethod
    def get_notebook(notebook_id: Any) -> Optional[Notebook]:
        MockServices.init_mock_state()
        for nb in st.session_state["notebooks"]:
            if (
                nb.id == notebook_id
                or str(nb.id) == str(notebook_id)
                or f"nb-{nb.id}" == str(notebook_id)
            ):
                return nb
        return None

    @staticmethod
    def create_notebook(name: str, description: str = None) -> Notebook:
        MockServices.init_mock_state()
        now = datetime.now(timezone.utc)
        new_nb = Notebook(
            id=_generate_notebook_id(),
            name=name,
            description=description,
            created_at=now,
            updated_at=now,
        )
        new_nb.documents = []
        new_nb.messages = []
        st.session_state["notebooks"].insert(0, new_nb)
        st.session_state["active_notebook_id"] = new_nb.id
        return new_nb

    @staticmethod
    def delete_notebook(notebook_id: Any):
        MockServices.init_mock_state()
        st.session_state["notebooks"] = [
            nb for nb in st.session_state["notebooks"]
            if (
                nb.id != notebook_id
                and str(nb.id) != str(notebook_id)
                and f"nb-{nb.id}" != str(notebook_id)
            )
        ]
        current_active = st.session_state.get("active_notebook_id")
        if (
            current_active == notebook_id
            or str(current_active) == str(notebook_id)
            or (current_active is not None and f"nb-{current_active}" == str(notebook_id))
            or (isinstance(notebook_id, str) and notebook_id.startswith("nb-") and str(current_active) == notebook_id.replace("nb-", ""))
        ):
            remaining = st.session_state["notebooks"]
            st.session_state["active_notebook_id"] = remaining[0].id if remaining else None

    @staticmethod
    def get_documents(notebook_id: Any) -> List[Document]:
        nb = MockServices.get_notebook(notebook_id)
        return nb.documents if nb else []

    @staticmethod
    def add_document(notebook_id: Any, file: UploadedFile) -> Optional[Document]:
        nb = MockServices.get_notebook(notebook_id)
        if not nb:
            return None

        filename = file.name
        try:
            file_size_bytes = file.size
        except AttributeError:
            file_size_bytes = len(file.getvalue()) if hasattr(file, "getvalue") else 0

        file_size_kb = round(file_size_bytes / 1024, 1)
        file_ext = Path(file.name).suffix.upper().replace(".", "")
        estimated_chunks = max(3, int(file_size_kb // 15) + 1)

        new_doc = Document(
            id=_generate_document_id(),
            notebook_id=nb.id,
            name=filename,
            file_type=file_ext,
            file_path=filename,
            chunk_count=estimated_chunks,
            created_at=datetime.now(timezone.utc),
        )
        new_doc.file_size_kb = file_size_kb
        nb.documents.insert(0, new_doc)
        return new_doc

    @staticmethod
    def delete_document(notebook_id: Any, document_id: Any):
        nb = MockServices.get_notebook(notebook_id)
        if not nb:
            raise Exception("Notebook com o notebook_id informado não existe!")
        nb.documents = [
            d for d in nb.documents
            if (
                d.id != document_id
                and str(d.id) != str(document_id)
                and f"doc-{d.id}" != str(document_id)
            )
        ]

    @staticmethod
    def get_messages(notebook_id: Any) -> List[ChatMessage]:
        nb = MockServices.get_notebook(notebook_id)
        return [ ChatMessage(**m) for m in nb["messages"] ] if nb else []

    @staticmethod
    def add_message(notebook_id: Any, role: str, content: str, sources: Optional[List[Dict[str, Any]]] = None):
        nb = MockServices.get_notebook(notebook_id)
        if not nb:
            return
        new_msg = {
            "id": _generate_message_id(),
            "role": role,
            "content": content,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "sources": sources or []
        }
        nb["messages"].append(new_msg)

        return ChatMessage(**new_msg)

    @staticmethod
    def clear_messages(notebook_id: Any):
        nb = MockServices.get_notebook(notebook_id)
        if not nb:
            return
        nb["messages"] = []

    @staticmethod
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

    @staticmethod
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
