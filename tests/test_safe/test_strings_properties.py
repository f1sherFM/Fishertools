"""
Property-based tests for safe string operations.

These tests validate Property 4: Safe Format Placeholder Handling
Feature: fishertools-bug-fixes
Requirements: 4.1, 4.2, 4.3
"""

import pytest
from hypothesis import given, strategies as st, assume
from fishertools.safe.strings import safe_format, PlaceholderBehavior
import re


class TestSafeFormatProperties:
    """Property-based tests for safe_format function."""
    
    @given(
        template=st.text(min_size=1, max_size=100),
        values=st.dictionaries(
            st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))),
            st.one_of(st.text(), st.integers(), st.floats(allow_nan=False, allow_infinity=False))
        ),
        behavior=st.sampled_from([PlaceholderBehavior.PRESERVE, PlaceholderBehavior.MISSING, PlaceholderBehavior.EMPTY])
    )
    def test_safe_format_never_raises_key_error(self, template, values, behavior):
        """
        **Property 4: Safe Format Placeholder Handling**
        **Feature: fishertools-bug-fixes, Property 4: Safe Format Placeholder Handling**
        **Validates: Requirements 4.1, 4.2, 4.3**
        
        For any template string with missing placeholders, safe_format() should handle them
        according to the configured behavior without raising KeyError.
        """
        try:
            result = safe_format(template, values, behavior=behavior)
            # Should always return a string
            assert isinstance(result, str)
            # Should never raise KeyError
            assert True
        except KeyError:
            pytest.fail("safe_format raised KeyError - should handle missing placeholders gracefully")
        except (ValueError, IndexError):
            # These are acceptable for malformed templates
            pass
    
    @given(
        placeholder_name=st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))),
        value=st.one_of(st.text(), st.integers(), st.floats(allow_nan=False, allow_infinity=False))
    )
    def test_safe_format_with_value_returns_formatted_string(self, placeholder_name, value):
        """
        **Property 4: Safe Format Placeholder Handling**
        **Feature: fishertools-bug-fixes, Property 4: Safe Format Placeholder Handling**
        **Validates: Requirements 4.1**
        
        When a placeholder has a corresponding value, safe_format() should successfully
        format the string with that value.
        """
        # Skip empty placeholder names or names with special characters
        assume(placeholder_name.strip() != "")
        assume(not any(c in placeholder_name for c in ['{', '}', ':', '!', '.']))
        # Skip numeric placeholder names (they're treated as positional)
        assume(not placeholder_name.isdigit())
        
        template = f"Hello, {{{placeholder_name}}}!"
        values = {placeholder_name: value}
        
        result = safe_format(template, values)
        # Should contain the string representation of the value
        assert str(value) in result
        # Should not contain the placeholder anymore
        assert f"{{{placeholder_name}}}" not in result
    
    @given(
        placeholder_name=st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')))
    )
    def test_safe_format_missing_behavior_adds_missing_marker(self, placeholder_name):
        """
        **Property 4: Safe Format Placeholder Handling**
        **Feature: fishertools-bug-fixes, Property 4: Safe Format Placeholder Handling**
        **Validates: Requirements 4.2**
        
        When using MISSING behavior with missing placeholders, safe_format() should
        replace them with "[MISSING: key_name]" format.
        """
        # Skip empty placeholder names or names with special characters
        assume(placeholder_name.strip() != "")
        assume(not any(c in placeholder_name for c in ['{', '}', ':', '!', '.']))
        # Skip numeric placeholder names (they're treated as positional)
        assume(not placeholder_name.isdigit())
        
        template = f"Hello, {{{placeholder_name}}}!"
        values = {}
        
        result = safe_format(template, values, behavior=PlaceholderBehavior.MISSING)
        # Should contain the MISSING marker
        assert "[MISSING:" in result
        assert placeholder_name in result
        # Should not contain the original placeholder
        assert f"{{{placeholder_name}}}" not in result
    
    @given(
        placeholder_name=st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')))
    )
    def test_safe_format_preserve_behavior_keeps_placeholder(self, placeholder_name):
        """
        **Property 4: Safe Format Placeholder Handling**
        **Feature: fishertools-bug-fixes, Property 4: Safe Format Placeholder Handling**
        **Validates: Requirements 4.3**
        
        When using PRESERVE behavior with missing placeholders, safe_format() should
        leave the original placeholders unchanged.
        """
        # Skip empty placeholder names or names with special characters
        assume(placeholder_name.strip() != "")
        assume(not any(c in placeholder_name for c in ['{', '}', ':', '!', '.']))
        # Skip numeric placeholder names (they're treated as positional)
        assume(not placeholder_name.isdigit())
        
        template = f"Hello, {{{placeholder_name}}}!"
        values = {}
        
        result = safe_format(template, values, behavior=PlaceholderBehavior.PRESERVE)
        # Should still contain the original placeholder
        assert f"{{{placeholder_name}}}" in result
        # Should not contain MISSING marker
        assert "[MISSING:" not in result
    
    @given(
        placeholder_name=st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')))
    )
    def test_safe_format_empty_behavior_removes_placeholder(self, placeholder_name):
        """
        **Property 4: Safe Format Placeholder Handling**
        **Feature: fishertools-bug-fixes, Property 4: Safe Format Placeholder Handling**
        **Validates: Requirements 4.3**
        
        When using EMPTY behavior with missing placeholders, safe_format() should
        replace them with empty strings.
        """
        # Skip empty placeholder names or names with special characters
        assume(placeholder_name.strip() != "")
        assume(not any(c in placeholder_name for c in ['{', '}', ':', '!', '.']))
        # Skip numeric placeholder names (they're treated as positional)
        assume(not placeholder_name.isdigit())
        
        template = f"Hello, {{{placeholder_name}}}!"
        values = {}
        
        result = safe_format(template, values, behavior=PlaceholderBehavior.EMPTY)
        # Should not contain the placeholder
        assert f"{{{placeholder_name}}}" not in result
        # Should not contain MISSING marker
        assert "[MISSING:" not in result
        # Should be shorter than original template (placeholder removed)
        assert len(result) < len(template)
    
    @given(
        text_before=st.text(min_size=0, max_size=50),
        text_after=st.text(min_size=0, max_size=50),
        placeholder_name=st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd'))),
        behavior=st.sampled_from([PlaceholderBehavior.PRESERVE, PlaceholderBehavior.MISSING, PlaceholderBehavior.EMPTY])
    )
    def test_safe_format_preserves_surrounding_text(self, text_before, text_after, placeholder_name, behavior):
        """
        **Property 4: Safe Format Placeholder Handling**
        **Feature: fishertools-bug-fixes, Property 4: Safe Format Placeholder Handling**
        **Validates: Requirements 4.1, 4.2, 4.3**
        
        For any template with text surrounding placeholders, safe_format() should
        preserve the surrounding text regardless of placeholder handling behavior.
        """
        # Skip empty placeholder names or names with special characters
        assume(placeholder_name.strip() != "")
        assume(not any(c in placeholder_name for c in ['{', '}', ':', '!', '.']))
        # Skip numeric placeholder names (they're treated as positional)
        assume(not placeholder_name.isdigit())
        
        template = f"{text_before}{{{placeholder_name}}}{text_after}"
        values = {}
        
        result = safe_format(template, values, behavior=behavior)
        # Should preserve text before and after placeholder
        assert text_before in result
        assert text_after in result
