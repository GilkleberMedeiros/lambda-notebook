from typing import TypedDict

import chromadb


class RegistryData(TypedDict):
  ids: list[any]
  documents: list[any]
  embeddings: list[any] | None
  metadatas: list[dict] | None

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


def add_registry(collection_name: str, data: RegistryData): 
  collection = get_collection(collection_name)
  if not collection: 
    return None

  collection.add(
    **data
  )

  return data

def get_all_registries(collection_name: str):
  collection = get_collection(collection_name)
  if not collection:
    return None
  
  return collection.get()

def get_registries(collection_name: str, limit: int = None, offset: int = None, where_filter: dict = None): 
  collection = get_collection(collection_name)
  if not collection:
    return None
  
  return collection.get(where=where_filter, limit=limit, offset=offset)

def update_registry(collection_name: str, data: RegistryData):
  collection = get_collection(collection_name)
  if not collection:
    return None

  collection.update(**data)

  return data

def delete_registry(collection_name: str, where_filter: dict = None):
  collection = get_collection(collection_name)
  if not collection:
    raise Exception(f"Não foi possível encontrar uma coleção com o nome {collection_name}")
  
  collection.delete(where=where_filter)


def query_documents(collection_name: str, query_texts: list[str] = None, query_embeddings: list[str] = None, nresults: int = 5, where_filter: dict = None):
  collection = get_collection(collection_name)
  if not collection:
    return None

  if not query_texts and not query_embeddings:
    return None
  
  return collection.query(query_embeddings, query_texts, n_results=nresults, where=where_filter)
