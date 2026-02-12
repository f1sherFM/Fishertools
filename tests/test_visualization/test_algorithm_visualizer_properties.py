"""
Property-based tests for algorithm visualizer.

Feature: fishertools-enhancements
These tests validate the correctness properties of algorithm visualization.
"""

import pytest
from hypothesis import given, strategies as st

from fishertools.visualization.algorithm_visualizer import AlgorithmVisualizer
from fishertools.visualization.models import (
    AlgorithmVisualization,
    SortingStep,
    SearchStep,
)


class TestSortingStepGeneration:
    """
    Property 11: Sorting step generation
    
    For any array and supported sorting algorithm, visualize_sorting() should
    generate a sequence of steps that correctly represents the algorithm's execution.
    
    Validates: Requirements 4.1, 4.2
    """
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=20))
    def test_sorting_produces_valid_steps(self, array):
        """Test that sorting produces valid step sequences."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array, algorithm='bubble_sort')
        
        # Should return AlgorithmVisualization
        assert isinstance(result, AlgorithmVisualization)
        
        # Should have steps
        assert isinstance(result.steps, list)
        
        # All steps should be SortingStep instances
        for step in result.steps:
            assert isinstance(step, SortingStep)
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_sorting_step_numbers_are_sequential(self, array):
        """Test that step numbers are sequential starting from 0."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array, algorithm='bubble_sort')
        
        for i, step in enumerate(result.steps):
            assert step.step_number == i, f"Step {i} has number {step.step_number}"
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_sorting_final_array_is_sorted(self, array):
        """Test that the final array state is sorted."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array, algorithm='bubble_sort')
        
        if result.steps:
            final_state = result.steps[-1].array_state
            assert final_state == sorted(array), \
                f"Final state {final_state} != sorted {sorted(array)}"
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_sorting_preserves_array_elements(self, array):
        """Test that sorting preserves all elements (no additions/deletions)."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array, algorithm='bubble_sort')
        
        if result.steps:
            final_state = result.steps[-1].array_state
            assert sorted(final_state) == sorted(array), \
                "Sorting changed array elements"
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_sorting_comparisons_count_increases_monotonically(self, array):
        """Test that comparison count never decreases."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array, algorithm='bubble_sort')
        
        prev_comparisons = 0
        for step in result.steps:
            assert step.comparisons_count >= prev_comparisons, \
                "Comparison count decreased"
            prev_comparisons = step.comparisons_count
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_sorting_swaps_count_increases_monotonically(self, array):
        """Test that swap count never decreases."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array, algorithm='bubble_sort')
        
        prev_swaps = 0
        for step in result.steps:
            assert step.swaps_count >= prev_swaps, \
                "Swap count decreased"
            prev_swaps = step.swaps_count
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_sorting_statistics_match_final_step(self, array):
        """Test that statistics match the final step counts."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array, algorithm='bubble_sort')
        
        if result.steps:
            final_step = result.steps[-1]
            assert result.statistics['comparisons'] == final_step.comparisons_count
            assert result.statistics['swaps'] == final_step.swaps_count
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=20))
    def test_sorting_preserves_input_array(self, array):
        """Test that the original input array is not modified."""
        visualizer = AlgorithmVisualizer()
        original = array.copy()
        result = visualizer.visualize_sorting(array, algorithm='bubble_sort')
        
        assert array == original, "Input array was modified"
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_sorting_array_states_have_correct_length(self, array):
        """Test that all array states have the same length as input."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array, algorithm='bubble_sort')
        
        for step in result.steps:
            assert len(step.array_state) == len(array), \
                f"Array state length {len(step.array_state)} != input length {len(array)}"


