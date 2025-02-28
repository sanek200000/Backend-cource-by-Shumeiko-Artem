from pydantic import BaseModel, ConfigDict

from schemas.facilities import Facility
from schemas.utils.check_fields import FieldStr


class RoomAdd(BaseModel):
    hotel_id: int
    title: FieldStr
    description: str | None = None
    price: int
    quantity: int


class RoomAddRequest(BaseModel):
    title: FieldStr
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] = []


class Room(RoomAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class RoomWithRels(Room):
    facilities: list[Facility]


class RoomPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None


class RoomPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] = []
