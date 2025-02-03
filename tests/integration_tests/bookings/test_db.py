from datetime import date
from schemas.bookings import BookingAdd


async def test_add_booking(db):
    room_id = (await db.rooms.get_all())[0].id
    user_id = (await db.users.get_all())[0].id

    booking_data = BookingAdd(
        room_id=room_id,
        user_id=user_id,
        date_from=date(year=2024, month=12, day=1),
        date_to=date(year=2024, month=12, day=10),
        price=100,
    )

    await db.bookings.add(booking_data)
    await db.commit()