class TestSearchStepGeneration:
    """
    Property 12: Search step generation
    
    For any sorted array, target value, and supported search algorithm,
    visualize_search() should generate steps that correctly represent the search process.
    
    Validates: Requirements 4.3, 4.4
    """
    
    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20),
        st.integers(min_value=-100, max_value=100)
    )
    def test_search_produces_valid_steps(self, array, target):
        """Test that search produces valid step sequences."""
        sorted_array = sorted(array)
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_search(sorted_array, target, algorithm='binary_search')
        
        # Should return AlgorithmVisualization
        assert isinstance(result, AlgorithmVisualization)
        
        # Should have steps
        assert isinstance(result.steps, list)
        assert len(result.steps) > 0
        
        # All steps should be SearchStep instances
        for step in result.steps:
            assert isinstance(step, SearchStep)
    
    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20),
        st.integers(min_value=-100, max_value=100)
    )
    def test_search_step_numbers_are_sequential(self, array, target):
        """Test that step numbers are sequential starting from 0."""
        sorted_array = sorted(array)
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_search(sorted_array, target, algorithm='binary_search')
        
        for i, step in enumerate(result.steps):
            assert step.step_number == i, f"Step {i} has number {step.step_number}"
    
    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20),
        st.integers(min_value=-100, max_value=100)
    )
    def test_search_finds_existing_elements(self, array, target):
        """Test that search correctly finds elements that exist in the array."""
        sorted_array = sorted(array)
        visualizer = AlgorithmVisualizer()
        
        # Search for an element that exists
        if sorted_array:
            existing_target = sorted_array[len(sorted_array) // 2]
            result = visualizer.visualize_search(sorted_array, existing_target, algorithm='binary_search')
            
            final_step = result.steps[-1]
            assert final_step.found == True, \
                f"Failed to find existing element {existing_target} in {sorted_array}"
    
    @given(
        st.lists(st.integers(min_value=0, max_value=50), min_size=1, max_size=20),
        st.integers(min_value=100, max_value=200)
    )
    def test_search_reports_missing_elements(self, array, target):
        """Test that search correctly reports when element is not found."""
        sorted_array = sorted(array)
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_search(sorted_array, target, algorithm='binary_search')
        
        final_step = result.steps[-1]
        if target not in sorted_array:
            assert final_step.found == False, \
                f"Incorrectly reported finding {target} in {sorted_array}"
    
    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20),
        st.integers(min_value=-100, max_value=100)
    )
    def test_search_range_narrows_monotonically(self, array, target):
        """Test that search range size never increases."""
        sorted_array = sorted(array)
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_search(sorted_array, target, algorithm='binary_search')
        
        prev_range_size = len(sorted_array)
        for step in result.steps[1:]:  # Skip initial step
            if step.found is None:  # Still searching
                left, right = step.search_range
                current_range_size = right - left + 1
                assert current_range_size <= prev_range_size, \
                    "Search range increased"
                prev_range_size = current_range_size
    
    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20),
        st.integers(min_value=-100, max_value=100)
    )
    def test_search_preserves_input_array(self, array, target):
        """Test that the original input array is not modified."""
        sorted_array = sorted(array)
        original = sorted_array.copy()
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_search(sorted_array, target, algorithm='binary_search')
        
        assert sorted_array == original, "Input array was modified"
    
    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20),
        st.integers(min_value=-100, max_value=100)
    )
    def test_search_middle_index_within_range(self, array, target):
        """Test that middle index is always within the search range."""
        sorted_array = sorted(array)
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_search(sorted_array, target, algorithm='binary_search')
        
        for step in result.steps[1:]:  # Skip initial step
            if step.found is None and step.middle_index >= 0:
                left, right = step.search_range
                assert left <= step.middle_index <= right, \
                    f"Middle index {step.middle_index} not in range [{left}, {right}]"


