import datetime
import http
import uuid
import jwt
from fastapi import HTTPException, Depends
from starlette.requests import Request
from passlib.context import CryptContext
import datetime
from src.config.config import get_config
from src.domains.auth.auth_repository import AuthRepository
from src.domains.auth.entities.user import User
from src.domains.auth.entities.user_oauth_token import UserOauthToken
from src.domains.auth.auth_interface import IAuthUseCase, IAuthRepository
from src.models.requests.auth_request import LoginRequest, RegisterRequest


class AuthUseCase(IAuthUseCase):
    def __init__(self, auth_repository: IAuthRepository = Depends(AuthRepository)):
        self.auth_repository = auth_repository

    def login(self, request: Request, login_request: LoginRequest) -> str:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        user = self.auth_repository.find_user(request, email=login_request.email)
        if user is None:
            raise HTTPException(status_code=http.HTTPStatus.UNAUTHORIZED, detail="Unauthorized")
        if not pwd_context.verify(login_request.password, user.password):
            raise HTTPException(status_code=http.HTTPStatus.UNAUTHORIZED, detail="Unauthorized")

        expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=8)

        token = self.auth_repository.generate_oauth_token(request, UserOauthToken(
            id=str(uuid.uuid1()),
            user_id=user.id,
            expires_at=expiration,
            revoked=0,
        ))

        payload = {
            "id": token.id,
            "exp": expiration
        }

        return str(jwt.encode(payload, get_config().app.jwt_key, algorithm="HS256"))

    def register(self, request: Request, register_request: RegisterRequest) -> User:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        user = User(
            name=register_request.name,
            email=register_request.email,
            password=pwd_context.hash(register_request.password)
        )
        user.validate_create()
        return self.auth_repository.create_user(request, user)