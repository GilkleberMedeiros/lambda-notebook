from email.encoders import encode_noop
from pathlib import Path
from streamlit.typing import UploadedFile

from src.database.db import get_session
from src.database.models import Notebook, Document
from src.database.repository import add_one, delete

from src.rag import vector_store as vstore


def create_notebook(name: str, description: str = None):
  with get_session() as session:
    nb = add_one(model=Notebook, session=session, name=name, description=description)
    _ = vstore.create_collection(make_nb_collection_name(nb.id))

    return nb

def get_notebook(notebook_id: int):
  with get_session() as session:
    return session.get(Notebook, notebook_id)

def get_all_notebooks():
  with get_session() as session:
    return session.query(Notebook).all()

def delete_notebook(notebook_id: int):
  with get_session() as session:
    delete(model=Notebook, session=session, instance_id=notebook_id)
    coll_name = make_nb_collection_name(notebook_id)
    vstore.delete_collection(coll_name)


def add_document(notebook_id: int, file: UploadedFile):
  with get_session() as session:
    notebook = session.get(Notebook, notebook_id)
    if notebook:
      filename = file.name
      file_size_kb = round(file.size / 1024, 1)
      file_ext = Path(file.name).suffix.upper().replace(".", "")

      document = add_one(
        model=Document,
        session=session,
        notebook_id=notebook_id,
        name=filename,
        file_type=file_ext,
        file_size_kb=file_size_kb,
        chunk_count=0
      )

      # TODO: Adicionar embedding usando modelo próprio. 
      file_content = file.read().decode()
      coll_name = make_nb_collection_name(notebook_id)
      
      # Define sempre chunk_index=0 e page=1 antes de implementar modelo de embedding próprio.
      doc = vstore.add_registry(coll_name, {
        "ids": [document.id], 
        "documents": [file_content], 
        "metadatas": [{"document_id": document.id, "filename": filename, "page": 1, "chunk_index": 0}]
      })
      if doc is None:
        raise Exception("Não foi possível salvar o arquivo no banco de embeddings.")
      
      return document
    else:
      return None

def get_documents(notebook_id: int) -> list[Document]:
  with get_session() as session:
    notebook = session.get(Notebook, notebook_id)
    if notebook:
      return notebook.documents
    else:
      return []

def delete_document(notebook_id: int, document_id: any):
  with get_session() as session:
    notebook = session.get(Notebook, notebook_id)
    if not notebook:
      raise Exception("Notebook com o notebook_id informado não existe!")

    delete(Document, session, document_id)
    coll_name = make_nb_collection_name(notebook_id)
    vstore.delete_registry(coll_name, {"document_id": document_id})


def make_nb_collection_name(notebook_id: int) -> str:
  return f"notebook_{notebook_id}"