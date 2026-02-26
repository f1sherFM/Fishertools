from __future__ import annotations

from contextlib import contextmanager
import importlib
import importlib.util
import sys
from pathlib import Path

import pytest


@contextmanager
def _fresh_import_fishertools():
    original_modules = {
        name: module
        for name, module in sys.modules.items()
        if name == "fishertools" or name.startswith("fishertools.")
    }

    try:
        for name in list(original_modules):
            sys.modules.pop(name, None)
        yield importlib.import_module("fishertools")
    finally:
        for name in list(sys.modules):
            if name == "fishertools" or name.startswith("fishertools."):
                sys.modules.pop(name, None)
        sys.modules.update(original_modules)


def _exec_star_import_namespace() -> dict[str, object]:
    namespace: dict[str, object] = {}
    exec("from fishertools import *", {}, namespace)
    return namespace


def _load_fishertools_init_module():
    module_path = Path("fishertools/__init__.py")
    spec = importlib.util.spec_from_file_location("fishertools_lazy_getattr_test", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_star_import_smoke_exports_key_symbols():
    with _fresh_import_fishertools():
        namespace = _exec_star_import_namespace()

        expected_symbols = {
            "explain_error",
            "safe_get",
            "safe_divide",
            "safe_request",
            "translate_error",
            "EnhancedVisualizer",
            "get_version_info",
        }
        assert expected_symbols.issubset(namespace.keys())


def test_star_import_policy_excludes_module_names_from_namespace():
    with _fresh_import_fishertools():
        namespace = _exec_star_import_namespace()

        excluded_module_names = {"safe", "errors", "network", "i18n", "utils", "helpers"}
        assert excluded_module_names.isdisjoint(namespace.keys())


def test_optional_dependency_failure_via_lazy_symbol_gives_friendly_error(monkeypatch: pytest.MonkeyPatch):
    with _fresh_import_fishertools() as fishertools:
        fishertools.__dict__.pop("safe_request", None)

        original_import_module = importlib.import_module

        def fake_import_module(name: str, package: str | None = None):
            if name == ".network" and package == "fishertools":
                raise ModuleNotFoundError("No module named 'requests'", name="requests")
            return original_import_module(name, package)

        monkeypatch.setattr(importlib, "import_module", fake_import_module)

        with pytest.raises(ImportError) as exc_info:
            # ``from fishertools import safe_request`` resolves via attribute access in this path.
            _ = fishertools.safe_request

        message = str(exc_info.value)
        assert "lazy fishertools attribute 'safe_request'" in message
        assert "optional dependency" in message.lower()
        assert "requests" in message
