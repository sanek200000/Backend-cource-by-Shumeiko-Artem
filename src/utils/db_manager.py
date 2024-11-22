from sqlalchemy.orm import Session
from repositories.bookings import BookingsRepository
from repositories.facilities import FacilitiesRepository
from repositories.hotels import HotelsRepository
from repositories.rooms import RoomsRepository
from repositories.users import UsersRepository


class DBManager:
    def __init__(self, session_factory) -> None:
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session: Session = self.session_factory()

        self.hotels = HotelsRepository(self.session)
        self.rooms = RoomsRepository(self.session)
        self.bookings = BookingsRepository(self.session)
        self.users = UsersRepository(self.session)
        self.facilities = FacilitiesRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
