from api.dependences import UserIdDep

from schemas.bookings import BookingAdd, BookingAddRequest
from services.base import BaseService
from services.rooms import RoomService


class BookingService(BaseService):
    async def get_my_bookings(self, user_id: UserIdDep):
        return await self.db.bookings.get_filtred(user_id=user_id)

    async def create_booking(self, user_id: UserIdDep, booking_data: BookingAddRequest):
        room = await RoomService(self.db).get_room_in_hotel_with_check(
            None,
            booking_data.room_id,
        )

        hotel = await self.db.hotels.get_one(id=room.hotel_id)
        room_price: int = room.price

        _booking_data = BookingAdd(
            user_id=user_id,
            price=room_price,
            **booking_data.model_dump(),
        )

        booking = await self.db.bookings.add_bookings(
            _booking_data,
            hotel_id=hotel.id,
        )

        await self.db.commit()
        return booking

    async def delete_booking(self, booking_id: int):
        await self.db.bookings.get_one(id=booking_id)
        await self.db.bookings.delete(id=booking_id)
        await self.db.commit()
