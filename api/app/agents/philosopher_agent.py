import json
from pathlib import Path

from app.adapters.llm.base import PersonaLLMClient


class PhilosopherAgent:
    def __init__(self, figure_data: dict, llm: PersonaLLMClient):
        self._figure = figure_data
        self._llm = llm
        self._system_prompt = self._build_system_prompt(figure_data)

    @classmethod
    def from_json_file(cls, path: str | Path, llm: PersonaLLMClient) -> "PhilosopherAgent":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(data, llm)

    @property
    def name(self) -> str:
        return self._figure["name"]

    def stream(self, user_message: str, history: list[dict[str, str]] | None = None):
        return self._llm.stream(
            system_prompt=self._system_prompt,
            user_message=user_message,
            history=history,
        )

    @staticmethod
    def _build_system_prompt(figure: dict) -> str:
        voice = figure["voice"]
        beliefs = figure["core_beliefs"]
        limits = figure["limits_and_dangers"]

        never_does = "; ".join(voice["never_does"])
        failure_modes = "; ".join(
            f"{fm['distortion']} (looks like: {fm['looks_like']})"
            for fm in limits["failure_modes"]
        )

        return (
            f"You are having a conversation AS {figure['name']} ({figure['lifespan']}), "
            f"not a modern assistant describing them from the outside. This is a study "
            f"companion, not a claim to be the real person -- if the user seems genuinely "
            f"confused about that, clarify plainly without breaking voice more than needed.\n\n"
            f"CENTRAL FRAME: {beliefs['central_frame']}\n\n"
            f"REGISTER: {voice['register']}\n"
            f"CADENCE: {voice['cadence']}\n\n"
            f"NEVER DO (this would be out of character): {never_does}\n\n"
            f"Where this philosophy goes wrong in a real person's hands, name it honestly "
            f"rather than only defending it: {failure_modes}\n\n"
            f"Safety stopgap (the real guardrail layer from TASKS 2.9 isn't built yet): if "
            f"the user's message reads as crisis-adjacent -- self-harm, wanting to disappear, "
            f"acute despair -- drop the persona entirely and respond as a direct, caring "
            f"modern voice pointing them to real support. Character consistency matters far "
            f"less than this."
        )
