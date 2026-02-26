# Import Facade: Minimal Eager Layer Design (`#31`)

This document fixes the design contract for Epic `#22`, issue `#31`.

It does **not** implement lazy dispatch for top-level symbols (that is issue `#32`).

## Goal

Define which top-level exports in `fishertools` must stay eager, and classify the rest as:

- lazy top-level candidates
- submodule-oriented facade exports (compat)

## Source of Truth

The machine-readable contract is stored in:

- `fishertools/_import_facade_contract.py`

Key declarations:

- `MINIMAL_EAGER_EXPORTS`
- `LAZY_TOP_LEVEL_EXPORTS`
- `SUBMODULE_FACADE_EXPORTS`
- `COMPATIBILITY_PLAN_NOTES`

## Minimal Eager Layer (Issue #31)

The minimal eager layer keeps immediately-available core symbols after `import fishertools`, including:

- `__version__`
- API mode controls: `set_api_mode`, `get_api_mode`, `api_mode`
- version helper: `get_version_info`
- core error API: `explain_error`, `explain_last_error`, `get_explanation`
- core exception classes
- core beginner-facing safe helpers: `safe_get`, `safe_divide`, `safe_read_file`, `safe_write_file`, `safe_file_exists`, `safe_open`

Rationale:

- these symbols are frequently used in quick-start scenarios
- they support stable beginner-focused workflows
- they minimize surprise in top-level imports while keeping room to slim the facade later

## Lazy Top-Level Candidates (for `#32`)

Examples of exports intentionally classified as lazy candidates:

- extended safe helpers and serializers
- visualization classes/functions
- learning helpers
- input prompt helpers
- network convenience functions/classes
- i18n convenience functions/classes

These remain public facade symbols for compatibility, but they do not need to be in the minimal eager layer.

## Submodule-Oriented Facade Exports (Compat)

Submodule names remain stable facade exports (examples):

- `errors`, `safe`, `learn`, `legacy`
- `network`, `i18n`, `visualization`
- `documentation`, `examples`, `debug`, `validation`
- legacy module names: `utils`, `decorators`, `helpers`

Consumers should prefer explicit submodule imports for these names:

```python
import fishertools.safe
import fishertools.errors
```

## Compatibility Plan

- Issue `#31` is design-only: no contraction of `fishertools.__all__`
- Issue `#32` may switch selected non-core top-level symbols to lazy dispatch
- Submodule facade names remain backward-compatible exports
- Any removal/reclassification with behavior change requires explicit API-compat communication

## Tests

`tests/test_imports_eager_facade_contract.py` verifies:

- required core names are in the minimal eager set
- eager/lazy/submodule groups do not overlap
- contract names remain represented in `fishertools.__all__` (except `__version__`, which is public but not listed today)
- compatibility notes are present for follow-up implementation work

