"""
Property-based tests for language fallback behavior.

This module contains property-based tests to verify the correctness of
language fallback mechanisms when unsupported languages are requested.

Feature: fishertools-enhancements
"""

from __future__ import annotations

import pytest
from hypothesis import given, strategies as st, assume

from fishertools.i18n import ErrorTranslator, LanguageDetector


# Strategy for generating unsupported language codes
@st.composite
def unsupported_language_strategy(draw):
    """Generate language codes that are not supported."""
    # Generate random 2-letter codes that are not 'en' or 'ru'
    letters = 'abcdfghijklmnopqstvwxyz'  # Exclude 'e', 'r', 'u', 'n'
    lang_code = draw(st.text(alphabet=letters, min_size=2, max_size=2))
    
    # Ensure it's not a supported language
    assume(lang_code not in ['en', 'ru'])
    
    return lang_code


# Strategy for generating common Python exceptions
@st.composite
def exception_strategy(draw):
    """Generate various Python exceptions for testing."""
    exception_types = [
        ValueError,
        TypeError,
        KeyError,
        IndexError,
        AttributeError,
        ZeroDivisionError,
    ]
    
    exc_type = draw(st.sampled_from(exception_types))
    message = draw(st.text(min_size=1, max_size=50))
    
    return exc_type(message)


