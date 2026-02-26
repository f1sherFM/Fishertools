from __future__ import annotations

import importlib


MODULE_NAMES_REMOVED_FROM_ALL = {
    "utils",
    "decorators",
    "helpers",
    "errors",
    "safe",
    "learn",
    "legacy",
    "input_utils",
    "async_logger",
    "async_safe",
    "learning",
    "documentation",
    "examples",
    "config",
    "integration",
    "visualization",
    "validation",
    "debug",
    "network",
    "i18n",
}


def test_public_symbol_exports_remain_in_all():
    fishertools = importlib.import_module("fishertools")
    expected_symbol_exports = {
        "explain_error",
        "safe_get",
        "safe_divide",
        "safe_request",
        "translate_error",
        "EnhancedVisualizer",
        "get_version_info",
    }
    assert expected_symbol_exports.issubset(set(fishertools.__all__))


def test_module_names_are_not_in_all_but_remain_accessible():
    fishertools = importlib.import_module("fishertools")
    public_exports = set(fishertools.__all__)

    assert MODULE_NAMES_REMOVED_FROM_ALL.isdisjoint(public_exports)

    # Compat: explicit attribute access still works for representative modules.
    assert hasattr(fishertools, "safe")
    assert hasattr(fishertools, "errors")
    assert hasattr(fishertools, "utils")
    assert hasattr(fishertools, "network")

