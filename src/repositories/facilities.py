from typing import Sequence
from httpx import delete
from sqlalchemy import insert, select
from models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from repositories.base import BaseRepository
from repositories.mappers.mappers import FacilityDataMapper
from schemas.facilities import RoomsFacilityAdd


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilityDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    mapper = FacilityDataMapper

    async def edit(self, room_id, facilities_ids):

        get_current_facilities_ids_query = select(self.model.facility_id).filter_by(
            room_id=room_id
        )
        res = await self.session.execute(get_current_facilities_ids_query)
        current_facilities_ids: Sequence[int] = res.scalars().all()
        print(f"================ {current_facilities_ids = }")

        ids_to_add = list(set(current_facilities_ids) - set(facilities_ids))
        ids_to_remove = list(set(facilities_ids) - set(current_facilities_ids))

        if ids_to_remove:
            query = delete(self.model).filter(
                self.model.room_id == room_id,
                self.model.facility_id.in_(ids_to_remove),
            )
            await self.session.execute(query)

        if ids_to_add:
            query = insert(self.model).values(
                [{"room_id": room_id, "facility_id": f_id} for f_id in ids_to_add]
            )
            await self.session.execute(query)
