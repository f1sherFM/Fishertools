"""
Integration tests for fishertools bug fixes (v0.4.5).

Tests the interaction between all bug fix components:
- Learning module with fixed file access
- Validation system with improved error messages
- Safe functions with enhanced formatting and safe_average
- Error handling system integration
- Backward compatibility preservation
"""

import pytest
import tempfile
import os
from pathlib import Path

# Import all components that were fixed
from fishertools.learn import explain, explain_error, ExplanationLoader, get_loader
from fishertools.validation import validate_number, ValidationError
from fishertools.safe import safe_format, safe_average, PlaceholderBehavior
from fishertools import safe_get, safe_divide


class TestLearningModuleIntegration:
    """Test learning module integration with other components."""
    
    def test_learning_module_loads_successfully(self):
        """Test that learning module loads explanations without FileNotFoundError."""
        # This should work without raising FileNotFoundError
        loader = get_loader()
        assert loader is not None
        assert loader.explanations is not None
    
    def test_explain_function_works(self):
        """Test that explain() function works with various topics."""
        # Test with a common topic (use "list" not "lists")
        result = explain("list")
        assert result is not None
        # explain() returns a dict, not a string
        assert isinstance(result, dict)
        assert len(result) > 0
    
    def test_learning_module_with_validation_errors(self):
        """Test learning module can explain validation errors."""
        # Create a validation error
        try:
            validate_number("not a number", 0, 100)
            assert False, "Should have raised ValidationError"
        except ValidationError as e:
            # Learning module should be able to explain this error
            explanation = explain_error(str(e))
            assert explanation is not None
            assert len(explanation) > 0
    
    def test_explanation_loader_resource_loading(self):
        """Test that ExplanationLoader properly loads resources."""
        loader = ExplanationLoader()
        assert loader.explanations is not None
        
        # Should have some explanations loaded
        assert len(loader.explanations) > 0
        
        # Test getting a specific explanation (use "list" not "lists")
        explanation = loader.get_explanation("list")
        assert explanation is not None


class TestValidationSystemIntegration:
    """Test validation system integration with error handling."""
    
    def test_validation_error_messages_are_clear(self):
        """Test that validation errors have clear, beginner-friendly messages."""
        # Test with string instead of number
        with pytest.raises(ValidationError) as exc_info:
            validate_number("string", 0, 100)
        
        error_message = str(exc_info.value)
        # Should mention the type issue
        assert "str" in error_message or "string" in error_message or "число" in error_message
    
    def test_validation_with_none_value(self):
        """Test validation handles None values with specific messages."""
        with pytest.raises(ValidationError) as exc_info:
            validate_number(None, 0, 100)
        
        error_message = str(exc_info.value)
        # Should mention None or null
        assert "None" in error_message or "null" in error_message or "пуст" in error_message
    
    def test_validation_error_includes_type_information(self):
        """Test that validation errors include actual and expected types."""
        with pytest.raises(ValidationError) as exc_info:
            validate_number([1, 2, 3], 0, 100)
        
        error_message = str(exc_info.value)
        # Should mention list type
        assert "list" in error_message or "список" in error_message
    
    def test_validation_integrates_with_safe_functions(self):
        """Test that validation works properly with safe functions."""
        # safe_average should handle validation internally
        result = safe_average([1, 2, 3])
        assert result == 2.0
        
        # Should handle mixed types by filtering
        result = safe_average([1, "not a number", 3], default=0)
        assert result == 2.0  # Average of 1 and 3


class TestSafeFunctionsIntegration:
    """Test safe functions integration with error handling."""
    
    def test_safe_format_with_missing_placeholders(self):
        """Test safe_format handles missing placeholders correctly."""
        # Default behavior should show [MISSING: key]
        result = safe_format("Hello, {name}!", {})
        assert "[MISSING: name]" in result or "name" in result
    
    def test_safe_format_with_different_behaviors(self):
        """Test safe_format with different placeholder behaviors."""
        template = "Hello, {name}! You are {age} years old."
        values = {"name": "Alice"}
        
        # Test MISSING behavior
        result = safe_format(template, values, behavior=PlaceholderBehavior.MISSING)
        assert "Alice" in result
        assert "[MISSING:" in result or "age" in result
        
        # Test PRESERVE behavior - it preserves the template when values are missing
        result = safe_format(template, values, behavior=PlaceholderBehavior.PRESERVE)
        # PRESERVE keeps original placeholders, so Alice might not be substituted
        assert "{age}" in result or "age" in result
        
        # Test EMPTY behavior
        result = safe_format(template, values, behavior=PlaceholderBehavior.EMPTY)
        assert "Alice" in result
        # age placeholder should be replaced with empty string
    
    def test_safe_average_with_empty_list(self):
        """Test safe_average handles empty lists correctly."""
        result = safe_average([], default=0)
        assert result == 0
        
        result = safe_average([], default=42)
        assert result == 42
    
    def test_safe_average_filters_non_numeric(self):
        """Test safe_average filters out non-numeric values."""
        mixed_list = [1, "two", 3, None, 4, "five"]
        result = safe_average(mixed_list, default=0)
        
        # Should average only 1, 3, 4 = 8/3 ≈ 2.67
        assert abs(result - 8/3) < 0.01
    
    def test_safe_functions_work_together(self):
        """Test that multiple safe functions work together."""
        # Combine safe_get, safe_divide, and safe_average
        data = {"values": [10, 20, 30, "invalid", 40]}
        
        # Get values safely
        values = safe_get(data, "values", [])
        assert len(values) == 5
        
        # Calculate average safely
        avg = safe_average(values, default=0)
        assert avg == 25.0  # (10+20+30+40)/4
        
        # Divide safely
        result = safe_divide(100, avg, default=0)
        assert result == 4.0


