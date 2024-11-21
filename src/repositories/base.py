from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
import sqlalchemy.exc
from sqlalchemy.ext.asyncio import AsyncSession

from db import Base


class BaseRepository:
    model: Base = None
    schema: BaseModel = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_filtred(self, *args, **kwargs):
        query = select(self.model).filter(*args).filter_by(**kwargs)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)

        return [self.schema.model_validate(row) for row in result.scalars().all()]

    async def get_all(self):
        return await self.get_filtred()

    async def get_one_or_none(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)

        row = result.scalars().one_or_none()
        if row:
            return self.schema.model_validate(row, from_attributes=True)

    async def add(self, data: BaseModel):
        try:
            query = insert(self.model).values(**data.model_dump()).returning(self.model)
            print(query.compile(compile_kwargs={"literal_binds": True}))
            result = await self.session.execute(query)

            row = result.scalars().one()
            return self.schema.model_validate(row, from_attributes=True)
        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(
                status_code=401,
                detail="Недопустимая дупликация данных",
            )

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **kwargs):
        try:
            query = (
                update(self.model)
                .filter_by(**kwargs)
                .values(**data.model_dump(exclude_unset=exclude_unset))
            )
            await self.session.execute(query)
        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(status_code=401, detail="Некорректные данные")

    async def delete(self, **kwargs):
        query = delete(self.model).filter_by(**kwargs)
        await self.session.execute(query)
