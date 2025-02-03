from datetime import date
from fastapi import APIRouter, Body, Query

from api.dependences import DB_DEP

from schemas.facilities import RoomsFacilityAdd
from schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest
from utils.openapi_examples import RoomsOE


router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Нумера"])


@router.get("/", summary="Посмотреть все номера в отеле")
async def get_rooms_in_hotel(
    db: DB_DEP,
    hotel_id: int,
    date_from: date = Query(example="2024-11-01"),
    date_to: date = Query(example="2024-11-08"),
):
    return await db.rooms.get_filtred_by_time(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to,
    )


@router.get("/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DB_DEP):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/", summary="Добавить номер в список")
async def create_room(
    db: DB_DEP,
    hotel_id: int,
    room_data: RoomAddRequest = Body(openapi_examples=RoomsOE.create),
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    f_ids = room_data.facilities_ids

    if f_ids != []:
        rooms_facilities_data = [
            RoomsFacilityAdd(room_id=room.id, facility_id=f_id)
            for f_id in room_data.facilities_ids
        ]

        await db.rooms_facilities.add_bulk(rooms_facilities_data)

    await db.commit()

    return {"status": "OK", "data": room}


@router.put("/{room_id}", summary="Обновление информации о номерах")
async def modify_room(
    db: DB_DEP,
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest,
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.rooms_facilities.edit(
        db=db,
        room_id=room_id,
        facilities_ids=room_data.facilities_ids,
    )

    await db.commit()

    return {"status": "OK"}


@router.patch("/{room_id}", summary="Частичное обновление информации о номерах")
async def modify_room(
    db: DB_DEP,
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
):
    _room_data = RoomPatch(
        hotel_id=hotel_id,
        **room_data.model_dump(exclude_unset=True),
    )
    _room_data_dict = room_data.model_dump(exclude_unset=True)

    await db.rooms.edit(
        _room_data,
        exclude_unset=True,
        hotel_id=hotel_id,
        id=room_id,
    )

    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.edit(
            db=db,
            room_id=room_id,
            facilities_ids=room_data.facilities_ids,
        )
    await db.commit()

    return {"status": "OK"}


@router.delete("/{room_id}", summary="Удалить номер в отеле")
async def delete_room(db: DB_DEP, hotel_id: int, room_title: str):
    await db.rooms.delete(hotel_id=hotel_id, title=room_title)
    await db.commit()

    return {"status": "OK"}
