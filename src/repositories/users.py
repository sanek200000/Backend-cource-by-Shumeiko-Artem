from pydantic import EmailStr
from sqlalchemy import select
from repositories.base import BaseRepository
from models.users import UsersOrm
from repositories.mappers.mappers import (
    UserDataMapper,
    UserWithHashedPasswordDataMapper,
)


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)

        if row := result.scalars().one_or_none():
            print(f"{row = }")
            return UserWithHashedPasswordDataMapper.map_to_domain_entity(row)
