import datetime
import http
from typing import Any, Coroutine
import uuid
import jwt
from fastapi import HTTPException, Depends
from starlette.requests import Request
from passlib.context import CryptContext
import datetime
from src.domains.book.book_interface import IBookRepository, IBookUseCase
from src.domains.book.book_repository import BookRepository
from src.domains.book.entities.books import Books
from src.models.requests.book_request import CreateBookRequest, IdBookRequest, KeywordBookRequest, UpdateBookRequest
from src.config.config import get_config

class BookUseCase(IBookUseCase):
    def __init__(self, book_repository: IBookRepository = Depends(BookRepository)):
        self.book_repository = book_repository

    async def create_book(self, request: Request, create_book_request: CreateBookRequest) -> Books:
        valid = await self.book_repository.validate_ISBN(create_book_request.ISBN)
        if valid is False:
            raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail="ISBN is invalid")

        book = Books(
            title = create_book_request.title,
            ISBN = create_book_request.ISBN,
            author = create_book_request.author,
            user_id = request.state.user.id
        )
        book.validate_create()
        
        return self.book_repository.create_book(request, book)
    
    async def update_book(self, request: Request, update_book_request: UpdateBookRequest) -> Books:
        count = self.book_repository.get_count_books_by_id(update_book_request.id)
        if count == 0:
            raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND, detail="Book not found")
        
        is_users = self.book_repository.get_count_user_of_book(request.state.user.id, update_book_request.id)
        if is_users == 0:
            raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail="Book is not owned by you")

        valid = await self.book_repository.validate_ISBN(update_book_request.ISBN)
        if valid is False:
            raise HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail="ISBN is invalid")

        book = Books(
            id = update_book_request.id,
            title = update_book_request.title,
            ISBN = update_book_request.ISBN,
            author = update_book_request.author
        )
        book.validate_update()

        return self.book_repository.update_book(request, book)
    
    def delete_book(self, request: Request, delete_book_request: IdBookRequest) -> Books:
        count = self.book_repository.get_count_books_by_id(delete_book_request.id)
        if count == 0:
            raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND, detail="Book not found")
        
        is_users = self.book_repository.get_count_user_of_book(request.state.user.id, delete_book_request.id)
        if is_users == 0:
            raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail="Book is not owned by you")

        return self.book_repository.delete_book(request, delete_book_request)
    
    def get_book(self, request: Request, get_book_request: IdBookRequest) -> Books:
        count = self.book_repository.get_count_books_by_id(get_book_request.id)
        if count == 0:
            raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND, detail="Book not found")
        
        is_users = self.book_repository.get_count_user_of_book(request.state.user.id, get_book_request.id)
        if is_users == 0:
            raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail="Book is not owned by you")

        return self.book_repository.get_book(request, get_book_request.id)
    
    def get_book_list(self, request: Request, keyword_book_request: KeywordBookRequest) -> list[Books]:
        if keyword_book_request.keyword is None:
            all_data = self.book_repository.get_book_list_user_id(request)
            return all_data

        data = self.book_repository.get_book_list_keyword(request, keyword_book_request.keyword)
        return data

        