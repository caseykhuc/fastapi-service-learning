from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel, TimestampMixin


class UserModel(BaseModel, TimestampMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(64), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(64))
