from datetime import date
from exceptions import (
    ObjictNotFoundException,
    RoomNotFoundException,
    check_date_to_after_date_from,
)
from schemas.facilities import RoomsFacilityAdd
from schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest
from services.base import BaseService
from services.hotels import HotelService


class RoomService(BaseService):
    async def get_room_in_hotel_with_check(self, hotel_id: int | None, room_id: int):
        """Checking the availability of a hotel room by its id

        Args:
            hotel_id (int|None): hotel id
            room_id (int): room id

        Raises:
            RoomNotFoundException: room not found in this hotel
        """
        if hotel_id:
            await HotelService(self.db).get_hotel_with_check(hotel_id)

        try:
            return await self.db.rooms.get_one(id=room_id)
        except ObjictNotFoundException:
            raise RoomNotFoundException

    async def get_rooms_in_hotel(self, hotel_id: int, date_from: date, date_to: date):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        check_date_to_after_date_from(date_from, date_to)
        return await self.db.rooms.get_filtred_by_time(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to,
        )

    async def get_room(self, hotel_id: int, room_id: int):
        await self.get_room_in_hotel_with_check(hotel_id, room_id)
        return await self.db.rooms.get_one_with_rels(id=room_id, hotel_id=hotel_id)

    async def create_room(self, hotel_id: int, room_data: RoomAddRequest):
        await HotelService(self.db).get_hotel_with_check(hotel_id)

        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        room = await self.db.rooms.add(_room_data)

        f_ids = room_data.facilities_ids
        if f_ids != []:
            rooms_facilities_data = [
                RoomsFacilityAdd(room_id=room.id, facility_id=f_id)
                for f_id in room_data.facilities_ids
            ]

            await self.db.rooms_facilities.add_bulk(rooms_facilities_data)

        await self.db.commit()
        return room

    async def modify_room(self, hotel_id: int, room_id: int, room_data: RoomAddRequest):
        await self.get_room_in_hotel_with_check(hotel_id, room_id)

        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        await self.db.rooms.edit(_room_data, id=room_id)

        await self.db.rooms_facilities.edit(
            room_id=room_id,
            facilities_ids=room_data.facilities_ids,
        )

        await self.db.commit()

    async def edit_room(self, hotel_id: int, room_id: int, room_data: RoomPatchRequest):
        await self.get_room_in_hotel_with_check(hotel_id, room_id)

        _room_data = RoomPatch(
            hotel_id=hotel_id,
            **room_data.model_dump(exclude_unset=True),
        )
        _room_data_dict = room_data.model_dump(exclude_unset=True)

        await self.db.rooms.edit(
            _room_data,
            exclude_unset=True,
            hotel_id=hotel_id,
            id=room_id,
        )

        if "facilities_ids" in _room_data_dict:
            await self.db.rooms_facilities.edit(
                room_id=room_id,
                facilities_ids=room_data.facilities_ids,
            )
        await self.db.commit()

    async def delete_room(self, hotel_id: int, room_id: int):
        await self.get_room_in_hotel_with_check(hotel_id, room_id)

        await self.db.rooms.delete(hotel_id=hotel_id, id=room_id)
        await self.db.commit()
