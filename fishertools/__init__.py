"""
Fishertools - practical tools for writing safer, clearer Python code.

Main function:
    explain_error() - explains Python exceptions in beginner-friendly terms.

Modules:
    errors - exception explanation system
    safe - safer utility helpers
    learn - educational helpers and examples
    legacy - backward compatibility utilities
"""
from __future__ import annotations

import importlib

from ._version import __version__
from .api_mode import set_api_mode, get_api_mode, api_mode
from ._import_facade_contract import MINIMAL_EAGER_EXPORTS

__author__ = "f1sherFM"


def get_version_info() -> dict:
    """
    Get detailed version information about fishertools
    
    Returns:
        dict: Dictionary containing version, author, and feature information
        
    Example:
        >>> info = get_version_info()
        >>> print(f"Fishertools v{info['version']}")
        >>> print(f"Features: {', '.join(info['features'])}")
    """
    return {
        "version": __version__,
        "author": __author__,
        "features": [
            "error_explanations",
            "safe_utilities",
            "visualization",
            "learning_tools",
            "input_validation",
            "network_operations",  # New in v0.4.7
            "internationalization",  # New in v0.4.7
            "algorithm_visualization",  # New in v0.4.7
        ],
        "enhancements": {
            "v0.4.7": [
                "Safe HTTP request operations with timeout handling",
                "Safe file download with progress tracking",
                "Enhanced visualization with colors and export",
                "Algorithm visualization (sorting, searching)",
                "Multilingual error explanations (Russian, English)",
                "Configuration management system",
            ]
        }
    }


# Primary API - main interface for users
from .errors import explain_error, explain_last_error, get_explanation

# Exception classes for error handling
from .errors import (
    FishertoolsError, ExceptionExplanation, ExplanationError, FormattingError, 
    ConfigurationError, PatternError, SafeUtilityError
)

# Safe utilities - commonly used beginner-friendly functions
from .safe import (
    safe_get, safe_divide, safe_max, safe_min, safe_sum,
    safe_read_file, safe_write_file, safe_file_exists, 
    safe_get_file_size, safe_list_files,
    safe_read_json, safe_write_json, safe_read_yaml, safe_write_yaml, safe_read_toml, safe_write_toml,
    safe_open, find_file, project_root
)

_LAZY_SUBMODULES = {
    # Legacy imports for backward compatibility
    "utils", "decorators", "helpers",
    # Module imports for advanced users
    "errors", "safe", "learn", "legacy", "input_utils",
    # Async modules
    "async_logger", "async_safe",
    # Enhancement modules
    "learning", "documentation", "examples", "config", "integration",
    # Phase 1 modules
    "visualization", "validation", "debug",
    # Network/i18n
    "network", "i18n",
}

_LAZY_SYMBOL_SOURCES = {
    # Safe helpers that are non-core for onboarding.
    "safe_max": ("safe", "safe_max"),
    "safe_min": ("safe", "safe_min"),
    "safe_sum": ("safe", "safe_sum"),
    "safe_get_file_size": ("safe", "safe_get_file_size"),
    "safe_list_files": ("safe", "safe_list_files"),
    "safe_read_json": ("safe", "safe_read_json"),
    "safe_write_json": ("safe", "safe_write_json"),
    "safe_read_yaml": ("safe", "safe_read_yaml"),
    "safe_write_yaml": ("safe", "safe_write_yaml"),
    "safe_read_toml": ("safe", "safe_read_toml"),
    "safe_write_toml": ("safe", "safe_write_toml"),
    "find_file": ("safe", "find_file"),
    "project_root": ("safe", "project_root"),
    # Visualization
    "visualize": ("visualization", "visualize"),
    "EnhancedVisualizer": ("visualization", "EnhancedVisualizer"),
    "AlgorithmVisualizer": ("visualization", "AlgorithmVisualizer"),
    "VisualizationConfig": ("visualization", "VisualizationConfig"),
    "VisualizationResult": ("visualization", "VisualizationResult"),
    # Learning tools
    "generate_example": ("learn", "generate_example"),
    "show_best_practice": ("learn", "show_best_practice"),
    "list_available_concepts": ("learn", "list_available_concepts"),
    "list_available_topics": ("learn", "list_available_topics"),
    # Input utilities
    "ask_int": ("input_utils", "ask_int"),
    "ask_float": ("input_utils", "ask_float"),
    "ask_str": ("input_utils", "ask_str"),
    "ask_choice": ("input_utils", "ask_choice"),
    "ask_yes_no": ("input_utils", "ask_yes_no"),
    "ask_int_range": ("input_utils", "ask_int_range"),
    "ask_float_range": ("input_utils", "ask_float_range"),
    "ask_regex": ("input_utils", "ask_regex"),
    # Network convenience
    "safe_request": ("network", "safe_request"),
    "safe_download": ("network", "safe_download"),
    "SafeHTTPClient": ("network", "SafeHTTPClient"),
    "SafeFileDownloader": ("network", "SafeFileDownloader"),
    "NetworkResponse": ("network", "NetworkResponse"),
    "DownloadResponse": ("network", "DownloadResponse"),
    # i18n convenience
    "translate_error": ("i18n", "translate_error"),
    "detect_language": ("i18n", "detect_language"),
    "ErrorTranslator": ("i18n", "ErrorTranslator"),
    "LanguageDetector": ("i18n", "LanguageDetector"),
    "ErrorExplanation": ("i18n", "ErrorExplanation"),
}


