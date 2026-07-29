from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievedChunk:
    section: str
    content: str
    score: float


class VectorStore(ABC):
    @abstractmethod
    async def upsert_chunks(
        self, *, figure_id: str, chunks: list[tuple[str, str, list[float]]]
    ) -> None:
        ...

    @abstractmethod
    async def search(
        self, *, figure_id: str, query_embedding: list[float], top_k: int = 5
    ) -> list[RetrievedChunk]: ...
