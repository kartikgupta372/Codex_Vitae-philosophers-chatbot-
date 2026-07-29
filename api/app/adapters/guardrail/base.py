from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class GuardrailResult:
    tripped: bool
    reason: str | None = None


class GuardrailClient(ABC):
    @abstractmethod
    async def check(self, message: str) -> GuardrailResult: ...
