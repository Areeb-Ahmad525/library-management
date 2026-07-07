from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models import Book
from src.utils.exceptions import BookNotFoundError


class BookRepository:
    """Repository for managing book records."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_book(self, title: str, author: str) -> Book:
        """
        Create and persist a new book.

        Args:
            title (str): The title of the book.
            author (str): The author of the book.

        Returns:
            Book: The newly created Book instance.
        """
        book = Book(title=title, author=author)
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """
        Return a book by id, or None if it does not exist.

        Args:
            book_id (int): The unique identifier of the book.

        Returns:
            Optional[Book]: The Book instance if found, otherwise None.
        """
        return self.db.get(Book, book_id)

    def get_all_books(self) -> List[Book]:
        """
        Return all books ordered by id.

        Returns:
            List[Book]: A list of all Book instances in the database.
        """
        return list(self.db.scalars(select(Book).order_by(Book.id)).all())

    def search_books(
        self, title: Optional[str] = None, author: Optional[str] = None
    ) -> List[Book]:
        """
        Search books by title and/or author using case-insensitive matching.

        Args:
            title (Optional[str]): A substring to search for in the book's title.
            author (Optional[str]): A substring to search for in the book's author.

        Returns:
            List[Book]: A list of Book instances matching the search criteria.
        """
        query = select(Book)
        if title is not None:
            query = query.where(Book.title.ilike(f"%{title}%"))
        if author is not None:
            query = query.where(Book.author.ilike(f"%{author}%"))
        query = query.order_by(Book.id)
        return list(self.db.scalars(query).all())

    def update_book(
        self,
        book_id: int,
        title: Optional[str] = None,
        author: Optional[str] = None,
    ) -> Book:
        """
        Update an existing book with any provided field values.

        Args:
            book_id (int): The unique identifier of the book to update.
            title (Optional[str]): The new title, if provided.
            author (Optional[str]): The new author, if provided.

        Returns:
            Book: The updated Book instance.

        Raises:
            BookNotFoundError: If no book exists with the given id.
        """
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
        """
        Delete a book and return True if the deletion succeeded.

        Args:
            book_id (int): The unique identifier of the book to delete.

        Returns:
            bool: True upon successful deletion.

        Raises:
            BookNotFoundError: If no book exists with the given id.
        """
        book = self.get_book_by_id(book_id)
        if book is None:
            raise BookNotFoundError(f"Book with id {book_id} was not found.")

        self.db.delete(book)
        self.db.commit()
        return True
