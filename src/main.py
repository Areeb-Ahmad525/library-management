import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.cli import CLI
from src.database.base import Base
from src.database.session import SessionLocal, engine
from src.repositories.book_repository import BookRepository
from src.repositories.loan_repository import LoanRepository
from src.repositories.member_repository import MemberRepository
from src.services.book_service import BookService
from src.services.loan_service import LoanService
from src.services.member_service import MemberService

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")


def main() -> None:
    """Create dependencies and start the interactive CLI."""
    Base.metadata.create_all(engine)

    db = SessionLocal()
    try:
        book_repository = BookRepository(db)
        member_repository = MemberRepository(db)
        loan_repository = LoanRepository(db)

        book_service = BookService(book_repository)
        member_service = MemberService(member_repository)
        loan_service = LoanService(loan_repository, book_repository, member_repository)

        cli = CLI(book_service, member_service, loan_service)
        cli.run()
    finally:
        db.close()


if __name__ == "__main__":
    main()