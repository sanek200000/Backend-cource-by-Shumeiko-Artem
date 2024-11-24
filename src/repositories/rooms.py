from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models.rooms import RoomsOrm
from repositories.base import BaseRepository
from repositories.utils import rooms_ids_for_booking
from schemas.rooms import Room, RoomWithRels


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtred_by_time(self, hotel_id, date_from, date_to):
        rooms_ids_to_get = rooms_ids_for_booking(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to,
        )

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(self.model.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)

        return [
            RoomWithRels.model_validate(model)
            for model in result.unique().scalars().all()
        ]
