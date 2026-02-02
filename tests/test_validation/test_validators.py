"""Tests for validation functions."""

import pytest
from fishertools.validation import (
    validate_email,
    validate_url,
    validate_number,
    validate_string,
    validate_structure,
    ValidationError,
)


class TestValidateEmail:
    """Tests for email validation."""

    def test_valid_email(self):
        """Test valid email addresses."""
        validate_email("user@example.com")
        validate_email("test.user@example.co.uk")
        validate_email("user+tag@example.com")

    def test_invalid_email(self):
        """Test invalid email addresses."""
        with pytest.raises(ValidationError):
            validate_email("invalid-email")

        with pytest.raises(ValidationError):
            validate_email("user@")

        with pytest.raises(ValidationError):
            validate_email("@example.com")


class TestValidateUrl:
    """Tests for URL validation."""

    def test_valid_url(self):
        """Test valid URLs."""
        validate_url("https://example.com")
        validate_url("http://example.com")
        validate_url("https://sub.example.co.uk")

    def test_invalid_url(self):
        """Test invalid URLs."""
        with pytest.raises(ValidationError):
            validate_url("not-a-url")

        with pytest.raises(ValidationError):
            validate_url("ftp://example.com")

        with pytest.raises(ValidationError):
            validate_url("example.com")


class TestValidateNumber:
    """Tests for number validation."""

    def test_valid_number_in_range(self):
        """Test valid numbers in range."""
        assert validate_number(50, min_val=0, max_val=100) == 50.0
        assert validate_number(0, min_val=0, max_val=100) == 0.0
        assert validate_number(100, min_val=0, max_val=100) == 100.0

    def test_number_below_minimum(self):
        """Test number below minimum."""
        with pytest.raises(ValidationError):
            validate_number(-1, min_val=0, max_val=100)

    def test_number_above_maximum(self):
        """Test number above maximum."""
        with pytest.raises(ValidationError):
            validate_number(101, min_val=0, max_val=100)

    def test_number_without_limits(self):
        """Test number without limits."""
        assert validate_number(-1000) == -1000.0
        assert validate_number(1000000) == 1000000.0

    def test_string_input_raises_validation_error(self):
        """Test that string input raises ValidationError with descriptive message."""
        with pytest.raises(ValidationError) as exc_info:
            validate_number("string", 0, 100)
        
        error = exc_info.value
        assert "Expected number, got str" in str(error)
        assert error.value == "string"
        assert error.expected_type == "number"

    def test_none_input_raises_validation_error(self):
        """Test that None input raises ValidationError with specific message."""
        with pytest.raises(ValidationError) as exc_info:
            validate_number(None)
        
        error = exc_info.value
        assert "Value cannot be None" in str(error)
        assert error.value is None
        assert error.expected_type == "number"

    def test_numeric_string_conversion(self):
        """Test that numeric strings are converted properly."""
        assert validate_number("42", min_val=0, max_val=100) == 42.0
        assert validate_number("3.14") == 3.14

    def test_invalid_string_raises_validation_error(self):
        """Test that non-numeric strings raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            validate_number("not_a_number")
        
        error = exc_info.value
        assert "Expected number, got str" in str(error)
        assert error.value == "not_a_number"
        assert error.expected_type == "number"

    def test_list_input_raises_validation_error(self):
        """Test that list input raises ValidationError with descriptive message."""
        with pytest.raises(ValidationError) as exc_info:
            validate_number([1, 2, 3])
        
        error = exc_info.value
        assert "Expected number, got list" in str(error)
        assert error.value == [1, 2, 3]
        assert error.expected_type == "number"

    def test_exact_string_case_from_requirements(self):
        """Test the exact case mentioned in requirements: validate_number('string', 0, 100)."""
        with pytest.raises(ValidationError) as exc_info:
            validate_number("string", 0, 100)
        
        error = exc_info.value
        # Verify it returns ValidationError instead of comparison operator errors
        assert "Expected number, got str" in str(error)
        assert error.value == "string"
        assert error.expected_type == "number"
        # Ensure it's a ValidationError, not a TypeError from comparison operators
        assert isinstance(error, ValidationError)

    def test_none_with_range_parameters(self):
        """Test None value handling with range parameters."""
        with pytest.raises(ValidationError) as exc_info:
            validate_number(None, min_val=0, max_val=100)
        
        error = exc_info.value
        assert "Value cannot be None" in str(error)
        assert error.value is None
        assert error.expected_type == "number"

    def test_dict_input_raises_validation_error(self):
        """Test that dict input raises ValidationError with descriptive message."""
        with pytest.raises(ValidationError) as exc_info:
            validate_number({"key": "value"})
        
        error = exc_info.value
        assert "Expected number, got dict" in str(error)
        assert error.value == {"key": "value"}
        assert error.expected_type == "number"

    def test_boolean_input_handling(self):
        """Test that boolean input is handled properly (bools are numbers in Python)."""
        # In Python, bool is a subclass of int, so True/False should work
        assert validate_number(True) == 1.0
        assert validate_number(False) == 0.0
        assert validate_number(True, min_val=0, max_val=2) == 1.0


class TestValidateString:
    """Tests for string validation."""

    def test_valid_string_length(self):
        """Test valid string lengths."""
        validate_string("hello", min_length=3, max_length=10)
        validate_string("hi", min_length=2)
        validate_string("hello", max_length=10)

    def test_string_too_short(self):
        """Test string too short."""
        with pytest.raises(ValidationError):
            validate_string("hi", min_length=3)

    def test_string_too_long(self):
        """Test string too long."""
        with pytest.raises(ValidationError):
            validate_string("hello world", max_length=5)

    def test_string_pattern_match(self):
        """Test string pattern matching."""
        validate_string("123", pattern=r"^\d+$")

    def test_string_pattern_no_match(self):
        """Test string pattern not matching."""
        with pytest.raises(ValidationError):
            validate_string("abc", pattern=r"^\d+$")


class TestValidateStructure:
    """Tests for structure validation."""

    def test_valid_structure(self):
        """Test valid data structure."""
        schema = {"name": str, "age": int}
        data = {"name": "Alice", "age": 25}
        validate_structure(data, schema)

    def test_missing_key(self):
        """Test missing required key."""
        schema = {"name": str, "age": int}
        data = {"name": "Alice"}
        with pytest.raises(ValidationError):
            validate_structure(data, schema)

    def test_wrong_type(self):
        """Test wrong type in structure."""
        schema = {"name": str, "age": int}
        data = {"name": "Alice", "age": "twenty-five"}
        with pytest.raises(ValidationError):
            validate_structure(data, schema)

    def test_complex_structure(self):
        """Test complex structure validation."""
        schema = {"name": str, "age": int, "active": bool}
        data = {"name": "Alice", "age": 25, "active": True}
        validate_structure(data, schema)
