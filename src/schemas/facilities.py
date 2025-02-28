from pydantic import BaseModel, ConfigDict

from schemas.utils.check_fields import FieldStr


class FacilitiesAdd(BaseModel):
    title: FieldStr


class Facility(FacilitiesAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class RoomsFacilityAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomsFacility(RoomsFacilityAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)
