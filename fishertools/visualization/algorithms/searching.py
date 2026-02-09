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

    Examples:
        Basic usage - search for an element:

        >>> from fishertools.visualization.algorithms import visualize_linear_search
        >>> array = [64, 34, 25, 12, 22, 11, 90]
        >>> target = 22
        >>> steps = list(visualize_linear_search(array, target))
        >>> print(f"Searched in {len(steps)} steps")
        >>> if steps[-1].found:
        ...     print(f"Found at index: {steps[-1].middle_index}")
        Searched in 7 steps
        Found at index: 4

        Searching unsorted data:

        >>> unsorted = [90, 11, 22, 12, 25, 34, 64]
        >>> target = 12
        >>> steps = list(visualize_linear_search(unsorted, target))
        >>> final_step = steps[-1]
        >>> if final_step.found:
        ...     print(f"Found {target} at index {final_step.middle_index}")
        ...     print(f"Took {len(steps)} steps")
        Found 12 at index 3
        Took 5 steps

        Element not found:

        >>> array = [1, 2, 3, 4, 5]
        >>> target = 10
        >>> steps = list(visualize_linear_search(array, target))
        >>> if not steps[-1].found:
        ...     print(f"{target} not found in array")
        ...     print(f"Checked all {len(array)} elements")
        10 not found in array
        Checked all 5 elements

        Tracking the search process:

        >>> array = [5, 2, 8, 1, 9]
        >>> target = 1
        >>> for step in visualize_linear_search(array, target):
        ...     if step.found is None:  # Still searching
        ...         print(f"Checking index {step.middle_index}: {array[step.middle_index]}")
        ...     elif step.found:
        ...         print(f"Found at index {step.middle_index}!")
        Checking index 0: 5
        Checking index 1: 2
        Checking index 2: 8
        Checking index 3: 1
        Found at index 3!

        Comparing with binary search:

        >>> from fishertools.visualization import AlgorithmVisualizer
        >>> visualizer = AlgorithmVisualizer()
        >>>
        >>> # Linear search on unsorted array
        >>> unsorted = [64, 34, 25, 12, 22, 11, 90]
        >>> linear_result = visualizer.visualize_search(unsorted, 11, 'linear_search')
        >>> print(f"Linear search steps: {len(linear_result.steps)}")
        >>>
        >>> # Binary search requires sorted array
        >>> sorted_array = sorted(unsorted)
        >>> binary_result = visualizer.visualize_search(sorted_array, 11, 'binary_search')
        >>> print(f"Binary search steps: {len(binary_result.steps)}")

        Using with AlgorithmVisualizer:

        >>> from fishertools.visualization import AlgorithmVisualizer
        >>> visualizer = AlgorithmVisualizer()
        >>> result = visualizer.visualize_search([64, 34, 25, 12, 22], 25, 'linear_search')
        >>> print(f"Algorithm: {result.algorithm_name}")
        >>> print(f"Found: {result.steps[-1].found}")
        >>> print(f"Index: {result.steps[-1].middle_index}")

    Time Complexity: O(n) - must check each element in worst case
    Space Complexity: O(1) - only uses constant extra space

    Note:
        Linear search is the only search algorithm that works on unsorted data.
        It's simple and efficient for small arrays or when the target is likely
        to be near the beginning.
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
            found=False,
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
        found=None,
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
            found=None,
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
                found=True,
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
        found=False,
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

    Examples:
        Basic usage - search in sorted array:

        >>> from fishertools.visualization.algorithms import visualize_jump_search
        >>> array = [11, 12, 22, 25, 34, 64, 90]  # Must be sorted
        >>> target = 22
        >>> steps = list(visualize_jump_search(array, target))
        >>> print(f"Searched in {len(steps)} steps")
        >>> if steps[-1].found:
        ...     print(f"Found at index: {steps[-1].middle_index}")
        Searched in 5 steps
        Found at index: 2

        Understanding jump size:

        >>> array = list(range(0, 100, 2))  # [0, 2, 4, ..., 98]
        >>> target = 50
        >>> steps = list(visualize_jump_search(array, target))
        >>> first_step = steps[0]
        >>> print(f"Array length: {len(array)}")
        >>> print(f"Jump size: {first_step.jump_size}")
        >>> print(f"Jump size = √{len(array)} = {first_step.jump_size}")
        Array length: 50
        Jump size: 7
        Jump size = √50 = 7

        Tracking jump operations:

        >>> array = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
        >>> target = 15
        >>> for step in visualize_jump_search(array, target):
        ...     if 'Jumping' in step.description:
        ...         print(f"{step.description}")
        ...         print(f"  Block: [{step.block_start}:{step.search_range[1]}]")
        Jumping to index 2: 5 < 15, continue jumping
          Block: [0:2]
        Jumping to index 5: 11 < 15, continue jumping
          Block: [3:5]
        ...

        Element not found:

        >>> array = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> target = 10
        >>> steps = list(visualize_jump_search(array, target))
        >>> if not steps[-1].found:
        ...     print(f"{target} not found in array")
        10 not found in array

        Error handling - unsorted array:

        >>> unsorted = [5, 2, 8, 1, 9]
        >>> try:
        ...     steps = list(visualize_jump_search(unsorted, 5))
        ... except ValueError as e:
        ...     print(f"Error: {e}")
        Error: Jump search requires a sorted array...

        Comparing with linear search:

        >>> from fishertools.visualization.algorithms import visualize_linear_search
        >>> sorted_array = list(range(1, 101))  # 1 to 100
        >>> target = 87
        >>>
        >>> jump_steps = list(visualize_jump_search(sorted_array, target))
        >>> linear_steps = list(visualize_linear_search(sorted_array, target))
        >>>
        >>> print(f"Jump search: {len(jump_steps)} steps")
        >>> print(f"Linear search: {len(linear_steps)} steps")
        >>> # Jump search is much faster on large sorted arrays!

        Using with AlgorithmVisualizer:

        >>> from fishertools.visualization import AlgorithmVisualizer
        >>> visualizer = AlgorithmVisualizer()
        >>> sorted_array = [11, 12, 22, 25, 34, 64, 90]
        >>> result = visualizer.visualize_search(sorted_array, 34, 'jump_search')
        >>> print(f"Algorithm: {result.algorithm_name}")
        >>> print(f"Found: {result.steps[-1].found}")
        >>> print(f"Index: {result.steps[-1].middle_index}")

        Educational use - understanding block search:

        >>> array = list(range(0, 50, 2))  # [0, 2, 4, ..., 48]
        >>> target = 30
        >>> for step in visualize_jump_search(array, target):
        ...     if step.jump_size and step.block_start is not None:
        ...         if 'Block identified' in step.description:
        ...             print(f"Target must be in block starting at {step.block_start}")
        ...             print(f"Block size: {step.jump_size}")
        Target must be in block starting at 10
        Block size: 5

    Time Complexity: O(√n) - jumps √n times, then linear search √n elements
    Space Complexity: O(1) - only uses constant extra space

    Note:
        Jump search requires a sorted array. If the array is not sorted,
        a ValueError will be raised. Use linear_search for unsorted arrays.
        Jump search is optimal when jumping backwards is costly, as it only
        jumps forward.
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
            found=False,
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
        block_start=0,
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
            block_start=prev,
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
            block_start=prev,
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
            block_start=prev,
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
                block_start=prev,
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
        block_start=prev,
    )
