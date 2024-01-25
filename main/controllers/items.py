from typing import Annotated

from fastapi import APIRouter, Depends

from main.engines.items import (
    add_item,
    count_items,
    delete_item,
    get_items,
    update_item,
)
from main.schemas.base import Empty
from main.schemas.item import (
    CategoryItemsSchema,
    ItemCreatePayloadSchema,
    ItemSchema,
    ItemUpdatePayloadSchema,
)
from main.utils.auth import RequestedUserId, require_authentication
from main.utils.category import get_category_from_request
from main.utils.common import PositiveIntPath, PositiveIntQuery
from main.utils.item import (
    RequestedItem,
    get_item_schema,
    require_item_creator,
    validate_item_name,
)

router: APIRouter = APIRouter()


DEFAULT_ITEMS_PER_PAGE = 20


@router.get(
    "/categories/{category_id}/items",
    response_model=CategoryItemsSchema,
    dependencies=[Depends(get_category_from_request)],
)
async def _get_category_items(
    category_id: PositiveIntPath,
    user_id: RequestedUserId,
    page: PositiveIntQuery = 1,
    number_per_page: PositiveIntQuery = DEFAULT_ITEMS_PER_PAGE,
):
    items = await get_items(
        category_id,
        (page - 1) * number_per_page,
        number_per_page,
    )
    total = await count_items(category_id)

    return CategoryItemsSchema(
        items=[get_item_schema(item, user_id) for item in items],
        total=total,
        page=page,
        number_per_page=number_per_page,
    )


@router.post(
    "/categories/{category_id}/items",
    response_model=ItemSchema,
    dependencies=[Depends(get_category_from_request)],
)
async def _add_category_items(
    category_id: PositiveIntPath,
    user_id: Annotated[int, Depends(require_authentication)],
    item_data: ItemCreatePayloadSchema,
):
    await validate_item_name(item_data.name)

    item = await add_item(
        **item_data.model_dump(),
        creator_id=user_id,
        category_id=category_id,
    )

    return get_item_schema(item, user_id)


@router.get("/items/{item_id}", response_model=ItemSchema)
async def _get_item(
    item: RequestedItem,
    user_id: RequestedUserId,
):
    return get_item_schema(item, user_id)


@router.put(
    "/items/{item_id}",
    response_model=ItemSchema,
)
async def _update_item(
    item: RequestedItem,
    item_data: ItemUpdatePayloadSchema,
    user_id: Annotated[int, Depends(require_item_creator)],
):
    if item_data.name:
        await validate_item_name(item_data.name)

    updated_item = await update_item(item.id, **item_data.model_dump())
    return get_item_schema(updated_item, user_id)


@router.delete(
    "/items/{item_id}",
    response_model=Empty,
    dependencies=[Depends(require_item_creator)],
)
async def _delete_item(
    item_id: PositiveIntPath,
):
    await delete_item(item_id)

    return Empty()
