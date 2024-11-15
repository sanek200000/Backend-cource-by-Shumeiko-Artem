from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db import Base


class BaseRepository:
    model: Base = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)

        return result.scalars().all()

    async def get_one_or_none(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.one_or_none(query)

        return result.scalars().all()

    async def add(self, data: BaseModel):
        query = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(query)

        return result.scalars().one()

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **kwargs):
        query = (
            update(self.model)
            .filter_by(**kwargs)
            .values(**data.model_dump(exclude_unset=True))
        )
        result = await self.session.execute(query)

    async def delete(self, **kwargs):
        query = delete(self.model).filter_by(**kwargs)
        await self.session.execute(query)
