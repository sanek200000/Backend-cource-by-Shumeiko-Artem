from datetime import date
from fastapi import HTTPException


class BaseException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjictNotFoundException(BaseException):
    detail = "Объект не найден"


class RoomNotFoundException(ObjictNotFoundException):
    detail = "Номер не найден."


class HotelNotFoundException(ObjictNotFoundException):
    detail = "Отель не найден."


class BookingNotFoundException(ObjictNotFoundException):
    detail = "Бронирование не найдено."


class AllRoomsAreBookedException(BaseException):
    detail = "Не осталось свободных номеров"


class UserAlradyExistException(BaseException):
    detail = "Похожий объект уже существует."


class DateToEaelierDateFromException(BaseException):
    detail = "Дата выезда раньше даты заезда."


class EmailNotRegisteredException(BaseException):
    detail = "Пользователь с таким email не зарегистрирован"


class IncorrectPasswordException(BaseException):
    detail = "Пароль неверный"


class IncorrectTokenException(BaseException):
    detail = "Некорректный токен"


class TokenExpiredException(BaseException):
    detail = "Срок действия токена истек"


"""=========================================== HTTP Exceptions ==============================="""


class BaseHTTPException(HTTPException):
    status_code = 500
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserNotrAuthHTTPException(BaseHTTPException):
    status_code = 401
    detail = "Не войдено."


class TokenExpiredHTTPException(BaseHTTPException):
    status_code = 401
    detail = "Срок действия токена истек"


class EmailNotRegisteredHTTPException(BaseHTTPException):
    status_code = 401
    detail = "Пользователь с таким email не зарегистрирован"


class IncorrectPasswordHTTPException(BaseHTTPException):
    status_code = 401
    detail = "Пароль неверный"


class UserAlradyExistHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Такой пользователь уже существует."


class RoomNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Номер не найден."


class HotelNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Отель не найден."


class BookingNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Бронирование не найдено."


class NoAccessTokenHTTPException(BaseHTTPException):
    status_code = 401
    detail = "Вы не предоставили токен доступа"


class IncorrectTokenHTTPException(BaseHTTPException):
    detail = "Некорректный токен"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(
            status_code=422, detail="Дата заезда не может быть позже даты выезда"
        )
