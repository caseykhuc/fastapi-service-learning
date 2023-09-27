from typing import Annotated

from fastapi import Depends

from main.commons.exceptions import (
    ErrorCode,
    ErrorMessage,
    Forbidden,
    NotFound,
)
from main.engines.categories import (
    get_category_by_id,
)
from main.models.category import CategoryModel
from main.utils.auth import require_authentication


async def get_category_or_404(id: int) -> CategoryModel:
    category = await get_category_by_id(id)

    if not category:
        raise NotFound()

    return category


async def require_category_creator(
    category_id: int,
    id: Annotated[int, Depends(require_authentication)],
):
    category = await get_category_or_404(category_id)

    if category.creator_id != id:
        raise Forbidden(
            error_message=ErrorMessage.NOT_CREATOR,
            error_code=ErrorCode.NOT_CREATOR,
        )
