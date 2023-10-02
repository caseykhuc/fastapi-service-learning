from typing import Annotated

import annotated_types
from pydantic import BaseModel, ConfigDict, PositiveInt, StrictStr


class BaseResponseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )


class BaseValidationSchema(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        frozen=True,
        str_strip_whitespace=True,
    )


NonEmptyStr = Annotated[StrictStr, annotated_types.MinLen(1)]
ShortStr = Annotated[NonEmptyStr, annotated_types.MaxLen(255)]
LongStr = Annotated[NonEmptyStr, annotated_types.MaxLen(5000)]


class Empty(BaseModel):
    model_config = ConfigDict(extra="forbid")


class PaginationSchema(BaseModel):
    total: int
    page: PositiveInt
    number_per_page: PositiveInt
