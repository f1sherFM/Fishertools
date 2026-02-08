"""
Sorting algorithm implementations with step-by-step visualization.

This module provides implementations of common sorting algorithms that generate
visualization steps for educational purposes. Each algorithm yields SortingStep
objects that can be used to understand how the algorithm works.
"""

from typing import Any, Iterator, List

from ..models import SortingStep


def visualize_quick_sort(array: List[Any]) -> Iterator[SortingStep]:
    """
    Generate quick sort visualization steps.
    
    Quick sort uses a divide-and-conquer strategy:
    1. Choose a pivot element (last element)
    2. Partition array so elements < pivot are left, > pivot are right
    3. Recursively sort left and right partitions
    
    Args:
        array: List to sort
    
    Yields:
        SortingStep objects showing each step of the algorithm
    
    Example:
        >>> from fishertools.visualization.algorithms import visualize_quick_sort
        >>> array = [64, 34, 25, 12, 22, 11, 90]
        >>> steps = list(visualize_quick_sort(array))
        >>> print(f"Sorted in {len(steps)} steps")
        >>> print(f"Final array: {steps[-1].array_state if steps else array}")
    
    Time Complexity: O(n log n) average, O(n²) worst case
    Space Complexity: O(log n) for recursion stack
    """
    if not array:
        return
    
    # Create a working copy to avoid modifying the input
    arr = array.copy()
    comparisons = 0
    swaps = 0
    step_num = 0
    
    def partition(low: int, high: int) -> int:
        """Partition the array around a pivot element."""
        nonlocal comparisons, swaps, step_num
        
        pivot = arr[high]
        
        # Show pivot selection
        yield SortingStep(
            step_number=step_num,
            description=f"Select pivot: {pivot} at index {high}",
            array_state=arr.copy(),
            highlighted_indices=[high],
            partition_index=high,
            comparisons_count=comparisons,
            swaps_count=swaps
        )
        step_num += 1
        
        i = low - 1
        
        for j in range(low, high):
            comparisons += 1
            
            # Show comparison
            yield SortingStep(
                step_number=step_num,
                description=f"Compare {arr[j]} with pivot {pivot}",
                array_state=arr.copy(),
                highlighted_indices=[j, high],
                comparison_indices=(j, high),
                partition_index=high,
                comparisons_count=comparisons,
                swaps_count=swaps
            )
            step_num += 1
            
            if arr[j] <= pivot:
                i += 1
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    swaps += 1
                    
                    # Show swap
                    yield SortingStep(
                        step_number=step_num,
                        description=f"Swap {arr[i]} and {arr[j]} (elements <= pivot)",
                        array_state=arr.copy(),
                        highlighted_indices=[i, j],
                        swap_occurred=True,
                        partition_index=high,
                        comparisons_count=comparisons,
                        swaps_count=swaps
                    )
                    step_num += 1
        
        # Place pivot in correct position
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        swaps += 1
        
        # Show pivot placement
        yield SortingStep(
            step_number=step_num,
            description=f"Place pivot {pivot} at index {i + 1}",
            array_state=arr.copy(),
            highlighted_indices=[i + 1],
            swap_occurred=True,
            partition_index=i + 1,
            comparisons_count=comparisons,
            swaps_count=swaps
        )
        step_num += 1
        
        return i + 1
    
    def quick_sort_recursive(low: int, high: int):
        """Recursively sort the array using quick sort."""
        if low < high:
            # Partition and get pivot index
            pivot_idx = yield from partition(low, high)
            
            # Recursively sort left partition
            yield from quick_sort_recursive(low, pivot_idx - 1)
            
            # Recursively sort right partition
            yield from quick_sort_recursive(pivot_idx + 1, high)
    
    # Start the recursive sorting
    yield from quick_sort_recursive(0, len(arr) - 1)
    
    # Final step showing sorted array
    yield SortingStep(
        step_number=step_num,
        description="Quick sort complete",
        array_state=arr.copy(),
        highlighted_indices=[],
        comparisons_count=comparisons,
        swaps_count=swaps
    )


