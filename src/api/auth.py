from fastapi import APIRouter, Body, Request, Response

from exceptions import (
    EmailNotRegisteredException,
    EmailNotRegisteredHTTPException,
    IncorrectPasswordException,
    IncorrectPasswordHTTPException,
    ObjictNotFoundException,
    UserAlradyExistException,
    UserAlradyExistHTTPException,
    UserNotrAuthHTTPException,
)
from schemas.users import UserRequestAdd
from services.auth import AuthService
from api.dependences import DB_DEP, UserIdDep
from utils.openapi_examples import AuthOE


router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.get("/me", summary="Получение токена авторизации")
async def get_me(db: DB_DEP, user_id: UserIdDep):
    return await AuthService(db).get_me(user_id)


@router.post("/register", summary="Регистрация")
async def register_user(
    db: DB_DEP,
    data: UserRequestAdd = Body(openapi_examples=AuthOE.register),
):

    try:
        await AuthService(db).register_user(data)
    except UserAlradyExistException:
        raise UserAlradyExistHTTPException
    return {"status": "OK"}


@router.post("/login", summary="LogIn")
async def login_user(
    db: DB_DEP,
    response: Response,
    data: UserRequestAdd = Body(openapi_examples=AuthOE.login),
):
    try:
        access_tocken = await AuthService(db).login_user(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException

    response.set_cookie("access_tocken", access_tocken)
    return {"access_tocken": access_tocken}


@router.post("/logout", summary="Выход из системы")
async def logout(request: Request, response: Response):
    try:
        await AuthService().logout(request, response)
    except ObjictNotFoundException:
        raise UserNotrAuthHTTPException
    return {"status": "OK"}
