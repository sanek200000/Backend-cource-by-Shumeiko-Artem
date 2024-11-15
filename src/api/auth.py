from datetime import datetime, timedelta, timezone
import email
from fastapi import APIRouter, HTTPException
import jwt

from repositories.users import UsersRepository
from schemas.users import UserAdd, UserRequestAdd
from db import async_session_maker


router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


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


@router.post("/login", summary="LogIn")
async def login_user(data: UserRequestAdd):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(email=data.email)
        if user:
            access_tocken = create_access_token({"user_id": user.id})
            return {"access_tocken": access_tocken}

        raise HTTPException(
            status_code=401,
            detail="Пользователь с таким email не зарегистрирован",
        )
