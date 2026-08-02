
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    environment: str = Field(default="development")

    # Widened for local dev since the current frontend is plain HTML/JS served
    # by *some* local static server (ES module imports like figure.html's
    # `import ... from './data.js'` fail outright over file://, so one must
    # already be running) -- common candidates covered here: VS Code Live
    # Server, Python's http.server, Vite. Tell me the actual port if chat
    # requests get a CORS error and this list doesn't cover it.
    cors_allow_origins: str = Field(
        default="http://localhost:3000,http://localhost:5500,http://127.0.0.1:5500,"
        "http://localhost:5173,http://localhost:8080,http://localhost:8000"
    )


    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/codex_vitae"
    )


    redis_url: str = Field(default="redis://localhost:6379/0")

    gemini_api_key: str = Field(default="")
    persona_model: str = Field(default="gemini-2.5-flash")

    groq_api_key: str = Field(default="")
    guardrail_model: str = Field(default="openai/gpt-oss-20b")

    voyage_api_key: str = Field(default="")
    embedding_model: str = Field(default="voyage-4-lite")
    embedding_dimensions: int = Field(default=1024)

    # PRD R3 / TASKS 2.9's break-character response. Default targets India
    # (Tele-MANAS -- the government's official 24/7 free multilingual mental
    # health helpline) since that's this project's likely primary audience,
    # with a generic fallback line for anyone elsewhere. If the actual
    # audience turns out to be different or more global, change this --
    # it's one config value, not buried in adapter code.
    crisis_response_message: str = Field(
        default=(
            "I want to stop and step outside the persona for a moment, because this "
            "matters more than staying in character.\n\n"
            "If you're thinking about suicide or self-harm, please reach out right now. "
            "In India, Tele-MANAS is free, confidential, and available 24/7: call 14416 "
            "or 1-800-891-4416. If you're elsewhere, please look up your local crisis "
            "line, or go to your nearest emergency room. You can also reach out to "
            "someone you trust.\n\n"
            "This app isn't a substitute for that kind of support, and I'd rather stop "
            "and say this plainly than continue as if nothing happened."
        )
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allow_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
