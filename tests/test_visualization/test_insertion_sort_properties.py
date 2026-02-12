"""
Property-based tests for insertion_sort algorithm.

Feature: fishertools-v0.4.0
These tests validate the correctness properties of the insertion_sort algorithm.
"""

import pytest
from hypothesis import given, strategies as st

from fishertools.visualization import AlgorithmVisualizer


class TestInsertionSortProperties:
    """
    Property tests for insertion_sort algorithm.
    
    Feature: fishertools-v0.4.0
    Task: 8.1 Write property tests for insertion_sort
    """
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=20))
    def test_insertion_sort_produces_sorted_output(self, array):
        """
        Property 6: All sorting algorithms produce sorted output (insertion_sort)
        
        Validates: Requirements 5.3
        
        For any list of integers, insertion_sort should produce a sorted array.
        """
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array.copy(), 'insertion_sort')
        
        # Property: output is sorted
        assert result.final_array == sorted(array)
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=20))
    def test_insertion_sort_preserves_elements(self, array):
        """
        Property 7: Sorting preserves elements (insertion_sort)
        
        Validates: Requirements 5.3
        
        Insertion sort should not add, remove, or change elements - only reorder them.
        The sorted array should contain exactly the same elements as the input.
        """
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array.copy(), 'insertion_sort')
        
        # Property: same elements (multiset equality)
        assert sorted(result.final_array) == sorted(array)
        assert len(result.final_array) == len(array)
        
        # Count occurrences of each element
        from collections import Counter
        assert Counter(result.final_array) == Counter(array)
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=2, max_size=20))
    def test_insertion_sort_highlights_sorted_portion(self, array):
        """
        Property 12: Insertion sort highlights sorted portion
        
        Validates: Requirements 5.4
        
        Insertion sort should highlight the sorted portion and the element being inserted
        in its visualization steps.
        """
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array.copy(), 'insertion_sort')
        
        # Property: steps should highlight indices showing sorted portion
        # At least some steps should have highlighted_indices
        steps_with_highlights = [step for step in result.steps if step.highlighted_indices]
        assert len(steps_with_highlights) > 0, "Insertion sort should highlight sorted portion"
        
        # Property: highlighted indices should be valid
        for step in result.steps:
            for idx in step.highlighted_indices:
                assert 0 <= idx < len(array), f"Invalid highlighted index {idx}"
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_insertion_sort_step_structure(self, array):
        """Test that insertion sort steps have proper structure."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array.copy(), 'insertion_sort')
        
        # Property: all steps have required attributes
        for step in result.steps:
            assert hasattr(step, 'step_number')
            assert hasattr(step, 'description')
            assert hasattr(step, 'array_state')
            assert hasattr(step, 'highlighted_indices')
            assert hasattr(step, 'comparisons_count')
            assert hasattr(step, 'swaps_count')
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_insertion_sort_statistics_accuracy(self, array):
        """Test that statistics accurately reflect the algorithm execution."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array.copy(), 'insertion_sort')
        
        # Property: statistics should be non-negative
        assert result.statistics.get('comparisons', 0) >= 0
        assert result.statistics.get('swaps', 0) >= 0
        
        # Property: final step should have same counts as statistics
        if result.steps:
            last_step = result.steps[-1]
            assert last_step.comparisons_count == result.statistics.get('comparisons', 0)
            assert last_step.swaps_count == result.statistics.get('swaps', 0)
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_insertion_sort_preserves_input_array(self, array):
        """Test that insertion sort does not modify the input array."""
        visualizer = AlgorithmVisualizer()
        original = array.copy()
        result = visualizer.visualize_sorting(array, 'insertion_sort')
        
        # Property: input array should be unchanged
        assert array == original
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_insertion_sort_step_numbers_sequential(self, array):
        """Test that step numbers are sequential."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array.copy(), 'insertion_sort')
        
        # Property: step numbers should be sequential starting from 0
        for i, step in enumerate(result.steps):
            assert step.step_number == i
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_insertion_sort_comparisons_monotonic(self, array):
        """Test that comparison count never decreases."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array.copy(), 'insertion_sort')
        
        # Property: comparisons should be monotonically increasing
        prev_comparisons = 0
        for step in result.steps:
            assert step.comparisons_count >= prev_comparisons
            prev_comparisons = step.comparisons_count
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_insertion_sort_swaps_monotonic(self, array):
        """Test that swap count never decreases."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array.copy(), 'insertion_sort')
        
        # Property: swaps should be monotonically increasing
        prev_swaps = 0
        for step in result.steps:
            assert step.swaps_count >= prev_swaps
            prev_swaps = step.swaps_count


