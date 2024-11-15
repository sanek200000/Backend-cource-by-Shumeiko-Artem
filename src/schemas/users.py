from pydantic import BaseModel, ConfigDict


class UserRequestAdd(BaseModel):
    name: str
    email: str
    password: str


class UserAdd(BaseModel):
    name: str
    email: str
    hashed_password: str


class User(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)
