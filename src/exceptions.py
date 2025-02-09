class BaseException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjictNotFoundException(BaseException):
    detail = "Объект не найден"
