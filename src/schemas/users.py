from pydantic import BaseModel, ConfigDict, EmailStr

from schemas.utils.check_fields import FieldStr, PasswordStr


class UserRequestAdd(BaseModel):
    name: FieldStr
    email: EmailStr
    password: PasswordStr


class UserAdd(BaseModel):
    name: FieldStr
    email: EmailStr
    hashed_password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: PasswordStr


class User(BaseModel):
    id: int
    name: FieldStr
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserWithHashedPassword(User):
    hashed_password: str
