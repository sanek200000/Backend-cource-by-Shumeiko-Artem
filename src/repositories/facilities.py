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

    async def edit(self, db, room_id, facilities_ids):
        current_facilities = set(
            f.facility_id
            for f in await db.rooms_facilities.get_filtred(room_id=room_id)
        )
        new_facilities = set(facilities_ids)

        to_add = new_facilities - current_facilities
        to_remove = current_facilities - new_facilities

        if to_remove:
            [
                await db.rooms_facilities.delete(room_id=room_id, facility_id=f_id)
                for f_id in to_remove
            ]

        if to_add:
            rooms_facilities_data = [
                RoomsFacilityAdd(room_id=room_id, facility_id=f_id) for f_id in to_add
            ]
            await db.rooms_facilities.add_bulk(rooms_facilities_data)
