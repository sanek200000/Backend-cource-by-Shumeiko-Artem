from datetime import date
from pydantic import BaseModel
from sqlalchemy import insert, select
from models.bookings import BookingsOrm
from models.rooms import RoomsOrm
from repositories.base import BaseRepository
from repositories.mappers.mappers import BookingDataMapper
from repositories.utils import rooms_ids_for_booking


class BookingsRepository(BaseRepository):
    model: BookingsOrm = BookingsOrm
    mapper: BookingDataMapper = BookingDataMapper

    async def get_bookings_with_today_checin(self):
        query = select(self.model).filter(self.model.date_from == date.today())

        res = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()
        ]

    async def add_bookings(self, data: BaseModel):
        data_dict: dict = data.model_dump()

        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=data_dict.get("date_from"),
            date_to=data_dict.get("date_to"),
        )

        rooms_ids_to_get = select(RoomsOrm.id).filter(
            RoomsOrm.id.in_(rooms_ids_to_get),
            RoomsOrm.id == data_dict.get("room_id"),
        )

        result = await self.session.execute(rooms_ids_to_get)
        free_room = result.scalars().all()

        print(f"=================== {free_room = } =======================")
        if free_room:
            return await self.add(data)