def visualize_merge_sort(array: List[Any]) -> Iterator[SortingStep]:
    """
    Generate merge sort visualization steps.
    
    Merge sort uses divide-and-conquer:
    1. Divide array into two halves
    2. Recursively sort each half
    3. Merge the sorted halves
    
    Args:
        array: List to sort
    
    Yields:
        SortingStep objects showing each step of the algorithm
    
    Example:
        >>> from fishertools.visualization.algorithms import visualize_merge_sort
        >>> array = [64, 34, 25, 12, 22, 11, 90]
        >>> steps = list(visualize_merge_sort(array))
        >>> print(f"Sorted in {len(steps)} steps")
        >>> print(f"Final array: {steps[-1].array_state if steps else array}")
    
    Time Complexity: O(n log n) guaranteed
    Space Complexity: O(n) for temporary arrays
    """
    if not array:
        # Handle empty array case
        yield SortingStep(
            step_number=0,
            description="Empty array - already sorted",
            array_state=[],
            highlighted_indices=[],
            comparisons_count=0,
            swaps_count=0
        )
        return
    
    # Create a working copy to avoid modifying the input
    arr = array.copy()
    comparisons = 0
    step_num = 0
    
    def merge(left: int, mid: int, right: int):
        """Merge two sorted subarrays."""
        nonlocal comparisons, step_num
        
        # Create temporary arrays for left and right halves
        left_arr = arr[left:mid + 1]
        right_arr = arr[mid + 1:right + 1]
        
        # Show merge start
        yield SortingStep(
            step_number=step_num,
            description=f"Merging subarrays [{left}:{mid}] and [{mid+1}:{right}]",
            array_state=arr.copy(),
            highlighted_indices=list(range(left, right + 1)),
            merge_range=(left, right),
            comparisons_count=comparisons,
            swaps_count=0
        )
        step_num += 1
        
        i = j = 0
        k = left
        
        # Merge the two arrays
        while i < len(left_arr) and j < len(right_arr):
            comparisons += 1
            
            if left_arr[i] <= right_arr[j]:
                arr[k] = left_arr[i]
                
                # Show element placement from left array
                yield SortingStep(
                    step_number=step_num,
                    description=f"Place {arr[k]} from left subarray at index {k}",
                    array_state=arr.copy(),
                    highlighted_indices=[k],
                    merge_range=(left, right),
                    comparisons_count=comparisons,
                    swaps_count=0
                )
                step_num += 1
                i += 1
            else:
                arr[k] = right_arr[j]
                
                # Show element placement from right array
                yield SortingStep(
                    step_number=step_num,
                    description=f"Place {arr[k]} from right subarray at index {k}",
                    array_state=arr.copy(),
                    highlighted_indices=[k],
                    merge_range=(left, right),
                    comparisons_count=comparisons,
                    swaps_count=0
                )
                step_num += 1
                j += 1
            
            k += 1
        
        # Copy remaining elements from left array
        while i < len(left_arr):
            arr[k] = left_arr[i]
            
            yield SortingStep(
                step_number=step_num,
                description=f"Copy remaining {arr[k]} from left subarray to index {k}",
                array_state=arr.copy(),
                highlighted_indices=[k],
                merge_range=(left, right),
                comparisons_count=comparisons,
                swaps_count=0
            )
            step_num += 1
            i += 1
            k += 1
        
        # Copy remaining elements from right array
        while j < len(right_arr):
            arr[k] = right_arr[j]
            
            yield SortingStep(
                step_number=step_num,
                description=f"Copy remaining {arr[k]} from right subarray to index {k}",
                array_state=arr.copy(),
                highlighted_indices=[k],
                merge_range=(left, right),
                comparisons_count=comparisons,
                swaps_count=0
            )
            step_num += 1
            j += 1
            k += 1
        
        # Show merge complete
        yield SortingStep(
            step_number=step_num,
            description=f"Merge complete for range [{left}:{right}]",
            array_state=arr.copy(),
            highlighted_indices=list(range(left, right + 1)),
            merge_range=(left, right),
            comparisons_count=comparisons,
            swaps_count=0
        )
        step_num += 1
    
    def merge_sort_recursive(left: int, right: int):
        """Recursively sort the array using merge sort."""
        nonlocal step_num
        
        if left < right:
            mid = (left + right) // 2
            
            # Show division
            yield SortingStep(
                step_number=step_num,
                description=f"Divide array at index {mid}: [{left}:{mid}] and [{mid+1}:{right}]",
                array_state=arr.copy(),
                highlighted_indices=list(range(left, right + 1)),
                merge_range=(left, right),
                comparisons_count=comparisons,
                swaps_count=0
            )
            step_num += 1
            
            # Recursively sort left half
            yield from merge_sort_recursive(left, mid)
            
            # Recursively sort right half
            yield from merge_sort_recursive(mid + 1, right)
            
            # Merge the sorted halves
            yield from merge(left, mid, right)
    
    # Start the recursive sorting
    yield from merge_sort_recursive(0, len(arr) - 1)
    
    # Final step showing sorted array
    yield SortingStep(
        step_number=step_num,
        description="Merge sort complete",
        array_state=arr.copy(),
        highlighted_indices=[],
        comparisons_count=comparisons,
        swaps_count=0
    )


