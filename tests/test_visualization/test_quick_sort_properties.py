"""
Property-based tests for quick_sort algorithm.

Feature: fishertools-v0.5.0
These tests validate the correctness properties of the quick_sort algorithm.
"""

import pytest
from hypothesis import given, strategies as st

from fishertools.visualization.algorithm_visualizer import AlgorithmVisualizer
from fishertools.visualization.models import AlgorithmVisualization, SortingStep


class TestQuickSortCorrectness:
    """
    Property 6: All sorting algorithms produce sorted output (quick_sort)
    Property 7: Sorting preserves elements (quick_sort)
    
    Validates: Requirements 3.3
    """
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=20))
    def test_quick_sort_produces_sorted_output(self, array):
        """
        Property 6: Quick sort produces sorted output.
        
        For any list of integers, quick_sort should produce a sorted array.
        """
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array, 'quick_sort')
        
        # Property: output is sorted
        assert result.final_array == sorted(array), \
            f"Quick sort failed to sort {array}: got {result.final_array}"
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=20))
    def test_quick_sort_preserves_elements(self, array):
        """
        Property 7: Sorting preserves elements.
        
        Quick sort should not add or remove elements, only reorder them.
        """
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array, 'quick_sort')
        
        # Property: same elements (multiset equality)
        assert sorted(result.final_array) == sorted(array), \
            f"Quick sort changed elements: {array} -> {result.final_array}"
        
        # Property: same length
        assert len(result.final_array) == len(array), \
            f"Quick sort changed array length: {len(array)} -> {len(result.final_array)}"


class TestQuickSortPartitionInformation:
    """
    Property 10: Quick sort includes partition information
    
    Validates: Requirements 3.4
    """
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=2, max_size=20))
    def test_quick_sort_includes_partition_index(self, array):
        """
        Property 10: Quick sort includes partition information.
        
        Quick sort steps should include partition_index to show pivot positions.
        """
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array, 'quick_sort')
        
        # At least some steps should have partition_index set
        partition_steps = [step for step in result.steps if step.partition_index is not None]
        
        assert len(partition_steps) > 0, \
            "Quick sort should include partition information in steps"
        
        # Partition indices should be valid
        for step in partition_steps:
            assert 0 <= step.partition_index < len(step.array_state), \
                f"Invalid partition index {step.partition_index} for array of length {len(step.array_state)}"
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_quick_sort_step_structure(self, array):
        """Test that quick sort steps have proper structure."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array, 'quick_sort')
        
        # All steps should be SortingStep instances
        for step in result.steps:
            assert isinstance(step, SortingStep), \
                f"Step {step.step_number} is not a SortingStep"
            
            # Array state should match input length
            assert len(step.array_state) == len(array), \
                f"Step {step.step_number} has wrong array length"
            
            # Counts should be non-negative
            assert step.comparisons_count >= 0
            assert step.swaps_count >= 0
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_quick_sort_statistics_accuracy(self, array):
        """Test that statistics accurately reflect the algorithm execution."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array, 'quick_sort')
        
        # Statistics should match final step
        if result.steps:
            final_step = result.steps[-1]
            assert result.statistics['comparisons'] == final_step.comparisons_count
            assert result.statistics['swaps'] == final_step.swaps_count
            assert result.statistics['steps'] == len(result.steps)
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_quick_sort_preserves_input_array(self, array):
        """Test that quick sort does not modify the input array."""
        visualizer = AlgorithmVisualizer()
        original = array.copy()
        result = visualizer.visualize_sorting(array, 'quick_sort')
        
        assert array == original, \
            "Quick sort modified the input array"
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_quick_sort_step_numbers_sequential(self, array):
        """Test that step numbers are sequential."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array, 'quick_sort')
        
        for i, step in enumerate(result.steps):
            assert step.step_number == i, \
                f"Step {i} has number {step.step_number}"
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_quick_sort_comparisons_monotonic(self, array):
        """Test that comparison count never decreases."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array, 'quick_sort')
        
        prev_comparisons = 0
        for step in result.steps:
            assert step.comparisons_count >= prev_comparisons, \
                f"Comparison count decreased at step {step.step_number}"
            prev_comparisons = step.comparisons_count
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_quick_sort_swaps_monotonic(self, array):
        """Test that swap count never decreases."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array, 'quick_sort')
        
        prev_swaps = 0
        for step in result.steps:
            assert step.swaps_count >= prev_swaps, \
                f"Swap count decreased at step {step.step_number}"
            prev_swaps = step.swaps_count
