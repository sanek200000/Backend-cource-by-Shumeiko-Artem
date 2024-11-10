from typing import Annotated
from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(None, gt=0)]
    per_page: Annotated[int | None, Query(None, gt=0, lt=20)]


PaginationDep = Annotated[PaginationParams, Depends()]
