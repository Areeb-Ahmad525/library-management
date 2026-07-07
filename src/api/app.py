from fastapi import Depends, FastAPI, Query
from sqlalchemy.orm import Session

from src.database.session import SessionLocal
from src.repositories.book_repository import BookRepository
from src.services.book_service import BookService


def get_db() -> Session:
    """
    Dependency generator that provides a database session for a request.

    Yields:
        Session: The SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_app() -> FastAPI:
    """
    Factory function to create and configure the FastAPI application.

    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    app = FastAPI(
        title="Library Management API",
        version="1.0.0",
        docs_url="/docs",
        openapi_url="/openapi.json",
    )

    @app.get("/health", tags=["Health"])
    def health_check() -> dict[str, str]:
        """
        Health check endpoint to verify the API is running.

        Returns:
            dict[str, str]: A simple status dictionary.
        """
        return {"status": "ok"}

    @app.get("/books", response_model=list[dict[str, object]], tags=["Books"])
    def list_books(db: Session = Depends(get_db)) -> list[dict[str, object]]:
        """
        Retrieve all books from the library.

        Args:
            db (Session): The database session dependency.

        Returns:
            list[dict[str, object]]: A list of book dictionaries.
        """
        book_repository = BookRepository(db)
        book_service = BookService(book_repository)
        books = book_service.list_books()
        return [
            {"id": book.id, "title": book.title, "author": book.author}
            for book in books
        ]

    @app.get("/books/search", response_model=list[dict[str, object]], tags=["Books"])
    def search_books(
        title: str | None = Query(default=None),
        author: str | None = Query(default=None),
        db: Session = Depends(get_db),
    ) -> list[dict[str, object]]:
        """
        Search for books by title and/or author.

        Args:
            title (str | None): Optional title substring to search for.
            author (str | None): Optional author substring to search for.
            db (Session): The database session dependency.

        Returns:
            list[dict[str, object]]: A list of matching book dictionaries.
        """
        book_repository = BookRepository(db)
        book_service = BookService(book_repository)
        books = book_service.search_books(title=title, author=author)
        return [
            {"id": book.id, "title": book.title, "author": book.author}
            for book in books
        ]

    return app


app = create_app()
