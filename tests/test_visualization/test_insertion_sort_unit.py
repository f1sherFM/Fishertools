"""
Unit tests for insertion_sort algorithm edge cases.

Feature: fishertools-v0.4.0
These tests validate specific behaviors and edge cases of the insertion_sort algorithm.
"""

import pytest

from fishertools.visualization import AlgorithmVisualizer


class TestInsertionSortEdgeCases:
    """Test edge cases for insertion_sort algorithm."""
    
    def test_empty_array(self):
        """Test insertion_sort with empty array returns empty result."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([], 'insertion_sort')
        
        assert result.final_array == []
        assert len(result.steps) >= 1  # At least one step for empty array
        assert result.statistics['comparisons'] == 0
        assert result.statistics['swaps'] == 0
    
    def test_single_element_array(self):
        """Test insertion_sort with single element array."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([42], 'insertion_sort')
        
        assert result.final_array == [42]
        assert result.statistics['comparisons'] == 0
        assert result.statistics['swaps'] == 0
    
    def test_already_sorted_array(self):
        """Test insertion_sort with already sorted array."""
        visualizer = AlgorithmVisualizer()
        sorted_array = [1, 2, 3, 4, 5]
        result = visualizer.visualize_sorting(sorted_array.copy(), 'insertion_sort')
        
        assert result.final_array == sorted_array
        # For already sorted array, insertion sort should have minimal comparisons
        # and no swaps (best case O(n))
        assert result.statistics['comparisons'] >= 0
        assert result.statistics['swaps'] == 0  # No shifts needed for sorted array
    
    def test_reverse_sorted_array(self):
        """Test insertion_sort with reverse sorted array."""
        visualizer = AlgorithmVisualizer()
        reverse_array = [5, 4, 3, 2, 1]
        result = visualizer.visualize_sorting(reverse_array.copy(), 'insertion_sort')
        
        assert result.final_array == [1, 2, 3, 4, 5]
        # Reverse sorted is worst case for insertion sort
        assert result.statistics['comparisons'] > 0
        assert result.statistics['swaps'] > 0
    
    def test_array_with_duplicates(self):
        """Test insertion_sort with array containing duplicate elements."""
        visualizer = AlgorithmVisualizer()
        array_with_dupes = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        result = visualizer.visualize_sorting(array_with_dupes.copy(), 'insertion_sort')
        
        assert result.final_array == sorted(array_with_dupes)
        # Verify duplicates are preserved
        from collections import Counter
        assert Counter(result.final_array) == Counter(array_with_dupes)
    
    def test_two_elements_sorted(self):
        """Test insertion_sort with two already sorted elements."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([1, 2], 'insertion_sort')
        
        assert result.final_array == [1, 2]
    
    def test_two_elements_unsorted(self):
        """Test insertion_sort with two unsorted elements."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([2, 1], 'insertion_sort')
        
        assert result.final_array == [1, 2]
        assert result.statistics['swaps'] > 0
    
    def test_all_same_elements(self):
        """Test insertion_sort with all identical elements."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([5, 5, 5, 5, 5], 'insertion_sort')
        
        assert result.final_array == [5, 5, 5, 5, 5]
        assert result.statistics['swaps'] == 0  # No shifts needed
    
    def test_negative_numbers(self):
        """Test insertion_sort with negative numbers."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([-5, 3, -1, 0, 2, -3], 'insertion_sort')
        
        assert result.final_array == [-5, -3, -1, 0, 2, 3]
    
    def test_mixed_positive_negative_zero(self):
        """Test insertion_sort with mix of positive, negative, and zero."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([0, -1, 1, -2, 2, 0], 'insertion_sort')
        
        assert result.final_array == [-2, -1, 0, 0, 1, 2]


class TestInsertionSortVisualizationDetails:
    """Test specific visualization details for insertion_sort."""
    
    def test_step_descriptions_are_meaningful(self):
        """Test that step descriptions provide meaningful information."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([3, 1, 2], 'insertion_sort')
        
        # All steps should have non-empty descriptions
        for step in result.steps:
            assert step.description
            assert len(step.description) > 0
    
    def test_highlighted_indices_are_valid(self):
        """Test that highlighted indices are within array bounds."""
        visualizer = AlgorithmVisualizer()
        array = [5, 2, 8, 1, 9]
        result = visualizer.visualize_sorting(array.copy(), 'insertion_sort')
        
        for step in result.steps:
            for idx in step.highlighted_indices:
                assert 0 <= idx < len(array)
    
    def test_array_state_length_consistent(self):
        """Test that array state length remains consistent throughout."""
        visualizer = AlgorithmVisualizer()
        array = [4, 2, 7, 1, 3]
        result = visualizer.visualize_sorting(array.copy(), 'insertion_sort')
        
        for step in result.steps:
            assert len(step.array_state) == len(array)
    
    def test_sorted_portion_grows(self):
        """Test that the sorted portion grows as algorithm progresses."""
        visualizer = AlgorithmVisualizer()
        array = [5, 2, 8, 1, 9, 3]
        result = visualizer.visualize_sorting(array.copy(), 'insertion_sort')
        
        # The sorted portion should grow from left to right
        # We can verify this by checking that highlighted indices
        # generally include more elements as we progress
        # (though this is a heuristic check)
        if len(result.steps) > 2:
            # At least some steps should show the growing sorted portion
            steps_with_highlights = [s for s in result.steps if s.highlighted_indices]
            assert len(steps_with_highlights) > 0
    
    def test_comparison_indices_when_present(self):
        """Test that comparison indices are valid when present."""
        visualizer = AlgorithmVisualizer()
        array = [3, 1, 4, 1, 5]
        result = visualizer.visualize_sorting(array.copy(), 'insertion_sort')
        
        for step in result.steps:
            if step.comparison_indices:
                i, j = step.comparison_indices
                assert 0 <= i < len(array)
                assert 0 <= j < len(array)


