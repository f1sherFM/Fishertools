"""
Property-based tests for linear_search algorithm.

Feature: fishertools-v0.5.0
These tests validate the correctness properties of the linear_search algorithm.
"""

import pytest
from hypothesis import given, strategies as st

from fishertools.visualization import AlgorithmVisualizer
from fishertools.visualization.algorithms import visualize_linear_search


class TestLinearSearchProperties:
    """
    Property tests for linear_search algorithm.
    
    Feature: fishertools-v0.5.0
    Task: 11.1 Write property tests for linear_search
    """
    
    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20)
    )
    def test_linear_search_finds_existing_targets(self, array):
        """
        Property 14: Search algorithms find existing targets (linear_search)
        
        Validates: Requirements 7.3
        
        For any element that exists in the array, linear_search should find it
        and return the correct index.
        """
        # Pick a random element from the array as target
        target = array[len(array) // 2]  # Use middle element
        
        # Run linear search
        steps = list(visualize_linear_search(array, target))
        
        # Property: should find the target
        assert steps, "Should generate at least one step"
        last_step = steps[-1]
        assert last_step.found is True, f"Should find {target} in {array}"
        
        # Property: found index should contain the target
        found_index = last_step.middle_index
        assert 0 <= found_index < len(array), f"Found index {found_index} out of bounds"
        assert array[found_index] == target, f"Element at found index should be {target}"
    
    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=20),
        st.integers(min_value=101, max_value=200)  # Target not in array range
    )
    def test_linear_search_reports_not_found_correctly(self, array, target):
        """
        Property 15: Search algorithms report not found correctly (linear_search)
        
        Validates: Requirements 7.3
        
        When searching for an element that doesn't exist in the array,
        linear_search should report found=False.
        """
        # Ensure target is not in array
        if target in array:
            return  # Skip this test case
        
        # Run linear search
        steps = list(visualize_linear_search(array, target))
        
        # Property: should report not found
        assert steps, "Should generate at least one step"
        last_step = steps[-1]
        assert last_step.found is False, f"Should not find {target} in {array}"
        
        # Property: middle_index should be -1 when not found
        assert last_step.middle_index == -1, "middle_index should be -1 when not found"
    
    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=2, max_size=20)
    )
    def test_linear_search_works_on_unsorted_arrays(self, array):
        """
        Property 16: Linear search works on unsorted arrays
        
        Validates: Requirements 7.1, 7.3
        
        Linear search should work correctly on unsorted arrays, unlike binary search
        which requires sorted input.
        """
        # Ensure array is unsorted (shuffle if needed)
        import random
        unsorted_array = array.copy()
        random.shuffle(unsorted_array)
        
        # Pick a target that exists
        target = unsorted_array[0]
        
        # Run linear search on unsorted array
        steps = list(visualize_linear_search(unsorted_array, target))
        
        # Property: should still find the target
        assert steps, "Should generate at least one step"
        last_step = steps[-1]
        assert last_step.found is True, f"Should find {target} even in unsorted array"
        
        # Property: found index should contain the target
        found_index = last_step.middle_index
        assert unsorted_array[found_index] == target
    
    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20)
    )
    def test_linear_search_step_structure(self, array):
        """Test that linear search steps have proper structure."""
        target = array[0]
        steps = list(visualize_linear_search(array, target))
        
        # Property: all steps have required attributes
        for step in steps:
            assert hasattr(step, 'step_number')
            assert hasattr(step, 'description')
            assert hasattr(step, 'array_state')
            assert hasattr(step, 'highlighted_indices')
            assert hasattr(step, 'search_range')
            assert hasattr(step, 'middle_index')
            assert hasattr(step, 'found')
    
    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20)
    )
    def test_linear_search_preserves_input_array(self, array):
        """Test that linear search does not modify the input array."""
        original = array.copy()
        target = array[0]
        
        # Run linear search
        steps = list(visualize_linear_search(array, target))
        
        # Property: input array should be unchanged
        assert array == original
    
    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20)
    )
    def test_linear_search_step_numbers_sequential(self, array):
        """Test that step numbers are sequential."""
        target = array[0]
        steps = list(visualize_linear_search(array, target))
        
        # Property: step numbers should be sequential starting from 0
        for i, step in enumerate(steps):
            assert step.step_number == i
    
    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20)
    )
    def test_linear_search_highlighted_indices_valid(self, array):
        """Test that highlighted indices are valid."""
        target = array[0]
        steps = list(visualize_linear_search(array, target))
        
        # Property: highlighted indices should be within bounds
        for step in steps:
            for idx in step.highlighted_indices:
                assert 0 <= idx < len(array), f"Invalid highlighted index {idx}"
    
    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20)
    )
    def test_linear_search_checks_sequentially(self, array):
        """Test that linear search checks elements sequentially from start."""
        target = array[-1]  # Target at end to check all elements
        steps = list(visualize_linear_search(array, target))
        
        # Property: should check elements in order from 0 to n-1
        # Filter steps that are checking elements (not initial/final steps)
        check_steps = [s for s in steps if s.found is None and s.highlighted_indices]
        
        # Indices should be sequential
        for i, step in enumerate(check_steps):
            if step.highlighted_indices:
                # Should be checking index i
                assert i in step.highlighted_indices or i == step.middle_index
    
    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20)
    )
    def test_linear_search_stops_when_found(self, array):
        """Test that linear search stops immediately when target is found."""
        target = array[0]  # Target at beginning
        steps = list(visualize_linear_search(array, target))
        
        # Property: should not check elements after finding target
        found_step_index = None
        for i, step in enumerate(steps):
            if step.found is True:
                found_step_index = i
                break
        
        # All steps after found should not exist (search stops)
        assert found_step_index is not None, "Should find the target"
        assert found_step_index == len(steps) - 1, "Should stop immediately after finding"
