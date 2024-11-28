from sqlalchemy import func, select
from models.hotels import HotelsOrm
from models.rooms import RoomsOrm
from repositories.base import BaseRepository

from repositories.mappers.mappers import HotelDataMapper
from repositories.utils import rooms_ids_for_booking


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    mapper = HotelDataMapper

    async def get_filtred_by_time(
        self,
        date_from,
        date_to,
        title,
        location,
        limit,
        offset,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=date_from,
            date_to=date_to,
            limit=limit,
            offset=offset,
        )
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        if title:
            hotels_ids_to_get = hotels_ids_to_get.filter(
                func.lower(self.model.title).contains(title.strip().lower())
            )

        if location:
            hotels_ids_to_get = hotels_ids_to_get.filter(
                func.lower(self.model.location).contains(location.strip().lower())
            )

        return await self.get_filtred(self.model.id.in_(hotels_ids_to_get))
