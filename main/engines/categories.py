from collections.abc import Sequence

from sqlalchemy import delete, func, select
from sqlalchemy.exc import IntegrityError

from main import db
from main.commons.exceptions import BadRequest, ErrorCode, ErrorMessage, NotFound
from main.models.category import CategoryModel
from main.models.item import ItemModel


async def get_categories() -> Sequence[CategoryModel]:
    statement = select(CategoryModel)
    result = await db.session.execute(statement)
    return result.scalars().all()


async def get_count_items(category_id: int) -> int | None:
    statement = (
        select(func.count("*"))
        .select_from(ItemModel)
        .where(ItemModel.category_id == category_id)
    )
    result = await db.session.execute(statement)
    return result.scalar()


async def get_items(category_id: int, offset: int, limit: int) -> Sequence[ItemModel]:
    statement = (
        select(ItemModel)
        .where(ItemModel.category_id == category_id)
        .offset(offset)
        .limit(limit)
    )
    result = await db.session.execute(statement)
    return result.scalars().all()


async def add_category(
    name: str,
    creator_id: int,
) -> CategoryModel:
    category = CategoryModel(name=name, creator_id=creator_id)

    try:
        db.session.add(category)
        await db.session.commit()
    except IntegrityError:
        raise BadRequest(
            error_message=ErrorMessage.CATEGORY_NAME_EXISTS,
            error_code=ErrorCode.CATEGORY_NAME_EXISTS,
        )

    return category


async def get_category_by_id(id: int) -> CategoryModel | None:
    statement = select(CategoryModel).where(CategoryModel.id == id)
    result = await db.session.execute(statement)
    return result.scalar()


async def delete_category(id: int):
    statement = delete(CategoryModel).where(CategoryModel.id == id)
    try:
        await db.session.execute(statement)
        await db.session.commit()
    except IntegrityError:
        raise NotFound()
