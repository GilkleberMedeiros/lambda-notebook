from sqlalchemy import create_engine


sqlite_engine = create_engine("sqlite:///src/storage/app.db")


# Importe todas as tabelas aq!
from src.database.models import Base, Notebook, Document, ChatMessage  # noqa: F401

Base.metadata.create_all(sqlite_engine)


