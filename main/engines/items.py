from collections.abc import Sequence

from sqlalchemy import delete, func, select

from main import db
from main.models.item import ItemModel


async def count_items(category_id: int) -> int:
    statement = (
        select(func.count())
        .select_from(ItemModel)
        .where(ItemModel.category_id == category_id)
    )
    result = await db.session.execute(statement)
    return result.scalar() or 0


async def get_items(category_id: int, offset: int, limit: int) -> Sequence[ItemModel]:
    statement = (
        select(ItemModel)
        .where(ItemModel.category_id == category_id)
        .offset(offset)
        .limit(limit)
    )
    result = await db.session.execute(statement)
    return result.scalars().all()


async def add_item(
    name: str,
    description: str,
    category_id: int,
    creator_id: int,
) -> ItemModel:
    item = ItemModel(
        name=name,
        description=description,
        creator_id=creator_id,
        category_id=category_id,
    )

    db.session.add(item)
    await db.session.commit()

    return item


async def get_item_by_id(id: int) -> ItemModel | None:
    statement = select(ItemModel).where(ItemModel.id == id)
    result = await db.session.execute(statement)
    return result.scalar()


async def get_item_by_name(name: str) -> ItemModel | None:
    statement = select(ItemModel).where(ItemModel.name == name)
    result = await db.session.execute(statement)
    return result.scalar()


async def update_item(id: int, name: str, description: str) -> ItemModel | None:
    item = await get_item_by_id(id)

    if not item:
        return None

    if name:
        item.name = name
    if description:
        item.description = description

    await db.session.commit()
    return item


async def delete_item(id: int):
    statement = delete(ItemModel).where(ItemModel.id == id)

    await db.session.execute(statement)
    await db.session.commit()
