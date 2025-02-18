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
