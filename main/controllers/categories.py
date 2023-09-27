from typing import Annotated

from fastapi import APIRouter, Depends

from main.commons.exceptions import NotFound
from main.engines.categories import (
    add_category,
    delete_category,
    get_categories,
)
from main.schemas.base import Empty
from main.schemas.category import CategoryCreatePayloadSchema, CategorySchema
from main.utils.auth import require_authentication
from main.utils.category import (
    get_category_or_404,
    require_category_creator,
    validate_category_name,
)

router: APIRouter = APIRouter()


@router.get(
    "/categories",
    response_model=list[CategorySchema],
)
async def _get_categories():
    categories = await get_categories()
    return categories


@router.post(
    "/categories",
    response_model=CategorySchema,
)
async def _add_category(
    category: CategoryCreatePayloadSchema,
    user_id: Annotated[int, Depends(require_authentication)],
):
    await validate_category_name(category.name)
    category = await add_category(name=category.name, creator_id=user_id)

    if not category:
        raise NotFound()

    return category


@router.get(
    "/categories/{category_id}",
    response_model=CategorySchema,
)
async def _get_category(category_id: int):
    category = await get_category_or_404(category_id)
    return category


@router.delete(
    "/categories/{category_id}",
    response_model=Empty,
    dependencies=[Depends(require_category_creator)],
)
async def _delete_category(
    category_id: int,
):
    await delete_category(category_id)

    return Empty()
