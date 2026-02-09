"""
Property-based tests for backward compatibility preservation.

Feature: fishertools-bug-fixes, Property 6: Backward Compatibility Preservation
For any existing fishertools API call with valid parameters, the function should 
continue to work with the same behavior as before the bug fixes.

**Validates: Requirements 6.1, 6.2, 6.3**
"""

import pytest
from hypothesis import given, strategies as st, assume, settings
from typing import Any

# Import modules to test
from fishertools.validation import ValidationError, validate_number, validate_email, validate_url
from fishertools.safe import safe_get, safe_divide, safe_max, safe_min, safe_sum, safe_average
from fishertools.safe import safe_format, PlaceholderBehavior
from fishertools.debug import debug_step_by_step, trace, set_breakpoint


def _is_numeric_string(value: str) -> bool:
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


class TestBackwardCompatibilityPreservation:
    """
    Property 6: Backward Compatibility Preservation
    
    For any existing fishertools API call with valid parameters, the function 
    should continue to work with the same behavior as before the bug fixes.
    
    **Validates: Requirements 6.1, 6.2, 6.3**
    """
    
    @given(
        value=st.one_of(st.integers(), st.floats(allow_nan=False, allow_infinity=False)),
        min_val=st.one_of(st.none(), st.floats(allow_nan=False, allow_infinity=False)),
        max_val=st.one_of(st.none(), st.floats(allow_nan=False, allow_infinity=False))
    )
    @settings(max_examples=100)
    def test_validate_number_preserves_behavior(self, value, min_val, max_val):
        """Property: validate_number returns float for valid numeric inputs."""
        # Skip invalid ranges
        if min_val is not None and max_val is not None and min_val > max_val:
            assume(False)
        
        # Skip values outside range
        if min_val is not None and value < min_val:
            assume(False)
        if max_val is not None and value > max_val:
            assume(False)
        
        # Property: Should return a float for valid inputs
        result = validate_number(value, min_val, max_val)
        assert isinstance(result, float)
        assert result == float(value)
    
    @given(
        value=st.one_of(
            st.text().filter(lambda s: not _is_numeric_string(s)),
            st.none(),
            st.lists(st.integers())
        )
    )
    @settings(max_examples=100)
    def test_validate_number_raises_validation_error_for_invalid_types(self, value):
        """Property: validate_number raises ValidationError for non-numeric types."""
        # Property: Should raise ValidationError for invalid types
        with pytest.raises(ValidationError) as exc_info:
            validate_number(value)
        
        # Property: Error should be catchable as Exception
        assert isinstance(exc_info.value, Exception)
        
        # Property: Error message should be descriptive
        error_msg = str(exc_info.value)
        assert len(error_msg) > 0
    
    @given(
        a=st.floats(allow_nan=False, allow_infinity=False, min_value=-1e100, max_value=1e100),
        b=st.floats(allow_nan=False, allow_infinity=False, min_value=-1e100, max_value=1e100).filter(lambda x: abs(x) > 1e-100),
        default=st.one_of(st.none(), st.floats(allow_nan=False, allow_infinity=False))
    )
    @settings(max_examples=100)
    def test_safe_divide_preserves_behavior_for_valid_inputs(self, a, b, default):
        """Property: safe_divide returns correct division result for non-zero divisor."""
        result = safe_divide(a, b, default)
        
        # Property: Should return a numeric result (or None if default is None and result is inf/nan)
        if result is not None:
            assert isinstance(result, (int, float))
            
            # Property: Result should be mathematically correct (if not infinity)
            expected = a / b
            import math
            if not math.isinf(expected) and not math.isnan(expected):
                assert abs(result - expected) < 1e-10  # Allow for floating point precision
    
    @given(
        a=st.floats(allow_nan=False, allow_infinity=False),
        default=st.one_of(st.none(), st.floats(allow_nan=False, allow_infinity=False))
    )
    @settings(max_examples=100)
    def test_safe_divide_by_zero_returns_default(self, a, default):
        """Property: safe_divide returns default when dividing by zero."""
        result = safe_divide(a, 0, default)
        
        # Property: Should return the default value
        assert result == default
    
    @given(
        data=st.dictionaries(st.text(min_size=1), st.integers()),
        key=st.text(min_size=1),
        default=st.one_of(st.none(), st.integers())
    )
    @settings(max_examples=100)
    def test_safe_get_dict_preserves_behavior(self, data, key, default):
        """Property: safe_get returns value or default for dictionaries."""
        result = safe_get(data, key, default)
        
        if key in data:
            # Property: Should return the actual value if key exists
            assert result == data[key]
        else:
            # Property: Should return default if key doesn't exist
            assert result == default
    
    @given(
        lst=st.lists(st.integers(), min_size=1, max_size=20),
        index=st.integers(min_value=-50, max_value=50),
        default=st.one_of(st.none(), st.integers())
    )
    @settings(max_examples=100)
    def test_safe_get_list_preserves_behavior(self, lst, index, default):
        """Property: safe_get returns value or default for lists."""
        result = safe_get(lst, index, default)
        
        if -len(lst) <= index < len(lst):
            # Property: Should return the actual value if index is valid
            assert result == lst[index]
        else:
            # Property: Should return default if index is out of range
            assert result == default
    
    @given(
        numbers=st.lists(st.floats(allow_nan=False, allow_infinity=False, min_value=-1e100, max_value=1e100), min_size=1, max_size=20),
        default=st.floats(allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_safe_average_preserves_behavior(self, numbers, default):
        """Property: safe_average calculates correct average for valid numbers."""
        result = safe_average(numbers, default)
        
        # Property: Should return a float
        assert isinstance(result, float)
        
        # Property: Result should be mathematically correct
        expected = sum(numbers) / len(numbers)
        import math
        # Handle potential overflow in sum
        if not math.isinf(expected) and not math.isnan(expected):
            assert abs(result - expected) < 1e-10
    
    @given(
        numbers=st.lists(
            st.one_of(
                st.floats(allow_nan=False, allow_infinity=False, min_value=-1e100, max_value=1e100),
                st.text(),
                st.none()
            ),
            min_size=1,
            max_size=20
        ),
        default=st.floats(allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_safe_average_filters_non_numeric(self, numbers, default):
        """Property: safe_average filters out non-numeric values."""
        result = safe_average(numbers, default)
        
        # Property: Should return a float
        assert isinstance(result, float)
        
        # Filter to get valid numbers
        valid_numbers = [n for n in numbers if isinstance(n, (int, float)) and not isinstance(n, bool)]
        
        if valid_numbers:
            # Property: Result should be average of valid numbers
            expected = sum(valid_numbers) / len(valid_numbers)
            import math
            # Handle potential overflow in sum
            if not math.isinf(expected) and not math.isnan(expected):
                assert abs(result - expected) < 1e-10
        else:
            # Property: Should return default if no valid numbers
            assert result == default
    
    @given(
        template=st.text(min_size=1, max_size=50),
        values=st.dictionaries(st.text(min_size=1, max_size=10), st.text(max_size=20))
    )
    @settings(max_examples=100)
    def test_safe_format_preserves_behavior(self, template, values):
        """Property: safe_format returns a string result."""
        result = safe_format(template, values)
        
        # Property: Should return a string
        assert isinstance(result, str)
        
        # Property: Result should not be empty if template is not empty
        if template:
            assert len(result) > 0
    
    @given(
        numbers=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1, max_size=20),
        default=st.one_of(st.none(), st.floats(allow_nan=False, allow_infinity=False))
    )
    @settings(max_examples=100)
    def test_safe_max_preserves_behavior(self, numbers, default):
        """Property: safe_max returns maximum value."""
        result = safe_max(numbers, default)
        
        # Property: Should return the maximum value
        expected = max(numbers)
        assert result == expected
    
    @given(
        numbers=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1, max_size=20),
        default=st.one_of(st.none(), st.floats(allow_nan=False, allow_infinity=False))
    )
    @settings(max_examples=100)
    def test_safe_min_preserves_behavior(self, numbers, default):
        """Property: safe_min returns minimum value."""
        result = safe_min(numbers, default)
        
        # Property: Should return the minimum value
        expected = min(numbers)
        assert result == expected
    
    @given(
        numbers=st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1, max_size=20),
        default=st.floats(allow_nan=False, allow_infinity=False)
    )
    @settings(max_examples=100)
    def test_safe_sum_preserves_behavior(self, numbers, default):
        """Property: safe_sum returns correct sum."""
        result = safe_sum(numbers, default)
        
        # Property: Should return the sum
        expected = sum(numbers)
        assert result == expected
    
    def test_validation_error_exception_hierarchy_preserved(self):
        """Property: ValidationError maintains exception hierarchy."""
        # Property: ValidationError should be an Exception
        assert issubclass(ValidationError, Exception)
        
        # Property: ValidationError instances should be catchable as Exception
        try:
            raise ValidationError("Test")
        except Exception as e:
            assert isinstance(e, ValidationError)
    
    @given(
        message=st.text(min_size=1, max_size=100),
        value=st.one_of(st.none(), st.integers(), st.text()),
        expected_type=st.one_of(st.none(), st.text(min_size=1, max_size=20))
    )
    @settings(max_examples=100)
    def test_validation_error_attributes_preserved(self, message, value, expected_type):
        """Property: ValidationError preserves all attributes."""
        error = ValidationError(message, value=value, expected_type=expected_type)
        
        # Property: Should have message
        assert str(error) == message
        
        # Property: Should have value attribute
        assert error.value == value
        
        # Property: Should have expected_type attribute
        assert error.expected_type == expected_type
    
    def test_debug_decorators_preserve_function_behavior(self):
        """Property: Debug decorators preserve function behavior."""
        
        @debug_step_by_step
        def add(a, b):
            return a + b
        
        @trace
        def multiply(a, b):
            return a * b
        
        # Property: Decorated functions should return correct results
        assert add(2, 3) == 5
        assert multiply(4, 5) == 20
        
        # Property: Function names should be preserved
        assert add.__name__ == "add"
        assert multiply.__name__ == "multiply"
    
    @given(
        behavior=st.sampled_from([PlaceholderBehavior.PRESERVE, PlaceholderBehavior.MISSING, PlaceholderBehavior.EMPTY])
    )
    @settings(max_examples=50)
    def test_placeholder_behavior_enum_preserved(self, behavior):
        """Property: PlaceholderBehavior enum values work with safe_format."""
        template = "Hello {name}"
        values = {}
        
        # Property: Should not raise an error
        result = safe_format(template, values, behavior=behavior)
        
        # Property: Should return a string
        assert isinstance(result, str)
        
        # Property: Behavior should affect output
        if behavior == PlaceholderBehavior.PRESERVE:
            assert "{name}" in result
        elif behavior == PlaceholderBehavior.MISSING:
            assert "MISSING" in result or "name" in result
        elif behavior == PlaceholderBehavior.EMPTY:
            assert "{name}" not in result