class TestAlgorithmStatisticsAccuracy:
    """
    Property 13: Algorithm statistics accuracy
    
    For any algorithm visualization, the returned statistics should accurately
    count the operations performed (comparisons, swaps, etc.)
    
    Validates: Requirements 4.5
    """
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_sorting_statistics_are_non_negative(self, array):
        """Test that all statistics are non-negative."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array, algorithm='bubble_sort')
        
        assert result.statistics['comparisons'] >= 0
        assert result.statistics['swaps'] >= 0
        assert result.statistics['steps'] >= 0
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_sorting_statistics_steps_count_matches(self, array):
        """Test that steps count in statistics matches actual step count."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array, algorithm='bubble_sort')
        
        assert result.statistics['steps'] == len(result.steps)
    
    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20),
        st.integers(min_value=-100, max_value=100)
    )
    def test_search_statistics_are_non_negative(self, array, target):
        """Test that all search statistics are non-negative."""
        sorted_array = sorted(array)
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_search(sorted_array, target, algorithm='binary_search')
        
        assert result.statistics['comparisons'] >= 0
        assert result.statistics['steps'] >= 0
    
    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20),
        st.integers(min_value=-100, max_value=100)
    )
    def test_search_statistics_steps_count_matches(self, array, target):
        """Test that steps count in statistics matches actual step count."""
        sorted_array = sorted(array)
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_search(sorted_array, target, algorithm='binary_search')
        
        assert result.statistics['steps'] == len(result.steps)
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=2, max_size=20))
    def test_sorting_already_sorted_array_has_minimal_swaps(self, array):
        """Test that sorting an already sorted array requires no swaps."""
        sorted_array = sorted(array)
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(sorted_array, algorithm='bubble_sort')
        
        # Already sorted array should have 0 swaps
        assert result.statistics['swaps'] == 0, \
            f"Sorted array required {result.statistics['swaps']} swaps"
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_sorting_statistics_reflect_algorithm_behavior(self, array):
        """Test that statistics accurately reflect bubble sort behavior."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array, algorithm='bubble_sort')
        
        # For bubble sort, comparisons should be at least n-1 for one pass
        n = len(array)
        if n > 1:
            assert result.statistics['comparisons'] >= n - 1, \
                "Too few comparisons for bubble sort"



class TestMergeSortProperties:
    """
    Property tests for merge_sort algorithm.
    
    Feature: fishertools-v0.4.0
    Validates: Requirements 4.1, 4.2, 4.3, 4.4
    """
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=20))
    def test_merge_sort_produces_sorted_output(self, array):
        """
        Property 6: All sorting algorithms produce sorted output (merge_sort)
        
        For any list of integers, merge_sort should produce a sorted array.
        Validates: Requirements 4.3
        """
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array, 'merge_sort')
        
        # Property: output is sorted
        assert result.final_array == sorted(array), \
            f"Merge sort output {result.final_array} != sorted {sorted(array)}"
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=20))
    def test_merge_sort_preserves_elements(self, array):
        """
        Property 7: Sorting preserves elements (merge_sort)
        
        For any list, merge_sort should preserve all elements (no additions/deletions).
        Validates: Requirements 4.3
        """
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array, 'merge_sort')
        
        # Property: all elements preserved
        assert sorted(result.final_array) == sorted(array), \
            "Merge sort changed array elements"
        assert len(result.final_array) == len(array), \
            "Merge sort changed array length"
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=2, max_size=20))
    def test_merge_sort_includes_merge_range_information(self, array):
        """
        Property 11: Merge sort includes merge range information
        
        For any array with 2+ elements, merge_sort steps should include merge_range 
        information showing division and merge boundaries.
        Validates: Requirements 4.4
        """
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array, 'merge_sort')
        
        # Property: merge_range is present in steps
        merge_steps = [step for step in result.steps if step.merge_range is not None]
        assert len(merge_steps) > 0, "No merge_range information found in steps"
        
        # Property: merge_range values are valid
        for step in merge_steps:
            left, right = step.merge_range
            assert 0 <= left <= right < len(array), \
                f"Invalid merge_range ({left}, {right}) for array of length {len(array)}"


