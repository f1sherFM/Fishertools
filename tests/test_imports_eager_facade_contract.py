from __future__ import annotations

import importlib
import importlib.util
import sys
from pathlib import Path


def _load_contract_module():
    module_path = Path("fishertools/_import_facade_contract.py")
    spec = importlib.util.spec_from_file_location("fishertools_import_facade_contract", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


contract = _load_contract_module()
COMPATIBILITY_PLAN_NOTES = contract.COMPATIBILITY_PLAN_NOTES
LAZY_TOP_LEVEL_EXPORTS = contract.LAZY_TOP_LEVEL_EXPORTS
MINIMAL_EAGER_EXPORTS = contract.MINIMAL_EAGER_EXPORTS
SUBMODULE_FACADE_EXPORTS = contract.SUBMODULE_FACADE_EXPORTS


def test_minimal_eager_exports_cover_issue_31_required_core_names():
    required_core_names = {
        "__version__",
        "get_version_info",
        "set_api_mode",
        "get_api_mode",
        "api_mode",
        "explain_error",
        "safe_get",
        "safe_divide",
    }
    assert required_core_names.issubset(MINIMAL_EAGER_EXPORTS)


def test_import_facade_contract_groups_do_not_overlap():
    assert MINIMAL_EAGER_EXPORTS.isdisjoint(LAZY_TOP_LEVEL_EXPORTS)
    assert MINIMAL_EAGER_EXPORTS.isdisjoint(SUBMODULE_FACADE_EXPORTS)
    assert LAZY_TOP_LEVEL_EXPORTS.isdisjoint(SUBMODULE_FACADE_EXPORTS)


def test_contract_exports_exist_in_public_facade_all():
    fishertools = importlib.import_module("fishertools")
    public_exports = set(fishertools.__all__)
    contract_exports = set(MINIMAL_EAGER_EXPORTS) | set(LAZY_TOP_LEVEL_EXPORTS)

    # ``__version__`` is a public module attribute but is not listed in __all__ today.
    contract_exports.discard("__version__")

    assert contract_exports.issubset(public_exports)


def test_submodule_facade_exports_remain_accessible_but_not_required_in_all():
    fishertools = importlib.import_module("fishertools")
    public_exports = set(fishertools.__all__)

    representative_submodules = {"safe", "errors", "network", "i18n", "utils"}
    assert representative_submodules.issubset(SUBMODULE_FACADE_EXPORTS)
    assert representative_submodules.isdisjoint(public_exports)
    for name in representative_submodules:
        assert hasattr(fishertools, name)


def test_compatibility_plan_notes_are_present_for_issue_31():
    assert len(COMPATIBILITY_PLAN_NOTES) >= 3
    assert any("issue #32" in note.lower() for note in COMPATIBILITY_PLAN_NOTES)
    assert any("__all__" in note for note in COMPATIBILITY_PLAN_NOTES)
