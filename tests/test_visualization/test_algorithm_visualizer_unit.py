"""
Unit tests for algorithm visualizer.

Feature: fishertools-enhancements
These tests validate specific behaviors and edge cases of algorithm visualization.
"""

import pytest

from fishertools.visualization.algorithm_visualizer import AlgorithmVisualizer
from fishertools.visualization.models import (
    AlgorithmVisualization,
    SortingStep,
    SearchStep,
)


class TestUnsupportedAlgorithmHandling:
    """
    Test error handling when unsupported algorithm names are provided.
    
    Validates: Requirements 4.6
    """
    
    def test_visualize_sorting_with_unsupported_algorithm_raises_error(self):
        """Test that unsupported sorting algorithm raises ValueError."""
        visualizer = AlgorithmVisualizer()
        
        with pytest.raises(ValueError) as exc_info:
            visualizer.visualize_sorting([3, 1, 2], algorithm='heap_sort')
        
        assert 'Unsupported algorithm' in str(exc_info.value)
        assert 'heap_sort' in str(exc_info.value)
    
    def test_visualize_search_with_unsupported_algorithm_raises_error(self):
        """Test that unsupported search algorithm raises ValueError."""
        visualizer = AlgorithmVisualizer()
        
        with pytest.raises(ValueError) as exc_info:
            visualizer.visualize_search([1, 2, 3], 2, algorithm='interpolation_search')
        
        assert 'Unsupported algorithm' in str(exc_info.value)
        assert 'interpolation_search' in str(exc_info.value)
    
    def test_error_message_includes_supported_algorithms(self):
        """Test that error message lists supported algorithms."""
        visualizer = AlgorithmVisualizer()
        
        with pytest.raises(ValueError) as exc_info:
            visualizer.visualize_sorting([1, 2, 3], algorithm='invalid')
        
        error_message = str(exc_info.value)
        assert 'bubble_sort' in error_message
        assert 'Supported algorithms' in error_message
    
    def test_supported_algorithms_are_accessible(self):
        """Test that supported algorithms can be queried."""
        visualizer = AlgorithmVisualizer()
        
        assert 'bubble_sort' in visualizer.supported_algorithms
        assert 'quick_sort' in visualizer.supported_algorithms
        assert 'binary_search' in visualizer.supported_algorithms
        assert len(visualizer.supported_algorithms) >= 3


