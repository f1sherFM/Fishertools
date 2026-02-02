"""
Error explanation system for the learning module.

This module provides contextual explanations for validation errors and other
common Python errors, helping beginners understand what went wrong and how to fix it.
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ErrorExplanationPattern:
    """
    Represents a pattern for matching and explaining specific error types.
    
    Attributes:
        pattern: Regex pattern to match error messages
        explanation: Educational explanation of what the error means
        suggestions: List of actionable suggestions to fix the error
        example_fix: Code example showing how to fix the error
        common_causes: List of common reasons this error occurs
    """
    pattern: str
    explanation: str
    suggestions: List[str]
    example_fix: str
    common_causes: List[str]


class ErrorPatternMatcher:
    """
    Handles pattern matching and explanation generation for error messages.
    
    This class implements the error pattern matching system required by the
    fishertools bug fixes specification.
    """
    
    def __init__(self):
        """Initialize the pattern matcher with predefined error patterns."""
        self._patterns = self._load_error_patterns()
        self._compiled_patterns = self._compile_patterns()
    
    def _load_error_patterns(self) -> List[ErrorExplanationPattern]:
        """
        Load predefined error patterns for common validation and Python errors.
        
        Returns:
            List of ErrorExplanationPattern objects
        """
        return [
            # ValidationError patterns - Type mismatch
            ErrorExplanationPattern(
                pattern=r"Expected\s+(\w+),\s+got\s+(\w+)",
                explanation="Функция ожидала один тип данных, но получила другой. Это происходит когда вы передаете неправильный тип аргумента в функцию.",
                suggestions=[
                    "Проверьте тип данных, который вы передаете в функцию",
                    "Используйте функции преобразования типов: int(), float(), str()",
                    "Убедитесь, что переменная содержит ожидаемый тип данных"
                ],
                example_fix="""# Неправильно:
validate_number("строка", 0, 100)  # Ошибка: Expected number, got str

# Правильно:
validate_number(42, 0, 100)        # Передаем число
# или преобразуем строку в число:
user_input = "42"
if user_input.isdigit():
    validate_number(int(user_input), 0, 100)""",
                common_causes=[
                    "Передача строки вместо числа",
                    "Использование None вместо ожидаемого значения",
                    "Неправильное преобразование типов"
                ]
            ),
            
            # ValidationError patterns - Range validation
            ErrorExplanationPattern(
                pattern=r"Value\s+(.+)\s+must\s+be\s+between\s+(.+)\s+and\s+(.+)",
                explanation="Значение находится вне допустимого диапазона. Функция проверяет, что число находится в определенных границах.",
                suggestions=[
                    "Проверьте, что значение находится в допустимом диапазоне",
                    "Убедитесь, что вы правильно понимаете ограничения функции",
                    "Используйте функции min() и max() для ограничения значений"
                ],
                example_fix="""# Неправильно:
validate_number(150, 0, 100)  # Ошибка: Value 150 must be between 0 and 100

# Правильно:
value = 150
max_allowed = 100
safe_value = min(value, max_allowed)  # Ограничиваем максимумом
validate_number(safe_value, 0, 100)""",
                common_causes=[
                    "Неправильный расчет значения",
                    "Неучтенные граничные случаи",
                    "Неправильное понимание требований"
                ]
            ),
            
            # ValidationError patterns - None values
            ErrorExplanationPattern(
                pattern=r"Value\s+cannot\s+be\s+None",
                explanation="Функция получила None (пустое значение) вместо ожидаемых данных. None означает отсутствие значения.",
                suggestions=[
                    "Проверьте, что переменная была правильно инициализирована",
                    "Используйте значения по умолчанию для предотвращения None",
                    "Добавьте проверку на None перед вызовом функции"
                ],
                example_fix="""# Неправильно:
result = None
validate_number(result, 0, 100)  # Ошибка: Value cannot be None

# Правильно:
result = get_user_input()
if result is not None:
    validate_number(result, 0, 100)
else:
    print("Значение не было введено")
    
