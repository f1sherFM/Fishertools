"""
Tests for i18n module data models.

This module tests the core data structures used for internationalization.
"""

from __future__ import annotations

import pytest

from fishertools.i18n.models import ErrorExplanation


class TestErrorExplanation:
    """Tests for ErrorExplanation data model."""
    
    def test_error_explanation_creation(self):
        """Test basic ErrorExplanation creation."""
        explanation = ErrorExplanation(
            explanation="This is an error",
            language="en"
        )
        assert explanation.explanation == "This is an error"
        assert explanation.language == "en"
        assert explanation.suggestions == []
        assert explanation.fallback_used is False
    
    def test_error_explanation_with_suggestions(self):
        """Test ErrorExplanation with suggestions."""
        explanation = ErrorExplanation(
            explanation="Division by zero occurred",
            language="en",
            suggestions=[
                "Check if denominator is zero before dividing",
                "Use a try-except block to handle the error"
            ]
        )
        assert len(explanation.suggestions) == 2
        assert "Check if denominator" in explanation.suggestions[0]
    
    def test_error_explanation_string_representation(self):
        """Test ErrorExplanation string representation."""
        explanation = ErrorExplanation(
            explanation="Test error",
            language="en",
            suggestions=["Fix 1", "Fix 2"]
        )
        str_repr = str(explanation)
        assert "Test error" in str_repr
        assert "Suggestions:" in str_repr
        assert "Fix 1" in str_repr
        assert "Fix 2" in str_repr
    
    def test_error_explanation_with_fallback(self):
        """Test ErrorExplanation with fallback flag."""
        explanation = ErrorExplanation(
            explanation="Error message",
            language="en",
            fallback_used=True
        )
        assert explanation.fallback_used is True
