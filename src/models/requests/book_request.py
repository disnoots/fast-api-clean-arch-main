import re
from typing import Any, Optional

from pydantic import BaseModel, EmailStr, validator, Field, field_validator
from pydantic_core.core_schema import ValidationInfo

class CreateBookRequest(BaseModel):
    title: str = Field(...)
    ISBN: str = Field(...)
    author: str = Field(...)

# class UpdateBookRequest(BaseModel):
#     id: int = Field(...)
#     title: Optional[str] = Field(None)
#     ISBN: Optional[str] = Field(None)
#     author: Optional[str] = Field(None)

class UpdateBookRequest(BaseModel):
    id: int = Field(...)
    title: str = Field(...)
    ISBN: str = Field(...)
    author: str = Field(...)

class IdBookRequest(BaseModel):
    id: int = Field(...)

class KeywordBookRequest(BaseModel):
    keyword: Optional[str] = Field(None)