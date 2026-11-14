from collections.abc import AsyncGenerator

import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import get_settings

_settings = get_settings()

# Serverless (Vercel): each invocation may run on a fresh event loop, and pooled asyncpg
# connections cannot move between loops, so open a connection per request there instead.
_pool_args = {"poolclass": NullPool} if os.getenv("VERCEL") else {"pool_pre_ping": True}

engine = create_async_engine(
    _settings.database_url,
    **_pool_args,
    # search_path keeps queries inside our schema; extensions holds pgvector on Supabase
    connect_args={"server_settings": {"search_path": f"{_settings.db_schema},extensions,public"}},
    echo=(_settings.environment == "development"),
)

async_session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


async def dispose_engine() -> None:
    await engine.dispose()
