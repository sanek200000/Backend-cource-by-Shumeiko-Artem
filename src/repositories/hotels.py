from sqlalchemy import func, select
from models.hotels import HotelsOrm
from models.rooms import RoomsOrm
from repositories.base import BaseRepository

from repositories.utils import rooms_ids_for_booking
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

    async def get_filtred_by_time(self, date_from, date_to):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        return await self.get_filtred(self.model.id.in_(hotels_ids_to_get))
