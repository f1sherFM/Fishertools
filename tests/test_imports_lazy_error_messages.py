from __future__ import annotations

import importlib

import pytest


def test_invalid_attribute_still_raises_attribute_error():
    fishertools = importlib.import_module("fishertools")

    with pytest.raises(AttributeError):
        getattr(fishertools, "definitely_not_a_real_export_12345")


def test_lazy_submodule_missing_raises_friendly_import_error(monkeypatch: pytest.MonkeyPatch):
    fishertools = importlib.import_module("fishertools")

    original_import_module = importlib.import_module

    def fake_import_module(name: str, package: str | None = None):
        if name == ".network" and package == "fishertools":
            raise ModuleNotFoundError("No module named 'fishertools.network'", name="fishertools.network")
        return original_import_module(name, package)

    monkeypatch.setattr(importlib, "import_module", fake_import_module)
    fishertools.__dict__.pop("network", None)

    with pytest.raises(ImportError, match="Failed to load lazy fishertools module 'network'"):
        _ = fishertools.network


def test_lazy_module_optional_dependency_failure_raises_friendly_import_error(
    monkeypatch: pytest.MonkeyPatch,
):
    fishertools = importlib.import_module("fishertools")

    original_import_module = importlib.import_module

    def fake_import_module(name: str, package: str | None = None):
        if name == ".network" and package == "fishertools":
            raise ModuleNotFoundError("No module named 'requests'", name="requests")
        return original_import_module(name, package)

    monkeypatch.setattr(importlib, "import_module", fake_import_module)
    fishertools.__dict__.pop("safe_request", None)

    with pytest.raises(ImportError) as exc_info:
        _ = fishertools.safe_request

    message = str(exc_info.value)
    assert "Failed to load lazy fishertools attribute 'safe_request'" in message
    assert "missing optional dependency" in message.lower()
    assert "requests" in message

