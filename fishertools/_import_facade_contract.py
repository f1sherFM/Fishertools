"""Import facade contract for top-level API loading behavior.

This module documents the intended *design contract* for issue #31:
- which names must remain eagerly available after ``import fishertools``
- which names are candidates for lazy top-level loading in issue #32
- which names should be treated as submodule-oriented access

It is intentionally declarative and does not implement lazy dispatch itself.
"""

from __future__ import annotations


# Minimal eager layer: versioning, API mode controls, and core beginner-facing
# functions/classes that should stay immediately available on import.
MINIMAL_EAGER_EXPORTS: frozenset[str] = frozenset(
    {
        "__version__",
        "get_version_info",
        "set_api_mode",
        "get_api_mode",
        "api_mode",
        "explain_error",
        "explain_last_error",
        "get_explanation",
        "FishertoolsError",
        "ExceptionExplanation",
        "ExplanationError",
        "FormattingError",
        "ConfigurationError",
        "PatternError",
        "SafeUtilityError",
        "safe_get",
        "safe_divide",
        "safe_read_file",
        "safe_write_file",
        "safe_file_exists",
        "safe_open",
    }
)


# Candidate names for lazy top-level loading in follow-up issue #32.
# These stay in the public facade for compatibility, but they do not need to be
# part of the minimal eager layer.
LAZY_TOP_LEVEL_EXPORTS: frozenset[str] = frozenset(
    {
        # Extended safe/file serialization helpers
        "safe_max",
        "safe_min",
        "safe_sum",
        "safe_get_file_size",
        "safe_list_files",
        "safe_read_json",
        "safe_write_json",
        "safe_read_yaml",
        "safe_write_yaml",
        "safe_read_toml",
        "safe_write_toml",
        "find_file",
        "project_root",
        # Visualization
        "visualize",
        "EnhancedVisualizer",
        "AlgorithmVisualizer",
        "VisualizationConfig",
        "VisualizationResult",
        # Learning/input/network/i18n convenience facade symbols
        "generate_example",
        "show_best_practice",
        "list_available_concepts",
        "list_available_topics",
        "ask_int",
        "ask_float",
        "ask_str",
        "ask_choice",
        "ask_yes_no",
        "ask_int_range",
        "ask_float_range",
        "ask_regex",
        "safe_request",
        "safe_download",
        "SafeHTTPClient",
        "SafeFileDownloader",
        "NetworkResponse",
        "DownloadResponse",
        "translate_error",
        "detect_language",
        "ErrorTranslator",
        "LanguageDetector",
        "ErrorExplanation",
    }
)


# Submodule-oriented names remain accessible on the facade, but consumers are
# encouraged to import them explicitly as submodules (e.g. ``import fishertools.safe``).
SUBMODULE_FACADE_EXPORTS: frozenset[str] = frozenset(
    {
        "utils",
        "decorators",
        "helpers",
        "errors",
        "safe",
        "learn",
        "legacy",
        "input_utils",
        "async_logger",
        "async_safe",
        "learning",
        "documentation",
        "examples",
        "config",
        "integration",
        "visualization",
        "validation",
        "debug",
        "network",
        "i18n",
    }
)


COMPATIBILITY_PLAN_NOTES: tuple[str, ...] = (
    "Issue #31 was a design-only step and did not change fishertools.__all__ at that time.",
    "Issue #32 may switch selected non-core top-level symbols to lazy dispatch without removing them.",
    "Submodule names remain stable facade exports for backward compatibility.",
    "Issue #36 contracts fishertools.__all__ to stable symbol exports while keeping submodule access via attributes.",
)
