from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def _load_checker_module():
    module_path = Path("scripts/check_release_version_consistency.py")
    spec = importlib.util.spec_from_file_location("check_release_version_consistency", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


checker = _load_checker_module()


def test_validate_snapshot_passes_when_versions_match():
    snapshot = checker.VersionConsistencySnapshot(
        package_version="0.5.5.1",
        readme_current_version="0.5.5.1",
        readme_install_version="0.5.5.1",
    )

    assert checker.validate_snapshot(snapshot) == []


def test_validate_snapshot_reports_readme_mismatches_actionably():
    snapshot = checker.VersionConsistencySnapshot(
        package_version="0.5.5.1",
        readme_current_version="0.5.3",
        readme_install_version="0.5.2",
    )

    errors = checker.validate_snapshot(snapshot)

    assert len(errors) == 2
    assert "Current version" in errors[0]
    assert "install command" in errors[1]
    assert "Update" in errors[0]
    assert "Update" in errors[1]


def test_validate_snapshot_accepts_v_prefixed_git_tag():
    snapshot = checker.VersionConsistencySnapshot(
        package_version="0.5.5.1",
        readme_current_version="0.5.5.1",
        readme_install_version="0.5.5.1",
    )

    assert checker.validate_snapshot(snapshot, git_tag="v0.5.5.1") == []


def test_validate_snapshot_reports_tag_mismatch_actionably():
    snapshot = checker.VersionConsistencySnapshot(
        package_version="0.5.5.1",
        readme_current_version="0.5.5.1",
        readme_install_version="0.5.5.1",
    )

    errors = checker.validate_snapshot(snapshot, git_tag="v0.5.5.0")

    assert len(errors) == 1
    assert "Git tag/package version mismatch" in errors[0]
    assert "Create/publish a tag matching" in errors[0]
