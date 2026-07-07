from fastapi import Depends, FastAPI, Query
from sqlalchemy.orm import Session

from src.database.session import SessionLocal
from src.repositories.book_repository import BookRepository
from src.services.book_service import BookService


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Library Management API",
        version="1.0.0",
        docs_url="/docs",
        openapi_url="/openapi.json",
    )

    @app.get("/health", tags=["Health"])
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/books", response_model=list[dict[str, object]], tags=["Books"])
    def list_books(db: Session = Depends(get_db)) -> list[dict[str, object]]:
        book_repository = BookRepository(db)
        book_service = BookService(book_repository)
        books = book_service.list_books()
        return [{"id": book.id, "title": book.title, "author": book.author} for book in books]

    @app.get("/books/search", response_model=list[dict[str, object]], tags=["Books"])
    def search_books(
        title: str | None = Query(default=None),
        author: str | None = Query(default=None),
        db: Session = Depends(get_db),
    ) -> list[dict[str, object]]:
        book_repository = BookRepository(db)
        book_service = BookService(book_repository)
        books = book_service.search_books(title=title, author=author)
        return [{"id": book.id, "title": book.title, "author": book.author} for book in books]

    return app


app = create_app()
