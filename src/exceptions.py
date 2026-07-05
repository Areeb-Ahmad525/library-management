"""Compatibility wrapper for the shared exception module."""

from src.utils.exceptions import (
    BookAlreadyIssuedError,
    BookNotFoundError,
    DuplicateEmailError,
    LibraryError,
    LoanNotFoundError,
    MemberNotFoundError,
    ValidationError,
)

__all__ = [
    "BookAlreadyIssuedError",
    "BookNotFoundError",
    "DuplicateEmailError",
    "LibraryError",
    "LoanNotFoundError",
    "MemberNotFoundError",
    "ValidationError",
]
