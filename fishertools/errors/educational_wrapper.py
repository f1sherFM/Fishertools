"""
Educational error message wrapper for fishertools.

This module provides a comprehensive error handling system that wraps
Python errors with beginner-friendly explanations and suggestions.
"""

import logging
import traceback
from typing import Optional, Callable, Any, Dict
from functools import wraps
from .explainer import ErrorExplainer
from .models import ExplainerConfig


# Configure dual-level logging
logger = logging.getLogger('fishertools')
debug_logger = logging.getLogger('fishertools.debug')

# Set up default handlers if not already configured
if not logger.handlers:
    # User-facing logger - simple messages
    user_handler = logging.StreamHandler()
    user_handler.setLevel(logging.INFO)
    user_formatter = logging.Formatter('%(message)s')
    user_handler.setFormatter(user_formatter)
    logger.addHandler(user_handler)
    logger.setLevel(logging.INFO)

if not debug_logger.handlers:
    # Debug logger - detailed technical information
    debug_handler = logging.StreamHandler()
    debug_handler.setLevel(logging.DEBUG)
    debug_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    debug_handler.setFormatter(debug_formatter)
    debug_logger.addHandler(debug_handler)
    debug_logger.setLevel(logging.DEBUG)


def _exception_trace(exc: Exception) -> str:
    """
    Render traceback string for a provided exception object.

    This works even when called outside an active except block.
    """
    return "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))


