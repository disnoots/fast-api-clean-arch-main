from datetime import datetime
from typing import Optional

from fastapi import Request, Depends
import httpx
from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.domains.book.book_interface import IBookRepository
from src.domains.book.entities.books import Books
from src.dependencies.database_dependency import get_sample_db

class BookRepository(IBookRepository):
    def __init__(self, db: Session = Depends(get_sample_db)):
        self.db = db

    def create_book(self, request: Request, books: Books) -> Books:
        self.db.add(books)
        self.db.commit()
        self.db.refresh(books)
        return books
    
    async def validate_ISBN(self, ISBN: str) -> bool:
        url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{ISBN}&jscmd=details&format=json"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    return True
            
            return False
        
    def get_count_books_by_id(self, id: int) -> int:
        return self.db.query(Books).filter(Books.id == id).count()
    
    def get_count_user_of_book(self, id: int, book_id: int) -> int:
        return self.db.query(Books).filter(Books.user_id == id, Books.id == book_id).count()
    
    def update_book(self, request: Request, book: Books) -> Books:
        book_db = self.db.query(Books).filter(Books.id == book.id).first()
        book_db.title = book.title
        book_db.ISBN = book.ISBN
        book_db.author = book.author
        self.db.commit()
        self.db.refresh(book_db)
        return book_db
    
    def delete_book(self, request: Request, id: int) -> Books:
        book_db = self.db.query(Books).filter(Books.id == id).first()
        self.db.delete(book_db)
        self.db.commit()
        return book_db
    
    def get_book(self, request: Request, id: int) -> Books:
        return self.db.query(Books).filter(Books.id == id).first()
    
    def get_book_list_user_id(self, request: Request) -> list[Books]:
        return self.db.query(Books).filter(Books.user_id == request.state.user.id).all()
    
    def get_book_list_keyword(self, request: Request, keyword: str) -> list[Books]:
        data = self.db.query(Books).filter(
        Books.user_id == request.state.user.id,
        or_(
            Books.title.contains(keyword),
            Books.ISBN.contains(keyword),
            Books.author.contains(keyword)
        )
        ).all()
        return data