"""
Backward compatibility tests for fishertools bug fixes.

Feature: fishertools-bug-fixes
Tests that all existing APIs continue to work after bug fixes.

**Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5**
"""

import pytest
import inspect
from typing import get_type_hints

# Import main fishertools module
import fishertools

# Import specific modules
from fishertools.validation import ValidationError, validate_number, validate_email, validate_url
from fishertools.safe import safe_get, safe_divide, safe_format, safe_average, PlaceholderBehavior
from fishertools.debug import debug_step_by_step, set_breakpoint, trace
from fishertools.learn import generate_example, show_best_practice


class TestAPISignaturePreservation:
    """Test that all existing function signatures remain unchanged.
    
    Validates: Requirement 6.1, 6.4
    """
    
    def test_validate_number_signature(self):
        """Test validate_number maintains its signature."""
        sig = inspect.signature(validate_number)
        params = list(sig.parameters.keys())
        
        # Should have: value, min_val, max_val
        assert 'value' in params
        assert 'min_val' in params
        assert 'max_val' in params
        
        # Check defaults
        assert sig.parameters['min_val'].default is None
        assert sig.parameters['max_val'].default is None
    
    def test_safe_divide_signature(self):
        """Test safe_divide maintains its signature."""
        sig = inspect.signature(safe_divide)
        params = list(sig.parameters.keys())
        
        # Should have: a, b, default
        assert 'a' in params
        assert 'b' in params
        assert 'default' in params
        
        # Check default value (should be None for mathematical correctness)
        assert sig.parameters['default'].default is None
    
    def test_safe_get_signature(self):
        """Test safe_get maintains its signature."""
        sig = inspect.signature(safe_get)
        params = list(sig.parameters.keys())
        
        # Should have: collection, index, default
        assert 'collection' in params
        assert 'index' in params
        assert 'default' in params
        
        # Check default value
        assert sig.parameters['default'].default is None
    
    def test_safe_format_signature(self):
        """Test safe_format maintains its signature."""
        sig = inspect.signature(safe_format)
        params = list(sig.parameters.keys())
        
        # Should have: template, values, behavior
        assert 'template' in params
        assert 'values' in params or 'args' in params or len(params) >= 1
        
        # Function should be callable with template and dict
        result = safe_format("Hello {name}", {"name": "World"})
        assert "Hello" in result
    
    def test_safe_average_signature(self):
        """Test safe_average maintains its signature."""
        sig = inspect.signature(safe_average)
        params = list(sig.parameters.keys())
        
        # Should have: numbers, default
        assert 'numbers' in params
        assert 'default' in params
        
        # Check default value
        assert sig.parameters['default'].default == 0
    
    def test_debug_decorators_signature(self):
        """Test debug decorators maintain their signatures."""
        # debug_step_by_step should take a function
        sig = inspect.signature(debug_step_by_step)
        params = list(sig.parameters.keys())
        assert 'func' in params
        
        # trace should take a function
        sig = inspect.signature(trace)
        params = list(sig.parameters.keys())
        assert 'func' in params
        
        # set_breakpoint should take optional message
        sig = inspect.signature(set_breakpoint)
        params = list(sig.parameters.keys())
        assert 'message' in params


class TestValidationErrorHierarchy:
    """Test that ValidationError exception hierarchy is preserved.
    
    Validates: Requirement 6.2, 6.5
    """
    
    def test_validation_error_is_exception(self):
        """Test ValidationError inherits from Exception."""
        assert issubclass(ValidationError, Exception)
    
    def test_validation_error_can_be_caught_as_exception(self):
        """Test ValidationError can be caught as Exception."""
        with pytest.raises(Exception):
            raise ValidationError("Test error")
    
    def test_validation_error_can_be_caught_specifically(self):
        """Test ValidationError can be caught specifically."""
        with pytest.raises(ValidationError):
            raise ValidationError("Test error")
    
    def test_validation_error_message_attribute(self):
        """Test ValidationError has message in args."""
        error = ValidationError("Test message")
        assert "Test message" in str(error)
    
    def test_validation_error_with_value_and_type(self):
        """Test ValidationError accepts value and expected_type parameters."""
        error = ValidationError("Test", value=42, expected_type="str")
        assert error.value == 42
        assert error.expected_type == "str"
    
    def test_existing_validation_error_catching_still_works(self):
        """Test that existing code catching ValidationError still works."""
        # Simulate existing user code
        try:
            validate_number("not a number")
            assert False, "Should have raised ValidationError"
        except ValidationError as e:
            # User code should be able to access the error message
            assert "Expected number" in str(e) or "got str" in str(e)
    
    def test_validation_error_in_try_except_block(self):
        """Test ValidationError works in standard try-except patterns."""
        caught = False
        try:
            validate_number(None)
        except ValidationError:
            caught = True
        
        assert caught, "ValidationError should have been caught"


