import enum
import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.core.config import get_settings

EMBEDDING_DIM = get_settings().embedding_dimensions


class Base(DeclarativeBase):
    pass


def _uuid_pk() -> Mapped[uuid.UUID]:
    return mapped_column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())


class PingRecord(Base):
    __tablename__ = "pings"

    id: Mapped[uuid.UUID] = _uuid_pk()
    message: Mapped[str] = mapped_column(Text, nullable=False)
    reply: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class FigureCategory(str, enum.Enum):
    ancient_philosophy = "ancient-philosophy"
    literature = "literature"
    warrior = "warrior"
    modern_thinkers = "modern-thinkers"


class FigureStatus(str, enum.Enum):
    draft = "draft"
    reviewed = "reviewed"
    published = "published"


class Figure(Base):
    __tablename__ = "figures"

    id: Mapped[uuid.UUID] = _uuid_pk()
    slug: Mapped[str] = mapped_column(Text, unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[FigureCategory] = mapped_column(Enum(FigureCategory, name="figure_category"), nullable=False, index=True)
    lifespan: Mapped[str] = mapped_column(Text, nullable=False)
    one_line: Mapped[str] = mapped_column(Text, nullable=False)
    is_living: Mapped[bool] = mapped_column(default=False, nullable=False)

    status: Mapped[FigureStatus] = mapped_column(
        Enum(FigureStatus, name="figure_status"), default=FigureStatus.draft, nullable=False, index=True
    )
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    data: Mapped[dict] = mapped_column(JSONB, nullable=False)
    system_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    chunks: Mapped[list["FigureChunk"]] = relationship(back_populates="figure", cascade="all, delete-orphan")


class FigureChunk(Base):
    __tablename__ = "figure_chunks"

    id: Mapped[uuid.UUID] = _uuid_pk()
    figure_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("figures.id", ondelete="CASCADE"), nullable=False, index=True)
    section: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(Vector(EMBEDDING_DIM), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    figure: Mapped["Figure"] = relationship(back_populates="chunks")


class ChatSession(Base):
    __tablename__ = "sessions"

    id: Mapped[uuid.UUID] = _uuid_pk()
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class SessionFigure(Base):
    __tablename__ = "session_figures"

    id: Mapped[uuid.UUID] = _uuid_pk()
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    figure_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("figures.id"), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Message(Base):
    __tablename__ = "messages"
    __table_args__ = (CheckConstraint("role IN ('user','assistant','system')", name="messages_role_check"),)

    id: Mapped[uuid.UUID] = _uuid_pk()
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    figure_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("figures.id"), nullable=False)
    role: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
