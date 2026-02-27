from __future__ import annotations

import json
from pathlib import Path

import fishertools


MANIFEST_PATH = Path("fishertools/public_api_manifest.json")


def _load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_manifest_exists_and_has_expected_top_level_sections():
    manifest = _load_manifest()

    assert manifest["schema_version"] == 1
    assert "stability_levels" in manifest
    assert "exports" in manifest
    assert "rules" in manifest


def test_manifest_has_all_required_stability_groups():
    manifest = _load_manifest()
    groups = set(manifest["exports"])

    expected_groups = {"stable", "advanced", "legacy", "module_only"}
    assert groups == expected_groups


def test_stable_and_advanced_exports_match_symbol_all_contract():
    manifest = _load_manifest()
    public_exports = set(fishertools.__all__)

    expected_symbol_exports = set(manifest["exports"]["stable"]) | set(manifest["exports"]["advanced"])
    assert expected_symbol_exports.issubset(public_exports)


def test_legacy_and_module_only_exports_not_required_in_all_but_accessible():
    manifest = _load_manifest()
    public_exports = set(fishertools.__all__)

    excluded_from_star_import = set(manifest["exports"]["legacy"]) | set(manifest["exports"]["module_only"])
    assert excluded_from_star_import.isdisjoint(public_exports)

    # Compatibility path: still accessible through module attributes/import dispatch.
    for name in {"utils", "errors", "safe", "network", "i18n"}:
        assert hasattr(fishertools, name)

