from api.dependences import UserIdDep
from services.base import BaseService


class BookingService(BaseService):
    async def get_my_bookings(self, user_id: UserIdDep):
        return await self.db.bookings.get_filtred(user_id=user_id)
