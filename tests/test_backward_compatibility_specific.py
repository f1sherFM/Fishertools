"""
Specific backward compatibility test cases.

Feature: fishertools-bug-fixes
Tests specific backward compatibility scenarios mentioned in requirements.

**Validates: Requirements 6.4, 6.5**
"""

import pytest
import sys
from io import StringIO

# Import modules to test
from fishertools.validation import ValidationError, validate_number
from fishertools.safe import safe_get, safe_divide, safe_format, safe_average
from fishertools.debug import debug_step_by_step, trace


class TestValidationErrorCatching:
    """Test that existing ValidationError catching still works.
    
    Validates: Requirement 6.5
    """
    
    def test_existing_validation_error_catching_pattern_1(self):
        """Test common pattern: try-except with ValidationError."""
        # This is a common pattern in existing user code
        try:
            validate_number("not a number")
            assert False, "Should have raised ValidationError"
        except ValidationError as e:
            # User code should be able to access error message
            assert str(e)  # Should have a message
            assert isinstance(e, Exception)  # Should be an Exception
    
    def test_existing_validation_error_catching_pattern_2(self):
        """Test pattern: catching as generic Exception."""
        # Some users might catch as generic Exception
        caught = False
        try:
            validate_number(None)
        except Exception as e:
            caught = True
            # Should still be a ValidationError
            assert isinstance(e, ValidationError)
        
        assert caught
    
    def test_existing_validation_error_catching_pattern_3(self):
        """Test pattern: multiple except blocks."""
        # Users might have multiple except blocks
        validation_error_caught = False
        generic_error_caught = False
        
        try:
            validate_number([1, 2, 3])
        except ValidationError:
            validation_error_caught = True
        except Exception:
            generic_error_caught = True
        
        # Should catch as ValidationError, not generic Exception
        assert validation_error_caught
        assert not generic_error_caught
    
    def test_validation_error_attributes_accessible(self):
        """Test that ValidationError attributes are accessible."""
        try:
            validate_number("string", 0, 100)
        except ValidationError as e:
            # Users should be able to access these attributes
            assert hasattr(e, 'value')
            assert hasattr(e, 'expected_type')
            # Message should be in string representation
            assert "str" in str(e) or "string" in str(e).lower()
    
    def test_validation_error_with_custom_message(self):
        """Test that custom ValidationError messages work."""
        custom_message = "Custom validation error"
        error = ValidationError(custom_message)
        
        # Should preserve the message
        assert str(error) == custom_message
        
        # Should be catchable
        with pytest.raises(ValidationError) as exc_info:
            raise error
        
        assert str(exc_info.value) == custom_message


class TestExistingFunctionSignatures:
    """Test that existing function signatures are preserved.
    
    Validates: Requirement 6.4
    """
    
    def test_validate_number_with_positional_args(self):
        """Test validate_number works with positional arguments."""
        # Old code might use positional args
        result = validate_number(42, 0, 100)
        assert result == 42.0
    
    def test_validate_number_with_keyword_args(self):
        """Test validate_number works with keyword arguments."""
        # Old code might use keyword args
        result = validate_number(value=42, min_val=0, max_val=100)
        assert result == 42.0
    
    def test_validate_number_with_mixed_args(self):
        """Test validate_number works with mixed arguments."""
        # Old code might mix positional and keyword args
        result = validate_number(42, min_val=0, max_val=100)
        assert result == 42.0
    
    def test_safe_divide_with_two_args(self):
        """Test safe_divide works with just two arguments."""
        # Old code might not specify default
        result = safe_divide(10, 2)
        assert result == 5.0
    
    def test_safe_divide_with_three_args(self):
        """Test safe_divide works with all three arguments."""
        # Old code might specify default
        result = safe_divide(10, 0, 0)
        assert result == 0
    
    def test_safe_get_with_two_args(self):
        """Test safe_get works with just collection and key."""
        # Old code might not specify default
        data = {"name": "Alice"}
        result = safe_get(data, "name")
        assert result == "Alice"
    
    def test_safe_get_with_three_args(self):
        """Test safe_get works with all three arguments."""
        # Old code might specify default
        data = {"name": "Alice"}
        result = safe_get(data, "age", 0)
        assert result == 0
    
    def test_safe_format_with_dict(self):
        """Test safe_format works with dictionary values."""
        # Old code uses dict for values
        result = safe_format("Hello {name}", {"name": "World"})
        assert result == "Hello World"
    
    def test_safe_format_with_kwargs(self):
        """Test safe_format works with keyword arguments."""
        # Old code might use kwargs
        result = safe_format("Hello {name}", name="World")
        assert result == "Hello World"
    
    def test_safe_average_with_list(self):
        """Test safe_average works with just a list."""
        # Old code might not specify default
        result = safe_average([1, 2, 3])
        assert result == 2.0
    
    def test_safe_average_with_default(self):
        """Test safe_average works with default parameter."""
        # Old code might specify default
        result = safe_average([], default=0)
        assert result == 0