class TestInsertionSortStatistics:
    """Test statistics tracking for insertion_sort."""
    
    def test_statistics_are_non_negative(self):
        """Test that all statistics are non-negative."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([3, 1, 4, 1, 5], 'insertion_sort')
        
        assert result.statistics['comparisons'] >= 0
        assert result.statistics['swaps'] >= 0
    
    def test_statistics_match_final_step(self):
        """Test that statistics match the final step counts."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([2, 4, 1, 3], 'insertion_sort')
        
        if result.steps:
            last_step = result.steps[-1]
            assert result.statistics['comparisons'] == last_step.comparisons_count
            assert result.statistics['swaps'] == last_step.swaps_count
    
    def test_best_case_performance(self):
        """Test insertion sort best case (already sorted) has O(n) comparisons."""
        visualizer = AlgorithmVisualizer()
        sorted_array = list(range(10))
        result = visualizer.visualize_sorting(sorted_array.copy(), 'insertion_sort')
        
        # Best case: n-1 comparisons, 0 swaps
        assert result.statistics['comparisons'] == len(sorted_array) - 1
        assert result.statistics['swaps'] == 0
    
    def test_worst_case_has_more_operations(self):
        """Test that worst case (reverse sorted) has more operations than best case."""
        visualizer = AlgorithmVisualizer()
        
        # Best case: sorted array
        sorted_array = [1, 2, 3, 4, 5]
        best_result = visualizer.visualize_sorting(sorted_array.copy(), 'insertion_sort')
        
        # Worst case: reverse sorted array
        reverse_array = [5, 4, 3, 2, 1]
        worst_result = visualizer.visualize_sorting(reverse_array.copy(), 'insertion_sort')
        
        # Worst case should have more comparisons and swaps
        assert worst_result.statistics['comparisons'] > best_result.statistics['comparisons']
        assert worst_result.statistics['swaps'] > best_result.statistics['swaps']


