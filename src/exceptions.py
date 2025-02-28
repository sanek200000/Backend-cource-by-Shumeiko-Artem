from datetime import date
from fastapi import HTTPException

from conf import SETTINGS


class BaseException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjictNotFoundException(BaseException):
    detail = "Объект не найден"


class ObjictAlradyExistException(BaseException):
    detail = "Похожий объект уже существует."


class RoomNotFoundException(ObjictNotFoundException):
    detail = "Номер не найден."


class HotelNotFoundException(ObjictNotFoundException):
    detail = "Отель не найден."


class BookingNotFoundException(ObjictNotFoundException):
    detail = "Бронирование не найдено."


class AllRoomsAreBookedException(BaseException):
    detail = "Не осталось свободных номеров"


class UserAlradyExistException(ObjictAlradyExistException):
    detail = "Такой пользователь уже существует."


class HotelAlradyExistException(ObjictAlradyExistException):
    detail = "Такой отель уже существует."


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


class EmptyFieldException(BaseException):
    detail = "Строка не может быть пустой"


class TooShortFieldException(BaseException):
    detail = "Строка слишком короткая"


class EmptyPasswordException(BaseException):
    detail = "Строка не может быть пустой"


class TooShortPasswordException(BaseException):
    detail = "Строка слишком короткая"


"""=========================================== HTTP Exceptions ==============================="""


class BaseHTTPException(HTTPException):
    status_code = 500
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(status_code=self.status_code, detail=self.detail)


class AllRoomsAreBookedHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Не осталось свободных номеров."


class DateToEaelierDateFromHTTPException(BaseHTTPException):
    status_code = 422
    detail = "Дата выезда раньше даты заезда."


class EmptyFielhHTTPException(BaseHTTPException):
    status_code = 415
    detail = "Строка не может быть пустой."


class EmptyPasswordHTTPException(BaseHTTPException):
    status_code = 415
    detail = "Пароль не может быть пустым."


class TooShortPasswordHTTPException(BaseHTTPException):
    status_code = 415
    detail = f"Пароль должен содержать минимум {SETTINGS.MIN_PASSSWORD_LEN} символа."


class TooShortFieldHTTPException(BaseHTTPException):
    status_code = 415
    detail = f"Строка должна содержать минимум {SETTINGS.MIN_FIELD_LEN} символ."


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


class FacilityAlradyExistHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Такая услуга уже есть в базе."


class HotelAlradyExistHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Такой отель уже существует."


class RoomAlradyExistHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Такой номер в этом отеле уже существует."


class RoomNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Номер не найден."


class HotelNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Отель не найден."


class FalicityNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Удобство не найдено."


class BookingNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Бронирование не найдено."


class NoAccessTokenHTTPException(BaseHTTPException):
    status_code = 401
    detail = "Вы не предоставили токен доступа"


class IncorrectTokenHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Некорректный токен"


class NoDataHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Нет данных для обновления"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(
            status_code=422, detail="Дата заезда не может быть позже даты выезда"
        )
