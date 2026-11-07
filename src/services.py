from pathlib import Path
from typing import Literal, Protocol
from datetime import datetime
from sqlalchemy import select, delete
from streamlit.typing import UploadedFile

from src.config import demonstrative_mode, CHAT_HISTORY_CONTEXT_WINDOW_SIZE
from src.database.db import get_session
from src.database.models import ChatMessage, Notebook, Document
from src.database import repository as repo

from src.rag import vector_store as vstore
from src.rag import ingestion
from src.utils import *


class _BaseServices(Protocol):
  uses_mock_services: bool

  @staticmethod
  def create_notebook(name: str, description: str = None) -> Notebook: ...

  @staticmethod
  def get_notebook(notebook_id: int) -> Notebook | None: ...

  @staticmethod
  def get_all_notebooks() -> list[Notebook]: ...

  @staticmethod
  def delete_notebook(notebook_id: int) -> None: ...

  @staticmethod
  def add_document(notebook_id: int, file: UploadedFile) -> Document | None: ...

  @staticmethod
  def get_documents(notebook_id: int) -> list[Document]: ...

  @staticmethod
  def delete_document(notebook_id: int, document_id: any) -> None: ...

  @staticmethod
  def get_messages(notebook_id: int) -> list[ChatMessage]: ...

  @staticmethod
  def add_message(notebook_id: int, role: Literal["user", "assistant"], content: str, sources: dict[str, any] = None) -> ChatMessage | None: ...

  @staticmethod
  def clear_messages(notebook_id: int) -> None: ...
    

