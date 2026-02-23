# Fishertools

Practical tools for writing safer, clearer Python code.

Fishertools helps you handle common failures, validate inputs, work with files safely, and explain errors in a beginner-friendly way.

## Version

Current version: `0.5.5.1`

## Install

```bash
pip install fishertools==0.5.5.1
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

## Release 0.5.5.1

- Package version set to `0.5.5.1`
- README rewritten for clarity
- Version references aligned across code and tests

## License

MIT
