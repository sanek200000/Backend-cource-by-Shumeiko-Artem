from sqlalchemy import func, select
from models.hotels import HotelsOrm
from repositories.base import BaseRepository

from schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(self, title, location, limit, offset):

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

        return [
            self.schema.model_validate(row, from_attributes=True)
            for row in result.scalars().all()
        ]
