from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.vectorstore.base import RetrievedChunk, VectorStore


class PgVectorStore(VectorStore):

    def __init__(self, db: AsyncSession):
        self._db = db

    async def upsert_chunks(
        self, *, figure_id: str, chunks: list[tuple[str, str, list[float]]]
    ) -> None:
        raise NotImplementedError("Week 2 — content loader (TASKS 2.3, 1.7).")

    async def search(
        self, *, figure_id: str, query_embedding: list[float], top_k: int = 5
    ) -> list[RetrievedChunk]:
        raise NotImplementedError("Week 2 — RAG retrieval (TASKS 2.6).")
