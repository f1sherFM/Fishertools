"""
Unit tests for specific error explanation scenarios in fishertools.learn.

Tests specific examples and edge cases for the explain_error function,
focusing on pattern recognition and fallback behavior.

**Validates: Requirements 3.2, 3.3**
"""

import pytest
from fishertools.learn.error_explanations import explain_error


class TestSpecificErrorExplanationScenarios:
    """Test specific error explanation scenarios and pattern recognition."""
    
    def test_type_mismatch_pattern_recognition(self):
        """
        Test "must be int, got str" pattern recognition.
        
        **Validates: Requirements 3.2**
        """
        error_message = "Expected int, got str"
        result = explain_error(error_message)
        
        # Should recognize the pattern and provide specific explanation
        assert "функция ожидала" in result["explanation"].lower()
        assert "тип данных" in result["explanation"].lower()
        
        # Should provide type-specific suggestions
        suggestions_text = " ".join(result["suggestions"]).lower()
        assert "тип данных" in suggestions_text or "преобразования типов" in suggestions_text
        assert "int()" in suggestions_text or "str()" in suggestions_text or "float()" in suggestions_text
        
        # Should provide code example with type conversion
        example = result["example_fix"]
        assert "int(" in example or "str(" in example or "float(" in example
        assert "validate_number" in example  # Should show correct usage
        
        # Should list common causes related to type mismatches
        causes_text = " ".join(result["common_causes"]).lower()
        assert any(cause in causes_text for cause in ["строки", "числа", "типов", "преобразован"])
    
    def test_number_string_type_mismatch(self):
        """Test specific case: Expected number, got str."""
        error_message = "Expected number, got str"
        result = explain_error(error_message)
        
        # Should provide specific explanation about number vs string
        explanation = result["explanation"].lower()
        assert "функция ожидала" in explanation
        assert "тип данных" in explanation or "получила другой" in explanation
        
        # Should suggest type conversion
        suggestions = result["suggestions"]
        assert len(suggestions) >= 2
        type_conversion_mentioned = any(
            "int()" in s or "float()" in s or "преобразования типов" in s.lower()
            for s in suggestions
        )
        assert type_conversion_mentioned, "Should mention type conversion functions"
    
    def test_range_validation_pattern_recognition(self):
        """Test range validation error pattern recognition."""
        error_message = "Value 150 must be between 0 and 100"
        result = explain_error(error_message)
        
        # Should recognize range validation pattern
        explanation = result["explanation"].lower()
        assert "диапазон" in explanation or "границ" in explanation
        
        # Should provide range-specific suggestions
        suggestions_text = " ".join(result["suggestions"]).lower()
        assert "диапазон" in suggestions_text or "границ" in suggestions_text
        assert "min()" in suggestions_text or "max()" in suggestions_text
        
        # Should show example with range limiting
        example = result["example_fix"]
        assert "min(" in example or "max(" in example
        assert "validate_number" in example
    
    def test_none_value_pattern_recognition(self):
        """Test None value error pattern recognition."""
        error_message = "Value cannot be None"
        result = explain_error(error_message)
        
        # Should recognize None pattern
        explanation = result["explanation"].lower()
        assert "none" in explanation or "пустое значение" in explanation
        
        # Should provide None-specific suggestions
        suggestions_text = " ".join(result["suggestions"]).lower()
        assert "none" in suggestions_text or "инициализирован" in suggestions_text
        
        # Should show example with None checking
        example = result["example_fix"]
        assert "is not None" in example or "is None" in example
        assert "None" in example
    
    def test_attribute_error_pattern_recognition(self):
        """Test AttributeError pattern recognition."""
        error_message = "'str' object has no attribute 'append'"
        result = explain_error(error_message)
        
        # Should recognize AttributeError pattern
        explanation = result["explanation"].lower()
        assert "атрибут" in explanation or "метод" in explanation
        assert "не существует" in explanation or "нет" in explanation
        
        # Should provide attribute-specific suggestions
        suggestions_text = " ".join(result["suggestions"]).lower()
        assert "атрибут" in suggestions_text or "метод" in suggestions_text
        assert "dir(" in suggestions_text or "правильность" in suggestions_text
        
        # Should show example with correct method usage
        example = result["example_fix"]
        assert "append" in example  # Should show correct usage context
        assert "список" in example.lower() or "list" in example.lower()
    
    def test_type_error_operand_pattern_recognition(self):
        """Test TypeError operand pattern recognition."""
        error_message = "unsupported operand type(s) for +: 'int' and 'str'"
        result = explain_error(error_message)
        
        # Should recognize operand type error
        explanation = result["explanation"].lower()
        assert "операц" in explanation or "несовместим" in explanation
        assert "тип" in explanation
        
        # Should provide operand-specific suggestions
        suggestions_text = " ".join(result["suggestions"]).lower()
        assert "совместим" in suggestions_text or "преобразован" in suggestions_text
        
        # Should show example with type conversion
        example = result["example_fix"]
        assert "+" in example  # Should show addition operation
        assert ("int(" in example and "str(" in example) or "преобразуем" in example.lower()
    
    def test_fallback_behavior_for_unknown_patterns(self):
        """
        Test fallback behavior for unknown error patterns.
        
        **Validates: Requirements 3.3**
        """
        unknown_error_message = "This is a completely unknown error message format"
        result = explain_error(unknown_error_message)
        
        # Should provide fallback explanation
        explanation = result["explanation"].lower()
        assert "произошла ошибка" in explanation
        assert "программирования" in explanation or "код" in explanation
        
        # Should provide general debugging suggestions
        suggestions = result["suggestions"]
        assert len(suggestions) >= 3  # Should provide multiple helpful suggestions
        
        suggestions_text = " ".join(suggestions).lower()
        general_advice_keywords = ["проверьте", "убедитесь", "попробуйте", "используйте"]
        assert any(keyword in suggestions_text for keyword in general_advice_keywords)
        
        # Should provide general debugging example
        example = result["example_fix"]
        assert "print(" in example  # Should show debugging techniques
        assert "try:" in example and "except" in example  # Should show error handling
        
        # Should list general common causes
        causes = result["common_causes"]
        assert len(causes) >= 3
        causes_text = " ".join(causes).lower()
        general_causes = ["опечатк", "тип", "переменн", "логическ"]
        assert any(cause in causes_text for cause in general_causes)
    
    def test_empty_error_message_fallback(self):
        """Test fallback behavior for empty error messages."""
        result = explain_error("")
        
        # Should handle empty message gracefully
        assert isinstance(result, dict)
        assert "explanation" in result
        assert "suggestions" in result
        assert result["explanation"].strip()  # Should not be empty
        assert len(result["suggestions"]) > 0  # Should provide suggestions
    
    def test_whitespace_only_error_message(self):
        """Test handling of whitespace-only error messages."""
        result = explain_error("   \t\n   ")
        
        # Should handle whitespace gracefully
        assert isinstance(result, dict)
        assert result["explanation"].strip()
        assert len(result["suggestions"]) > 0
    
    def test_very_long_error_message(self):
        """Test handling of very long error messages."""
        long_message = "This is a very long error message " * 20
        result = explain_error(long_message)
        
        # Should handle long messages without issues
        assert isinstance(result, dict)
        assert result["original_error"] == long_message
        assert result["explanation"].strip()
        assert len(result["suggestions"]) > 0
    
    def test_error_message_with_special_characters(self):
        """Test handling of error messages with special characters."""
        special_message = "Error with special chars: @#$%^&*()[]{}|\\:;\"'<>?,./"
        result = explain_error(special_message)
        
        # Should handle special characters gracefully
        assert isinstance(result, dict)
        assert result["original_error"] == special_message
        assert result["explanation"].strip()
    
    def test_multiple_pattern_matches_priority(self):
        """Test behavior when error message could match multiple patterns."""
        # This message could match both "Expected X, got Y" and "Value cannot be None" patterns
        complex_message = "Expected number, got NoneType - Value cannot be None"
        result = explain_error(complex_message)
        
        # Should match the first applicable pattern
        assert isinstance(result, dict)
        explanation = result["explanation"].lower()
        
        # Should provide specific explanation (not fallback)
        assert "произошла ошибка в вашем коде" not in explanation
        
        # Should be coherent and helpful
        assert len(result["suggestions"]) > 0
        assert result["example_fix"].strip()
    
    def test_case_insensitive_pattern_matching(self):
        """Test that pattern matching is case-insensitive."""
        # Test with different cases
        messages = [
            "Expected number, got str",
            "EXPECTED NUMBER, GOT STR", 
            "expected number, got str",
            "Expected Number, Got Str"
        ]
        
        results = [explain_error(msg) for msg in messages]
        
        # All should be recognized as the same pattern type
        for result in results:
            explanation = result["explanation"].lower()
            assert "функция ожидала" in explanation or "тип данных" in explanation
            # Should not be fallback explanation
            assert "произошла ошибка в вашем коде" not in explanation
    
    def test_original_error_preservation(self):
        """Test that original error message is always preserved."""
        test_messages = [
            "Expected int, got str",
            "Unknown error format",
            "",
            "Value 50 must be between 0 and 10"
        ]
        
        for message in test_messages:
            result = explain_error(message)
            assert result["original_error"] == message, \
                f"Original error not preserved for: {message}"
    
    def test_explanation_structure_consistency(self):
        """Test that all explanations have consistent structure."""
        test_messages = [
            "Expected number, got str",
            "Value cannot be None", 
            "Unknown error pattern",
            "'list' object has no attribute 'append'"
        ]
        
        for message in test_messages:
            result = explain_error(message)
            
            # Check required fields
            required_fields = ["explanation", "suggestions", "example_fix", "common_causes", "original_error"]
            for field in required_fields:
                assert field in result, f"Missing field '{field}' for message: {message}"
                
            # Check field types and content
            assert isinstance(result["explanation"], str) and result["explanation"].strip()
            assert isinstance(result["suggestions"], list) and len(result["suggestions"]) > 0
            assert isinstance(result["example_fix"], str) and result["example_fix"].strip()
            assert isinstance(result["common_causes"], list) and len(result["common_causes"]) > 0
            assert isinstance(result["original_error"], str)