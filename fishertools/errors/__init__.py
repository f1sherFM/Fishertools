"""
Error explanation system for fishertools.

This module provides tools to explain Python errors in simple, understandable terms
for beginners learning Python.
"""

from .explainer import ErrorExplainer, explain_error
from .patterns import ErrorPattern
from .formatters import ConsoleFormatter, PlainFormatter, JsonFormatter, get_formatter
from .models import ErrorExplanation, ExplainerConfig
from .exceptions import (
    FishertoolsError, ExplanationError, FormattingError, 
    ConfigurationError, PatternError, SafeUtilityError
)
from .recovery import (
    ErrorRecoveryManager, ErrorSeverity, RecoveryStrategy, ErrorContext, RecoveryAction,
    get_recovery_manager, handle_error_with_recovery, with_error_recovery
)

__all__ = [
    "ErrorExplainer", "explain_error", "ErrorPattern", 
    "ConsoleFormatter", "PlainFormatter", "JsonFormatter", "get_formatter",
    "ErrorExplanation", "ExplainerConfig",
    "FishertoolsError", "ExplanationError", "FormattingError", 
    "ConfigurationError", "PatternError", "SafeUtilityError",
    "ErrorRecoveryManager", "ErrorSeverity", "RecoveryStrategy", "ErrorContext", "RecoveryAction",
    "get_recovery_manager", "handle_error_with_recovery", "with_error_recovery"
]