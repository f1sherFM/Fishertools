"""
Tests for v0.4.7 fixes.

Tests cover:
1. Generic types support in validators (Union, Optional, List)
2. Generic types support in type_checker decorator
3. get_explanation() function that returns string
4. Regex performance optimization in safe_format
"""

from __future__ import annotations

import pytest
import time
from typing import Union, Optional, List, Dict

from fishertools.validation import validate_structure, validate_types
from fishertools.validation.exceptions import ValidationError
from fishertools.errors import explain_error, get_explanation
from fishertools.safe import safe_format, PlaceholderBehavior


class TestGenericTypesInValidators:
    """Test generic types support in validate_structure."""

    def test_optional_type(self):
        """Test Optional[int] support."""
        schema = {"value": Optional[int]}
        
        # Should accept int
        validate_structure({"value": 42}, schema)
        
        # Should accept None
        validate_structure({"value": None}, schema)
        
        # Should reject string
        with pytest.raises(ValidationError):
            validate_structure({"value": "string"}, schema)

    def test_union_type(self):
        """Test Union[int, str] support."""
        schema = {"id": Union[int, str]}
        
        # Should accept int
        validate_structure({"id": 123}, schema)
        
        # Should accept str
        validate_structure({"id": "abc"}, schema)
        
        # Should reject float
        with pytest.raises(ValidationError):
            validate_structure({"id": 3.14}, schema)

    def test_list_type(self):
        """Test List[int] support."""
        schema = {"items": List[int]}
        
        # Should accept list of ints
        validate_structure({"items": [1, 2, 3]}, schema)
        
        # Should accept empty list
        validate_structure({"items": []}, schema)
        
        # Should reject list with non-ints
        with pytest.raises(ValidationError):
            validate_structure({"items": [1, "2", 3]}, schema)

    def test_dict_type(self):
        """Test Dict[str, int] support."""
        schema = {"mapping": Dict[str, int]}
        
        # Should accept correct dict
        validate_structure({"mapping": {"a": 1, "b": 2}}, schema)
        
        # Should reject dict with wrong value type
        with pytest.raises(ValidationError):
            validate_structure({"mapping": {"a": "1"}}, schema)

    def test_complex_nested_types(self):
        """Test complex nested generic types."""
        schema = {
            "data": Optional[List[Union[int, str]]],
            "metadata": Dict[str, Optional[int]]
        }
        
        # Should accept valid data
        validate_structure({
            "data": [1, "two", 3],
            "metadata": {"count": 5, "total": None}
        }, schema)
        
        # Should accept None for optional
        validate_structure({
            "data": None,
            "metadata": {}
        }, schema)


class TestGenericTypesInTypeChecker:
    """Test generic types support in @validate_types decorator."""

    def test_union_parameter(self):
        """Test Union type in function parameters."""
        @validate_types
        def process(value: Union[int, str]) -> str:
            return str(value)
        
        # Should accept int
        assert process(42) == "42"
        
        # Should accept str
        assert process("hello") == "hello"
        
        # Should reject float
        with pytest.raises(ValidationError):
            process(3.14)

    def test_optional_parameter(self):
        """Test Optional type in function parameters."""
        @validate_types
        def greet(name: Optional[str]) -> str:
            return f"Hello, {name or 'Guest'}!"
        
        # Should accept str
        assert greet("Alice") == "Hello, Alice!"
        
        # Should accept None
        assert greet(None) == "Hello, Guest!"
        
        # Should reject int
        with pytest.raises(ValidationError):
            greet(123)

    def test_list_parameter(self):
        """Test List type in function parameters."""
        @validate_types
        def sum_list(numbers: List[int]) -> int:
            return sum(numbers)
        
        # Should accept list of ints
        assert sum_list([1, 2, 3]) == 6
        
        # Should reject list with non-ints
        with pytest.raises(ValidationError):
            sum_list([1, "2", 3])

    def test_union_return_type(self):
        """Test Union type in return value."""
        @validate_types
        def get_value(key: str) -> Union[int, str, None]:
            values = {"a": 1, "b": "two"}
            return values.get(key)
        
        # Should accept int return
        assert get_value("a") == 1
        
        # Should accept str return
        assert get_value("b") == "two"
        
        # Should accept None return
        assert get_value("c") is None


