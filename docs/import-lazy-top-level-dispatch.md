# Import Facade: Lazy Top-Level Symbol Dispatch (`#32`)

This document describes the partial lazy top-level symbol dispatch implemented for Epic `#22`, issue `#32`.

## What changed

`fishertools.__init__` now keeps a minimal eager onboarding layer and resolves a selected set of top-level symbols lazily via `__getattr__`.

Implemented lazy symbol categories:

- visualization top-level exports
- learning helper exports
- input utility prompt exports
- network convenience exports
- i18n convenience exports
- selected non-core safe helpers (serializers, file helpers)

## What remains eager

The onboarding/core path remains eager (examples):

- `__version__`
- API mode controls
- core error API (`explain_error`, ...)
- core safe helpers (`safe_get`, `safe_divide`, `safe_read_file`, `safe_write_file`, `safe_file_exists`, `safe_open`)

This follows the design contract documented in `docs/import-facade-eager-design.md`.

## Compatibility Notes

- Public names remain in `fishertools.__all__`
- Attribute access still works (`from fishertools import safe_request`, `fishertools.translate_error`, etc.)
- Import timing may change: import errors for lazy symbols can now appear at first attribute access instead of `import fishertools`

## Tests

`tests/test_imports_lazy_top_level_dispatch.py` verifies:

- onboarding/core symbols are still available immediately
- selected symbols load submodules only on attribute access
- lazy-loaded values are cached on the `fishertools` module globals

