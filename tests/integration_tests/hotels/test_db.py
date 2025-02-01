from db import ASYNC_SESSION_MAKER
from schemas.hotels import HotelAdd
from utils.db_manager import DBManager


async def test_add_hotel():
    hotel_data = HotelAdd(title="Hotel 5 stars", location="Sochi")

    async with DBManager(session_factory=ASYNC_SESSION_MAKER) as db:
        new_hotel_data = await db.hotels.add(hotel_data)
        await db.commit()
