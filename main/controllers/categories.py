from typing import Annotated

from fastapi import APIRouter, Depends

from main.engines.categories import (
    add_category,
    delete_category,
    get_categories,
)
from main.schemas.base import Empty
from main.schemas.category import CategoryCreatePayloadSchema, CategorySchema
from main.utils.auth import RequestedUserId, require_authentication
from main.utils.category import (
    RequestedCategory,
    get_category_schema,
    require_category_creator,
    validate_category_name,
)
from main.utils.common import PositiveIntPath

router: APIRouter = APIRouter()


@router.get(
    "/categories",
    response_model=list[CategorySchema],
)
async def _get_categories(user_id: RequestedUserId):
    return [
        get_category_schema(category, user_id) for category in await get_categories()
    ]


@router.post(
    "/categories",
    response_model=CategorySchema,
)
async def _add_category(
    category: CategoryCreatePayloadSchema,
    user_id: Annotated[int, Depends(require_authentication)],
):
    await validate_category_name(category.name)
    return get_category_schema(
        await add_category(**category.__dict__, creator_id=user_id),
        user_id,
    )


@router.get(
    "/categories/{category_id}",
    response_model=CategorySchema,
)
async def _get_category(category: RequestedCategory, user_id: RequestedUserId):
    return get_category_schema(category, user_id)


@router.delete(
    "/categories/{category_id}",
    response_model=Empty,
    dependencies=[Depends(require_category_creator)],
)
async def _delete_category(
    category_id: PositiveIntPath,
):
    await delete_category(category_id)

    return Empty()
