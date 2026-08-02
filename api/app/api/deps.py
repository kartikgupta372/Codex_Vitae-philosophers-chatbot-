from collections.abc import AsyncGenerator
from pathlib import Path

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.guardrail.base import GuardrailClient
from app.adapters.guardrail.groq_adapter import GroqGuardrailAdapter
from app.adapters.llm.base import PersonaLLMClient
from app.adapters.llm.gemini_adapter import GeminiAdapter
from app.agents.philosopher_agent import PhilosopherAgent
from app.core.config import Settings, get_settings
from app.db.session import get_db
from app.repositories.base import PingRepository
from app.repositories.postgres_ping_repo import PostgresPingRepository
from app.services.chat_service import ChatService
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


# --- Guardrail ---
def get_guardrail_client(settings: Settings = Depends(get_settings)) -> GuardrailClient:
    return GroqGuardrailAdapter(api_key=settings.groq_api_key, model=settings.guardrail_model)


# --- Chat / agents ---
# deps.py -> app/api/ -> app/ -> api/ -> project root, then content/figures.
_FIGURES_DIR = Path(__file__).resolve().parents[3] / "content" / "figures"

# Module-level, not constructed inside get_chat_service: FastAPI builds a new
# ChatService per request (Depends doesn't cache by default the way
# get_settings's @lru_cache does), so if this cache lived inside ChatService's
# __init__ instead, it would be empty again on every single request and never
# actually cache anything. Living here, it persists for the life of the process.
_agent_cache: dict[str, PhilosopherAgent] = {}


def get_chat_service(llm: PersonaLLMClient = Depends(get_llm_client)) -> ChatService:
    return ChatService(llm=llm, figures_dir=_FIGURES_DIR, cache=_agent_cache)
