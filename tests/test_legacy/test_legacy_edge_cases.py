"""Edge-case tests for legacy compatibility behavior."""

import pytest

from fishertools import helpers
from fishertools import legacy


def test_legacy_generate_password_zero_length_returns_empty_string() -> None:
    """Legacy API keeps historical behavior for non-positive password length."""
    assert legacy.generate_password(0) == ""
    assert legacy.generate_password(-5) == ""


def test_helpers_generate_password_non_positive_length_raises() -> None:
    """Current helpers API validates length strictly."""
    with pytest.raises(ValueError):
        helpers.generate_password(0)
    with pytest.raises(ValueError):
        helpers.generate_password(-5)


def test_legacy_chunk_list_zero_size_raises_value_error() -> None:
    """Legacy behavior for zero chunk size is preserved."""
    with pytest.raises(ValueError):
        legacy.chunk_list([1, 2, 3], 0)


def test_legacy_chunk_list_negative_size_returns_empty_list() -> None:
    """Legacy behavior for negative chunk size is preserved."""
    assert legacy.chunk_list([1, 2, 3], -1) == []


def test_helpers_chunk_list_non_positive_size_raises() -> None:
    """Current helpers API validates chunk size strictly."""
    with pytest.raises(ValueError):
        helpers.chunk_list([1, 2, 3], 0)
    with pytest.raises(ValueError):
        helpers.chunk_list([1, 2, 3], -1)


def test_invalid_hash_algorithm_raises_value_error_in_legacy_and_helpers() -> None:
    """Both legacy and helpers should raise ValueError for unsupported algorithms."""
    with pytest.raises(ValueError):
        legacy.hash_string("abc", "not_a_real_hash")
    with pytest.raises(ValueError):
        helpers.hash_string("abc", "not_a_real_hash")
