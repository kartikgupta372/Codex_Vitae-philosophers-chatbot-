from typing import Sequence, Union

import sqlalchemy as sa
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects import postgresql

from alembic import op
from app.core.config import get_settings

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

EMBEDDING_DIM = get_settings().embedding_dimensions


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    figure_category = postgresql.ENUM(
        "ancient-philosophy", "literature", "warrior", "modern-thinkers",
        name="figure_category",
    )
    figure_status = postgresql.ENUM(
        "draft", "reviewed", "published",
        name="figure_status",
    )

    op.create_table(
        "figures",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("slug", sa.Text(), nullable=False, unique=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("category", figure_category, nullable=False),
        sa.Column("lifespan", sa.Text(), nullable=False),
        sa.Column("one_line", sa.Text(), nullable=False),
        sa.Column("is_living", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("status", figure_status, nullable=False, server_default="draft"),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("data", postgresql.JSONB(), nullable=False),
        sa.Column("system_prompt", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_figures_slug", "figures", ["slug"])
    op.create_index("ix_figures_category", "figures", ["category"])
    op.create_index("ix_figures_status", "figures", ["status"])

    op.create_table(
        "figure_chunks",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("figure_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("figures.id", ondelete="CASCADE"), nullable=False),
        sa.Column("section", sa.Text(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("embedding", Vector(EMBEDDING_DIM), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_figure_chunks_figure_id", "figure_chunks", ["figure_id"])
    op.execute(
        "CREATE INDEX ix_figure_chunks_embedding_hnsw ON figure_chunks "
        "USING hnsw (embedding vector_cosine_ops)"
    )

    op.create_table(
        "sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "session_figures",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("figure_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("figures.id"), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_session_figures_session_id", "session_figures", ["session_id"])

    op.create_table(
        "messages",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("figure_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("figures.id"), nullable=False),
        sa.Column("role", sa.Text(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.CheckConstraint("role IN ('user','assistant','system')", name="messages_role_check"),
    )
    op.create_index("ix_messages_session_created", "messages", ["session_id", "created_at"])


def downgrade() -> None:
    op.drop_table("messages")
    op.drop_table("session_figures")
    op.drop_table("sessions")
    op.execute("DROP INDEX IF EXISTS ix_figure_chunks_embedding_hnsw")
    op.drop_table("figure_chunks")
    op.drop_table("figures")
    postgresql.ENUM(name="figure_status").drop(op.get_bind())
    postgresql.ENUM(name="figure_category").drop(op.get_bind())
