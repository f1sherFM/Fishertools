from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run_check(tmp_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "scripts/check_text_encoding.py", "--root", str(tmp_path)],
        capture_output=True,
        text=True,
        check=False,
    )


def test_encoding_check_passes_for_valid_utf8_text_and_binary_allowlist(tmp_path: Path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "readme.md").write_text("Normal UTF-8 text\nПривет\n", encoding="utf-8")
    (tmp_path / "image.png").write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00")

    result = run_check(tmp_path)

    assert result.returncode == 0
    assert "passed" in result.stdout


def test_encoding_check_fails_on_invalid_utf8_bytes(tmp_path: Path):
    bad_file = tmp_path / "broken.txt"
    bad_file.write_bytes(b"\xff\xfe\xfd")

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "broken.txt" in result.stdout
    assert "invalid_utf8" in result.stdout


def test_encoding_check_fails_on_mojibake_markers(tmp_path: Path):
    # Typical mojibake fragments produced by wrong decoding should be reported.
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "bad.md").write_text("РµСЃС‚ mojibake payload", encoding="utf-8")

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "docs/bad.md" in result.stdout
    assert "suspicious_mojibake_markers" in result.stdout
    assert ("Ѓ" in result.stdout) or ("suspicious_mojibake_markers" in result.stdout)
