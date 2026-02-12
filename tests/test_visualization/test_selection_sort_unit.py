"""
Unit tests for selection_sort algorithm edge cases.

Feature: fishertools-v0.5.2
These tests validate specific behaviors and edge cases of the selection_sort algorithm.
"""

import pytest

from fishertools.visualization import AlgorithmVisualizer


class TestSelectionSortEdgeCases:
    """Test edge cases for selection_sort algorithm."""
    
    def test_empty_array(self):
        """Test selection_sort with empty array returns empty result."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([], 'selection_sort')
        
        assert result.final_array == []
        assert len(result.steps) >= 1  # At least one step for empty array
        assert result.statistics['comparisons'] == 0
        assert result.statistics['swaps'] == 0
    
    def test_single_element_array(self):
        """Test selection_sort with single element array."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([42], 'selection_sort')
        
        assert result.final_array == [42]
        # Single element is already sorted, no comparisons needed
        assert result.statistics['comparisons'] == 0
        assert result.statistics['swaps'] == 0
    
    def test_already_sorted_array(self):
        """Test selection_sort with already sorted array."""
        visualizer = AlgorithmVisualizer()
        sorted_array = [1, 2, 3, 4, 5]
        result = visualizer.visualize_sorting(sorted_array.copy(), 'selection_sort')
        
        assert result.final_array == sorted_array
        # Selection sort always does n(n-1)/2 comparisons regardless of input
        assert result.statistics['comparisons'] > 0
        # For already sorted array, minimum is always in correct position
        assert result.statistics['swaps'] == 0
    
    def test_reverse_sorted_array(self):
        """Test selection_sort with reverse sorted array."""
        visualizer = AlgorithmVisualizer()
        reverse_array = [5, 4, 3, 2, 1]
        result = visualizer.visualize_sorting(reverse_array.copy(), 'selection_sort')
        
        assert result.final_array == [1, 2, 3, 4, 5]
        # Selection sort always does same number of comparisons
        assert result.statistics['comparisons'] > 0
        # Reverse sorted requires swaps
        assert result.statistics['swaps'] > 0
    
    def test_array_with_duplicates(self):
        """Test selection_sort with array containing duplicate elements."""
        visualizer = AlgorithmVisualizer()
        array_with_dupes = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        result = visualizer.visualize_sorting(array_with_dupes.copy(), 'selection_sort')
        
        assert result.final_array == sorted(array_with_dupes)
        # Verify duplicates are preserved
        from collections import Counter
        assert Counter(result.final_array) == Counter(array_with_dupes)
    
    def test_two_elements_sorted(self):
        """Test selection_sort with two already sorted elements."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([1, 2], 'selection_sort')
        
        assert result.final_array == [1, 2]
        assert result.statistics['comparisons'] == 1
        assert result.statistics['swaps'] == 0
    
    def test_two_elements_unsorted(self):
        """Test selection_sort with two unsorted elements."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([2, 1], 'selection_sort')
        
        assert result.final_array == [1, 2]
        assert result.statistics['comparisons'] == 1
        assert result.statistics['swaps'] == 1
    
    def test_all_same_elements(self):
        """Test selection_sort with all identical elements."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([5, 5, 5, 5, 5], 'selection_sort')
        
        assert result.final_array == [5, 5, 5, 5, 5]
        # Comparisons still happen
        assert result.statistics['comparisons'] > 0
        # No swaps needed since all elements are equal
        assert result.statistics['swaps'] == 0
    
    def test_negative_numbers(self):
        """Test selection_sort with negative numbers."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([-5, 3, -1, 0, 2, -3], 'selection_sort')
        
        assert result.final_array == [-5, -3, -1, 0, 2, 3]
    
    def test_mixed_positive_negative_zero(self):
        """Test selection_sort with mix of positive, negative, and zero."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([0, -1, 1, -2, 2, 0], 'selection_sort')
        
        assert result.final_array == [-2, -1, 0, 0, 1, 2]


class TestSelectionSortVisualizationDetails:
    """Test specific visualization details for selection_sort."""
    
    def test_step_descriptions_are_meaningful(self):
        """Test that step descriptions provide meaningful information."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([3, 1, 2], 'selection_sort')
        
        # All steps should have non-empty descriptions
        for step in result.steps:
            assert step.description
            assert len(step.description) > 0
    
    def test_highlighted_indices_are_valid(self):
        """Test that highlighted indices are within array bounds."""
        visualizer = AlgorithmVisualizer()
        array = [5, 2, 8, 1, 9]
        result = visualizer.visualize_sorting(array.copy(), 'selection_sort')
        
        for step in result.steps:
            for idx in step.highlighted_indices:
                assert 0 <= idx < len(array)
    
    def test_array_state_length_consistent(self):
        """Test that array state length remains consistent throughout."""
        visualizer = AlgorithmVisualizer()
        array = [4, 2, 7, 1, 3]
        result = visualizer.visualize_sorting(array.copy(), 'selection_sort')
        
        for step in result.steps:
            assert len(step.array_state) == len(array)
    
    def test_minimum_search_visualization(self):
        """Test that minimum search is visualized properly."""
        visualizer = AlgorithmVisualizer()
        array = [5, 2, 8, 1, 9, 3]
        result = visualizer.visualize_sorting(array.copy(), 'selection_sort')
        
        # Should have steps showing minimum search
        search_steps = [s for s in result.steps if 'minimum' in s.description.lower() or 'search' in s.description.lower()]
        assert len(search_steps) > 0, "Should have steps showing minimum search"
    
    def test_comparison_indices_when_present(self):
        """Test that comparison indices are valid when present."""
        visualizer = AlgorithmVisualizer()
        array = [3, 1, 4, 1, 5]
        result = visualizer.visualize_sorting(array.copy(), 'selection_sort')
        
        for step in result.steps:
            if step.comparison_indices:
                i, j = step.comparison_indices
                assert 0 <= i < len(array)
                assert 0 <= j < len(array)
    
    def test_swap_positions_highlighted(self):
        """Test that swap positions are highlighted."""
        visualizer = AlgorithmVisualizer()
        array = [3, 1, 2]
        result = visualizer.visualize_sorting(array.copy(), 'selection_sort')
        
        # Find steps where swaps occurred
        swap_steps = [s for s in result.steps if s.swap_occurred]
        
        # Each swap step should highlight the swapped positions
        for step in swap_steps:
            assert len(step.highlighted_indices) >= 2, "Swap steps should highlight at least 2 indices"


