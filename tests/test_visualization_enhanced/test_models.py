"""
Tests for enhanced visualization module data models.

This module tests the core data structures used for enhanced visualization.
"""

from __future__ import annotations

import pytest

from fishertools.visualization.models import (
    VisualizationConfig,
    VisualizationResult,
    AlgorithmStep,
    SortingStep,
    SearchStep,
    AlgorithmVisualization,
)


class TestVisualizationConfig:
    """Tests for VisualizationConfig data model."""
    
    def test_default_config(self):
        """Test default VisualizationConfig."""
        config = VisualizationConfig()
        assert config.style == 'default'
        assert config.colors is False
        assert config.max_depth is None
        assert config.export_format is None
        assert config.color_scheme == 'default'
    
    def test_custom_config(self):
        """Test custom VisualizationConfig."""
        config = VisualizationConfig(
            style='tree',
            colors=True,
            max_depth=5,
            export_format='json',
            color_scheme='dark'
        )
        assert config.style == 'tree'
        assert config.colors is True
        assert config.max_depth == 5
        assert config.export_format == 'json'
        assert config.color_scheme == 'dark'


class TestVisualizationResult:
    """Tests for VisualizationResult data model."""
    
    def test_result_without_export(self):
        """Test VisualizationResult without export."""
        result = VisualizationResult(content="Test content")
        assert result.content == "Test content"
        assert result.exported_file is None
        assert str(result) == "Test content"
    
    def test_result_with_export(self):
        """Test VisualizationResult with export."""
        result = VisualizationResult(
            content="Test content",
            exported_file="/tmp/output.json"
        )
        assert result.content == "Test content"
        assert result.exported_file == "/tmp/output.json"


class TestAlgorithmStep:
    """Tests for AlgorithmStep data model."""
    
    def test_basic_step(self):
        """Test basic AlgorithmStep."""
        step = AlgorithmStep(
            step_number=1,
            description="Compare elements",
            array_state=[3, 1, 2]
        )
        assert step.step_number == 1
        assert step.description == "Compare elements"
        assert step.array_state == [3, 1, 2]
        assert step.highlighted_indices == []
        assert step.comparison_indices is None
        assert step.swap_occurred is False


class TestSortingStep:
    """Tests for SortingStep data model."""
    
    def test_sorting_step(self):
        """Test SortingStep with counters."""
        step = SortingStep(
            step_number=1,
            description="Swap elements",
            array_state=[1, 3, 2],
            comparisons_count=5,
            swaps_count=2,
            swap_occurred=True
        )
        assert step.step_number == 1
        assert step.comparisons_count == 5
        assert step.swaps_count == 2
        assert step.swap_occurred is True


class TestSearchStep:
    """Tests for SearchStep data model."""
    
    def test_search_step(self):
        """Test SearchStep with search range."""
        step = SearchStep(
            step_number=1,
            description="Check middle element",
            array_state=[1, 2, 3, 4, 5],
            search_range=(0, 4),
            middle_index=2
        )
        assert step.step_number == 1
        assert step.search_range == (0, 4)
        assert step.middle_index == 2
        assert step.found is None


class TestAlgorithmVisualization:
    """Tests for AlgorithmVisualization data model."""
    
    def test_empty_visualization(self):
        """Test empty AlgorithmVisualization."""
        viz = AlgorithmVisualization(steps=[])
        assert len(viz) == 0
        assert viz.steps == []
        assert viz.statistics == {}
    
    def test_visualization_with_steps(self):
        """Test AlgorithmVisualization with steps."""
        steps = [
            AlgorithmStep(
                step_number=i,
                description=f"Step {i}",
                array_state=[1, 2, 3]
            )
            for i in range(3)
        ]
        viz = AlgorithmVisualization(
            steps=steps,
            statistics={"comparisons": 10, "swaps": 5},
            algorithm_name="bubble_sort",
            input_data=[3, 2, 1]
        )
        assert len(viz) == 3
        assert viz.statistics["comparisons"] == 10
        assert viz.algorithm_name == "bubble_sort"
        assert viz.input_data == [3, 2, 1]
