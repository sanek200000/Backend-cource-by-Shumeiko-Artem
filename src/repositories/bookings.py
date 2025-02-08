from datetime import date
from fastapi import HTTPException
from sqlalchemy import select
from models.bookings import BookingsOrm
from models.rooms import RoomsOrm
from repositories.base import BaseRepository
from repositories.mappers.mappers import BookingDataMapper
from repositories.utils import rooms_ids_for_booking
from schemas.bookings import BookingAdd


class BookingsRepository(BaseRepository):
    model: BookingsOrm = BookingsOrm
    mapper: BookingDataMapper = BookingDataMapper

    async def get_bookings_with_today_checin(self):
        query = select(self.model).filter(self.model.date_from == date.today())

        res = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()
        ]

    async def add_bookings(self, data: BookingAdd, hotel_id: int):

        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=data.date_from,
            date_to=data.date_to,
            hotel_id=hotel_id,
        )

        result = await self.session.execute(rooms_ids_to_get)
        free_rooms = result.scalars().all()

        if data.room_id in free_rooms:
            return await self.add(data)
        else:
            raise HTTPException(500)
