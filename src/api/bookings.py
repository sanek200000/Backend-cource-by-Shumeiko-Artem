from fastapi import APIRouter

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
    user_request = await db.users.get_one_or_none(id=user_id)
    user_id = user_request.model_dump().get("id")

    _booking_data = BookingAdd(user_id=user_id, **booking_data.model_dump())
    booking = await db.bookings.add(_booking_data)
    await db.commit()

    return {"status": "OK", "data": booking}
