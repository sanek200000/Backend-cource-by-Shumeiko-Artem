from pydantic import BaseModel
from sqlalchemy import select
from models.rooms import RoomsOrm
from repositories.base import BaseRepository
from schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all(self, hotel_id: int):
        query = select(self.model).filter_by(hotel_id=hotel_id)

        print(query.compile(compile_kwargs={"literal_binds": True}))

        result = await self.session.execute(query)
        return [
            self.schema.model_validate(row, from_attributes=True)
            for row in result.scalars().all()
        ]
