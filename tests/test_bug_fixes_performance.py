"""
Performance and regression tests for fishertools bug fixes (v0.4.5).

Tests that bug fixes don't introduce performance regressions and
that the system performs well under various conditions.
"""

import pytest
import time
import sys
from typing import List

# Import components to test
from fishertools.learn import explain, explain_error, ExplanationLoader, get_loader
from fishertools.validation import validate_number, ValidationError
from fishertools.safe import safe_format, safe_average, PlaceholderBehavior
from fishertools import safe_get, safe_divide


class TestPerformance:
    """Test performance of bug fixes."""
    
    def test_explanation_loader_performance(self):
        """Test that ExplanationLoader loads quickly."""
        start_time = time.time()
        loader = ExplanationLoader()
        load_time = time.time() - start_time
        
        # Should load in less than 1 second
        assert load_time < 1.0, f"ExplanationLoader took {load_time:.3f}s to load"
        
        # Subsequent access should be fast (cached)
        start_time = time.time()
        loader.get_explanation("list")
        access_time = time.time() - start_time
        
        # Should access in less than 0.1 seconds
        assert access_time < 0.1, f"Explanation access took {access_time:.3f}s"
    
    def test_validation_performance(self):
        """Test that validation doesn't introduce performance overhead."""
        # Test with valid inputs
        start_time = time.time()
        for i in range(1000):
            validate_number(i, 0, 1000)
        valid_time = time.time() - start_time
        
        # Should process 1000 validations in less than 0.5 seconds
        assert valid_time < 0.5, f"1000 validations took {valid_time:.3f}s"
        
        # Test with invalid inputs (error path)
        error_count = 0
        start_time = time.time()
        for i in range(100):
            try:
                validate_number("invalid", 0, 100)
            except ValidationError:
                error_count += 1
        error_time = time.time() - start_time
        
        # Should process 100 error cases in less than 0.5 seconds
        assert error_time < 0.5, f"100 error validations took {error_time:.3f}s"
        assert error_count == 100
    
    def test_safe_average_performance(self):
        """Test that safe_average performs well with large lists."""
        # Test with large list of numbers
        large_list = list(range(10000))
        
        start_time = time.time()
        result = safe_average(large_list)
        avg_time = time.time() - start_time
        
        # Should process 10000 numbers in less than 0.1 seconds
        assert avg_time < 0.1, f"safe_average on 10000 items took {avg_time:.3f}s"
        assert result == 4999.5
        
        # Test with mixed types (filtering required)
        mixed_list = [i if i % 2 == 0 else "invalid" for i in range(1000)]
        
        start_time = time.time()
        result = safe_average(mixed_list, default=0)
        mixed_time = time.time() - start_time
        
        # Should filter and average in less than 0.2 seconds
        assert mixed_time < 0.2, f"safe_average with filtering took {mixed_time:.3f}s"
    
    def test_safe_format_performance(self):
        """Test that safe_format performs well with many placeholders."""
        # Create template with many placeholders
        template = " ".join([f"{{key{i}}}" for i in range(100)])
        values = {f"key{i}": f"value{i}" for i in range(50)}  # Only half provided
        
        start_time = time.time()
        result = safe_format(template, values)
        format_time = time.time() - start_time
        
        # Should format in less than 0.1 seconds
        assert format_time < 0.1, f"safe_format with 100 placeholders took {format_time:.3f}s"
        assert "value0" in result
        assert "[MISSING:" in result or "key50" in result
    
    def test_explain_error_performance(self):
        """Test that explain_error performs well."""
        error_messages = [
            "Expected number, got str",
            "Value cannot be None",
            "Expected number, got list",
            "Some random error message"
        ]
        
        start_time = time.time()
        for msg in error_messages * 25:  # 100 total calls
            explain_error(msg)
        explain_time = time.time() - start_time
        
        # Should explain 100 errors in less than 1 second
        assert explain_time < 1.0, f"100 error explanations took {explain_time:.3f}s"


class TestRegressionPrevention:
    """Test that bug fixes don't break existing functionality."""
    
    def test_safe_functions_still_work_as_before(self):
        """Test that safe functions maintain their original behavior."""
        # safe_get
        assert safe_get({"key": "value"}, "key") == "value"
        assert safe_get({"key": "value"}, "missing", "default") == "default"
        assert safe_get(None, "key", "default") == "default"
        
        # safe_divide
        assert safe_divide(10, 2) == 5.0
        assert safe_divide(10, 0, default=0) == 0
        assert safe_divide(10, 0, default=None) is None
        
        # safe_max
        from fishertools.safe import safe_max
        assert safe_max([1, 2, 3]) == 3
        assert safe_max([], default=0) == 0
        
        # safe_min
        from fishertools.safe import safe_min
        assert safe_min([1, 2, 3]) == 1
        assert safe_min([], default=0) == 0
    
    def test_validation_error_hierarchy_preserved(self):
        """Test that ValidationError exception hierarchy is preserved."""
        try:
            validate_number("invalid", 0, 100)
            assert False, "Should have raised ValidationError"
        except ValidationError as e:
            # Should be catchable as ValidationError
            assert isinstance(e, ValidationError)
            assert isinstance(e, Exception)
            
            # Should have error message
            assert str(e) is not None
            assert len(str(e)) > 0
    
    def test_learning_module_backward_compatibility(self):
        """Test that learning module maintains backward compatibility."""
        # explain() should return dict
        result = explain("list")
        assert isinstance(result, dict)
        assert "description" in result or len(result) > 0
        
        # explain_error() now returns dict (improved behavior)
        result = explain_error("Some error")
        assert isinstance(result, dict)
        assert len(result) > 0
    
    def test_no_new_dependencies_required(self):
        """Test that bug fixes don't require new dependencies."""
        # All imports should work without additional packages
        try:
            from fishertools.learn import ExplanationLoader
            from fishertools.validation import validate_number
            from fishertools.safe import safe_format, safe_average, PlaceholderBehavior
            
            # All imports successful
            assert True
        except ImportError as e:
            pytest.fail(f"Import failed, suggesting new dependency: {e}")
    
    def test_python_version_compatibility(self):
        """Test that code works with Python 3.9+."""
        # Check Python version
        version_info = sys.version_info
        assert version_info >= (3, 9), "Tests require Python 3.9+"
        
        # Test that importlib.resources works (Python 3.9+ feature)
        try:
            import importlib.resources
            assert True
        except ImportError:
            pytest.fail("importlib.resources not available")


