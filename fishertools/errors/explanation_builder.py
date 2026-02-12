"""
Explanation builder for error explanation system.

This module handles creation of error explanations,
separating concerns from the main ErrorExplainer class.
"""

from typing import Optional, Dict, Any
from .models import ErrorExplanation, ErrorPattern, ExceptionExplanation
from .exceptions import ExplanationError


class ExplanationBuilder:
    """
    Builds error explanations from patterns and exceptions.
    
    Responsibilities:
    - Create explanations from patterns
    - Create fallback explanations
    - Create emergency explanations
    - Handle explanation errors gracefully
    """
    
    def create_from_pattern(
        self,
        exception: Exception,
        pattern: ErrorPattern,
        context: Optional[Dict[str, Any]] = None
    ) -> ErrorExplanation:
        """
        Create explanation using a matched pattern with optional context.
        
        Args:
            exception: The original exception
            pattern: The matched pattern
            context: Optional context for more specific explanations
            
        Returns:
            ErrorExplanation based on the pattern
            
        Raises:
            ExplanationError: If explanation creation fails
        """
        try:
            # Start with base explanation from pattern
            explanation = pattern.explanation
            fix_tip = pattern.tip
            additional_info = f"Частые причины: {', '.join(pattern.common_causes)}"
            
            # Enrich with context if provided
            if context:
                explanation, fix_tip, additional_info = self._enrich_with_context(
                    exception, explanation, fix_tip, additional_info, context
                )
            
            return ErrorExplanation(
                original_error=str(exception),
                error_type=type(exception).__name__,
                simple_explanation=explanation,
                fix_tip=fix_tip,
                code_example=pattern.example,
                additional_info=additional_info
            )
        except Exception as e:
            raise ExplanationError(
                f"Не удалось создать объяснение из паттерна: {e}",
                exception_type=type(exception).__name__,
                original_error=e
            ) from e
    def create_fallback(self, exception: Exception, context: Optional[Dict[str, Any]] = None) -> ErrorExplanation:
        """
        Create a generic explanation for unsupported exceptions.
        
        Args:
            exception: The exception to explain
            context: Optional context for more specific explanations
            
        Returns:
            Generic ErrorExplanation
        """
        try:
            error_type = type(exception).__name__
            
            explanation = f"Произошла ошибка типа {error_type}. Это означает, что в вашем коде что-то пошло не так."
            fix_tip = "Внимательно прочитайте сообщение об ошибке и проверьте строку кода, где произошла ошибка. Убедитесь, что все переменные определены и имеют правильные типы."
            additional_info = "Если вы не можете решить проблему самостоятельно, попробуйте поискать информацию об этом типе ошибки в документации Python или задать вопрос на форуме."
            
            # Enrich with context if provided
            if context:
                explanation, fix_tip, additional_info = self._enrich_with_context(
                    exception, explanation, fix_tip, additional_info, context
                )
            
            return ErrorExplanation(
                original_error=str(exception),
                error_type=error_type,
                simple_explanation=explanation,
                fix_tip=fix_tip,
                code_example=f"# Пример обработки ошибки {error_type}:\ntry:\n    # ваш код здесь\n    pass\nexcept {error_type} as e:\n    print(f'Ошибка: {{e}}')",
                additional_info=additional_info
            )
        except Exception as e:
            # If even fallback fails, create emergency explanation
            return self.create_emergency(exception, e)
    
    def _enrich_with_context(
        self,
        exception: Exception,
        explanation: str,
        fix_tip: str,
        additional_info: str,
        context: Dict[str, Any]
    ) -> tuple[str, str, str]:
        """
        Enrich explanation with context-specific details.
        
        Args:
            exception: The original exception
            explanation: Base explanation
            fix_tip: Base fix tip
            additional_info: Base additional info
            context: Context dictionary
            
        Returns:
            Tuple of (enriched_explanation, enriched_fix_tip, enriched_additional_info)
        """
        error_type = type(exception).__name__
        variable_name = context.get('variable_name', 'переменная')
        operation = context.get('operation', 'unknown')
        
        # IndexError with list_access context
        if error_type == 'IndexError' and operation == 'list_access':
            index = context.get('index')
            if index is not None:
                explanation += f"\n\nВы попытались получить доступ к индексу {index} в '{variable_name}'."
                # Try to get list length from context if available
                if 'list_length' in context:
                    list_length = context['list_length']
                    explanation += f" Список содержит только {list_length} элемент(ов)."
                    explanation += f" Допустимые индексы: от 0 до {list_length - 1}."
                
                fix_tip += f"\n\n✓ Проверьте длину списка: if {index} < len({variable_name}): ..."
                fix_tip += f"\n✓ Используйте safe_get(): safe_get({variable_name}, {index}, default=None)"
        
        # KeyError with dict_access context
        elif error_type == 'KeyError' and operation == 'dict_access':
            key = context.get('key')
            if key is not None:
                explanation += f"\n\nВы попытались получить доступ к ключу '{key}' в словаре '{variable_name}', но такого ключа не существует."
                
                # Show available keys if provided
                if 'available_keys' in context:
                    available_keys = context['available_keys']
                    if available_keys:
                        keys_str = ', '.join(f"'{k}'" for k in available_keys[:5])
                        if len(available_keys) > 5:
                            keys_str += f", ... (всего {len(available_keys)} ключей)"
                        explanation += f"\n\nДоступные ключи: {keys_str}"
                
                fix_tip += f"\n\n✓ Проверьте наличие ключа: if '{key}' in {variable_name}: ..."
                fix_tip += f"\n✓ Используйте .get(): {variable_name}.get('{key}', default_value)"
        
        # ZeroDivisionError with division context
        elif error_type == 'ZeroDivisionError' and operation == 'division':
            value = context.get('value', 0)
            explanation += f"\n\nВы попытались разделить на {value} (ноль)."
            
            if variable_name != 'переменная':
                fix_tip += f"\n\n✓ Проверьте значение перед делением: if {variable_name} != 0: ..."
                fix_tip += f"\n✓ Используйте safe_divide(): safe_divide(числитель, {variable_name}, default=0)"
        
        # TypeError with concatenation context
        elif error_type == 'TypeError' and operation == 'concatenation':
            expected_type = context.get('expected_type', 'str')
            actual_type = context.get('actual_type', 'unknown')
            
            explanation += f"\n\nВы попытались объединить значения несовместимых типов."
            explanation += f" Ожидался тип '{expected_type}', но получен '{actual_type}'."
            
            if variable_name != 'переменная':
                fix_tip += f"\n\n✓ Преобразуйте тип: str({variable_name})"
                fix_tip += f"\n✓ Проверьте тип: if isinstance({variable_name}, {expected_type}): ..."
        
        # Generic operation-specific guidance
        elif operation != 'unknown':
            operation_tips = {
                'type_conversion': "✓ Убедитесь, что значение можно преобразовать в нужный тип",
                'attribute_access': "✓ Проверьте, что объект имеет нужный атрибут: hasattr(obj, 'attr')",
                'import': "✓ Убедитесь, что модуль установлен: pip install <module_name>",
                'function_call': "✓ Проверьте количество и типы аргументов функции"
            }
            
            if operation in operation_tips:
                fix_tip += f"\n\n{operation_tips[operation]}"
        
        # Add variable name to additional info if provided
        if variable_name != 'переменная':
            additional_info += f"\n\nПеременная: {variable_name}"
        
        return explanation, fix_tip, additional_info
    
    def create_emergency(
        self,
        exception: Exception,
        original_error: Exception
    ) -> ErrorExplanation:
        """
        Create a minimal explanation when all other methods fail.
        
        This is the last resort for graceful degradation.
        
        Args:
            exception: The original exception to explain
            original_error: The error that prevented normal explanation
            
        Returns:
            Minimal ErrorExplanation that should always work
        """
        try:
            error_type = getattr(type(exception), '__name__', 'Unknown')
            error_message = str(exception) if exception else 'Неизвестная ошибка'
            
            return ErrorExplanation(
                original_error=error_message,
                error_type=error_type,
                simple_explanation="Произошла ошибка в вашем коде. К сожалению, не удалось создать подробное объяснение.",
                fix_tip="Проверьте сообщение об ошибке выше и попробуйте найти проблему в коде. Обратитесь за помощью, если не можете решить проблему самостоятельно.",
                code_example="# Общий способ обработки ошибок:\ntry:\n    # ваш код\n    pass\nexcept Exception as e:\n    print(f'Ошибка: {e}')",
                additional_info=f"Внутренняя ошибка fishertools: {original_error}"
            )
        except Exception:
            # Absolute last resort - create explanation with minimal dependencies
            return ErrorExplanation(
                original_error="Критическая ошибка",
                error_type="Critical",
                simple_explanation="Произошла критическая ошибка в системе объяснения ошибок.",
                fix_tip="Обратитесь к разработчикам fishertools с описанием проблемы.",
                code_example="# Обратитесь за помощью",
                additional_info="Критическая ошибка системы"
            )
    
    def create_structured_from_basic(
        self,
        error_explanation: ErrorExplanation
    ) -> ExceptionExplanation:
        """
        Convert basic ErrorExplanation to structured ExceptionExplanation.
        
        Args:
            error_explanation: Basic error explanation
            
        Returns:
            Structured ExceptionExplanation
        """
        return ExceptionExplanation(
            exception_type=error_explanation.error_type,
            simple_explanation=error_explanation.simple_explanation,
            fix_suggestions=[error_explanation.fix_tip],
            code_example=error_explanation.code_example,
            traceback_context=error_explanation.additional_info
        )
    
    def create_emergency_structured(
        self,
        exception: Exception,
        original_error: Exception
    ) -> ExceptionExplanation:
        """
        Create a minimal structured explanation when all other methods fail.
        
        Args:
            exception: The original exception to explain
            original_error: The error that prevented normal explanation
            
        Returns:
            Minimal ExceptionExplanation that should always work
        """
        try:
            error_type = getattr(type(exception), '__name__', 'Unknown')
            
            return ExceptionExplanation(
                exception_type=error_type,
                simple_explanation="An error occurred in your code. Unfortunately, a detailed explanation could not be generated.",
                fix_suggestions=[
                    "Check the error message above and try to find the problem in your code.",
                    "Search for information about this error type in Python documentation.",
                    "Ask for help if you cannot solve the problem yourself."
                ],
                code_example=f"# General error handling:\ntry:\n    # your code\n    pass\nexcept {error_type} as e:\n    print(f'Error: {{e}}')",
                traceback_context=f"Internal fishertools error: {original_error}"
            )
        except Exception:
            # Absolute last resort
            return ExceptionExplanation(
                exception_type="Critical",
                simple_explanation="A critical error occurred in the error explanation system.",
                fix_suggestions=["Contact fishertools developers with a description of the problem."],
                code_example="# Please contact support",
                traceback_context="Critical system error"
            )

