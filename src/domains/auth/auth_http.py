import http

from fastapi import APIRouter, Request, Depends

from src.dependencies.auth_dependency import bearer_auth
from src.domains.auth.auth_interface import IAuthUseCase
from src.domains.auth.auth_usecase import AuthUseCase
from src.models.requests.auth_request import LoginRequest, RegisterRequest
from src.models.responses.auth_response import LoginResponse
from src.models.responses.basic_response import BasicResponse, IdResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(request: Request, register_request: RegisterRequest, auth_uc: IAuthUseCase = Depends(AuthUseCase)) -> BasicResponse[IdResponse]:
    data = auth_uc.register(request, register_request)
    return BasicResponse(
        data=IdResponse(id=data.id),
        message="success registering user",
        status_code=http.HTTPStatus.OK
    )


@router.post("/login")
def login(
        request: Request,
        login_request: LoginRequest,
        auth_uc: IAuthUseCase = Depends(AuthUseCase)
) -> BasicResponse[LoginResponse]:
    token = auth_uc.login(request, login_request)
    return BasicResponse(
        data=LoginResponse(
            token=token,
        ),
        message="success logging in",
        status_code=http.HTTPStatus.OK
    )


@router.get("/user", dependencies=[Depends(bearer_auth)])
def get_current_user(request: Request) -> BasicResponse[IdResponse]:
    return BasicResponse(
        data=request.state.user.name,
        message="success getting user",
        status_code=http.HTTPStatus.OK
    )