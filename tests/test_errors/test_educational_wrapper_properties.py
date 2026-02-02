"""
Property-based tests for educational error wrapper.

Feature: fishertools-bug-fixes
Property 7: Educational Error Messages
Validates: Requirements 8.1, 8.2, 8.4
"""

import pytest
from hypothesis import given, strategies as st, assume, settings
from fishertools.errors import (
    EducationalErrorWrapper, 
    explain_exception,
    with_educational_errors,
    FishertoolsError
)


# Strategy for generating various exception types
@st.composite
def exception_strategy(draw):
    """Generate various types of exceptions for testing."""
    exception_types = [
        (ImportError, st.text(min_size=1)),
        (ModuleNotFoundError, st.text(min_size=1)),
        (FileNotFoundError, st.text(min_size=1)),
        (PermissionError, st.text(min_size=1)),
        (IOError, st.text(min_size=1)),
        (TypeError, st.text(min_size=1)),
        (ValueError, st.text(min_size=1)),
        (AttributeError, st.text(min_size=1)),
        (KeyError, st.text(min_size=1)),
        (IndexError, st.text(min_size=1)),
        (ZeroDivisionError, st.text(min_size=1)),
    ]
    
    exc_type, message_strategy = draw(st.sampled_from(exception_types))
    message = draw(message_strategy)
    
    return exc_type(message)


