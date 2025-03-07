from typing import Sequence
from asyncpg import ForeignKeyViolationError
from sqlalchemy import insert, select, delete
from models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from repositories.base import BaseRepository
from repositories.mappers.mappers import FacilityDataMapper
import sqlalchemy.exc


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

        ids_to_remove = list(set(current_facilities_ids) - set(facilities_ids))
        ids_to_add = list(set(facilities_ids) - set(current_facilities_ids))

        if ids_to_remove:
            query = delete(self.model).filter(
                self.model.room_id == room_id,
                self.model.facility_id.in_(ids_to_remove),
            )
            try:
                await self.session.execute(query)
            except sqlalchemy.exc.IntegrityError as ex:
                if isinstance(ex.orig.__cause__, ForeignKeyViolationError):
                    raise ForeignKeyViolationError
                else:
                    raise ex

        if ids_to_add:
            query = insert(self.model).values(
                [{"room_id": room_id, "facility_id": f_id} for f_id in ids_to_add]
            )
            try:
                await self.session.execute(query)
            except sqlalchemy.exc.IntegrityError as ex:
                if isinstance(ex.orig.__cause__, ForeignKeyViolationError):
                    raise ForeignKeyViolationError
                else:
                    raise ex
