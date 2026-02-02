"""
Unit tests for safe collection operations.

These tests validate specific examples and edge cases for safe collection functions.
"""

import pytest
from fishertools.safe.collections import safe_average


class TestSafeAverage:
    """Unit tests for safe_average function."""
    
    def test_safe_average_with_valid_integers(self):
        """
        Test safe_average([1, 2, 3]) returns 2.0
        Requirements: 5.3, 5.1
        """
        result = safe_average([1, 2, 3])
        assert result == 2.0
    
    def test_safe_average_with_empty_list_default_zero(self):
        """
        Test safe_average([], default=0) returns 0
        Requirements: 5.4, 5.1
        """
        result = safe_average([], default=0)
        assert result == 0
    
    def test_safe_average_with_empty_list_no_default(self):
        """
        Test empty list behavior with default parameter
        Requirements: 5.4, 5.1
        """
        result = safe_average([])
        assert result == 0  # Default is 0
    
    def test_safe_average_with_floats(self):
        """Test safe_average with floating point numbers."""
        result = safe_average([1.5, 2.5, 3.0])
        assert abs(result - 2.3333333333333335) < 1e-10
    
    def test_safe_average_filters_non_numeric_values(self):
        """
        Test safe_average filters out non-numeric values
        Requirements: 5.2
        """
        result = safe_average([1, 2, "invalid", 3])
        assert result == 2.0
    
    def test_safe_average_with_all_non_numeric_values(self):
        """
        Test safe_average with all non-numeric values returns default
        Requirements: 5.2
        """
        result = safe_average(["a", "b", "c"], default=-1)
        assert result == -1
    
    def test_safe_average_filters_booleans(self):
        """Test that booleans are filtered out (not treated as 0/1)."""
        result = safe_average([1, 2, True, False, 3])
        assert result == 2.0  # Should only average [1, 2, 3]
    
    def test_safe_average_with_none_values(self):
        """Test safe_average filters out None values."""
        result = safe_average([1, None, 2, None, 3])
        assert result == 2.0
    
    def test_safe_average_with_mixed_types(self):
        """Test safe_average with various mixed types."""
        result = safe_average([1, "text", 2, None, True, 3, [1, 2], {"key": "value"}])
        assert result == 2.0  # Should only average [1, 2, 3]
    
    def test_safe_average_with_single_value(self):
        """Test safe_average with a single value."""
        result = safe_average([5])
        assert result == 5.0
    
    def test_safe_average_with_negative_numbers(self):
        """Test safe_average with negative numbers."""
        result = safe_average([-1, -2, -3])
        assert result == -2.0
    
    def test_safe_average_with_zero(self):
        """Test safe_average with zeros."""
        result = safe_average([0, 0, 0])
        assert result == 0.0
    
    def test_safe_average_with_custom_default(self):
        """Test safe_average with custom default value."""
        result = safe_average([], default=100)
        assert result == 100
    
    def test_safe_average_with_large_numbers(self):
        """Test safe_average with large numbers."""
        result = safe_average([1000000, 2000000, 3000000])
        assert result == 2000000.0