class EducationalErrorWrapper:
    """
    Wraps errors with educational explanations for beginners.
    
    This class provides methods to enhance error messages with:
    - Beginner-friendly explanations
    - Specific fix suggestions
    - Code examples
    - Dual-level logging (simple for users, detailed for debugging)
    """
    
    def __init__(self, config: Optional[ExplainerConfig] = None):
        """
        Initialize the educational error wrapper.
        
        Args:
            config: Configuration for error explanation behavior
        """
        self.config = config or ExplainerConfig()
        self.explainer = ErrorExplainer(self.config)
        self._error_patterns = self._initialize_error_patterns()
    
    def _initialize_error_patterns(self) -> Dict[type, Dict[str, str]]:
        """
        Initialize common error patterns with educational explanations.
        
        Returns:
            Dictionary mapping exception types to educational content
        """
        return {
            ImportError: {
                'explanation': 'Не удалось импортировать модуль или пакет',
                'suggestion': 'Убедитесь, что пакет установлен: pip install <package_name>',
                'example': 'pip install fishertools'
            },
            ModuleNotFoundError: {
                'explanation': 'Python не может найти указанный модуль',
                'suggestion': 'Проверьте название модуля и установите его через pip',
                'example': 'pip install <module_name>'
            },
            FileNotFoundError: {
                'explanation': 'Файл не найден по указанному пути',
                'suggestion': 'Проверьте путь к файлу и убедитесь, что файл существует',
                'example': 'import os\nif os.path.exists("file.txt"):\n    with open("file.txt") as f:\n        data = f.read()'
            },
            PermissionError: {
                'explanation': 'Недостаточно прав для выполнения операции',
                'suggestion': 'Проверьте права доступа к файлу или запустите с правами администратора',
                'example': 'Попробуйте запустить программу от имени администратора'
            },
            IOError: {
                'explanation': 'Ошибка ввода-вывода при работе с файлом',
                'suggestion': 'Проверьте, что файл доступен и не используется другой программой',
                'example': 'with open("file.txt", "r") as f:\n    data = f.read()'
            },
            TypeError: {
                'explanation': 'Операция применена к объекту неподходящего типа',
                'suggestion': 'Проверьте типы переменных и используйте правильные операции',
                'example': 'x = "5"\ny = int(x) + 10  # Преобразуйте строку в число'
            },
            ValueError: {
                'explanation': 'Функция получила аргумент правильного типа, но с неподходящим значением',
                'suggestion': 'Проверьте значения аргументов функции',
                'example': 'x = int("123")  # Правильно\n# x = int("abc")  # Ошибка'
            },
            AttributeError: {
                'explanation': 'Объект не имеет указанного атрибута или метода',
                'suggestion': 'Проверьте правильность имени атрибута и тип объекта',
                'example': 'my_list = [1, 2, 3]\nmy_list.append(4)  # Правильно\n# my_list.add(4)  # Ошибка - нет метода add'
            },
            KeyError: {
                'explanation': 'Ключ не найден в словаре',
                'suggestion': 'Проверьте наличие ключа перед обращением или используйте метод .get()',
                'example': 'data = {"name": "Alice"}\nvalue = data.get("age", 0)  # Безопасно'
            },
            IndexError: {
                'explanation': 'Индекс выходит за пределы списка',
                'suggestion': 'Проверьте длину списка перед обращением по индексу',
                'example': 'my_list = [1, 2, 3]\nif len(my_list) > 5:\n    value = my_list[5]'
            },
            ZeroDivisionError: {
                'explanation': 'Попытка деления на ноль',
                'suggestion': 'Проверьте делитель перед выполнением деления',
                'example': 'if denominator != 0:\n    result = numerator / denominator'
            }
        }
    
    def wrap_error(self, exception: Exception, context: Optional[str] = None) -> str:
        """
        Wrap an error with educational explanation.
        
        Args:
            exception: The exception to wrap
            context: Optional context about where the error occurred
            
        Returns:
            Educational error message as a string
        """
        try:
            # Get basic pattern-based explanation
            error_type = type(exception)
            pattern_info = self._error_patterns.get(error_type, {})
            
            # Try to get detailed explanation from explainer
            try:
                explanation = self.explainer.explain(exception)
                educational_msg = f"""
╔══════════════════════════════════════════════════════════════╗
║  ОШИБКА: {error_type.__name__}
╠══════════════════════════════════════════════════════════════╣
║  Что произошло:
║  {explanation.simple_explanation}
║
║  Как исправить:
║  {explanation.fix_tip}
║
║  Пример правильного кода:
║  {explanation.code_example}
╚══════════════════════════════════════════════════════════════╝
"""
            except Exception as explain_error:
                debug_logger.debug(
                    "Explainer fallback activated for %s: %s",
                    error_type.__name__,
                    explain_error,
                )
                # Fallback to pattern-based explanation
                educational_msg = f"""
╔══════════════════════════════════════════════════════════════╗
║  ОШИБКА: {error_type.__name__}
╠══════════════════════════════════════════════════════════════╣
║  Что произошло:
║  {pattern_info.get('explanation', 'Произошла ошибка в программе')}
║
║  Как исправить:
║  {pattern_info.get('suggestion', 'Проверьте код и попробуйте снова')}
║
║  Пример:
║  {pattern_info.get('example', 'См. документацию')}
╚══════════════════════════════════════════════════════════════╝
"""
            
            if context:
                educational_msg += f"\nКонтекст: {context}\n"
            
            educational_msg += f"\nОригинальная ошибка: {exception}\n"
            
            # Log to both loggers
            logger.info(f"Ошибка {error_type.__name__}: {exception}")
            debug_logger.debug(
                f"Educational error wrapper called for {error_type.__name__}\n"
                f"Context: {context}\n"
                f"Traceback: {_exception_trace(exception)}"
            )
            
            return educational_msg
            
        except Exception:
            # Ultimate fallback
            debug_logger.exception("Error in wrap_error")
            return f"Ошибка: {exception}\nНе удалось создать подробное объяснение."
    
    def enhance_import_error(self, exception: ImportError) -> str:
        """
        Provide enhanced explanation for import errors.
        
        Args:
            exception: The ImportError to explain
            
        Returns:
            Enhanced error message with installation suggestions
        """
        error_msg = str(exception)
        module_name = None
        
        # Try to extract module name from error message
        if "No module named" in error_msg:
            parts = error_msg.split("'")
            if len(parts) >= 2:
                module_name = parts[1]
        
        if module_name:
            return f"""
Модуль '{module_name}' не установлен.

Чтобы установить модуль, выполните:
    pip install {module_name}

Если модуль является частью другого пакета, попробуйте:
    pip install --upgrade pip
    pip search {module_name}

Проверьте также:
- Правильность написания имени модуля
- Активирована ли нужная виртуальная среда
- Установлен ли Python и pip в системе
"""
        else:
            return self.wrap_error(exception, "Ошибка импорта модуля")
    
    def enhance_file_error(self, exception: Exception) -> str:
        """
        Provide enhanced explanation for file operation errors.
        
        Args:
            exception: The file-related exception to explain
            
        Returns:
            Enhanced error message with file operation guidance
        """
        error_type = type(exception).__name__
        error_msg = str(exception)
        
        # Extract filename if present
        filename = None
        if "'" in error_msg or '"' in error_msg:
            parts = error_msg.replace('"', "'").split("'")
            if len(parts) >= 2:
                filename = parts[1]
        
        explanation = f"""
Ошибка при работе с файлом: {error_type}

Что произошло:
{error_msg}
"""
        
        if isinstance(exception, FileNotFoundError):
            explanation += f"""
Файл не найден. Возможные причины:
- Файл не существует по указанному пути
- Неправильный путь к файлу (проверьте слэши / или \\)
- Файл находится в другой директории

Как исправить:
1. Проверьте, существует ли файл:
   import os
   print(os.path.exists("{filename or 'your_file.txt'}"))

2. Проверьте текущую директорию:
   print(os.getcwd())

3. Используйте абсолютный путь или проверьте относительный путь
"""
        elif isinstance(exception, PermissionError):
            explanation += f"""
Недостаточно прав для доступа к файлу. Возможные причины:
- Файл открыт в другой программе
- Недостаточно прав доступа к файлу или директории
- Попытка записи в защищенную директорию

Как исправить:
1. Закройте файл в других программах
2. Проверьте права доступа к файлу
3. Запустите программу с правами администратора (если необходимо)
4. Используйте другую директорию для записи
"""
        else:
            explanation += f"""
Рекомендации:
- Проверьте путь к файлу
- Убедитесь, что файл не используется другой программой
- Проверьте права доступа
- Используйте конструкцию with open() для автоматического закрытия файлов
"""
        
        debug_logger.debug("File error enhanced for %s", error_type)
        return explanation


