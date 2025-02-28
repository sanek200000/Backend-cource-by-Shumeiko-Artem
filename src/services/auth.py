from asyncpg import UniqueViolationError
from fastapi import Request, Response
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

from conf import SETTINGS
from exceptions import (
    EmailNotRegisteredException,
    IncorrectPasswordException,
    IncorrectTokenException,
    ObjictNotFoundException,
    TokenExpiredException,
    UserAlradyExistException,
)
from schemas.users import UserAdd, UserLogin, UserRequestAdd
from services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_tocken(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            SETTINGS.JWT_SECRET_KEY,
            algorithm=SETTINGS.JWT_ALGORITHM,
        )
        return encoded_jwt

    def hash_password(self, password: str):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_token(self, token: str):
        try:
            return jwt.decode(
                token,
                SETTINGS.JWT_SECRET_KEY,
                algorithms=[SETTINGS.JWT_ALGORITHM],
            )
        except jwt.exceptions.DecodeError:
            raise IncorrectTokenException
        except jwt.exceptions.ExpiredSignatureError:
            raise TokenExpiredException

    async def get_me(self, user_id: int):
        return await self.db.users.get_one_or_none(id=user_id)

    async def register_user(self, data: UserRequestAdd):
        hashed_password = self.pwd_context.hash(data.password)

        new_user_data = UserAdd(
            name=data.name,
            email=data.email,
            hashed_password=hashed_password,
        )

        try:
            await self.db.users.add(new_user_data)
        except UniqueViolationError:
            raise UserAlradyExistException

        await self.db.commit()

    async def login_user(self, data: UserLogin):

        user = await self.db.users.get_user_with_hashed_password(email=data.email)
        if not user:
            raise EmailNotRegisteredException
        if not self.verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordException

        access_tocken = self.create_access_tocken({"user_id": user.id})
        return access_tocken

    async def logout(self, request: Request, response: Response):
        if "access_tocken" in request.cookies:
            response.delete_cookie("access_tocken")
        else:
            raise ObjictNotFoundException
