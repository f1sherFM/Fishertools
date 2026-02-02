"""
Property-based tests for error explanation parsing in fishertools.learn.

Tests the correctness properties of the explain_error function using hypothesis
for property-based testing.

**Feature: fishertools-bug-fixes, Property 3: Error Explanation Parsing**

**Validates: Requirements 3.1**
"""

import pytest
from hypothesis import given, strategies as st, assume
from typing import Any

from fishertools.learn.error_explanations import explain_error


class TestErrorExplanationParsing:
    """
    Property 3: Error Explanation Parsing
    
    For any ValidationError message, explain_error() should parse the error and 
    provide contextual explanations or helpful fallback guidance.
    
    **Feature: fishertools-bug-fixes, Property 3: Error Explanation Parsing**
    **Validates: Requirements 3.1**
    """
    
    @given(
        error_message=st.one_of(
            st.text(min_size=1, max_size=200),  # General error messages
            st.from_regex(r'Expected \w+, got \w+'),  # Type mismatch pattern
            st.from_regex(r'Value .+ must be between .+ and .+'),  # Range pattern
            st.from_regex(r'Value cannot be None'),  # None value pattern
            st.from_regex(r"unsupported operand type.*'\w+' and '\w+'"),  # TypeError pattern
            st.from_regex(r"'\w+' object has no attribute '\w+'"),  # AttributeError pattern
        )
    )
    def test_explain_error_always_returns_structured_explanation(self, error_message):
        """
        Property test: For any error message, explain_error() should return a structured explanation.
        
        This test validates that explain_error() always returns a dictionary with the required
        fields, regardless of whether the error message matches a known pattern or not.
        
        **Validates: Requirements 3.1**
        """
        # Skip empty or whitespace-only messages
        assume(error_message.strip())
        
        result = explain_error(error_message)
        
        # Verify result is a dictionary
        assert isinstance(result, dict), f"explain_error should return dict, got {type(result)}"
        
        # Verify required fields are present
        required_fields = ["explanation", "suggestions", "example_fix", "common_causes", "original_error"]
        for field in required_fields:
            assert field in result, f"Missing required field '{field}' in result"
        
        # Verify field types
        assert isinstance(result["explanation"], str), "explanation should be a string"
        assert isinstance(result["suggestions"], list), "suggestions should be a list"
        assert isinstance(result["example_fix"], str), "example_fix should be a string"
        assert isinstance(result["common_causes"], list), "common_causes should be a list"
        assert isinstance(result["original_error"], str), "original_error should be a string"
        
        # Verify content is not empty
        assert result["explanation"].strip(), "explanation should not be empty"
        assert len(result["suggestions"]) > 0, "suggestions should not be empty"
        assert result["example_fix"].strip(), "example_fix should not be empty"
        assert len(result["common_causes"]) > 0, "common_causes should not be empty"
        
        # Verify original error is preserved
        assert result["original_error"] == error_message, "original_error should match input"
    
    @given(
        validation_error_message=st.one_of(
            st.from_regex(r'Expected number, got str'),
            st.from_regex(r'Expected int, got float'),
            st.from_regex(r'Expected string, got int'),
            st.from_regex(r'Value \d+ must be between \d+ and \d+'),
            st.from_regex(r'Value cannot be None'),
        )
    )
    def test_validation_error_patterns_provide_specific_explanations(self, validation_error_message):
        """
        Property test: ValidationError patterns should provide specific, contextual explanations.
        
        This test validates that known ValidationError patterns are recognized and provide
        specific explanations rather than generic fallback explanations.
        
        **Validates: Requirements 3.1, 3.2**
        """
        result = explain_error(validation_error_message)
        
        # For known patterns, explanations should be specific and educational
        explanation = result["explanation"].lower()
        
        # Should not be the generic fallback explanation
        assert "произошла ошибка в вашем коде" not in explanation, \
            "Should provide specific explanation, not generic fallback"
        
        # Should contain educational content about the specific error type
        if "expected" in validation_error_message.lower() and "got" in validation_error_message.lower():
            # Type mismatch errors should explain type compatibility
            assert any(keyword in explanation for keyword in ["тип", "данных", "функция", "ожидала"]), \
                f"Type mismatch explanation should mention types or functions: {explanation}"
        
        elif "must be between" in validation_error_message.lower():
            # Range errors should explain boundaries
            assert any(keyword in explanation for keyword in ["диапазон", "границ", "значение"]), \
                f"Range error explanation should mention ranges or boundaries: {explanation}"
        
        elif "cannot be none" in validation_error_message.lower():
            # None errors should explain null values
            assert any(keyword in explanation for keyword in ["none", "пустое", "значение", "отсутств"]), \
                f"None error explanation should mention null/empty values: {explanation}"
    
    @given(
        unknown_error_message=st.text(min_size=5, max_size=100).filter(
            lambda x: not any(pattern in x.lower() for pattern in [
                "expected", "got", "must be between", "cannot be none", 
                "unsupported operand", "has no attribute"
            ])
        )
    )
    def test_unknown_patterns_provide_helpful_fallback(self, unknown_error_message):
        """
        Property test: Unknown error patterns should provide helpful fallback explanations.
        
        This test validates that when explain_error() cannot find a specific pattern match,
        it provides a helpful generic explanation with useful suggestions.
        
        **Validates: Requirements 3.3**
        """
        # Skip empty or whitespace-only messages
        assume(unknown_error_message.strip())
        
        result = explain_error(unknown_error_message)
        
        # Should provide fallback explanation
        explanation = result["explanation"].lower()
        assert "произошла ошибка" in explanation or "ошибка в" in explanation, \
            "Should provide fallback explanation for unknown patterns"
        
        # Should provide general debugging suggestions
        suggestions = [s.lower() for s in result["suggestions"]]
        helpful_keywords = ["проверьте", "убедитесь", "попробуйте", "используйте", "добавьте"]
        assert any(keyword in " ".join(suggestions) for keyword in helpful_keywords), \
            "Fallback suggestions should contain helpful debugging advice"
        
        # Should provide general debugging example
        example = result["example_fix"].lower()
        assert any(keyword in example for keyword in ["print", "try", "except", "type"]), \
            "Fallback example should contain general debugging techniques"
    
    @given(
        error_input=st.one_of(
            st.none(),
            st.text(max_size=0),  # Empty string
            st.just("   "),       # Whitespace only
        )
    )
    def test_edge_case_inputs_handled_gracefully(self, error_input):
        """
        Property test: Edge case inputs should be handled gracefully.
        
        This test validates that explain_error() handles edge cases like None,
        empty strings, and whitespace-only strings without crashing.
        
        **Validates: Requirements 3.1**
        """
        # Should not raise exceptions for edge cases
        result = explain_error(error_input)
        
        # Should still return structured result
        assert isinstance(result, dict), "Should return dict even for edge cases"
        
        # Should have all required fields
        required_fields = ["explanation", "suggestions", "example_fix", "common_causes", "original_error"]
        for field in required_fields:
            assert field in result, f"Missing field '{field}' for edge case input"
        
        # Should provide helpful content even for edge cases
        assert result["explanation"].strip(), "Should provide explanation for edge cases"
        assert len(result["suggestions"]) > 0, "Should provide suggestions for edge cases"
    
    @given(
        non_string_input=st.one_of(
            st.integers(),
            st.floats(allow_nan=False, allow_infinity=False),
            st.booleans(),
            st.lists(st.text()),
            st.dictionaries(st.text(), st.text()),
        )
    )
    def test_non_string_inputs_converted_to_string(self, non_string_input):
        """
        Property test: Non-string inputs should be converted to strings gracefully.
        
        This test validates that explain_error() can handle non-string inputs
        by converting them to strings before processing.
        
        **Validates: Requirements 3.1**
        """
        # Should not raise exceptions for non-string inputs
        result = explain_error(non_string_input)
        
        # Should return structured result
        assert isinstance(result, dict), "Should return dict for non-string inputs"
        
        # Original error should be string representation of input
        assert result["original_error"] == str(non_string_input), \
            "Should convert non-string input to string representation"
        
        # Should provide meaningful explanation
        assert result["explanation"].strip(), "Should provide explanation for non-string inputs"
    
    @given(
        error_message=st.text(min_size=1, max_size=50)
    )
    def test_explanation_quality_metrics(self, error_message):
        """
        Property test: All explanations should meet quality metrics.
        
        This test validates that explanations are educational, actionable,
        and appropriate for beginners learning Python.
        
        **Validates: Requirements 3.1, 3.4**
        """
        assume(error_message.strip())
        
        result = explain_error(error_message)
        
        # Explanation should be educational (reasonable length)
        explanation = result["explanation"]
        assert 20 <= len(explanation) <= 500, \
            f"Explanation should be educational length (20-500 chars), got {len(explanation)}"
        
        # Suggestions should be actionable (contain action words)
        suggestions_text = " ".join(result["suggestions"]).lower()
        action_words = ["проверьте", "убедитесь", "используйте", "добавьте", "попробуйте", "измените"]
        assert any(word in suggestions_text for word in action_words), \
            "Suggestions should contain actionable advice"
        
        # Example should contain code (has code-like elements)
        example = result["example_fix"]
        code_indicators = ["=", "(", ")", "def", "if", "print", "#", "import"]
        assert any(indicator in example for indicator in code_indicators), \
            "Example should contain code-like elements"
        
        # Common causes should be informative
        causes_text = " ".join(result["common_causes"]).lower()
        assert len(causes_text) > 10, "Common causes should provide informative content"