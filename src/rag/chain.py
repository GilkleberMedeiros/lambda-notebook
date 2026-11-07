from typing import Literal, NamedTuple

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import get_llm_api_key, get_llm_model
from src.database import models
from src.rag import vector_store as vstore
from src.rag import ingestion
from src.utils import make_nb_collection_name


_SYSTEM_PROMPT = """
Você é um assistente prestativo. Use os seguintes pedaços de contexto recuperados 
dos documentos fornecidos pelo usuário para responder à pergunta. 
Se a resposta não estiver no contexto/documentos fornecidos, explique ao usuário 
que os documentos fornecidos não contém a informação solicitada.

Contexto: 
{context}
"""

class ChatMessage(NamedTuple):
  role: Literal["human", "ai"]
  text: str

def make_prompt(chat_messages: list[ChatMessage], system_prompt: str = _SYSTEM_PROMPT): 
  return ChatPromptTemplate([
    ("system", system_prompt), 
    *chat_messages
  ])

def get_relevant_docs(query: str, notebook_id: int, where_filter: dict = None):
  coll_name = make_nb_collection_name(notebook_id)
  q_embeddings = ingestion.embed_documents([query])[0]

  return vstore.query_documents(coll_name, query_embeddings=q_embeddings, nresults=10, where_filter=where_filter)

def make_llm():
  llm = ChatGoogleGenerativeAI(model=get_llm_model(), api_key=get_llm_api_key())
  return llm


def convert_chat_messages_to_prompt_messages(messages: list[models.ChatMessage]): 
  ROLES_MAP = {
    "user": "human", 
    "assistant": "ai"
  }

  return [ ChatMessage(ROLES_MAP[msg.role], msg.content) for msg in messages ]
