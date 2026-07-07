import unittest


from src.database.base import Base
from src.utils.exceptions import (
    BookAlreadyIssuedError,
    BookNotFoundError,
    DuplicateEmailError,
    LoanNotFoundError,
    MemberNotFoundError,
    ValidationError,
)
from src.repositories.book_repository import BookRepository
from src.repositories.loan_repository import LoanRepository
from src.repositories.member_repository import MemberRepository
from src.services.book_service import BookService
from src.services.loan_service import LoanService
from src.services.member_service import MemberService


class ServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        from src.database.session import engine
        from sqlalchemy.orm import Session

        self.connection = engine.connect()
        self.transaction = self.connection.begin()
        self.session = Session(bind=self.connection, join_transaction_mode="create_savepoint")
        Base.metadata.create_all(self.connection)

        self.book_repository = BookRepository(self.session)
        self.member_repository = MemberRepository(self.session)
        self.loan_repository = LoanRepository(self.session)

        self.book_service = BookService(self.book_repository)
        self.member_service = MemberService(self.member_repository)
        self.loan_service = LoanService(
            self.loan_repository,
            self.book_repository,
            self.member_repository,
        )

    def tearDown(self) -> None:
        self.session.close()
        self.transaction.rollback()
        self.connection.close()

    def test_book_service_validates_inputs(self) -> None:
        """Verify that the book service rejects empty titles or authors with a ValidationError."""
        with self.assertRaises(ValidationError):
            self.book_service.add_book("   ", "  ")

    def test_member_service_rejects_duplicate_email(self) -> None:
        """Verify that the member service enforces unique email addresses."""
        self.member_service.register_member("Alice", "alice@example.com")

        with self.assertRaises(DuplicateEmailError):
            self.member_service.register_member("Alicia", "alice@example.com")

    def test_loan_service_prevents_duplicate_active_loans(self) -> None:
        """Verify that a book cannot be issued to multiple members simultaneously."""
        book = self.book_service.add_book("Dune", "Frank Herbert")
        member = self.member_service.register_member("Bob", "bob@example.com")

        self.loan_service.issue_book(book.id, member.id)

        with self.assertRaises(BookAlreadyIssuedError):
            self.loan_service.issue_book(book.id, member.id)

    def test_loan_service_returns_book_and_raises_when_missing(self) -> None:
        """Verify that returning a book succeeds, and returning it again raises a LoanNotFoundError."""
        book = self.book_service.add_book("1984", "George Orwell")
        member = self.member_service.register_member("Carol", "carol@example.com")

        loan = self.loan_service.issue_book(book.id, member.id)
        self.loan_service.return_book(loan.id)

        with self.assertRaises(LoanNotFoundError):
            self.loan_service.return_book(loan.id)

    def test_services_raise_domain_errors_for_missing_entities(self) -> None:
        """Verify that issuing loans for non-existent books or members raises domain-specific exceptions."""
        with self.assertRaises(BookNotFoundError):
            self.loan_service.issue_book(999, 1)

        book = self.book_service.add_book("1984", "George Orwell")

        with self.assertRaises(MemberNotFoundError):
            self.loan_service.issue_book(book.id, 999)


if __name__ == "__main__":
    unittest.main()