class Services(_BaseServices): 
  uses_mock_services = False

  @staticmethod
  def create_notebook(name: str, description: str = None):
    with get_session() as session:
      nb = repo.add_one(model=Notebook, session=session, name=name, description=description)
      _ = vstore.create_collection(make_nb_collection_name(nb.id))
      __ = vstore.create_collection(make_nb_chat_collection_name(nb.id))

      return nb
  
  @staticmethod
  def get_notebook(notebook_id: int):
    with get_session() as session:
      return session.get(Notebook, notebook_id)
  
  @staticmethod
  def get_all_notebooks():
    with get_session() as session:
      return session.query(Notebook).all()
  
  @staticmethod
  def delete_notebook(notebook_id: int):
    with get_session() as session:
      repo.delete(model=Notebook, session=session, instance_id=notebook_id)
      coll_name = make_nb_collection_name(notebook_id)
      chat_coll_name = make_nb_chat_collection_name(notebook_id)
      vstore.delete_collection(coll_name)
      vstore.delete_collection(chat_coll_name)

  
  @staticmethod
  def add_document(notebook_id: int, file: UploadedFile):
    with get_session() as session:
      notebook = session.get(Notebook, notebook_id)
      if notebook:
        try:
          filename = file.name
          file_ext = Path(file.name).suffix.upper().replace(".", "")

          # Salva arquivo original em storage/notebooks
          file_bytes = file.read()
          p = Path(f"./src/storage/notebook/{notebook_id}")
          p.mkdir(parents=True, exist_ok=True)
          p = p.joinpath(filename)
          p.write_bytes(file_bytes)

          # Faz o embedding do arquivo
          docs = ingestion.load_documents([p])
          chunks = ingestion.split_documents(docs)
          chunks = [ chunk for nested in chunks for chunk in nested ]
          embeddings = ingestion.embed_documents(chunks)

          document = repo.add_one(
            model=Document,
            session=session,
            notebook_id=notebook_id,
            name=filename,
            file_type=file_ext,
            file_path=str(p.resolve()),
            chunk_count=len(chunks)
          )

          coll_name = make_nb_collection_name(notebook_id)
          
          # Salva os chunks + embeddings do documento no vector store
          for idx in range(len(chunks)):
            page = chunks[idx].metadata.get("page") or chunks[idx].metadata.get("page_number")
            page = page if page is not None else -1

            doc = vstore.add_registry(coll_name, {
              "ids": [f"doc-{document.id}_chunk-{idx}"], 
              "documents": [chunks[idx].page_content], 
              "embeddings": [embeddings[idx]],
              "metadatas": [{"document_id": document.id, "filename": filename, "page": page, "chunk_index": idx}]
            })
            if doc is None:
              raise Exception("Não foi possível salvar o arquivo no banco de embeddings.")
          
          return document
        except Exception as e: 
          # Deleta arquivo em caso de erro
          p = Path(f"./storage/notebook/{notebook_id}").joinpath(file.name)
          p.unlink(missing_ok=True)

          # Deleta o registro no vector_store em caso de erro
          coll_name = make_nb_collection_name(notebook_id)
          vstore.delete_registry(coll_name, {"document_id": document.id})

          # Repassa o erro para rollback no DB
          raise e
      else:
        return None
  
  @staticmethod
  def get_documents(notebook_id: int) -> list[Document]:
    with get_session() as session:
      notebook = session.get(Notebook, notebook_id)
      if notebook:
        return notebook.documents
      else:
        return []
  
  @staticmethod
  def delete_document(notebook_id: int, document_id: any):
    with get_session() as session:
      notebook = session.get(Notebook, notebook_id)
      if not notebook:
        raise Exception(f"Notebook com o notebook_id={notebook_id} não existe!")

      doc = session.get(Document, document_id)
      if not notebook:
        raise Exception(f"Document com o document_id={document_id} não existe!")

      repo.delete(Document, session, document_id)
      coll_name = make_nb_collection_name(notebook_id)
      vstore.delete_registry(coll_name, {"document_id": document_id})
      Path(doc.file_path).resolve().unlink(missing_ok=True)

  @staticmethod
  def get_messages(notebook_id: int) -> list[ChatMessage]: 
    with get_session() as session:
      notebook = session.get(Notebook, notebook_id)
      if not notebook:
        raise Exception(f"Notebook com o notebook_id={notebook_id} não existe!")

      smt = select(ChatMessage).where(ChatMessage.notebook_id == notebook.id)
      messages = session.scalars(smt).all()

      return messages

  @staticmethod
  def add_message(notebook_id: int, role: Literal["user", "assistant"], content: str, sources: dict[str, any]  = None): 
    with get_session() as session:
      notebook = session.get(Notebook, notebook_id)
      if not notebook:
        return None

      try:
        message = repo.add_one(ChatMessage, session, notebook_id=notebook.id, role=role, content=content, sources=sources)

        chunks = ingestion.split_documents([message.content])
        # Flaten chunks array
        chunks = [ chunk for nested in chunks for chunk in nested ]
        embeddings = ingestion.embed_documents(chunks)

        coll_name = make_nb_chat_collection_name(notebook_id)

        ids = []
        contents = []
        metadatas = []
        for idx, chunk in enumerate(chunks):
          ids.append(f"chatmsg-{message.id}_chunk-{idx}")
          cnt = chunk.page_content if isinstance(chunk, ingestion.Document) else chunk
          contents.append(cnt)
          metadatas.append({
            "chat_message_id": message.id, 
            "role": message.role, 
            "chunk_index": idx, 
            "created_at": message.created_at.isoformat()
          })

        msg = vstore.add_registry(coll_name, {
          "ids": ids,
          "documents": contents, 
          "embeddings": embeddings, 
          "metadatas": metadatas
        })
        if not msg:
          raise Exception("Não foi possível salvar a mensagem no banco de embeddings.")

        # Pega todos os registros e o tamanho da janela de contexto do chat
        r = vstore.get_all_registries(coll_name)
        if r is not None:
          f = lambda m: (m["created_at"], m["chat_message_id"])
          message_seq = { f(m) for m in r["metadatas"] }
          chat_context_size = len(message_seq)

          # Deleta as mensagens mais antigas quando o tamanho da janela de 
          # contexto é excedido
          if chat_context_size >= CHAT_HISTORY_CONTEXT_WINDOW_SIZE:
            diff = chat_context_size - CHAT_HISTORY_CONTEXT_WINDOW_SIZE
            for _ in range(diff):
              id = min(*message_seq, key=lambda v: datetime.fromisoformat(v[0]))
              vstore.delete_registry(coll_name, {"chat_message_id": id})

        return message

      except Exception as e:
        # Deleta o registro no vector_store em caso de erro
        coll_name = make_nb_chat_collection_name(notebook_id)
        vstore.delete_registry(coll_name, {"chat_message_id": message.id})

        # Repassa o erro para rollback no DB
        raise e

  @staticmethod
  def clear_messages(notebook_id: int):
    with get_session() as session:
      notebook = session.get(Notebook, notebook_id)
      if not notebook:
        raise Exception(f"Notebook com o notebook_id={notebook_id} não existe!")

      smt = delete(ChatMessage).where(ChatMessage.notebook_id == notebook_id)
      session.execute(smt)
      # Limpa os embeddings das mensagens
      coll_name = make_nb_chat_collection_name(notebook_id)
      vstore.delete_collection(coll_name)
      vstore.create_collection(coll_name)


def get_service():
  """
  Retorna os serviços.  Serviços Mock se estiver em modo demonstrativo 
  (sem chave de API LLM) ou os serviços reais se não estiver em modo 
  demonstrativo. 
  """

  if demonstrative_mode():
    from src.mock_services import MockServices
    return MockServices()
  
  return Services()

