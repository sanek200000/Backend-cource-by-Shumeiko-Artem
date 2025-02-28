from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from db import Base


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=100))
    email: Mapped[str] = mapped_column(String(length=50), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(length=64))
