import os

from dotenv import load_dotenv

load_dotenv()


DEFAULT_LLM_MODEL = "gemini-3.1-flash-lite"
DEFAULT_EMBEDDING_MODEL = "models/gemini-embedding-2"
CHAT_HISTORY_CONTEXT_WINDOW_SIZE = 15
APP_DATA_PATH = "./src/storage/"


_LLM_API_KEY = os.getenv("LLM_API_KEY")
_LLM_MODEL = os.getenv("LLM_MODEL") or DEFAULT_LLM_MODEL
_EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL") or DEFAULT_EMBEDDING_MODEL


def demonstrative_mode() -> bool:
  """
  Retorna True se o aplicativo estiver em modo demonstrativo (sem chave de API) e 
  False caso contrário. 
  """
  return not _LLM_API_KEY

def set_llm_api_key(api_key: str):
  """
  Define a chave de API do LLM.
  """
  global _LLM_API_KEY
  _LLM_API_KEY = api_key

def get_llm_api_key() -> str:
  """
  Retorna a chave de API do LLM.
  """
  return _LLM_API_KEY

def set_llm_model(model: str):
  """
  Define o modelo do LLM.
  """
  global _LLM_MODEL
  _LLM_MODEL = model

def get_llm_model() -> str:
  """
  Retorna o modelo do LLM.
  """
  return _LLM_MODEL

def set_embedding_model(model: str):
  """
  Define o modelo de embedding.
  """
  global _EMBEDDING_MODEL
  _EMBEDDING_MODEL = model

def get_embedding_model() -> str:
  """
  Retorna o modelo de embedding.
  """
  return _EMBEDDING_MODEL