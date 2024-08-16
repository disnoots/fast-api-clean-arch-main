from sqlalchemy import String, Boolean, ForeignKey, DateTime, Integer
from sqlalchemy.orm import MappedColumn, mapped_column, relationship, Relationship
from src.shared.entities.basemodel import BaseModel

from src.domains.auth.entities.user import User


class UserOauthToken(BaseModel):
    __tablename__ = "user_oauth_tokens"
    id: MappedColumn[str] = mapped_column(String, primary_key=True)
    user_id: MappedColumn[int] = mapped_column(Integer, ForeignKey(User.id))
    expires_at: MappedColumn[str] = mapped_column(DateTime)
    revoked: MappedColumn[bool] = mapped_column(Boolean)
    user = relationship(User, back_populates="tokens")
