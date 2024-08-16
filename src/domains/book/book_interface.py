import abc

from fastapi import Request

from src.domains.book.entities.books import Books
from src.models.requests.book_request import CreateBookRequest, IdBookRequest, KeywordBookRequest, UpdateBookRequest

class IBookUseCase(abc.ABC):
    @abc.abstractmethod
    async def create_book(self, request: Request, create_book_request: CreateBookRequest) -> Books:
        pass

    @abc.abstractmethod
    async def update_book(self, request: Request, update_book_request: UpdateBookRequest) -> Books:
        pass

    @abc.abstractmethod
    def delete_book(self, request: Request, delete_book_request: IdBookRequest) -> Books:
        pass

    @abc.abstractmethod
    def get_book(self, request: Request, get_book_request: IdBookRequest) -> Books:
        pass

    @abc.abstractmethod
    def get_book_list(self, request: Request, keyword_book_request: KeywordBookRequest) -> list[Books]:
        pass

class IBookRepository(abc.ABC):
    @abc.abstractmethod
    def create_book(self, request: Request, books: Books) -> Books:
        pass

    @abc.abstractmethod
    async def validate_ISBN(self, ISBN: str) -> bool:
        pass

    @abc.abstractmethod
    def get_count_books_by_id(self, id: int) -> int:
        pass

    @abc.abstractmethod
    def get_count_user_of_book(self, id: int, book_id: int) -> int:
        pass

    @abc.abstractmethod
    def update_book(self, request: Request, book: Books) -> Books:
        pass

    @abc.abstractmethod
    def delete_book(self, request: Request, book: Books) -> Books:
        pass

    @abc.abstractmethod
    def get_book(self, request: Request, id: int) -> Books:
        pass

    @abc.abstractmethod
    def get_book_list_user_id(self, request: Request) -> list[Books]:
        pass

    @abc.abstractmethod
    def get_book_list_keyword(self, request: Request, keyword: str) -> list[Books]:
        pass