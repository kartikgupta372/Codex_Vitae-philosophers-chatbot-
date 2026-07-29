from dataclasses import dataclass

from app.adapters.llm.base import PersonaLLMClient
from app.repositories.base import PingRepository

_SKELETON_SYSTEM_PROMPT = (
    "You are a one-line deploy check for a project called Codex Vitae, a study "
    "companion for historical and modern thinkers. Reply in a single short "
    "sentence acknowledging the test message — nothing else."
)


@dataclass(frozen=True)
class PingResult:
    id: str
    message: str
    reply: str


class PingService:
    def __init__(self, repo: PingRepository, llm: PersonaLLMClient):
        self._repo = repo
        self._llm = llm

    async def record(self, message: str) -> PingResult:
        reply = await self._collect(
            self._llm.stream(system_prompt=_SKELETON_SYSTEM_PROMPT, user_message=message)
        )
        ping_id = await self._repo.save(message=message, reply=reply)
        return PingResult(id=ping_id, message=message, reply=reply)

    @staticmethod
    async def _collect(chunks) -> str:
        parts = [chunk async for chunk in chunks]
        return "".join(parts)
