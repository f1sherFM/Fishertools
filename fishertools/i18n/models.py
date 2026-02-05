"""
Data models for internationalization.

This module defines the core data structures used for multilingual error
explanations and language management.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class ErrorExplanation:
    """
    Structured error explanation with multilingual support.
    
    This class represents a complete error explanation including the main
    explanation text, the language used, and helpful suggestions for fixing
    the error.
    
    Attributes:
        explanation: The main error explanation text
        language: Language code (e.g., 'en', 'ru')
        suggestions: List of suggestions for fixing the error
        fallback_used: Whether a fallback language was used
    """
    explanation: str
    language: str
    suggestions: List[str] = field(default_factory=list)
    fallback_used: bool = False
    
    def __str__(self) -> str:
        """Human-readable representation of the explanation."""
        result = self.explanation
        if self.suggestions:
            result += "\n\nSuggestions:\n"
            result += "\n".join(f"  - {s}" for s in self.suggestions)
        return result
