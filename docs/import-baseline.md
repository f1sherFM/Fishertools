# Import Baseline (`import fishertools`)

This document fixes the baseline for Epic `#22` / Issue `#30`:

- current eager import map in `fishertools/__init__.py`
- smoke/diagnostic scenario for `import fishertools`
- baseline metrics used for later import-model refactors

## Why this exists

Without a baseline, changes to `fishertools/__init__.py` are hard to evaluate and regressions are easy to miss.

## Smoke / Diagnostic Scenario

The baseline smoke test is implemented in `tests/test_imports_baseline.py`.

It checks:

- `import fishertools` succeeds
- `fishertools.__all__` exists and is non-empty
- a known subset of eager modules is loaded during import
- `fishertools/__init__.py` still declares expected eager import groups

The test intentionally does **not** enforce a strict time threshold, because CI and local environments vary.

## Baseline Metrics (local snapshot)

Measured on local dev environment on `2026-02-25` with:

```bash
python - <<'PY'
import importlib, sys, time
before = set(sys.modules)
start = time.perf_counter()
mod = importlib.import_module("fishertools")
elapsed_ms = (time.perf_counter() - start) * 1000
loaded = sorted(m for m in (set(sys.modules) - before) if m.startswith("fishertools"))
print(round(elapsed_ms, 3), len(loaded), len(mod.__all__))
PY
```

Observed snapshot:

- Import time: about `416.672 ms`
- Loaded `fishertools*` modules: `78`
- `len(fishertools.__all__)`: `81`

These numbers are diagnostic and may differ by machine/python version. Use them as a comparison baseline, not a hard limit.

## Current Eager Import Map (from `fishertools/__init__.py`)

Top-level `from ... import ...` groups currently declared:

- `._version` -> `__version__`
- `.api_mode` -> `set_api_mode`, `get_api_mode`, `api_mode`
- `.errors` -> primary API functions + exception classes
- `.safe` -> safe utility functions (collections/files/serialization helpers)
- `.visualization` -> visualization functions/classes
- `.learn` -> learning helpers
- `.input_utils` -> input prompts/validators
- `.network` -> request/download helpers and response classes
- `.i18n` -> translation/language helpers

In addition, `fishertools/__init__.py` eagerly imports many modules/packages for facade exposure via statements like `from . import errors`, `from . import safe`, `from . import visualization`, etc.

## Key Eager Dependencies Seen in Baseline Import

Examples of modules loaded as part of `import fishertools` in the current baseline:

- `fishertools.errors.*`
- `fishertools.safe.*`
- `fishertools.learn.*`
- `fishertools.visualization.*`
- `fishertools.network.*`
- `fishertools.i18n.*`
- `fishertools.documentation.*`
- `fishertools.learning.*`
- `fishertools.validation.*`
- `fishertools.debug.*`

## Follow-up for Next Issues in Epic

- `#31`: define minimal eager facade based on this map
- `#32`: move selected top-level exports to lazy dispatch after the facade contract is agreed

