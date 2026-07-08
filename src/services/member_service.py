import logging
from typing import List, Optional

from src.database.models import Member
from src.repositories.member_repository import MemberRepository
from src.utils.exceptions import (
    DuplicateEmailError,
    MemberNotFoundError,
    ValidationError,
)
from src.utils.validators import (
    normalize_optional_text,
    normalize_required_text,
    validate_email,
)

logger = logging.getLogger(__name__)


class MemberService:
    """Apply business rules for member operations."""

    def __init__(self, member_repository: MemberRepository) -> None:
        self.member_repository = member_repository

    def register_member(self, name: str, email: str) -> Member:
        """Create a new member after validating the provided values."""
        normalized_name = self._normalize_required_field(name, "name")
        normalized_email = self._validate_email(email)

        try:
            member = self.member_repository.create_member(
                normalized_name, normalized_email
            )
        except DuplicateEmailError:
            logger.warning("Validation failure: duplicate email %s", normalized_email)
            raise

        logger.info("Member registered: %s", member.email)
        return member

    def get_member(self, member_id: int) -> Optional[Member]:
        """Return a member by id, or None if it is missing."""
        member = self.member_repository.get_member_by_id(member_id)
        if member is None:
            raise MemberNotFoundError(f"Member with id {member_id} was not found.")
        return member

    def list_members(self) -> List[Member]:
        """Return all members in the repository."""
        return self.member_repository.get_all_members()

    def update_member(
        self,
        member_id: int,
        name: Optional[str] = None,
        email: Optional[str] = None,
    ) -> Member:
        """Update a member after validating any provided values."""
        self.get_member(member_id)

        normalized_name = self._normalize_optional_field(name, "name")
        normalized_email = self._validate_optional_email(email)

        member = self.member_repository.update_member(
            member_id,
            name=normalized_name,
            email=normalized_email,
        )
        return member

    def remove_member(self, member_id: int) -> bool:
        """Remove a member after ensuring it exists."""
        self.get_member(member_id)
        self.member_repository.delete_member(member_id)
        return True

    def _normalize_required_field(self, value: str, field_name: str) -> str:
        try:
            return normalize_required_text(value, field_name)
        except ValueError as exc:
            logger.warning("Validation failure: %s is empty", field_name)
            raise ValidationError(str(exc)) from exc

    def _normalize_optional_field(
        self, value: Optional[str], field_name: str
    ) -> Optional[str]:
        try:
            return normalize_optional_text(value, field_name)
        except ValueError as exc:
            logger.warning("Validation failure: %s is empty", field_name)
            raise ValidationError(str(exc)) from exc

    def _validate_email(self, email: str) -> str:
        try:
            return validate_email(email)
        except ValueError as exc:
            logger.warning("Validation failure: invalid email %s", email)
            raise ValidationError(str(exc)) from exc

    def _validate_optional_email(self, email: Optional[str]) -> Optional[str]:
        if email is None:
            return None
        return self._validate_email(email)
