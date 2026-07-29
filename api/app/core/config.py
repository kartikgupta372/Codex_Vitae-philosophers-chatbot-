
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    environment: str = Field(default="development")
    cors_allow_origins: str = Field(default="http://localhost:3000")


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

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allow_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()