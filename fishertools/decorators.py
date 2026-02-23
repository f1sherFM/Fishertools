"""Useful decorators for debugging, profiling, and retry/caching helpers."""
from __future__ import annotations

import functools
import time
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def timer(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator that prints execution time for a function call."""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start_time = time.time()
        result: R = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} completed in {end_time - start_time:.4f} seconds")
        return result

    return wrapper


def debug(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator that prints function arguments and return value."""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}: args={args}, kwargs={kwargs}")
        result: R = func(*args, **kwargs)
        print(f"{func.__name__} returned: {result}")
        return result

    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Retry a function call on exception up to `max_attempts` times."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    print(
                        f"Attempt {attempt + 1} failed: {e}. "
                        f"Retrying in {delay} seconds..."
                    )
                    time.sleep(delay)
            raise RuntimeError("Unexpected error in retry decorator")

        return wrapper

    return decorator


def cache_result(func: Callable[P, R]) -> Callable[P, R]:
    """Simple decorator that caches results by args/kwargs string key."""

    cache: dict[str, R] = {}

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        key = str(args) + str(sorted(kwargs.items()))

        if key in cache:
            print(f"Using cached result for {func.__name__}")
            return cache[key]

        result: R = func(*args, **kwargs)
        cache[key] = result
        return result

    return wrapper


def validate_types(**expected_types: type) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Validate selected argument types before calling the function."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            import inspect

            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            for param_name, expected_type in expected_types.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"Parameter '{param_name}' must be of type "
                            f"{expected_type.__name__}, got {type(value).__name__}"
                        )

            return func(*args, **kwargs)

        return wrapper

    return decorator
