from typing import Annotated

from fastapi import APIRouter, Depends

from main.commons.exceptions import NotFound
from main.engines.categories import (
    add_category,
    delete_category,
    get_categories,
    get_category_by_id,
)
from main.models.category import CategoryModel
from main.schemas.base import Empty
from main.schemas.category import CategoryCreatePayloadSchema, CategorySchema
from main.utils.auth import require_authentication, require_creator

router: APIRouter = APIRouter()


async def _get_category_or_404(id: int) -> CategoryModel:
    category = await get_category_by_id(id)

    if not category:
        raise NotFound()

    return category


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
    category = await add_category(name=category.name, creator_id=user_id)

    if not category:
        raise NotFound()

    return category


@router.delete(
    "/categories/{category_id}",
    response_model=Empty,
)
async def _delete_category(
    category_id: int,
    user_id: Annotated[int, Depends(require_authentication)],
):
    category = await _get_category_or_404(category_id)

    await require_creator(category.creator_id, user_id)

    category = await delete_category(category_id)

    return Empty()


@router.get(
    "/categories/{category_id}",
    response_model=CategorySchema,
)
async def _get_category(category_id: int):
    category = await _get_category_or_404(category_id)
    return category
