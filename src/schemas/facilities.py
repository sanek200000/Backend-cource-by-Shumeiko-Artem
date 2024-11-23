from pydantic import BaseModel, ConfigDict


class FacilitiesAdd(BaseModel):
    title: str


class Facility(FacilitiesAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class RoomsFacilityAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomsFacility(RoomsFacilityAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)
