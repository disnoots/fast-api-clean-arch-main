import http

import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.requests import Request

from src.config.config import get_config
from src.domains.auth.auth_interface import IAuthRepository
from src.domains.auth.auth_repository import AuthRepository

http_bearer = HTTPBearer()


def bearer_auth(request: Request, auth: HTTPAuthorizationCredentials = Security(http_bearer),
                auth_repo: IAuthRepository = Depends(AuthRepository)) -> None:
    payload = jwt.decode(auth.credentials, get_config().app.jwt_key, algorithms=["HS256"])

    user = auth_repo.find_user_by_oauth_token_id(request, payload["id"])
    if user is None:
        raise HTTPException(status_code=http.HTTPStatus.UNAUTHORIZED, detail="Unauthorized")
    request.state.user = user
