from datetime import date

from sqlalchemy import func, select
from sqlalchemy.sql.functions import count
from models.bookings import BookingsOrm
from models.rooms import RoomsOrm
from repositories.base import BaseRepository
from repositories.utils import rooms_ids_for_booking
from schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtred_by_time(self, hotel_id, date_from, date_to):
        query = rooms_ids_for_booking(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to,
        )

        return await self.get_filtred(self.model.id.in_(query))
