"""
Tests for improved error handling in debug_step_by_step decorator.

Tests cover:
- Basic error handling with on_error callback
- Selective error handling
- Error handler that returns False (re-raises)
- Error handler that itself raises
- Backward compatibility (no on_error)
"""

from __future__ import annotations

import pytest
from io import StringIO
import sys

from fishertools.debug import debug_step_by_step


class TestDebugStepByStepErrorHandling:
    """Test error handling in debug_step_by_step decorator."""

    def test_basic_error_handling_returns_none(self, capsys):
        """Test that handled errors return None."""
        
        def handle_all_errors(e):
            return True  # Handle all errors
        
        @debug_step_by_step(on_error=handle_all_errors)
        def divide(a, b):
            return a / b
        
        # Should not raise, returns None
        result = divide(10, 0)
        
        assert result is None
        
        captured = capsys.readouterr()
        assert "ZeroDivisionError" in captured.out
        assert "Error handled by callback" in captured.out

    def test_selective_error_handling(self, capsys):
        """Test selective error handling based on exception type."""
        
        def handle_only_value_errors(e):
            if isinstance(e, ValueError):
                return True  # Handle ValueError
            return False  # Re-raise other errors
        
        @debug_step_by_step(on_error=handle_only_value_errors)
        def process(value):
            if value < 0:
                raise ValueError("Negative value")
            if value == 0:
                raise ZeroDivisionError("Zero value")
            return value * 2
        
        # ValueError should be handled
        result = process(-1)
        assert result is None
        
        captured = capsys.readouterr()
        assert "ValueError" in captured.out
        assert "Error handled by callback" in captured.out
        
        # ZeroDivisionError should be re-raised
        with pytest.raises(ZeroDivisionError):
            process(0)

    def test_error_handler_returns_false(self, capsys):
        """Test that returning False from handler re-raises error."""
        
        def handle_nothing(e):
            return False  # Don't handle any errors
        
        @debug_step_by_step(on_error=handle_nothing)
        def divide(a, b):
            return a / b
        
        # Should raise because handler returns False
        with pytest.raises(ZeroDivisionError):
            divide(10, 0)
        
        captured = capsys.readouterr()
        assert "ZeroDivisionError" in captured.out
        assert "Error handled by callback" not in captured.out

    def test_error_handler_itself_raises(self, capsys):
        """Test that if error handler raises, original error is re-raised."""
        
        def buggy_handler(e):
            raise RuntimeError("Handler is broken")
        
        @debug_step_by_step(on_error=buggy_handler)
        def divide(a, b):
            return a / b
        
        # Should raise original ZeroDivisionError, not RuntimeError
        with pytest.raises(ZeroDivisionError):
            divide(10, 0)
        
        captured = capsys.readouterr()
        assert "ZeroDivisionError" in captured.out
        assert "Error handler itself raised" in captured.out
        assert "Handler is broken" in captured.out

    def test_backward_compatibility_no_on_error(self, capsys):
        """Test that decorator works without on_error (backward compatibility)."""
        
        @debug_step_by_step
        def divide(a, b):
            return a / b
        
        # Should work normally
        result = divide(10, 2)
        assert result == 5.0
        
        # Should raise on error
        with pytest.raises(ZeroDivisionError):
            divide(10, 0)
        
        captured = capsys.readouterr()
        assert "ZeroDivisionError" in captured.out

    def test_successful_execution_with_on_error(self, capsys):
        """Test that on_error doesn't interfere with successful execution."""
        
        def handle_errors(e):
            return True
        
        @debug_step_by_step(on_error=handle_errors)
        def add(a, b):
            return a + b
        
        result = add(2, 3)
        assert result == 5
        
        captured = capsys.readouterr()
        assert "✅ Result: 5" in captured.out
        assert "Exception" not in captured.out

    def test_error_handler_with_logging(self, capsys):
        """Test error handler that logs before handling."""
        
        logged_errors = []
        
        def log_and_handle(e):
            logged_errors.append(e)
            print(f"Logged error: {type(e).__name__}")
            return True
        
        @debug_step_by_step(on_error=log_and_handle)
        def divide(a, b):
            return a / b
        
        result = divide(10, 0)
        
        assert result is None
        assert len(logged_errors) == 1
        assert isinstance(logged_errors[0], ZeroDivisionError)
        
        captured = capsys.readouterr()
        assert "Logged error: ZeroDivisionError" in captured.out

    def test_multiple_errors_in_sequence(self, capsys):
        """Test handling multiple errors in sequence."""
        
        handled_count = [0]
        
        def count_and_handle(e):
            handled_count[0] += 1
            return True
        
        @debug_step_by_step(on_error=count_and_handle)
        def divide(a, b):
            return a / b
        
        # Call multiple times with errors
        divide(10, 0)
        divide(20, 0)
        divide(30, 0)
        
        assert handled_count[0] == 3

    def test_error_handler_with_context(self, capsys):
        """Test error handler that uses exception context."""
        
        def handle_with_context(e):
            if hasattr(e, 'args') and e.args:
                print(f"Error message: {e.args[0]}")
            return True
        
        @debug_step_by_step(on_error=handle_with_context)
        def validate(value):
            if value < 0:
                raise ValueError("Value must be positive")
            return value
        
        result = validate(-5)
        
        assert result is None
        captured = capsys.readouterr()
        assert "Error message: Value must be positive" in captured.out

    def test_decorator_with_parentheses_no_args(self, capsys):
        """Test decorator with parentheses but no arguments."""
        
        @debug_step_by_step()
        def add(a, b):
            return a + b
        
        result = add(2, 3)
        assert result == 5
        
        captured = capsys.readouterr()
        assert "✅ Result: 5" in captured.out


