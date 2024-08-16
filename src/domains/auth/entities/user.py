from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, MappedColumn, relationship

from src.shared.entities.basemodel import BaseModel
from src.validators.validator import Validator

class User(BaseModel):
    __tablename__ = "users"
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: MappedColumn[str] = mapped_column(String)
    email: MappedColumn[str] = mapped_column(String, unique=True)
    password: MappedColumn[str] = mapped_column(String)
    tokens = relationship("UserOauthToken", back_populates="user")

    def validate_create(self) -> None:
        validator = Validator(self)
        validator.unique_db("email", User, "email", None)
