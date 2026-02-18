# API Behavior Modes

Fishertools supports two global API behavior modes:

- `friendly` (default): return safe defaults for beginner-friendly APIs where possible.
- `strict`: raise exceptions for invalid inputs and operational failures.

## Usage

```python
from fishertools import set_api_mode, get_api_mode, api_mode

set_api_mode("strict")
print(get_api_mode())  # strict

with api_mode("friendly"):
    ...
```

## Current coverage

Mode-aware behavior is applied in key safe-file APIs:

- `safe_read_file`
- `safe_write_file`
- `safe_file_exists`

`friendly` mode preserves backward-compatible default-return behavior.
`strict` mode raises explicit exceptions for invalid input and I/O failures.
