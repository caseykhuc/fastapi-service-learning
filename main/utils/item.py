from typing import Annotated

from fastapi import Depends

from main.commons.exceptions import (
    BadRequest,
    ErrorCode,
    ErrorMessage,
    Forbidden,
    NotFound,
)
from main.engines.items import (
    get_item_by_id,
    get_item_by_name,
)
from main.models.item import ItemModel
from main.utils.auth import require_authentication

from .common import PositiveIntPath


async def get_item_or_404(id: PositiveIntPath) -> ItemModel:
    item = await get_item_by_id(id)

    if not item:
        raise NotFound()

    return item


async def require_item_creator(
    item_id: PositiveIntPath,
    user_id: Annotated[int, Depends(require_authentication)],
):
    item = await get_item_or_404(item_id)

    if item.creator_id != user_id:
        raise Forbidden(
            error_message=ErrorMessage.NOT_CREATOR,
            error_code=ErrorCode.NOT_CREATOR,
        )


async def validate_item_name(name: str):
    item = await get_item_by_name(name)

    if item:
        raise BadRequest(
            error_message=ErrorMessage.ITEM_NAME_EXISTS,
            error_code=ErrorCode.ITEM_NAME_EXISTS,
        )
