from typing import Annotated

from fastapi import Path, Query

PositiveIntPath = Annotated[int, Path(ge=1)]
PositiveIntQuery = Annotated[int, Query(ge=1)]
