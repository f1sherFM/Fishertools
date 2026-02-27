# Release Versioning Policy (`#41`)

This policy defines how fishertools versions and release artifacts are synchronized.

## 1. Version Formats

Primary release format:
- `MAJOR.MINOR.PATCH` (example: `0.6.0`)

Supported hotfix formats:
- `MAJOR.MINOR.PATCH.HOTFIX` (example: `0.5.5.1`)
- `MAJOR.MINOR.PATCH.postN` (example: `0.5.5.post1`)

## 2. When to Use `X.Y.Z.postN` vs `X.Y.Z.N`

Use `X.Y.Z.postN` when:
- the release is packaging-only or metadata-only
- runtime/API behavior is unchanged
- you need a post-release correction for distribution artifacts

Use `X.Y.Z.N` when:
- hotfix contains runtime code/test/doc behavior changes shipped as a normal patch train
- team intentionally follows numeric 4-part hotfix continuity already used in this project

Rule of thumb:
- prefer one format consistently within a release line
- do not mix `.N` and `.postN` for the same fix intent without explicit release note justification

## 3. Synchronization Requirements Per Release Tag

For a release tag `vX.Y.Z` or `vX.Y.Z.N`:
- `fishertools/_version.py::__version__` must equal normalized tag version
- README `Current version` must match the same version
- README install command (`pip install fishertools==...`) must match the same version

## 4. CI Checks Enforcing This Policy

The following checks from release hardening are the required gate:

- `python scripts/check_release_version_consistency.py`
- `python scripts/check_release_version_consistency.py --git-tag vX.Y.Z`
- `python scripts/check_text_encoding.py --root .`
- `python scripts/check_explicit_encoding.py`

See also: `docs/release-flow.md`

