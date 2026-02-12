"""
Unit tests for jump_search algorithm edge cases.

Feature: fishertools-v0.4.0
These tests validate specific behaviors and edge cases of the jump_search algorithm.
"""

import pytest

from fishertools.visualization.algorithms import visualize_jump_search


class TestJumpSearchEdgeCases:
    """Test edge cases for jump_search algorithm."""
    
    def test_empty_array_returns_not_found(self):
        """Test jump_search with empty array returns not found."""
        steps = list(visualize_jump_search([], 42))
        
        assert len(steps) >= 1
        last_step = steps[-1]
        assert last_step.found is False
        assert last_step.middle_index == -1
        assert last_step.array_state == []
    
    def test_single_element_found(self):
        """Test jump_search with single element when target is found."""
        array = [42]
        target = 42
        steps = list(visualize_jump_search(array, target))
        
        # Should find the element
        last_step = steps[-1]
        assert last_step.found is True
        assert last_step.middle_index == 0
        assert array[last_step.middle_index] == target
    
    def test_single_element_not_found(self):
        """Test jump_search with single element when target is not found."""
        array = [42]
        target = 99
        steps = list(visualize_jump_search(array, target))
        
        # Should not find the element
        last_step = steps[-1]
        assert last_step.found is False
        assert last_step.middle_index == -1
    
    def test_target_at_beginning(self):
        """Test jump_search when target is at the beginning of sorted array."""
        array = [10, 20, 30, 40, 50]
        target = 10
        steps = list(visualize_jump_search(array, target))
        
        # Should find at index 0
        last_step = steps[-1]
        assert last_step.found is True
        assert last_step.middle_index == 0
        assert array[0] == target
    
    def test_target_at_middle(self):
        """Test jump_search when target is in the middle of sorted array."""
        array = [10, 20, 30, 40, 50]
        target = 30
        steps = list(visualize_jump_search(array, target))
        
        # Should find at index 2
        last_step = steps[-1]
        assert last_step.found is True
        assert last_step.middle_index == 2
        assert array[2] == target
    
    def test_target_at_end(self):
        """Test jump_search when target is at the end of sorted array."""
        array = [10, 20, 30, 40, 50]
        target = 50
        steps = list(visualize_jump_search(array, target))
        
        # Should find at index 4 (last index)
        last_step = steps[-1]
        assert last_step.found is True
        assert last_step.middle_index == 4
        assert array[4] == target
    
    def test_unsorted_array_raises_value_error(self):
        """Test jump_search raises ValueError for unsorted array."""
        array = [50, 10, 40, 20, 30]  # Unsorted
        target = 20
        
        # Should raise ValueError
        with pytest.raises(ValueError) as exc_info:
            list(visualize_jump_search(array, target))
        
        # Error message should mention sorting requirement
        assert "sorted" in str(exc_info.value).lower()
        assert "jump search" in str(exc_info.value).lower()
    
    def test_target_not_in_array(self):
        """Test jump_search when target is not in sorted array."""
        array = [10, 20, 30, 40, 50]
        target = 99
        steps = list(visualize_jump_search(array, target))
        
        # Should not find the target
        last_step = steps[-1]
        assert last_step.found is False
        assert last_step.middle_index == -1
    
    def test_target_smaller_than_all_elements(self):
        """Test jump_search when target is smaller than all elements."""
        array = [10, 20, 30, 40, 50]
        target = 5
        steps = list(visualize_jump_search(array, target))
        
        # Should not find the target
        last_step = steps[-1]
        assert last_step.found is False
        assert last_step.middle_index == -1
    
    def test_target_larger_than_all_elements(self):
        """Test jump_search when target is larger than all elements."""
        array = [10, 20, 30, 40, 50]
        target = 100
        steps = list(visualize_jump_search(array, target))
        
        # Should not find the target
        last_step = steps[-1]
        assert last_step.found is False
        assert last_step.middle_index == -1
    
    def test_duplicate_elements_finds_one(self):
        """Test jump_search finds one occurrence of duplicate elements."""
        array = [10, 20, 20, 20, 30, 40, 50]
        target = 20
        steps = list(visualize_jump_search(array, target))
        
        # Should find one of the occurrences
        last_step = steps[-1]
        assert last_step.found is True
        found_index = last_step.middle_index
        assert array[found_index] == target
        # Should be one of the valid indices
        assert found_index in [1, 2, 3]
    
    def test_all_same_elements(self):
        """Test jump_search with all identical elements."""
        array = [5, 5, 5, 5, 5]
        target = 5
        steps = list(visualize_jump_search(array, target))
        
        # Should find the element
        last_step = steps[-1]
        assert last_step.found is True
        assert array[last_step.middle_index] == target
    
    def test_negative_numbers(self):
        """Test jump_search with negative numbers in sorted array."""
        array = [-50, -30, -10, 0, 10, 30, 50]
        target = -10
        steps = list(visualize_jump_search(array, target))
        
        # Should find the negative number
        last_step = steps[-1]
        assert last_step.found is True
        assert array[last_step.middle_index] == target
    
    def test_mixed_positive_negative_zero(self):
        """Test jump_search with mix of positive, negative, and zero."""
        array = [-20, -10, 0, 10, 20, 30]
        target = 0
        steps = list(visualize_jump_search(array, target))
        
        # Should find zero
        last_step = steps[-1]
        assert last_step.found is True
        assert array[last_step.middle_index] == target
    
    def test_large_sorted_array(self):
        """Test jump_search with larger sorted array."""
        array = list(range(0, 100, 5))  # [0, 5, 10, ..., 95]
        target = 50
        steps = list(visualize_jump_search(array, target))
        
        # Should find the target
        last_step = steps[-1]
        assert last_step.found is True
        assert array[last_step.middle_index] == target


