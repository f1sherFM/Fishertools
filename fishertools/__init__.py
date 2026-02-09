"""
Fishertools - инструменты, которые делают Python удобнее и безопаснее для новичков

Основная функция:
    explain_error() - объясняет ошибки Python в понятных словах

Модули:
    errors - система объяснения ошибок
    safe - безопасные утилиты для новичков
    learn - обучающие инструменты
    legacy - функции для обратной совместимости
"""

from __future__ import annotations

from ._version import __version__

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

# Visualization functions (existing + enhanced)
from .visualization import (
    visualize,  # Existing function
    EnhancedVisualizer,  # New enhanced visualizer
    AlgorithmVisualizer,  # New algorithm visualizer
    VisualizationConfig,  # Configuration model
    VisualizationResult,  # Result model
)

# Learning tools - educational functions
from .learn import (
    generate_example, show_best_practice, 
    list_available_concepts, list_available_topics
)

# Input validation functions
from .input_utils import (
    ask_int, ask_float, ask_str, ask_choice,
    ask_yes_no, ask_int_range, ask_float_range, ask_regex
)

# Legacy imports for backward compatibility
from . import utils
from . import decorators  
from . import helpers

# Module imports for advanced users who want to access specific modules
from . import errors
from . import safe
from . import learn
from . import legacy
from . import input_utils

# Async modules for async/await support
from . import async_logger
from . import async_safe

# New enhancement modules (fishertools-enhancements)
from . import learning
from . import documentation
from . import examples
from . import config
from . import integration

# Phase 1 modules (v0.5.1+)
from . import visualization
from . import validation
from . import debug

# Enhancement modules for safe network operations and i18n (v0.4.7+)
from . import network
from . import i18n

# Network operations - convenience functions
from .network import (
    safe_request,  # Safe HTTP requests
    safe_download,  # Safe file downloads
    SafeHTTPClient,  # HTTP client class
    SafeFileDownloader,  # File downloader class
    NetworkResponse,  # Response model
    DownloadResponse,  # Download response model
)

# Internationalization - multilingual support
from .i18n import (
    translate_error,  # Translate error messages
    detect_language,  # Detect system language
    ErrorTranslator,  # Error translator class
    LanguageDetector,  # Language detector class
    ErrorExplanation,  # Error explanation model
)

__all__ = [
    # Version information
    "get_version_info",
    
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