def with_educational_errors(context: Optional[str] = None):
    """
    Decorator to wrap function errors with educational explanations.
    
    Args:
        context: Optional context description for the function
        
    Returns:
        Decorated function that provides educational error messages
        
    Example:
        @with_educational_errors("calculating average")
        def calculate_average(numbers):
            return sum(numbers) / len(numbers)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                wrapper_instance = EducationalErrorWrapper()
                func_context = context or f"функции {func.__name__}"
                educational_msg = wrapper_instance.wrap_error(e, func_context)
                
                # Log the educational message
                logger.error(educational_msg)
                
                # Preserve the original exception type and traceback.
                raise
        
        return wrapper
    return decorator


# Global instance for convenience
_global_wrapper = None


def get_educational_wrapper() -> EducationalErrorWrapper:
    """
    Get the global educational error wrapper instance.
    
    Returns:
        Global EducationalErrorWrapper instance
    """
    global _global_wrapper
    if _global_wrapper is None:
        _global_wrapper = EducationalErrorWrapper()
    return _global_wrapper


def explain_exception(exception: Exception, context: Optional[str] = None) -> str:
    """
    Convenience function to explain an exception with educational context.
    
    Args:
        exception: The exception to explain
        context: Optional context about where the error occurred
        
    Returns:
        Educational error message
        
    Example:
        try:
            result = 10 / 0
        except Exception as e:
            print(explain_exception(e, "dividing numbers"))
    """
    wrapper = get_educational_wrapper()
    return wrapper.wrap_error(exception, context)
