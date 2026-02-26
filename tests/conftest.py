"""
Pytest configuration and fixtures for fishertools tests.
"""

import os
import tempfile
import importlib.util
import inspect
import asyncio
from pathlib import Path

import pytest
from hypothesis import settings, Verbosity


pytest_plugins = []
HAS_PYTEST_ASYNCIO = importlib.util.find_spec("pytest_asyncio") is not None
if HAS_PYTEST_ASYNCIO:
    pytest_plugins.append("pytest_asyncio")


# Configure hypothesis for property-based testing
settings.register_profile(
    "default",
    max_examples=100,
    verbosity=Verbosity.normal,
    database=None,  # Avoid file locking/permission issues in OneDrive-backed workspaces
)
settings.load_profile("default")


def pytest_configure() -> None:
    """Use a workspace-local temp directory to avoid Windows/OneDrive temp ACL issues."""
    tmp_root = Path(__file__).resolve().parents[1] / ".pytest_tmp"
    tmp_root.mkdir(exist_ok=True)

    tmp_path = str(tmp_root)
    os.environ["TMPDIR"] = tmp_path
    os.environ["TEMP"] = tmp_path
    os.environ["TMP"] = tmp_path
    tempfile.tempdir = tmp_path


def pytest_pyfunc_call(pyfuncitem):
    """Fallback async test runner when pytest-asyncio is unavailable in some CI jobs."""
    if HAS_PYTEST_ASYNCIO:
        return None

    test_func = pyfuncitem.obj
    if not inspect.iscoroutinefunction(test_func):
        return None

    marker = pyfuncitem.get_closest_marker("asyncio")
    if marker is None:
        return None

    funcargs = {name: pyfuncitem.funcargs[name] for name in pyfuncitem._fixtureinfo.argnames}
    asyncio.run(test_func(**funcargs))
    return True


@pytest.fixture
def sample_exceptions():
    """Fixture providing common exception types for testing."""
    return [
        TypeError("'str' object cannot be interpreted as an integer"),
        ValueError("invalid literal for int() with base 10: 'abc'"),
        AttributeError("'str' object has no attribute 'append'"),
        IndexError("list index out of range"),
        KeyError("'missing_key'"),
        ImportError("No module named 'nonexistent_module'"),
        SyntaxError("invalid syntax"),
    ]
