from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.llm.base import PersonaLLMClient
from app.adapters.llm.gemini_adapter import GeminiAdapter
from app.core.config import Settings, get_settings
from app.db.session import get_db
from app.repositories.base import PingRepository
from app.repositories.postgres_ping_repo import PostgresPingRepository
from app.services.ping_service import PingService


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_db():
        yield session


def get_ping_repository(db: AsyncSession = Depends(get_db_session)) -> PingRepository:
    return PostgresPingRepository(db)


def get_llm_client(settings: Settings = Depends(get_settings)) -> PersonaLLMClient:
    return GeminiAdapter(api_key=settings.gemini_api_key, model=settings.persona_model)


def get_ping_service(
    repo: PingRepository = Depends(get_ping_repository),
    llm: PersonaLLMClient = Depends(get_llm_client),
) -> PingService:
    return PingService(repo, llm)
