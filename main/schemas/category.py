from .base import BaseResponseSchema, BaseValidationSchema, LongStr, ShortStr


class CategoryCreatePayloadSchema(BaseValidationSchema):
    name: ShortStr
    description: LongStr


class CategorySchema(BaseResponseSchema):
    id: int
    name: ShortStr
    description: LongStr
    is_creator: bool
