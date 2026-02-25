#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


README_PATH = Path("README.md")
VERSION_FILE = Path("fishertools/_version.py")


@dataclass(frozen=True)
class VersionConsistencySnapshot:
    package_version: str
    readme_current_version: str | None
    readme_install_version: str | None


def load_package_version() -> str:
    source = VERSION_FILE.read_text(encoding="utf-8")
    match = re.search(r'__version__\s*=\s*"([^"]+)"', source)
    if not match:
        raise ValueError("Could not parse package version from fishertools/_version.py")
    return match.group(1)


def load_readme_versions() -> tuple[str | None, str | None]:
    content = README_PATH.read_text(encoding="utf-8")
    current_match = re.search(r"Current version:\s*`([^`]+)`", content)
    install_match = re.search(r"pip install fishertools==([^\s`]+)", content)
    return (
        current_match.group(1) if current_match else None,
        install_match.group(1) if install_match else None,
    )


def build_snapshot() -> VersionConsistencySnapshot:
    package_version = load_package_version()
    readme_current, readme_install = load_readme_versions()
    return VersionConsistencySnapshot(
        package_version=package_version,
        readme_current_version=readme_current,
        readme_install_version=readme_install,
    )


def normalize_tag_version(tag: str) -> str:
    return tag[1:] if tag.startswith("v") else tag


def validate_snapshot(snapshot: VersionConsistencySnapshot, git_tag: str | None = None) -> list[str]:
    errors: list[str] = []
    package_version = snapshot.package_version

    if snapshot.readme_current_version is None:
        errors.append("README.md: missing 'Current version: `...`' line")
    elif snapshot.readme_current_version != package_version:
        errors.append(
            "README.md current version mismatch: "
            f"README has {snapshot.readme_current_version}, package has {package_version}. "
            "Update the 'Current version' line in README.md."
        )

    if snapshot.readme_install_version is None:
        errors.append("README.md: missing 'pip install fishertools==<version>' install command")
    elif snapshot.readme_install_version != package_version:
        errors.append(
            "README.md install command mismatch: "
            f"README has {snapshot.readme_install_version}, package has {package_version}. "
            "Update the install command version in README.md."
        )

    if git_tag:
        normalized = normalize_tag_version(git_tag)
        if normalized != package_version:
            errors.append(
                "Git tag/package version mismatch: "
                f"tag {git_tag} -> {normalized}, package has {package_version}. "
                "Create/publish a tag matching fishertools/_version.py (optionally with 'v' prefix)."
            )

    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check version consistency across README, package version, and optional git tag."
    )
    parser.add_argument(
        "--git-tag",
        help="Optional git tag to compare with package version (e.g. v0.5.5.1 or 0.5.5.1)",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        snapshot = build_snapshot()
    except (OSError, ValueError) as exc:
        print(f"Version consistency check failed to read inputs: {exc}")
        return 1

    errors = validate_snapshot(snapshot, git_tag=args.git_tag)
    if errors:
        print("Release version consistency check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Release version consistency check passed "
        f"(package={snapshot.package_version}, README current/install aligned"
        + (f", tag={args.git_tag}" if args.git_tag else "")
        + ")"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