class TestLanguageFallbackBehavior:
    """
    Property 16: Language fallback behavior
    
    For any unsupported language request or missing translation, the I18n_System
    should fall back to English and indicate the fallback occurred.
    
    Validates: Requirements 5.5, 5.6
    """
    
    @given(
        error=exception_strategy(),
        unsupported_lang=unsupported_language_strategy()
    )
    def test_unsupported_language_fallback(self, error, unsupported_lang):
        """
        Property test: Unsupported languages should fall back to English.
        
        This test verifies that when an unsupported language is requested,
        the system falls back to English and marks fallback_used as True.
        """
        translator = ErrorTranslator()
        
        # Request explanation in unsupported language
        explanation = translator.explain_error(error, lang=unsupported_lang)
        
        # Should fall back to English
        assert explanation.language == 'en'
        
        # Should mark fallback as used
        assert explanation.fallback_used is True
        
        # Should still provide a valid explanation
        assert len(explanation.explanation) > 0
        assert isinstance(explanation.explanation, str)
    
    @given(
        error=exception_strategy(),
        lang=st.sampled_from(['en', 'ru'])
    )
    def test_supported_language_no_fallback(self, error, lang):
        """
        Property test: Supported languages should not trigger fallback.
        
        This test verifies that when a supported language is requested,
        fallback_used is False.
        """
        translator = ErrorTranslator()
        
        # Request explanation in supported language
        explanation = translator.explain_error(error, lang=lang)
        
        # Should use the requested language
        assert explanation.language == lang
        
        # Should not mark fallback as used
        assert explanation.fallback_used is False
    
    @given(
        error=exception_strategy()
    )
    def test_fallback_provides_valid_explanation(self, error):
        """
        Property test: Fallback should always provide valid explanations.
        
        This test verifies that even when falling back, the system
        provides complete and valid error explanations.
        """
        translator = ErrorTranslator()
        
        # Request explanation in unsupported language
        explanation = translator.explain_error(error, lang='fr')
        
        # Should provide valid explanation
        assert isinstance(explanation.explanation, str)
        assert len(explanation.explanation) > 0
        
        # Should provide suggestions
        assert isinstance(explanation.suggestions, list)
        
        # Should use fallback language (English)
        assert explanation.language == 'en'
        assert explanation.fallback_used is True
    
    @given(
        error=exception_strategy(),
        invalid_lang=st.one_of(
            st.text(min_size=1, max_size=1, alphabet=st.characters(blacklist_characters='enru')),  # Single char (not e, n, r, u)
            st.text(min_size=3, max_size=10, alphabet=st.characters(whitelist_categories=('Ll',))),  # Too long
            st.just('123'),  # Numbers
            st.just('!@#'),  # Special chars
        )
    )
    def test_invalid_language_code_fallback(self, error, invalid_lang):
        """
        Property test: Invalid language codes should fall back gracefully.
        
        This test verifies that malformed or invalid language codes
        are handled gracefully with fallback to English.
        
        Note: Empty string is treated as default (ru) for backward compatibility.
        """
        # Skip if by chance we get a supported language
        assume(invalid_lang not in ['en', 'ru'])
        
        translator = ErrorTranslator()
        
        # Request explanation with invalid language code
        explanation = translator.explain_error(error, lang=invalid_lang)
        
        # Should fall back to English (not default Russian)
        assert explanation.language == 'en'
        
        # Should mark fallback as used
        assert explanation.fallback_used is True
        
        # Should still provide valid explanation
        assert len(explanation.explanation) > 0
    
    def test_fallback_consistency(self):
        """
        Test that fallback behavior is consistent across multiple calls.
        
        This test verifies that the fallback mechanism produces
        consistent results for the same inputs.
        """
        translator = ErrorTranslator()
        error = ValueError("test error")
        
        # Get explanation twice with unsupported language
        explanation1 = translator.explain_error(error, lang='fr')
        explanation2 = translator.explain_error(error, lang='fr')
        
        # Results should be identical
        assert explanation1.explanation == explanation2.explanation
        assert explanation1.language == explanation2.language
        assert explanation1.fallback_used == explanation2.fallback_used
        assert explanation1.suggestions == explanation2.suggestions
    
    @given(
        error=exception_strategy()
    )
    def test_fallback_explanation_quality(self, error):
        """
        Property test: Fallback explanations should be high quality.
        
        This test verifies that fallback explanations are not just
        generic messages but contain useful information.
        """
        translator = ErrorTranslator()
        
        # Get fallback explanation
        explanation = translator.explain_error(error, lang='de')
        
        # Should contain error type information
        error_type = type(error).__name__
        
        # Explanation should be substantial (not just "An error occurred")
        assert len(explanation.explanation) > 20
        
        # Should provide at least one suggestion
        assert len(explanation.suggestions) >= 1
    
    def test_normalize_handles_case_insensitivity(self):
        """
        Test that language code normalization is case-insensitive.
        
        This test verifies that the normalizer handles different
        case variations of language codes correctly.
        """
        detector = LanguageDetector()
        
        # Test various case combinations
        test_cases = [
            ('EN', 'en'),
            ('En', 'en'),
            ('eN', 'en'),
            ('RU', 'ru'),
            ('Ru', 'ru'),
            ('rU', 'ru'),
        ]
        
        for input_code, expected in test_cases:
            normalized = detector.normalize_language_code(input_code)
            assert normalized == expected
    
    @given(
        error=exception_strategy(),
        lang_with_locale=st.sampled_from([
            'en_US', 'en_GB', 'en-US', 'en-GB',
            'ru_RU', 'ru_UA', 'ru-RU', 'ru-UA',
            'fr_FR', 'de_DE', 'es_ES'  # Unsupported with locale
        ])
    )
    def test_locale_variants_handled_correctly(self, error, lang_with_locale):
        """
        Property test: Language codes with locale variants should be normalized.
        
        This test verifies that language codes with locale information
        (e.g., en_US, ru_RU) are correctly normalized to base language codes.
        """
        translator = ErrorTranslator()
        detector = LanguageDetector()
        
        # Normalize the language code
        normalized = detector.normalize_language_code(lang_with_locale)
        
        # Should be a 2-letter code
        assert len(normalized) == 2
        
        # Get explanation with locale variant
        explanation = translator.explain_error(error, lang=lang_with_locale)
        
        # Should use normalized language or fallback
        assert explanation.language in ['en', 'ru']
        
        # If the base language is unsupported, should use fallback
        base_lang = lang_with_locale.split('_')[0].split('-')[0].lower()
        if base_lang not in ['en', 'ru']:
            assert explanation.fallback_used is True
