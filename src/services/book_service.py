import logging
from typing import List, Optional

from src.database.models import Book
from src.repositories.book_repository import BookRepository
from src.utils.exceptions import BookNotFoundError, ValidationError
from src.utils.validators import normalize_optional_text, normalize_required_text

logger = logging.getLogger(__name__)


class BookService:
    """Apply business rules for book operations."""

    def __init__(self, book_repository: BookRepository) -> None:
        self.book_repository = book_repository

    def add_book(self, title: str, author: str) -> Book:
        """Create a new book after validating the provided values."""
        normalized_title = self._normalize_required_field(title, "title")
        normalized_author = self._normalize_required_field(author, "author")

        book = self.book_repository.create_book(normalized_title, normalized_author)
        logger.info("Book created: %s", book.title)
        return book

    def get_book(self, book_id: int) -> Optional[Book]:
        """Return a book by id, or None if it is missing."""
        book = self.book_repository.get_book_by_id(book_id)
        if book is None:
            raise BookNotFoundError(f"Book with id {book_id} was not found.")
        return book

    def list_books(self) -> List[Book]:
        """Return all books in the repository."""
        return self.book_repository.get_all_books()

    def update_book(
        self,
        book_id: int,
        title: Optional[str] = None,
        author: Optional[str] = None,
    ) -> Book:
        """Update a book after validating any provided values."""
        self.get_book(book_id)

        normalized_title = self._normalize_optional_field(title, "title")
        normalized_author = self._normalize_optional_field(author, "author")

        book = self.book_repository.update_book(
            book_id,
            title=normalized_title,
            author=normalized_author,
        )
        return book

    def remove_book(self, book_id: int) -> bool:
        """Remove a book after ensuring it exists."""
        self.get_book(book_id)
        self.book_repository.delete_book(book_id)
        logger.info("Book removed: %s", book_id)
        return True

    def _normalize_required_field(self, value: str, field_name: str) -> str:
        try:
            return normalize_required_text(value, field_name)
        except ValueError as exc:
            logger.warning("Validation failure: %s is empty", field_name)
            raise ValidationError(str(exc)) from exc

    def _normalize_optional_field(self, value: Optional[str], field_name: str) -> Optional[str]:
        try:
            return normalize_optional_text(value, field_name)
        except ValueError as exc:
            logger.warning("Validation failure: %s is empty", field_name)
            raise ValidationError(str(exc)) from exc
