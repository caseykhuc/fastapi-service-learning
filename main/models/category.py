from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel, TimestampMixin

if TYPE_CHECKING:
    from .item import ItemModel


class CategoryModel(BaseModel, TimestampMixin):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str] = mapped_column(String(5000))
    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    items: Mapped[list["ItemModel"]] = relationship(
        back_populates="category",
        lazy="raise",
        cascade="all, delete",
    )
