from sys import prefix
from fastapi import APIRouter

from repositories.users import UsersRepository
from schemas.users import UserAdd, UserRequestAdd
from db import async_session_maker


router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", summary="Регистрация")
async def register_user(data: UserRequestAdd):

    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(
        name=data.name,
        email=data.email,
        hashed_password=hashed_password,
    )

    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}
