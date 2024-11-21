from fastapi import APIRouter, Body, HTTPException

from api.dependences import DB_DEP, UserIdDep
from schemas.bookings import BookingAdd, BookingAddRequest


router = APIRouter(prefix="/bookings", tags=["Бронирование номеров"])


@router.get("/", summary="Посмотреть все бронирования")
async def get_all_bookings(db: DB_DEP):
    return await db.bookings.get_all()


@router.get("/me", summary="Посмотреть мои бронирования")
async def get_all_bookings(db: DB_DEP, user_id: UserIdDep):
    return await db.bookings.get_filtred(user_id=user_id)


@router.post("/", summary="Добавить бронирование")
async def create_booking(
    db: DB_DEP,
    user_id: UserIdDep,
    booking_data: BookingAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Бронирование1",
                "value": {
                    "room_id": 7,
                    "date_from": "2024-11-01",
                    "date_to": "2024-11-10",
                },
            },
            "2": {
                "summary": "Бронирование2",
                "value": {
                    "room_id": 7,
                    "date_from": "2024-10-25",
                    "date_to": "2024-11-05",
                },
            },
            "3": {
                "summary": "Бронирование3",
                "value": {
                    "room_id": 7,
                    "date_from": "2024-11-09",
                    "date_to": "2024-11-20",
                },
            },
        }
    ),
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
