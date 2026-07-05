from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models import Book
from src.exceptions import BookNotFoundError


class BookRepository:
    """Repository for managing book records."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_book(self, title: str, author: str) -> Book:
        """Create and persist a new book."""
        book = Book(title=title, author=author)
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """Return a book by id, or None if it does not exist."""
        return self.db.get(Book, book_id)

    def get_all_books(self) -> List[Book]:
        """Return all books ordered by id."""
        return list(self.db.scalars(select(Book).order_by(Book.id)).all())

    def update_book(
        self,
        book_id: int,
        title: Optional[str] = None,
        author: Optional[str] = None,
    ) -> Book:
        """Update an existing book with any provided field values."""
        book = self.get_book_by_id(book_id)
        if book is None:
            raise BookNotFoundError(f"Book with id {book_id} was not found.")

        if title is not None:
            book.title = title
        if author is not None:
            book.author = author

        self.db.commit()
        self.db.refresh(book)
        return book

    def delete_book(self, book_id: int) -> bool:
        """Delete a book and return True if the deletion succeeded."""
        book = self.get_book_by_id(book_id)
        if book is None:
            raise BookNotFoundError(f"Book with id {book_id} was not found.")

        self.db.delete(book)
        self.db.commit()
        return True
