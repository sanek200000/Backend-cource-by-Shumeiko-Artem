from fastapi import APIRouter, Body

from db import async_session_maker

from repositories.rooms import RoomsRepository
from schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest


router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Нумера"])


@router.get("/", summary="Посмотреть все номера в отеле")
async def get_rooms_in_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtred(hotel_id=hotel_id)


@router.post("/", summary="Добавить номер в список")
async def create_room(
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
    async with async_session_maker() as session:
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

        room = await RoomsRepository(session).add(_room_data)
        await session.commit()

    return {"status": "OK", "data": room}


@router.put("/{room_id}", summary="Обновление информации о номерах")
async def modify_room(room_id: int, room_data: RoomAdd):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, id=room_id)
        await session.commit()

    return {"status": "OK"}


@router.patch("/{room_id}", summary="Частичное обновление информации о номерах")
async def modify_room(hotel_id: int, room_title: str, room_data: RoomPatchRequest):
    _room_data = RoomPatch(
        hotel_id=hotel_id,
        **room_data.model_dump(exclude_unset=True),
    )

    async with async_session_maker() as session:
        await RoomsRepository(session).edit(
            _room_data,
            exclude_unset=True,
            hotel_id=hotel_id,
            title=room_title,
        )
        await session.commit()

    return {"status": "OK"}


@router.delete("/{room_id}", summary="Удалить вид номера в отеле")
async def delete_room(hotel_id: int, room_title: str):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id=hotel_id, title=room_title)
        await session.commit()

    return {"status": "OK"}