class TestEducationalErrorMessagesProperty:
    """
    Property 7: Educational Error Messages
    
    For any unexpected error in fishertools functions, the system should 
    provide educational error messages when possible, with beginner-friendly 
    explanations.
    
    **Validates: Requirements 8.1, 8.2, 8.4**
    """
    
    @given(exception=exception_strategy())
    @settings(max_examples=100, deadline=None)
    def test_all_errors_get_educational_explanation(self, exception):
        """
        Property: Every exception should receive an educational explanation.
        
        For any exception, the wrapper should provide:
        - A non-empty explanation message
        - The message should be a string
        - The message should contain some educational content
        """
        wrapper = EducationalErrorWrapper()
        
        # Wrap the error
        result = wrapper.wrap_error(exception)
        
        # Verify we got a string response
        assert isinstance(result, str), "Educational message must be a string"
        
        # Verify the message is not empty
        assert len(result.strip()) > 0, "Educational message cannot be empty"
        
        # Verify the message contains the error type name
        error_type_name = type(exception).__name__
        assert error_type_name in result, f"Message should mention error type {error_type_name}"
        
        # Verify the message contains some educational keywords
        educational_keywords = [
            'Что произошло', 'Как исправить', 'Пример', 'ОШИБКА',
            'Ошибка', 'произошло', 'исправить', 'Проверьте'
        ]
        has_educational_content = any(keyword in result for keyword in educational_keywords)
        assert has_educational_content, "Message should contain educational content"
    
    @given(
        exception=exception_strategy(),
        context=st.one_of(st.none(), st.text(min_size=1, max_size=100))
    )
    @settings(max_examples=100, deadline=None)
    def test_context_preserved_in_explanation(self, exception, context):
        """
        Property: Context information should be preserved in explanations.
        
        When context is provided, it should appear in the educational message.
        """
        wrapper = EducationalErrorWrapper()
        
        # Wrap the error with context
        result = wrapper.wrap_error(exception, context)
        
        # Verify result is a string
        assert isinstance(result, str)
        
        # If context was provided, it should appear in the result
        if context and context.strip():
            assert 'Контекст' in result or context in result, \
                "Context should be included in the educational message"
    
    @given(exception=exception_strategy())
    @settings(max_examples=100, deadline=None)
    def test_original_error_included(self, exception):
        """
        Property: Original error message should be included.
        
        The educational wrapper should always include the original error
        message for reference.
        """
        wrapper = EducationalErrorWrapper()
        
        # Wrap the error
        result = wrapper.wrap_error(exception)
        
        # Verify the original error message is mentioned
        assert 'Оригинальная ошибка' in result or str(exception) in result, \
            "Original error should be included in the message"
    
    @given(exception=exception_strategy())
    @settings(max_examples=100, deadline=None)
    def test_explain_exception_convenience_function(self, exception):
        """
        Property: Convenience function should work for all exceptions.
        
        The explain_exception function should provide the same guarantees
        as the wrapper class.
        """
        # Use convenience function
        result = explain_exception(exception)
        
        # Verify basic properties
        assert isinstance(result, str)
        assert len(result.strip()) > 0
        assert type(exception).__name__ in result
    
    @given(
        exception=st.sampled_from([
            ImportError("No module named 'test_module'"),
            ModuleNotFoundError("No module named 'another_module'"),
        ])
    )
    @settings(max_examples=50, deadline=None)
    def test_import_errors_get_installation_suggestions(self, exception):
        """
        Property: Import errors should include installation suggestions.
        
        For ImportError and ModuleNotFoundError, the explanation should
        include pip install suggestions.
        """
        wrapper = EducationalErrorWrapper()
        
        # Get enhanced import error explanation
        result = wrapper.enhance_import_error(exception)
        
        # Verify installation suggestions are present
        assert 'pip install' in result, \
            "Import errors should suggest pip install"
        
        # Verify it's educational
        assert isinstance(result, str)
        assert len(result.strip()) > 0
    
    @given(
        exception=st.sampled_from([
            FileNotFoundError("test.txt"),
            PermissionError("Cannot access file"),
            IOError("File operation failed"),
        ])
    )
    @settings(max_examples=50, deadline=None)
    def test_file_errors_get_file_operation_guidance(self, exception):
        """
        Property: File errors should include file operation guidance.
        
        For file-related errors, the explanation should include guidance
        about file paths, permissions, and common issues.
        """
        wrapper = EducationalErrorWrapper()
        
        # Get enhanced file error explanation
        result = wrapper.enhance_file_error(exception)
        
        # Verify file operation guidance is present
        file_keywords = ['файл', 'путь', 'директори', 'прав']
        has_file_guidance = any(keyword in result.lower() for keyword in file_keywords)
        assert has_file_guidance, \
            "File errors should include file operation guidance"
        
        # Verify it's educational
        assert isinstance(result, str)
        assert len(result.strip()) > 0
    
    def test_decorator_preserves_function_behavior(self):
        """
        Property: Decorator should not change function behavior on success.
        
        When a function succeeds, the decorator should return the same result.
        """
        @with_educational_errors("test function")
        def successful_function(x, y):
            return x + y
        
        # Test that function works normally
        result = successful_function(5, 3)
        assert result == 8, "Decorator should not change successful function behavior"
    
    @given(
        x=st.integers(),
        y=st.integers().filter(lambda n: n == 0)
    )
    @settings(max_examples=50, deadline=None)
    def test_decorator_enhances_errors(self, x, y):
        """
        Property: Decorator should enhance errors when they occur.
        
        When a function raises an error, the decorator should log
        educational information (but still raise the error).
        """
        @with_educational_errors("division operation")
        def failing_function(a, b):
            return a / b
        
        # The function should still raise the error
        with pytest.raises(ZeroDivisionError):
            failing_function(x, y)
    
    @given(exception=exception_strategy())
    @settings(max_examples=100, deadline=None)
    def test_wrapper_never_raises_on_explanation(self, exception):
        """
        Property: Wrapper should never raise exceptions during explanation.
        
        Even if explanation fails, the wrapper should return a fallback
        message rather than raising an exception.
        """
        wrapper = EducationalErrorWrapper()
        
        # This should never raise, even for weird exceptions
        try:
            result = wrapper.wrap_error(exception)
            assert isinstance(result, str)
            assert len(result) > 0
        except Exception as e:
            pytest.fail(f"Wrapper raised exception during explanation: {e}")
    
    @given(
        exception=exception_strategy(),
        context=st.text(max_size=1000)
    )
    @settings(max_examples=100, deadline=None)
    def test_explanation_length_reasonable(self, exception, context):
        """
        Property: Explanations should be reasonably sized.
        
        Educational messages should not be excessively long or short.
        """
        wrapper = EducationalErrorWrapper()
        result = wrapper.wrap_error(exception, context)
        
        # Should have some minimum content
        assert len(result) >= 50, "Explanation too short to be useful"
        
        # Should not be excessively long (unless context is very long)
        max_reasonable_length = 5000 + len(context or "")
        assert len(result) <= max_reasonable_length, \
            "Explanation unreasonably long"
    
    @given(exception=exception_strategy())
    @settings(max_examples=100, deadline=None)
    def test_explanation_is_beginner_friendly(self, exception):
        """
        Property: Explanations should use beginner-friendly language.
        
        Educational messages should avoid overly technical jargon and
        provide clear, simple explanations.
        """
        wrapper = EducationalErrorWrapper()
        result = wrapper.wrap_error(exception)
        
        # Should contain beginner-friendly phrases
        beginner_phrases = [
            'Что произошло', 'Как исправить', 'Проверьте',
            'Убедитесь', 'Попробуйте', 'Пример'
        ]
        
        has_beginner_language = any(phrase in result for phrase in beginner_phrases)
        assert has_beginner_language, \
            "Explanation should use beginner-friendly language"
        
        # Should not be just a technical stack trace
        assert 'Traceback' not in result or 'Что произошло' in result, \
            "Should provide explanation, not just traceback"


class TestEducationalWrapperEdgeCases:
    """Test edge cases for educational error wrapper."""
    
    def test_wrapper_handles_exception_with_empty_message(self):
        """Test that wrapper handles exceptions with empty messages."""
        wrapper = EducationalErrorWrapper()
        exception = ValueError("")
        
        result = wrapper.wrap_error(exception)
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert 'ValueError' in result
    
    def test_wrapper_handles_exception_with_unicode(self):
        """Test that wrapper handles exceptions with unicode characters."""
        wrapper = EducationalErrorWrapper()
        exception = ValueError("Ошибка с юникодом: 你好 🎉")
        
        result = wrapper.wrap_error(exception)
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_wrapper_handles_nested_exceptions(self):
        """Test that wrapper handles nested exceptions."""
        wrapper = EducationalErrorWrapper()
        
        try:
            try:
                raise ValueError("Inner error")
            except ValueError as e:
                raise TypeError("Outer error") from e
        except TypeError as exception:
            result = wrapper.wrap_error(exception)
            
            assert isinstance(result, str)
            assert len(result) > 0
            assert 'TypeError' in result
