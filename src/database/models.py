from datetime import datetime, timezone

from sqlalchemy import ForeignKey, Text, TypeDecorator
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase): ...


class CreateTimestampMixin:
  created_at: Mapped[datetime] = mapped_column(nullable=False, default=lambda: datetime.now(timezone.utc))


class JSONStringDBPipe(TypeDecorator):
  """
  Um TypeDecorator para armazenar dados JSON como strings no banco de dados.
  """

  impl = Text

  def process_bind_param(self, value, dialect):
    if value is not None:
      import json
      return json.dumps(value)
    return value

  def process_result_value(self, value, dialect):
    if value is not None:
      import json
      return json.loads(value)
    return value



class Notebook(CreateTimestampMixin, Base):
  __tablename__ = "notebooks"

  id: Mapped[int] = mapped_column(primary_key=True)
  name: Mapped[str] = mapped_column(nullable=False)
  updated_at: Mapped[datetime] = mapped_column(nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

  documents: Mapped[list["Document"]] = relationship("Document", back_populates="notebook", cascade="all, delete-orphan")


class Document(CreateTimestampMixin, Base):
  __tablename__ = "documents"

  id: Mapped[int] = mapped_column(primary_key=True)
  notebook_id: Mapped[int] = mapped_column(ForeignKey("notebooks.id", ondelete="CASCADE"), nullable=False)
  name: Mapped[str] = mapped_column(nullable=False)
  file_type: Mapped[str] = mapped_column(nullable=False)
  file_path: Mapped[str] = mapped_column(nullable=False)
  chunk_count: Mapped[int] = mapped_column(default=0)

  notebook: Mapped["Notebook"] = relationship("Notebook", back_populates="documents")


class ChatMessage(CreateTimestampMixin, Base):
  __tablename__ = "chat_messages"

  id: Mapped[int] = mapped_column(primary_key=True)
  notebook_id: Mapped[int] = mapped_column(ForeignKey("notebooks.id", ondelete="CASCADE"), nullable=False)
  role: Mapped[str] = mapped_column(nullable=False)
  content: Mapped[str] = mapped_column(nullable=False)
  sources: Mapped[dict] = mapped_column(JSONStringDBPipe, nullable=True)

  notebook: Mapped["Notebook"] = relationship("Notebook")



