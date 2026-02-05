"""
Property-based tests for backward compatibility of fishertools enhancements.

Feature: fishertools-enhancements
Property 17: Legacy function compatibility

This module uses property-based testing to ensure that all existing
functionality continues to work correctly after adding enhancements.
"""

from __future__ import annotations

import pytest
from hypothesis import given, strategies as st, assume
from typing import Any


class TestLegacyFunctionCompatibilityProperties:
    """Property-based tests for legacy function compatibility.
    
    **Validates: Requirements 6.1, 6.2, 6.4**
    """
    
    @given(
        data=st.dictionaries(
            keys=st.text(min_size=1, max_size=20),
            values=st.one_of(
                st.integers(),
                st.floats(allow_nan=False, allow_infinity=False),
                st.text(),
                st.booleans(),
                st.none()
            ),
            min_size=1,
            max_size=10
        ),
        key=st.text(min_size=1, max_size=20)
    )
    def test_safe_get_behavior_unchanged(self, data: dict, key: str):
        """
        Property 17: Legacy function compatibility - safe_get
        
        For any dictionary and key, safe_get should return the value if present
        or None if absent, maintaining backward compatibility.
        
        **Validates: Requirements 6.1, 6.2, 6.4**
        """
        from fishertools import safe_get
        
        result = safe_get(data, key)
        
        if key in data:
            assert result == data[key], "safe_get should return the value for existing keys"
        else:
            assert result is None, "safe_get should return None for missing keys"
    
    @given(
        data=st.dictionaries(
            keys=st.text(min_size=1, max_size=20),
            values=st.one_of(
                st.integers(),
                st.floats(allow_nan=False, allow_infinity=False),
                st.text(),
                st.booleans()
            ),
            min_size=1,
            max_size=10
        ),
        key=st.text(min_size=1, max_size=20),
        default=st.one_of(st.integers(), st.text(), st.booleans())
    )
    def test_safe_get_with_default_unchanged(self, data: dict, key: str, default: Any):
        """
        Property 17: Legacy function compatibility - safe_get with default
        
        For any dictionary, key, and default value, safe_get should return
        the default when key is missing, maintaining backward compatibility.
        
        **Validates: Requirements 6.1, 6.2, 6.4**
        """
        from fishertools import safe_get
        
        result = safe_get(data, key, default=default)
        
        if key in data:
            assert result == data[key], "safe_get should return the value for existing keys"
        else:
            assert result == default, "safe_get should return default for missing keys"
    
    @given(
        a=st.floats(allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6),
        b=st.floats(allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6)
    )
    def test_safe_divide_behavior_unchanged(self, a: float, b: float):
        """
        Property 17: Legacy function compatibility - safe_divide
        
        For any two numbers, safe_divide should return the division result
        or None for division by zero or overflow, maintaining backward compatibility.
        
        **Validates: Requirements 6.1, 6.2, 6.4**
        """
        from fishertools import safe_divide
        import math
        
        result = safe_divide(a, b)
        
        if b == 0:
            assert result is None, "safe_divide should return None for division by zero"
        else:
            # Check if division would overflow
            try:
                expected = a / b
                if math.isinf(expected) or math.isnan(expected):
                    # Overflow case - safe_divide returns None
                    assert result is None, "safe_divide should return None for overflow"
                else:
                    assert result is not None, "safe_divide should return a value for non-zero divisor"
                    assert abs(result - expected) < 1e-9, "safe_divide should return correct division result"
            except (OverflowError, ZeroDivisionError):
                # Edge case - safe_divide should return None
                assert result is None, "safe_divide should return None for edge cases"
    
    @given(
        a=st.floats(allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6),
        b=st.floats(allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6),
        default=st.floats(allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6)
    )
    def test_safe_divide_with_default_unchanged(self, a: float, b: float, default: float):
        """
        Property 17: Legacy function compatibility - safe_divide with default
        
        For any two numbers and default value, safe_divide should return
        the default when dividing by zero or overflow, maintaining backward compatibility.
        
        **Validates: Requirements 6.1, 6.2, 6.4**
        """
        from fishertools import safe_divide
        import math
        
        result = safe_divide(a, b, default=default)
        
        if b == 0:
            assert result == default, "safe_divide should return default for division by zero"
        else:
            # Check if division would overflow
            try:
                expected = a / b
                if math.isinf(expected) or math.isnan(expected):
                    # Overflow case - safe_divide returns default
                    assert result == default, "safe_divide should return default for overflow"
                else:
                    # Use relative tolerance for large numbers
                    if abs(expected) > 1e-6:
                        assert abs(result - expected) / abs(expected) < 1e-6, "safe_divide should return correct division result"
                    else:
                        assert abs(result - expected) < 1e-6, "safe_divide should return correct division result"
            except (OverflowError, ZeroDivisionError):
                # Edge case - safe_divide should return default
                assert result == default, "safe_divide should return default for edge cases"
    
    @given(
        numbers=st.lists(
            st.floats(allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6),
            min_size=1,
            max_size=20
        )
    )
    def test_safe_max_behavior_unchanged(self, numbers: list):
        """
        Property 17: Legacy function compatibility - safe_max
        
        For any list of numbers, safe_max should return the maximum value,
        maintaining backward compatibility.
        
        **Validates: Requirements 6.1, 6.2, 6.4**
        """
        from fishertools import safe_max
        
        result = safe_max(numbers)
        expected = max(numbers)
        
        assert result == expected, "safe_max should return the maximum value"
    
    @given(
        numbers=st.lists(
            st.floats(allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6),
            min_size=1,
            max_size=20
        )
    )
    def test_safe_min_behavior_unchanged(self, numbers: list):
        """
        Property 17: Legacy function compatibility - safe_min
        
        For any list of numbers, safe_min should return the minimum value,
        maintaining backward compatibility.
        
        **Validates: Requirements 6.1, 6.2, 6.4**
        """
        from fishertools import safe_min
        
        result = safe_min(numbers)
        expected = min(numbers)
        
        assert result == expected, "safe_min should return the minimum value"
    
    @given(
        numbers=st.lists(
            st.floats(allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6),
            min_size=1,
            max_size=20
        )
    )
    def test_safe_sum_behavior_unchanged(self, numbers: list):
        """
        Property 17: Legacy function compatibility - safe_sum
        
        For any list of numbers, safe_sum should return the sum,
        maintaining backward compatibility.
        
        **Validates: Requirements 6.1, 6.2, 6.4**
        """
        from fishertools import safe_sum
        
        result = safe_sum(numbers)
        expected = sum(numbers)
        
        assert abs(result - expected) < 1e-6, "safe_sum should return the correct sum"
    
    @given(
        data=st.one_of(
            st.integers(),
            st.floats(allow_nan=False, allow_infinity=False),
            st.text(),
            st.booleans(),
            st.lists(st.integers(), max_size=10),
            st.dictionaries(st.text(max_size=10), st.integers(), max_size=5)
        )
    )
    def test_visualize_returns_string(self, data: Any):
        """
        Property 17: Legacy function compatibility - visualize
        
        For any data structure, visualize should return a non-empty string,
        maintaining backward compatibility.
        
        **Validates: Requirements 6.1, 6.2, 6.4**
        """
        from fishertools import visualize
        
        result = visualize(data)
        
        assert isinstance(result, str), "visualize should return a string"
        assert len(result) > 0, "visualize should return a non-empty string"
    
    @given(
        error_type=st.sampled_from([
            ValueError,
            TypeError,
            KeyError,
            IndexError,
            AttributeError,
            ZeroDivisionError,
        ]),
        message=st.text(min_size=1, max_size=100, alphabet=st.characters(blacklist_categories=('Cs',)))
    )
    def test_explain_error_returns_string(self, error_type: type, message: str):
        """
        Property 17: Legacy function compatibility - explain_error
        
        For any exception type and message, explain_error should return
        a non-empty string explanation when return_text=True, maintaining backward compatibility.
        
        **Validates: Requirements 6.1, 6.2, 6.4**
        """
        from fishertools import explain_error
        
        try:
            raise error_type(message)
        except Exception as e:
            # Use return_text=True to get the explanation as a string
            result = explain_error(e, return_text=True)
            
            assert isinstance(result, str), "explain_error should return a string when return_text=True"
            assert len(result) > 0, "explain_error should return a non-empty string"


