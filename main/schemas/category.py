from .base import BaseResponseSchema, BaseValidationSchema, ShortStr


class CategoryCreatePayloadSchema(BaseValidationSchema):
    name: ShortStr


class CategorySchema(BaseResponseSchema):
    id: int
    name: ShortStr
