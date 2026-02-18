# API Guarantees And Fallback Matrix

This document defines user-facing guarantees for stability-sensitive modules.

## Public API Guarantees

### `fishertools.errors`
- `explain_error`, `explain_last_error`, `get_explanation` remain backward compatible.
- Formatter types `console`, `plain`, `json` are stable.
- New extension points are additive:
  - `register_formatter`
  - `register_pattern_provider`

### `fishertools.safe`
- Safe helpers keep friendly defaults in default mode.
- Strict mode is opt-in (`set_api_mode("strict")`).
- Existing function names/signatures remain valid.

### `fishertools.i18n`
- `translate_error` and `ErrorTranslator.explain_error` keep language fallback behavior.
- New translation provider hook is additive:
  - `register_translation_provider`

### `fishertools.patterns`
- `SimpleLogger` remains file-based and append-only.
- Path validation became stricter for invalid targets (reserved names, empty/null-byte, directory path).

## Fallback Behavior Matrix

| Module/API | Friendly mode (default) | Strict mode |
|---|---|---|
| `safe_read_file` | returns `default` on invalid path/I/O/decode errors | raises input/I/O exceptions |
| `safe_write_file` | returns `False` on write failures | raises write exceptions |
| `safe_file_exists` | returns `False` for invalid input/path errors | raises input exceptions |
| `ErrorTranslator` | falls back to configured/default language | same fallback policy |
| `ErrorExplainer` pattern matching | falls back to generic explanation | same fallback policy |

## Migration Notes

### 1) Moving to strict behavior mode
If your app relied on default-return behavior, keep using friendly mode (default).
If you need explicit failures for observability/testing:

```python
from fishertools import set_api_mode

set_api_mode("strict")
```

### 2) Logger path validation
Some previously tolerated invalid paths now fail fast at logger initialization.
Wrap logger construction where path may be user-provided.

### 3) Plugin hooks (additive)
Custom formatter/pattern/translation providers can be registered without changing existing code paths.
No migration required for existing users.
