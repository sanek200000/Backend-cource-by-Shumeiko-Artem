from fastapi import APIRouter, Body

from api.dependences import DB_DEP
from db import async_session_maker

from repositories.rooms import RoomsRepository
from schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest


router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Нумера"])


@router.get("/", summary="Посмотреть все номера в отеле")
async def get_rooms_in_hotel(db: DB_DEP, hotel_id: int):
    return await db.rooms.get_filtred(hotel_id=hotel_id)


@router.post("/", summary="Добавить номер в список")
async def create_room(
    db: DB_DEP,
    hotel_id: int,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "standart",
                "value": {
                    "hotel_id": 0,
                    "title": "standart",
                    "description": "sfsdfsdf sdfsdf sdfsdf sdfsdf",
                    "price": 10,
                    "quantity": 10,
                },
            },
            "2": {
                "summary": "comfort",
                "value": {
                    "hotel_id": 0,
                    "title": "comfort",
                    "description": "sfsdfsdf sdfsdf sdfsdf sdfsdf",
                    "price": 100,
                    "quantity": 5,
                },
            },
            "3": {
                "summary": "luxe",
                "value": {
                    "hotel_id": 0,
                    "title": "luxe",
                    "description": "sfsdfsdf sdfsdf sdfsdf sdfsdf",
                    "price": 1000,
                    "quantity": 1,
                },
            },
        }
    ),
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    await db.commit()

    return {"status": "OK", "data": room}


@router.put("/{room_id}", summary="Обновление информации о номерах")
async def modify_room(db: DB_DEP, room_id: int, room_data: RoomAdd):
    await db.rooms.edit(room_data, id=room_id)
    await db.commit()

    return {"status": "OK"}


@router.patch("/{room_id}", summary="Частичное обновление информации о номерах")
async def modify_room(
    db: DB_DEP, hotel_id: int, room_title: str, room_data: RoomPatchRequest
):
    _room_data = RoomPatch(
        hotel_id=hotel_id,
        **room_data.model_dump(exclude_unset=True),
    )

    await db.rooms.edit(
        _room_data,
        exclude_unset=True,
        hotel_id=hotel_id,
        title=room_title,
    )
    await db.commit()

    return {"status": "OK"}


@router.delete("/{room_id}", summary="Удалить номер в отеле")
async def delete_room(db: DB_DEP, hotel_id: int, room_title: str):
    await db.rooms.delete(hotel_id=hotel_id, title=room_title)
    await db.commit()

    return {"status": "OK"}
