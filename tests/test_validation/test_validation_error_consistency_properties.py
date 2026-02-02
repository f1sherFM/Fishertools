"""
Property-based tests for validation error consistency in fishertools.validation.

Tests the correctness properties of the validate_number function using hypothesis
for property-based testing.

**Feature: fishertools-bug-fixes, Property 2: Validation Error Consistency**
**Validates: Requirements 2.1, 2.4, 2.5**
"""

import pytest
from hypothesis import given, strategies as st, assume
from typing import Any

from fishertools.validation import validate_number, ValidationError


class TestValidationErrorConsistency:
    """
    Property 2: Validation Error Consistency
    
    For any non-numeric input to validate_number(), the system should raise 
    ValidationError with a descriptive message including both the actual and 
    expected types.
    
    **Feature: fishertools-bug-fixes, Property 2: Validation Error Consistency**
    **Validates: Requirements 2.1, 2.4, 2.5**
    """
    
    @given(
        non_numeric_value=st.one_of(
            st.text(),                    # strings (including non-numeric strings)
            st.lists(st.integers()),      # lists
            st.dictionaries(st.text(), st.integers()),  # dictionaries
            st.tuples(st.integers()),     # tuples
            st.sets(st.integers()),       # sets
            st.booleans(),                # booleans
            st.none(),                    # None values
            st.complex_numbers().filter(
                lambda x: not (x.real != x.real or x.imag != x.imag)  # Filter out NaN values
            ),                            # complex numbers
            st.binary(),                  # bytes
        ),
        min_val=st.one_of(st.none(), st.floats(allow_nan=False, allow_infinity=False, min_value=-1000, max_value=1000)),
        max_val=st.one_of(st.none(), st.floats(allow_nan=False, allow_infinity=False, min_value=-1000, max_value=1000))
    )
    def test_non_numeric_input_raises_validation_error_with_type_info(self, non_numeric_value, min_val, max_val):
        """
        Property test: For any non-numeric input, validate_number() should raise 
        ValidationError with descriptive message including actual and expected types.
        
        This test validates that the enhanced validate_number() implementation 
        provides clear, educational error messages for beginners.
        """
        # Skip numeric strings that can be converted to numbers
        if isinstance(non_numeric_value, str):
            try:
                float(non_numeric_value)
                assume(False)  # Skip numeric strings
            except (ValueError, TypeError):
                pass  # This is what we want to test - non-numeric strings
        
        # Skip actual numeric types (int, float)
        assume(not isinstance(non_numeric_value, (int, float)))
        
        # Ensure min_val <= max_val if both are provided
        if min_val is not None and max_val is not None:
            assume(min_val <= max_val)
        
        # The function should raise ValidationError for non-numeric inputs
        with pytest.raises(ValidationError) as exc_info:
            validate_number(non_numeric_value, min_val, max_val)
        
        error = exc_info.value
        error_message = str(error)
        
        # Verify the error has the expected structure and information
        assert isinstance(error, ValidationError), "Should raise ValidationError specifically"
        
        # Verify the error message contains type information
        if non_numeric_value is None:
            # Special case for None values
            assert "Value cannot be None" in error_message, f"Error message should mention None: {error_message}"
        else:
            # For other non-numeric types, should mention expected and actual types
            actual_type = type(non_numeric_value).__name__
            assert "Expected number" in error_message or "number" in error_message.lower(), \
                f"Error message should mention expected type 'number': {error_message}"
            assert actual_type in error_message, \
                f"Error message should mention actual type '{actual_type}': {error_message}"
        
        # Verify the error has the enhanced attributes
        assert hasattr(error, 'value'), "ValidationError should have 'value' attribute"
        assert hasattr(error, 'expected_type'), "ValidationError should have 'expected_type' attribute"
        
        # Verify the attributes contain correct information
        assert error.value == non_numeric_value, "Error should store the actual value that failed"
        assert error.expected_type == "number", "Error should indicate expected type as 'number'"
        
        # Verify the error message is educational and beginner-friendly
        assert len(error_message) > 10, "Error message should be descriptive"
        
        # Should not contain cryptic Python error messages
        cryptic_messages = [
            "unsupported operand type",
            "can't compare",
            "unorderable types",
            "'<' not supported",
            "'>' not supported"
        ]
        for cryptic in cryptic_messages:
            assert cryptic not in error_message.lower(), \
                f"Error message should not contain cryptic Python message '{cryptic}': {error_message}"
    
    @given(
        numeric_string=st.one_of(
            st.from_regex(r'^-?\d+$'),           # integers like "42", "-123"
            st.from_regex(r'^-?\d+\.\d+$'),      # decimals like "3.14", "-2.5"
            st.from_regex(r'^-?\d+\.?\d*[eE][+-]?\d+$')  # scientific notation like "1e5", "2.5E-3"
        ),
        min_val=st.one_of(st.none(), st.floats(allow_nan=False, allow_infinity=False, min_value=-1000, max_value=1000)),
        max_val=st.one_of(st.none(), st.floats(allow_nan=False, allow_infinity=False, min_value=-1000, max_value=1000))
    )
    def test_numeric_strings_do_not_raise_type_errors(self, numeric_string, min_val, max_val):
        """
        Property test: Numeric strings should be converted successfully, not raise type errors.
        
        This test validates that strings that can be converted to numbers are handled
        properly and don't trigger the type error path.
        """
        # Ensure min_val <= max_val if both are provided
        if min_val is not None and max_val is not None:
            assume(min_val <= max_val)
        
        # Skip strings that can't actually be converted to float
        try:
            expected_value = float(numeric_string)
        except (ValueError, OverflowError):
            assume(False)  # Skip strings that can't be converted
        
        # Skip infinite or NaN values
        assume(not (expected_value != expected_value or abs(expected_value) == float('inf')))
        
        try:
            result = validate_number(numeric_string, min_val, max_val)
            
            # Should return the converted numeric value
            assert isinstance(result, float), "Should return float for numeric strings"
            assert abs(result - expected_value) < 1e-10, "Should convert string to correct numeric value"
            
        except ValidationError as e:
            # If ValidationError is raised, it should be for range validation, not type validation
            error_message = str(e)
            
            # Should not be a type error
            assert "Expected number, got str" not in error_message, \
                f"Numeric string should not trigger type error: {error_message}"
            
            # Should be a range error if any error occurs
            if min_val is not None or max_val is not None:
                range_keywords = ["minimum", "maximum", "less than", "greater than", "between"]
                assert any(keyword in error_message.lower() for keyword in range_keywords), \
                    f"Error for numeric string should be range-related: {error_message}"
    
    @given(
        valid_number=st.one_of(
            st.integers(min_value=-1000, max_value=1000),
            st.floats(allow_nan=False, allow_infinity=False, min_value=-1000, max_value=1000)
        ),
        min_val=st.one_of(st.none(), st.floats(allow_nan=False, allow_infinity=False, min_value=-1000, max_value=1000)),
        max_val=st.one_of(st.none(), st.floats(allow_nan=False, allow_infinity=False, min_value=-1000, max_value=1000))
    )
    def test_valid_numbers_do_not_raise_type_errors(self, valid_number, min_val, max_val):
        """
        Property test: Valid numeric inputs should not raise type-related ValidationErrors.
        
        This test validates that actual numeric types (int, float) are handled correctly
        and only raise ValidationError for range issues, not type issues.
        """
        # Ensure min_val <= max_val if both are provided
        if min_val is not None and max_val is not None:
            assume(min_val <= max_val)
        
        try:
            result = validate_number(valid_number, min_val, max_val)
            
            # Should return the number as float
            assert isinstance(result, float), "Should return float for valid numbers"
            assert abs(result - float(valid_number)) < 1e-10, "Should preserve numeric value"
            
        except ValidationError as e:
            # If ValidationError is raised, it should be for range validation, not type validation
            error_message = str(e)
            
            # Should not be a type error
            type_error_messages = [
                "Expected number, got int",
                "Expected number, got float", 
                "Expected number, got"
            ]
            for type_msg in type_error_messages:
                assert type_msg not in error_message, \
                    f"Valid number should not trigger type error: {error_message}"
            
            # Should be a range error
            range_keywords = ["minimum", "maximum", "less than", "greater than", "between"]
            assert any(keyword in error_message.lower() for keyword in range_keywords), \
                f"Error for valid number should be range-related: {error_message}"
    
    @given(
        invalid_input=st.one_of(
            st.text().filter(lambda x: x and not x.strip()),  # whitespace-only strings
            st.text().filter(lambda x: x and not any(c.isdigit() for c in x)),  # non-numeric text
            st.lists(st.text()),  # lists of strings
            st.dictionaries(st.text(), st.text()),  # string dictionaries
        )
    )
    def test_error_message_consistency_across_input_types(self, invalid_input):
        """
        Property test: Error messages should be consistent in format across different input types.
        
        This test validates that all non-numeric inputs get consistent, well-formatted
        error messages that follow the same pattern.
        """
        with pytest.raises(ValidationError) as exc_info:
            validate_number(invalid_input)
        
        error = exc_info.value
        error_message = str(error)
        
        # All error messages should follow consistent format
        assert len(error_message) > 0, "Error message should not be empty"
        
        # Should contain type information in a consistent format
        actual_type = type(invalid_input).__name__
        
        # Should mention the expected type
        assert "number" in error_message.lower() or "Expected number" in error_message, \
            f"Error message should mention expected type: {error_message}"
        
        # Should mention the actual type
        assert actual_type in error_message, \
            f"Error message should mention actual type '{actual_type}': {error_message}"
        
        # Should be beginner-friendly (no technical jargon)
        technical_terms = [
            "TypeError", "ValueError", "AttributeError",
            "operand", "unorderable", "unsupported",
            "__lt__", "__gt__", "__eq__"
        ]
        for term in technical_terms:
            assert term not in error_message, \
                f"Error message should not contain technical term '{term}': {error_message}"
        
        # Verify enhanced error attributes are present and correct
        assert error.value == invalid_input, "Error should store the actual failing value"
        assert error.expected_type == "number", "Error should indicate expected type"
    
    def test_none_input_special_handling(self):
        """
        Test that None input gets special, clear error message.
        
        This validates the specific requirement for None value handling.
        """
        with pytest.raises(ValidationError) as exc_info:
            validate_number(None)
        
        error = exc_info.value
        error_message = str(error)
        
        # Should have specific message for None
        assert "Value cannot be None" in error_message, \
            f"None should get specific error message: {error_message}"
        
        # Should have correct attributes
        assert error.value is None, "Error should store None as the failing value"
        assert error.expected_type == "number", "Error should indicate expected type"
    
    @given(
        complex_input=st.complex_numbers().filter(
            lambda x: not (x.real != x.real or x.imag != x.imag)  # Filter out NaN values
        )
    )
    def test_complex_number_handling(self, complex_input):
        """
        Property test: Complex numbers should be handled with clear error messages.
        
        This test validates that complex numbers (which are numeric but not supported)
        get appropriate error messages.
        """
        with pytest.raises(ValidationError) as exc_info:
            validate_number(complex_input)
        
        error = exc_info.value
        error_message = str(error)
        
        # Should mention the type issue
        assert "complex" in error_message, \
            f"Error message should mention complex type: {error_message}"
        assert "number" in error_message.lower(), \
            f"Error message should mention expected type: {error_message}"
        
        # Should have correct attributes
        assert error.value == complex_input, "Error should store the complex number"
        assert error.expected_type == "number", "Error should indicate expected type"
    
    @given(
        non_numeric_value=st.one_of(
            st.text().filter(lambda x: x and len(x) > 0 and not _is_convertible_to_float(x)),
            st.lists(st.integers()),
            st.dictionaries(st.text(), st.integers())
        ),
        min_val=st.floats(allow_nan=False, allow_infinity=False, min_value=-100, max_value=100),
        max_val=st.floats(allow_nan=False, allow_infinity=False, min_value=-100, max_value=100)
    )
    def test_type_errors_occur_before_range_validation(self, non_numeric_value, min_val, max_val):
        """
        Property test: Type validation should occur before range validation.
        
        This test validates that when both type and range issues exist,
        the type error is reported first with clear messaging.
        """
        # Ensure min_val <= max_val
        if min_val > max_val:
            min_val, max_val = max_val, min_val
        
        with pytest.raises(ValidationError) as exc_info:
            validate_number(non_numeric_value, min_val, max_val)
        
        error = exc_info.value
        error_message = str(error)
        
        # Should be a type error, not a range error
        type_keywords = ["Expected number", "got", type(non_numeric_value).__name__]
        range_keywords = ["minimum", "maximum", "less than", "greater than"]
        
        # Should contain type-related keywords
        assert any(keyword in error_message for keyword in type_keywords), \
            f"Should be type error: {error_message}"
        
        # Should NOT contain range-related keywords
        assert not any(keyword in error_message for keyword in range_keywords), \
            f"Should not be range error when type is wrong: {error_message}"
        
        # Should have correct error attributes
        assert error.value == non_numeric_value, "Error should store the non-numeric value"
        assert error.expected_type == "number", "Error should indicate expected type"


def _is_convertible_to_float(s: str) -> bool:
    """Helper function to check if a string can be converted to float."""
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False