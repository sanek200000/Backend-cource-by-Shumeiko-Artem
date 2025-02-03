from db import ASYNC_SESSION_MAKER_NULL_POOL
from schemas.hotels import HotelAdd
from utils.db_manager import DBManager


async def test_add_hotel(db):
    hotel_data = HotelAdd(title="Hotel 5 stars", location="Sochi")
    new_hotel_data = await db.hotels.add(hotel_data)
    await db.commit()
