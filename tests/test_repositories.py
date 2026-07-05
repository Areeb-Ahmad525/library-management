import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.base import Base
from src.exceptions import BookNotFoundError, DuplicateEmailError, LoanNotFoundError, MemberNotFoundError
from src.repositories.book_repository import BookRepository
from src.repositories.loan_repository import LoanRepository
from src.repositories.member_repository import MemberRepository


class RepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)
        self.session = self.session_factory()

    def tearDown(self) -> None:
        self.session.close()
        self.engine.dispose()

    def test_book_repository_crud(self) -> None:
        repository = BookRepository(self.session)

        book = repository.create_book("Dune", "Frank Herbert")
        self.assertEqual(book.title, "Dune")

        fetched = repository.get_book_by_id(book.id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.author, "Frank Herbert")

        updated = repository.update_book(book.id, title="Dune: Part Two")
        self.assertEqual(updated.title, "Dune: Part Two")

        self.assertTrue(repository.delete_book(book.id))
        self.assertIsNone(repository.get_book_by_id(book.id))

    def test_member_repository_duplicate_email(self) -> None:
        repository = MemberRepository(self.session)

        repository.create_member("Alice", "alice@example.com")

        with self.assertRaises(DuplicateEmailError):
            repository.create_member("Alice Clone", "alice@example.com")

    def test_loan_repository_issue_and_return(self) -> None:
        book_repository = BookRepository(self.session)
        member_repository = MemberRepository(self.session)
        loan_repository = LoanRepository(self.session)

        book = book_repository.create_book("1984", "George Orwell")
        member = member_repository.create_member("Bob", "bob@example.com")

        loan = loan_repository.issue_book(book.id, member.id)
        self.assertEqual(loan.book_id, book.id)
        self.assertEqual(loan.member_id, member.id)
        self.assertEqual(len(loan_repository.get_active_loans()), 1)

        returned_loan = loan_repository.return_book(loan.id)
        self.assertEqual(returned_loan.id, loan.id)
        self.assertEqual(len(loan_repository.get_active_loans()), 0)

        with self.assertRaises(LoanNotFoundError):
            loan_repository.return_book(loan.id)

    def test_loan_repository_validates_book_and_member(self) -> None:
        loan_repository = LoanRepository(self.session)
        book_repository = BookRepository(self.session)
        book_repository.create_book("1984", "George Orwell")

        with self.assertRaises(BookNotFoundError):
            loan_repository.issue_book(999, 1)

        with self.assertRaises(MemberNotFoundError):
            loan_repository.issue_book(1, 999)


if __name__ == "__main__":
    unittest.main()