def visualize_insertion_sort(array: List[Any]) -> Iterator[SortingStep]:
    """
    Generate insertion sort visualization steps.
    
    Insertion sort builds a sorted array one element at a time by inserting
    each element into its correct position in the sorted portion.
    
    Algorithm:
    1. Start with the first element as the sorted portion
    2. For each subsequent element:
       - Compare it with elements in the sorted portion (right to left)
       - Shift larger elements one position to the right
       - Insert the element at its correct position
    3. Repeat until all elements are in the sorted portion
    
    Args:
        array: List to sort
    
    Yields:
        SortingStep objects showing each step of the algorithm
    
    Example:
        >>> from fishertools.visualization.algorithms import visualize_insertion_sort
        >>> array = [64, 34, 25, 12, 22, 11, 90]
        >>> steps = list(visualize_insertion_sort(array))
        >>> print(f"Sorted in {len(steps)} steps")
        >>> print(f"Final array: {steps[-1].array_state if steps else array}")
    
    Time Complexity: O(n²) worst case, O(n) best case (already sorted)
    Space Complexity: O(1)
    """
    if not array:
        # Handle empty array case
        yield SortingStep(
            step_number=0,
            description="Empty array - already sorted",
            array_state=[],
            highlighted_indices=[],
            comparisons_count=0,
            swaps_count=0
        )
        return
    
    # Create a working copy to avoid modifying the input
    arr = array.copy()
    comparisons = 0
    insertions = 0  # Track insertions (shifts)
    step_num = 0
    
    # Initial state - first element is considered sorted
    yield SortingStep(
        step_number=step_num,
        description=f"Start: {arr[0]} is the sorted portion",
        array_state=arr.copy(),
        highlighted_indices=[0],
        comparisons_count=comparisons,
        swaps_count=insertions
    )
    step_num += 1
    
    # Iterate through the array starting from the second element
    for i in range(1, len(arr)):
        key = arr[i]
        
        # Show the element being inserted
        yield SortingStep(
            step_number=step_num,
            description=f"Insert {key} into sorted portion [0:{i}]",
            array_state=arr.copy(),
            highlighted_indices=list(range(i + 1)),  # Highlight sorted portion + current element
            comparisons_count=comparisons,
            swaps_count=insertions
        )
        step_num += 1
        
        # Find the correct position for the key in the sorted portion
        j = i - 1
        
        # Shift elements greater than key one position to the right
        while j >= 0:
            comparisons += 1
            
            # Show comparison
            yield SortingStep(
                step_number=step_num,
                description=f"Compare {key} with {arr[j]}",
                array_state=arr.copy(),
                highlighted_indices=[j, i],
                comparison_indices=(j, i),
                comparisons_count=comparisons,
                swaps_count=insertions
            )
            step_num += 1
            
            if arr[j] > key:
                # Shift element to the right
                arr[j + 1] = arr[j]
                insertions += 1
                
                # Show shift
                yield SortingStep(
                    step_number=step_num,
                    description=f"Shift {arr[j]} right to position {j + 1}",
                    array_state=arr.copy(),
                    highlighted_indices=[j, j + 1],
                    swap_occurred=True,
                    comparisons_count=comparisons,
                    swaps_count=insertions
                )
                step_num += 1
                j -= 1
            else:
                # Found the correct position
                break
        
        # Insert the key at its correct position
        arr[j + 1] = key
        
        # Show insertion
        yield SortingStep(
            step_number=step_num,
            description=f"Place {key} at position {j + 1}",
            array_state=arr.copy(),
            highlighted_indices=list(range(i + 1)),  # Highlight the now-sorted portion
            comparisons_count=comparisons,
            swaps_count=insertions
        )
        step_num += 1
    
    # Final step showing sorted array
    yield SortingStep(
        step_number=step_num,
        description="Insertion sort complete",
        array_state=arr.copy(),
        highlighted_indices=[],
        comparisons_count=comparisons,
        swaps_count=insertions
    )


