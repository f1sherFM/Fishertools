"""Parametrized edge-case matrix for legacy/helpers compatibility guarantees."""

from __future__ import annotations

from typing import Any

import pytest

from fishertools import helpers
from fishertools import legacy


@pytest.mark.parametrize(
    ("value", "default"),
    [
        pytest.param("", "", id="empty-string"),
        pytest.param("   ", "", id="whitespace-only"),
        pytest.param("Привет,   мир!!!", "", id="unicode-cyrillic-spacing"),
        pytest.param("cafe\u0301@@##", "", id="unicode-combining-accent"),
    ],
)
def test_clean_string_edge_case_matrix(value: Any, default: str) -> None:
    """Legacy and helpers should keep matching clean_string behavior for edge inputs."""
    assert helpers.clean_string(value, default=default) == legacy.clean_string(value)


@pytest.mark.parametrize(
    ("value", "helper_default", "helper_expected", "legacy_exception"),
    [
        pytest.param(
            None,
            "fallback",
            "fallback",
            AttributeError,
            id="clean-string-none-divergence",
        ),
        pytest.param(
            12345,
            "",
            "12345",
            AttributeError,
            id="clean-string-int-divergence",
        ),
    ],
)
def test_clean_string_non_string_behavior_is_documented(
    value: Any,
    helper_default: str,
    helper_expected: str,
    legacy_exception: type[BaseException],
) -> None:
    """Document the helper-vs-legacy difference for non-string inputs."""
    assert helpers.clean_string(value, default=helper_default) == helper_expected
    with pytest.raises(legacy_exception):
        legacy.clean_string(value)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("email", "expected"),
    [
        pytest.param("", False, id="empty"),
        pytest.param("simple@example.com", True, id="ascii-valid"),
        pytest.param("bad@@example.com", False, id="double-at"),
        pytest.param("почта@example.com", False, id="unicode-local-part"),
        pytest.param("name@пример.рф", False, id="unicode-domain"),
    ],
)
def test_validate_email_string_matrix(email: str, expected: bool) -> None:
    """String inputs should preserve identical validation result in legacy/helpers."""
    assert helpers.validate_email(email) is expected
    assert legacy.validate_email(email) is expected


@pytest.mark.parametrize(
    ("email", "expected_helper", "legacy_exception"),
    [
        pytest.param(None, False, TypeError, id="none-divergence"),
        pytest.param(123, False, TypeError, id="int-divergence"),
        pytest.param(["a@b.com"], False, TypeError, id="list-divergence"),
    ],
)
def test_validate_email_non_string_behavior_is_documented(
    email: Any, expected_helper: bool, legacy_exception: type[BaseException]
) -> None:
    """
    Document the known behavior difference:
    - helpers returns False for non-string inputs
    - legacy raises from regex.match(...)
    """
    assert helpers.validate_email(email) is expected_helper
    with pytest.raises(legacy_exception):
        legacy.validate_email(email)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "dicts",
    [
        pytest.param(tuple(), id="no-dicts"),
        pytest.param(({},), id="single-empty"),
        pytest.param(({}, {"a": 1}), id="leading-empty"),
        pytest.param(({"a": 1}, {}), id="trailing-empty"),
        pytest.param(
            ({"a": {"x": 1}}, {"a": {"y": 2}}),
            id="nested-overwrite-not-deep-merge",
        ),
        pytest.param(
            ({"a": 1, "b": 2}, {"b": 3}, {"c": 4}),
            id="multi-overwrite-chain",
        ),
    ],
)
def test_merge_dicts_edge_case_matrix(dicts: tuple[dict[str, Any], ...]) -> None:
    """Merge behavior should match exactly, including nested overwrite semantics."""
    assert helpers.merge_dicts(*dicts) == legacy.merge_dicts(*dicts)


@pytest.mark.parametrize(
    ("config_data", "key", "default", "expected"),
    [
        pytest.param({}, "a", None, None, id="empty-config-miss"),
        pytest.param({"a": 1}, "a", None, 1, id="top-level-hit"),
        pytest.param({"a": {"b": {"c": 1}}}, "a.b.c", None, 1, id="deep-hit"),
        pytest.param({"a": {"b": {"c": 1}}}, "a.b.x", "miss", "miss", id="deep-miss"),
        pytest.param({"": {"x": 7}}, ".x", "miss", 7, id="empty-segment-key"),
    ],
)
def test_quickconfig_get_edge_case_matrix(
    config_data: dict[str, Any], key: str, default: Any, expected: Any
) -> None:
    """QuickConfig dotted-path lookups should stay aligned between legacy/helpers."""
    helper_cfg = helpers.QuickConfig(config_data)
    legacy_cfg = legacy.QuickConfig(config_data)
    assert helper_cfg.get(key, default) == expected
    assert legacy_cfg.get(key, default) == expected


@pytest.mark.parametrize(
    "algorithm",
    [
        pytest.param("not_a_real_hash", id="bogus-name"),
        pytest.param("SHA256_BAD", id="invalid-uppercase-name"),
        pytest.param("", id="empty-algorithm"),
    ],
)
def test_hash_string_invalid_algorithm_exception_type_parity(algorithm: str) -> None:
    """Unsupported algorithms should raise ValueError in both APIs."""
    with pytest.raises(ValueError) as helper_exc:
        helpers.hash_string("abc", algorithm)
    with pytest.raises(ValueError) as legacy_exc:
        legacy.hash_string("abc", algorithm)

    # Message text may differ; issue #19 tracks exception-type parity as the contract.
    assert isinstance(helper_exc.value, ValueError)
    assert isinstance(legacy_exc.value, ValueError)


@pytest.mark.parametrize(
    ("length", "include_symbols", "legacy_result", "helper_exception"),
    [
        pytest.param(0, True, "", ValueError, id="pwd-zero-length"),
        pytest.param(-1, False, "", ValueError, id="pwd-negative-length"),
    ],
)
def test_generate_password_known_behavior_difference_matrix(
    length: int,
    include_symbols: bool,
    legacy_result: str,
    helper_exception: type[BaseException],
) -> None:
    """Document intentionally preserved legacy/helper divergence for invalid lengths."""
    assert legacy.generate_password(length, include_symbols) == legacy_result
    with pytest.raises(helper_exception):
        helpers.generate_password(length, include_symbols)


@pytest.mark.parametrize(
    ("items", "chunk_size", "legacy_out", "helper_exception"),
    [
        pytest.param([1, 2, 3], -1, [], ValueError, id="chunk-negative"),
        pytest.param([1, 2, 3], 0, ValueError, ValueError, id="chunk-zero"),
    ],
)
def test_chunk_list_known_behavior_difference_matrix(
    items: list[int],
    chunk_size: int,
    legacy_out: Any,
    helper_exception: type[BaseException],
) -> None:
    """Document intentionally preserved chunk_list divergence on non-positive sizes."""
    if isinstance(legacy_out, type) and issubclass(legacy_out, BaseException):
        with pytest.raises(legacy_out):
            legacy.chunk_list(items, chunk_size)
    else:
        assert legacy.chunk_list(items, chunk_size) == legacy_out

    with pytest.raises(helper_exception):
        helpers.chunk_list(items, chunk_size)
