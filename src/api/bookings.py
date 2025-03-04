from fastapi import APIRouter, Body

from api.dependences import DB_DEP, UserIdDep
from exceptions import (
    AllRoomsAreBookedException,
    AllRoomsAreBookedHTTPException,
    BookingNotFoundHTTPException,
    DateToEaelierDateFromException,
    DateToEaelierDateFromHTTPException,
    ObjictNotFoundException,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
)
from schemas.bookings import BookingAddRequest
from services.bookings import BookingService
from utils.openapi_examples import BookingOE


router = APIRouter(prefix="/bookings", tags=["Бронирование номеров"])


@router.get("", summary="Посмотреть все бронирования")
async def get_all_bookings(db: DB_DEP):
    return await db.bookings.get_all()


@router.get("/me", summary="Посмотреть мои бронирования")
async def get_my_bookings(db: DB_DEP, user_id: UserIdDep):
    return await BookingService(db).get_my_bookings(user_id)


@router.post("", summary="Добавить бронирование")
async def create_booking(
    db: DB_DEP,
    user_id: UserIdDep,
    booking_data: BookingAddRequest = Body(openapi_examples=BookingOE.create),
):
    try:
        booking = await BookingService(db).create_booking(user_id, booking_data)
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except DateToEaelierDateFromException:
        raise DateToEaelierDateFromHTTPException
    return {"status": "OK", "data": booking}


@router.delete("/{booking_id}", summary="Удалить бронирование")
async def delete_booking(db: DB_DEP, booking_id: int):
    try:
        await BookingService(db).delete_booking(booking_id)
    except ObjictNotFoundException:
        raise BookingNotFoundHTTPException
    return {"status": "Ok"}
