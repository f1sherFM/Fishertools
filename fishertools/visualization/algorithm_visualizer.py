"""
Algorithm visualization for educational purposes.

This module provides step-by-step visualization of common algorithms like
sorting and searching to help users understand how they work.
"""

from __future__ import annotations

from typing import Any, Iterator

from .algorithms.searching import (
    visualize_jump_search,
    visualize_linear_search,
)
from .algorithms.sorting import (
    visualize_insertion_sort,
    visualize_merge_sort,
    visualize_quick_sort,
    visualize_selection_sort,
)
from .models import (
    AlgorithmVisualization,
    SearchStep,
    SortingStep,
)


class AlgorithmVisualizer:
    """
    Visualizes common algorithms step by step.

    This class provides educational visualizations of sorting and searching
    algorithms, showing each step of the algorithm execution with statistics.

    Supported sorting algorithms:
    - bubble_sort: Simple comparison-based sorting with adjacent swaps
    - quick_sort: Divide-and-conquer sorting using partitioning
    - merge_sort: Divide-and-conquer sorting with merging
    - insertion_sort: Build sorted array by inserting elements
    - selection_sort: Repeatedly select minimum element

    Supported search algorithms:
    - binary_search: Efficient search in sorted arrays (O(log n))
    - linear_search: Sequential search in any array (O(n))
    - jump_search: Block-based search in sorted arrays (O(√n))
    """

    def __init__(self, language: str = "auto"):
        """
        Initialize the algorithm visualizer.

        Args:
            language: Language for step descriptions ('en', 'ru', 'auto').
                     Currently stored for future multilingual support.
        """
        self.language = language
        self.supported_algorithms = {
            "bubble_sort": self._visualize_bubble_sort,
            "binary_search": self._visualize_binary_search,
            "quick_sort": visualize_quick_sort,
            "merge_sort": visualize_merge_sort,
            "insertion_sort": visualize_insertion_sort,
            "selection_sort": visualize_selection_sort,
            "linear_search": visualize_linear_search,
            "jump_search": visualize_jump_search,
        }

    def visualize_sorting(
        self, array: list[Any], algorithm: str = "bubble_sort", step_delay: float = 0.5
    ) -> AlgorithmVisualization:
        """
        Visualize sorting algorithms step by step.

        This method generates a step-by-step visualization of a sorting
        algorithm, showing comparisons, swaps, and the evolving array state.

        Args:
            array: Array to sort
            algorithm: Sorting algorithm name ('bubble_sort', etc.)
            step_delay: Delay between steps in seconds (for display)

        Returns:
            AlgorithmVisualization with all steps and statistics

        Raises:
            ValueError: If algorithm is not supported
        """
        if algorithm not in self.supported_algorithms:
            supported = ", ".join(self.supported_algorithms.keys())
            raise ValueError(
                f"Unsupported algorithm '{algorithm}'. "
                f"Supported algorithms: {supported}"
            )

        # Make a copy of the array to avoid modifying the original
        array_copy = list(array)

        # Generate steps using the appropriate algorithm
        visualizer_func = self.supported_algorithms[algorithm]
        steps = list(visualizer_func(array_copy))  # type: ignore[operator]

        # Extract statistics from the final step
        statistics = {}
        if steps and isinstance(steps[-1], SortingStep):
            final_step = steps[-1]
            statistics = {
                "comparisons": final_step.comparisons_count,
                "swaps": final_step.swaps_count,
                "steps": len(steps),
            }

        return AlgorithmVisualization(
            steps=steps,
            statistics=statistics,
            algorithm_name=algorithm,
            input_data=list(array),
        )

    def visualize_search(
        self,
        array: list[Any],
        target: Any,
        algorithm: str = "binary_search",
        step_delay: float = 0.5,
    ) -> AlgorithmVisualization:
        """
        Visualize search algorithms step by step.

        This method generates a step-by-step visualization of a search
        algorithm, showing the search range, comparisons, and progress.

        Args:
            array: Array to search in
            target: Value to search for
            algorithm: Search algorithm name ('binary_search', etc.)
            step_delay: Delay between steps in seconds (for display)

        Returns:
            AlgorithmVisualization with all steps and statistics

        Raises:
            ValueError: If algorithm is not supported
        """
        if algorithm not in self.supported_algorithms:
            supported = ", ".join(self.supported_algorithms.keys())
            raise ValueError(
                f"Unsupported algorithm '{algorithm}'. "
                f"Supported algorithms: {supported}"
            )

        # Make a copy of the array to avoid modifying the original
        array_copy = list(array)

        # Generate steps using the appropriate algorithm
        visualizer_func = self.supported_algorithms[algorithm]
        steps = list(visualizer_func(array_copy, target))  # type: ignore[operator]

        # Extract statistics from the steps
        statistics = {
            "comparisons": len(steps),
            "steps": len(steps),
            "found": (
                steps[-1].found if steps and hasattr(steps[-1], "found") else False
            ),
        }

        return AlgorithmVisualization(
            steps=steps,
            statistics=statistics,
            algorithm_name=algorithm,
            input_data=list(array),
        )

    def _visualize_bubble_sort(self, array: list[Any]) -> Iterator[SortingStep]:
        """
        Generate bubble sort visualization steps.

        Bubble sort repeatedly steps through the list, compares adjacent elements
        and swaps them if they are in the wrong order. The pass through the list
        is repeated until the list is sorted.

        Args:
            array: Array to sort (will be modified in place)

        Yields:
            SortingStep objects representing each step
        """
        n = len(array)
        comparisons = 0
        swaps = 0
        step_num = 0

        # Initial state
        yield SortingStep(
            step_number=step_num,
            description=f"Initial array: {array}",
            array_state=array.copy(),
            highlighted_indices=[],
            comparisons_count=comparisons,
            swaps_count=swaps,
        )
        step_num += 1

        # Bubble sort algorithm
        for i in range(n):
            swapped = False

            for j in range(0, n - i - 1):
                # Compare adjacent elements
                comparisons += 1

                yield SortingStep(
                    step_number=step_num,
                    description=f"Comparing {array[j]} and {array[j + 1]}",
                    array_state=array.copy(),
                    highlighted_indices=[j, j + 1],
                    comparison_indices=(j, j + 1),
                    swap_occurred=False,
                    comparisons_count=comparisons,
                    swaps_count=swaps,
                )
                step_num += 1

                # Swap if needed
                if array[j] > array[j + 1]:
                    array[j], array[j + 1] = array[j + 1], array[j]
                    swaps += 1
                    swapped = True

                    yield SortingStep(
                        step_number=step_num,
                        description=f"Swapped {array[j + 1]} and {array[j]}",
                        array_state=array.copy(),
                        highlighted_indices=[j, j + 1],
                        comparison_indices=(j, j + 1),
                        swap_occurred=True,
                        comparisons_count=comparisons,
                        swaps_count=swaps,
                    )
                    step_num += 1

            # If no swaps occurred, array is sorted
            if not swapped:
                break

        # Final sorted state
        yield SortingStep(
            step_number=step_num,
            description=f"Array sorted: {array}",
            array_state=array.copy(),
            highlighted_indices=[],
            comparisons_count=comparisons,
            swaps_count=swaps,
        )

    def _visualize_binary_search(
        self, array: list[Any], target: Any
    ) -> Iterator[SearchStep]:
        """
        Generate binary search visualization steps.

        Binary search finds the position of a target value within a sorted array
        by repeatedly dividing the search interval in half.

        Args:
            array: Sorted array to search in
            target: Value to search for

        Yields:
            SearchStep objects representing each step
        """
        left = 0
        right = len(array) - 1
        step_num = 0

        # Initial state
        yield SearchStep(
            step_number=step_num,
            description=f"Searching for {target} in array: {array}",
            array_state=array.copy(),
            highlighted_indices=[],
            search_range=(left, right),
            middle_index=0,
            found=None,
        )
        step_num += 1

        # Binary search algorithm
        while left <= right:
            mid = (left + right) // 2

            # Show current search range and middle element
            yield SearchStep(
                step_number=step_num,
                description=f"Checking middle element at index {mid}: {array[mid]}",
                array_state=array.copy(),
                highlighted_indices=[mid],
                search_range=(left, right),
                middle_index=mid,
                found=None,
            )
            step_num += 1

            # Check if target is found
            if array[mid] == target:
                yield SearchStep(
                    step_number=step_num,
                    description=f"Found {target} at index {mid}!",
                    array_state=array.copy(),
                    highlighted_indices=[mid],
                    search_range=(left, right),
                    middle_index=mid,
                    found=True,
                )
                return

            # Decide which half to search
            elif array[mid] < target:
                yield SearchStep(
                    step_number=step_num,
                    description=f"{array[mid]} < {target}, searching right half",
                    array_state=array.copy(),
                    highlighted_indices=[mid],
                    search_range=(left, right),
                    middle_index=mid,
                    found=None,
                )
                step_num += 1
                left = mid + 1
            else:
                yield SearchStep(
                    step_number=step_num,
                    description=f"{array[mid]} > {target}, searching left half",
                    array_state=array.copy(),
                    highlighted_indices=[mid],
                    search_range=(left, right),
                    middle_index=mid,
                    found=None,
                )
                step_num += 1
                right = mid - 1

        # Target not found
        yield SearchStep(
            step_number=step_num,
            description=f"{target} not found in array",
            array_state=array.copy(),
            highlighted_indices=[],
            search_range=(left, right),
            middle_index=-1,
            found=False,
        )
