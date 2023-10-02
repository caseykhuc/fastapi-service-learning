from pydantic import model_validator

from .base import (
    BaseResponseSchema,
    BaseValidationSchema,
    LongStr,
    PaginationSchema,
    ShortStr,
)


class ItemCreatePayloadSchema(BaseValidationSchema):
    name: ShortStr
    description: LongStr


class ItemUpdatePayloadSchema(BaseValidationSchema):
    name: ShortStr | None = None
    description: LongStr | None = None

    @model_validator(mode="after")
    def check_not_empty(self) -> "ItemUpdatePayloadSchema":
        if self.name is None and self.description is None:
            raise ValueError("There is no data to update.")
        return self


class PlainItemSchema(BaseResponseSchema):
    id: int
    name: ShortStr
    description: LongStr


class ItemSchema(PlainItemSchema):
    category_id: int


class CategoryItemsSchema(BaseResponseSchema, PaginationSchema):
    items: list[PlainItemSchema]
