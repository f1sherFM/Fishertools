# Fishertools

Practical tools for writing safer, clearer Python code.

Fishertools helps you handle common failures, validate inputs, work with files safely, and explain errors in a beginner-friendly way.

## Version

Current version: `0.6.0`

## Install

```bash
pip install fishertools==0.6.0
```

For local development:

```bash
git clone <YOUR_REPO_URL>
cd My_1st_library_python
pip install -e .
```

## Quick Start

```python
from fishertools import explain_error, safe_get, safe_divide

value = safe_get([10, 20, 30], 10, default=0)
print(value)  # 0

result = safe_divide(10, 0, default=None)
print(result)  # None

try:
    int("abc")
except Exception as e:
    explain_error(e, language="en")
```

## Documentation

- [Getting Started](docs/getting-started.md)
- [Features](docs/features.md)
- [Installation](docs/installation.md)
- [API Reference](docs/api-reference.md)
- [Import Baseline (import fishertools)](docs/import-baseline.md)
- [Import Facade Eager Design](docs/import-facade-eager-design.md)
- [Import Lazy Top-Level Dispatch](docs/import-lazy-top-level-dispatch.md)
- [Import `__all__` Policy](docs/import-all-policy.md)
- [Import Lazy Error Handling](docs/import-lazy-error-handling.md)
- [Public API Stability Levels](docs/public-api-stability-levels.md)
- [Public API Contract Manifest](docs/public-api-contract-manifest.md)
- [Versioning Policy](docs/versioning-policy.md)
- [Examples](docs/examples.md)
- [Limitations](docs/limitations.md)
- [Contributing](docs/contributing.md)

## Core Capabilities

### Error Explanation

- `explain_error(exception, language="ru|en|auto")`
- `explain_last_error()` inside `except`
- `get_explanation(exception, format_type="console|plain|json")`

### Safe Utilities

- Collections: `safe_get`, `safe_pop`, `safe_slice`
- Math: `safe_divide`, `safe_average`
- Strings: `safe_format`, `safe_split`, `safe_join`
- Files: `safe_read_file`, `safe_write_file`, `safe_read_json`, `safe_write_json`

### Validation and Debugging

- Type validation decorators and helpers
- Step-by-step debug tools
- Tracing helpers

### Visualization

- Data structure visualization
- Sorting and searching algorithm visualization

### Learning Helpers

- Interactive helpers for learning Python basics

## Common Examples

### JSON error output

```python
from fishertools.errors import get_explanation

try:
    data = {"a": 1}
    print(data["b"])
except Exception as e:
    payload = get_explanation(e, format_type="json")
    print(payload)
```

### Context-aware explanation

```python
from fishertools.errors import explain_error

try:
    arr = [1, 2, 3]
    arr[10]
except Exception as e:
    explain_error(
        e,
        context={
            "operation": "list_access",
            "variable_name": "arr",
            "index": 10,
        },
    )
```

## Compatibility

- Python `>=3.8`
- Linux / macOS / Windows

## Quality

- Broad automated test coverage
- Property-based tests
- Backward compatibility tests

## Development

Run tests:

```bash
pytest -q -p no:cacheprovider
```

Run linter:

```bash
ruff check .
```

Run release encoding guard (UTF-8 + mojibake heuristics):

```bash
python scripts/check_text_encoding.py --root .
```

Run explicit `encoding=` guard for release-critical file I/O:

```bash
python scripts/check_explicit_encoding.py
```

Run release version consistency checks (HEAD and optional tag):

```bash
python scripts/check_release_version_consistency.py
python scripts/check_release_version_consistency.py --git-tag vX.Y.Z
```

## Release 0.6.0

- Package version set to `0.6.0`
- README rewritten for clarity
- Version references aligned across code and tests
- Import baseline doc and diagnostic smoke test for `import fishertools` added (Epic `#22`, issue `#30`)
- Added CI release encoding guard for UTF-8 validation and mojibake markers (Epic `#21`, issue `#26`)
- Added explicit `encoding=` check for release-critical text file I/O (Epic `#21`, issue `#27`)
- Added release version consistency checks for README/package and release tag validation (Epic `#21`, issue `#28`)
- Added minimal eager facade design contract for top-level imports (Epic `#22`, issue `#31`)
- Added lazy top-level symbol dispatch for selected facade exports (Epic `#22`, issue `#32`)
- Adopted compact `fishertools.__all__` policy (functions/classes only; module names excluded) (Epic `#24`, issue `#36`)
- Added friendly lazy-import error diagnostics for submodules and selected top-level symbols (Epic `#24`, issue `#37`)
- Added `import *` and optional-deps regression tests for import UX (Epic `#24`, issue `#38`)
- Added public API stability levels and contract manifest backed by compatibility tests (Epic `#23`, issues `#33/#34/#35`)
- Updated get_version_info to avoid stale historical enhancement keys and added regression checks (Epic `#25`, issues `#39/#40`)
- Added formal hotfix/version synchronization policy docs (Epic `#25`, issue `#41`)

## License

MIT
