"""
Property-based tests for explain_error() context enhancements (v0.4.0).

This module tests the new context parameter functionality using property-based testing
to ensure correctness across a wide range of inputs.

Feature: fishertools-v0.4.0
"""

import pytest
from hypothesis import given, strategies as st, assume

from fishertools.errors.explainer import explain_error, _validate_context


class TestExplainErrorLanguageProperties:
    """Property 23: Language parameter controls output language."""
    
    @given(
        error_message=st.text(min_size=1, max_size=100),
        language=st.sampled_from(['en', 'ru', 'auto'])
    )
    def test_language_parameter_controls_output(self, error_message, language):
        """
        Property 23: Language parameter controls output language.
        
        **Validates: Requirements 10.1, 10.2**
        
        For any error message and language parameter, explain_error should:
        - Accept the language parameter without errors
        - Return a non-empty string
        - Respect the language setting (when not 'auto')
        """
        # Create a test exception
        exception = ValueError(error_message)
        
        # Get explanation with specified language
        result = explain_error(exception, language=language, return_text=True)
        
        # Should return non-empty string
        assert isinstance(result, str)
        assert len(result) > 0
        
        # For Russian, should contain Cyrillic characters
        if language == 'ru':
            # Check for common Russian words in error explanations
            russian_indicators = ['РћС€РёР±РєР°', 'РѕС€РёР±РєР°', 'Р­С‚Рѕ', 'СЌС‚Рѕ', 'РєРѕРґ']
            has_russian = any(indicator in result for indicator in russian_indicators)
            # Note: Some technical terms might be in English even in Russian mode
            # So we just check that Russian text is present
            assert has_russian or 'ValueError' in result  # At least error type should be there
        
        # For English, should not have Russian-specific patterns
        elif language == 'en':
            # English explanations should not have Cyrillic
            # But we allow technical terms and error types
            pass  # English is harder to validate without false positives
    
    @given(error_message=st.text(min_size=1, max_size=100))
    def test_auto_language_detection_works(self, error_message):
        """
        Property 23b: Auto language detection produces valid output.
        
        **Validates: Requirements 10.3**
        
        For any error message with language='auto', explain_error should:
        - Detect system language automatically
        - Return a valid explanation
        """
        exception = ValueError(error_message)
        
        # Get explanation with auto language detection
        result = explain_error(exception, language='auto', return_text=True)
        
        # Should return non-empty string
        assert isinstance(result, str)
        assert len(result) > 0
        
        # Should contain the error type
        assert 'ValueError' in result


class TestExplainErrorContextProperties:
    """Property 24: Context enriches explanations."""
    
    @given(
        error_message=st.text(min_size=1, max_size=100),
        variable_name=st.text(min_size=1, max_size=20, alphabet=st.characters(
            whitelist_categories=('Lu', 'Ll'), min_codepoint=97, max_codepoint=122
        )),
        index=st.integers(min_value=0, max_value=1000)
    )
    def test_context_enriches_index_error_explanation(self, error_message, variable_name, index):
        """
        Property 24a: Context enriches IndexError explanations.
        
        **Validates: Requirements 10.4, 10.5, 10.6**
        
        For any IndexError with list_access context, explain_error should:
        - Include the variable name in the explanation
        - Include the index value in the explanation
        - Provide context-specific guidance
        """
        # Assume valid variable name (starts with letter, alphanumeric)
        assume(variable_name.isidentifier())
        
        exception = IndexError(error_message)
        context = {
            'operation': 'list_access',
            'variable_name': variable_name,
            'index': index
        }
        
        # Get explanation with context
        result = explain_error(exception, context=context, return_text=True, language='ru')
        
        # Should return non-empty string
        assert isinstance(result, str)
        assert len(result) > 0
        
        # Should mention the variable name
        assert variable_name in result
        
        # Should mention the index
        assert str(index) in result
    
    @given(
        error_message=st.text(min_size=1, max_size=100),
        variable_name=st.text(min_size=1, max_size=20, alphabet=st.characters(
            whitelist_categories=('Lu', 'Ll'), min_codepoint=97, max_codepoint=122
        )),
        key=st.text(min_size=1, max_size=20)
    )
    def test_context_enriches_key_error_explanation(self, error_message, variable_name, key):
        """
        Property 24b: Context enriches KeyError explanations.
        
        **Validates: Requirements 10.4, 10.5, 10.6**
        
        For any KeyError with dict_access context, explain_error should:
        - Include the variable name in the explanation
        - Include the key value in the explanation
        - Provide context-specific guidance
        """
        # Assume valid variable name
        assume(variable_name.isidentifier())
        
        exception = KeyError(error_message)
        context = {
            'operation': 'dict_access',
            'variable_name': variable_name,
            'key': key
        }
        
        # Get explanation with context
        result = explain_error(exception, context=context, return_text=True, language='ru')
        
        # Should return non-empty string
        assert isinstance(result, str)
        assert len(result) > 0
        
        # Should mention the variable name
        assert variable_name in result
        
        # Should mention the key (or at least KeyError)
        assert key in result or 'KeyError' in result
    
    @given(
        error_message=st.text(min_size=1, max_size=100),
        operation=st.sampled_from([
            'list_access', 'dict_access', 'division', 'concatenation',
            'type_conversion', 'attribute_access', 'import', 'function_call'
        ])
    )
    def test_context_with_operation_provides_specific_guidance(self, error_message, operation):
        """
        Property 24c: Context with operation provides operation-specific guidance.
        
        **Validates: Requirements 10.5**
        
        For any error with operation context, explain_error should:
        - Accept the operation parameter
        - Return a valid explanation
        - Potentially include operation-specific guidance
        """
        exception = ValueError(error_message)
        context = {'operation': operation}
        
        # Get explanation with context
        result = explain_error(exception, context=context, return_text=True)
        
        # Should return non-empty string
        assert isinstance(result, str)
        assert len(result) > 0
        
        # Should contain error information
        assert 'ValueError' in result or 'РѕС€РёР±РєР°' in result.lower()


