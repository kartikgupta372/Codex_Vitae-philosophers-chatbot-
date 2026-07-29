from abc import ABC, abstractmethod
from collections.abc import AsyncIterator


class PersonaLLMClient(ABC):
    @abstractmethod
    def stream(
        self,
        *,
        system_prompt: str,
        user_message: str,
        history: list[dict[str, str]] | None = None,
    ) -> AsyncIterator[str]:
        ...
