from abc import ABC, abstractmethod
from typing import Any


class PingRepository(ABC):
    @abstractmethod
    async def save(self, *, message: str, reply: str) -> str:
        ...


class FigureRepository(ABC):

    @abstractmethod
    async def get_by_slug(self, slug: str) -> dict[str, Any] | None: ...

    @abstractmethod
    async def list_published(self, *, category: str | None = None) -> list[dict[str, Any]]: ...

    @abstractmethod
    async def upsert(self, figure_data: dict[str, Any]) -> str:
        ...


class SessionRepository(ABC):

    @abstractmethod
    async def create(self, *, user_id: str | None) -> str: ...

    @abstractmethod
    async def get_active_figure(self, session_id: str) -> str | None: ...

    @abstractmethod
    async def set_active_figure(self, session_id: str, figure_id: str) -> None:
        ...


class MessageRepository(ABC):

    @abstractmethod
    async def append(self, *, session_id: str, figure_id: str, role: str, content: str) -> None: ...

    @abstractmethod
    async def history(self, session_id: str, *, limit: int = 50) -> list[dict[str, Any]]: ...
