from groq import AsyncGroq

from app.adapters.guardrail.base import GuardrailClient, GuardrailResult


class GroqGuardrailAdapter(GuardrailClient):

    def __init__(self, api_key: str, model: str):
        self._client = AsyncGroq(api_key=api_key)
        self._model = model

    async def check(self, message: str) -> GuardrailResult:
        raise NotImplementedError(
            "Week 3 (TASKS 2.9 / PRD R3). Fail-closed in the meantime: callers "
            "should treat this raising as tripped=True, not let it fall through."
        )
