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
    to end until the target is found or the array is exhausted. This algorithm
    works on both sorted and unsorted arrays.
    
    Algorithm:
    1. Start at the first element (index 0)
    2. Compare current element with target
    3. If match found, return the index
    4. If not found, move to next element
    5. Repeat until target found or end of array reached
    
    Args:
        array: List to search (can be sorted or unsorted)
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
    
    Time Complexity: O(n) - must check each element in worst case
    Space Complexity: O(1) - only uses constant extra space
    """
    n = len(array)
    comparisons = 0
    step_num = 0
    
    # Handle empty array
    if n == 0:
        yield SearchStep(
            step_number=step_num,
            description=f"Array is empty, {target} not found",
            array_state=[],
            highlighted_indices=[],
            search_range=(0, 0),
            middle_index=-1,
            found=False
        )
        return
    
    # Initial state
    yield SearchStep(
        step_number=step_num,
        description=f"Starting linear search for {target}",
        array_state=array.copy(),
        highlighted_indices=[],
        search_range=(0, n - 1),
        middle_index=0,
        found=None
    )
    step_num += 1
    
    # Sequential search through array
    for i in range(n):
        comparisons += 1
        
        # Check current element
        yield SearchStep(
            step_number=step_num,
            description=f"Checking index {i}: {array[i]} == {target}?",
            array_state=array.copy(),
            highlighted_indices=[i],
            search_range=(0, n - 1),
            middle_index=i,
            found=None
        )
        step_num += 1
        
        # Target found
        if array[i] == target:
            yield SearchStep(
                step_number=step_num,
                description=f"Found {target} at index {i}!",
                array_state=array.copy(),
                highlighted_indices=[i],
                search_range=(0, n - 1),
                middle_index=i,
                found=True
            )
            return
    
    # Target not found
    yield SearchStep(
        step_number=step_num,
        description=f"{target} not found in array",
        array_state=array.copy(),
        highlighted_indices=[],
        search_range=(0, n - 1),
        middle_index=-1,
        found=False
    )


def visualize_jump_search(array: List[Any], target: Any) -> Iterator[SearchStep]:
    """
    Generate jump search visualization steps.
    
    Jump search works on sorted arrays by jumping ahead by fixed steps (√n)
    until finding a block where the target might be, then performing linear
    search within that block. This algorithm combines the efficiency of block
    jumping with the simplicity of linear search.
    
    Algorithm:
    1. Calculate jump size as √n (square root of array length)
    2. Jump ahead by jump_size until finding element >= target
    3. Perform linear search in the identified block
    4. Return found index or not found
    
    Args:
        array: Sorted list to search (MUST be sorted)
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
    
    Time Complexity: O(√n) - jumps √n times, then linear search √n elements
    Space Complexity: O(1) - only uses constant extra space
    
    Note:
        Jump search requires a sorted array. If the array is not sorted,
        a ValueError will be raised. Use linear_search for unsorted arrays.
    """
    import math
    
    n = len(array)
    step_num = 0
    
    # Handle empty array
    if n == 0:
        yield SearchStep(
            step_number=step_num,
            description=f"Array is empty, {target} not found",
            array_state=[],
            highlighted_indices=[],
            search_range=(0, 0),
            middle_index=-1,
            found=False
        )
        return
    
    # Validate array is sorted
    for i in range(len(array) - 1):
        if array[i] > array[i + 1]:
            raise ValueError(
                f"Jump search requires a sorted array. "
                f"Array is not sorted at indices {i} and {i + 1}: "
                f"{array[i]} > {array[i + 1]}. "
                f"Please sort the array first or use linear_search."
            )
    
    # Calculate jump size
    jump_size = int(math.sqrt(n))
    
    # Initial state - show jump size calculation
    yield SearchStep(
        step_number=step_num,
        description=f"Starting jump search for {target}, jump size: {jump_size} (√{n})",
        array_state=array.copy(),
        highlighted_indices=[],
        search_range=(0, n - 1),
        middle_index=0,
        found=None,
        jump_size=jump_size,
        block_start=0
    )
    step_num += 1
    
    # Jump through blocks
    prev = 0
    while prev < n and array[min(prev + jump_size, n) - 1] < target:
        jump_index = min(prev + jump_size, n) - 1
        
        yield SearchStep(
            step_number=step_num,
            description=f"Jumping to index {jump_index}: {array[jump_index]} < {target}, continue jumping",
            array_state=array.copy(),
            highlighted_indices=[jump_index],
            search_range=(prev, jump_index),
            middle_index=jump_index,
            found=None,
            jump_size=jump_size,
            block_start=prev
        )
        step_num += 1
        prev += jump_size
        
        # Check if we've jumped past the end
        if prev >= n:
            break
    
    # Determine the block to search
    block_end = min(prev + jump_size, n)
    
    # Show the identified block
    if prev < n:
        yield SearchStep(
            step_number=step_num,
            description=f"Block identified: indices {prev} to {block_end - 1}, performing linear search",
            array_state=array.copy(),
            highlighted_indices=list(range(prev, block_end)),
            search_range=(prev, block_end - 1),
            middle_index=prev,
            found=None,
            jump_size=jump_size,
            block_start=prev
        )
        step_num += 1
    
    # Linear search within the identified block
    for i in range(prev, block_end):
        yield SearchStep(
            step_number=step_num,
            description=f"Checking index {i}: {array[i]} == {target}?",
            array_state=array.copy(),
            highlighted_indices=[i],
            search_range=(prev, block_end - 1),
            middle_index=i,
            found=None,
            jump_size=jump_size,
            block_start=prev
        )
        step_num += 1
        
        # Target found
        if array[i] == target:
            yield SearchStep(
                step_number=step_num,
                description=f"Found {target} at index {i}!",
                array_state=array.copy(),
                highlighted_indices=[i],
                search_range=(prev, block_end - 1),
                middle_index=i,
                found=True,
                jump_size=jump_size,
                block_start=prev
            )
            return
        
        # Target is smaller than current element (array is sorted)
        if array[i] > target:
            break
    
    # Target not found
    yield SearchStep(
        step_number=step_num,
        description=f"{target} not found in array",
        array_state=array.copy(),
        highlighted_indices=[],
        search_range=(prev, block_end - 1),
        middle_index=-1,
        found=False,
        jump_size=jump_size,
        block_start=prev
    )
