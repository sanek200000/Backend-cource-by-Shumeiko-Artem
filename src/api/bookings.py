from fastapi import APIRouter, HTTPException

from api.dependences import DB_DEP, UserIdDep
from schemas.bookings import BookingAdd, BookingAddRequest


router = APIRouter(prefix="/bookings", tags=["Бронирование номеров"])


@router.get("/", summary="Посмотреть все бронирования")
async def get_all_bookings(db: DB_DEP):
    return await db.bookings.get_all()


@router.post("/", summary="Добавить бронирование")
async def create_booking(
    db: DB_DEP,
    booking_data: BookingAddRequest,
    user_id: UserIdDep,
):
    try:
        room = await db.rooms.get_one_or_none(id=booking_data.room_id)
        room_price: int = room.price
    except AttributeError:
        raise HTTPException(status_code=404, detail="Такого номера не существует")

    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )

    booking = await db.bookings.add(_booking_data)
    await db.commit()

    return {"status": "OK", "data": booking}
