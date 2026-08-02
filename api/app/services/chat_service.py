"""
Resolves a figure slug to its PhilosopherAgent -- this IS the "activated when
the character is chosen" mechanism. There's no per-figure agent class (that
would mean 44 near-identical files); one PhilosopherAgent class is generic
over any figure's data, and this service just picks which figure.json feeds
it based on whatever slug the frontend sends with the request.

Agents are cached by slug so repeat messages in the same session (and repeat
requests for a popular figure across different users) don't re-read + re-parse
the JSON file and rebuild the system prompt every single turn -- see deps.py
for why the cache dict lives at module scope there rather than here.

Deliberately stateless beyond that cache: conversation history is NOT
persisted to Postgres yet (that's session persistence, TASKS 2.5/2.7) -- the
frontend sends the full history with every request. Real limitation once
sessions need to survive a page reload, fine for now.
"""
from pathlib import Path

from app.adapters.llm.base import PersonaLLMClient
from app.agents.philosopher_agent import PhilosopherAgent


class ChatService:
    def __init__(
        self,
        llm: PersonaLLMClient,
        figures_dir: Path,
        cache: dict[str, PhilosopherAgent],
    ):
        self._llm = llm
        self._figures_dir = figures_dir
        self._agents = cache

    def get_agent(self, slug: str) -> PhilosopherAgent | None:
        """Returns None for any of the 32 roster figures without a real
        extraction yet -- the route turns that into a 404. The frontend
        already knows which 12 are real via data.js's FIGURE_SLUGS and
        shouldn't be offering chat for the rest, but this is the actual
        enforcement point, not just a UI nicety."""
        if slug in self._agents:
            return self._agents[slug]

        path = self._figures_dir / f"{slug}.json"
        if not path.exists():
            return None

        agent = PhilosopherAgent.from_json_file(path, self._llm)
        self._agents[slug] = agent
        return agent
