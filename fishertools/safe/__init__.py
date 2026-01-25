"""
Safe utilities module for fishertools.

This module provides beginner-friendly versions of common operations
that prevent typical mistakes and provide helpful error messages.
"""

from .collections import safe_get, safe_divide
from .files import safe_read_file
from .strings import safe_string_operations

__all__ = ["safe_get", "safe_divide", "safe_read_file", "safe_string_operations"]