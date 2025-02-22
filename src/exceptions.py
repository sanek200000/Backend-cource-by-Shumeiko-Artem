from datetime import date
from fastapi import HTTPException


class BaseException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class BaseHTTPException(HTTPException):
    status_code = 500
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(status_code=self.status_code, detail=self.detail)


class ObjictNotFoundException(BaseException):
    detail = "Объект не найден"


class RoomNotFoundException(ObjictNotFoundException):
    detail = "Номер не найден."

class HotelNotFoundException(ObjictNotFoundException):
    detail = "Отель не найден."


class AllRoomsAreBookedException(BaseException):
    detail = "Не осталось свободных номеров"


class UserAlradyExistException(BaseException):
    detail = "Похожий объект уже существует."


class DateToEaelierDateFromException(BaseException):
    detail = "Дата выезда раньше даты заезда."


class RoomNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Номер не найден."


class HotelNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Отель не найден."


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(
            status_code=422, detail="Дата заезда не может быть позже даты выезда"
        )
