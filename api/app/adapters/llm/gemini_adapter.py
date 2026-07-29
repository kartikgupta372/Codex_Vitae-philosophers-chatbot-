from collections.abc import AsyncIterator

from google import genai
from google.genai import types

from app.adapters.llm.base import PersonaLLMClient


class GeminiAdapter(PersonaLLMClient):
    def __init__(self, api_key: str, model: str):
        self._client = genai.Client(api_key=api_key)
        self._model = model

    async def stream(
        self,
        *,
        system_prompt: str,
        user_message: str,
        history: list[dict[str, str]] | None = None,
    ) -> AsyncIterator[str]:
        contents = [self._to_content(turn) for turn in (history or [])]
        contents.append(types.Content(role="user", parts=[types.Part.from_text(text=user_message)]))

        response_stream = await self._client.aio.models.generate_content_stream(
            model=self._model,
            contents=contents,
            config=types.GenerateContentConfig(system_instruction=system_prompt),
        )
        async for chunk in response_stream:
            if chunk.text:
                yield chunk.text

    @staticmethod
    def _to_content(turn: dict[str, str]) -> types.Content:
        role = "model" if turn["role"] == "assistant" else "user"
        return types.Content(role=role, parts=[types.Part.from_text(text=turn["content"])])
