import http

from fastapi import APIRouter, Request, Depends
from src.domains.sharepoint.sharepoint_interface import ISharepointUseCase
from src.domains.sharepoint.sharepoint_usecase import SharepointUseCase
from src.models.requests.sharepoint_action_1_request import Action1Request, DownloadRequest
from src.models.responses.basic_response import BasicResponse

router = APIRouter(prefix="/sharepoint", tags=["Sharepoint"])

@router.post("/download_files")
async def download_files(request: Request, sharepoint_uc: ISharepointUseCase = Depends(SharepointUseCase)) -> BasicResponse:
    data = sharepoint_uc.download_files(request)
    return BasicResponse(
        data=data,
        message="success",
        status_code=http.HTTPStatus.OK
    )

@router.post("/read_action_1")
async def action_1(request: Request, sharepoint_uc: ISharepointUseCase = Depends(SharepointUseCase)) -> BasicResponse:
    data = sharepoint_uc.action_1(request)
    return BasicResponse(
        data=data,
        message="success",
        status_code=http.HTTPStatus.OK
    )

@router.post("/read_action_2")
async def action_2(request: Request, sharepoint_uc: ISharepointUseCase = Depends(SharepointUseCase)) -> BasicResponse:
    data = sharepoint_uc.action_2(request)
    return BasicResponse(
        data=data,
        message="success",
        status_code=http.HTTPStatus.OK
    )
