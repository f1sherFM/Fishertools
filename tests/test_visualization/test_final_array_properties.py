"""
Property-based tests for final_array attribute.

Feature: fishertools-v0.4.0
These tests validate the correctness properties of the final_array attribute
in AlgorithmVisualization.
"""

import pytest
from hypothesis import given, strategies as st

from fishertools.visualization.algorithm_visualizer import AlgorithmVisualizer
from fishertools.visualization.models import (
    AlgorithmVisualization,
    AlgorithmStep,
    SortingStep,
    SearchStep,
)


class TestFinalArrayProperty:
    """
    Property 21: Final array matches last step
    
    For any algorithm visualization with steps, the final_array attribute
    should match the array_state from the last step.
    
    Validates: Requirements 9.1, 9.2, 9.3
    """
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=20))
    def test_final_array_matches_last_step_sorting(self, array):
        """Test that final_array matches last step for sorting algorithms."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array, algorithm='bubble_sort')
        
        if result.steps:
            # final_array should match the array_state of the last step
            last_step = result.steps[-1]
            assert hasattr(last_step, 'array_state')
            assert result.final_array == last_step.array_state, \
                f"final_array {result.final_array} != last step {last_step.array_state}"
        else:
            # If no steps, final_array should match input_data
            assert result.final_array == result.input_data
    
    @given(
        st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20),
        st.integers(min_value=-100, max_value=100)
    )
    def test_final_array_matches_last_step_search(self, array, target):
        """Test that final_array matches last step for search algorithms."""
        visualizer = AlgorithmVisualizer()
        sorted_array = sorted(array)
        result = visualizer.visualize_search(sorted_array, target, algorithm='binary_search')
        
        if result.steps:
            # final_array should match the array_state of the last step
            last_step = result.steps[-1]
            assert hasattr(last_step, 'array_state')
            assert result.final_array == last_step.array_state, \
                f"final_array {result.final_array} != last step {last_step.array_state}"
        else:
            # If no steps, final_array should match input_data
            assert result.final_array == result.input_data


class TestFinalArrayImmutability:
    """
    Property 22: Final array is a copy (immutability)
    
    The final_array attribute should be a copy of the array state, not a reference,
    to prevent mutation of the visualization result.
    
    Validates: Requirements 9.1, 9.2
    """
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=1, max_size=20))
    def test_final_array_is_copy_not_reference(self, array):
        """Test that final_array is a copy, not a reference to the last step."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting(array, algorithm='bubble_sort')
        
        if result.steps:
            last_step = result.steps[-1]
            
            # Modify final_array
            original_final = result.final_array.copy()
            result.final_array.append(999)
            
            # Last step's array_state should not be affected
            assert last_step.array_state != result.final_array, \
                "final_array is not a copy - modifying it affected the last step"
            
            # Restore for next assertion
            result.final_array.pop()
            
            # Modify last step's array_state
            last_step.array_state.append(888)
            
            # final_array should not be affected (it was computed in __post_init__)
            # Note: This tests that final_array was created as a copy
            assert result.final_array == original_final, \
                "final_array was affected by modifying last step's array_state"
    
    @given(st.lists(st.integers(min_value=-100, max_value=100), min_size=0, max_size=20))
    def test_final_array_empty_steps_returns_copy(self, array):
        """Test that final_array returns a copy of input_data when no steps exist."""
        # Create visualization with no steps
        viz = AlgorithmVisualization(
            steps=[],
            statistics={},
            algorithm_name="test",
            input_data=array
        )
        
        # Modify final_array
        original_input = viz.input_data.copy()
        viz.final_array.append(999)
        
        # input_data should not be affected
        assert viz.input_data == original_input, \
            "final_array is not a copy - modifying it affected input_data"