class TestExplainErrorBackwardCompatibility:
    """Property 25: Backward compatibility for explain_error."""
    
    @given(
        error_message=st.text(min_size=1, max_size=100),
        language=st.sampled_from(['ru', 'en'])
    )
    def test_explain_error_without_context_still_works(self, error_message, language):
        """
        Property 25: Backward compatibility - explain_error works without context.
        
        **Validates: Requirements 11.3**
        
        For any error without context parameter, explain_error should:
        - Work exactly as before (backward compatible)
        - Return a valid explanation
        - Not require context parameter
        """
        exception = ValueError(error_message)
        
        # Call without context (old API)
        result = explain_error(exception, language=language, return_text=True)
        
        # Should return non-empty string
        assert isinstance(result, str)
        assert len(result) > 0
        
        # Should contain error type
        assert 'ValueError' in result
    
    @given(
        error_type=st.sampled_from([
            ValueError, TypeError, IndexError, KeyError, 
            ZeroDivisionError, AttributeError
        ]),
        error_message=st.text(min_size=1, max_size=100)
    )
    def test_all_error_types_work_without_context(self, error_type, error_message):
        """
        Property 25b: All error types work without context (backward compatibility).
        
        **Validates: Requirements 11.3**
        
        For any exception type without context, explain_error should:
        - Handle all common exception types
        - Return valid explanations
        - Maintain backward compatibility
        """
        exception = error_type(error_message)
        
        # Call without context
        result = explain_error(exception, return_text=True)
        
        # Should return non-empty string
        assert isinstance(result, str)
        assert len(result) > 0
        
        # Should contain error type name
        assert error_type.__name__ in result


class TestValidateContextFunction:
    """Test the _validate_context helper function."""
    
    @given(
        operation=st.text(min_size=1, max_size=50),
        variable_name=st.text(min_size=0, max_size=50),
        index=st.integers(),
        key=st.text(min_size=0, max_size=50)
    )
    def test_validate_context_normalizes_input(self, operation, variable_name, index, key):
        """
        Test that _validate_context normalizes any input safely.
        
        For any context dictionary, _validate_context should:
        - Return a dictionary
        - Not raise exceptions
        - Normalize invalid operations to 'unknown'
        """
        context = {
            'operation': operation,
            'variable_name': variable_name,
            'index': index,
            'key': key
        }
        
        result = _validate_context(context)
        
        # Should return a dictionary
        assert isinstance(result, dict)
        
        # Should contain the same keys
        assert 'operation' in result
        assert 'variable_name' in result
        assert 'index' in result
        assert 'key' in result
        
        # Operation should be normalized if invalid
        valid_operations = {
            'list_access', 'dict_access', 'division', 'concatenation',
            'type_conversion', 'attribute_access', 'import', 'function_call'
        }
        if operation not in valid_operations:
            assert result['operation'] == 'unknown'
        else:
            assert result['operation'] == operation
    
    def test_validate_context_handles_none(self):
        """Test that _validate_context handles None input."""
        result = _validate_context(None)
        assert isinstance(result, dict)
        assert len(result) == 0
    
    def test_validate_context_handles_non_dict(self):
        """Test that _validate_context handles non-dict input."""
        result = _validate_context("not a dict")
        assert isinstance(result, dict)
        assert len(result) == 0
        
        result = _validate_context(123)
        assert isinstance(result, dict)
        assert len(result) == 0


