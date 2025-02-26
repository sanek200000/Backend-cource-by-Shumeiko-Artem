from pydantic_core import PydanticCustomError, core_schema


class PasswordStr(str):
    """
    Пользовательский тип для пароля.
    Пароль должен быть не пустым и содержать минимум 3 символа.
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        """
        Метод, который определяет схему валидации для пользовательского типа.
        """
        return core_schema.with_info_plain_validator_function(cls._validate)

    @classmethod
    def _validate(
        cls, value: str, info: core_schema.ValidationInfo
    ) -> str:  # Убрали параметр info
        """
        Валидация пароля.
        """
        if not value or not value.strip():
            raise PydanticCustomError("password_empty", "Пароль не может быть пустым")
        if len(value) < 3:
            raise PydanticCustomError(
                "password_too_short",
                "Пароль должен содержать минимум 3 символа",
            )
        return cls(value)
