# Import Facade: Lazy Import Error Handling (`#37`)

This document describes the lazy import error UX for Epic `#24`, issue `#37`.

## Goal

When lazy imports fail in `fishertools.__getattr__`, users should get an actionable `ImportError` with API context instead of a raw low-level import traceback message.

## Behavior

`fishertools.__getattr__` now wraps `ImportError` for lazy-loaded:

- submodules (for example `fishertools.network`)
- selected lazy top-level symbols (for example `fishertools.safe_request`)

### Case 1: Fishertools lazy submodule is missing

Example:

- user accesses `fishertools.network`
- `fishertools.network` submodule is unavailable

Result:

- `ImportError` explains which lazy module/attribute was being loaded
- message states that the expected `fishertools.<module>` submodule is not available

### Case 2: External/optional dependency is missing inside lazy module

Example:

- user accesses `fishertools.safe_request`
- `fishertools.network` import fails because a dependency (e.g. `requests`) is missing

Result:

- `ImportError` explains that a lazy fishertools attribute failed to load
- message hints that an optional dependency or internal module import failed
- missing dependency name is included when available

## Non-goals

- suppressing unrelated runtime exceptions
- converting unknown attributes into `ImportError`

Invalid attribute access still raises `AttributeError`.