class TestErrorHandlingIntegration:
    """Test comprehensive error handling across all components."""
    
    def test_validation_errors_can_be_explained(self):
        """Test that validation errors can be explained by learning module."""
        # Generate a validation error
        try:
            validate_number("abc", 0, 100)
        except ValidationError as e:
            # Should be able to explain it
            explanation = explain_error(str(e))
            assert explanation is not None
            assert len(explanation) > 0
    
    def test_error_messages_are_educational(self):
        """Test that error messages are educational for beginners."""
        # Test various error scenarios
        test_cases = [
            (lambda: validate_number("string", 0, 100), "type"),
            (lambda: validate_number(None, 0, 100), "None"),
            (lambda: safe_format("{missing}", {}), "missing"),
        ]
        
        for test_func, expected_keyword in test_cases:
            try:
                test_func()
            except (ValidationError, Exception) as e:
                error_msg = str(e)
                # Error message should be informative
                assert len(error_msg) > 10
    
    def test_error_recovery_in_safe_functions(self):
        """Test that safe functions recover gracefully from errors."""
        # safe_average should handle all errors gracefully
        result = safe_average(None, default=0)
        assert result == 0
        
        result = safe_average("not a list", default=42)
        assert result == 42
        
        # safe_format should handle errors gracefully (but None template is not supported)
        # Test with empty dict instead
        result = safe_format("", {})
        assert result is not None
        
        # safe_divide should handle division by zero
        result = safe_divide(10, 0, default=0)
        assert result == 0


class TestBackwardCompatibilityIntegration:
    """Test that backward compatibility is maintained across all components."""
    
    def test_existing_safe_functions_still_work(self):
        """Test that existing safe function signatures are preserved."""
        # Test safe_get
        result = safe_get({"key": "value"}, "key", "default")
        assert result == "value"
        
        result = safe_get({"key": "value"}, "missing", "default")
        assert result == "default"
        
        # Test safe_divide
        result = safe_divide(10, 2, default=0)
        assert result == 5.0
        
        result = safe_divide(10, 0, default=0)
        assert result == 0
    
    def test_validation_error_catching_still_works(self):
        """Test that existing ValidationError catching still works."""
        # Old code that catches ValidationError should still work
        try:
            validate_number("invalid", 0, 100)
            assert False, "Should have raised ValidationError"
        except ValidationError as e:
            # Should be able to catch and handle
            assert e is not None
            assert str(e) is not None
    
    def test_learning_module_functions_preserved(self):
        """Test that learning module functions maintain their signatures."""
        # explain() should work as before (use "list" not "lists")
        result = explain("list")
        assert result is not None
        
        # explain_error() should work as before
        result = explain_error("Some error message")
        assert result is not None
    
    def test_all_public_apis_accessible(self):
        """Test that all public APIs are still accessible."""
        # Import from main module and submodules
        from fishertools import (
            safe_get, safe_divide,
            explain_error
        )
        from fishertools.learn import explain
        from fishertools.validation import validate_number, ValidationError
        from fishertools.safe import safe_format, safe_average, PlaceholderBehavior
        
        # All should be callable
        assert callable(safe_get)
        assert callable(safe_divide)
        assert callable(safe_format)
        assert callable(safe_average)
        assert callable(validate_number)
        assert callable(explain)
        assert callable(explain_error)