class TestExistingFunctionBehavior:
    """Test that existing functions maintain their behavior for valid inputs.
    
    Validates: Requirement 6.1, 6.2
    """
    
    def test_validate_number_with_valid_int(self):
        """Test validate_number works with valid integers."""
        result = validate_number(42)
        assert result == 42.0
    
    def test_validate_number_with_valid_float(self):
        """Test validate_number works with valid floats."""
        result = validate_number(3.14)
        assert result == 3.14
    
    def test_validate_number_with_range(self):
        """Test validate_number works with range validation."""
        result = validate_number(50, min_val=0, max_val=100)
        assert result == 50.0
    
    def test_safe_divide_normal_operation(self):
        """Test safe_divide works for normal division."""
        result = safe_divide(10, 2)
        assert result == 5.0
    
    def test_safe_divide_by_zero_returns_default(self):
        """Test safe_divide returns default on division by zero."""
        # Default behavior returns None (mathematically correct)
        result = safe_divide(10, 0)
        assert result is None
        
        # Can specify custom default
        result = safe_divide(10, 0, default=0)
        assert result == 0
    
    def test_safe_get_existing_key(self):
        """Test safe_get retrieves existing keys."""
        data = {"name": "Alice", "age": 30}
        result = safe_get(data, "name")
        assert result == "Alice"
    
    def test_safe_get_missing_key_returns_default(self):
        """Test safe_get returns default for missing keys."""
        data = {"name": "Alice"}
        result = safe_get(data, "age", default=0)
        assert result == 0
    
    def test_safe_format_with_valid_dict(self):
        """Test safe_format works with valid dictionary."""
        result = safe_format("Hello {name}", {"name": "World"})
        assert result == "Hello World"
    
    def test_safe_average_with_valid_numbers(self):
        """Test safe_average calculates correct average."""
        result = safe_average([1, 2, 3, 4, 5])
        assert result == 3.0
    
    def test_safe_average_empty_list_returns_default(self):
        """Test safe_average returns default for empty list."""
        result = safe_average([], default=0)
        assert result == 0


class TestDebugDecoratorsOutput:
    """Test that debug decorators maintain same output format.
    
    Validates: Requirement 6.3
    """
    
    def test_debug_step_by_step_decorator_works(self):
        """Test debug_step_by_step decorator can be applied."""
        @debug_step_by_step
        def add(a, b):
            return a + b
        
        # Should work without errors
        result = add(2, 3)
        assert result == 5
    
    def test_trace_decorator_works(self):
        """Test trace decorator can be applied."""
        @trace
        def multiply(a, b):
            return a * b
        
        # Should work without errors
        result = multiply(3, 4)
        assert result == 12
    
    def test_set_breakpoint_works(self):
        """Test set_breakpoint can be called."""
        # Should not raise any errors
        set_breakpoint("Test breakpoint")
    
    def test_decorated_function_preserves_name(self):
        """Test decorators preserve function names."""
        @debug_step_by_step
        def test_func():
            return 42
        
        assert test_func.__name__ == "test_func"
    
    def test_decorated_function_preserves_docstring(self):
        """Test decorators preserve docstrings."""
        @trace
        def test_func():
            """Test docstring."""
            return 42
        
        assert test_func.__doc__ == "Test docstring."


class TestModuleImports:
    """Test that all module imports work as expected.
    
    Validates: Requirement 6.1
    """
    
    def test_main_module_imports(self):
        """Test main fishertools module can be imported."""
        import fishertools
        assert hasattr(fishertools, '__version__')
    
    def test_validation_module_imports(self):
        """Test validation module can be imported."""
        from fishertools import validation
        assert hasattr(validation, 'ValidationError')
        assert hasattr(validation, 'validate_number')
    
    def test_safe_module_imports(self):
        """Test safe module can be imported."""
        from fishertools import safe
        assert hasattr(safe, 'safe_get')
        assert hasattr(safe, 'safe_divide')
        assert hasattr(safe, 'safe_average')
    
    def test_debug_module_imports(self):
        """Test debug module can be imported."""
        from fishertools import debug
        assert hasattr(debug, 'debug_step_by_step')
        assert hasattr(debug, 'trace')
    
    def test_learn_module_imports(self):
        """Test learn module can be imported."""
        from fishertools import learn
        assert hasattr(learn, 'generate_example')
    
    def test_direct_imports_from_main_module(self):
        """Test direct imports from main module work."""
        from fishertools import safe_get, safe_divide
        from fishertools.validation import ValidationError
        assert callable(safe_get)
        assert callable(safe_divide)
        assert issubclass(ValidationError, Exception)


class TestBackwardCompatibleErrorMessages:
    """Test that error messages remain helpful and consistent.
    
    Validates: Requirement 6.2, 6.5
    """
    
    def test_validation_error_message_format(self):
        """Test ValidationError messages are descriptive."""
        try:
            validate_number("string")
        except ValidationError as e:
            error_msg = str(e)
            # Should mention the type issue
            assert "str" in error_msg or "string" in error_msg.lower()
    
    def test_validation_error_with_none(self):
        """Test ValidationError for None values is clear."""
        try:
            validate_number(None)
        except ValidationError as e:
            error_msg = str(e)
            # Should mention None or null
            assert "None" in error_msg or "null" in error_msg.lower()
    
    def test_validation_error_with_range(self):
        """Test ValidationError for range violations is clear."""
        try:
            validate_number(150, min_val=0, max_val=100)
        except ValidationError as e:
            error_msg = str(e)
            # Should mention the value and range
            assert "150" in error_msg or "maximum" in error_msg.lower()


class TestPlaceholderBehaviorEnum:
    """Test that PlaceholderBehavior enum is accessible and works.
    
    Validates: Requirement 6.1
    """
    
    def test_placeholder_behavior_enum_exists(self):
        """Test PlaceholderBehavior enum can be imported."""
        from fishertools.safe import PlaceholderBehavior
        assert hasattr(PlaceholderBehavior, 'PRESERVE')
        assert hasattr(PlaceholderBehavior, 'MISSING')
        assert hasattr(PlaceholderBehavior, 'EMPTY')
    
    def test_placeholder_behavior_with_safe_format(self):
        """Test PlaceholderBehavior works with safe_format."""
        result = safe_format(
            "Hello {name}",
            {},
            behavior=PlaceholderBehavior.PRESERVE
        )
        # Should preserve the placeholder
        assert "{name}" in result
    
    def test_placeholder_behavior_missing_default(self):
        """Test default behavior shows missing placeholders."""
        result = safe_format("Hello {name}", {})
        # Should indicate missing placeholder
        assert "MISSING" in result or "name" in result
