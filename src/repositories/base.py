from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
import sqlalchemy.exc
from sqlalchemy.ext.asyncio import AsyncSession

from db import Base
from exceptions import ObjictNotFoundException
from repositories.mappers.base import DataMapper


class BaseRepository:
    model: Base = None
    mapper: DataMapper

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_filtred(self, *args, **kwargs):
        query = select(self.model).filter(*args).filter_by(**kwargs)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)

        return [
            self.mapper.map_to_domain_entity(data=row) for row in result.scalars().all()
        ]

    async def get_all(self):
        return await self.get_filtred()

    async def get_one_or_none(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)

        row = result.scalars().one_or_none()
        if row:
            return self.mapper.map_to_domain_entity(row)

    async def get_one(self, **kwargs):
        "sqlalchemy.exc.NoResultFound"
        "sqlalchemy.exc.DBAPIError"
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        try:
            row = result.scalars().one()
        except sqlalchemy.exc.NoResultFound:
            raise ObjictNotFoundException
        return self.mapper.map_to_domain_entity(row)

    async def add(self, data: BaseModel):
        try:
            query = insert(self.model).values(**data.model_dump()).returning(self.model)
            print(query.compile(compile_kwargs={"literal_binds": True}))
            result = await self.session.execute(query)

            row = result.scalars().one()
            return self.mapper.map_to_domain_entity(row)
        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(
                status_code=401,
                detail="Недопустимая дупликация данных",
            )

    async def add_bulk(self, data: list[BaseModel]):
        query = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(query)

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

    async def edit_bulk(self, data: BaseModel, exclude_unset: bool = False, **kwargs):
        query = (
            update(self.model)
            .filter_by(**kwargs)
            .values([item.model_dump(exclude_unset=exclude_unset) for item in data])
        )
        await self.session.execute(query)

    async def delete(self, **kwargs):
        query = delete(self.model).filter_by(**kwargs)
        await self.session.execute(query)
