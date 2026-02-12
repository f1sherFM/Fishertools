"""
Property-based tests for selection_sort algorithm.

Feature: fishertools-v0.4.0
These tests validate the correctness properties of the selection_sort algorithm.
"""

import pytest
from hypothesis import given, strategies as st

from fishertools.visualization import AlgorithmVisualizer


class TestSelectionSortProperties:
    """
    Property tests for selection_sort algorithm.
    
    Feature: fishertools-v0.4.0
    Task: 9.1 Write property tests for selection_sort
    """
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=20))
    def test_selection_sort_produces_sorted_output(self, array):
        """
        Property 6: All sorting algorithms produce sorted output (selection_sort)
        
        Validates: Requirements 6.3
        
        For any list of integers, selection_sort should produce a sorted array.
        """
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array.copy(), 'selection_sort')
        
        # Property: output is sorted
        assert result.final_array == sorted(array)
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=20))
    def test_selection_sort_preserves_elements(self, array):
        """
        Property 7: Sorting preserves elements (selection_sort)
        
        Validates: Requirements 6.3
        
        Selection sort should not add, remove, or change elements - only reorder them.
        The sorted array should contain exactly the same elements as the input.
        """
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array.copy(), 'selection_sort')
        
        # Property: same elements (multiset equality)
        assert sorted(result.final_array) == sorted(array)
        assert len(result.final_array) == len(array)
        
        # Count occurrences of each element
        from collections import Counter
        assert Counter(result.final_array) == Counter(array)
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=2, max_size=20))
    def test_selection_sort_highlights_minimum_search(self, array):
        """
        Property 13: Selection sort highlights minimum search
        
        Validates: Requirements 6.4
        
        Selection sort should highlight the minimum element being searched
        and swap positions in its visualization steps.
        """
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array.copy(), 'selection_sort')
        
        # Property: steps should highlight indices showing minimum search
        # At least some steps should have highlighted_indices
        steps_with_highlights = [step for step in result.steps if step.highlighted_indices]
        assert len(steps_with_highlights) > 0, "Selection sort should highlight minimum search"
        
        # Property: highlighted indices should be valid
        for step in result.steps:
            for idx in step.highlighted_indices:
                assert 0 <= idx < len(array), f"Invalid highlighted index {idx}"
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_selection_sort_step_structure(self, array):
        """Test that selection sort steps have proper structure."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array.copy(), 'selection_sort')
        
        # Property: all steps have required attributes
        for step in result.steps:
            assert hasattr(step, 'step_number')
            assert hasattr(step, 'description')
            assert hasattr(step, 'array_state')
            assert hasattr(step, 'highlighted_indices')
            assert hasattr(step, 'comparisons_count')
            assert hasattr(step, 'swaps_count')
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_selection_sort_statistics_accuracy(self, array):
        """Test that statistics accurately reflect the algorithm execution."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array.copy(), 'selection_sort')
        
        # Property: statistics should be non-negative
        assert result.statistics.get('comparisons', 0) >= 0
        assert result.statistics.get('swaps', 0) >= 0
        
        # Property: final step should have same counts as statistics
        if result.steps:
            last_step = result.steps[-1]
            assert last_step.comparisons_count == result.statistics.get('comparisons', 0)
            assert last_step.swaps_count == result.statistics.get('swaps', 0)
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_selection_sort_preserves_input_array(self, array):
        """Test that selection sort does not modify the input array."""
        visualizer = AlgorithmVisualizer()
        original = array.copy()
        result = visualizer.visualize_sorting(array, 'selection_sort')
        
        # Property: input array should be unchanged
        assert array == original
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_selection_sort_step_numbers_sequential(self, array):
        """Test that step numbers are sequential."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array.copy(), 'selection_sort')
        
        # Property: step numbers should be sequential starting from 0
        for i, step in enumerate(result.steps):
            assert step.step_number == i
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_selection_sort_comparisons_monotonic(self, array):
        """Test that comparison count never decreases."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array.copy(), 'selection_sort')
        
        # Property: comparisons should be monotonically increasing
        prev_comparisons = 0
        for step in result.steps:
            assert step.comparisons_count >= prev_comparisons
            prev_comparisons = step.comparisons_count
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_selection_sort_swaps_monotonic(self, array):
        """Test that swap count never decreases."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array.copy(), 'selection_sort')
        
        # Property: swaps should be monotonically increasing
        prev_swaps = 0
        for step in result.steps:
            assert step.swaps_count >= prev_swaps
            prev_swaps = step.swaps_count
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=2, max_size=20))
    def test_selection_sort_comparison_indices_valid(self, array):
        """Test that comparison indices are valid when present."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array.copy(), 'selection_sort')
        
        # Property: comparison indices should be within bounds
        for step in result.steps:
            if step.comparison_indices:
                i, j = step.comparison_indices
                assert 0 <= i < len(array)
                assert 0 <= j < len(array)
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=2, max_size=20))
    def test_selection_sort_swap_occurred_flag(self, array):
        """Test that swap_occurred flag is set correctly."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array.copy(), 'selection_sort')
        
        # Property: if swap_occurred is True, swaps_count should increase
        prev_swaps = 0
        for step in result.steps:
            if step.swap_occurred:
                assert step.swaps_count > prev_swaps, "Swap occurred but count didn't increase"
            prev_swaps = step.swaps_count


