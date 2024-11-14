from sqlalchemy import func, insert, literal_column, select
from models.hotels import HotelsOrm
from repositories.base import BaseRepository

from db import async_session_maker, engine


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(self, location, title, limit, offset):

        query = select(self.model)

        if title:
            query = query.filter(
                func.lower(self.model.title).contains(title.strip().lower())
            )
        if location:
            query = query.filter(
                func.lower(self.model.location).contains(location.strip().lower())
            )
        query = query.limit(limit).offset(offset)

        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)

        return result.scalars().all()

    async def add(self, hotel_data):
        add_hotel_stmt = (
            insert(self.model)
            .values(**hotel_data.model_dump())
            .returning(literal_column("*"))
        )
        print(
            add_hotel_stmt.compile(bind=engine, compile_kwargs={"literal_binds": True})
        )
        result = await self.session.execute(add_hotel_stmt)

        return dict(result.one_or_none()._mapping)
