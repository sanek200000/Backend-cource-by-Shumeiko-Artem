from fastapi import HTTPException
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

from conf import SETTINGS
from services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict):
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

    def encode_token(self, token: str):
        try:
            return jwt.decode(
                token,
                SETTINGS.JWT_SECRET_KEY,
                algorithms=[SETTINGS.JWT_ALGORITHM],
            )
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Неверный токен")
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Срок действия подписи истек")
