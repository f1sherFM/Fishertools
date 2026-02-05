"""
Property-based tests for language detection.

This module contains property-based tests to verify the correctness of
system language detection functionality.

Feature: fishertools-enhancements
"""

from __future__ import annotations

import locale
import pytest
from hypothesis import given, strategies as st, assume
from unittest.mock import patch

from fishertools.i18n import LanguageDetector


class TestLanguageDetection:
    """
    Property 15: Language detection
    
    For any system with detectable locale settings, calling explain_error()
    with lang='auto' should use the appropriate language based on system settings.
    
    Validates: Requirements 5.4
    """
    
    @given(
        locale_code=st.sampled_from([
            'en_US', 'en_GB', 'en_CA', 'en_AU',
            'ru_RU', 'ru_UA',
            'fr_FR', 'de_DE', 'es_ES', 'it_IT',
            'zh_CN', 'ja_JP', 'ko_KR'
        ])
    )
    def test_language_detection_with_various_locales(self, locale_code):
        """
        Property test: Language detection should work with various locale codes.
        
        This test verifies that the language detector can handle different
        locale formats and extract the correct language code.
        """
        detector = LanguageDetector()
        
        # Mock the locale.getdefaultlocale to return our test locale
        with patch('locale.getdefaultlocale', return_value=(locale_code, 'UTF-8')):
            detected_lang = detector.detect_system_language()
        
        # Verify the result is a valid language code
        assert isinstance(detected_lang, str)
        assert len(detected_lang) == 2  # Should be 2-letter code
        
        # Verify it's either a supported language or the default
        assert detected_lang in detector.SUPPORTED_LANGUAGES or \
               detected_lang == detector.DEFAULT_LANGUAGE
    
    def test_language_detection_returns_supported_language(self):
        """
        Test that language detection always returns a supported language.
        
        This test verifies that the detector never returns an unsupported
        language code, even with unusual system settings.
        """
        detector = LanguageDetector()
        
        # Test with various mock locales
        test_locales = [
            ('en_US', 'UTF-8'),
            ('ru_RU', 'UTF-8'),
            ('fr_FR', 'UTF-8'),  # Unsupported
            ('de_DE', 'UTF-8'),  # Unsupported
            (None, None),        # No locale
            ('', ''),            # Empty locale
        ]
        
        for locale_tuple in test_locales:
            with patch('locale.getdefaultlocale', return_value=locale_tuple):
                detected_lang = detector.detect_system_language()
                
                # Should always return a supported language or default
                assert detected_lang in detector.SUPPORTED_LANGUAGES or \
                       detected_lang == detector.DEFAULT_LANGUAGE
    
    def test_language_detection_handles_errors_gracefully(self):
        """
        Test that language detection handles errors gracefully.
        
        This test verifies that the detector returns the default language
        when locale detection fails.
        """
        detector = LanguageDetector()
        
        # Mock locale.getdefaultlocale to raise an exception
        with patch('locale.getdefaultlocale', side_effect=locale.Error("Test error")):
            detected_lang = detector.detect_system_language()
        
        # Should return default language on error
        assert detected_lang == detector.DEFAULT_LANGUAGE
    
    @given(
        lang_code=st.text(min_size=2, max_size=10, alphabet=st.characters(whitelist_categories=('Ll', 'Lu')))
    )
    def test_is_language_supported_property(self, lang_code):
        """
        Property test: is_language_supported should correctly identify supported languages.
        
        This test verifies that the method correctly identifies whether
        a language code is supported.
        """
        detector = LanguageDetector()
        
        result = detector.is_language_supported(lang_code)
        
        # Result should be boolean
        assert isinstance(result, bool)
        
        # If result is True, the language should be in SUPPORTED_LANGUAGES
        if result:
            assert lang_code.lower() in detector.SUPPORTED_LANGUAGES
    
    @given(
        lang_code=st.sampled_from([
            'en', 'EN', 'En', 'eN',
            'ru', 'RU', 'Ru', 'rU',
            'en_US', 'en-US', 'en_GB', 'en-GB',
            'ru_RU', 'ru-RU', 'ru_UA', 'ru-UA'
        ])
    )
    def test_normalize_language_code_property(self, lang_code):
        """
        Property test: normalize_language_code should handle various formats.
        
        This test verifies that the normalizer can handle different
        language code formats and produce consistent output.
        """
        detector = LanguageDetector()
        
        normalized = detector.normalize_language_code(lang_code)
        
        # Normalized code should be lowercase
        assert normalized.islower()
        
        # Normalized code should be 2 characters
        assert len(normalized) == 2
        
        # Normalized code should be either supported or fallback
        assert normalized in detector.SUPPORTED_LANGUAGES or \
               normalized == detector.FALLBACK_LANGUAGE
    
    def test_normalize_handles_empty_and_none(self):
        """
        Test that normalize_language_code handles empty and None values.
        
        This test verifies that the normalizer returns the default language
        for invalid inputs.
        """
        detector = LanguageDetector()
        
        # Test with None
        assert detector.normalize_language_code(None) == detector.DEFAULT_LANGUAGE
        
        # Test with empty string
        assert detector.normalize_language_code('') == detector.DEFAULT_LANGUAGE
    
    @given(
        error=st.sampled_from([
            ValueError("test"),
            TypeError("test"),
            KeyError("test")
        ])
    )
    def test_auto_language_detection_integration(self, error):
        """
        Property test: 'auto' language detection should work with error translator.
        
        This test verifies that the 'auto' language parameter correctly
        triggers language detection.
        """
        from fishertools.i18n import ErrorTranslator
        
        translator = ErrorTranslator()
        
        # Get explanation with 'auto' language
        explanation = translator.explain_error(error, lang='auto')
        
        # Should return a valid explanation
        assert isinstance(explanation.explanation, str)
        assert len(explanation.explanation) > 0
        
        # Language should be one of the supported languages
        assert explanation.language in translator.language_detector.SUPPORTED_LANGUAGES
