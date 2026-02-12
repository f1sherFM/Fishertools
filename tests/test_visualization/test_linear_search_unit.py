"""
Unit tests for linear_search algorithm edge cases.

Feature: fishertools-v0.5.2
These tests validate specific behaviors and edge cases of the linear_search algorithm.
"""

import pytest

from fishertools.visualization.algorithms import visualize_linear_search


class TestLinearSearchEdgeCases:
    """Test edge cases for linear_search algorithm."""
    
    def test_empty_array_returns_not_found(self):
        """Test linear_search with empty array returns not found."""
        steps = list(visualize_linear_search([], 42))
        
        assert len(steps) >= 1
        last_step = steps[-1]
        assert last_step.found is False
        assert last_step.middle_index == -1
        assert last_step.array_state == []
    
    def test_single_element_found(self):
        """Test linear_search with single element when target is found."""
        array = [42]
        target = 42
        steps = list(visualize_linear_search(array, target))
        
        # Should find the element
        last_step = steps[-1]
        assert last_step.found is True
        assert last_step.middle_index == 0
        assert array[last_step.middle_index] == target
    
    def test_single_element_not_found(self):
        """Test linear_search with single element when target is not found."""
        array = [42]
        target = 99
        steps = list(visualize_linear_search(array, target))
        
        # Should not find the element
        last_step = steps[-1]
        assert last_step.found is False
        assert last_step.middle_index == -1
    
    def test_target_at_beginning(self):
        """Test linear_search when target is at the beginning of array."""
        array = [10, 20, 30, 40, 50]
        target = 10
        steps = list(visualize_linear_search(array, target))
        
        # Should find at index 0
        last_step = steps[-1]
        assert last_step.found is True
        assert last_step.middle_index == 0
        assert array[0] == target
        
        # Should stop quickly (minimal steps)
        # Initial step + check step + found step = 3 steps
        assert len(steps) <= 4
    
    def test_target_at_middle(self):
        """Test linear_search when target is in the middle of array."""
        array = [10, 20, 30, 40, 50]
        target = 30
        steps = list(visualize_linear_search(array, target))
        
        # Should find at index 2
        last_step = steps[-1]
        assert last_step.found is True
        assert last_step.middle_index == 2
        assert array[2] == target
    
    def test_target_at_end(self):
        """Test linear_search when target is at the end of array."""
        array = [10, 20, 30, 40, 50]
        target = 50
        steps = list(visualize_linear_search(array, target))
        
        # Should find at index 4 (last index)
        last_step = steps[-1]
        assert last_step.found is True
        assert last_step.middle_index == 4
        assert array[4] == target
        
        # Should check all elements before finding
        # More steps than finding at beginning
        assert len(steps) > 4
    
    def test_unsorted_array_works(self):
        """Test linear_search works correctly on unsorted array."""
        array = [50, 10, 40, 20, 30]  # Unsorted
        target = 20
        steps = list(visualize_linear_search(array, target))
        
        # Should still find the target
        last_step = steps[-1]
        assert last_step.found is True
        assert last_step.middle_index == 3
        assert array[3] == target
    
    def test_target_not_in_array(self):
        """Test linear_search when target is not in array."""
        array = [10, 20, 30, 40, 50]
        target = 99
        steps = list(visualize_linear_search(array, target))
        
        # Should not find the target
        last_step = steps[-1]
        assert last_step.found is False
        assert last_step.middle_index == -1
        
        # Should check all elements
        # Initial + n checks + not found = n + 2 steps
        assert len(steps) >= len(array) + 1
    
    def test_duplicate_elements_finds_first(self):
        """Test linear_search finds first occurrence of duplicate elements."""
        array = [10, 20, 30, 20, 50]
        target = 20
        steps = list(visualize_linear_search(array, target))
        
        # Should find first occurrence at index 1
        last_step = steps[-1]
        assert last_step.found is True
        assert last_step.middle_index == 1
        assert array[1] == target
    
    def test_all_same_elements(self):
        """Test linear_search with all identical elements."""
        array = [5, 5, 5, 5, 5]
        target = 5
        steps = list(visualize_linear_search(array, target))
        
        # Should find at first index
        last_step = steps[-1]
        assert last_step.found is True
        assert last_step.middle_index == 0
    
    def test_negative_numbers(self):
        """Test linear_search with negative numbers."""
        array = [-5, -3, -1, 0, 2, 3]
        target = -1
        steps = list(visualize_linear_search(array, target))
        
        # Should find the negative number
        last_step = steps[-1]
        assert last_step.found is True
        assert array[last_step.middle_index] == target
    
    def test_mixed_positive_negative_zero(self):
        """Test linear_search with mix of positive, negative, and zero."""
        array = [0, -1, 1, -2, 2, 0]
        target = -2
        steps = list(visualize_linear_search(array, target))
        
        # Should find -2
        last_step = steps[-1]
        assert last_step.found is True
        assert array[last_step.middle_index] == target


