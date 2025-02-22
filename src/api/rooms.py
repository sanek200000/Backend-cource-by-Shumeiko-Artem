from datetime import date
from fastapi import APIRouter, Body, Query

from api.dependences import DB_DEP

from exceptions import (
    HotelNotFoundException,
    HotelNotFoundHTTPException,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
)
from schemas.rooms import RoomAddRequest, RoomPatchRequest
from services.rooms import RoomService
from utils.openapi_examples import RoomsOE


router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Нумера"])


@router.get("/", summary="Посмотреть все номера в отеле")
async def get_rooms_in_hotel(
    db: DB_DEP,
    hotel_id: int,
    date_from: date = Query(example="2024-11-01"),
    date_to: date = Query(example="2024-11-08"),
):
    return await RoomService(db).get_rooms_in_hotel(hotel_id, date_from, date_to)


@router.get("/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DB_DEP):
    try:
        return await RoomService(db).get_room(hotel_id=hotel_id, room_id=room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("/", summary="Добавить номер в список")
async def create_room(
    db: DB_DEP,
    hotel_id: int,
    room_data: RoomAddRequest = Body(openapi_examples=RoomsOE.create),
):
    try:
        room = await RoomService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK", "data": room}


@router.put("/{room_id}", summary="Обновление информации о номерах")
async def modify_room(
    db: DB_DEP,
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest,
):
    try:
        await RoomService(db).modify_room(hotel_id, room_id, room_data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK"}


@router.patch("/{room_id}", summary="Частичное обновление информации о номерах")
async def edit_room(
    db: DB_DEP,
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
):
    try:
        await RoomService(db).edit_room(hotel_id, room_id, room_data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK"}


@router.delete("/{room_id}", summary="Удалить номер в отеле")
async def delete_room(hotel_id: int, room_id: int, db: DB_DEP):
    try:
        await RoomService(db).delete_room(hotel_id, room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK"}