class TestImportCompatibilityProperties:
    """Property-based tests for import compatibility.
    
    **Validates: Requirements 6.3**
    """
    
    def test_all_legacy_functions_importable(self):
        """
        Property 17: Legacy function compatibility - imports
        
        All legacy functions should be importable from the main module,
        maintaining backward compatibility.
        
        **Validates: Requirements 6.3**
        """
        legacy_functions = [
            "explain_error",
            "safe_get",
            "safe_divide",
            "safe_max",
            "safe_min",
            "safe_sum",
            "safe_read_file",
            "safe_write_file",
            "safe_file_exists",
            "safe_get_file_size",
            "safe_list_files",
            "visualize",
            "generate_example",
            "show_best_practice",
            "list_available_concepts",
            "list_available_topics",
            "ask_int",
            "ask_float",
            "ask_str",
            "ask_choice",
        ]
        
        import fishertools
        
        for func_name in legacy_functions:
            assert hasattr(fishertools, func_name), f"{func_name} should be importable"
            func = getattr(fishertools, func_name)
            assert callable(func), f"{func_name} should be callable"
    
    def test_all_legacy_modules_importable(self):
        """
        Property 17: Legacy function compatibility - module imports
        
        All legacy modules should be importable from the main module,
        maintaining backward compatibility.
        
        **Validates: Requirements 6.3**
        """
        legacy_modules = [
            "errors",
            "safe",
            "learn",
            "legacy",
            "input_utils",
            "utils",
            "decorators",
            "helpers",
        ]
        
        import fishertools
        
        for module_name in legacy_modules:
            assert hasattr(fishertools, module_name), f"{module_name} should be importable"
            module = getattr(fishertools, module_name)
            assert module is not None, f"{module_name} should not be None"
    
    def test_new_functions_available_alongside_legacy(self):
        """
        Property 17: Legacy function compatibility - new functions coexist
        
        New enhancement functions should be available alongside legacy functions
        without breaking existing imports.
        
        **Validates: Requirements 6.3, 6.4**
        """
        new_functions = [
            "safe_request",
            "safe_download",
            "translate_error",
            "detect_language",
            "get_version_info",
        ]
        
        import fishertools
        
        # Check new functions are available
        for func_name in new_functions:
            assert hasattr(fishertools, func_name), f"{func_name} should be importable"
            func = getattr(fishertools, func_name)
            assert callable(func), f"{func_name} should be callable"
        
        # Check legacy functions still work
        assert callable(fishertools.explain_error)
        assert callable(fishertools.safe_get)
        assert callable(fishertools.visualize)
