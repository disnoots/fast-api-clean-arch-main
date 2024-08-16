from typing import TypeVar, Generic

from pydantic import BaseModel

class BookResponse(BaseModel):
    id: int
    title: str
    ISBN: str
    author: str
    user_id: int