class TestEdgeCases:
    """Test edge cases for algorithm visualization."""
    
    def test_sorting_empty_array(self):
        """Test sorting an empty array."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([])
        
        assert isinstance(result, AlgorithmVisualization)
        assert len(result.steps) >= 1  # At least initial state
        assert result.statistics['swaps'] == 0
        assert result.statistics['comparisons'] == 0
    
    def test_sorting_single_element(self):
        """Test sorting a single element array."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([42])
        
        assert isinstance(result, AlgorithmVisualization)
        assert result.steps[-1].array_state == [42]
        assert result.statistics['swaps'] == 0
    
    def test_sorting_two_elements_sorted(self):
        """Test sorting two already sorted elements."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([1, 2])
        
        assert result.steps[-1].array_state == [1, 2]
        assert result.statistics['swaps'] == 0
    
    def test_sorting_two_elements_unsorted(self):
        """Test sorting two unsorted elements."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([2, 1])
        
        assert result.steps[-1].array_state == [1, 2]
        assert result.statistics['swaps'] == 1
    
    def test_search_empty_array(self):
        """Test searching in an empty array."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_search([], 5)
        
        assert isinstance(result, AlgorithmVisualization)
        # Should handle gracefully
    
    def test_search_single_element_found(self):
        """Test searching for element in single-element array (found)."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_search([42], 42)
        
        assert result.steps[-1].found == True
    
    def test_search_single_element_not_found(self):
        """Test searching for element in single-element array (not found)."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_search([42], 99)
        
        assert result.steps[-1].found == False
    
    def test_sorting_with_duplicates(self):
        """Test sorting array with duplicate elements."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([3, 1, 2, 1, 3])
        
        assert result.steps[-1].array_state == [1, 1, 2, 3, 3]
    
    def test_search_with_duplicates(self):
        """Test searching in array with duplicates."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_search([1, 2, 2, 2, 3], 2)
        
        # Should find one of the 2s
        assert result.steps[-1].found == True
    
    def test_sorting_negative_numbers(self):
        """Test sorting array with negative numbers."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([-5, 3, -1, 0, 2])
        
        assert result.steps[-1].array_state == [-5, -1, 0, 2, 3]
    
    def test_search_negative_numbers(self):
        """Test searching for negative number."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_search([-5, -1, 0, 2, 3], -1)
        
        assert result.steps[-1].found == True


class TestVisualizationDetails:
    """Test specific visualization details."""
    
    def test_sorting_step_descriptions_are_meaningful(self):
        """Test that step descriptions provide useful information."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([3, 1, 2])
        
        for step in result.steps:
            assert isinstance(step.description, str)
            assert len(step.description) > 0
    
    def test_search_step_descriptions_are_meaningful(self):
        """Test that search step descriptions provide useful information."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_search([1, 2, 3, 4, 5], 3)
        
        for step in result.steps:
            assert isinstance(step.description, str)
            assert len(step.description) > 0
    
    def test_sorting_highlighted_indices_are_valid(self):
        """Test that highlighted indices are within array bounds."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([3, 1, 2])
        
        for step in result.steps:
            for idx in step.highlighted_indices:
                assert 0 <= idx < len(step.array_state)
    
    def test_search_highlighted_indices_are_valid(self):
        """Test that search highlighted indices are within array bounds."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_search([1, 2, 3, 4, 5], 3)
        
        for step in result.steps:
            for idx in step.highlighted_indices:
                assert 0 <= idx < len(step.array_state)
    
    def test_sorting_comparison_indices_are_valid(self):
        """Test that comparison indices are valid when present."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([3, 1, 2])
        
        for step in result.steps:
            if step.comparison_indices is not None:
                i, j = step.comparison_indices
                assert 0 <= i < len(step.array_state)
                assert 0 <= j < len(step.array_state)
    
    def test_algorithm_name_is_stored(self):
        """Test that algorithm name is stored in result."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([1, 2, 3])
        
        assert result.algorithm_name == 'bubble_sort'
    
    def test_input_data_is_preserved(self):
        """Test that original input data is stored."""
        visualizer = AlgorithmVisualizer()
        original = [3, 1, 2]
        result = visualizer.visualize_sorting(original)
        
        assert result.input_data == original



class TestMergeSortEdgeCases:
    """
    Unit tests for merge_sort edge cases.
    
    Feature: fishertools-v0.5.1
    Validates: Requirements 4.1, 4.2, 4.3
    """
    
    def test_merge_sort_empty_array(self):
        """Test merge sort with empty array."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([], 'merge_sort')
        
        assert isinstance(result, AlgorithmVisualization)
        assert result.final_array == []
        assert result.statistics['comparisons'] == 0
    
    def test_merge_sort_single_element(self):
        """Test merge sort with single element array."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([42], 'merge_sort')
        
        assert result.final_array == [42]
        assert result.statistics['comparisons'] == 0
    
    def test_merge_sort_already_sorted(self):
        """Test merge sort with already sorted array."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([1, 2, 3, 4, 5], 'merge_sort')
        
        assert result.final_array == [1, 2, 3, 4, 5]
        # Merge sort still does comparisons even if sorted
        assert result.statistics['comparisons'] > 0
    
    def test_merge_sort_reverse_sorted(self):
        """Test merge sort with reverse sorted array."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([5, 4, 3, 2, 1], 'merge_sort')
        
        assert result.final_array == [1, 2, 3, 4, 5]
        assert result.statistics['comparisons'] > 0
    
    def test_merge_sort_with_duplicates(self):
        """Test merge sort with duplicate elements."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([3, 1, 2, 1, 3, 2], 'merge_sort')
        
        assert result.final_array == [1, 1, 2, 2, 3, 3]
        # Verify all elements preserved
        assert sorted(result.final_array) == sorted([3, 1, 2, 1, 3, 2])
    
    def test_merge_sort_two_elements_sorted(self):
        """Test merge sort with two already sorted elements."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([1, 2], 'merge_sort')
        
        assert result.final_array == [1, 2]
    
    def test_merge_sort_two_elements_unsorted(self):
        """Test merge sort with two unsorted elements."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([2, 1], 'merge_sort')
        
        assert result.final_array == [1, 2]
    
    def test_merge_sort_negative_numbers(self):
        """Test merge sort with negative numbers."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([-5, 3, -1, 0, 2], 'merge_sort')
        
        assert result.final_array == [-5, -1, 0, 2, 3]
    
    def test_merge_sort_all_same_elements(self):
        """Test merge sort with all identical elements."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([5, 5, 5, 5], 'merge_sort')
        
        assert result.final_array == [5, 5, 5, 5]
    
    def test_merge_sort_statistics_accuracy(self):
        """Test that merge sort statistics are accurate."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([3, 1, 2], 'merge_sort')
        
        # Verify statistics exist
        assert 'comparisons' in result.statistics
        assert 'steps' in result.statistics
        assert result.statistics['steps'] == len(result.steps)
        
        # Merge sort should have no swaps (it uses merging, not swapping)
        assert result.statistics['swaps'] == 0

