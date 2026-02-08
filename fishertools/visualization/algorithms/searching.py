"""
Search algorithm implementations with step-by-step visualization.

This module provides implementations of common search algorithms that generate
visualization steps for educational purposes. Each algorithm yields SearchStep
objects that can be used to understand how the algorithm works.
"""

from typing import Any, Iterator, List

from ..models import SearchStep


def visualize_linear_search(array: List[Any], target: Any) -> Iterator[SearchStep]:
    """
    Generate linear search visualization steps.
    
    Linear search sequentially checks each element in the array from start
    to end until the target is found or the array is exhausted.
    
    Args:
        array: List to search
        target: Value to search for
    
    Yields:
        SearchStep objects showing each step of the algorithm
    
    Example:
        >>> from fishertools.visualization.algorithms import visualize_linear_search
        >>> array = [64, 34, 25, 12, 22, 11, 90]
        >>> target = 22
        >>> steps = list(visualize_linear_search(array, target))
        >>> print(f"Searched in {len(steps)} steps")
        >>> if steps and steps[-1].found:
        ...     print(f"Found at index: {steps[-1].middle_index}")
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    # Placeholder implementation - will be implemented in task 11
    if not array:
        yield SearchStep(
            step_number=0,
            description=f"Array is empty, {target} not found",
            array_state=[],
            highlighted_indices=[],
            search_range=(0, 0),
            middle_index=-1,
            found=False
        )
        return
    
    # Return a single step for now to maintain structure
    yield SearchStep(
        step_number=0,
        description="Linear search implementation pending",
        array_state=array.copy(),
        highlighted_indices=[],
        search_range=(0, len(array) - 1),
        middle_index=0,
        found=None
    )


def visualize_jump_search(array: List[Any], target: Any) -> Iterator[SearchStep]:
    """
    Generate jump search visualization steps.
    
    Jump search works on sorted arrays by jumping ahead by fixed steps (√n)
    until finding a block where the target might be, then performing linear
    search within that block.
    
    Args:
        array: Sorted list to search
        target: Value to search for
    
    Yields:
        SearchStep objects showing each step of the algorithm
    
    Raises:
        ValueError: If the array is not sorted
    
    Example:
        >>> from fishertools.visualization.algorithms import visualize_jump_search
        >>> array = [11, 12, 22, 25, 34, 64, 90]  # Must be sorted
        >>> target = 22
        >>> steps = list(visualize_jump_search(array, target))
        >>> print(f"Searched in {len(steps)} steps")
        >>> if steps and steps[-1].found:
        ...     print(f"Found at index: {steps[-1].middle_index}")
    
    Time Complexity: O(√n)
    Space Complexity: O(1)
    """
    # Placeholder implementation - will be implemented in task 12
    if not array:
        yield SearchStep(
            step_number=0,
            description=f"Array is empty, {target} not found",
            array_state=[],
            highlighted_indices=[],
            search_range=(0, 0),
            middle_index=-1,
            found=False
        )
        return
    
    # Return a single step for now to maintain structure
    yield SearchStep(
        step_number=0,
        description="Jump search implementation pending",
        array_state=array.copy(),
        highlighted_indices=[],
        search_range=(0, len(array) - 1),
        middle_index=0,
        found=None
    )
