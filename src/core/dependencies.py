from fastapi import Query, Depends
from pydantic import BaseModel
from typing import Annotated


class Pagination(BaseModel):
    page: Annotated[int | None, Query(None, gt=1)]
    per_page: Annotated[int | None, Query(None, gt=1, lt=20)]


PgnDepds = Annotated[Pagination, Depends()]