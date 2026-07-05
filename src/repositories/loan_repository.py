from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models import Book, Loan, Member
from src.utils.exceptions import BookNotFoundError, LoanNotFoundError, MemberNotFoundError


class LoanRepository:
    """Repository for managing book loans."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def issue_book(self, book_id: int, member_id: int) -> Loan:
        """Create a new active loan for an existing book and member."""
        try:
            book = self.db.get(Book, book_id)
            if book is None:
                raise BookNotFoundError(f"Book with id {book_id} was not found.")

            member = self.db.get(Member, member_id)
            if member is None:
                raise MemberNotFoundError(f"Member with id {member_id} was not found.")

            loan = Loan(book_id=book_id, member_id=member_id)
            self.db.add(loan)
            self.db.commit()
            self.db.refresh(loan)
            return loan
        except (BookNotFoundError, MemberNotFoundError):
            self.db.rollback()
            raise
        except Exception:
            self.db.rollback()
            raise

    def return_book(self, loan_id: int) -> Loan:
        """Return a loan by removing it from the active loan set."""
        loan = self.db.get(Loan, loan_id)
        if loan is None:
            raise LoanNotFoundError(f"Loan with id {loan_id} was not found.")

        try:
            self.db.delete(loan)
            self.db.commit()
            return loan
        except Exception:
            self.db.rollback()
            raise

    def get_active_loans(self) -> List[Loan]:
        """Return all currently active loans."""
        return list(self.db.scalars(select(Loan).order_by(Loan.id)).all())

    def get_member_loans(self, member_id: int) -> List[Loan]:
        """Return all loans for a specific member."""
        member = self.db.get(Member, member_id)
        if member is None:
            raise MemberNotFoundError(f"Member with id {member_id} was not found.")

        return list(
            self.db.scalars(
                select(Loan)
                .where(Loan.member_id == member_id)
                .order_by(Loan.id)
            ).all()
        )

    def get_book_loans(self, book_id: int) -> List[Loan]:
        """Return all loans for a specific book."""
        book = self.db.get(Book, book_id)
        if book is None:
            raise BookNotFoundError(f"Book with id {book_id} was not found.")

        return list(
            self.db.scalars(
                select(Loan)
                .where(Loan.book_id == book_id)
                .order_by(Loan.id)
            ).all()
        )
