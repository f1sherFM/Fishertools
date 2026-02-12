"""
Property-based tests for jump_search algorithm.

Feature: fishertools-v0.4.0
These tests validate the correctness properties of the jump_search algorithm.
"""

import pytest
from hypothesis import given, strategies as st

from fishertools.visualization import AlgorithmVisualizer
from fishertools.visualization.algorithms import visualize_jump_search


class TestJumpSearchProperties:
    """
    Property tests for jump_search algorithm.
    
    Feature: fishertools-v0.4.0
    Task: 12.1 Write property tests for jump_search
    """
    
    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20)
    )
    def test_jump_search_finds_existing_targets(self, array):
        """
        Property 14: Search algorithms find existing targets (jump_search)
        
        Validates: Requirements 8.3
        
        For any element that exists in a sorted array, jump_search should find it
        and return the correct index.
        """
        # Sort the array (jump search requires sorted input)
        sorted_array = sorted(array)
        
        # Pick a random element from the array as target
        target = sorted_array[len(sorted_array) // 2]  # Use middle element
        
        # Run jump search
        steps = list(visualize_jump_search(sorted_array, target))
        
        # Property: should find the target
        assert steps, "Should generate at least one step"
        last_step = steps[-1]
        assert last_step.found is True, f"Should find {target} in {sorted_array}"
        
        # Property: found index should contain the target
        found_index = last_step.middle_index
        assert 0 <= found_index < len(sorted_array), f"Found index {found_index} out of bounds"
        assert sorted_array[found_index] == target, f"Element at found index should be {target}"
    
    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=20),
        st.integers(min_value=101, max_value=200)  # Target not in array range
    )
    def test_jump_search_reports_not_found_correctly(self, array, target):
        """
        Property 15: Search algorithms report not found correctly (jump_search)
        
        Validates: Requirements 8.3
        
        When searching for an element that doesn't exist in a sorted array,
        jump_search should report found=False.
        """
        # Sort the array
        sorted_array = sorted(array)
        
        # Ensure target is not in array
        if target in sorted_array:
            return  # Skip this test case
        
        # Run jump search
        steps = list(visualize_jump_search(sorted_array, target))
        
        # Property: should report not found
        assert steps, "Should generate at least one step"
        last_step = steps[-1]
        assert last_step.found is False, f"Should not find {target} in {sorted_array}"
        
        # Property: middle_index should be -1 when not found
        assert last_step.middle_index == -1, "middle_index should be -1 when not found"
    
    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=2, max_size=20)
    )
    def test_jump_search_requires_sorted_arrays(self, array):
        """
        Property 17: Jump search requires sorted arrays
        
        Validates: Requirements 8.5
        
        Jump search should raise ValueError when given an unsorted array.
        """
        # Ensure array is unsorted
        import random
        unsorted_array = array.copy()
        random.shuffle(unsorted_array)
        
        # Check if array is actually unsorted
        is_sorted = all(unsorted_array[i] <= unsorted_array[i + 1] 
                       for i in range(len(unsorted_array) - 1))
        
        if is_sorted:
            # Array happened to be sorted after shuffle, skip
            return
        
        # Pick a target
        target = unsorted_array[0]
        
        # Property: should raise ValueError for unsorted array
        with pytest.raises(ValueError) as exc_info:
            list(visualize_jump_search(unsorted_array, target))
        
        # Property: error message should mention sorting requirement
        assert "sorted" in str(exc_info.value).lower(), \
            "Error message should mention that array must be sorted"
    
    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20)
    )
    def test_jump_search_includes_jump_information(self, array):
        """
        Property 20: Jump search includes jump information
        
        Validates: Requirements 8.4
        
        Jump search steps should include jump_size and block_start information
        to show the block-based search strategy.
        """
        # Sort the array
        sorted_array = sorted(array)
        target = sorted_array[0]
        
        # Run jump search
        steps = list(visualize_jump_search(sorted_array, target))
        
        # Property: all steps should have jump_size set
        for step in steps:
            assert hasattr(step, 'jump_size'), "Step should have jump_size attribute"
            assert step.jump_size is not None, "jump_size should be set"
            assert step.jump_size > 0, "jump_size should be positive"
        
        # Property: all steps should have block_start set
        for step in steps:
            assert hasattr(step, 'block_start'), "Step should have block_start attribute"
            assert step.block_start is not None, "block_start should be set"
            assert step.block_start >= 0, "block_start should be non-negative"
    
    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20)
    )
    def test_jump_search_step_structure(self, array):
        """Test that jump search steps have proper structure."""
        sorted_array = sorted(array)
        target = sorted_array[0]
        steps = list(visualize_jump_search(sorted_array, target))
        
        # Property: all steps have required attributes
        for step in steps:
            assert hasattr(step, 'step_number')
            assert hasattr(step, 'description')
            assert hasattr(step, 'array_state')
            assert hasattr(step, 'highlighted_indices')
            assert hasattr(step, 'search_range')
            assert hasattr(step, 'middle_index')
            assert hasattr(step, 'found')
            assert hasattr(step, 'jump_size')
            assert hasattr(step, 'block_start')
    
    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20)
    )
    def test_jump_search_preserves_input_array(self, array):
        """Test that jump search does not modify the input array."""
        sorted_array = sorted(array)
        original = sorted_array.copy()
        target = sorted_array[0]
        
        # Run jump search
        steps = list(visualize_jump_search(sorted_array, target))
        
        # Property: input array should be unchanged
        assert sorted_array == original
    
    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20)
    )
    def test_jump_search_step_numbers_sequential(self, array):
        """Test that step numbers are sequential."""
        sorted_array = sorted(array)
        target = sorted_array[0]
        steps = list(visualize_jump_search(sorted_array, target))
        
        # Property: step numbers should be sequential starting from 0
        for i, step in enumerate(steps):
            assert step.step_number == i
    
    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20)
    )
    def test_jump_search_highlighted_indices_valid(self, array):
        """Test that highlighted indices are valid."""
        sorted_array = sorted(array)
        target = sorted_array[0]
        steps = list(visualize_jump_search(sorted_array, target))
        
        # Property: highlighted indices should be within bounds
        for step in steps:
            for idx in step.highlighted_indices:
                assert 0 <= idx < len(sorted_array), f"Invalid highlighted index {idx}"
    
    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=4, max_size=20)
    )
    def test_jump_search_efficiency(self, array):
        """Test that jump search uses fewer comparisons than linear search."""
        sorted_array = sorted(array)
        # Target at end to maximize comparisons
        target = sorted_array[-1]
        
        steps = list(visualize_jump_search(sorted_array, target))
        
        # Property: should use O(в€љn) steps, not O(n)
        # Count only the checking steps (not initial, jump, or found steps)
        check_steps = [s for s in steps if "Checking" in s.description]
        
        import math
        # For jump search, we check at most в€љn elements in the final block
        expected_max_checks = int(math.sqrt(len(sorted_array))) + 1
        
        # Jump search should check fewer elements than array size
        assert len(check_steps) <= expected_max_checks + 2, \
            f"Jump search should check at most в€љn elements, got {len(check_steps)}"


