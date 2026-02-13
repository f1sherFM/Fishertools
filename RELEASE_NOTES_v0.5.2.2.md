# Release Notes: fishertools v0.5.2.2

## Overview

This patch release fixes the short package description shown on PyPI by replacing a corrupted (mojibake) value with a clean UTF-8 English description.

## Changes

### Packaging Metadata
- Fixed `project.description` in `pyproject.toml` to a clean ASCII/UTF-8 string.
- Bumped version to `0.5.2.2`.

## Files Updated

- `pyproject.toml`
- `fishertools/_version.py`
- `README.md`

---

**Release v0.5.2.2**
