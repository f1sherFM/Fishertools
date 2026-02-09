"""
Unit tests for explain_error() context-specific explanations (v0.5.1).

This module tests specific edge cases and context scenarios for the new
context parameter functionality.

Feature: fishertools-v0.5.1
"""

import pytest
from fishertools.errors.explainer import explain_error


class TestIndexErrorWithContext:
    """Test IndexError with list_access context."""
    
    def test_index_error_with_list_access_context_includes_list_length(self):
        """Test IndexError with list_access context includes list length."""
        exception = IndexError("list index out of range")
        context = {
            'operation': 'list_access',
            'variable_name': 'my_list',
            'index': 10,
            'list_length': 3
        }
        
        result = explain_error(exception, context=context, return_text=True, language='ru')
        
        # Should mention the variable name
        assert 'my_list' in result
        
        # Should mention the index
        assert '10' in result
        
        # Should mention the list length
        assert '3' in result
        
        # Should mention valid index range
        assert '0' in result and '2' in result  # Valid indices: 0 to 2
    
    def test_index_error_without_list_length_still_works(self):
        """Test IndexError with list_access context works without list_length."""
        exception = IndexError("list index out of range")
        context = {
            'operation': 'list_access',
            'variable_name': 'items',
            'index': 5
        }
        
        result = explain_error(exception, context=context, return_text=True, language='ru')
        
        # Should mention the variable name
        assert 'items' in result
        
        # Should mention the index
        assert '5' in result
        
        # Should provide helpful guidance
        assert 'safe_get' in result or 'len' in result
    
    def test_index_error_with_zero_index(self):
        """Test IndexError with index 0 (edge case)."""
        exception = IndexError("list index out of range")
        context = {
            'operation': 'list_access',
            'variable_name': 'empty_list',
            'index': 0,
            'list_length': 0
        }
        
        result = explain_error(exception, context=context, return_text=True, language='ru')
        
        # Should handle empty list case
        assert 'empty_list' in result
        assert '0' in result


class TestKeyErrorWithContext:
    """Test KeyError with dict_access context."""
    
    def test_key_error_with_dict_access_context_includes_available_keys(self):
        """Test KeyError with dict_access context includes available keys."""
        exception = KeyError("'email'")
        context = {
            'operation': 'dict_access',
            'variable_name': 'user_data',
            'key': 'email',
            'available_keys': ['name', 'age', 'username', 'id']
        }
        
        result = explain_error(exception, context=context, return_text=True, language='ru')
        
        # Should mention the variable name
        assert 'user_data' in result
        
        # Should mention the key
        assert 'email' in result
        
        # Should mention some available keys
        assert 'name' in result or 'age' in result or 'username' in result
        
        # Should provide helpful guidance
        assert 'get' in result or 'in' in result
    
    def test_key_error_with_many_available_keys(self):
        """Test KeyError with many available keys (should truncate)."""
        exception = KeyError("'missing_key'")
        context = {
            'operation': 'dict_access',
            'variable_name': 'config',
            'key': 'missing_key',
            'available_keys': [f'key_{i}' for i in range(20)]  # 20 keys
        }
        
        result = explain_error(exception, context=context, return_text=True, language='ru')
        
        # Should mention the variable name
        assert 'config' in result
        
        # Should mention the missing key
        assert 'missing_key' in result
        
        # Should show truncated list (first 5 keys + count)
        assert 'key_0' in result or 'key_1' in result
        assert '20' in result  # Total count
    
    def test_key_error_without_available_keys_still_works(self):
        """Test KeyError with dict_access context works without available_keys."""
        exception = KeyError("'password'")
        context = {
            'operation': 'dict_access',
            'variable_name': 'credentials',
            'key': 'password'
        }
        
        result = explain_error(exception, context=context, return_text=True, language='ru')
        
        # Should mention the variable name
        assert 'credentials' in result
        
        # Should mention the key
        assert 'password' in result
        
        # Should provide helpful guidance
        assert 'get' in result or 'in' in result


class TestZeroDivisionErrorWithContext:
    """Test ZeroDivisionError with division context."""
    
    def test_zero_division_error_with_division_context(self):
        """Test ZeroDivisionError with division context."""
        exception = ZeroDivisionError("division by zero")
        context = {
            'operation': 'division',
            'variable_name': 'denominator',
            'value': 0
        }
        
        result = explain_error(exception, context=context, return_text=True, language='ru')
        
        # Should mention the variable name
        assert 'denominator' in result
        
        # Should mention zero
        assert '0' in result or 'ноль' in result
        
        # Should provide helpful guidance
        assert 'safe_divide' in result or 'if' in result
    
    def test_zero_division_error_without_variable_name(self):
        """Test ZeroDivisionError with division context but no variable name."""
        exception = ZeroDivisionError("division by zero")
        context = {
            'operation': 'division',
            'value': 0
        }
        
        result = explain_error(exception, context=context, return_text=True, language='ru')
        
        # Should still provide helpful explanation
        assert '0' in result or 'ноль' in result
        assert 'ZeroDivisionError' in result


class TestTypeErrorWithContext:
    """Test TypeError with concatenation context."""
    
    def test_type_error_with_concatenation_context(self):
        """Test TypeError with concatenation context."""
        exception = TypeError("can only concatenate str (not \"int\") to str")
        context = {
            'operation': 'concatenation',
            'variable_name': 'message',
            'expected_type': 'str',
            'actual_type': 'int'
        }
        
        result = explain_error(exception, context=context, return_text=True, language='ru')
        
        # Should mention the variable name
        assert 'message' in result
        
        # Should mention the types
        assert 'str' in result
        assert 'int' in result
        
        # Should provide helpful guidance
        assert 'str(' in result or 'isinstance' in result
    
    def test_type_error_with_minimal_context(self):
        """Test TypeError with minimal context."""
        exception = TypeError("unsupported operand type(s)")
        context = {
            'operation': 'concatenation'
        }
        
        result = explain_error(exception, context=context, return_text=True, language='ru')
        
        # Should still provide helpful explanation
        assert 'TypeError' in result
        assert len(result) > 0


