import chromadb
from streamlit.typing import UploadedFile


chroma_client = chromadb.PersistentClient("./src/storage/chromadb")


def create_collection(name: str): 
  return chroma_client.get_or_create_collection(name=name)

def get_collection(name: str):
  try:
    return chroma_client.get_collection(name=name)
  except Exception:
    return None

def delete_collection(name: str):
  try:
    chroma_client.delete_collection(name=name)
  except Exception:
    pass


def add_document(collection_name: str, document_id: str, file: UploadedFile): 
  collection = get_collection(collection_name)
  if not collection: 
    return 

  filename = file.name
  file_content = file.read().decode("utf-8")

  # TODO: Adicionar embedding usando modelo próprio. 

  # Define sempre chunk_index=0 e page=1 antes de implementar modelo de embedding próprio.
  collection.add(
    ids=[document_id],
    metadatas=[{"filename": filename, "chunk_index": 0, "page": 1, "document_id": document_id}],
    documents=[file_content]
  )

  return {"id": document_id, "document": file_content, "metadata": {"filename": filename, "chunk_index": 0, "page": 1, "document_id": document_id}}

def get_all_documents(collection_name: str):
  collection = get_collection(collection_name)
  if not collection:
    return []
  
  return collection.get()

def get_documents(collection_name: str, limit: int = None, offset: int = None, where_filter: dict = None): 
  collection = get_collection(collection_name)
  if not collection:
    return []
  
  return collection.get(where=where_filter)

def delete_document(collection_name: str, where_filter: dict = None):
  collection = get_collection(collection_name)
  if not collection:
    return
  
  collection.delete(where=where_filter)


def query_documents(collection_name: str, query_texts: list[str] = None, query_embeddings: list[str] = None, nresults: int = 5, where_filter: dict = None):
  collection = get_collection(collection_name)
  if not collection:
    return []

  if not query_texts and not query_embeddings:
    return []
  
  return collection.query(query_embeddings, query_texts, n_results=nresults, where=where_filter)
