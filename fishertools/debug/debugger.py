"""Step-by-step debugging functionality."""

from __future__ import annotations

import functools
import inspect
from typing import Any, Callable, Optional


def debug_step_by_step(func: Callable = None, *, on_error: Optional[Callable[[Exception], bool]] = None) -> Callable:
    """Decorator for step-by-step function execution with flexible error handling.

    Shows each step of function execution with variable values. Supports custom
    error handling through the on_error callback.

    Args:
        func: Function to debug
        on_error: Optional callback for error handling. 
                 Signature: (exception) -> bool
                 If returns True, error is considered handled and execution continues.
                 If returns False or None, error is re-raised.

    Returns:
        Decorated function

    Examples:
        Basic usage:
        >>> @debug_step_by_step
        ... def add(a, b):
        ...     result = a + b
        ...     return result
        >>> add(2, 3)
        🔍 Debugging: add
        Step 1: a = 2
        Step 2: b = 3
        Step 3: result = 5
        ✅ Result: 5
        5

        With error handler:
        >>> def handle_error(e):
        ...     print(f"Handled: {e}")
        ...     return True  # Error is handled
        >>> @debug_step_by_step(on_error=handle_error)
        ... def divide(a, b):
        ...     return a / b
        >>> divide(10, 0)  # Returns None instead of raising
        🔍 Debugging: divide
        Step 1: a = 10
        Step 2: b = 0
        Step 3: ❌ Exception: ZeroDivisionError: division by zero
        Handled: division by zero
        ⚠️ Error handled by callback
        None

        Selective error handling:
        >>> def handle_only_value_errors(e):
        ...     if isinstance(e, ValueError):
        ...         return True  # Handle ValueError
        ...     return False  # Re-raise other errors
        >>> @debug_step_by_step(on_error=handle_only_value_errors)
        ... def process(value):
        ...     if value < 0:
        ...         raise ValueError("Negative value")
        ...     return value * 2
    """
    
    def decorator(f: Callable) -> Callable:
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            print(f"\n🔍 Debugging: {f.__name__}")
            print()

            # Get function signature
            sig = inspect.signature(f)
            params = list(sig.parameters.keys())

            # Print arguments
            step = 1
            for i, arg in enumerate(args):
                if i < len(params):
                    print(f"Step {step}: {params[i]} = {repr(arg)}")
                    step += 1

            for key, value in kwargs.items():
                print(f"Step {step}: {key} = {repr(value)}")
                step += 1

            # Execute function
            try:
                result = f(*args, **kwargs)
                print(f"Step {step}: return {repr(result)}")
                print()
                print(f"✅ Result: {repr(result)}")
                print()
                return result
            except Exception as e:
                print(f"Step {step}: ❌ Exception: {type(e).__name__}: {e}")
                print()
                
                # Try custom error handler if provided
                if on_error:
                    try:
                        handled = on_error(e)
                        if handled:
                            print(f"⚠️ Error handled by callback")
                            print()
                            return None  # Error was handled
                    except Exception as handler_error:
                        print(f"⚠️ Error handler itself raised: {type(handler_error).__name__}: {handler_error}")
                        print()
                        # Fall through to re-raise original error
                
                # Re-raise if not handled
                raise

        return wrapper
    
    # Support both @debug_step_by_step and @debug_step_by_step(on_error=...)
    if func is None:
        # Called with arguments: @debug_step_by_step(on_error=...)
        return decorator
    else:
        # Called without arguments: @debug_step_by_step
        return decorator(func)


def set_breakpoint(message: str = "Breakpoint") -> None:
    """Set a breakpoint for debugging.

    Pauses execution and allows inspection of variables.

    Args:
        message: Message to display

    Examples:
        >>> x = 10
        >>> set_breakpoint("Check x value")
        🔴 Breakpoint: Check x value
        >>> y = x * 2
    """
    frame = inspect.currentframe()
    if frame and frame.f_back:
        caller_frame = frame.f_back
        filename = caller_frame.f_code.co_filename
        lineno = caller_frame.f_lineno
        print(f"\n🔴 Breakpoint: {message}")
        print(f"   at {filename}:{lineno}")
        print()
