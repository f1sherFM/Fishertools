"""
Global API behavior mode for public fishertools APIs.

Modes:
- friendly: return safe defaults where possible
- strict: raise exceptions on invalid inputs and I/O failures
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Iterator

_VALID_MODES = {"friendly", "strict"}
_api_mode = os.getenv("FISHERTOOLS_API_MODE", "friendly").strip().lower() or "friendly"
if _api_mode not in _VALID_MODES:
    _api_mode = "friendly"


def set_api_mode(mode: str) -> None:
    mode_normalized = str(mode).strip().lower()
    if mode_normalized not in _VALID_MODES:
        raise ValueError("mode must be 'friendly' or 'strict'")
    global _api_mode
    _api_mode = mode_normalized


def get_api_mode() -> str:
    return _api_mode


def is_strict_mode() -> bool:
    return _api_mode == "strict"


@contextmanager
def api_mode(mode: str) -> Iterator[None]:
    previous = get_api_mode()
    set_api_mode(mode)
    try:
        yield
    finally:
        set_api_mode(previous)

