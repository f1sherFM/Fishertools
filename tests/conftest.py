"""
Pytest configuration and fixtures for fishertools tests.
"""

import os
import tempfile
import importlib.util
from pathlib import Path

import pytest
from hypothesis import settings, Verbosity


pytest_plugins = []
if importlib.util.find_spec("pytest_asyncio") is not None:
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
