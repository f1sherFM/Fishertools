# Release Flow

Single source of truth for version is:

- `fishertools/_version.py` (`__version__`)

`pyproject.toml` reads package version dynamically from this attribute.

## Steps

1. Update `fishertools/_version.py` to the next semantic version (`MAJOR.MINOR.PATCH` or project hotfix format `MAJOR.MINOR.PATCH.HOTFIX`, e.g. `0.5.5.1`).
2. Run checks:
   - `pytest -q`
   - `python scripts/check_text_encoding.py --root .`
   - `python scripts/check_explicit_encoding.py`
   - `python scripts/check_release_version_consistency.py`
   - `mypy fishertools/api_mode.py fishertools/cli.py fishertools/patterns/logger.py fishertools/errors/formatters.py fishertools/errors/pattern_loader.py fishertools/i18n/error_translator.py`
3. Update release notes/changelog.
4. Validate the release tag against package version:
   - `python scripts/check_release_version_consistency.py --git-tag vX.Y.Z`
5. Create tag and GitHub release.
6. Build and validate package artifacts:
   - `python -m build`
   - `python -m twine check dist/*`
7. Publish package artifacts.

## Guardrails

- Tests enforce semver format for `fishertools.__version__`.
- Tests enforce pyproject dynamic version mapping consistency.
- CI enforces UTF-8/mojibake checks, explicit `encoding=` rules for release-critical files, and version consistency.

## Release Encoding and Artifact Policy (Issue #29)

This section is the single place for release hardening rules.

### Encoding Standard

- UTF-8 is the default encoding for repository text files and release-facing docs.
- Text file I/O in release-critical scripts/tests must use explicit `encoding=...` (typically `utf-8`).
- Binary I/O (`rb`, `wb`, etc.) must not use `encoding=`.

### Artifact Consistency Rules

- `fishertools/_version.py` is the source of truth for the package version.
- `README.md` must contain the same version in:
  - `Current version:`
  - `pip install fishertools==...`
- Release tags may be `vX.Y.Z` or `X.Y.Z` (including hotfix suffixes like `0.5.5.1`), but the normalized tag value must match the package version.

### Pre-Tag Checklist

- UTF-8/mojibake guard passes
- Explicit `encoding=` guard passes
- README/package version consistency guard passes
- Release tag matches package version
- `python -m build` succeeds
- `python -m twine check dist/*` passes

### Common Failure Examples

- Mojibake in docs/console output:
  - Example symptom: garbled text fragments instead of readable UTF-8 output
  - Detection: `python scripts/check_text_encoding.py --root .`
- Missing explicit `encoding=` in release-critical text I/O:
  - Example: `open("pyproject.toml")` in a release helper script
  - Fix: `open("pyproject.toml", encoding="utf-8")`
- Version drift between README and package metadata:
  - Example: `fishertools/_version.py` is `0.5.5.1`, but README install command still shows older version
  - Detection: `python scripts/check_release_version_consistency.py`
- Tag/package mismatch in release pipeline:
  - Example: release tag `v0.5.5.0` while package version is `0.5.5.1`
  - Detection: `python scripts/check_release_version_consistency.py --git-tag v0.5.5.0`

## Encoding Guard (Issue #26)

Before publishing, run:

```bash
python scripts/check_text_encoding.py --root .
```

What it checks:

- text files decode as UTF-8
- binary artifacts are skipped via extension allowlist
- common mojibake markers are detected (for example latin-1-style marker pairs and high-signal mojibake chars)

Note: the checker contains a temporary path allowlist for known legacy mojibake files already present in the repository. New files with the same issue should fail CI.

## Explicit `encoding=` Guard (Issue #27)

Run:

```bash
python scripts/check_explicit_encoding.py
```

Scope (current): release-critical scripts/tests only.

Policy:

- text-mode `open()` calls must specify `encoding=...`
- binary modes (`rb`, `wb`, etc.) are allowed without `encoding=`
- this is a targeted guard, not a repository-wide rule yet

## Version Consistency Guard (Issue #28)

Run for `HEAD` (README vs package version):

```bash
python scripts/check_release_version_consistency.py
```

Run for release tag validation (tag vs package version):

```bash
python scripts/check_release_version_consistency.py --git-tag vX.Y.Z
```

Policy:

- `README.md` "Current version" must match `fishertools/_version.py`
- `README.md` install command version must match `fishertools/_version.py`
- release tag may be `vX.Y.Z` or `X.Y.Z`, but normalized value must match package version