def visualize_selection_sort(array: List[Any]) -> Iterator[SortingStep]:
    """
    Generate selection sort visualization steps.
    
    Selection sort repeatedly finds the minimum element from the unsorted
    portion and places it at the beginning of the unsorted portion.
    
    Algorithm:
    1. Find the minimum element in the unsorted portion
    2. Swap it with the first element of the unsorted portion
    3. Move the boundary between sorted and unsorted portions one position right
    4. Repeat until the entire array is sorted
    
    Args:
        array: List to sort
    
    Yields:
        SortingStep objects showing each step of the algorithm
    
    Example:
        >>> from fishertools.visualization.algorithms import visualize_selection_sort
        >>> array = [64, 34, 25, 12, 22, 11, 90]
        >>> steps = list(visualize_selection_sort(array))
        >>> print(f"Sorted in {len(steps)} steps")
        >>> print(f"Final array: {steps[-1].array_state if steps else array}")
    
    Time Complexity: O(n²)
    Space Complexity: O(1)
    """
    if not array:
        # Handle empty array case
        yield SortingStep(
            step_number=0,
            description="Empty array - already sorted",
            array_state=[],
            highlighted_indices=[],
            comparisons_count=0,
            swaps_count=0
        )
        return
    
    # Create a working copy to avoid modifying the input
    arr = array.copy()
    comparisons = 0
    swaps = 0
    step_num = 0
    
    # Initial state
    yield SortingStep(
        step_number=step_num,
        description="Start selection sort",
        array_state=arr.copy(),
        highlighted_indices=[],
        comparisons_count=comparisons,
        swaps_count=swaps
    )
    step_num += 1
    
    # Iterate through the array
    for i in range(len(arr)):
        # Find the minimum element in the unsorted portion
        min_idx = i
        
        # Show the start of searching for minimum
        yield SortingStep(
            step_number=step_num,
            description=f"Search for minimum in unsorted portion [{i}:{len(arr)-1}]",
            array_state=arr.copy(),
            highlighted_indices=list(range(i, len(arr))),
            comparisons_count=comparisons,
            swaps_count=swaps
        )
        step_num += 1
        
        # Search for minimum element in unsorted portion
        for j in range(i + 1, len(arr)):
            comparisons += 1
            
            # Show comparison
            yield SortingStep(
                step_number=step_num,
                description=f"Compare {arr[j]} with current minimum {arr[min_idx]}",
                array_state=arr.copy(),
                highlighted_indices=[min_idx, j],
                comparison_indices=(min_idx, j),
                comparisons_count=comparisons,
                swaps_count=swaps
            )
            step_num += 1
            
            if arr[j] < arr[min_idx]:
                # Found a new minimum
                old_min_idx = min_idx
                min_idx = j
                
                # Show new minimum found
                yield SortingStep(
                    step_number=step_num,
                    description=f"New minimum found: {arr[min_idx]} at index {min_idx}",
                    array_state=arr.copy(),
                    highlighted_indices=[old_min_idx, min_idx],
                    comparisons_count=comparisons,
                    swaps_count=swaps
                )
                step_num += 1
        
        # Swap the minimum element with the first element of unsorted portion
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1
            
            # Show swap
            yield SortingStep(
                step_number=step_num,
                description=f"Swap minimum {arr[i]} with position {i}",
                array_state=arr.copy(),
                highlighted_indices=[i, min_idx],
                swap_occurred=True,
                comparisons_count=comparisons,
                swaps_count=swaps
            )
            step_num += 1
        else:
            # Minimum is already in correct position
            yield SortingStep(
                step_number=step_num,
                description=f"Minimum {arr[i]} already at position {i}",
                array_state=arr.copy(),
                highlighted_indices=[i],
                comparisons_count=comparisons,
                swaps_count=swaps
            )
            step_num += 1
        
        # Show sorted portion growing
        yield SortingStep(
            step_number=step_num,
            description=f"Sorted portion: [0:{i}], element {arr[i]} in place",
            array_state=arr.copy(),
            highlighted_indices=list(range(i + 1)),
            comparisons_count=comparisons,
            swaps_count=swaps
        )
        step_num += 1
    
    # Final step showing sorted array
    yield SortingStep(
        step_number=step_num,
        description="Selection sort complete",
        array_state=arr.copy(),
        highlighted_indices=[],
        comparisons_count=comparisons,
        swaps_count=swaps
    )