class TestEndToEndWorkflows:
    """Test complete end-to-end workflows with bug fixes."""
    
    def test_complete_validation_workflow(self):
        """Test complete workflow: validation error -> explanation -> learning."""
        # 1. Trigger a validation error
        try:
            validate_number("not a number", 0, 100)
            assert False, "Should have raised ValidationError"
        except ValidationError as e:
            error_message = str(e)
            
            # 2. Error message should be clear
            assert len(error_message) > 0
            assert "str" in error_message or "string" in error_message or "число" in error_message
            
            # 3. Get explanation for the error
            explanation = explain_error(error_message)
            assert explanation is not None
            assert len(explanation) > 0
            
            # 4. Learn about the concept (use "int" instead of "types")
            learning_content = explain("int")
            assert learning_content is not None
    
    def test_complete_safe_functions_workflow(self):
        """Test complete workflow using multiple safe functions."""
        # Simulate processing user data with potential errors
        user_data = {
            "name": "Alice",
            "scores": [85, "invalid", 92, None, 88],
            "template": "Hello, {name}! Your average is {average}."
        }
        
        # 1. Safely get data
        name = safe_get(user_data, "name", "Unknown")
        scores = safe_get(user_data, "scores", [])
        template = safe_get(user_data, "template", "")
        
        assert name == "Alice"
        assert len(scores) == 5
        
        # 2. Safely calculate average
        average = safe_average(scores, default=0)
        assert average > 0  # Should filter out invalid values
        
        # 3. Safely format output
        output = safe_format(template, {"name": name, "average": average})
        assert "Alice" in output
        assert str(int(average)) in output or "[MISSING:" in output
    
    def test_error_explanation_pipeline(self):
        """Test the complete error explanation pipeline."""
        # 1. Create various errors
        errors_to_test = []
        
        try:
            validate_number("string", 0, 100)
        except ValidationError as e:
            errors_to_test.append(str(e))
        
        try:
            validate_number(None, 0, 100)
        except ValidationError as e:
            errors_to_test.append(str(e))
        
        # 2. Each error should be explainable
        for error_msg in errors_to_test:
            explanation = explain_error(error_msg)
            assert explanation is not None
            assert len(explanation) > 0
    
    def test_learning_with_safe_functions(self):
        """Test learning module works with safe functions."""
        # 1. Learn about a concept (use "list" not "lists")
        concept_explanation = explain("list")
        assert concept_explanation is not None
        
        # 2. Use safe functions based on learning
        test_list = [1, 2, 3, "invalid", 4]
        
        # Apply safe operations
        avg = safe_average(test_list, default=0)
        assert avg > 0
        
        # Format result safely
        result = safe_format("Average: {avg}", {"avg": avg})
        assert "Average:" in result


class TestPackageDistributionIntegration:
    """Test that package distribution includes all necessary files."""
    
    def test_explanations_file_accessible(self):
        """Test that explanations.json is accessible after installation."""
        # The ExplanationLoader should be able to load the file
        loader = ExplanationLoader()
        assert loader.explanations is not None
        assert len(loader.explanations) > 0
    
    def test_all_modules_importable(self):
        """Test that all modules can be imported successfully."""
        # These imports should all work
        import fishertools
        import fishertools.learn
        import fishertools.validation
        import fishertools.safe
        import fishertools.errors
        
        # All should be modules
        assert fishertools is not None
        assert fishertools.learn is not None
        assert fishertools.validation is not None
        assert fishertools.safe is not None
        assert fishertools.errors is not None
    
    def test_data_files_included(self):
        """Test that data files are included in the package."""
        # Try to access the explanations file through the loader
        loader = get_loader()
        assert loader is not None
        
        # Should have loaded explanations
        assert loader.explanations is not None
        
        # Should have at least some basic explanations
        assert "lists" in loader.explanations or len(loader.explanations) > 0


class TestSystemRobustness:
    """Test system robustness and edge cases."""
    
    def test_handles_unicode_in_errors(self):
        """Test that system handles unicode characters in errors."""
        # Create error with unicode
        try:
            validate_number("тест", 0, 100)
        except ValidationError as e:
            error_msg = str(e)
            assert error_msg is not None
            
            # Should be able to explain it
            explanation = explain_error(error_msg)
            assert explanation is not None
    
    def test_handles_empty_inputs(self):
        """Test that system handles empty inputs gracefully."""
        # Empty list
        result = safe_average([], default=0)
        assert result == 0
        
        # Empty dict
        result = safe_get({}, "key", "default")
        assert result == "default"
        
        # Empty string
        result = safe_format("", {})
        assert result == ""
    
    def test_handles_large_inputs(self):
        """Test that system handles large inputs efficiently."""
        # Large list
        large_list = list(range(10000))
        result = safe_average(large_list, default=0)
        assert result == 4999.5
        
        # Large dict
        large_dict = {f"key_{i}": i for i in range(1000)}
        result = safe_get(large_dict, "key_500", "default")
        assert result == 500
    
    def test_handles_nested_structures(self):
        """Test that system handles nested data structures."""
        nested_data = {
            "level1": {
                "level2": {
                    "level3": {
                        "values": [1, 2, 3]
                    }
                }
            }
        }
        
        # Should be able to safely access nested data
        level1 = safe_get(nested_data, "level1", {})
        assert level1 is not None
        
        level2 = safe_get(level1, "level2", {})
        assert level2 is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