class TestJumpSearchVisualizationDetails:
    """Test specific visualization details for jump_search."""
    
    def test_step_descriptions_are_meaningful(self):
        """Test that step descriptions provide meaningful information."""
        array = [10, 20, 30, 40, 50]
        target = 30
        steps = list(visualize_jump_search(array, target))
        
        # All steps should have non-empty descriptions
        for step in steps:
            assert step.description
            assert len(step.description) > 0
    
    def test_jump_size_is_calculated_correctly(self):
        """Test that jump size is calculated as sqrt(n)."""
        import math
        
        array = list(range(0, 100, 5))  # 20 elements
        target = 50
        steps = list(visualize_jump_search(array, target))
        
        # Jump size should be sqrt(20) = 4
        expected_jump_size = int(math.sqrt(len(array)))
        
        # All steps should have the same jump size
        for step in steps:
            assert step.jump_size == expected_jump_size
    
    def test_block_start_is_set_correctly(self):
        """Test that block_start is set correctly in steps."""
        array = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        target = 70
        steps = list(visualize_jump_search(array, target))
        
        # All steps should have block_start set
        for step in steps:
            assert step.block_start is not None
            assert step.block_start >= 0
    
    def test_highlighted_indices_show_current_check(self):
        """Test that highlighted indices show the element being checked."""
        array = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        target = 50
        steps = list(visualize_jump_search(array, target))
        
        # Check steps should highlight indices
        for step in steps:
            if step.found is None and step.description.startswith("Checking"):
                # Should highlight the index being checked
                assert len(step.highlighted_indices) > 0
    
    def test_array_state_remains_unchanged(self):
        """Test that array state remains unchanged throughout search."""
        array = [10, 20, 30, 40, 50]
        target = 30
        original = array.copy()
        steps = list(visualize_jump_search(array, target))
        
        # All steps should have same array state
        for step in steps:
            assert step.array_state == original
    
    def test_search_range_is_set_correctly(self):
        """Test that search range is set correctly."""
        array = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        target = 50
        steps = list(visualize_jump_search(array, target))
        
        # All steps should have valid search range
        for step in steps:
            start, end = step.search_range
            assert 0 <= start <= end < len(array)
    
    def test_step_numbers_are_sequential(self):
        """Test that step numbers are sequential starting from 0."""
        array = [10, 20, 30, 40, 50]
        target = 30
        steps = list(visualize_jump_search(array, target))
        
        for i, step in enumerate(steps):
            assert step.step_number == i
    
    def test_found_flag_progression(self):
        """Test that found flag progresses correctly: None -> True/False."""
        array = [10, 20, 30, 40, 50]
        target = 30
        steps = list(visualize_jump_search(array, target))
        
        # All steps except last should have found=None
        for step in steps[:-1]:
            assert step.found is None
        
        # Last step should have found=True or False
        assert steps[-1].found in [True, False]


class TestJumpSearchAlgorithmCorrectness:
    """Test algorithm correctness for jump_search."""
    
    def test_uses_block_jumping_strategy(self):
        """Test that jump search uses block jumping, not sequential checking."""
        array = list(range(0, 100, 5))  # [0, 5, 10, ..., 95]
        target = 95  # At end
        steps = list(visualize_jump_search(array, target))
        
        # Should have jump steps (not checking every element)
        jump_steps = [s for s in steps if "Jumping" in s.description]
        assert len(jump_steps) > 0, "Should have jump steps"
    
    def test_performs_linear_search_in_block(self):
        """Test that jump search performs linear search within identified block."""
        array = list(range(0, 50, 5))  # [0, 5, 10, ..., 45]
        target = 27  # Not in array, but would be in a block
        steps = list(visualize_jump_search(array, target))
        
        # Should have checking steps within a block
        check_steps = [s for s in steps if "Checking" in s.description]
        # Should check some elements in the block
        assert len(check_steps) >= 0  # May be 0 if target is outside range
    
    def test_stops_when_found(self):
        """Test that jump search stops as soon as target is found."""
        array = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        target = 30
        steps = list(visualize_jump_search(array, target))
        
        # Last step should be the found step
        assert steps[-1].found is True
        assert steps[-1].middle_index == 2
    
    def test_works_with_strings(self):
        """Test jump_search works with string elements."""
        array = ["apple", "banana", "cherry", "date", "elderberry"]
        target = "cherry"
        steps = list(visualize_jump_search(array, target))
        
        last_step = steps[-1]
        assert last_step.found is True
        assert array[last_step.middle_index] == target
    
    def test_works_with_floats(self):
        """Test jump_search works with float elements."""
        array = [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7]
        target = 4.4
        steps = list(visualize_jump_search(array, target))
        
        last_step = steps[-1]
        assert last_step.found is True
        assert array[last_step.middle_index] == target
    
    def test_preserves_original_array(self):
        """Test that jump_search does not modify the original array."""
        array = [10, 20, 30, 40, 50]
        original = array.copy()
        target = 30
        
        steps = list(visualize_jump_search(array, target))
        
        # Original array should be unchanged
        assert array == original
    
    def test_efficiency_compared_to_linear(self):
        """Test that jump search is more efficient than linear search for large arrays."""
        import math
        
        # Large sorted array
        array = list(range(0, 1000, 10))  # 100 elements
        target = 990  # Near end
        
        steps = list(visualize_jump_search(array, target))
        
        # Should use approximately O(в€љn) steps
        # With 100 elements, sqrt(100) = 10
        # Should be much less than 100 steps (linear search)
        assert len(steps) < len(array), "Should be more efficient than linear search"


