# Import Policy for `fishertools.__all__` (`#36`)

This document defines the `__all__` policy for Epic `#24`, issue `#36`.

## Policy (Compact `__all__`)

`fishertools.__all__` should contain stable facade exports (functions/classes) intended for:

- `from fishertools import *` usage
- compact public API discovery

`fishertools.__all__` should **not** contain module names (for example `safe`, `errors`, `network`, `utils`, etc.).

## Why module names were removed from `__all__`

Including module names in `__all__` makes `from fishertools import *` heavier and more fragile because it can trigger:

- extra imports
- lazy import side effects
- optional dependency failures earlier than expected

Removing module names keeps star import focused on stable symbols and improves import UX.

## Compatibility Notes

Module access remains supported:

```python
import fishertools
import fishertools.safe

from fishertools import safe_request   # still supported
from fishertools import utils          # explicit import still supported via attribute access
```

What changes:

- `from fishertools import *` no longer injects module names such as `utils`, `safe`, `network`, `i18n`

What does not change:

- explicit imports of submodules/legacy modules continue to work
- `fishertools.<module>` attribute access continues to work (lazy submodule dispatch)
- function/class exports remain in `__all__`

## Potential Breaking Changes and Mitigations

1. Code relying on `from fishertools import *` to get module names (`safe`, `errors`, `utils`, ...)
   - Mitigation: switch to explicit imports (`import fishertools.safe` or `from fishertools import safe_request`)
2. Code introspecting `fishertools.__all__` and expecting module names
   - Mitigation: use explicit module allowlist or check `hasattr(fishertools, "<module>")` instead
3. Tests asserting legacy modules are in `__all__`
   - Mitigation: update tests to assert module accessibility, not star-import exposure

## Follow-up Alignment

- `#37` will improve lazy import error messages for module access paths
- `#38` will add regression tests for `import *` and optional dependency scenarios using this policy

## `import *` Contract (Current)

`from fishertools import *` is supported as a compatibility path with a compact symbol-only export set:

- includes stable function/class facade exports
- excludes module names and submodule handles

This behavior is covered by regression tests in `tests/test_imports_star_and_optional_deps.py`.
