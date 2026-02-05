"""
Multilingual error explanation system.

This module provides functionality to translate error messages and explanations
into different languages with automatic fallback behavior.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, Optional

from .models import ErrorExplanation
from .language_detector import LanguageDetector


class ErrorTranslator:
    """
    Translates error messages and explanations to different languages.
    
    This class provides a system for translating error messages using gettext
    or similar translation infrastructure, with automatic language detection
    and fallback behavior.
    
    Attributes:
        language_detector: Language detector for automatic language selection
    """
    
    def __init__(self):
        """Initialize the error translator."""
        self.language_detector = LanguageDetector()
        self._translations: Dict[str, Dict] = {}
        self._load_translations()
    
    def explain_error(
        self,
        error: Exception,
        lang: str = 'ru'
    ) -> ErrorExplanation:
        """
        Provide error explanation in the specified language.
        
        This method generates a human-readable explanation of an error in the
        requested language, with automatic fallback if the language is not
        supported or translations are missing.
        
        Args:
            error: The exception to explain
            lang: Language code ('en', 'ru', or 'auto' for detection)
        
        Returns:
            ErrorExplanation with translated text and suggestions
        """
        # Store original language for fallback detection
        original_lang = lang
        
        # Handle 'auto' language detection
        if lang == 'auto':
            lang = self.language_detector.detect_system_language()
            original_lang = lang  # Don't mark auto-detection as fallback
        
        # Check if language is supported before normalization
        fallback_used = False
        if not self.language_detector.is_language_supported(lang):
            # Mark that we're using fallback
            fallback_used = True
        
        # Normalize the language code (this may also trigger fallback)
        normalized_lang = self.language_detector.normalize_language_code(lang)
        
        # If normalization changed the language to fallback, mark it
        if not fallback_used and normalized_lang != lang.lower().split('_')[0].split('-')[0]:
            if not self.language_detector.is_language_supported(lang.lower().split('_')[0].split('-')[0]):
                fallback_used = True
        
        lang = normalized_lang
        
        # Get error type
        error_type = type(error).__name__
        
        # Get explanation template and format it
        template = self._get_error_template(error_type, lang)
        explanation = self._format_error_explanation(template, error)
        
        # Get suggestions
        suggestions = self._get_suggestions(error_type, lang)
        
        return ErrorExplanation(
            explanation=explanation,
            language=lang,
            suggestions=suggestions,
            fallback_used=fallback_used
        )
    
    def _get_error_template(self, error_type: str, language: str) -> str:
        """
        Get error explanation template for a specific error type.
        
        Args:
            error_type: Type of error (e.g., 'ValueError', 'TypeError')
            language: Target language code
        
        Returns:
            Error explanation template string
        """
        # Get translations for the language
        lang_translations = self._translations.get(language, {})
        
        # Try to get specific error type template
        error_data = lang_translations.get(error_type)
        if error_data:
            return error_data.get('explanation', '')
        
        # Fall back to generic template
        generic_data = lang_translations.get('generic', {})
        return generic_data.get('explanation', 'An error occurred: {error_type}')
    
    def _format_error_explanation(
        self,
        template: str,
        error: Exception
    ) -> str:
        """
        Format error explanation with specific error details.
        
        Args:
            template: Error explanation template
            error: The exception with specific details
        
        Returns:
            Formatted error explanation
        """
        error_type = type(error).__name__
        error_message = str(error)
        
        # Format the template with error details
        try:
            formatted = template.format(
                error_type=error_type,
                error_message=error_message
            )
            return formatted
        except (KeyError, ValueError):
            # If formatting fails, return template as-is
            return template
    
    def _load_translations(self) -> None:
        """
        Load translation files from the locales directory.
        
        This method loads JSON translation files for all supported languages.
        """
        # Get the path to the locales directory
        locales_dir = Path(__file__).parent / 'locales'
        
        # Load translations for each supported language
        for lang in self.language_detector.SUPPORTED_LANGUAGES:
            lang_file = locales_dir / lang / 'errors.json'
            
            if lang_file.exists():
                try:
                    with open(lang_file, 'r', encoding='utf-8') as f:
                        self._translations[lang] = json.load(f)
                except (json.JSONDecodeError, IOError):
                    # If loading fails, use empty dict for this language
                    self._translations[lang] = {}
            else:
                self._translations[lang] = {}
    
    def _get_suggestions(self, error_type: str, language: str) -> list:
        """
        Get fix suggestions for a specific error type.
        
        Args:
            error_type: Type of error (e.g., 'ValueError', 'TypeError')
            language: Target language code
        
        Returns:
            List of suggestion strings
        """
        # Get translations for the language
        lang_translations = self._translations.get(language, {})
        
        # Try to get specific error type suggestions
        error_data = lang_translations.get(error_type)
        if error_data and 'suggestions' in error_data:
            return error_data['suggestions']
        
        # Fall back to generic suggestions
        generic_data = lang_translations.get('generic', {})
        return generic_data.get('suggestions', [])


# Convenience function for one-off translations
def translate_error(
    error: Exception,
    lang: str = 'ru'
) -> ErrorExplanation:
    """
    Translate an error without creating a translator instance.
    
    This is a convenience function for one-off error translations.
    
    Args:
        error: The exception to explain
        lang: Language code ('en', 'ru', or 'auto' for detection)
    
    Returns:
        ErrorExplanation with translated text and suggestions
    """
    translator = ErrorTranslator()
    return translator.explain_error(error, lang)