class TestDebugStepByStepEdgeCases:
    """Test edge cases for debug_step_by_step."""

    def test_error_handler_returns_none(self, capsys):
        """Test that returning None from handler re-raises error."""
        
        def handle_returns_none(e):
            return None  # Falsy value
        
        @debug_step_by_step(on_error=handle_returns_none)
        def divide(a, b):
            return a / b
        
        # Should raise because handler returns None (falsy)
        with pytest.raises(ZeroDivisionError):
            divide(10, 0)

    def test_error_handler_returns_truthy_non_bool(self, capsys):
        """Test that returning truthy non-bool value handles error."""
        
        def handle_returns_string(e):
            return "handled"  # Truthy but not bool
        
        @debug_step_by_step(on_error=handle_returns_string)
        def divide(a, b):
            return a / b
        
        # Should handle because "handled" is truthy
        result = divide(10, 0)
        assert result is None

    def test_nested_decorated_functions(self, capsys):
        """Test nested functions with debug_step_by_step."""
        
        def handle_errors(e):
            return True
        
        @debug_step_by_step(on_error=handle_errors)
        def outer(x):
            return inner(x)
        
        @debug_step_by_step(on_error=handle_errors)
        def inner(x):
            return 1 / x
        
        # Both should handle the error
        result = outer(0)
        assert result is None

    def test_function_with_no_parameters(self, capsys):
        """Test decorator on function with no parameters."""
        
        def handle_errors(e):
            return True
        
        @debug_step_by_step(on_error=handle_errors)
        def raise_error():
            raise ValueError("Test error")
        
        result = raise_error()
        assert result is None
        
        captured = capsys.readouterr()
        assert "ValueError" in captured.out

    def test_function_with_kwargs_only(self, capsys):
        """Test decorator on function with keyword-only arguments."""
        
        def handle_errors(e):
            return True
        
        @debug_step_by_step(on_error=handle_errors)
        def divide(*, a, b):
            return a / b
        
        result = divide(a=10, b=0)
        assert result is None


class TestBackwardCompatibility:
    """Test backward compatibility with existing code."""

    def test_old_usage_still_works(self, capsys):
        """Test that old usage pattern still works."""
        
        @debug_step_by_step
        def add(a, b):
            return a + b
        
        result = add(2, 3)
        assert result == 5
        
        captured = capsys.readouterr()
        assert "Debugging: add" in captured.out
        assert "✅ Result: 5" in captured.out

    def test_old_usage_raises_on_error(self, capsys):
        """Test that old usage still raises errors."""
        
        @debug_step_by_step
        def divide(a, b):
            return a / b
        
        with pytest.raises(ZeroDivisionError):
            divide(10, 0)
        
        captured = capsys.readouterr()
        assert "ZeroDivisionError" in captured.out

    def test_function_metadata_preserved(self):
        """Test that function metadata is preserved."""
        
        def handle_errors(e):
            return True
        
        @debug_step_by_step(on_error=handle_errors)
        def my_function(x, y):
            """My function docstring."""
            return x + y
        
        assert my_function.__name__ == "my_function"
        assert my_function.__doc__ == "My function docstring."


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
