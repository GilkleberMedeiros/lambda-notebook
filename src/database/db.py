from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import APP_DATA_PATH

p = Path(APP_DATA_PATH).joinpath("app.db")
sqlite_engine = create_engine(f"sqlite:///{str(p)}")


# Importe todas as tabelas aq!
from src.database.models import Base, Notebook, Document, ChatMessage  # noqa: F401

Base.metadata.create_all(sqlite_engine)


@contextmanager
def get_session():
  session = sessionmaker(bind=sqlite_engine, expire_on_commit=False)()

  try: 
    yield session
    session.commit()
  except Exception as e:
    session.rollback()
    raise e
  finally:
    session.close()
  