def __getattr__(name: str):
    """Lazily import selected submodules/symbols while preserving the public API."""
    if name in _LAZY_SYMBOL_SOURCES and name not in MINIMAL_EAGER_EXPORTS:
        module_name, attr_name = _LAZY_SYMBOL_SOURCES[name]
        module = importlib.import_module(f".{module_name}", __name__)
        value = getattr(module, attr_name)
        globals()[name] = value
        return value
    if name in _LAZY_SUBMODULES:
        module = importlib.import_module(f".{name}", __name__)
        globals()[name] = module
        return module
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    # Version information
    "get_version_info",
    "set_api_mode", "get_api_mode", "api_mode",
    
    # Primary API - the main function users should import
    "explain_error",
    "explain_last_error",
    "get_explanation",  # New in v0.4.7
    
    # Exception classes for error handling
    "FishertoolsError", "ExceptionExplanation", "ExplanationError", "FormattingError", 
    "ConfigurationError", "PatternError", "SafeUtilityError",
    
    # Safe utilities - direct access to commonly used functions
    "safe_get", "safe_divide", "safe_max", "safe_min", "safe_sum",
    "safe_read_file", "safe_write_file", "safe_file_exists", 
    "safe_get_file_size", "safe_list_files",
    "safe_read_json", "safe_write_json", "safe_read_yaml", "safe_write_yaml", "safe_read_toml", "safe_write_toml",
    "safe_open", "find_file", "project_root",
    
    # Visualization functions (existing + enhanced)
    "visualize",
    "EnhancedVisualizer",
    "AlgorithmVisualizer",
    "VisualizationConfig",
    "VisualizationResult",
    
    # Input validation functions
    "ask_int", "ask_float", "ask_str", "ask_choice",
    "ask_yes_no", "ask_int_range", "ask_float_range", "ask_regex",
    
    # Learning tools - direct access to educational functions
    "generate_example", "show_best_practice", 
    "list_available_concepts", "list_available_topics",
    
    # Legacy modules for backward compatibility
    "utils", "decorators", "helpers",
    
    # New modules for advanced usage
    "errors", "safe", "learn", "legacy", "input_utils",
    
    # Async modules for async/await support
    "async_logger", "async_safe",
    
    # Enhancement modules (fishertools-enhancements)
    "learning", "documentation", "examples", "config", "integration",
    
    # Phase 1 modules (v0.4.1+)
    "visualization", "validation", "debug",
    
    # Enhancement modules for safe network operations and i18n (v0.4.7+)
    "network", "i18n",
    
    # Network operations - convenience functions
    "safe_request", "safe_download",
    "SafeHTTPClient", "SafeFileDownloader",
    "NetworkResponse", "DownloadResponse",
    
    # Internationalization - multilingual support
    "translate_error", "detect_language",
    "ErrorTranslator", "LanguageDetector",
    "ErrorExplanation",
]

