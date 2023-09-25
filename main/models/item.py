from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel

if TYPE_CHECKING:
    from .category import CategoryModel


class ItemModel(BaseModel):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(5000))
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    category: Mapped["CategoryModel"] = relationship(lazy="raise")
    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
