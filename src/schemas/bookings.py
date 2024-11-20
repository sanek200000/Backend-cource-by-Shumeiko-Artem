from datetime import date
from pydantic import BaseModel, ConfigDict


class BookingAdd(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int


class BookingAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date
    price: int


class Booking(BookingAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)
