from fastapi import APIRouter, HTTPException, Response

from schemas.users import UserAdd, UserRequestAdd
from services.auth import AuthService
from api.dependences import DB_DEP, UserIdDep


router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.delete("/logout", summary="Выход из системы")
async def logout(response: Response):
    response.delete_cookie("access_tocken")
    return {"status": "OK"}


@router.get("/me", summary="Получение токена авторизации")
async def get_me(db: DB_DEP, user_id: UserIdDep):

    return await db.users.get_one_or_none(id=user_id)


@router.post("/register", summary="Регистрация")
async def register_user(db: DB_DEP, data: UserRequestAdd):
    hashed_password = AuthService().pwd_context.hash(data.password)
    new_user_data = UserAdd(
        name=data.name,
        email=data.email,
        hashed_password=hashed_password,
    )

    await db.users.add(new_user_data)
    await db.commit()

    return {"status": "OK"}


@router.post("/login", summary="LogIn")
async def login_user(db: DB_DEP, data: UserRequestAdd, response: Response):
    user = await db.users.get_user_with_hashed_password(email=data.email)

    if user and AuthService().verify_password(data.password, user.hashed_password):
        access_tocken = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_tocken", access_tocken)
        return {"access_tocken": access_tocken}

    raise HTTPException(status_code=401, detail="Неверный логин или пароль")
