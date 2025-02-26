from pydantic import BaseModel, ConfigDict, EmailStr

from schemas.utils.check_fields import PasswordStr


class UserRequestAdd(BaseModel):
    name: str
    email: EmailStr
    password: PasswordStr


class UserAdd(BaseModel):
    name: str
    email: EmailStr
    hashed_password: str


class User(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserWithHashedPassword(User):
    hashed_password: str