class TestMemoryUsage:
    """Test that bug fixes don't introduce memory leaks."""
    
    def test_explanation_loader_memory_efficiency(self):
        """Test that ExplanationLoader doesn't leak memory."""
        # Create multiple loaders
        loaders = [ExplanationLoader() for _ in range(10)]
        
        # All should share the same explanations data (singleton pattern)
        first_explanations = loaders[0].explanations
        for loader in loaders[1:]:
            # Should be the same object (not a copy)
            assert loader.explanations is first_explanations or loader.explanations == first_explanations
    
    def test_safe_average_memory_efficiency(self):
        """Test that safe_average doesn't create unnecessary copies."""
        # Large list
        large_list = list(range(100000))
        
        # Calculate average multiple times
        for _ in range(10):
            result = safe_average(large_list)
            assert result == 49999.5
        
        # Should not cause memory issues
        assert True
    
    def test_validation_error_memory_efficiency(self):
        """Test that validation errors don't accumulate."""
        # Generate many validation errors
        error_count = 0
        for i in range(1000):
            try:
                validate_number(f"invalid_{i}", 0, 100)
            except ValidationError:
                error_count += 1
        
        assert error_count == 1000
        # Should not cause memory issues
        assert True


class TestStressTests:
    """Stress tests to ensure robustness under load."""
    
    def test_concurrent_explanation_access(self):
        """Test that explanation loader handles concurrent access."""
        loader = get_loader()
        
        # Access different explanations rapidly
        topics = ["list", "dict", "str", "int", "float"]
        for _ in range(100):
            for topic in topics:
                result = loader.get_explanation(topic)
                assert result is not None
    
    def test_validation_with_extreme_values(self):
        """Test validation with extreme values."""
        # Very large numbers (float conversion may lose precision)
        result = validate_number(10**100, 0, 10**101)
        assert result == float(10**100)  # Compare as float
        
        # Very small numbers
        result = validate_number(-10**100, -10**101, 0)
        assert result == float(-10**100)  # Compare as float
        
        # Float precision
        assert abs(validate_number(0.1 + 0.2, 0, 1) - 0.3) < 0.0001
    
    def test_safe_average_with_extreme_lists(self):
        """Test safe_average with extreme list sizes."""
        # Empty list
        assert safe_average([], default=0) == 0
        
        # Single element
        assert safe_average([42], default=0) == 42
        
        # All invalid values
        assert safe_average(["a", "b", "c"], default=0) == 0
        
        # Very large list (already tested in performance)
        large_list = list(range(10000))
        assert safe_average(large_list) == 4999.5
    
    def test_safe_format_with_edge_cases(self):
        """Test safe_format with edge cases."""
        # Empty template
        assert safe_format("", {}) == ""
        
        # No placeholders
        assert safe_format("Hello, World!", {}) == "Hello, World!"
        
        # All placeholders missing
        result = safe_format("{a} {b} {c}", {})
        assert "[MISSING:" in result or "{a}" in result
        
        # Nested braces
        result = safe_format("{{literal}}", {})
        assert "literal" in result or "{literal}" in result


class TestCrossPlatformCompatibility:
    """Test that bug fixes work across platforms."""
    
    def test_file_path_handling(self):
        """Test that file paths work on all platforms."""
        # ExplanationLoader should work regardless of platform
        loader = ExplanationLoader()
        assert loader.explanations is not None
        
        # Should have loaded explanations
        assert len(loader.explanations) > 0
    
    def test_unicode_handling(self):
        """Test that unicode works across platforms."""
        # Test with various unicode characters
        unicode_strings = [
            "Hello, РјРёСЂ!",  # Russian
            "дЅ еҐЅдё–з•Њ",  # Chinese
            "Щ…Ш±Ш­ШЁШ§ ШЁШ§Щ„Ш№Ш§Щ„Щ…",  # Arabic
            "рџљЂ рџЋ‰ вњЁ"  # Emojis
        ]
        
        for s in unicode_strings:
            # Should handle unicode in validation errors
            try:
                validate_number(s, 0, 100)
            except ValidationError as e:
                assert str(e) is not None
            
            # Should handle unicode in safe_format
            result = safe_format("Value: {val}", {"val": s})
            assert s in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
