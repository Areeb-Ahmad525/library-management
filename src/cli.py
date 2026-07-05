import logging
from typing import Optional

from src.exceptions import (
    BookAlreadyIssuedError,
    BookNotFoundError,
    DuplicateEmailError,
    LoanNotFoundError,
    MemberNotFoundError,
    ValidationError,
)
from src.services.book_service import BookService
from src.services.loan_service import LoanService
from src.services.member_service import MemberService

logger = logging.getLogger(__name__)


class CLI:
    """Interactive command-line interface for library management."""

    def __init__(
        self,
        book_service: BookService,
        member_service: MemberService,
        loan_service: LoanService,
    ) -> None:
        self.book_service = book_service
        self.member_service = member_service
        self.loan_service = loan_service

    def run(self) -> None:
        """Start the interactive CLI loop."""
        while True:
            self._print_header("Library Management System")
            print("1. Book Management")
            print("2. Member Management")
            print("3. Loan Management")
            print("4. Exit")
            choice = self._prompt_choice("Select an option", 1, 4)

            if choice == 1:
                self._book_menu()
            elif choice == 2:
                self._member_menu()
            elif choice == 3:
                self._loan_menu()
            else:
                print("Goodbye!")
                break

    def _book_menu(self) -> None:
        """Display and handle the book management submenu."""
        while True:
            self._print_header("Book Management")
            print("1. Add Book")
            print("2. List Books")
            print("3. Search Book by ID")
            print("4. Update Book")
            print("5. Delete Book")
            print("6. Back")
            choice = self._prompt_choice("Select an option", 1, 6)

            if choice == 1:
                self._add_book()
            elif choice == 2:
                self._list_books()
            elif choice == 3:
                self._search_book()
            elif choice == 4:
                self._update_book()
            elif choice == 5:
                self._delete_book()
            else:
                break

    def _member_menu(self) -> None:
        """Display and handle the member management submenu."""
        while True:
            self._print_header("Member Management")
            print("1. Register Member")
            print("2. List Members")
            print("3. Search Member")
            print("4. Update Member")
            print("5. Delete Member")
            print("6. Back")
            choice = self._prompt_choice("Select an option", 1, 6)

            if choice == 1:
                self._register_member()
            elif choice == 2:
                self._list_members()
            elif choice == 3:
                self._search_member()
            elif choice == 4:
                self._update_member()
            elif choice == 5:
                self._delete_member()
            else:
                break

    def _loan_menu(self) -> None:
        """Display and handle the loan management submenu."""
        while True:
            self._print_header("Loan Management")
            print("1. Issue Book")
            print("2. Return Book")
            print("3. View Active Loans")
            print("4. View Loans by Member")
            print("5. Back")
            choice = self._prompt_choice("Select an option", 1, 5)

            if choice == 1:
                self._issue_book()
            elif choice == 2:
                self._return_book()
            elif choice == 3:
                self._view_active_loans()
            elif choice == 4:
                self._view_member_loans()
            else:
                break

    def _add_book(self) -> None:
        """Prompt for book details and create a book through the service layer."""
        title = self._prompt_non_empty("Title")
        author = self._prompt_non_empty("Author")

        try:
            book = self.book_service.add_book(title, author)
        except ValidationError as exc:
            self._show_error(str(exc))
            return

        self._print_success(
            "Book added successfully.",
            {
                "ID": book.id,
                "Title": book.title,
                "Author": book.author,
            },
        )

    def _list_books(self) -> None:
        """List all books."""
        books = self.book_service.list_books()
        if not books:
            print("No books found.")
            return

        print("ID   Title                     Author")
        print("-" * 44)
        for book in books:
            print(f"{book.id:<4} {book.title:<25} {book.author}")

    def _search_book(self) -> None:
        """Search for a book by id."""
        book_id = self._prompt_int("Book ID")
        try:
            book = self.book_service.get_book(book_id)
        except BookNotFoundError as exc:
            self._show_error(str(exc))
            return

        self._print_success(
            "Book found.",
            {"ID": book.id, "Title": book.title, "Author": book.author},
        )

    def _update_book(self) -> None:
        """Update an existing book."""
        book_id = self._prompt_int("Book ID")
        title = self._prompt_optional("Title")
        author = self._prompt_optional("Author")

        try:
            book = self.book_service.update_book(book_id, title=title, author=author)
        except (BookNotFoundError, ValidationError) as exc:
            self._show_error(str(exc))
            return

        self._print_success(
            "Book updated successfully.",
            {"ID": book.id, "Title": book.title, "Author": book.author},
        )

    def _delete_book(self) -> None:
        """Delete a book."""
        book_id = self._prompt_int("Book ID")
        try:
            self.book_service.remove_book(book_id)
        except BookNotFoundError as exc:
            self._show_error(str(exc))
            return

        print("Book deleted successfully.")

    def _register_member(self) -> None:
        """Prompt for member details and register a member through the service layer."""
        name = self._prompt_non_empty("Name")
        email = self._prompt_non_empty("Email")

        try:
            member = self.member_service.register_member(name, email)
        except (ValidationError, DuplicateEmailError) as exc:
            self._show_error(str(exc))
            return

        self._print_success(
            "Member registered successfully.",
            {"ID": member.id, "Name": member.name, "Email": member.email},
        )

    def _list_members(self) -> None:
        """List all members."""
        members = self.member_service.list_members()
        if not members:
            print("No members found.")
            return

        print("ID   Name                      Email")
        print("-" * 44)
        for member in members:
            print(f"{member.id:<4} {member.name:<25} {member.email}")

    def _search_member(self) -> None:
        """Search for a member by id."""
        member_id = self._prompt_int("Member ID")
        try:
            member = self.member_service.get_member(member_id)
        except MemberNotFoundError as exc:
            self._show_error(str(exc))
            return

        self._print_success(
            "Member found.",
            {"ID": member.id, "Name": member.name, "Email": member.email},
        )

    def _update_member(self) -> None:
        """Update an existing member."""
        member_id = self._prompt_int("Member ID")
        name = self._prompt_optional("Name")
        email = self._prompt_optional("Email")

        try:
            member = self.member_service.update_member(member_id, name=name, email=email)
        except (MemberNotFoundError, ValidationError, DuplicateEmailError) as exc:
            self._show_error(str(exc))
            return

        self._print_success(
            "Member updated successfully.",
            {"ID": member.id, "Name": member.name, "Email": member.email},
        )

    def _delete_member(self) -> None:
        """Delete a member."""
        member_id = self._prompt_int("Member ID")
        try:
            self.member_service.remove_member(member_id)
        except MemberNotFoundError as exc:
            self._show_error(str(exc))
            return

        print("Member deleted successfully.")

    def _issue_book(self) -> None:
        """Issue a book to a member."""
        book_id = self._prompt_int("Book ID")
        member_id = self._prompt_int("Member ID")

        try:
            loan = self.loan_service.issue_book(book_id, member_id)
        except (BookNotFoundError, MemberNotFoundError, BookAlreadyIssuedError) as exc:
            self._show_error(str(exc))
            return

        self._print_success(
            "Book issued successfully.",
            {"Loan ID": loan.id, "Book ID": loan.book_id, "Member ID": loan.member_id},
        )

    def _return_book(self) -> None:
        """Return a previously issued book."""
        loan_id = self._prompt_int("Loan ID")

        try:
            loan = self.loan_service.return_book(loan_id)
        except LoanNotFoundError as exc:
            self._show_error(str(exc))
            return

        self._print_success(
            "Book returned successfully.",
            {"Loan ID": loan.id, "Book ID": loan.book_id, "Member ID": loan.member_id},
        )

    def _view_active_loans(self) -> None:
        """Display all active loans."""
        loans = self.loan_service.get_active_loans()
        if not loans:
            print("No active loans found.")
            return

        print("ID   Book ID   Member ID")
        print("-" * 24)
        for loan in loans:
            print(f"{loan.id:<4} {loan.book_id:<8} {loan.member_id}")

    def _view_member_loans(self) -> None:
        """Display all loans for a specific member."""
        member_id = self._prompt_int("Member ID")
        try:
            loans = self.loan_service.get_member_loans(member_id)
        except MemberNotFoundError as exc:
            self._show_error(str(exc))
            return

        if not loans:
            print("No loans found for this member.")
            return

        print("ID   Book ID   Member ID")
        print("-" * 24)
        for loan in loans:
            print(f"{loan.id:<4} {loan.book_id:<8} {loan.member_id}")

    def _prompt_choice(self, prompt: str, minimum: int, maximum: int) -> int:
        """Prompt for a numeric menu choice until it is valid."""
        while True:
            value = input(f"{prompt}: ").strip()
            if value.isdigit():
                choice = int(value)
                if minimum <= choice <= maximum:
                    return choice
            print("Invalid option. Please try again.")

    def _prompt_non_empty(self, field_name: str) -> str:
        """Prompt for a non-empty text value."""
        while True:
            value = input(f"{field_name}: ").strip()
            if value:
                return value
            print(f"{field_name} cannot be empty.")

    def _prompt_optional(self, field_name: str) -> Optional[str]:
        """Prompt for an optional field value, allowing blank input to skip updates."""
        value = input(f"{field_name} (leave blank to skip): ").strip()
        return value or None

    def _prompt_int(self, field_name: str) -> int:
        """Prompt for an integer value until valid."""
        while True:
            value = input(f"{field_name}: ").strip()
            if value.isdigit():
                return int(value)
            print("Please enter a valid number.")

    def _print_header(self, title: str) -> None:
        """Print a formatted section header."""
        print("\n" + "-" * 32)
        print(title)
        print("-" * 32)

    def _show_error(self, message: str) -> None:
        """Show a friendly error message to the user."""
        print(f"Error: {message}")

    def _print_success(self, title: str, details: dict[str, object]) -> None:
        """Print a formatted success message with fields."""
        print(f"\n{title}")
        for key, value in details.items():
            print(f"{key}: {value}")
        print("-" * 32)
