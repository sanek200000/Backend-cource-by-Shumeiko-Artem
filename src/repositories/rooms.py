from sqlalchemy import select
from sqlalchemy.orm import selectinload
from exceptions import ObjictNotFoundException
from models.rooms import RoomsOrm
from repositories.base import BaseRepository
from repositories.mappers.mappers import RoomDataMapper, RoomDataWithRelsMapper
from repositories.utils import rooms_ids_for_booking


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

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
            RoomDataWithRelsMapper.map_to_domain_entity(model)
            for model in result.unique().scalars().all()
        ]

    async def get_one_or_none(self, **kwargs):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**kwargs)
        )
        result = await self.session.execute(query)

        row = result.scalars().one_or_none()
        if row:
            return RoomDataWithRelsMapper.map_to_domain_entity(row)
        raise ObjictNotFoundException
