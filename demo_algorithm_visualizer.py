"""
Demonstration of the Algorithm Visualizer module.

This script shows how to use the algorithm visualizer to see
step-by-step execution of sorting and searching algorithms.
"""

from fishertools.visualization.algorithm_visualizer import AlgorithmVisualizer


def demo_bubble_sort():
    """Demonstrate bubble sort visualization."""
    print("=" * 60)
    print("BUBBLE SORT VISUALIZATION")
    print("=" * 60)
    
    visualizer = AlgorithmVisualizer()
    array = [5, 2, 8, 1, 9]
    
    print(f"\nOriginal array: {array}")
    result = visualizer.visualize_sorting(array, algorithm='bubble_sort')
    
    print(f"\nTotal steps: {len(result.steps)}")
    print(f"Comparisons: {result.statistics['comparisons']}")
    print(f"Swaps: {result.statistics['swaps']}")
    
    print("\nFirst few steps:")
    for step in result.steps[:5]:
        print(f"  Step {step.step_number}: {step.description}")
        print(f"    Array: {step.array_state}")
    
    print(f"\nFinal sorted array: {result.steps[-1].array_state}")


def demo_binary_search():
    """Demonstrate binary search visualization."""
    print("\n" + "=" * 60)
    print("BINARY SEARCH VISUALIZATION")
    print("=" * 60)
    
    visualizer = AlgorithmVisualizer()
    array = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    target = 13
    
    print(f"\nArray: {array}")
    print(f"Searching for: {target}")
    
    result = visualizer.visualize_search(array, target, algorithm='binary_search')
    
    print(f"\nTotal steps: {len(result.steps)}")
    print(f"Found: {result.statistics['found']}")
    
    print("\nSearch steps:")
    for step in result.steps:
        print(f"  Step {step.step_number}: {step.description}")
        if hasattr(step, 'search_range'):
            print(f"    Range: {step.search_range}, Middle: {step.middle_index}")


def demo_error_handling():
    """Demonstrate error handling for unsupported algorithms."""
    print("\n" + "=" * 60)
    print("ERROR HANDLING DEMONSTRATION")
    print("=" * 60)
    
    visualizer = AlgorithmVisualizer()
    
    try:
        result = visualizer.visualize_sorting([1, 2, 3], algorithm='quick_sort')
    except ValueError as e:
        print(f"\nCaught expected error: {e}")
    
    print(f"\nSupported algorithms: {list(visualizer.supported_algorithms.keys())}")


if __name__ == "__main__":
    demo_bubble_sort()
    demo_binary_search()
    demo_error_handling()
    
    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)
