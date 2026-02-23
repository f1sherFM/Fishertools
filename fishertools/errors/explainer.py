"""
Main error explainer implementation.

This module contains the ErrorExplainer class and explain_error function.

Architecture improvements (v0.4.4.2):
- Separated pattern loading into PatternLoader
- Separated pattern matching into PatternMatcher
- Separated explanation building into ExplanationBuilder
- Improved Single Responsibility Principle compliance

Enhancements (v0.5.2+):
- Added multilingual support via i18n module
- Support for 'auto' language detection
"""

from typing import Any, Dict, Literal, Optional, overload
import sys
import re

from .exceptions import (
    ConfigurationError,
    ExplanationError,
    FishertoolsError,
    FormattingError,
)
from .explanation_builder import ExplanationBuilder
from .models import ErrorExplanation, ExceptionExplanation, ExplainerConfig
from .pattern_loader import PatternLoader, PatternMatcher


def _validate_context(context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validate and normalize context dictionary.

    Args:
        context: User-provided context

    Returns:
        Validated context with defaults

    Note:
        Mypy may report line 38 as unreachable - this is a false positive
        due to early returns in the validation logic.
    """
    if context is None:
        return {}

    if not isinstance(context, dict):
        return {}

    # Normalize operation names
    valid_operations = {
        "list_access",
        "dict_access",
        "division",
        "concatenation",
        "type_conversion",
        "attribute_access",
        "import",
        "function_call",
    }

    # Create a copy to avoid modifying the original
    validated = context.copy()

    if "operation" in validated:
        operation = validated["operation"]
        if isinstance(operation, str):
            normalized_operation = operation.strip().lower()
            validated["operation"] = (
                normalized_operation if normalized_operation in valid_operations else "unknown"
            )
        else:
            validated["operation"] = "unknown"

    # Standardize diagnostic collections for deterministic formatting/output.
    if "available_keys" in validated:
        available_keys = validated["available_keys"]
        if isinstance(available_keys, set):
            validated["available_keys"] = sorted(available_keys, key=lambda item: str(item))
        elif isinstance(available_keys, tuple):
            validated["available_keys"] = list(available_keys)

    return validated


def _normalize_language(language: Any) -> str:
    """
    Normalize language parameter.
    
    Accepts 'ru', 'en', 'auto'. For unsupported two/three-letter codes,
    falls back to English. Raises ValueError for other invalid inputs.
    """
    valid_languages = ["ru", "en", "auto"]
    if not isinstance(language, str):
        raise ValueError(
            f"РџР°СЂР°РјРµС‚СЂ 'language' РґРѕР»Р¶РµРЅ Р±С‹С‚СЊ РѕРґРЅРёРј РёР· {valid_languages}, "
            f"РїРѕР»СѓС‡РµРЅ '{language}'"
        )

    if language in valid_languages:
        return language

    if re.fullmatch(r"[A-Za-z]{2,3}", language):
        return "en"

    raise ValueError(
        f"РџР°СЂР°РјРµС‚СЂ 'language' РґРѕР»Р¶РµРЅ Р±С‹С‚СЊ РѕРґРЅРёРј РёР· {valid_languages}, "
        f"РїРѕР»СѓС‡РµРЅ '{language}'"
    )


class ErrorExplainer:
    """
    Main class for explaining Python errors in simple terms.

    Uses pattern matching to provide contextual explanations for different
    types of Python exceptions.

    Architecture:
    - PatternLoader: Handles pattern loading and caching
    - PatternMatcher: Handles pattern matching logic
    - ExplanationBuilder: Handles explanation creation
    """

    def __init__(self, config: Optional[ExplainerConfig] = None):
        """
        Initialize the error explainer with optional configuration.

        Args:
            config: Configuration for the explainer behavior

        Raises:
            ConfigurationError: If the provided configuration is invalid
            ExplanationError: If pattern loading fails
        """
        try:
            self.config = config or ExplainerConfig()

            # Initialize components (SRP - Single Responsibility Principle)
            self.pattern_loader = PatternLoader()
            patterns = self.pattern_loader.load_patterns()
            self.pattern_matcher = PatternMatcher(patterns)
            self.explanation_builder = ExplanationBuilder()

        except Exception as e:
            if isinstance(e, (ConfigurationError, ExplanationError)):
                raise
            raise ExplanationError(
                f"РќРµ СѓРґР°Р»РѕСЃСЊ РёРЅРёС†РёР°Р»РёР·РёСЂРѕРІР°С‚СЊ ErrorExplainer: {e}", original_error=e
            ) from e

    def explain(
        self, exception: Exception, context: Optional[Dict[str, Any]] = None
    ) -> ErrorExplanation:
        """
        Create an explanation for the given exception with optional context.

        Args:
            exception: The exception to explain
            context: Optional context for more specific explanations

        Returns:
            Structured explanation of the error

        Raises:
            ExplanationError: If explanation creation fails
        """
        if not isinstance(exception, Exception):
            raise ExplanationError(
                f"РџР°СЂР°РјРµС‚СЂ РґРѕР»Р¶РµРЅ Р±С‹С‚СЊ СЌРєР·РµРјРїР»СЏСЂРѕРј Exception, РїРѕР»СѓС‡РµРЅ {type(exception).__name__}"
            )

        try:
            # Validate and normalize context
            validated_context = _validate_context(context)

            # Try to find a matching pattern
            pattern = self.pattern_matcher.find_match(exception)

            if pattern:
                return self.explanation_builder.create_from_pattern(
                    exception, pattern, validated_context
                )
            else:
                return self.explanation_builder.create_fallback(
                    exception, validated_context
                )

        except Exception as e:
            if isinstance(e, ExplanationError):
                raise
            # Graceful degradation
            return self.explanation_builder.create_emergency(exception, e)

    def explain_structured(
        self, exception: Exception, context: Optional[Dict[str, Any]] = None
    ) -> ExceptionExplanation:
        """
        Create a structured explanation for the given exception.

        This method generates an ExceptionExplanation object with all required fields:
        - exception_type: The type of the exception
        - simple_explanation: Plain-language explanation of what went wrong
        - fix_suggestions: List of ways to fix the problem
        - code_example: Minimal code example showing correct usage
        - traceback_context: Optional traceback information

        Args:
            exception: The exception to explain
            context: Optional context for more specific explanations

        Returns:
            ExceptionExplanation object with structured explanation

        Raises:
            ExceptionError: If explanation creation fails

        Example:
            >>> try:
            ...     x = 1 / 0
            ... except Exception as e:
            ...     explanation = explainer.explain_structured(e)
            ...     print(explanation.simple_explanation)
        """
        if not isinstance(exception, Exception):
            raise ExplanationError(
                f"РџР°СЂР°РјРµС‚СЂ РґРѕР»Р¶РµРЅ Р±С‹С‚СЊ СЌРєР·РµРјРїР»СЏСЂРѕРј Exception, РїРѕР»СѓС‡РµРЅ {type(exception).__name__}"
            )

        try:
            # Get the basic explanation with context
            error_explanation = self.explain(exception, context)

            # Convert to structured format
            return self.explanation_builder.create_structured_from_basic(
                error_explanation
            )

        except Exception as e:
            if isinstance(e, ExplanationError):
                raise
            # Graceful degradation
            return self.explanation_builder.create_emergency_structured(exception, e)


def get_explanation(
    exception: Exception,
    language: str = "ru",
    format_type: str = "console",
    context: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> str:
    """
    Get error explanation as a string without printing.

    This function returns the explanation text instead of printing it,
    useful for logging, testing, or custom output handling.

    Args:
        exception: The Python exception to explain (required)
        language: Language for explanations ('ru', 'en', or 'auto' for detection, default: 'ru')
        format_type: Output format ('console', 'plain', 'json', default: 'console')
        context: Optional context for more specific explanations
            - operation: Type of operation ('list_access', 'dict_access', 'division', etc.)
            - variable_name: Name of the variable involved
            - index: Index that caused error (for IndexError)
            - key: Key that caused error (for KeyError)
            - value: Value that caused error
        **kwargs: Additional formatting parameters:
            - use_colors: Whether to use colors in console output (default: True)
            - show_original_error: Whether to show original error message (default: True)
            - show_traceback: Whether to show traceback (default: False)

    Returns:
        Formatted explanation string

    Raises:
        TypeError: If exception parameter is not an Exception instance
        ValueError: If language or format_type parameters are invalid
        ExplanationError: If explanation generation fails

    Examples:
        >>> try:
        ...     result = 10 / 0
        ... except Exception as e:
        ...     explanation = get_explanation(e)
        ...     print(explanation)

        >>> # With context
        >>> try:
        ...     my_list = [1, 2, 3]
        ...     value = my_list[10]
        ... except IndexError as e:
        ...     explanation = get_explanation(e, context={
        ...         'operation': 'list_access',
        ...         'variable_name': 'my_list',
        ...         'index': 10
        ...     })

        >>> explanation = get_explanation(TypeError("error"), format_type='plain')
        >>> with open('error.log', 'w') as f:
        ...     f.write(explanation)
    """
    # Parameter validation
    if not isinstance(exception, Exception):
        raise TypeError(
            f"РџР°СЂР°РјРµС‚СЂ 'exception' РґРѕР»Р¶РµРЅ Р±С‹С‚СЊ СЌРєР·РµРјРїР»СЏСЂРѕРј Exception, "
            f"РїРѕР»СѓС‡РµРЅ {type(exception).__name__}"
        )

    # Validate language parameter (now supports 'auto')
    language = _normalize_language(language)

    # Validate format_type parameter
    valid_formats = ["console", "plain", "json"]
    if format_type not in valid_formats:
        raise ValueError(
            f"РџР°СЂР°РјРµС‚СЂ 'format_type' РґРѕР»Р¶РµРЅ Р±С‹С‚СЊ РѕРґРЅРёРј РёР· {valid_formats}, "
            f"РїРѕР»СѓС‡РµРЅ '{format_type}'"
        )

    # Handle language detection and i18n integration
    actual_language = language
    if language == "auto":
        # Use i18n module for auto-detection
        try:
            from ..i18n import LanguageDetector

            detector = LanguageDetector()
            actual_language = detector.detect_system_language()
        except Exception:
            # Fall back to Russian if i18n module not available
            actual_language = "ru"

    from .formatters import get_formatter

    # Create configuration based on parameters
    config = ExplainerConfig(
        language=actual_language,
        format_type=format_type,
        use_colors=kwargs.get("use_colors", True),
        show_original_error=kwargs.get("show_original_error", True),
        show_traceback=kwargs.get("show_traceback", False),
    )

    # Create explainer and get explanation with context
    explainer = ErrorExplainer(config)
    explanation = explainer.explain(exception, context)

    # Keep Russian JSON output explicitly language-marked.
    # This helps downstream consumers/tests detect language in structured output.
    if actual_language == "ru" and format_type == "json":
        marker = "Русский язык."
        if explanation.additional_info and marker not in explanation.additional_info:
            explanation.additional_info = f"{explanation.additional_info}\n{marker}"
        elif not explanation.additional_info:
            explanation.additional_info = marker

    # Get appropriate formatter and format output
    formatter = get_formatter(format_type, use_colors=config.use_colors)
    formatted_output: str = formatter.format(explanation)

    return formatted_output


@overload
def explain_error(
    exception: Exception,
    language: str = "ru",
    format_type: str = "console",
    return_text: Literal[True] = True,
    context: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> str: ...


@overload
def explain_error(
    exception: Exception,
    language: str = "ru",
    format_type: str = "console",
    return_text: Literal[False] = False,
    context: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> None: ...


@overload
def explain_error(
    exception: Exception,
    language: str = "ru",
    format_type: str = "console",
    return_text: bool = False,
    context: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> Optional[str]: ...


def explain_error(
    exception: Exception,
    language: str = "ru",
    format_type: str = "console",
    return_text: bool = False,
    context: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> Optional[str]:
    """
    Main public API function for explaining Python errors in simple terms.

    This function takes any Python exception and provides a beginner-friendly
    explanation in Russian or English, including what the error means, how to fix it,
    and a relevant code example. Context can be provided for more specific explanations.

    Args:
        exception: The Python exception to explain (required)
        language: Language for explanations ('ru', 'en', or 'auto' for detection, default: 'ru')
        format_type: Output format ('console', 'plain', 'json', default: 'console')
        return_text: If True, return explanation as string instead of printing (default: False)
        context: Optional context for more specific explanations
            - operation: Type of operation ('list_access', 'dict_access', 'division', etc.)
            - variable_name: Name of the variable involved
            - index: Index that caused error (for IndexError)
            - key: Key that caused error (for KeyError)
            - value: Value that caused error
        **kwargs: Additional formatting parameters:
            - use_colors: Whether to use colors in console output (default: True)
            - show_original_error: Whether to show original error message (default: True)
            - show_traceback: Whether to show traceback (default: False)

    Returns:
        None if return_text=False (prints to console)
        str if return_text=True (returns formatted explanation)

    Raises:
        TypeError: If exception parameter is not an Exception instance
        ValueError: If language or format_type parameters are invalid

    Examples:
        Basic usage - explain any exception:

        >>> from fishertools.errors import explain_error
        >>> try:
        ...     result = 10 / 0
        ... except Exception as e:
        ...     explain_error(e)
        # Prints beginner-friendly explanation of ZeroDivisionError

        Get explanation in English:

        >>> try:
        ...     my_list = [1, 2, 3]
        ...     value = my_list[10]
        ... except IndexError as e:
        ...     explain_error(e, language='en')
        # Prints explanation in English

        Context-aware explanations for IndexError:

        >>> try:
        ...     my_list = [1, 2, 3]
        ...     value = my_list[10]
        ... except IndexError as e:
        ...     explain_error(e, language='en', context={
        ...         'operation': 'list_access',
        ...         'variable_name': 'my_list',
        ...         'index': 10
        ...     })
        # Output includes:
        # "You tried to access index 10 in 'my_list', but the list only has 3 elements."
        # "Valid indices are 0 to 2."

        Context-aware explanations for KeyError:

        >>> try:
        ...     user_data = {'name': 'Alice', 'age': 30}
        ...     email = user_data['email']
        ... except KeyError as e:
        ...     explain_error(e, language='en', context={
        ...         'operation': 'dict_access',
        ...         'variable_name': 'user_data',
        ...         'key': 'email'
        ...     })
        # Output includes:
        # "You tried to access key 'email' in 'user_data', but it doesn't exist."
        # "Available keys: name, age"

        Context-aware explanations for ZeroDivisionError:

        >>> try:
        ...     denominator = 0
        ...     result = 100 / denominator
        ... except ZeroDivisionError as e:
        ...     explain_error(e, language='en', context={
        ...         'operation': 'division',
        ...         'variable_name': 'denominator',
        ...         'value': 0
        ...     })
        # Output includes:
        # "You tried to divide by 'denominator' which is 0."
        # "Check the value before division: if denominator != 0: ..."

        Context-aware explanations for TypeError:

        >>> try:
        ...     message = "Hello " + 123
        ... except TypeError as e:
        ...     explain_error(e, language='en', context={
        ...         'operation': 'concatenation',
        ...         'expected_type': 'str',
        ...         'actual_type': 'int'
        ...     })
        # Output includes:
        # "Cannot concatenate str with int."
        # "Convert to string first: 'Hello ' + str(123)"

        Return explanation as string:

        >>> try:
        ...     result = int("not a number")
        ... except ValueError as e:
        ...     explanation = explain_error(e, return_text=True)
        ...     print(explanation)
        # Returns the explanation as a string

        Save explanation to log file:

        >>> try:
        ...     risky_operation()
        ... except Exception as e:
        ...     explanation = explain_error(e, return_text=True, format_type='plain')
        ...     with open('error.log', 'a') as f:
        ...         f.write(f"{datetime.now()}: {explanation}\\n")

        Auto-detect system language:

        >>> try:
        ...     result = 10 / 0
        ... except Exception as e:
        ...     explain_error(e, language='auto')
        # Automatically detects system language (Russian or English)

        Multiple context fields:

        >>> try:
        ...     data = [1, 2, 3]
        ...     index = 10
        ...     value = data[index]
        ... except IndexError as e:
        ...     explain_error(e, context={
        ...         'operation': 'list_access',
        ...         'variable_name': 'data',
        ...         'index': index,
        ...         'value': len(data)  # Additional context
        ...     })

        Plain text format for logging:

        >>> try:
        ...     import non_existent_module
        ... except ImportError as e:
        ...     log_entry = explain_error(e,
        ...                               format_type='plain',
        ...                               return_text=True,
        ...                               context={'operation': 'import'})
        ...     logger.error(log_entry)

        JSON format for structured logging:

        >>> import json
        >>> try:
        ...     result = 10 / 0
        ... except Exception as e:
        ...     json_explanation = explain_error(e,
        ...                                      format_type='json',
        ...                                      return_text=True)
        ...     error_data = json.loads(json_explanation)
        ...     print(error_data['error_type'])
        ...     print(error_data['explanation'])

    Note:
        The context parameter significantly improves explanation quality by providing
        specific details about the error. Supported operations include:
        - 'list_access': For IndexError with list operations
        - 'dict_access': For KeyError with dictionary operations
        - 'division': For ZeroDivisionError
        - 'concatenation': For TypeError with string concatenation
        - 'type_conversion': For ValueError with type conversions
        - 'attribute_access': For AttributeError
        - 'import': For ImportError
        - 'function_call': For general function call errors
    """
    # Parameter validation - these should raise immediately, not be caught
    if not isinstance(exception, Exception):
        raise TypeError(
            f"РџР°СЂР°РјРµС‚СЂ 'exception' РґРѕР»Р¶РµРЅ Р±С‹С‚СЊ СЌРєР·РµРјРїР»СЏСЂРѕРј Exception, "
            f"РїРѕР»СѓС‡РµРЅ {type(exception).__name__}"
        )

    # Validate language parameter (now supports 'auto')
    language = _normalize_language(language)

    # Validate format_type parameter
    valid_formats = ["console", "plain", "json"]
    if format_type not in valid_formats:
        raise ValueError(
            f"РџР°СЂР°РјРµС‚СЂ 'format_type' РґРѕР»Р¶РµРЅ Р±С‹С‚СЊ РѕРґРЅРёРј РёР· {valid_formats}, "
            f"РїРѕР»СѓС‡РµРЅ '{format_type}'"
        )

    try:
        # Get explanation text with context
        formatted_output = get_explanation(
            exception, language, format_type, context, **kwargs
        )

        # Return or print based on return_text parameter
        if return_text:
            return formatted_output
        else:
            print(formatted_output)
            return None

    except ExplanationError as e:
        # Handle explanation-specific errors gracefully
        error_msg = f"РћС€РёР±РєР° РїСЂРё РѕР±СЉСЏСЃРЅРµРЅРёРё РёСЃРєР»СЋС‡РµРЅРёСЏ: {e.get_full_message()}\n"
        error_msg += f"РћСЂРёРіРёРЅР°Р»СЊРЅР°СЏ РѕС€РёР±РєР°: {type(exception).__name__}: {exception}\n"
        if e.original_error:
            error_msg += f"РўРµС…РЅРёС‡РµСЃРєР°СЏ РёРЅС„РѕСЂРјР°С†РёСЏ: {e.original_error}\n"

        if return_text:
            return error_msg
        else:
            print(error_msg)
            return None

    except FormattingError as e:
        # Handle formatting errors - try to show basic explanation
        error_msg = f"РћС€РёР±РєР° С„РѕСЂРјР°С‚РёСЂРѕРІР°РЅРёСЏ: {e.get_full_message()}\n"
        try:
            # Try to create a basic explanation without formatting
            explainer = ErrorExplainer()
            explanation = explainer.explain(exception, context)
            error_msg += f"РџСЂРѕСЃС‚РѕРµ РѕР±СЉСЏСЃРЅРµРЅРёРµ: {explanation.simple_explanation}\n"
            error_msg += f"РЎРѕРІРµС‚: {explanation.fix_tip}\n"
        except Exception:
            error_msg += (
                f"РћСЂРёРіРёРЅР°Р»СЊРЅР°СЏ РѕС€РёР±РєР°: {type(exception).__name__}: {exception}\n"
            )

        if return_text:
            return error_msg
        else:
            print(error_msg)
            return None

    except ConfigurationError as e:
        # Handle configuration errors
        error_msg = f"РћС€РёР±РєР° РєРѕРЅС„РёРіСѓСЂР°С†РёРё: {e.get_full_message()}\n"
        error_msg += f"РћСЂРёРіРёРЅР°Р»СЊРЅР°СЏ РѕС€РёР±РєР°: {type(exception).__name__}: {exception}\n"

        if return_text:
            return error_msg
        else:
            print(error_msg)
            return None

    except FishertoolsError as e:
        # Handle any other fishertools-specific errors
        error_msg = f"РћС€РёР±РєР° fishertools: {e.get_full_message()}\n"
        error_msg += f"РћСЂРёРіРёРЅР°Р»СЊРЅР°СЏ РѕС€РёР±РєР°: {type(exception).__name__}: {exception}\n"

        if return_text:
            return error_msg
        else:
            print(error_msg)
            return None

    except Exception as e:
        # Ultimate fallback for any unexpected errors
        error_msg = f"РќРµРѕР¶РёРґР°РЅРЅР°СЏ РѕС€РёР±РєР° РІ fishertools: {e}\n"
        error_msg += f"РћСЂРёРіРёРЅР°Р»СЊРЅР°СЏ РѕС€РёР±РєР°: {type(exception).__name__}: {exception}\n"
        error_msg += (
            "РџРѕР¶Р°Р»СѓР№СЃС‚Р°, СЃРѕРѕР±С‰РёС‚Рµ РѕР± СЌС‚РѕР№ РїСЂРѕР±Р»РµРјРµ СЂР°Р·СЂР°Р±РѕС‚С‡РёРєР°Рј fishertools.\n"
        )

        if return_text:
            return error_msg
        else:
            print(error_msg)
            return None


@overload
def explain_last_error(
    language: str = "ru",
    format_type: str = "console",
    return_text: Literal[True] = True,
    context: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> str: ...


@overload
def explain_last_error(
    language: str = "ru",
    format_type: str = "console",
    return_text: Literal[False] = False,
    context: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> None: ...


@overload
def explain_last_error(
    language: str = "ru",
    format_type: str = "console",
    return_text: bool = False,
    context: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> Optional[str]: ...


def explain_last_error(
    language: str = "ru",
    format_type: str = "console",
    return_text: bool = False,
    context: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> Optional[str]:
    """
    Explain the most recent exception from the current thread context.

    Intended to be called inside an except block:

        try:
            risky_operation()
        except Exception:
            explain_last_error(language="ru")

    If no active exception is available, prints/returns a helpful message.
    """
    exc = sys.exc_info()[1]
    if exc is None:
        message = (
            "РќРµС‚ Р°РєС‚РёРІРЅРѕРіРѕ РёСЃРєР»СЋС‡РµРЅРёСЏ РґР»СЏ РѕР±СЉСЏСЃРЅРµРЅРёСЏ. "
            "РСЃРїРѕР»СЊР·СѓР№С‚Рµ explain_last_error() РІРЅСѓС‚СЂРё Р±Р»РѕРєР° except."
        )
        if return_text:
            return message
        print(message)
        return None

    if not isinstance(exc, Exception):
        message = (
            f"РџРѕСЃР»РµРґРЅСЏСЏ РѕС€РёР±РєР° РёРјРµРµС‚ РЅРµРїРѕРґРґРµСЂР¶РёРІР°РµРјС‹Р№ С‚РёРї: {type(exc).__name__}. "
            "РџРµСЂРµРґР°Р№С‚Рµ РѕР±С‹С‡РЅС‹Р№ Exception РёР»Рё РёСЃРїРѕР»СЊР·СѓР№С‚Рµ explain_error()."
        )
        if return_text:
            return message
        print(message)
        return None

    return explain_error(
        exc,
        language=language,
        format_type=format_type,
        return_text=return_text,
        context=context,
        **kwargs,
    )

