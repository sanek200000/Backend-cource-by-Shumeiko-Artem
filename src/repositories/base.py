from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from db import Base


class BaseRepository:
    model = None

    def __init__(self, session) -> None:
        self.session = session

    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)

        return result.scalars().all()

    async def get_one_or_none(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.one_or_none(query)

        return result.scalars().all()
