"""Type checking functionality."""

from __future__ import annotations

import functools
import sys
from typing import get_type_hints, Any, Union, get_origin, get_args
from .exceptions import ValidationError


# Python 3.8 compatibility
if sys.version_info >= (3, 8):
    from typing import get_origin, get_args
else:
    def get_origin(tp):
        return getattr(tp, '__origin__', None)
    
    def get_args(tp):
        return getattr(tp, '__args__', ())


def _check_type(value: Any, expected_type: type) -> bool:
    """
    Check if value matches expected type, supporting generic types.
    
    Args:
        value: Value to check
        expected_type: Expected type (can be generic)
        
    Returns:
        True if value matches type, False otherwise
    """
    origin = get_origin(expected_type)
    
    # Handle Union types (including Optional)
    if origin is Union:
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
    
    # Handle regular types
    try:
        return isinstance(value, expected_type)
    except TypeError:
        return False


def validate_types(func):
    """Decorator to validate function argument and return types.

    Uses type hints to validate arguments and return value.
    Supports generic types like Union, Optional, List, Dict.

    Args:
        func: Function to decorate

    Returns:
        Decorated function

    Raises:
        ValidationError: If type validation fails

    Examples:
        >>> @validate_types
        ... def add(a: int, b: int) -> int:
        ...     return a + b
        >>> add(1, 2)
        3
        >>> add("1", 2)  # Raises ValidationError
        
        >>> from typing import Union, Optional
        >>> @validate_types
        ... def process(value: Union[int, str]) -> Optional[str]:
        ...     return str(value) if value else None
        >>> process(42)
        '42'
        >>> process("hello")
        'hello'
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get type hints
        hints = get_type_hints(func)

        # Get function signature
        import inspect

        sig = inspect.signature(func)
        params = list(sig.parameters.keys())

        # Check argument types
        for i, arg in enumerate(args):
            if i < len(params):
                param_name = params[i]
                if param_name in hints:
                    expected_type = hints[param_name]
                    if not _check_type(arg, expected_type):
                        # Get readable type name
                        origin = get_origin(expected_type)
                        if origin:
                            type_name = str(expected_type)
                        else:
                            type_name = expected_type.__name__ if hasattr(expected_type, '__name__') else str(expected_type)
                        
                        raise ValidationError(
                            f"Argument '{param_name}' must be {type_name}, "
                            f"got {type(arg).__name__}"
                        )

        # Check keyword argument types
        for key, value in kwargs.items():
            if key in hints:
                expected_type = hints[key]
                if not _check_type(value, expected_type):
                    origin = get_origin(expected_type)
                    if origin:
                        type_name = str(expected_type)
                    else:
                        type_name = expected_type.__name__ if hasattr(expected_type, '__name__') else str(expected_type)
                    
                    raise ValidationError(
                        f"Argument '{key}' must be {type_name}, "
                        f"got {type(value).__name__}"
                    )

        # Call function
        result = func(*args, **kwargs)

        # Check return type
        if "return" in hints:
            expected_return_type = hints["return"]
            if not _check_type(result, expected_return_type):
                origin = get_origin(expected_return_type)
                if origin:
                    type_name = str(expected_return_type)
                else:
                    type_name = expected_return_type.__name__ if hasattr(expected_return_type, '__name__') else str(expected_return_type)
                
                raise ValidationError(
                    f"Return value must be {type_name}, "
                    f"got {type(result).__name__}"
                )

        return result

    return wrapper
