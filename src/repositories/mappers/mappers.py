from models.hotels import HotelsOrm
from repositories.mappers.base import DataMapper
from schemas.hotels import Hotel


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel
