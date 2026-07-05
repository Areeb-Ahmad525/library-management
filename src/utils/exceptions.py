class LibraryError(Exception):
    """Base exception for library management errors."""


class BookNotFoundError(LibraryError):
    """Raised when a requested book does not exist."""


class MemberNotFoundError(LibraryError):
    """Raised when a requested member does not exist."""


class LoanNotFoundError(LibraryError):
    """Raised when a requested loan does not exist."""


class DuplicateEmailError(LibraryError):
    """Raised when a member email is already registered."""


class BookAlreadyIssuedError(LibraryError):
    """Raised when a book already has an active loan."""


class ValidationError(LibraryError):
    """Raised when input values fail business validation rules."""
