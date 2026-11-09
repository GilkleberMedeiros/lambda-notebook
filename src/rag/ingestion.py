from pathlib import Path

from langchain_core.documents import Document
from langchain_community.document_loaders.base import BaseLoader
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_community.document_loaders.markdown import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings

from src.config import get_embedding_model, get_llm_api_key


_EXT_2_LOADER_MAP: dict[str, BaseLoader] = {
  ".pdf": PyPDFLoader, 
  ".txt": TextLoader,
  ".docx": Docx2txtLoader, 
  ".md": UnstructuredMarkdownLoader
}

def load_documents(files: list[str | Path]) -> list[Document]:
  documents = []
  for file in files:
    if isinstance(file, str):
      file = Path(file)

    ext = file.suffix.lower()
    loader = _EXT_2_LOADER_MAP.get(ext)
    if loader is None:
      raise Exception(f"Não foi possível encontrar um loader para o documento com extensão {ext}!")
    
    pages: list[Document] = loader(file_path=str(file)).load()
    # Add Metadata
    def f(v: Document): 
      v.metadata["source"] = str(file)
      return v
    pages = list(map(f, pages))

    documents.extend(pages)

  return documents

def split_documents(docs: list[Document] | list[str]) -> list[list[Document]] | list[list[str]]:
  splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)


  texts = []
  for doc in docs:
    if isinstance(doc, str):
      splitted = splitter.split_text(doc)
      texts.append(splitted)
      continue

    splitted = splitter.split_documents([doc])
    texts.append(splitted)

  return texts

def embed_documents(docs: list[Document] | list[str]): 
  model = GoogleGenerativeAIEmbeddings(model=get_embedding_model(), api_key=get_llm_api_key())

  texts = []
  for i in range(len(docs)):
    doc = docs[i]
    if isinstance(doc, Document):
      texts.append(doc.page_content)
      continue

    texts.append(doc)


  embeddings = model.embed_documents(texts, batch_size=len(texts))

  return embeddings