"""
System language detection for automatic localization.

This module provides functionality to detect the user's system language
settings and determine the appropriate language for error messages.
"""

from __future__ import annotations

import locale
from typing import Optional


class LanguageDetector:
    """
    Detects system language settings for automatic localization.
    
    This class provides methods to detect the user's system language and
    determine which language should be used for error messages and other
    user-facing text.
    """
    
    # Supported language codes
    SUPPORTED_LANGUAGES = {'en', 'ru'}
    DEFAULT_LANGUAGE = 'ru'  # Maintain backward compatibility
    FALLBACK_LANGUAGE = 'en'
    
    def detect_system_language(self, default: Optional[str] = None) -> str:
        """
        Detect the system language using locale settings.
        
        This method attempts to detect the user's system language by checking
        locale settings. If detection fails or the language is not supported,
        it returns the default language.
        
        Args:
            default: Fallback language if detection fails or unsupported.
                If None, uses DEFAULT_LANGUAGE.

        Returns:
            Language code (e.g., 'en', 'ru')
        """
        fallback = self.normalize_language_code(default) if default else self.DEFAULT_LANGUAGE
        try:
            # locale.getdefaultlocale() is deprecated (Python 3.15+),
            # so we prefer getlocale() and keep a conservative fallback.
            lang_code = None
            locale_info = locale.getlocale()
            if locale_info:
                lang_code = locale_info[0]

            if not lang_code:
                current_locale = locale.setlocale(locale.LC_CTYPE, None)
                if current_locale:
                    lang_code = current_locale
            
            if lang_code:
                # Normalize and check if supported
                normalized = self.normalize_language_code(lang_code, fallback=fallback)
                if self.is_language_supported(normalized):
                    return normalized
            
            # If detection failed or unsupported, return default
            return fallback
            
        except (ValueError, TypeError, locale.Error):
            # If any error occurs during detection, return default
            return fallback

    def is_language_supported(self, lang_code: Optional[str]) -> bool:
        """
        Check if a language is supported.
        
        Args:
            lang_code: Language code to check (e.g., 'en', 'ru')
        
        Returns:
            True if the language is supported, False otherwise
        """
        if not isinstance(lang_code, str):
            return False
        return lang_code.lower() in self.SUPPORTED_LANGUAGES

    def normalize_language_code(
        self,
        lang_code: Optional[str],
        fallback: Optional[str] = None
    ) -> str:
        """
        Normalize a language code to a standard format.
        
        This method handles various language code formats (e.g., 'en_US', 'en-US')
        and normalizes them to a simple two-letter code.
        
        Args:
            lang_code: Language code to normalize
        
        Returns:
            Normalized language code (e.g., 'en', 'ru')
        """
        resolved_fallback = (
            fallback
            if fallback in self.SUPPORTED_LANGUAGES
            else self.DEFAULT_LANGUAGE
        )
        if not lang_code:
            return resolved_fallback
        
        # Extract the base language code (first two letters)
        base_code = lang_code.lower().split('_')[0].split('-')[0]
        
        # Return the base code if supported, otherwise return fallback
        return base_code if self.is_language_supported(base_code) else resolved_fallback


# Convenience function for one-off language detection
def detect_language(
    lang_code: Optional[str] = None,
    default: str = LanguageDetector.DEFAULT_LANGUAGE
) -> str:
    """
    Detect the system language without creating a detector instance.
    
    This is a convenience function for one-off language detection.
    
    Args:
        lang_code: Optional explicit locale/language code to normalize.
            If omitted, detects from system locale.
        default: Fallback language if detection/normalization fails.

    Returns:
        Language code (e.g., 'en', 'ru')
    """
    detector = LanguageDetector()
    normalized_default = detector.normalize_language_code(default)
    if lang_code is not None:
        return detector.normalize_language_code(lang_code, fallback=normalized_default)
    return detector.detect_system_language(default=normalized_default)
