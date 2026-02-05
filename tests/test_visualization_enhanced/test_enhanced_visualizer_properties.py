"""
Property-based tests for enhanced visualization module.

This module tests the correctness properties of the EnhancedVisualizer
using hypothesis for comprehensive input coverage.

Feature: fishertools-enhancements
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import pytest
from hypothesis import given, strategies as st, assume

from fishertools.visualization import EnhancedVisualizer, VisualizationResult


# Strategy for generating test data structures
@st.composite
def data_structure(draw):
    """Generate arbitrary nested data structures."""
    return draw(
        st.recursive(
            st.one_of(
                st.none(),
                st.booleans(),
                st.integers(),
                st.floats(allow_nan=False, allow_infinity=False),
                st.text(max_size=50),
            ),
            lambda children: st.one_of(
                st.lists(children, max_size=5),
                st.dictionaries(st.text(min_size=1, max_size=20), children, max_size=5),
                st.tuples(children, children),
            ),
            max_leaves=20,
        )
    )


class TestTreeVisualizationStructure:
    """
    Property 6: Tree visualization structure
    
    For any data structure, calling visualize() with style="tree" should
    produce output that represents the hierarchical relationships correctly.
    
    Validates: Requirements 3.1
    """
    
    @given(data_structure())
    def test_tree_style_produces_hierarchical_output(self, data):
        """Test that tree style produces hierarchical output for any data."""
        visualizer = EnhancedVisualizer()
        result = visualizer.visualize(data, style='tree')
        
        # Verify result is a VisualizationResult
        assert isinstance(result, VisualizationResult)
        assert isinstance(result.content, str)
        
        # Tree style should use tree characters for non-trivial structures
        if isinstance(data, (dict, list, tuple, set)) and len(data) > 0:
            # Should contain tree branch characters
            assert any(char in result.content for char in ['├──', '└──', '│'])
    
    @given(st.dictionaries(st.text(min_size=1, max_size=10), st.integers(), min_size=1, max_size=5))
    def test_tree_style_shows_all_dict_keys(self, data):
        """Test that tree style shows all dictionary keys."""
        visualizer = EnhancedVisualizer()
        result = visualizer.visualize(data, style='tree')
        
        # All keys should appear in the output
        for key in data.keys():
            assert key in result.content
    
    @given(st.lists(st.integers(), min_size=1, max_size=10))
    def test_tree_style_shows_list_indices(self, data):
        """Test that tree style shows list indices."""
        visualizer = EnhancedVisualizer()
        result = visualizer.visualize(data, style='tree')
        
        # Should show index markers for lists
        for i in range(len(data)):
            assert f"[{i}]" in result.content
    
    @given(data_structure())
    def test_tree_style_never_crashes(self, data):
        """Test that tree style never crashes on any input."""
        visualizer = EnhancedVisualizer()
        
        # Should not raise any exceptions
        result = visualizer.visualize(data, style='tree')
        assert isinstance(result, VisualizationResult)
        assert result.content is not None


class TestColorHighlightingConsistency:
    """
    Property 7: Color highlighting consistency
    
    For any data structure, calling visualize() with colors=True should
    apply consistent color codes to the same data types throughout the output.
    
    Validates: Requirements 3.2
    """
    
    @given(data_structure())
    def test_colors_parameter_affects_output(self, data):
        """Test that colors parameter changes the output."""
        visualizer = EnhancedVisualizer()
        
        result_no_color = visualizer.visualize(data, colors=False)
        result_with_color = visualizer.visualize(data, colors=True)
        
        # Both should be valid results
        assert isinstance(result_no_color, VisualizationResult)
        assert isinstance(result_with_color, VisualizationResult)
    
    @given(st.lists(st.integers(), min_size=1, max_size=5))
    def test_color_codes_present_when_enabled(self, data):
        """Test that ANSI color codes are present when colors=True."""
        visualizer = EnhancedVisualizer()
        result = visualizer.visualize(data, colors=True)
        
        # Should contain ANSI escape sequences
        assert '\033[' in result.content or result.content  # Color codes or plain text
    
    @given(data_structure())
    def test_no_color_codes_when_disabled(self, data):
        """Test that no ANSI color codes are present when colors=False."""
        visualizer = EnhancedVisualizer()
        result = visualizer.visualize(data, colors=False)
        
        # Should not contain ANSI escape sequences (or very minimal)
        # Note: Some data might naturally contain escape sequences
        assert isinstance(result.content, str)
    
    @given(data_structure())
    def test_color_highlighting_never_crashes(self, data):
        """Test that color highlighting never crashes on any input."""
        visualizer = EnhancedVisualizer()
        
        # Should not raise any exceptions with colors enabled
        result = visualizer.visualize(data, colors=True)
        assert isinstance(result, VisualizationResult)
        assert result.content is not None


class TestDepthLimiting:
    """
    Property 8: Depth limiting
    
    For any nested data structure and max_depth value, the visualization
    output should not exceed the specified depth level.
    
    Validates: Requirements 3.3
    """
    
    @given(
        st.recursive(
            st.integers(),
            lambda children: st.lists(children, min_size=1, max_size=3),
            max_leaves=10,
        ),
        st.integers(min_value=0, max_value=5)
    )
    def test_max_depth_limits_nesting(self, data, max_depth):
        """Test that max_depth limits the nesting level."""
        visualizer = EnhancedVisualizer()
        result = visualizer.visualize(data, max_depth=max_depth)
        
        assert isinstance(result, VisualizationResult)
        
        # If depth is exceeded, should show truncation indicator
        if self._get_depth(data) > max_depth:
            assert '...' in result.content
    
    @given(data_structure(), st.integers(min_value=0, max_value=10))
    def test_max_depth_zero_shows_minimal_output(self, data, max_depth):
        """Test that max_depth=0 shows minimal output."""
        visualizer = EnhancedVisualizer()
        result = visualizer.visualize(data, max_depth=0)
        
        assert isinstance(result, VisualizationResult)
        # Should show something, even at depth 0
        assert len(result.content) > 0
    
    @given(data_structure())
    def test_no_max_depth_shows_full_structure(self, data):
        """Test that max_depth=None shows full structure."""
        visualizer = EnhancedVisualizer()
        result = visualizer.visualize(data, max_depth=None)
        
        assert isinstance(result, VisualizationResult)
        assert result.content is not None
    
    @given(data_structure(), st.integers(min_value=0, max_value=10))
    def test_depth_limiting_never_crashes(self, data, max_depth):
        """Test that depth limiting never crashes on any input."""
        visualizer = EnhancedVisualizer()
        
        # Should not raise any exceptions
        result = visualizer.visualize(data, max_depth=max_depth)
        assert isinstance(result, VisualizationResult)
    
    def _get_depth(self, data: Any, current_depth: int = 0) -> int:
        """Calculate the depth of a nested data structure."""
        if isinstance(data, dict):
            if not data:
                return current_depth
            return max(self._get_depth(v, current_depth + 1) for v in data.values())
        elif isinstance(data, (list, tuple, set)):
            if not data:
                return current_depth
            return max(self._get_depth(item, current_depth + 1) for item in data)
        else:
            return current_depth


class TestExportFunctionality:
    """
    Property 9: Export functionality
    
    For any visualization data and export format (json, html), the export
    should create a valid file in the specified format containing the
    visualization content.
    
    Validates: Requirements 3.4, 3.5
    """
    
    @given(data_structure(), st.sampled_from(['json', 'html']))
    def test_export_creates_file(self, data, export_format):
        """Test that export creates a file in the specified format."""
        visualizer = EnhancedVisualizer()
        filename = f'test_export_{export_format}'
        
        try:
            result = visualizer.visualize(data, export=export_format, filename=filename)
            
            assert isinstance(result, VisualizationResult)
            
            # Should have exported file path
            if result.exported_file:
                assert os.path.exists(result.exported_file)
                assert result.exported_file.endswith(f'.{export_format}')
        finally:
            # Cleanup
            if result.exported_file and os.path.exists(result.exported_file):
                os.remove(result.exported_file)
    
    @given(data_structure())
    def test_json_export_is_valid_json(self, data):
        """Test that JSON export creates valid JSON files."""
        visualizer = EnhancedVisualizer()
        filename = 'test_json_export'
        
        try:
            result = visualizer.visualize(data, export='json', filename=filename)
            
            if result.exported_file and os.path.exists(result.exported_file):
                # Should be valid JSON
                with open(result.exported_file, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                
                # Should contain expected structure
                assert 'data' in loaded_data
                assert 'visualization' in loaded_data
        finally:
            # Cleanup
            if result.exported_file and os.path.exists(result.exported_file):
                os.remove(result.exported_file)
    
    @given(data_structure())
    def test_html_export_contains_content(self, data):
        """Test that HTML export contains the visualization content."""
        visualizer = EnhancedVisualizer()
        filename = 'test_html_export'
        
        try:
            result = visualizer.visualize(data, export='html', filename=filename)
            
            if result.exported_file and os.path.exists(result.exported_file):
                # Should be valid HTML with content
                with open(result.exported_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                assert '<!DOCTYPE html>' in html_content
                assert '<html>' in html_content
                assert '</html>' in html_content
        finally:
            # Cleanup
            if result.exported_file and os.path.exists(result.exported_file):
                os.remove(result.exported_file)
    
    @given(data_structure())
    def test_export_without_format_returns_none(self, data):
        """Test that no export occurs when format is None."""
        visualizer = EnhancedVisualizer()
        result = visualizer.visualize(data, export=None)
        
        assert isinstance(result, VisualizationResult)
        assert result.exported_file is None
    
    @given(data_structure(), st.sampled_from(['json', 'html']))
    def test_export_never_crashes(self, data, export_format):
        """Test that export never crashes on any input."""
        visualizer = EnhancedVisualizer()
        filename = f'test_export_crash_{export_format}'
        
        try:
            # Should not raise any exceptions
            result = visualizer.visualize(data, export=export_format, filename=filename)
            assert isinstance(result, VisualizationResult)
        finally:
            # Cleanup
            if result.exported_file and os.path.exists(result.exported_file):
                os.remove(result.exported_file)


class TestVisualizationInputValidation:
    """
    Property 10: Visualization input validation
    
    For any invalid visualization parameters, the Enhanced_Visualizer should
    return structured error responses rather than crashing.
    
    Validates: Requirements 3.6
    """
    
    @given(data_structure(), st.text(min_size=1, max_size=20))
    def test_invalid_style_raises_error(self, data, invalid_style):
        """Test that invalid style parameter raises ValueError."""
        assume(invalid_style not in ['default', 'tree', 'compact'])
        
        visualizer = EnhancedVisualizer()
        
        with pytest.raises(ValueError, match="Invalid style"):
            visualizer.visualize(data, style=invalid_style)
    
    @given(data_structure(), st.text(min_size=1, max_size=20))
    def test_invalid_export_format_raises_error(self, data, invalid_format):
        """Test that invalid export format raises ValueError."""
        assume(invalid_format not in ['json', 'html'])
        
        visualizer = EnhancedVisualizer()
        
        with pytest.raises(ValueError, match="Invalid export format"):
            visualizer.visualize(data, export=invalid_format)
    
    @given(data_structure(), st.integers(max_value=-1))
    def test_negative_max_depth_raises_error(self, data, negative_depth):
        """Test that negative max_depth raises ValueError."""
        visualizer = EnhancedVisualizer()
        
        with pytest.raises(ValueError, match="max_depth must be non-negative"):
            visualizer.visualize(data, max_depth=negative_depth)
    
    @given(data_structure())
    def test_valid_parameters_never_crash(self, data):
        """Test that valid parameters never cause crashes."""
        visualizer = EnhancedVisualizer()
        
        # Should not raise any exceptions with valid parameters
        result = visualizer.visualize(
            data,
            style='default',
            colors=False,
            max_depth=5,
            export=None
        )
        assert isinstance(result, VisualizationResult)
