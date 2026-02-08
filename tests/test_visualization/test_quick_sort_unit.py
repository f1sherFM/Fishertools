"""
Unit tests for quick_sort algorithm edge cases.

Feature: fishertools-v0.5.0
These tests validate specific behaviors and edge cases of the quick_sort algorithm.
"""

import pytest

from fishertools.visualization.algorithm_visualizer import AlgorithmVisualizer
from fishertools.visualization.models import AlgorithmVisualization, SortingStep


class TestQuickSortEdgeCases:
    """Test edge cases for quick_sort algorithm."""
    
    def test_empty_array(self):
        """Test quick_sort with empty array returns empty result."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([], 'quick_sort')
        
        assert isinstance(result, AlgorithmVisualization)
        assert result.final_array == []
        # Empty array should have no steps, so statistics might be empty or zero
        assert result.statistics.get('comparisons', 0) == 0
        assert result.statistics.get('swaps', 0) == 0
    
    def test_single_element_array(self):
        """Test quick_sort with single element array."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([42], 'quick_sort')
        
        assert isinstance(result, AlgorithmVisualization)
        assert result.final_array == [42]
        # Single element requires no comparisons or swaps
        assert result.statistics['comparisons'] == 0
        assert result.statistics['swaps'] == 0
    
    def test_already_sorted_array(self):
        """Test quick_sort with already sorted array."""
        visualizer = AlgorithmVisualizer()
        sorted_array = [1, 2, 3, 4, 5]
        result = visualizer.visualize_sorting(sorted_array, 'quick_sort')
        
        assert result.final_array == [1, 2, 3, 4, 5]
        # Should still perform comparisons but minimal swaps
        assert result.statistics['comparisons'] > 0
        # Already sorted should have some swaps due to pivot placement
        assert result.statistics['swaps'] >= 0
    
    def test_reverse_sorted_array(self):
        """Test quick_sort with reverse sorted array."""
        visualizer = AlgorithmVisualizer()
        reverse_array = [5, 4, 3, 2, 1]
        result = visualizer.visualize_sorting(reverse_array, 'quick_sort')
        
        assert result.final_array == [1, 2, 3, 4, 5]
        # Reverse sorted requires many comparisons and swaps
        assert result.statistics['comparisons'] > 0
        assert result.statistics['swaps'] > 0
    
    def test_array_with_duplicates(self):
        """Test quick_sort with array containing duplicate elements."""
        visualizer = AlgorithmVisualizer()
        array_with_dupes = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        result = visualizer.visualize_sorting(array_with_dupes, 'quick_sort')
        
        assert result.final_array == [1, 1, 2, 3, 3, 4, 5, 5, 6, 9]
        # Should preserve all duplicates
        assert result.final_array.count(1) == 2
        assert result.final_array.count(3) == 2
        assert result.final_array.count(5) == 2
    
    def test_two_elements_sorted(self):
        """Test quick_sort with two already sorted elements."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([1, 2], 'quick_sort')
        
        assert result.final_array == [1, 2]
    
    def test_two_elements_unsorted(self):
        """Test quick_sort with two unsorted elements."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([2, 1], 'quick_sort')
        
        assert result.final_array == [1, 2]
        assert result.statistics['swaps'] > 0
    
    def test_all_same_elements(self):
        """Test quick_sort with all identical elements."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([5, 5, 5, 5, 5], 'quick_sort')
        
        assert result.final_array == [5, 5, 5, 5, 5]
        # All same elements should require minimal swaps
        assert result.statistics['comparisons'] > 0
    
    def test_negative_numbers(self):
        """Test quick_sort with negative numbers."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([-5, 3, -1, 0, 2, -3], 'quick_sort')
        
        assert result.final_array == [-5, -3, -1, 0, 2, 3]
    
    def test_mixed_positive_negative_zero(self):
        """Test quick_sort with mix of positive, negative, and zero."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([0, -1, 1, -2, 2, 0], 'quick_sort')
        
        assert result.final_array == [-2, -1, 0, 0, 1, 2]


class TestQuickSortVisualizationDetails:
    """Test specific visualization details for quick_sort."""
    
    def test_step_descriptions_are_meaningful(self):
        """Test that step descriptions provide useful information."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([3, 1, 2], 'quick_sort')
        
        for step in result.steps:
            assert isinstance(step.description, str)
            assert len(step.description) > 0
    
    def test_highlighted_indices_are_valid(self):
        """Test that highlighted indices are within array bounds."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([3, 1, 2, 4, 5], 'quick_sort')
        
        for step in result.steps:
            for idx in step.highlighted_indices:
                assert 0 <= idx < len(step.array_state), \
                    f"Invalid highlighted index {idx} for array of length {len(step.array_state)}"
    
    def test_partition_index_is_valid_when_present(self):
        """Test that partition_index is valid when set."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([3, 1, 2, 4, 5], 'quick_sort')
        
        for step in result.steps:
            if step.partition_index is not None:
                assert 0 <= step.partition_index < len(step.array_state), \
                    f"Invalid partition index {step.partition_index}"
    
    def test_algorithm_name_is_stored(self):
        """Test that algorithm name is stored in result."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([1, 2, 3], 'quick_sort')
        
        assert result.algorithm_name == 'quick_sort'
    
    def test_input_data_is_preserved(self):
        """Test that original input data is stored."""
        visualizer = AlgorithmVisualizer()
        original = [3, 1, 2]
        result = visualizer.visualize_sorting(original, 'quick_sort')
        
        assert result.input_data == original
    
    def test_steps_are_sorting_step_instances(self):
        """Test that all steps are SortingStep instances."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([3, 1, 2], 'quick_sort')
        
        for step in result.steps:
            assert isinstance(step, SortingStep)
    
    def test_comparison_indices_valid_when_present(self):
        """Test that comparison indices are valid when present."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([3, 1, 2, 4], 'quick_sort')
        
        for step in result.steps:
            if step.comparison_indices is not None:
                i, j = step.comparison_indices
                assert 0 <= i < len(step.array_state)
                assert 0 <= j < len(step.array_state)


class TestQuickSortStatistics:
    """Test statistics tracking for quick_sort."""
    
    def test_statistics_are_non_negative(self):
        """Test that all statistics are non-negative."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([3, 1, 2], 'quick_sort')
        
        assert result.statistics['comparisons'] >= 0
        assert result.statistics['swaps'] >= 0
        assert result.statistics['steps'] >= 0
    
    def test_statistics_steps_count_matches(self):
        """Test that steps count in statistics matches actual step count."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([3, 1, 2], 'quick_sort')
        
        assert result.statistics['steps'] == len(result.steps)
    
    def test_final_step_matches_statistics(self):
        """Test that final step counts match statistics."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([3, 1, 2], 'quick_sort')
        
        if result.steps:
            final_step = result.steps[-1]
            assert result.statistics['comparisons'] == final_step.comparisons_count
            assert result.statistics['swaps'] == final_step.swaps_count