class TestSelectionSortStatistics:
    """Test statistics tracking for selection_sort."""
    
    def test_statistics_are_non_negative(self):
        """Test that all statistics are non-negative."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([3, 1, 4, 1, 5], 'selection_sort')
        
        assert result.statistics['comparisons'] >= 0
        assert result.statistics['swaps'] >= 0
    
    def test_statistics_match_final_step(self):
        """Test that statistics match the final step counts."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([2, 4, 1, 3], 'selection_sort')
        
        if result.steps:
            last_step = result.steps[-1]
            assert result.statistics['comparisons'] == last_step.comparisons_count
            assert result.statistics['swaps'] == last_step.swaps_count
    
    def test_comparison_count_formula(self):
        """Test that selection sort does n(n-1)/2 comparisons."""
        visualizer = AlgorithmVisualizer()
        
        # Test with different array sizes
        for n in [3, 4, 5, 6]:
            array = list(range(n, 0, -1))  # Reverse sorted
            result = visualizer.visualize_sorting(array, 'selection_sort')
            
            # Selection sort always does n(n-1)/2 comparisons
            expected_comparisons = n * (n - 1) // 2
            assert result.statistics['comparisons'] == expected_comparisons
    
    def test_best_case_swaps(self):
        """Test selection sort best case (already sorted) has 0 swaps."""
        visualizer = AlgorithmVisualizer()
        sorted_array = list(range(10))
        result = visualizer.visualize_sorting(sorted_array.copy(), 'selection_sort')
        
        # Best case: 0 swaps (already sorted)
        assert result.statistics['swaps'] == 0
    
    def test_worst_case_swaps(self):
        """Test selection sort with reverse sorted array."""
        visualizer = AlgorithmVisualizer()
        
        # Reverse sorted array
        reverse_array = [5, 4, 3, 2, 1]
        result = visualizer.visualize_sorting(reverse_array.copy(), 'selection_sort')
        
        # Selection sort does at most n-1 swaps (one per pass if needed)
        # But not all passes require a swap (e.g., if minimum is already in position)
        assert result.statistics['swaps'] <= len(reverse_array) - 1
        assert result.statistics['swaps'] > 0  # At least some swaps needed


class TestSelectionSortAlgorithmCorrectness:
    """Test algorithm correctness for selection_sort."""
    
    def test_sorted_portion_grows(self):
        """Test that sorted portion grows from left to right."""
        visualizer = AlgorithmVisualizer()
        array = [5, 2, 8, 1, 9, 3]
        result = visualizer.visualize_sorting(array.copy(), 'selection_sort')
        
        # After each pass, one more element should be in its final position
        # We can verify this by checking that the array becomes progressively more sorted
        if len(result.steps) > 2:
            # Find steps that show sorted portion
            sorted_portion_steps = [s for s in result.steps if 'sorted portion' in s.description.lower()]
            assert len(sorted_portion_steps) > 0, "Should have steps showing sorted portion"
    
    def test_minimum_element_placement(self):
        """Test that minimum element is placed correctly in each pass."""
        visualizer = AlgorithmVisualizer()
        array = [5, 2, 8, 1, 9]
        result = visualizer.visualize_sorting(array.copy(), 'selection_sort')
        
        # The algorithm should find and place minimum elements
        # After first pass, smallest element should be at index 0
        # After second pass, second smallest should be at index 1, etc.
        
        # Verify final result is sorted
        assert result.final_array == sorted(array)
    
    def test_stability_not_guaranteed(self):
        """Test that selection sort is not stable (equal elements may be reordered)."""
        # Note: Selection sort is NOT a stable sort
        # This test documents this behavior
        visualizer = AlgorithmVisualizer()
        
        # Use tuples to track original positions
        # In practice, we just verify the algorithm works correctly
        array = [3, 1, 3, 2]
        result = visualizer.visualize_sorting(array.copy(), 'selection_sort')
        
        # Should still produce sorted output
        assert result.final_array == [1, 2, 3, 3]


