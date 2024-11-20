from models.rooms import RoomsOrm
from repositories.base import BaseRepository
from schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room
