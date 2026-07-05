import re
from typing import Optional


def normalize_required_text(value: str, field_name: str) -> str:
    """Trim and validate a required text field."""
    normalized_value = value.strip() if isinstance(value, str) else ""
    if not normalized_value:
        raise ValueError(f"{field_name.capitalize()} cannot be empty.")
    return normalized_value


def normalize_optional_text(value: Optional[str], field_name: str) -> Optional[str]:
    """Trim and validate an optional text field."""
    if value is None:
        return None
    normalized_value = value.strip()
    if not normalized_value:
        raise ValueError(f"{field_name.capitalize()} cannot be empty.")
    return normalized_value


def validate_email(email: str) -> str:
    """Validate an email address format."""
    normalized_email = normalize_required_text(email, "email")
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", normalized_email):
        raise ValueError("Email format is invalid.")
    return normalized_email
