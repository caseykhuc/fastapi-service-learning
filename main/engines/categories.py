from collections.abc import Sequence

from sqlalchemy import delete, select

from main import db
from main.models.category import CategoryModel


async def get_categories() -> Sequence[CategoryModel]:
    statement = select(CategoryModel)
    result = await db.session.execute(statement)
    return result.scalars().all()


async def add_category(
    name: str,
    creator_id: int,
) -> CategoryModel:
    category = CategoryModel(name=name, creator_id=creator_id)

    db.session.add(category)
    await db.session.commit()

    return category


async def get_category_by_id(id: int) -> CategoryModel | None:
    statement = select(CategoryModel).where(CategoryModel.id == id)
    result = await db.session.execute(statement)
    return result.scalar()


async def get_category_by_name(name: str) -> CategoryModel | None:
    statement = select(CategoryModel).where(CategoryModel.name == name)
    result = await db.session.execute(statement)
    return result.scalar()


async def delete_category(id: int):
    statement = delete(CategoryModel).where(CategoryModel.id == id)

    await db.session.execute(statement)
    await db.session.commit()
