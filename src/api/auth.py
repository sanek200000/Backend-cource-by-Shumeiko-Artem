from sys import prefix
from fastapi.routing import APIRoute

from repositories.users import UsersRepository
from schemas.users import UserAdd, UserRequestAdd
from db import async_session_maker


router = APIRoute(prefix="/auth", tags=["Аутентификация и авторизация"])


@router("/register")
async def register_user(data: UserRequestAdd):

    hashed_password = "dfsdfsdf34rawfdsf34r300"
    new_user_data = UserAdd(
        name=data.name,
        email=data.email,
        hashed_password=hashed_password,
    )

    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit

    return {"status": "OK"}
