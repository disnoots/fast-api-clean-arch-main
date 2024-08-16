from datetime import datetime
from typing import Optional

from fastapi import Request, Depends
from sqlalchemy.orm import Session

from src.dependencies.database_dependency import get_sample_db
from src.domains.auth.entities.user import User
from src.domains.auth.entities.user_oauth_token import UserOauthToken
from src.domains.auth.auth_interface import IAuthRepository


class AuthRepository(IAuthRepository):
    def find_user(
            self, request: Request, user_id: str | None = None, email: str | None = None
    ) -> User | None:
        pass
        query = self.db.query(User)
        if user_id is not None:
            query = query.filter(User.id == user_id)
        if email is not None:
            query = query.filter(User.email == email)

        return query.first()

    def __init__(self, db: Session = Depends(get_sample_db)):
        self.db = db

    def create_user(self, request: Request, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def generate_oauth_token(
            self, request: Request, token: UserOauthToken
    ) -> UserOauthToken:
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token

    def find_user_by_oauth_token_id(
            self, request: Request, token_id: str
    ) -> User | None:
        token = (
            self.db.query(UserOauthToken)
            .filter(UserOauthToken.revoked == False)
            .filter(UserOauthToken.expires_at > datetime.now())
            .filter(UserOauthToken.id.like(token_id))
            .first()
        )
        if token is None:
            return None
        return token.user  # type: ignore