# Или используйте значение по умолчанию:
result = get_user_input() or 0  # Если None, используем 0""",
                common_causes=[
                    "Переменная не была инициализирована",
                    "Функция вернула None вместо значения",
                    "Неправильная обработка пользовательского ввода"
                ]
            ),
            
            # General TypeError patterns
            ErrorExplanationPattern(
                pattern=r"unsupported\s+operand\s+type.*'(.+)'\s+and\s+'(.+)'",
                explanation="Вы пытаетесь выполнить операцию (сложение, умножение и т.д.) между несовместимыми типами данных.",
                suggestions=[
                    "Убедитесь, что оба операнда имеют совместимые типы",
                    "Используйте преобразование типов перед операцией",
                    "Проверьте типы данных с помощью type() или isinstance()"
                ],
                example_fix="""# Неправильно:
result = 5 + "3"  # TypeError: unsupported operand type(s)

# Правильно:
result = 5 + int("3")    # Преобразуем строку в число: 8
# или
result = str(5) + "3"    # Преобразуем число в строку: "53" """,
                common_causes=[
                    "Смешивание чисел и строк",
                    "Неправильные типы из пользовательского ввода",
                    "Ошибки в логике программы"
                ]
            ),
            
            # AttributeError patterns
            ErrorExplanationPattern(
                pattern=r"'(.+)'\s+object\s+has\s+no\s+attribute\s+'(.+)'",
                explanation="Вы пытаетесь обратиться к методу или атрибуту, которого не существует у данного типа объекта.",
                suggestions=[
                    "Проверьте правильность написания имени метода или атрибута",
                    "Убедитесь, что используете правильный тип объекта",
                    "Используйте dir(объект) для просмотра доступных методов"
                ],
                example_fix="""# Неправильно:
my_string = "hello"
my_string.append("!")  # AttributeError: 'str' object has no attribute 'append'

# Правильно:
my_string = "hello"
my_string = my_string + "!"  # Для строк используем конкатенацию
# или для списков:
my_list = ["hello"]
my_list.append("!")  # У списков есть метод append""",
                common_causes=[
                    "Путаница между методами разных типов данных",
                    "Опечатки в именах методов",
                    "Неправильный тип объекта"
                ]
            )
        ]
    
    def _compile_patterns(self) -> List[Tuple[re.Pattern, ErrorExplanationPattern]]:
        """
        Compile regex patterns for efficient matching.
        
        Returns:
            List of tuples containing compiled patterns and their corresponding explanations
        """
        compiled = []
        for pattern in self._patterns:
            try:
                compiled_regex = re.compile(pattern.pattern, re.IGNORECASE)
                compiled.append((compiled_regex, pattern))
            except re.error as e:
                # Log pattern compilation error but continue with other patterns
                print(f"Warning: Failed to compile pattern '{pattern.pattern}': {e}")
        return compiled
    
    def find_matching_pattern(self, error_message: str) -> Optional[ErrorExplanationPattern]:
        """
        Find the first pattern that matches the given error message.
        
        Args:
            error_message: The error message to match against patterns
            
        Returns:
            ErrorExplanationPattern if a match is found, None otherwise
        """
        if not error_message:
            return None
            
        for compiled_pattern, explanation_pattern in self._compiled_patterns:
            if compiled_pattern.search(error_message):
                return explanation_pattern
        
        return None
    
    def get_fallback_explanation(self, error_message: str) -> Dict[str, str]:
        """
        Provide a generic helpful explanation when no specific pattern matches.
        
        Args:
            error_message: The original error message
            
        Returns:
            Dictionary with fallback explanation
        """
        return {
            "explanation": "Произошла ошибка в вашем коде. Это обычная часть процесса программирования!",
            "suggestions": [
                "Внимательно прочитайте сообщение об ошибке - оно часто содержит подсказки",
                "Проверьте типы данных ваших переменных",
                "Убедитесь, что все переменные правильно инициализированы",
                "Попробуйте упростить код и протестировать по частям"
            ],
            "example_fix": """# Общий подход к отладке:
# 1. Добавьте print() для проверки значений переменных
print(f"Значение переменной: {my_variable}")
print(f"Тип переменной: {type(my_variable)}")

# 2. Используйте try-except для обработки ошибок
try:
    # ваш код здесь
    result = risky_operation()
except Exception as e:
    print(f"Произошла ошибка: {e}")""",
            "common_causes": [
                "Опечатки в коде",
                "Неправильные типы данных",
                "Неинициализированные переменные",
                "Логические ошибки в алгоритме"
            ],
            "original_error": error_message
        }


def explain_error(error_message: str) -> Dict[str, str]:
    """
    Provide contextual explanation for error messages.
    
    This function implements the error explanation system required by Requirements 3.1-3.4.
    It parses error messages and provides educational explanations with suggestions for fixes.
    
    Args:
        error_message: The error message to explain (can be from ValidationError or other exceptions)
        
    Returns:
        Dictionary containing:
        - explanation: What the error means in simple terms
        - suggestions: List of actionable suggestions to fix the error
        - example_fix: Code example showing how to fix the error
        - common_causes: List of common reasons this error occurs
        - original_error: The original error message (for reference)
        
    Examples:
        >>> result = explain_error("Expected number, got str")
        >>> print(result['explanation'])
        Функция ожидала один тип данных, но получила другой...
        
        >>> result = explain_error("Value 150 must be between 0 and 100")
        >>> print(result['suggestions'][0])
        Проверьте, что значение находится в допустимом диапазоне
    """
    if not isinstance(error_message, str):
        error_message = str(error_message)
    
    matcher = ErrorPatternMatcher()
    pattern = matcher.find_matching_pattern(error_message)
    
    if pattern:
        return {
            "explanation": pattern.explanation,
            "suggestions": pattern.suggestions,
            "example_fix": pattern.example_fix,
            "common_causes": pattern.common_causes,
            "original_error": error_message
        }
    else:
        return matcher.get_fallback_explanation(error_message)