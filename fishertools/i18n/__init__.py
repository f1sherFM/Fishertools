"""
Internationalization module for fishertools.

This module provides multilingual support for error explanations and other
user-facing messages, with automatic language detection and fallback behavior.

Main components:
    - ErrorTranslator: Multilingual error explanation system
    - LanguageDetector: System language detection
    - ErrorExplanation: Structured error explanation data
"""

from __future__ import annotations

from .models import ErrorExplanation
from .error_translator import (
    ErrorTranslator,
    translate_error,
    register_translation_provider,
    get_translation_providers,
)
from .language_detector import LanguageDetector, detect_language

__all__ = [
    # Core classes
    "ErrorTranslator",
    "LanguageDetector",
    
    # Convenience functions
    "translate_error",
    "detect_language",
    "register_translation_provider",
    "get_translation_providers",
    
    # Data models
    "ErrorExplanation",
]
