"""
Unit tests for default Russian behavior in i18n module.

This module tests that the default behavior (without language parameter)
uses Russian language for backward compatibility.

Feature: fishertools-enhancements
Validates: Requirements 5.1
"""

from __future__ import annotations

import pytest

from fishertools.i18n import ErrorTranslator


class TestDefaultRussianBehavior:
    """
    Unit tests for default Russian behavior.
    
    These tests verify that explain_error() without language parameter
    uses Russian as the default language, maintaining backward compatibility.
    
    Validates: Requirements 5.1
    """
    
    def test_default_language_is_russian(self):
        """
        Test that explain_error() without language parameter uses Russian.
        
        This test verifies backward compatibility - the default behavior
        should use Russian language.
        """
        translator = ErrorTranslator()
        error = ValueError("test error")
        
        # Call without language parameter (should default to 'ru')
        explanation = translator.explain_error(error)
        
        # Should use Russian
        assert explanation.language == 'ru'
        
        # Should not mark fallback as used (Russian is the default)
        assert explanation.fallback_used is False
    
    def test_explicit_russian_parameter(self):
        """
        Test that explicitly passing 'ru' works correctly.
        
        This test verifies that explicitly requesting Russian language
        produces the same result as the default behavior.
        """
        translator = ErrorTranslator()
        error = TypeError("test error")
        
        # Call with explicit 'ru' parameter
        explanation = translator.explain_error(error, lang='ru')
        
        # Should use Russian
        assert explanation.language == 'ru'
        
        # Should not mark fallback as used
        assert explanation.fallback_used is False
    
    def test_russian_explanation_contains_cyrillic(self):
        """
        Test that Russian explanations contain Cyrillic characters.
        
        This test verifies that Russian explanations are actually in Russian
        and not just English with a 'ru' label.
        """
        translator = ErrorTranslator()
        
        # Test with common error types
        error_types = [
            ValueError("test"),
            TypeError("test"),
            KeyError("test"),
            IndexError("test"),
            ZeroDivisionError("test"),
        ]
        
        for error in error_types:
            explanation = translator.explain_error(error, lang='ru')
            
            # Should contain Cyrillic characters
            has_cyrillic = any(
                '\u0400' <= char <= '\u04FF' 
                for char in explanation.explanation
            )
            assert has_cyrillic, f"Russian explanation for {type(error).__name__} should contain Cyrillic"
    
    def test_russian_suggestions_are_in_russian(self):
        """
        Test that Russian suggestions contain Cyrillic characters.
        
        This test verifies that suggestions are also translated to Russian.
        """
        translator = ErrorTranslator()
        error = ValueError("test error")
        
        explanation = translator.explain_error(error, lang='ru')
        
        # Should have suggestions
        assert len(explanation.suggestions) > 0
        
        # At least one suggestion should contain Cyrillic
        has_cyrillic_suggestion = any(
            any('\u0400' <= char <= '\u04FF' for char in suggestion)
            for suggestion in explanation.suggestions
        )
        assert has_cyrillic_suggestion, "Russian suggestions should contain Cyrillic"
    
    def test_default_vs_explicit_russian_consistency(self):
        """
        Test that default behavior matches explicit Russian parameter.
        
        This test verifies that calling without parameter and calling with
        lang='ru' produce identical results.
        """
        translator = ErrorTranslator()
        error = AttributeError("test error")
        
        # Get explanation with default (no parameter)
        default_explanation = translator.explain_error(error)
        
        # Get explanation with explicit 'ru'
        explicit_explanation = translator.explain_error(error, lang='ru')
        
        # Results should be identical
        assert default_explanation.explanation == explicit_explanation.explanation
        assert default_explanation.language == explicit_explanation.language
        assert default_explanation.suggestions == explicit_explanation.suggestions
        assert default_explanation.fallback_used == explicit_explanation.fallback_used
    
    def test_russian_error_types_coverage(self):
        """
        Test that Russian translations exist for common error types.
        
        This test verifies that the most common Python error types have
        Russian translations available.
        """
        translator = ErrorTranslator()
        
        # Common error types that should have Russian translations
        common_errors = [
            ValueError("test"),
            TypeError("test"),
            KeyError("test"),
            IndexError("test"),
            AttributeError("test"),
            ZeroDivisionError("test"),
            FileNotFoundError("test"),
            ImportError("test"),
            NameError("test"),
        ]
        
        for error in common_errors:
            explanation = translator.explain_error(error, lang='ru')
            
            # Should have non-empty explanation
            assert len(explanation.explanation) > 0
            
            # Should have suggestions
            assert len(explanation.suggestions) > 0
            
            # Should be in Russian
            assert explanation.language == 'ru'
    
    def test_backward_compatibility_with_existing_code(self):
        """
        Test backward compatibility with existing fishertools usage.
        
        This test simulates how existing code might use the error translator
        and verifies it still works as expected.
        """
        # Simulate existing code that doesn't specify language
        translator = ErrorTranslator()
        
        try:
            # Simulate an error
            result = 10 / 0
        except ZeroDivisionError as e:
            explanation = translator.explain_error(e)
            
            # Should work without errors
            assert explanation is not None
            assert explanation.language == 'ru'
            assert len(explanation.explanation) > 0
            assert len(explanation.suggestions) > 0
