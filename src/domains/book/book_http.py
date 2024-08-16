import http

from fastapi import APIRouter, Request, Depends

from src.models.responses.book_response import BookResponse
from src.domains.book.book_interface import IBookUseCase
from src.domains.book.book_usecase import BookUseCase
from src.models.requests.book_request import CreateBookRequest, IdBookRequest, KeywordBookRequest, UpdateBookRequest
from src.models.responses.basic_response import BasicResponse, IdResponse
from src.dependencies.auth_dependency import bearer_auth

router = APIRouter(prefix="/book", tags=["Book"])

@router.post("/create", dependencies=[Depends(bearer_auth)])
async def create_book(request: Request, create_book_request: CreateBookRequest, book_uc: IBookUseCase = Depends(BookUseCase)) -> BasicResponse[IdResponse]:
    data = await book_uc.create_book(request, create_book_request)
    return BasicResponse(
        data=IdResponse(id=data.id),
        message="success inserting book",
        status_code=http.HTTPStatus.OK
    )

@router.post("/update", dependencies=[Depends(bearer_auth)])
async def update_book(request: Request, update_book_request: UpdateBookRequest, book_uc: IBookUseCase = Depends(BookUseCase)) -> BasicResponse[IdResponse]:
    data = await book_uc.update_book(request, update_book_request)
    return BasicResponse(
        data=IdResponse(id=data.id),
        message="success updating book",
        status_code=http.HTTPStatus.OK
    )

@router.post("/delete", dependencies=[Depends(bearer_auth)])
def delete_book(request: Request, delete_book_request: IdBookRequest, book_uc: IBookUseCase = Depends(BookUseCase)) -> BasicResponse[IdResponse]:
    data = book_uc.delete_book(request, delete_book_request)
    return BasicResponse(
        data=IdResponse(id=data.id),
        message="success deleting book",
        status_code=http.HTTPStatus.OK
    )

@router.post("/get", dependencies=[Depends(bearer_auth)])
def get_book_detail(request: Request, get_book_request: IdBookRequest, book_uc: IBookUseCase = Depends(BookUseCase)) -> BasicResponse[BookResponse]:
    data = book_uc.get_book(request, get_book_request)
    return BasicResponse(
        data=BookResponse(
            id=data.id,
            title=data.title,
            ISBN=data.ISBN,
            author=data.author,
            user_id=data.user_id
        ),
        message="success getting book",
        status_code=http.HTTPStatus.OK
    )

@router.post("/list", dependencies=[Depends(bearer_auth)])
def get_book_list(request: Request, keyword_book_request: KeywordBookRequest, book_uc: IBookUseCase = Depends(BookUseCase)) -> BasicResponse[list[BookResponse]]:
    data = book_uc.get_book_list(request, keyword_book_request)
    return BasicResponse(
        data=[BookResponse(
            id=d.id,
            title=d.title,
            ISBN=d.ISBN,
            author=d.author,
            user_id=d.user_id
        ) for d in data],
        message="success getting book list",
        status_code=http.HTTPStatus.OK
    )
    