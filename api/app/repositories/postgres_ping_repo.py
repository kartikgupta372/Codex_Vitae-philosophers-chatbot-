from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import PingRecord
from app.repositories.base import PingRepository


class PostgresPingRepository(PingRepository):
    def __init__(self, db: AsyncSession):
        self._db = db

    async def save(self, *, message: str, reply: str) -> str:
        record = PingRecord(message=message, reply=reply)
        self._db.add(record)
        await self._db.commit()
        await self._db.refresh(record)
        return str(record.id)
