"""
Pure normalization helpers for errors subsystem.
"""

from typing import Any, Dict, cast
import re


_VALID_OPERATIONS = {
    "list_access",
    "dict_access",
    "division",
    "concatenation",
    "type_conversion",
    "attribute_access",
    "import",
    "function_call",
}

_VALID_LANGUAGES = ("ru", "en", "auto")


def normalize_context(context: Any) -> Dict[str, Any]:
    """Validate and normalize explainer context for deterministic formatting."""
    if context is None or not isinstance(context, dict):
        return {}

    validated = cast(Dict[str, Any], context.copy())

    if "operation" in validated:
        operation = validated["operation"]
        if isinstance(operation, str):
            normalized_operation = operation.strip().lower()
            validated["operation"] = (
                normalized_operation if normalized_operation in _VALID_OPERATIONS else "unknown"
            )
        else:
            validated["operation"] = "unknown"

    if "available_keys" in validated:
        available_keys = validated["available_keys"]
        if isinstance(available_keys, set):
            validated["available_keys"] = sorted(available_keys, key=lambda item: str(item))
        elif isinstance(available_keys, tuple):
            validated["available_keys"] = list(available_keys)

    return validated


def normalize_language(language: Any) -> str:
    """Normalize language argument used by explainers."""
    valid_languages = list(_VALID_LANGUAGES)
    if not isinstance(language, str):
        raise ValueError(
            f"Parameter 'language' must be one of {valid_languages}, got '{language}'"
        )

    if language in _VALID_LANGUAGES:
        return language

    if re.fullmatch(r"[A-Za-z]{2,3}", language):
        return "en"

    raise ValueError(
        f"Parameter 'language' must be one of {valid_languages}, got '{language}'"
    )


def normalize_diagnostic_text(text: str) -> str:
    """Normalize diagnostics text for deterministic formatter output."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    normalized = "\n".join(line.rstrip() for line in normalized.split("\n"))
    return normalized.strip()
