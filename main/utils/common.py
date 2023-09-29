from typing import Annotated

from fastapi import Path

PositiveIntPath = Annotated[int, Path(ge=1)]
