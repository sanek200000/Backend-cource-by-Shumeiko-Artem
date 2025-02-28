from pydantic import BaseModel, Field

from schemas.utils.check_fields import FieldStr


class HotelAdd(BaseModel):
    title: FieldStr
    location: FieldStr


class Hotel(HotelAdd):
    id: int


class HotelPatch(BaseModel):
    title: FieldStr | None = Field(default=None)
    location: FieldStr | None = Field(default=None)
