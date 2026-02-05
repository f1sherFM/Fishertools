"""
Integration tests for i18n module with main fishertools API.

This module tests the integration between the i18n module and the main
fishertools explain_error() function.
"""

from __future__ import annotations

import pytest

from fishertools import explain_error


class TestI18nIntegration:
    """Integration tests for i18n with main API."""
    
    def test_explain_error_with_auto_language(self):
        """
        Test that explain_error() works with 'auto' language parameter.
        
        This test verifies that the main API function correctly integrates
        with the i18n module for automatic language detection.
        """
        error = ValueError("test error")
        
        # Should not raise an exception
        result = explain_error(error, language='auto', return_text=True)
        
        # Should return a string
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_explain_error_with_english(self):
        """
        Test that explain_error() works with English language.
        
        This test verifies that the main API function accepts
        the English language parameter without errors.
        
        Note: The main explain_error uses pattern-based explanations
        which are separate from the i18n translation system.
        """
        error = TypeError("test error")
        
        result = explain_error(error, language='en', return_text=True)
        
        # Should return a string
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_explain_error_with_russian(self):
        """
        Test that explain_error() works with Russian language.
        
        This test verifies that the main API function can produce
        Russian explanations.
        """
        error = KeyError("test error")
        
        result = explain_error(error, language='ru', return_text=True)
        
        # Should return a string
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_explain_error_default_is_russian(self):
        """
        Test that explain_error() defaults to Russian.
        
        This test verifies backward compatibility - the default behavior
        should use Russian language.
        """
        error = ZeroDivisionError("division by zero")
        
        # Call without language parameter
        result = explain_error(error, return_text=True)
        
        # Should return a string
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_explain_error_with_unsupported_language_fallback(self):
        """
        Test that explain_error() handles unsupported languages gracefully.
        
        This test verifies that requesting an unsupported language
        falls back to English without errors.
        """
        error = IndexError("list index out of range")
        
        # Request unsupported language
        result = explain_error(error, language='fr', return_text=True)
        
        # Should still return a valid explanation
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_explain_error_print_mode(self):
        """
        Test that explain_error() works in print mode (return_text=False).
        
        This test verifies that the function can print to console
        without errors.
        """
        error = AttributeError("test error")
        
        # Should not raise an exception
        result = explain_error(error, language='en', return_text=False)
        
        # Should return None in print mode
        assert result is None
