from datetime import date
from schemas.bookings import BookingAdd, BookingPatch


async def test_booking_CRUD(db):
    room_id = (await db.rooms.get_all())[0].id
    user_id = (await db.users.get_all())[0].id

    booking_data = BookingAdd(
        room_id=room_id,
        user_id=user_id,
        date_from=date(year=2024, month=12, day=1),
        date_to=date(year=2024, month=12, day=10),
        price=100,
    )
    booking_data_ = BookingPatch(price=200)

    # Вносим запись в БД
    response_add = await db.bookings.add(booking_data)
    booking_id = response_add.id

    # Проверяем запись в БД
    response_get = await db.bookings.get_one_or_none(id=booking_id)
    assert response_add == response_get

    # Изменяем запись в БД
    await db.bookings.edit(booking_data_, exclude_unset=True, id=booking_id)
    response_get = await db.bookings.get_one_or_none(id=booking_id)
    assert response_get.price == 200

    # Удаляем запись из БД
    response_delete = await db.bookings.delete(id=booking_id)
    assert response_delete == None

    await db.commit()
