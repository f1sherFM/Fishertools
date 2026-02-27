# Public API Contract Manifest (`#34`)

Single source of truth for top-level public API contract:

- `fishertools/public_api_manifest.json`

## Purpose

The manifest centralizes:
- stability level classification for exports
- contract-level list of public exports
- rules for extending top-level API

This avoids drift between `__all__`, docs, and compatibility tests.

## Integration

Compatibility tests read the manifest directly and validate:
- stable + advanced exports remain in `fishertools.__all__`
- legacy + module-only exports remain accessible without relying on `__all__`
- import UX expectations under lazy/eager model

## Update Process

When changing top-level exports:
1. update `fishertools/public_api_manifest.json`
2. update code exports (`__all__`, lazy dispatcher, module access)
3. update tests and docs in same PR

