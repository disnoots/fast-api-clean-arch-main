import abc

from fastapi import Request

from src.domains.auth.entities.user import User
from src.domains.auth.entities.user_oauth_token import UserOauthToken
from src.models.requests.auth_request import LoginRequest, RegisterRequest


class IAuthUseCase(abc.ABC):
    @abc.abstractmethod
    def login(self, request: Request, login_request: LoginRequest) -> str:
        pass

    @abc.abstractmethod
    def register(self, request: Request, login_request: RegisterRequest) -> User:
        pass


class IAuthRepository(abc.ABC):
    @abc.abstractmethod
    def create_user(self, request: Request, user: User) -> User:
        pass

    @abc.abstractmethod
    def generate_oauth_token(
        self, request: Request, token: UserOauthToken
    ) -> UserOauthToken:
        pass

    @abc.abstractmethod
    def find_user(
        self, request: Request, user_id: str | None = None, email: str | None = None
    ) -> User | None:
        pass

    @abc.abstractmethod
    def find_user_by_oauth_token_id(
        self, request: Request, token_id: str
    ) -> User | None:
        pass
