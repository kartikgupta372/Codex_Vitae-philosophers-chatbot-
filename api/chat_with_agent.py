import asyncio
import sys

from app.adapters.llm.gemini_adapter import GeminiAdapter
from app.agents.philosopher_agent import PhilosopherAgent
from app.core.config import get_settings

DEFAULT_FIGURE = "../content/figures/marcus-aurelius.json"


async def main() -> None:
    figure_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FIGURE
    settings = get_settings()

    if not settings.gemini_api_key:
        print("GEMINI_API_KEY is empty in your .env -- nothing to call.")
        return

    llm = GeminiAdapter(api_key=settings.gemini_api_key, model=settings.persona_model)
    agent = PhilosopherAgent.from_json_file(figure_path, llm)

    print(f"Talking with {agent.name}. Type 'quit' to exit.\n")
    history: list[dict[str, str]] = []

    while True:
        user_message = input("you: ").strip()
        if not user_message:
            continue
        if user_message.lower() in {"quit", "exit"}:
            break

        print(f"{agent.name}: ", end="", flush=True)
        reply_parts: list[str] = []
        async for chunk in agent.stream(user_message, history=history):
            print(chunk, end="", flush=True)
            reply_parts.append(chunk)
        print("\n")

        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": "".join(reply_parts)})


if __name__ == "__main__":
    asyncio.run(main())
