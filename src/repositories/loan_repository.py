from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from src.database.models import Book, Loan, Member
from src.utils.exceptions import (
    BookNotFoundError,
    LoanNotFoundError,
    MemberNotFoundError,
)


class LoanRepository:
    """Repository for managing book loans."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def issue_book(self, book_id: int, member_id: int) -> Loan:
        """
        Create a new active loan for an existing book and member.

        Args:
            book_id (int): The ID of the book to be issued.
            member_id (int): The ID of the member taking the loan.

        Returns:
            Loan: The newly created Loan instance.

        Raises:
            BookNotFoundError: If the book does not exist.
            MemberNotFoundError: If the member does not exist.
        """
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
        """
        Return a loan by removing it from the active loan set.

        Args:
            loan_id (int): The ID of the loan to return.

        Returns:
            Loan: The Loan instance that was returned and deleted.

        Raises:
            LoanNotFoundError: If the loan does not exist.
        """
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
        """
        Return all currently active loans.

        Returns:
            List[Loan]: A list of all active loans with book and member eager loaded.
        """
        return list(
            self.db.scalars(
                select(Loan)
                .options(joinedload(Loan.book), joinedload(Loan.member))
                .order_by(Loan.id)
            )
            .unique()
            .all()
        )

    def get_member_loans(self, member_id: int) -> List[Loan]:
        """
        Return all loans for a specific member.

        Args:
            member_id (int): The ID of the member.

        Returns:
            List[Loan]: A list of the member's loans with books eager loaded.

        Raises:
            MemberNotFoundError: If the member does not exist.
        """
        member = self.db.get(Member, member_id)
        if member is None:
            raise MemberNotFoundError(f"Member with id {member_id} was not found.")

        return list(
            self.db.scalars(
                select(Loan)
                .options(joinedload(Loan.book), joinedload(Loan.member))
                .where(Loan.member_id == member_id)
                .order_by(Loan.id)
            )
            .unique()
            .all()
        )

    def get_book_loans(self, book_id: int) -> List[Loan]:
        """
        Return all loans for a specific book.

        Args:
            book_id (int): The ID of the book.

        Returns:
            List[Loan]: A list of the book's loans with members eager loaded.

        Raises:
            BookNotFoundError: If the book does not exist.
        """
        book = self.db.get(Book, book_id)
        if book is None:
            raise BookNotFoundError(f"Book with id {book_id} was not found.")

        return list(
            self.db.scalars(
                select(Loan)
                .options(joinedload(Loan.book), joinedload(Loan.member))
                .where(Loan.book_id == book_id)
                .order_by(Loan.id)
            )
            .unique()
            .all()
        )
