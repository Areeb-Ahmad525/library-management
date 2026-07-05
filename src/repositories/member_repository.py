from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models import Member
from src.utils.exceptions import DuplicateEmailError, MemberNotFoundError


class MemberRepository:
    """Repository for managing member records."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_member(self, name: str, email: str) -> Member:
        """Create and persist a new member if the email is unique."""
        existing_member = self.db.scalar(select(Member).where(Member.email == email))
        if existing_member is not None:
            raise DuplicateEmailError(f"Email {email} is already registered.")

        member = Member(name=name, email=email)
        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)
        return member

    def get_member_by_id(self, member_id: int) -> Optional[Member]:
        """Return a member by id, or None if it does not exist."""
        return self.db.get(Member, member_id)

    def get_all_members(self) -> List[Member]:
        """Return all members ordered by id."""
        return list(self.db.scalars(select(Member).order_by(Member.id)).all())

    def update_member(
        self,
        member_id: int,
        name: Optional[str] = None,
        email: Optional[str] = None,
    ) -> Member:
        """Update an existing member with any provided field values."""
        member = self.get_member_by_id(member_id)
        if member is None:
            raise MemberNotFoundError(f"Member with id {member_id} was not found.")

        if email is not None:
            existing_member = self.db.scalar(select(Member).where(Member.email == email))
            if existing_member is not None and existing_member.id != member_id:
                raise DuplicateEmailError(f"Email {email} is already registered.")
            member.email = email

        if name is not None:
            member.name = name

        self.db.commit()
        self.db.refresh(member)
        return member

    def delete_member(self, member_id: int) -> bool:
        """Delete a member and return True if the deletion succeeded."""
        member = self.get_member_by_id(member_id)
        if member is None:
            raise MemberNotFoundError(f"Member with id {member_id} was not found.")

        self.db.delete(member)
        self.db.commit()
        return True
