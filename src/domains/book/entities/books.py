from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import mapped_column, MappedColumn, relationship

from src.shared.entities.basemodel import BaseModel
from src.validators.validator import Validator

class Books(BaseModel):
    __tablename__ = "books"
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: MappedColumn[str] = mapped_column(String)
    ISBN: MappedColumn[str] = mapped_column(String, unique=True)
    author: MappedColumn[str] = mapped_column(String)
    user_id: MappedColumn[int] = mapped_column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="user")

    def validate_create(self) -> None:
        validator = Validator(self)
        validator.unique_db("ISBN", Books, "ISBN", None)

    def validate_update(self) -> None:
        validator = Validator(self)
        validator.unique_db("ISBN", Books, "ISBN", "id")
