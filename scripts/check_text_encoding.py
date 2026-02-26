#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


# Binary file extensions are skipped by design. The list is intentionally small
# and explicit so the CI check stays understandable and easy to review.
BINARY_EXTENSION_ALLOWLIST = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".pdf",
    ".zip",
    ".gz",
    ".tar",
    ".whl",
    ".so",
    ".dll",
    ".dylib",
    ".pyc",
}

# Repository paths that can contain generated/binary artifacts and should not be
# scanned as source text.
SKIPPED_DIRECTORIES = {
    ".git",
    ".hypothesis",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "test_env",
    "test_main_pypi",
    "dist",
    "build",
    "__pycache__",
    "fishertools.egg-info",
}

# Temporary baseline for known mojibake-containing files already present in the
# repository. The goal of issue #26 is to prevent *new* regressions first.
# Follow-up cleanup should remove entries from this allowlist as files are fixed.
MOJIBAKE_PATH_ALLOWLIST = {
    "docs/formatter-output-contract.md",
    "fishertools/__init__.py",
    "fishertools/errors/explainer.py",
    "fishertools/errors/explanation_builder.py",
    "fishertools/errors/formatters.py",
    "scripts/check_text_encoding.py",  # contains marker examples used by the checker
    "tests/test_bug_fixes_performance.py",
    "tests/test_errors/test_api.py",
    "tests/test_errors/test_explain_error_context_properties.py",
    "tests/test_errors/test_explain_error_context_unit.py",
    "tests/test_errors/test_formatter_contract.py",
    "tests/test_integration.py",
    "tests/test_release_encoding_ci.py",  # contains synthetic mojibake test payload
    "tests/test_safe/test_collections_properties.py",
    "tests/test_visualization/test_jump_search_properties.py",
    "tests/test_visualization/test_jump_search_unit.py",
}

# High-signal mojibake markers. `Ð`/`Ñ` usually appear when UTF-8 bytes are
# decoded as latin-1/cp1252. The extended Cyrillic chars below (`Ѓ`, `љ`, etc.)
# frequently appear inside sequences like `РµСЃС‚` and are uncommon in regular
# Russian project docs/code comments, so they are less noisy than checking `Р`
# directly.
MOJIBAKE_SUBSTRINGS = ("Ð", "Ñ", "�")
MOJIBAKE_HIGH_SIGNAL_CHARS = frozenset("ЃЌЉЊЋЏђѓєѕіїјљњћќўџ")


@dataclass(frozen=True)
class FileEncodingProblem:
    path: str
    reason: str


def should_skip_path(file_path: Path) -> bool:
    if any(part in SKIPPED_DIRECTORIES for part in file_path.parts):
        return True
    return file_path.suffix.lower() in BINARY_EXTENSION_ALLOWLIST


def iter_repository_files(root_dir: Path) -> list[Path]:
    files: list[Path] = []
    for path in root_dir.rglob("*"):
        if not path.is_file():
            continue
        if should_skip_path(path.relative_to(root_dir)):
            continue
        files.append(path)
    return sorted(files)


def detect_mojibake_markers(text: str) -> list[str]:
    found_markers = [marker for marker in MOJIBAKE_SUBSTRINGS if marker in text]
    found_high_signal_chars = sorted({char for char in text if char in MOJIBAKE_HIGH_SIGNAL_CHARS})
    return found_markers + found_high_signal_chars


def check_file_utf8_and_mojibake(file_path: Path, root_dir: Path) -> list[FileEncodingProblem]:
    problems: list[FileEncodingProblem] = []
    relative_path = file_path.relative_to(root_dir).as_posix()

    try:
        raw_bytes = file_path.read_bytes()
    except OSError as exc:
        return [FileEncodingProblem(relative_path, f"read_error: {exc}")]

    try:
        decoded_text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        reason = f"invalid_utf8: byte {exc.start}-{exc.end} ({exc.reason})"
        return [FileEncodingProblem(relative_path, reason)]

    found_markers = detect_mojibake_markers(decoded_text)
    if found_markers and relative_path not in MOJIBAKE_PATH_ALLOWLIST:
        marker_list = ", ".join(sorted(found_markers))
        problems.append(FileEncodingProblem(relative_path, f"suspicious_mojibake_markers: {marker_list}"))

    return problems


def run_encoding_scan(root_dir: Path) -> list[FileEncodingProblem]:
    all_problems: list[FileEncodingProblem] = []
    for file_path in iter_repository_files(root_dir):
        all_problems.extend(check_file_utf8_and_mojibake(file_path, root_dir))
    return all_problems


def build_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate repository text files as UTF-8 and detect common mojibake markers."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Repository root to scan (default: current directory)",
    )
    return parser


def main() -> int:
    parser = build_cli_parser()
    args = parser.parse_args()
    root_dir = args.root.resolve()

    problems = run_encoding_scan(root_dir)
    if not problems:
        print(f"UTF-8/mojibake check passed: no problems found under {root_dir}")
        return 0

    print("UTF-8/mojibake check failed. Problem files:")
    for problem in problems:
        print(f"- {problem.path}: {problem.reason}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
