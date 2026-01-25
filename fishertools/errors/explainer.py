"""
Main error explainer implementation.

This module contains the ErrorExplainer class and explain_error function.
"""

from typing import Optional, List
from .models import ErrorExplanation, ExplainerConfig, ErrorPattern
from .patterns import load_default_patterns


class ErrorExplainer:
    """
    Main class for explaining Python errors in simple terms.
    
    Uses pattern matching to provide contextual explanations for different
    types of Python exceptions.
    """
    
    def __init__(self, config: Optional[ExplainerConfig] = None):
        """
        Initialize the error explainer with optional configuration.
        
        Args:
            config: Configuration for the explainer behavior
        """
        self.config = config or ExplainerConfig()
        self.patterns = self._load_patterns()
    
    def _load_patterns(self) -> List[ErrorPattern]:
        """
        Load error patterns for matching exceptions.
        
        Returns:
            List of ErrorPattern objects
        """
        return load_default_patterns()
    
    def explain(self, exception: Exception) -> ErrorExplanation:
        """
        Create an explanation for the given exception.
        
        Args:
            exception: The exception to explain
            
        Returns:
            Structured explanation of the error
        """
        # Try to find a matching pattern
        pattern = self._match_pattern(exception)
        
        if pattern:
            return self._create_explanation_from_pattern(exception, pattern)
        else:
            return self._create_fallback_explanation(exception)
    
    def _match_pattern(self, exception: Exception) -> Optional[ErrorPattern]:
        """
        Find the best matching pattern for the given exception.
        
        Args:
            exception: The exception to match
            
        Returns:
            Matching ErrorPattern or None if no match found
        """
        for pattern in self.patterns:
            if pattern.matches(exception):
                return pattern
        return None
    
    def _create_explanation_from_pattern(self, exception: Exception, 
                                       pattern: ErrorPattern) -> ErrorExplanation:
        """
        Create explanation using a matched pattern.
        
        Args:
            exception: The original exception
            pattern: The matched pattern
            
        Returns:
            ErrorExplanation based on the pattern
        """
        return ErrorExplanation(
            original_error=str(exception),
            error_type=type(exception).__name__,
            simple_explanation=pattern.explanation,
            fix_tip=pattern.tip,
            code_example=pattern.example,
            additional_info=f"Частые причины: {', '.join(pattern.common_causes)}"
        )
    
    def _create_fallback_explanation(self, exception: Exception) -> ErrorExplanation:
        """
        Create a generic explanation for unsupported exceptions.
        
        Args:
            exception: The exception to explain
            
        Returns:
            Generic ErrorExplanation
        """
        error_type = type(exception).__name__
        
        return ErrorExplanation(
            original_error=str(exception),
            error_type=error_type,
            simple_explanation=f"Произошла ошибка типа {error_type}. Это означает, что в вашем коде что-то пошло не так.",
            fix_tip="Внимательно прочитайте сообщение об ошибке и проверьте строку кода, где произошла ошибка. Убедитесь, что все переменные определены и имеют правильные типы.",
            code_example=f"# Пример обработки ошибки {error_type}:\ntry:\n    # ваш код здесь\n    pass\nexcept {error_type} as e:\n    print(f'Ошибка: {{e}}')",
            additional_info="Если вы не можете решить проблему самостоятельно, попробуйте поискать информацию об этом типе ошибки в документации Python или задать вопрос на форуме."
        )


def explain_error(exception: Exception, 
                 language: str = 'ru',
                 format_type: str = 'console',
                 **kwargs) -> None:
    """
    Main public API function for explaining Python errors in simple terms.
    
    This function takes any Python exception and provides a beginner-friendly
    explanation in Russian, including what the error means, how to fix it,
    and a relevant code example.
    
    Args:
        exception: The Python exception to explain (required)
        language: Language for explanations ('ru' or 'en', default: 'ru')
        format_type: Output format ('console', 'plain', 'json', default: 'console')
        **kwargs: Additional formatting parameters:
            - use_colors: Whether to use colors in console output (default: True)
            - show_original_error: Whether to show original error message (default: True)
            - show_traceback: Whether to show traceback (default: False)
    
    Raises:
        TypeError: If exception parameter is not an Exception instance
        ValueError: If language or format_type parameters are invalid
    
    Examples:
        >>> try:
        ...     result = 10 / 0
        ... except Exception as e:
        ...     explain_error(e)
        
        >>> explain_error(TypeError("'str' object cannot be interpreted as an integer"))
        
        >>> explain_error(ValueError("invalid literal"), format_type='json')
    """
    # Parameter validation
    if not isinstance(exception, Exception):
        raise TypeError(f"Параметр 'exception' должен быть экземпляром Exception, "
                       f"получен {type(exception).__name__}")
    
    # Validate language parameter
    valid_languages = ['ru', 'en']
    if language not in valid_languages:
        raise ValueError(f"Параметр 'language' должен быть одним из {valid_languages}, "
                        f"получен '{language}'")
    
    # Validate format_type parameter
    valid_formats = ['console', 'plain', 'json']
    if format_type not in valid_formats:
        raise ValueError(f"Параметр 'format_type' должен быть одним из {valid_formats}, "
                        f"получен '{format_type}'")
    
    try:
        from .formatters import get_formatter
        
        # Create configuration based on parameters
        config = ExplainerConfig(
            language=language,
            format_type=format_type,
            use_colors=kwargs.get('use_colors', True),
            show_original_error=kwargs.get('show_original_error', True),
            show_traceback=kwargs.get('show_traceback', False)
        )
        
        # Create explainer and get explanation
        explainer = ErrorExplainer(config)
        explanation = explainer.explain(exception)
        
        # Get appropriate formatter and format output
        formatter = get_formatter(format_type, use_colors=config.use_colors)
        formatted_output = formatter.format(explanation)
        
        # Output to console by default
        print(formatted_output)
        
    except Exception as e:
        # Graceful error handling - if explanation fails, show basic info
        print(f"Ошибка при объяснении исключения: {e}")
        print(f"Оригинальная ошибка: {type(exception).__name__}: {exception}")
        print("Пожалуйста, сообщите об этой проблеме разработчикам fishertools.")