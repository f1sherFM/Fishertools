"""
Unit tests for safe string operations.

These tests validate specific examples and edge cases for safe string functions.
Feature: fishertools-bug-fixes
Requirements: 4.5
"""

import pytest
from fishertools.safe.strings import safe_format, PlaceholderBehavior


class TestSafeFormat:
    """Unit tests for safe_format function."""
    
    def test_safe_format_with_missing_placeholder_default_behavior(self):
        """
        Test safe_format("Hello, {name}!", {}) returns "Hello, [MISSING: name]!"
        Validates: Requirement 4.5
        """
        result = safe_format("Hello, {name}!", {})
        assert result == "Hello, [MISSING: name]!"
    
    def test_safe_format_with_value(self):
        """Test safe_format with provided value."""
        result = safe_format("Hello, {name}!", {"name": "Alice"})
        assert result == "Hello, Alice!"
    
    def test_safe_format_preserve_behavior(self):
        """Test safe_format with PRESERVE behavior keeps original placeholder."""
        result = safe_format("Hello, {name}!", {}, behavior=PlaceholderBehavior.PRESERVE)
        assert result == "Hello, {name}!"
    
    def test_safe_format_empty_behavior(self):
        """Test safe_format with EMPTY behavior removes placeholder."""
        result = safe_format("Hello, {name}!", {}, behavior=PlaceholderBehavior.EMPTY)
        assert result == "Hello, !"
    
    def test_safe_format_missing_behavior_explicit(self):
        """Test safe_format with explicit MISSING behavior."""
        result = safe_format("Hello, {name}!", {}, behavior=PlaceholderBehavior.MISSING)
        assert result == "Hello, [MISSING: name]!"
    
    def test_safe_format_multiple_placeholders(self):
        """Test safe_format with multiple placeholders."""
        result = safe_format("Hello, {first} {last}!", {"first": "John"})
        assert result == "Hello, John [MISSING: last]!"
    
    def test_safe_format_all_values_provided(self):
        """Test safe_format when all values are provided."""
        result = safe_format("Hello, {first} {last}!", {"first": "John", "last": "Doe"})
        assert result == "Hello, John Doe!"
    
    def test_safe_format_with_kwargs(self):
        """Test safe_format with keyword arguments."""
        result = safe_format("Hello, {name}!", name="Bob")
        assert result == "Hello, Bob!"
    
    def test_safe_format_with_positional_args(self):
        """Test safe_format with positional arguments."""
        result = safe_format("Hello, {}!", "World")
        assert result == "Hello, World!"
    
    def test_safe_format_with_format_spec(self):
        """Test safe_format with format specification."""
        result = safe_format("Value: {:.2f}", 3.14159)
        assert result == "Value: 3.14"
    
    def test_safe_format_mixed_values_and_kwargs(self):
        """Test safe_format with both values dict and kwargs."""
        result = safe_format("Hello, {first} {last}!", {"first": "John"}, last="Doe")
        assert result == "Hello, John Doe!"
    
    def test_safe_format_empty_template(self):
        """Test safe_format with empty template."""
        result = safe_format("", {})
        assert result == ""
    
    def test_safe_format_no_placeholders(self):
        """Test safe_format with no placeholders."""
        result = safe_format("Hello, World!", {})
        assert result == "Hello, World!"
    
    def test_safe_format_preserve_with_multiple_missing(self):
        """Test PRESERVE behavior with multiple missing placeholders."""
        result = safe_format("Hello, {first} {last}!", {}, behavior=PlaceholderBehavior.PRESERVE)
        assert result == "Hello, {first} {last}!"
    
    def test_safe_format_empty_with_multiple_missing(self):
        """Test EMPTY behavior with multiple missing placeholders."""
        result = safe_format("Hello, {first} {last}!", {}, behavior=PlaceholderBehavior.EMPTY)
        assert result == "Hello,  !"
    
    def test_safe_format_with_numeric_value(self):
        """Test safe_format with numeric values."""
        result = safe_format("Count: {count}", {"count": 42})
        assert result == "Count: 42"
    
    def test_safe_format_with_float_value(self):
        """Test safe_format with float values."""
        result = safe_format("Price: {price}", {"price": 19.99})
        assert result == "Price: 19.99"
    
    def test_safe_format_with_none_value(self):
        """Test safe_format with None value."""
        result = safe_format("Value: {val}", {"val": None})
        assert result == "Value: None"
    
    def test_safe_format_backward_compatibility_positional(self):
        """Test backward compatibility with positional arguments."""
        # Old usage should still work
        result = safe_format("Hello, {}!", "World")
        assert result == "Hello, World!"
    
    def test_safe_format_backward_compatibility_kwargs(self):
        """Test backward compatibility with keyword arguments."""
        # Old usage should still work
        result = safe_format("Hello, {name}!", name="Alice")
        assert result == "Hello, Alice!"
    
    def test_safe_format_backward_compatibility_missing_returns_template(self):
        """Test backward compatibility - missing args returns template with PRESERVE."""
        # Old behavior was to return template on error
        result = safe_format("Hello, {}!", behavior=PlaceholderBehavior.PRESERVE)
        assert result == "Hello, {}!"
