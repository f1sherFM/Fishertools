# Public API Stability Levels (`#33`)

This document defines the stability levels for top-level `fishertools` exports.

## Levels

### `stable`
- Core top-level API with strongest compatibility guarantees
- Intended for onboarding and high-frequency usage
- Breaking changes require explicit deprecation cycle

Examples:
- `explain_error`, `safe_get`, `safe_divide`, `safe_read_file`
- API mode controls (`set_api_mode`, `get_api_mode`, `api_mode`)
- core exception types

### `advanced`
- Extended top-level convenience API, typically lazy-loaded
- Backward compatible by default, but import timing may change

Examples:
- visualization helpers/classes
- network and i18n convenience exports
- extended safe helpers and input helpers

### `legacy`
- Legacy compatibility exports
- Kept for backward compatibility, but excluded from star-import contract

Examples:
- `utils`, `decorators`, `helpers`

### `module_only`
- Submodule-oriented facade entries
- Accessible through explicit module usage, not part of symbol `__all__` contract

Examples:
- `errors`, `safe`, `learn`, `network`, `i18n`, `visualization`

## Compatibility Guarantees by Level

- `stable`: strongest guarantees, no silent removals or breaking signature changes
- `advanced`: compatible API surface expected; lazy/eager import timing may evolve
- `legacy`: preserved compatibility path, but no guarantee to appear in `from fishertools import *`
- `module_only`: module accessibility is guaranteed, star-import inclusion is not

## Rule for Adding New Top-Level Exports

1. Assign stability level before adding export
2. Update contract manifest (`fishertools/public_api_manifest.json`) in the same PR
3. Add/update tests validating contract and import UX
4. Document compatibility impact if behavior changes

