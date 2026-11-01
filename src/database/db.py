from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sqlite_engine = create_engine("sqlite:///src/storage/app.db")


# Importe todas as tabelas aq!
from src.database.models import Base, Notebook, Document, ChatMessage  # noqa: F401

Base.metadata.create_all(sqlite_engine)


@contextmanager
def get_session():
  session = sessionmaker(bind=sqlite_engine)()

  try: 
    yield session
    session.commit()
  except Exception as e:
    session.rollback()
    raise e
  finally:
    session.close()
  


