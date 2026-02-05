"""
Property-based tests for i18n error translator.

This module contains property-based tests to verify the correctness of
multilingual error explanation functionality.

Feature: fishertools-enhancements
"""

from __future__ import annotations

import pytest
from hypothesis import given, strategies as st, assume

from fishertools.i18n import ErrorTranslator, ErrorExplanation


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
        FileNotFoundError,
        ImportError,
        NameError,
    ]
    
    exc_type = draw(st.sampled_from(exception_types))
    message = draw(st.text(min_size=1, max_size=100))
    
    return exc_type(message)


class TestMultilingualErrorSupport:
    """
    Property 14: Multilingual error support
    
    For any error and supported language code (en, ru), explain_error()
    should return an ErrorExplanation in the requested language.
    
    Validates: Requirements 5.2, 5.3
    """
    
    @given(
        error=exception_strategy(),
        lang=st.sampled_from(['en', 'ru'])
    )
    def test_multilingual_error_support(self, error, lang):
        """
        Property test: Error explanations should be provided in requested language.
        
        This test verifies that for any error and supported language,
        the translator returns an explanation in the correct language.
        """
        translator = ErrorTranslator()
        
        # Get explanation in requested language
        explanation = translator.explain_error(error, lang=lang)
        
        # Verify the result is an ErrorExplanation
        assert isinstance(explanation, ErrorExplanation)
        
        # Verify the language matches the request
        assert explanation.language == lang
        
        # Verify explanation is not empty
        assert len(explanation.explanation) > 0
        
        # Verify explanation is a string
        assert isinstance(explanation.explanation, str)
        
        # Verify suggestions is a list
        assert isinstance(explanation.suggestions, list)
        
        # Verify fallback_used is a boolean
        assert isinstance(explanation.fallback_used, bool)
    
    @given(
        error=exception_strategy()
    )
    def test_english_explanation_content(self, error):
        """
        Test that English explanations contain English text.
        
        This test verifies that English explanations use English language
        patterns and don't contain Cyrillic characters.
        """
        translator = ErrorTranslator()
        explanation = translator.explain_error(error, lang='en')
        
        # English explanations should not contain Cyrillic characters
        cyrillic_pattern = any(
            '\u0400' <= char <= '\u04FF' 
            for char in explanation.explanation
        )
        assert not cyrillic_pattern, "English explanation contains Cyrillic characters"
    
    @given(
        error=exception_strategy()
    )
    def test_russian_explanation_content(self, error):
        """
        Test that Russian explanations contain Russian text.
        
        This test verifies that Russian explanations use Cyrillic characters
        as expected for Russian language content.
        """
        translator = ErrorTranslator()
        explanation = translator.explain_error(error, lang='ru')
        
        # Russian explanations should contain Cyrillic characters
        # (at least in common error types)
        error_type = type(error).__name__
        
        # For known error types, verify Cyrillic presence
        known_types = [
            'ValueError', 'TypeError', 'KeyError', 'IndexError',
            'AttributeError', 'ZeroDivisionError', 'FileNotFoundError',
            'ImportError', 'NameError'
        ]
        
        if error_type in known_types:
            cyrillic_pattern = any(
                '\u0400' <= char <= '\u04FF' 
                for char in explanation.explanation
            )
            assert cyrillic_pattern, f"Russian explanation for {error_type} should contain Cyrillic"
    
    @given(
        error=exception_strategy(),
        lang=st.sampled_from(['en', 'ru'])
    )
    def test_suggestions_are_strings(self, error, lang):
        """
        Test that all suggestions are non-empty strings.
        
        This test verifies that suggestions are properly formatted
        and contain useful information.
        """
        translator = ErrorTranslator()
        explanation = translator.explain_error(error, lang=lang)
        
        # All suggestions should be non-empty strings
        for suggestion in explanation.suggestions:
            assert isinstance(suggestion, str)
            assert len(suggestion) > 0
    
    @given(
        error=exception_strategy()
    )
    def test_consistency_across_calls(self, error):
        """
        Test that multiple calls with same error produce consistent results.
        
        This test verifies that the translator is deterministic and
        produces the same explanation for the same error.
        """
        translator = ErrorTranslator()
        
        # Get explanation twice
        explanation1 = translator.explain_error(error, lang='en')
        explanation2 = translator.explain_error(error, lang='en')
        
        # Results should be identical
        assert explanation1.explanation == explanation2.explanation
        assert explanation1.language == explanation2.language
        assert explanation1.suggestions == explanation2.suggestions
        assert explanation1.fallback_used == explanation2.fallback_used
