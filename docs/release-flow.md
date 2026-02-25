# Release Flow

Single source of truth for version is:

- `fishertools/_version.py` (`__version__`)

`pyproject.toml` reads package version dynamically from this attribute.

## Steps

1. Update `fishertools/_version.py` to the next semantic version (`MAJOR.MINOR.PATCH`).
2. Run checks:
   - `pytest -q`
   - `mypy fishertools/api_mode.py fishertools/cli.py fishertools/patterns/logger.py fishertools/errors/formatters.py fishertools/errors/pattern_loader.py fishertools/i18n/error_translator.py`
3. Update release notes/changelog.
4. Create tag and GitHub release.
5. Publish package artifacts.

## Guardrails

- Tests enforce semver format for `fishertools.__version__`.
- Tests enforce pyproject dynamic version mapping consistency.

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
