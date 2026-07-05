import logging
from typing import List

from src.database.models import Loan
from src.exceptions import (
    BookAlreadyIssuedError,
    BookNotFoundError,
    LoanNotFoundError,
    MemberNotFoundError,
)
from src.repositories.book_repository import BookRepository
from src.repositories.loan_repository import LoanRepository
from src.repositories.member_repository import MemberRepository

logger = logging.getLogger(__name__)


class LoanService:
    """Apply business rules for loan operations."""

    def __init__(
        self,
        loan_repository: LoanRepository,
        book_repository: BookRepository,
        member_repository: MemberRepository,
    ) -> None:
        self.loan_repository = loan_repository
        self.book_repository = book_repository
        self.member_repository = member_repository

    def issue_book(self, book_id: int, member_id: int) -> Loan:
        """Issue a loan for a book to a member if the business rules allow it."""
        self._ensure_book_exists(book_id)
        self._ensure_member_exists(member_id)
        self._ensure_book_is_available(book_id)

        loan = self.loan_repository.issue_book(book_id, member_id)
        logger.info("Loan issued: book_id=%s member_id=%s", book_id, member_id)
        return loan

    def return_book(self, loan_id: int) -> Loan:
        """Return an active loan and mark it as completed."""
        loan = self.loan_repository.get_active_loans()
        active_loan_ids = {existing_loan.id for existing_loan in loan}
        if loan_id not in active_loan_ids:
            raise LoanNotFoundError(f"Loan with id {loan_id} was not found.")

        returned_loan = self.loan_repository.return_book(loan_id)
        logger.info("Loan returned: loan_id=%s", loan_id)
        return returned_loan

    def get_active_loans(self) -> List[Loan]:
        """Return all active loans."""
        return self.loan_repository.get_active_loans()

    def get_member_loans(self, member_id: int) -> List[Loan]:
        """Return all loans for a specific member."""
        self._ensure_member_exists(member_id)
        return self.loan_repository.get_member_loans(member_id)

    def _ensure_book_exists(self, book_id: int) -> None:
        if self.book_repository.get_book_by_id(book_id) is None:
            raise BookNotFoundError(f"Book with id {book_id} was not found.")

    def _ensure_member_exists(self, member_id: int) -> None:
        if self.member_repository.get_member_by_id(member_id) is None:
            raise MemberNotFoundError(f"Member with id {member_id} was not found.")

    def _ensure_book_is_available(self, book_id: int) -> None:
        active_loans = self.loan_repository.get_active_loans()
        if any(loan.book_id == book_id for loan in active_loans):
            raise BookAlreadyIssuedError(f"Book with id {book_id} is already on loan.")