class TestLinearSearchVisualizationDetails:
    """Test specific visualization details for linear_search."""
    
    def test_step_descriptions_are_meaningful(self):
        """Test that step descriptions provide meaningful information."""
        array = [10, 20, 30]
        target = 20
        steps = list(visualize_linear_search(array, target))
        
        # All steps should have non-empty descriptions
        for step in steps:
            assert step.description
            assert len(step.description) > 0
    
    def test_highlighted_indices_show_current_check(self):
        """Test that highlighted indices show the element being checked."""
        array = [10, 20, 30, 40, 50]
        target = 30
        steps = list(visualize_linear_search(array, target))
        
        # Check steps (not initial or final) should highlight current index
        check_steps = [s for s in steps[1:-1] if s.found is None]
        for step in check_steps:
            # Should highlight the index being checked
            assert len(step.highlighted_indices) > 0
            # Highlighted index should match middle_index
            assert step.middle_index in step.highlighted_indices
    
    def test_array_state_remains_unchanged(self):
        """Test that array state remains unchanged throughout search."""
        array = [10, 20, 30, 40, 50]
        target = 30
        original = array.copy()
        steps = list(visualize_linear_search(array, target))
        
        # All steps should have same array state
        for step in steps:
            assert step.array_state == original
    
    def test_search_range_covers_entire_array(self):
        """Test that search range covers the entire array."""
        array = [10, 20, 30, 40, 50]
        target = 30
        steps = list(visualize_linear_search(array, target))
        
        # All steps should have search range covering entire array
        for step in steps:
            assert step.search_range == (0, len(array) - 1)
    
    def test_middle_index_progresses_sequentially(self):
        """Test that middle_index progresses from 0 to n-1."""
        array = [10, 20, 30, 40, 50]
        target = 99  # Not in array to check all elements
        steps = list(visualize_linear_search(array, target))
        
        # Filter check steps
        check_steps = [s for s in steps if s.found is None and s.highlighted_indices]
        
        # Middle index should progress: 0, 1, 2, 3, 4
        for i, step in enumerate(check_steps):
            assert step.middle_index == i
    
    def test_found_flag_progression(self):
        """Test that found flag progresses correctly: None -> True/False."""
        array = [10, 20, 30]
        target = 20
        steps = list(visualize_linear_search(array, target))
        
        # Initial and check steps should have found=None
        for step in steps[:-1]:
            if step.description.startswith("Starting"):
                assert step.found is None
            elif "Checking" in step.description:
                assert step.found is None
        
        # Last step should have found=True or False
        assert steps[-1].found in [True, False]
    
    def test_step_numbers_are_sequential(self):
        """Test that step numbers are sequential starting from 0."""
        array = [10, 20, 30, 40, 50]
        target = 30
        steps = list(visualize_linear_search(array, target))
        
        for i, step in enumerate(steps):
            assert step.step_number == i


class TestLinearSearchAlgorithmCorrectness:
    """Test algorithm correctness for linear_search."""
    
    def test_checks_every_element_when_not_found(self):
        """Test that linear search checks every element when target not found."""
        array = [10, 20, 30, 40, 50]
        target = 99
        steps = list(visualize_linear_search(array, target))
        
        # Should have check steps for each element
        check_steps = [s for s in steps if "Checking" in s.description]
        assert len(check_steps) == len(array)
    
    def test_stops_immediately_when_found(self):
        """Test that linear search stops as soon as target is found."""
        array = [10, 20, 30, 40, 50]
        target = 20  # At index 1
        steps = list(visualize_linear_search(array, target))
        
        # Should check indices 0 and 1, then stop
        check_steps = [s for s in steps if "Checking" in s.description]
        assert len(check_steps) == 2  # Checked index 0 and 1
    
    def test_time_complexity_linear(self):
        """Test that number of checks is proportional to array size."""
        # For target not in array, should check all n elements
        for n in [5, 10, 15]:
            array = list(range(n))
            target = -1  # Not in array
            steps = list(visualize_linear_search(array, target))
            
            check_steps = [s for s in steps if "Checking" in s.description]
            assert len(check_steps) == n
    
    def test_works_with_strings(self):
        """Test linear_search works with string elements."""
        array = ["apple", "banana", "cherry", "date"]
        target = "cherry"
        steps = list(visualize_linear_search(array, target))
        
        last_step = steps[-1]
        assert last_step.found is True
        assert array[last_step.middle_index] == target
    
    def test_works_with_floats(self):
        """Test linear_search works with float elements."""
        array = [1.5, 2.7, 3.9, 4.2, 5.8]
        target = 3.9
        steps = list(visualize_linear_search(array, target))
        
        last_step = steps[-1]
        assert last_step.found is True
        assert array[last_step.middle_index] == target
    
    def test_preserves_original_array(self):
        """Test that linear_search does not modify the original array."""
        array = [10, 20, 30, 40, 50]
        original = array.copy()
        target = 30
        
        steps = list(visualize_linear_search(array, target))
        
        # Original array should be unchanged
        assert array == original