class TestDebugDecoratorsCompatibility:
    """Test that debug decorators work with existing code patterns.
    
    Validates: Requirement 6.4
    """
    
    def test_debug_step_by_step_with_simple_function(self):
        """Test debug_step_by_step works with simple functions."""
        @debug_step_by_step
        def add(a, b):
            return a + b
        
        # Should work and return correct result
        result = add(2, 3)
        assert result == 5
    
    def test_debug_step_by_step_with_multiple_statements(self):
        """Test debug_step_by_step works with multiple statements."""
        @debug_step_by_step
        def calculate(x):
            y = x * 2
            z = y + 10
            return z
        
        result = calculate(5)
        assert result == 20
    
    def test_trace_with_recursive_function(self):
        """Test trace works with recursive functions."""
        @trace
        def factorial(n):
            if n <= 1:
                return 1
            return n * factorial(n - 1)
        
        result = factorial(3)
        assert result == 6
    
    def test_trace_with_nested_calls(self):
        """Test trace works with nested function calls."""
        @trace
        def outer(x):
            def inner(y):
                return y * 2
            return inner(x) + 1
        
        result = outer(5)
        assert result == 11
    
    def test_decorated_function_can_be_called_multiple_times(self):
        """Test decorated functions can be called multiple times."""
        @debug_step_by_step
        def multiply(a, b):
            return a * b
        
        # Should work multiple times
        assert multiply(2, 3) == 6
        assert multiply(4, 5) == 20
        assert multiply(0, 10) == 0


class TestBackwardCompatibleBehavior:
    """Test that behavior remains consistent with previous versions.
    
    Validates: Requirement 6.5
    """
    
    def test_safe_divide_by_zero_behavior(self):
        """Test safe_divide behavior with zero divisor."""
        # Default behavior should return None (mathematically correct)
        result = safe_divide(10, 0)
        assert result is None
        
        # With explicit default, should return that default
        result = safe_divide(10, 0, default=0)
        assert result == 0
    
    def test_safe_get_missing_key_behavior(self):
        """Test safe_get behavior with missing keys."""
        data = {"name": "Alice"}
        
        # Without default, should return None
        result = safe_get(data, "age")
        assert result is None
        
        # With default, should return default
        result = safe_get(data, "age", default=0)
        assert result == 0
    
    def test_safe_average_empty_list_behavior(self):
        """Test safe_average behavior with empty list."""
        # Default behavior should return 0
        result = safe_average([])
        assert result == 0
        
        # With explicit default, should return that default
        result = safe_average([], default=-1)
        assert result == -1
    
    def test_validate_number_type_error_behavior(self):
        """Test validate_number raises ValidationError for wrong types."""
        # Should raise ValidationError, not TypeError
        with pytest.raises(ValidationError):
            validate_number("string")
        
        with pytest.raises(ValidationError):
            validate_number(None)
        
        with pytest.raises(ValidationError):
            validate_number([1, 2, 3])
    
    def test_validate_number_range_error_behavior(self):
        """Test validate_number raises ValidationError for out of range."""
        # Should raise ValidationError for out of range values
        with pytest.raises(ValidationError):
            validate_number(150, min_val=0, max_val=100)
        
        with pytest.raises(ValidationError):
            validate_number(-10, min_val=0, max_val=100)
    
    def test_safe_format_missing_placeholder_behavior(self):
        """Test safe_format behavior with missing placeholders."""
        # Should handle missing placeholders gracefully
        result = safe_format("Hello {name}", {})
        
        # Should return a string (not raise an error)
        assert isinstance(result, str)
        
        # Should indicate the missing placeholder somehow
        assert "name" in result or "MISSING" in result


class TestExceptionHierarchyPreservation:
    """Test that exception hierarchy is preserved.
    
    Validates: Requirement 6.5
    """
    
    def test_validation_error_is_exception(self):
        """Test ValidationError is an Exception."""
        assert issubclass(ValidationError, Exception)
    
    def test_validation_error_is_base_exception(self):
        """Test ValidationError is a BaseException."""
        assert issubclass(ValidationError, BaseException)
    
    def test_validation_error_can_be_raised(self):
        """Test ValidationError can be raised."""
        with pytest.raises(ValidationError):
            raise ValidationError("Test error")
    
    def test_validation_error_can_be_caught_as_exception(self):
        """Test ValidationError can be caught as Exception."""
        caught = False
        try:
            raise ValidationError("Test error")
        except Exception:
            caught = True
        
        assert caught
    
    def test_validation_error_preserves_traceback(self):
        """Test ValidationError preserves traceback information."""
        try:
            validate_number("invalid")
        except ValidationError:
            # Should have traceback information
            import traceback
            tb = traceback.format_exc()
            assert "ValidationError" in tb
            assert "validate_number" in tb
