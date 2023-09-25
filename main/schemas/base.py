from typing import Annotated

import annotated_types
from pydantic import BaseModel, ConfigDict, StrictStr


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
