"""
Safe string operations for beginners.

This module provides safe string handling utilities that gracefully
handle None values and common string operation errors.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional, List, Any, Dict
import re


# Compiled regex pattern for placeholder matching (module-level for performance)
_PLACEHOLDER_PATTERN = re.compile(r'\{([^}:!]+)(?:[^}]*)?\}')


class PlaceholderBehavior(Enum):
    """
    Defines how safe_format() handles missing placeholders.
    
    Attributes:
        PRESERVE: Keep original placeholders unchanged (e.g., "{name}")
        MISSING: Replace with "[MISSING: key_name]" format
        EMPTY: Replace with empty string
    """
    PRESERVE = "preserve"
    MISSING = "missing"
    EMPTY = "empty"


def safe_strip(text: Optional[str], chars: Optional[str] = None, default: str = '') -> str:
    """
    Safely strip whitespace or characters from a string.
    
    Handles None values gracefully instead of raising AttributeError.
    
    Args:
        text: String to strip (can be None)
        chars: Characters to remove (None means whitespace)
        default: Value to return if text is None
        
    Returns:
        Stripped string or default value
        
    Examples:
        >>> safe_strip("  hello  ")
        'hello'
        >>> safe_strip(None)
        ''
        >>> safe_strip(None, default="N/A")
        'N/A'
        >>> safe_strip("...hello...", chars=".")
        'hello'
    """
    if text is None:
        return default
    try:
        return text.strip(chars)
    except (AttributeError, TypeError):
        return default


def safe_split(text: Optional[str], sep: Optional[str] = None, 
               maxsplit: int = -1, default: Optional[List[str]] = None) -> List[str]:
    """
    Safely split a string into a list.
    
    Handles None values and returns empty list or default instead of raising errors.
    
    Args:
        text: String to split (can be None)
        sep: Separator (None means any whitespace)
        maxsplit: Maximum number of splits
        default: Value to return if text is None (defaults to empty list)
        
    Returns:
        List of strings or default value
        
    Examples:
        >>> safe_split("a,b,c", ",")
        ['a', 'b', 'c']
        >>> safe_split(None)
        []
        >>> safe_split(None, default=["N/A"])
        ['N/A']
        >>> safe_split("a b c", maxsplit=1)
        ['a', 'b c']
    """
    if default is None:
        default = []
    
    if text is None:
        return default
    
    try:
        return text.split(sep, maxsplit)
    except (AttributeError, TypeError):
        return default


def safe_join(separator: str, items: List[Any], skip_none: bool = True, 
              stringify: bool = True) -> str:
    """
    Safely join items into a string.
    
    Handles None values in the list and can convert non-strings to strings.
    
    Args:
        separator: String to use between items
        items: List of items to join (can contain None)
        skip_none: If True, skip None values; if False, convert to "None"
        stringify: If True, convert non-strings to strings
        
    Returns:
        Joined string
        
    Examples:
        >>> safe_join(", ", ["a", "b", "c"])
        'a, b, c'
        >>> safe_join(", ", ["a", None, "c"])
        'a, c'
        >>> safe_join(", ", ["a", None, "c"], skip_none=False)
        'a, None, c'
        >>> safe_join("-", [1, 2, 3])
        '1-2-3'
    """
    if items is None:
        return ""
    
    try:
        processed = []
        for item in items:
            if item is None:
                if not skip_none:
                    processed.append("None")
            elif stringify and not isinstance(item, str):
                processed.append(str(item))
            else:
                processed.append(item)
        
        return separator.join(processed)
    except (TypeError, AttributeError):
        return ""


def safe_format(template: str, values: Optional[Dict[str, Any]] = None, 
                behavior: Optional[PlaceholderBehavior] = None,
                *args, **kwargs) -> str:
    """
    Safely format a string template with configurable placeholder handling.
    
    Supports both positional and keyword arguments, with configurable behavior
    for missing placeholders.
    
    Args:
        template: Format string template
        values: Dictionary of values for named placeholders (optional)
        behavior: How to handle missing placeholders (default: MISSING)
        *args: Positional arguments for formatting
        **kwargs: Keyword arguments for formatting
        
    Returns:
        Formatted string with placeholders handled according to behavior
        
    Examples:
        >>> safe_format("Hello, {name}!", {"name": "Alice"})
        'Hello, Alice!'
        >>> safe_format("Hello, {name}!", {})
        'Hello, [MISSING: name]!'
        >>> safe_format("Hello, {name}!", {}, behavior=PlaceholderBehavior.PRESERVE)
        'Hello, {name}!'
        >>> safe_format("Hello, {name}!", {}, behavior=PlaceholderBehavior.EMPTY)
        'Hello, !'
        >>> safe_format("Hello, {}!", "World")
        'Hello, World!'
        >>> safe_format("Value: {:.2f}", 3.14159)
        'Value: 3.14'
    """
    # Default behavior
    if behavior is None:
        behavior = PlaceholderBehavior.MISSING
    
    # Handle backward compatibility: if values is not a dict, treat it as a positional arg
    if values is not None and not isinstance(values, dict):
        # Old usage: safe_format(template, *args, **kwargs)
        args = (values,) + args
        values = None
    
    # Merge values dict with kwargs if provided
    if values is not None:
        format_kwargs = {**values, **kwargs}
    else:
        format_kwargs = kwargs
    
    try:
        # Try normal formatting first
        return template.format(*args, **format_kwargs)
    except (KeyError, IndexError, ValueError, TypeError) as e:
        # Handle missing placeholders based on behavior
        if isinstance(e, KeyError) and behavior != PlaceholderBehavior.PRESERVE:
            # Use pre-compiled pattern for better performance
            def replace_placeholder(match):
                placeholder_name = match.group(1).strip()
                
                # Skip positional placeholders (empty or numeric)
                if placeholder_name == "" or placeholder_name.isdigit():
                    return match.group(0)
                
                # Check if this placeholder has a value
                if placeholder_name in format_kwargs:
                    try:
                        # Try to format just this placeholder
                        return match.group(0).format(**{placeholder_name: format_kwargs[placeholder_name]})
                    except (ValueError, KeyError):
                        pass
                
                # Handle missing placeholder based on behavior
                if behavior == PlaceholderBehavior.MISSING:
                    return f"[MISSING: {placeholder_name}]"
                elif behavior == PlaceholderBehavior.EMPTY:
                    return ""
                else:  # PRESERVE
                    return match.group(0)
            
            return _PLACEHOLDER_PATTERN.sub(replace_placeholder, template)
        
        # For other errors or PRESERVE behavior, return original template
        return template


def safe_lower(text: Optional[str], default: str = '') -> str:
    """
    Safely convert string to lowercase.
    
    Args:
        text: String to convert (can be None)
        default: Value to return if text is None
        
    Returns:
        Lowercase string or default value
        
    Examples:
        >>> safe_lower("HELLO")
        'hello'
        >>> safe_lower(None)
        ''
    """
    if text is None:
        return default
    try:
        return text.lower()
    except (AttributeError, TypeError):
        return default


def safe_upper(text: Optional[str], default: str = '') -> str:
    """
    Safely convert string to uppercase.
    
    Args:
        text: String to convert (can be None)
        default: Value to return if text is None
        
    Returns:
        Uppercase string or default value
        
    Examples:
        >>> safe_upper("hello")
        'HELLO'
        >>> safe_upper(None)
        ''
    """
    if text is None:
        return default
    try:
        return text.upper()
    except (AttributeError, TypeError):
        return default


__all__ = [
    'PlaceholderBehavior',
    'safe_strip',
    'safe_split', 
    'safe_join',
    'safe_format',
    'safe_lower',
    'safe_upper'
]