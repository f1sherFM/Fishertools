"""Validation exceptions."""

from typing import Any, Optional


class ValidationError(Exception):
    """Raised when validation fails.
    
    This exception provides detailed information about validation failures
    to help beginners understand what went wrong.
    """

    def __init__(self, message: str, value: Any = None, expected_type: Optional[str] = None):
        """Initialize ValidationError with detailed information.
        
        Args:
            message: Human-readable error message
            value: The actual value that failed validation (optional)
            expected_type: The expected type as a string (optional)
        """
        super().__init__(message)
        self.value = value
        self.expected_type = expected_type
