from pydantic import BaseModel, ConfigDict

from schemas.facilities import Facility
from schemas.utils.check_fields import FieldInt, FieldStr


class RoomAdd(BaseModel):
    hotel_id: int
    title: FieldStr
    description: str | None = None
    price: FieldInt
    quantity: FieldInt


class RoomAddRequest(BaseModel):
    title: FieldStr
    description: str | None = None
    price: FieldInt
    quantity: FieldInt
    facilities_ids: list[int] = []


class Room(RoomAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class RoomWithRels(Room):
    facilities: list[Facility]


class RoomPatch(BaseModel):
    hotel_id: int | None = None
    title: FieldStr | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None


class RoomPatchRequest(BaseModel):
    title: FieldStr | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] = []
