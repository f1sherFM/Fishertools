"""
Error explanation system for fishertools.

This module provides tools to explain Python errors in simple, understandable terms
for beginners learning Python.
"""

from .explainer import ErrorExplainer, explain_error
from .patterns import ErrorPattern
from .formatters import ConsoleFormatter, PlainFormatter, JsonFormatter, get_formatter
from .models import ErrorExplanation, ExplainerConfig

__all__ = [
    "ErrorExplainer", "explain_error", "ErrorPattern", 
    "ConsoleFormatter", "PlainFormatter", "JsonFormatter", "get_formatter",
    "ErrorExplanation", "ExplainerConfig"
]