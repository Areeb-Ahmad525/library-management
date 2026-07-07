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
        """
        Create and persist a new member if the email is unique.

        Args:
            name (str): The full name of the member.
            email (str): The email address of the member.

        Returns:
            Member: The newly created Member instance.

        Raises:
            DuplicateEmailError: If a member with the same email already exists.
        """
        existing_member = self.db.scalar(select(Member).where(Member.email == email))
        if existing_member is not None:
            raise DuplicateEmailError(f"Email {email} is already registered.")

        member = Member(name=name, email=email)
        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)
        return member

    def get_member_by_id(self, member_id: int) -> Optional[Member]:
        """
        Return a member by id, or None if it does not exist.

        Args:
            member_id (int): The unique identifier of the member.

        Returns:
            Optional[Member]: The Member instance if found, otherwise None.
        """
        return self.db.get(Member, member_id)

    def get_all_members(self) -> List[Member]:
        """
        Return all members ordered by id.

        Returns:
            List[Member]: A list of all Member instances in the database.
        """
        return list(self.db.scalars(select(Member).order_by(Member.id)).all())

    def update_member(
        self,
        member_id: int,
        name: Optional[str] = None,
        email: Optional[str] = None,
    ) -> Member:
        """
        Update an existing member with any provided field values.

        Args:
            member_id (int): The unique identifier of the member to update.
            name (Optional[str]): The new name, if provided.
            email (Optional[str]): The new email, if provided.

        Returns:
            Member: The updated Member instance.

        Raises:
            MemberNotFoundError: If the member does not exist.
            DuplicateEmailError: If the new email is already registered to another member.
        """
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
        """
        Delete a member and return True if the deletion succeeded.

        Args:
            member_id (int): The unique identifier of the member to delete.

        Returns:
            bool: True upon successful deletion.

        Raises:
            MemberNotFoundError: If the member does not exist.
        """
        member = self.get_member_by_id(member_id)
        if member is None:
            raise MemberNotFoundError(f"Member with id {member_id} was not found.")

        self.db.delete(member)
        self.db.commit()
        return True
