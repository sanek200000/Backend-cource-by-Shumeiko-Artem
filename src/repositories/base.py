import logging
from typing import Any
from asyncpg import ForeignKeyViolationError, PostgresSyntaxError, UniqueViolationError
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

    async def get_filtred(self, *args, **kwargs) -> list[BaseModel | Any]:
        query = select(self.model).filter(*args).filter_by(**kwargs)
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)

        rows = result.scalars().all()
        return [self.mapper.map_to_domain_entity(row) for row in rows]

    async def get_all(self):
        return await self.get_filtred()

    async def get_one_with_rels(self, **kwargs):
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

    async def get_one_or_none(self, **filter_by) -> BaseModel | None | Any:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()

        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel):
        query = insert(self.model).values(**data.model_dump()).returning(self.model)
        print(query.compile(compile_kwargs={"literal_binds": True}))

        try:
            result = await self.session.execute(query)
        except sqlalchemy.exc.IntegrityError as ex:
            logging.error(
                f"Не удалось добавить данные в БД, входные данные={data}, тип ошибки: {type(ex.orig.__cause__)}"
            )
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise UniqueViolationError
            else:
                logging.error(
                    f"Незнакомая ошибка, входные данные={data}, тип ошибки: {type(ex.orig.__cause__)}"
                )
                raise ex

        row = result.scalars().one()
        return self.mapper.map_to_domain_entity(row)

    async def add_bulk(self, data: list[BaseModel]):
        query = insert(self.model).values([item.model_dump() for item in data])
        try:
            await self.session.execute(query)
        except sqlalchemy.exc.IntegrityError as ex:
            if isinstance(ex.orig.__cause__, ForeignKeyViolationError):
                raise ForeignKeyViolationError
            else:
                raise ex

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **kwargs):
        query = (
            update(self.model)
            .filter_by(**kwargs)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        try:
            await self.session.execute(query)
        except sqlalchemy.exc.IntegrityError as ex:
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise UniqueViolationError
            else:
                raise ex
        except sqlalchemy.exc.ProgrammingError as ex:
            if isinstance(ex.orig.__cause__, PostgresSyntaxError):
                raise PostgresSyntaxError
            else:
                raise ex

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
