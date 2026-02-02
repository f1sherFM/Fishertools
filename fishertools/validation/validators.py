"""Data validation functions."""

import re
from typing import Any, Dict, Optional, Type
from .exceptions import ValidationError


def validate_email(email: str) -> None:
    """Validate email format.

    Args:
        email: Email to validate

    Raises:
        ValidationError: If email is invalid

    Examples:
        >>> validate_email("user@example.com")
        >>> validate_email("invalid-email")  # Raises ValidationError
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        raise ValidationError(f"Invalid email format: {email}")


def validate_url(url: str) -> None:
    """Validate URL format.

    Args:
        url: URL to validate

    Raises:
        ValidationError: If URL is invalid

    Examples:
        >>> validate_url("https://example.com")
        >>> validate_url("not-a-url")  # Raises ValidationError
    """
    pattern = r"^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    if not re.match(pattern, url):
        raise ValidationError(f"Invalid URL format: {url}")


def validate_number(
    value: Any,
    min_val: Optional[float] = None,
    max_val: Optional[float] = None,
) -> float:
    """Validate that value is a number and optionally within range.

    Args:
        value: Value to validate (should be numeric)
        min_val: Minimum value (inclusive)
        max_val: Maximum value (inclusive)

    Returns:
        The validated number as a float

    Raises:
        ValidationError: If value is not numeric or out of range

    Examples:
        >>> validate_number(42, min_val=0, max_val=100)
        42.0
        >>> validate_number("string", min_val=0, max_val=100)  # Raises ValidationError
        >>> validate_number(None)  # Raises ValidationError
    """
    # Handle None values specifically
    if value is None:
        raise ValidationError(
            "Value cannot be None", 
            value=value, 
            expected_type="number"
        )
    
    # Try to convert to float and validate type
    try:
        # Check if it's already a number type
        if not isinstance(value, (int, float)):
            # Try to convert string numbers
            if isinstance(value, str):
                try:
                    numeric_value = float(value)
                except ValueError:
                    raise ValidationError(
                        f"Expected number, got {type(value).__name__}",
                        value=value,
                        expected_type="number"
                    )
            else:
                raise ValidationError(
                    f"Expected number, got {type(value).__name__}",
                    value=value,
                    expected_type="number"
                )
        else:
            numeric_value = float(value)
    except (TypeError, ValueError) as e:
        # Catch any other type conversion errors
        raise ValidationError(
            f"Expected number, got {type(value).__name__}",
            value=value,
            expected_type="number"
        ) from e

    # Wrap range comparisons in try-catch to handle any comparison errors
    try:
        if min_val is not None and numeric_value < min_val:
            raise ValidationError(f"Value {numeric_value} is less than minimum {min_val}")

        if max_val is not None and numeric_value > max_val:
            raise ValidationError(f"Value {numeric_value} is greater than maximum {max_val}")
    except TypeError as e:
        # Handle cases where comparison operators fail
        raise ValidationError(
            f"Cannot compare {type(numeric_value).__name__} with range limits",
            value=numeric_value,
            expected_type="comparable number"
        ) from e

    return numeric_value


def validate_string(
    value: str,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    pattern: Optional[str] = None,
) -> None:
    """Validate string properties.

    Args:
        value: String to validate
        min_length: Minimum length
        max_length: Maximum length
        pattern: Regex pattern to match

    Raises:
        ValidationError: If validation fails

    Examples:
        >>> validate_string("hello", min_length=3, max_length=10)
        >>> validate_string("hi", min_length=3)  # Raises ValidationError
    """
    if min_length is not None and len(value) < min_length:
        raise ValidationError(
            f"String length {len(value)} is less than minimum {min_length}"
        )

    if max_length is not None and len(value) > max_length:
        raise ValidationError(
            f"String length {len(value)} is greater than maximum {max_length}"
        )

    if pattern is not None and not re.match(pattern, value):
        raise ValidationError(f"String does not match pattern: {pattern}")


def validate_structure(data: Dict[str, Any], schema: Dict[str, Type]) -> None:
    """Validate data structure against schema.

    Args:
        data: Data to validate
        schema: Schema with type definitions

    Raises:
        ValidationError: If structure is invalid

    Examples:
        >>> schema = {"name": str, "age": int}
        >>> validate_structure({"name": "Alice", "age": 25}, schema)
        >>> validate_structure({"name": "Bob", "age": "thirty"}, schema)  # Raises
    """
    for key, expected_type in schema.items():
        if key not in data:
            raise ValidationError(f"Missing required key: {key}")

        value = data[key]
        if not isinstance(value, expected_type):
            raise ValidationError(
                f"Key '{key}' must be {expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
