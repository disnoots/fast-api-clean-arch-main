import re
from typing import Any, Optional

from pydantic import BaseModel, EmailStr, validator, Field, field_validator
from pydantic_core.core_schema import ValidationInfo

class Action1Request(BaseModel):
    link_1: str = Field(...)
    link_2: str = Field(...)

class DownloadRequest(BaseModel):
    # root_folder: str = Field(...)
    download_path: str = Field(...)