#!/usr/bin/env python3
from __future__ import annotations

import ast
import sys
from dataclasses import dataclass
from pathlib import Path


# Issue #27 scope: only release-critical scripts/tests, not global repo enforcement.
CRITICAL_TEXT_IO_FILES = (
    "prepare_release.py",
    "tests/test_release_version_consistency.py",
    "tests/test_release_encoding_ci.py",
)

# Binary modes are excluded from the explicit `encoding=` requirement.
BINARY_MODE_FLAGS = ("b",)


@dataclass(frozen=True)
class EncodingCheckProblem:
    path: str
    line: int
    reason: str


def _is_open_call(node: ast.Call) -> bool:
    return isinstance(node.func, ast.Name) and node.func.id == "open"


def _literal_string(node: ast.AST | None) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _get_open_mode(call: ast.Call) -> str:
    if len(call.args) >= 2:
        mode = _literal_string(call.args[1])
        if mode is not None:
            return mode
    for keyword in call.keywords:
        if keyword.arg == "mode":
            mode = _literal_string(keyword.value)
            if mode is not None:
                return mode
    return "r"


def _has_encoding_keyword(call: ast.Call) -> bool:
    return any(keyword.arg == "encoding" for keyword in call.keywords)


def _is_binary_mode(mode: str) -> bool:
    return any(flag in mode for flag in BINARY_MODE_FLAGS)


def check_file_for_explicit_encoding(file_path: Path) -> list[EncodingCheckProblem]:
    source = file_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(file_path))

    problems: list[EncodingCheckProblem] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not _is_open_call(node):
            continue

        mode = _get_open_mode(node)
        if _is_binary_mode(mode):
            continue

        if not _has_encoding_keyword(node):
            problems.append(
                EncodingCheckProblem(
                    path=file_path.as_posix(),
                    line=node.lineno,
                    reason=f"open() in text mode '{mode}' must specify encoding=",
                )
            )

    return problems


def run_check() -> list[EncodingCheckProblem]:
    problems: list[EncodingCheckProblem] = []
    for rel_path in CRITICAL_TEXT_IO_FILES:
        file_path = Path(rel_path)
        if not file_path.exists():
            problems.append(
                EncodingCheckProblem(
                    path=rel_path,
                    line=1,
                    reason="critical file missing",
                )
            )
            continue
        problems.extend(check_file_for_explicit_encoding(file_path))
    return problems


def main() -> int:
    problems = run_check()
    if not problems:
        print("Explicit encoding check passed for critical release files")
        return 0

    print("Explicit encoding check failed:")
    for problem in problems:
        print(f"- {problem.path}:{problem.line}: {problem.reason}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
