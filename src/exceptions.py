class BaseException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjictNotFoundException(BaseException):
    detail = "Объект не найден"


class AllRoomsAreBookedException(BaseException):
    detail = "Не осталось свободных номеров"


class UserAlradyExistException(BaseException):
    detail = "Пользователь с таким именеи или почтой уже зарегестрирован."


class DateToEaelierDateFromException(BaseException):
    detail = "Дата выезда раньше даты заезда."
