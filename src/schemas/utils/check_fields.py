from typing import Annotated
from pydantic import AfterValidator
from pydantic_core import PydanticCustomError

from conf import SETTINGS


def validate_password(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PydanticCustomError("password_empty", "Пароль не может быть пустым")
    if len(value) < SETTINGS.MIN_PASSSWORD_LEN:
        raise PydanticCustomError(
            "password_too_short",
            f"Пароль должен содержать минимум {SETTINGS.MIN_PASSSWORD_LEN} символа",
        )
    return value


def validate_str(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PydanticCustomError("non_empty_str", "Строка не может быть пустой")
    # if len(value) < SETTINGS.MIN_FIELD_LEN:
    #    raise PydanticCustomError(
    #        "min_length",
    #        f"Строка должна содержать минимум {SETTINGS.MIN_FIELD_LEN} символ",
    #    )
    return value


PasswordStr = Annotated[str, AfterValidator(validate_password)]
FieldStr = Annotated[str, AfterValidator(validate_str)]
