"""Data validation functions."""

from __future__ import annotations

import re
import sys
from typing import Any, Dict, Optional, Type, Union, get_origin, get_args
from .exceptions import ValidationError


# Python 3.8 compatibility for get_origin/get_args
if sys.version_info >= (3, 8):
    from typing import get_origin, get_args
else:
    def get_origin(tp):
        return getattr(tp, '__origin__', None)
    
    def get_args(tp):
        return getattr(tp, '__args__', ())


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
    
    # Accept numeric strings and bools (bool is a subclass of int in Python)
    if isinstance(value, (int, float, bool)):
        numeric_value = float(value)
    elif isinstance(value, str):
        try:
            numeric_value = float(value)
        except (TypeError, ValueError) as e:
            raise ValidationError(
                f"Expected number, got {type(value).__name__}",
                value=value,
                expected_type="number"
            ) from e
    else:
        raise ValidationError(
            f"Expected number, got {type(value).__name__}",
            value=value,
            expected_type="number"
        )

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


def _check_type(value: Any, expected_type: Type) -> bool:
    """
    Check if value matches expected type, supporting generic types.
    
    Handles Union, Optional, List, Dict, and other generic types properly.
    
    Args:
        value: Value to check
        expected_type: Expected type (can be generic like Union[int, str])
        
    Returns:
        True if value matches type, False otherwise
        
    Examples:
        >>> _check_type(42, int)
        True
        >>> _check_type(42, Union[int, str])
        True
        >>> _check_type([1, 2, 3], List[int])
        True
        >>> _check_type([1, "2", 3], List[int])
        False
    """
    origin = get_origin(expected_type)
    
    # Handle Union types (including Optional)
    if origin is Union:
        # Optional[X] is Union[X, None]
        return any(_check_type(value, arg) for arg in get_args(expected_type))
    
    # Handle List types
    if origin is list:
        if not isinstance(value, list):
            return False
        args = get_args(expected_type)
        if args:
            item_type = args[0]
            return all(_check_type(item, item_type) for item in value)
        return True
    
    # Handle Dict types
    if origin is dict:
        if not isinstance(value, dict):
            return False
        args = get_args(expected_type)
        if len(args) == 2:
            key_type, value_type = args
            return all(
                _check_type(k, key_type) and _check_type(v, value_type)
                for k, v in value.items()
            )
        return True
    
    # Handle Tuple types
    if origin is tuple:
        if not isinstance(value, tuple):
            return False
        args = get_args(expected_type)
        if args:
            if len(args) != len(value):
                return False
            return all(_check_type(v, t) for v, t in zip(value, args))
        return True
    
    # Handle regular types
    try:
        return isinstance(value, expected_type)
    except TypeError:
        # If isinstance fails (e.g., with some generic types), return False
        return False


def validate_structure(data: Dict[str, Any], schema: Dict[str, Type]) -> None:
    """
    Validate data structure against schema with support for generic types.
    
    Supports Union, Optional, List, Dict, and other generic types.

    Args:
        data: Data to validate
        schema: Schema with type definitions (supports generic types)

    Raises:
        ValidationError: If structure is invalid

    Examples:
        >>> schema = {"name": str, "age": int}
        >>> validate_structure({"name": "Alice", "age": 25}, schema)
        
        >>> from typing import Optional, List, Union
        >>> schema = {"value": Optional[int], "items": List[int]}
        >>> validate_structure({"value": 42, "items": [1, 2, 3]}, schema)
        
        >>> schema = {"id": Union[int, str]}
        >>> validate_structure({"id": "abc123"}, schema)
    """
    for key, expected_type in schema.items():
        if key not in data:
            raise ValidationError(f"Missing required key: {key}")

        value = data[key]
        
        # Use _check_type for generic type support
        if not _check_type(value, expected_type):
            # Get readable type name
            origin = get_origin(expected_type)
            if origin:
                type_name = str(expected_type)
            else:
                type_name = expected_type.__name__ if hasattr(expected_type, '__name__') else str(expected_type)
            
            raise ValidationError(
                f"Key '{key}' must be {type_name}, "
                f"got {type(value).__name__}"
            )
