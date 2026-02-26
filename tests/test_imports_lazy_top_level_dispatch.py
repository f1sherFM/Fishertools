from __future__ import annotations

from contextlib import contextmanager
import importlib
import sys


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


def test_core_onboarding_symbols_still_available_after_import():
    with _fresh_import_fishertools() as fishertools:
        assert callable(fishertools.explain_error)
        assert callable(fishertools.safe_get)
        assert callable(fishertools.safe_divide)
        assert callable(fishertools.safe_read_file)
        assert callable(fishertools.safe_open)


def test_selected_top_level_symbols_are_loaded_lazily_on_access():
    with _fresh_import_fishertools() as fishertools:
        assert "fishertools.network" not in sys.modules
        assert "fishertools.i18n" not in sys.modules
        assert "fishertools.visualization" not in sys.modules

        assert callable(fishertools.safe_request)
        assert callable(fishertools.translate_error)
        assert fishertools.EnhancedVisualizer is not None

        assert "fishertools.network" in sys.modules
        assert "fishertools.i18n" in sys.modules
        assert "fishertools.visualization" in sys.modules


def test_lazy_loaded_symbols_are_cached_on_module_globals():
    with _fresh_import_fishertools() as fishertools:
        first = fishertools.safe_request
        second = fishertools.safe_request

        assert first is second
        assert fishertools.__dict__["safe_request"] is first
