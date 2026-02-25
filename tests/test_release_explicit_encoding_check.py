from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def _load_checker_module():
    module_path = Path("scripts/check_explicit_encoding.py")
    spec = importlib.util.spec_from_file_location("check_explicit_encoding", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


check_explicit_encoding = _load_checker_module()


def test_release_critical_file_list_is_defined_and_existing():
    for rel_path in check_explicit_encoding.CRITICAL_TEXT_IO_FILES:
        assert Path(rel_path).exists(), f"Missing critical file: {rel_path}"


def test_binary_mode_open_is_allowed_without_encoding(tmp_path: Path):
    sample = tmp_path / "sample.py"
    sample.write_text("with open('x.bin', 'rb') as f:\n    f.read()\n", encoding="utf-8")

    problems = check_explicit_encoding.check_file_for_explicit_encoding(sample)

    assert problems == []


def test_text_mode_open_requires_explicit_encoding(tmp_path: Path):
    sample = tmp_path / "sample.py"
    sample.write_text("with open('x.txt', 'r') as f:\n    f.read()\n", encoding="utf-8")

    problems = check_explicit_encoding.check_file_for_explicit_encoding(sample)

    assert len(problems) == 1
    assert "must specify encoding=" in problems[0].reason


def test_current_release_critical_files_pass_check():
    problems = check_explicit_encoding.run_check()
    assert problems == []
