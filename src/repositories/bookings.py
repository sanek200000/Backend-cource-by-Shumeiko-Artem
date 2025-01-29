from datetime import date
from sqlalchemy import select
from models.bookings import BookingsOrm
from repositories.base import BaseRepository
from repositories.mappers.mappers import BookingDataMapper


class BookingsRepository(BaseRepository):
    model: BookingsOrm = BookingsOrm
    mapper: BookingDataMapper = BookingDataMapper

    async def get_bookings_with_today_checin(self):
        query = select(self.model).filter(self.model.date_from == date.today())

        res = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()
        ]
