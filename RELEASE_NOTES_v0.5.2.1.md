# Release Notes: fishertools v0.5.2.1

## Overview

This patch release aligns the network response API with the documented requests-like helpers, removes duplicated model definitions, fixes Makefile targets to the current project layout, and adds missing changelog coverage.

## Changes

### Network API Consistency
- Unified `NetworkRequest` and `NetworkResponse` model usage to a single source.
- Public `fishertools.network.NetworkResponse` now includes:
  - `.json()` helper
  - `.text` property
  - `.content` property
- Added `headers` field to the shared response model to preserve existing behavior from safe requests.

### Build/Dev Tooling
- Updated `Makefile` targets to use real paths:
  - `format`: `black fishertools/ examples/ tests/`
  - `lint`: `ruff check fishertools/ examples/ tests/` and `mypy fishertools/`
  - `lint-flake8`: `flake8 fishertools/` and `mypy fishertools/`
- Demo target now runs `examples/refactored_safe_usage.py`.

### Documentation and Process
- Added `0.5.2` entry to `CHANGELOG.md` to match the package version.

## Compatibility

- No breaking API changes.
- Existing `NetworkResponse.data` usage remains valid.

## Files Updated

- `fishertools/network/models.py`
- `fishertools/network/safe_requests.py`
- `fishertools/network/__init__.py`
- `Makefile`
- `CHANGELOG.md`

## Tests

Targeted tests passed:
- `pytest tests/test_network/test_models.py -q`
- `pytest tests/test_network/test_safe_requests_properties.py -q`
- `pytest tests/test_enhancements_integration.py -q`

---

**Release v0.5.2.1**