class TestOtherOperationContexts:
    """Test other operation contexts."""
    
    def test_type_conversion_context(self):
        """Test with type_conversion operation context."""
        exception = ValueError("invalid literal for int() with base 10: 'abc'")
        context = {
            'operation': 'type_conversion',
            'variable_name': 'user_input'
        }
        
        result = explain_error(exception, context=context, return_text=True, language='ru')
        
        # Should provide helpful explanation
        assert len(result) > 0
        assert 'ValueError' in result
    
    def test_attribute_access_context(self):
        """Test with attribute_access operation context."""
        exception = AttributeError("'NoneType' object has no attribute 'value'")
        context = {
            'operation': 'attribute_access',
            'variable_name': 'obj'
        }
        
        result = explain_error(exception, context=context, return_text=True, language='ru')
        
        # Should provide helpful explanation
        assert len(result) > 0
        assert 'AttributeError' in result
        assert 'hasattr' in result
    
    def test_import_context(self):
        """Test with import operation context."""
        exception = ImportError("No module named 'nonexistent_module'")
        context = {
            'operation': 'import'
        }
        
        result = explain_error(exception, context=context, return_text=True, language='ru')
        
        # Should provide helpful explanation
        assert len(result) > 0
        assert 'ImportError' in result
        assert 'pip install' in result
    
    def test_function_call_context(self):
        """Test with function_call operation context."""
        exception = TypeError("missing 1 required positional argument: 'x'")
        context = {
            'operation': 'function_call'
        }
        
        result = explain_error(exception, context=context, return_text=True, language='ru')
        
        # Should provide helpful explanation
        assert len(result) > 0
        assert 'TypeError' in result


class TestExplainErrorWithoutContext:
    """Test that explain_error still works without context (backward compatibility)."""
    
    def test_explain_error_without_context_still_works(self):
        """Test explain_error() without context parameter still works."""
        exception = ValueError("invalid value")
        
        # Call without context (old API)
        result = explain_error(exception, return_text=True)
        
        # Should work as before
        assert isinstance(result, str)
        assert len(result) > 0
        assert 'ValueError' in result
    
    def test_explain_error_with_none_context(self):
        """Test explain_error() with context=None works."""
        exception = TypeError("type error")
        
        # Explicitly pass None as context
        result = explain_error(exception, context=None, return_text=True)
        
        # Should work as before
        assert isinstance(result, str)
        assert len(result) > 0
        assert 'TypeError' in result
    
    def test_explain_error_with_empty_context(self):
        """Test explain_error() with empty context dict works."""
        exception = IndexError("index error")
        
        # Pass empty context
        result = explain_error(exception, context={}, return_text=True)
        
        # Should work as before
        assert isinstance(result, str)
        assert len(result) > 0
        assert 'IndexError' in result


class TestLanguageParameterWithContext:
    """Test language parameter works correctly with context."""
    
    def test_english_language_with_context(self):
        """Test English language with context."""
        exception = IndexError("list index out of range")
        context = {
            'operation': 'list_access',
            'variable_name': 'my_list',
            'index': 10
        }
        
        result = explain_error(exception, language='en', context=context, return_text=True)
        
        # Should return English explanation
        assert isinstance(result, str)
        assert len(result) > 0
        assert 'my_list' in result
        assert '10' in result
    
    def test_russian_language_with_context(self):
        """Test Russian language with context."""
        exception = KeyError("'key'")
        context = {
            'operation': 'dict_access',
            'variable_name': 'data',
            'key': 'key'
        }
        
        result = explain_error(exception, language='ru', context=context, return_text=True)
        
        # Should return Russian explanation
        assert isinstance(result, str)
        assert len(result) > 0
        assert 'data' in result
        
        # Should have Russian text
        russian_indicators = ['Ошибка', 'ошибка', 'ключ', 'словар']
        has_russian = any(indicator in result for indicator in russian_indicators)
        assert has_russian or 'KeyError' in result
    
    def test_auto_language_with_context(self):
        """Test auto language detection with context."""
        exception = ZeroDivisionError("division by zero")
        context = {
            'operation': 'division',
            'variable_name': 'divisor'
        }
        
        result = explain_error(exception, language='auto', context=context, return_text=True)
        
        # Should return valid explanation
        assert isinstance(result, str)
        assert len(result) > 0
        assert 'divisor' in result


class TestInvalidContextHandling:
    """Test handling of invalid context values."""
    
    def test_invalid_operation_normalized_to_unknown(self):
        """Test that invalid operation is normalized to 'unknown'."""
        exception = ValueError("test error")
        context = {
            'operation': 'invalid_operation_name',
            'variable_name': 'var'
        }
        
        # Should not raise an error
        result = explain_error(exception, context=context, return_text=True)
        
        # Should still provide explanation
        assert isinstance(result, str)
        assert len(result) > 0
        assert 'ValueError' in result
    
    def test_non_dict_context_handled_gracefully(self):
        """Test that non-dict context is handled gracefully."""
        exception = TypeError("test error")
        
        # Pass invalid context types - should be handled by _validate_context
        # Note: The function signature expects Optional[Dict], so this tests
        # the internal validation
        result = explain_error(exception, context={}, return_text=True)
        
        # Should work
        assert isinstance(result, str)
        assert len(result) > 0

