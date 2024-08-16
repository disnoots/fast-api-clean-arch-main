from typing import TypeVar, Generic

from pydantic import BaseModel

T = TypeVar('T')


class IdResponse(BaseModel):
    id: str | int


class BasicResponse(Generic[T], BaseModel):
    data: T
    message: str | None
    status_code: int
