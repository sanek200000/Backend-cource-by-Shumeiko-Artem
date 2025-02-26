from typing import Annotated
from fastapi import Depends, Query, Request
from pydantic import BaseModel

from db import ASYNC_SESSION_MAKER
from exceptions import (
    IncorrectTokenException,
    IncorrectTokenHTTPException,
    NoAccessTokenHTTPException,
    TokenExpiredException,
    TokenExpiredHTTPException,
)
from services.auth import AuthService
from utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, gt=0)]
    per_page: Annotated[int | None, Query(None, gt=0, lt=21)]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request):
    token = request.cookies.get("access_tocken")
    if token:
        return token
    raise NoAccessTokenHTTPException


def get_current_user_id(token: str = Depends(get_token)):
    try:
        data = AuthService().decode_token(token)
    except IncorrectTokenException:
        raise IncorrectTokenHTTPException
    except TokenExpiredException:
        raise TokenExpiredHTTPException
    return data.get("user_id")


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=ASYNC_SESSION_MAKER) as db:
        yield db


DB_DEP = Annotated[int, Depends(get_db)]