class TestGetExplanationFunction:
    """Test get_explanation() function that returns string."""

    def test_returns_string(self):
        """Test that get_explanation returns a string."""
        try:
            1 / 0
        except Exception as e:
            result = get_explanation(e)
            assert isinstance(result, str)
            assert len(result) > 0

    def test_does_not_print(self, capsys):
        """Test that get_explanation doesn't print to stdout."""
        try:
            1 / 0
        except Exception as e:
            result = get_explanation(e)
            captured = capsys.readouterr()
            assert captured.out == ""  # Nothing printed
            assert len(result) > 0  # But string returned

    def test_explain_error_with_return_text(self):
        """Test explain_error with return_text=True."""
        try:
            1 / 0
        except Exception as e:
            result = explain_error(e, return_text=True)
            assert isinstance(result, str)
            assert len(result) > 0

    def test_explain_error_without_return_text(self, capsys):
        """Test explain_error without return_text prints."""
        try:
            1 / 0
        except Exception as e:
            result = explain_error(e, return_text=False)
            assert result is None  # Returns None
            captured = capsys.readouterr()
            assert len(captured.out) > 0  # But prints

    def test_get_explanation_with_different_formats(self):
        """Test get_explanation with different formats."""
        try:
            1 / 0
        except Exception as e:
            # Console format
            console = get_explanation(e, format_type='console')
            assert isinstance(console, str)
            
            # Plain format
            plain = get_explanation(e, format_type='plain')
            assert isinstance(plain, str)
            
            # JSON format
            json_str = get_explanation(e, format_type='json')
            assert isinstance(json_str, str)

    def test_can_save_to_file(self, tmp_path):
        """Test that explanation can be saved to file."""
        try:
            1 / 0
        except Exception as e:
            explanation = get_explanation(e)
            
            # Save to file
            log_file = tmp_path / "error.log"
            log_file.write_text(explanation, encoding='utf-8')
            
            # Read back
            content = log_file.read_text(encoding='utf-8')
            assert content == explanation


class TestRegexPerformance:
    """Test regex performance optimization in safe_format."""

    def test_compiled_pattern_used(self):
        """Test that compiled pattern is used (performance test)."""
        template = "Hello, {name}! You are {age} years old."
        
        # Warm up
        for _ in range(10):
            safe_format(template, {})
        
        # Measure performance
        iterations = 1000
        start = time.perf_counter()
        for _ in range(iterations):
            safe_format(template, {})
        elapsed = time.perf_counter() - start
        
        # Should be fast (< 0.1s for 1000 iterations)
        assert elapsed < 0.1, f"Too slow: {elapsed}s for {iterations} iterations"

    def test_pattern_reuse(self):
        """Test that pattern is reused across calls."""
        # Multiple calls should use same compiled pattern
        results = []
        for i in range(100):
            result = safe_format("Value: {x}", {})
            results.append(result)
        
        # All should have same result
        assert all(r == "Value: [MISSING: x]" for r in results)

    def test_no_performance_regression(self):
        """Test that there's no performance regression."""
        template = "User {name} ({id}) has {count} items"
        values = {"name": "Alice", "id": 123}
        
        # Should complete quickly even with many calls
        start = time.perf_counter()
        for _ in range(10000):
            safe_format(template, values)
        elapsed = time.perf_counter() - start
        
        # Should be very fast (< 1s for 10000 iterations)
        assert elapsed < 1.0, f"Performance regression: {elapsed}s"


class TestBackwardCompatibility:
    """Test that all fixes maintain backward compatibility."""

    def test_old_validate_structure_still_works(self):
        """Test that old usage of validate_structure still works."""
        schema = {"name": str, "age": int}
        validate_structure({"name": "Alice", "age": 25}, schema)
        
        with pytest.raises(ValidationError):
            validate_structure({"name": "Bob", "age": "thirty"}, schema)

    def test_old_validate_types_still_works(self):
        """Test that old usage of @validate_types still works."""
        @validate_types
        def add(a: int, b: int) -> int:
            return a + b
        
        assert add(1, 2) == 3
        
        with pytest.raises(ValidationError):
            add("1", 2)

    def test_old_explain_error_still_works(self, capsys):
        """Test that old usage of explain_error still works."""
        try:
            1 / 0
        except Exception as e:
            explain_error(e)
            captured = capsys.readouterr()
            assert len(captured.out) > 0

    def test_old_safe_format_still_works(self):
        """Test that old usage of safe_format still works."""
        result = safe_format("Hello, {name}!", {"name": "World"})
        assert result == "Hello, World!"
        
        result = safe_format("Hello, {name}!", {})
        assert result == "Hello, [MISSING: name]!"


class TestEdgeCases:
    """Test edge cases for all fixes."""

    def test_deeply_nested_generic_types(self):
        """Test deeply nested generic types."""
        schema = {
            "data": Optional[List[Dict[str, Union[int, str]]]]
        }
        
        validate_structure({
            "data": [
                {"a": 1, "b": "two"},
                {"c": 3, "d": "four"}
            ]
        }, schema)

    def test_empty_generic_types(self):
        """Test empty generic types."""
        schema = {
            "items": List[int],
            "mapping": Dict[str, str]
        }
        
        validate_structure({
            "items": [],
            "mapping": {}
        }, schema)

    def test_get_explanation_with_invalid_exception(self):
        """Test get_explanation with invalid input."""
        with pytest.raises(TypeError):
            get_explanation("not an exception")

    def test_safe_format_with_complex_placeholders(self):
        """Test safe_format with complex placeholders."""
        # With format specs
        result = safe_format("Value: {x:.2f}", {"x": 3.14159})
        assert result == "Value: 3.14"
        
        # With missing complex placeholder
        result = safe_format("Value: {x:.2f}", {})
        assert "[MISSING: x]" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
