import re
from typing import Optional


def normalize_required_text(value: str, field_name: str) -> str:
    """
    Trim and validate a required text field.

    Args:
        value (str): The input text to normalize.
        field_name (str): The name of the field for error reporting.

    Returns:
        str: The stripped text.

    Raises:
        ValueError: If the resulting text is empty.
    """
    normalized_value = value.strip() if isinstance(value, str) else ""
    if not normalized_value:
        raise ValueError(f"{field_name.capitalize()} cannot be empty.")
    return normalized_value


def normalize_optional_text(value: Optional[str], field_name: str) -> Optional[str]:
    """
    Trim and validate an optional text field.

    Args:
        value (Optional[str]): The input text, or None.
        field_name (str): The name of the field for error reporting.

    Returns:
        Optional[str]: The stripped text, or None if the input was None.

    Raises:
        ValueError: If the provided text is empty after stripping.
    """
    if value is None:
        return None
    normalized_value = value.strip()
    if not normalized_value:
        raise ValueError(f"{field_name.capitalize()} cannot be empty.")
    return normalized_value


def validate_email(email: str) -> str:
    """
    Validate an email address format.

    Args:
        email (str): The email address to validate.

    Returns:
        str: The normalized, validated email.

    Raises:
        ValueError: If the email format is invalid.
    """
    normalized_email = normalize_required_text(email, "email")
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", normalized_email):
        raise ValueError("Email format is invalid.")
    return normalized_email
