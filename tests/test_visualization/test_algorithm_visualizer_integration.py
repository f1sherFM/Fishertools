"""
Integration tests for AlgorithmVisualizer with all supported algorithms.

Feature: fishertools-v0.5.2, Task 13.1
These tests validate that all sorting and search algorithms can be called
via the AlgorithmVisualizer interface and work correctly together.
"""

import pytest

from fishertools.visualization.algorithm_visualizer import AlgorithmVisualizer
from fishertools.visualization.models import AlgorithmVisualization


class TestSortingAlgorithmsIntegration:
    """
    Integration tests for all sorting algorithms via visualize_sorting().
    
    Validates: Requirements 3.1, 4.1, 5.1, 6.1
    """
    
    def test_bubble_sort_can_be_called(self):
        """Test that bubble_sort can be called via visualize_sorting()."""
        visualizer = AlgorithmVisualizer()
        array = [64, 34, 25, 12, 22, 11, 90]
        
        result = visualizer.visualize_sorting(array, algorithm='bubble_sort')
        
        assert isinstance(result, AlgorithmVisualization)
        assert result.algorithm_name == 'bubble_sort'
        assert result.final_array == sorted(array)
        assert len(result.steps) > 0
    
    def test_quick_sort_can_be_called(self):
        """Test that quick_sort can be called via visualize_sorting()."""
        visualizer = AlgorithmVisualizer()
        array = [64, 34, 25, 12, 22, 11, 90]
        
        result = visualizer.visualize_sorting(array, algorithm='quick_sort')
        
        assert isinstance(result, AlgorithmVisualization)
        assert result.algorithm_name == 'quick_sort'
        assert result.final_array == sorted(array)
        assert len(result.steps) > 0
    
    def test_merge_sort_can_be_called(self):
        """Test that merge_sort can be called via visualize_sorting()."""
        visualizer = AlgorithmVisualizer()
        array = [64, 34, 25, 12, 22, 11, 90]
        
        result = visualizer.visualize_sorting(array, algorithm='merge_sort')
        
        assert isinstance(result, AlgorithmVisualization)
        assert result.algorithm_name == 'merge_sort'
        assert result.final_array == sorted(array)
        assert len(result.steps) > 0
    
    def test_insertion_sort_can_be_called(self):
        """Test that insertion_sort can be called via visualize_sorting()."""
        visualizer = AlgorithmVisualizer()
        array = [64, 34, 25, 12, 22, 11, 90]
        
        result = visualizer.visualize_sorting(array, algorithm='insertion_sort')
        
        assert isinstance(result, AlgorithmVisualization)
        assert result.algorithm_name == 'insertion_sort'
        assert result.final_array == sorted(array)
        assert len(result.steps) > 0
    
    def test_selection_sort_can_be_called(self):
        """Test that selection_sort can be called via visualize_sorting()."""
        visualizer = AlgorithmVisualizer()
        array = [64, 34, 25, 12, 22, 11, 90]
        
        result = visualizer.visualize_sorting(array, algorithm='selection_sort')
        
        assert isinstance(result, AlgorithmVisualization)
        assert result.algorithm_name == 'selection_sort'
        assert result.final_array == sorted(array)
        assert len(result.steps) > 0
    
    def test_all_sorting_algorithms_produce_same_result(self):
        """Test that all sorting algorithms produce the same sorted result."""
        visualizer = AlgorithmVisualizer()
        array = [64, 34, 25, 12, 22, 11, 90]
        expected = sorted(array)
        
        sorting_algorithms = ['bubble_sort', 'quick_sort', 'merge_sort', 
                             'insertion_sort', 'selection_sort']
        
        for algorithm in sorting_algorithms:
            result = visualizer.visualize_sorting(array.copy(), algorithm=algorithm)
            assert result.final_array == expected, \
                f"{algorithm} produced incorrect result: {result.final_array}"
    
    def test_sorting_algorithms_with_empty_array(self):
        """Test that all sorting algorithms handle empty arrays."""
        visualizer = AlgorithmVisualizer()
        array = []
        
        sorting_algorithms = ['bubble_sort', 'quick_sort', 'merge_sort', 
                             'insertion_sort', 'selection_sort']
        
        for algorithm in sorting_algorithms:
            result = visualizer.visualize_sorting(array, algorithm=algorithm)
            assert result.final_array == [], \
                f"{algorithm} failed with empty array"
    
    def test_sorting_algorithms_with_single_element(self):
        """Test that all sorting algorithms handle single element arrays."""
        visualizer = AlgorithmVisualizer()
        array = [42]
        
        sorting_algorithms = ['bubble_sort', 'quick_sort', 'merge_sort', 
                             'insertion_sort', 'selection_sort']
        
        for algorithm in sorting_algorithms:
            result = visualizer.visualize_sorting(array, algorithm=algorithm)
            assert result.final_array == [42], \
                f"{algorithm} failed with single element"
    
    def test_sorting_algorithms_with_duplicates(self):
        """Test that all sorting algorithms handle duplicate elements."""
        visualizer = AlgorithmVisualizer()
        array = [3, 1, 2, 1, 3, 2]
        expected = [1, 1, 2, 2, 3, 3]
        
        sorting_algorithms = ['bubble_sort', 'quick_sort', 'merge_sort', 
                             'insertion_sort', 'selection_sort']
        
        for algorithm in sorting_algorithms:
            result = visualizer.visualize_sorting(array.copy(), algorithm=algorithm)
            assert result.final_array == expected, \
                f"{algorithm} failed with duplicates: {result.final_array}"


class TestSearchAlgorithmsIntegration:
    """
    Integration tests for all search algorithms via visualize_search().
    
    Validates: Requirements 7.1, 8.1
    """
    
    def test_binary_search_can_be_called(self):
        """Test that binary_search can be called via visualize_search()."""
        visualizer = AlgorithmVisualizer()
        array = [11, 12, 22, 25, 34, 64, 90]
        target = 22
        
        result = visualizer.visualize_search(array, target, algorithm='binary_search')
        
        assert isinstance(result, AlgorithmVisualization)
        assert result.algorithm_name == 'binary_search'
        assert result.steps[-1].found == True
        assert len(result.steps) > 0
    
    def test_linear_search_can_be_called(self):
        """Test that linear_search can be called via visualize_search()."""
        visualizer = AlgorithmVisualizer()
        array = [64, 34, 25, 12, 22, 11, 90]  # Unsorted is OK for linear search
        target = 22
        
        result = visualizer.visualize_search(array, target, algorithm='linear_search')
        
        assert isinstance(result, AlgorithmVisualization)
        assert result.algorithm_name == 'linear_search'
        assert result.steps[-1].found == True
        assert len(result.steps) > 0
    
    def test_jump_search_can_be_called(self):
        """Test that jump_search can be called via visualize_search()."""
        visualizer = AlgorithmVisualizer()
        array = [11, 12, 22, 25, 34, 64, 90]  # Must be sorted for jump search
        target = 22
        
        result = visualizer.visualize_search(array, target, algorithm='jump_search')
        
        assert isinstance(result, AlgorithmVisualization)
        assert result.algorithm_name == 'jump_search'
        assert result.steps[-1].found == True
        assert len(result.steps) > 0
    
    def test_all_search_algorithms_find_existing_element(self):
        """Test that all search algorithms find an existing element."""
        visualizer = AlgorithmVisualizer()
        sorted_array = [11, 12, 22, 25, 34, 64, 90]
        target = 25
        
        # Binary and jump search require sorted array
        result_binary = visualizer.visualize_search(sorted_array, target, 
                                                    algorithm='binary_search')
        assert result_binary.steps[-1].found == True
        
        result_jump = visualizer.visualize_search(sorted_array, target, 
                                                  algorithm='jump_search')
        assert result_jump.steps[-1].found == True
        
        # Linear search works on any array
        unsorted_array = [64, 34, 25, 12, 22, 11, 90]
        result_linear = visualizer.visualize_search(unsorted_array, target, 
                                                    algorithm='linear_search')
        assert result_linear.steps[-1].found == True
    
    def test_all_search_algorithms_report_missing_element(self):
        """Test that all search algorithms correctly report missing elements."""
        visualizer = AlgorithmVisualizer()
        sorted_array = [11, 12, 22, 25, 34, 64, 90]
        target = 99  # Not in array
        
        search_algorithms = ['binary_search', 'linear_search', 'jump_search']
        
        for algorithm in search_algorithms:
            result = visualizer.visualize_search(sorted_array, target, 
                                                algorithm=algorithm)
            assert result.steps[-1].found == False, \
                f"{algorithm} incorrectly reported finding {target}"
    
    def test_search_algorithms_with_empty_array(self):
        """Test that all search algorithms handle empty arrays."""
        visualizer = AlgorithmVisualizer()
        array = []
        target = 5
        
        search_algorithms = ['binary_search', 'linear_search', 'jump_search']
        
        for algorithm in search_algorithms:
            result = visualizer.visualize_search(array, target, algorithm=algorithm)
            assert result.steps[-1].found == False, \
                f"{algorithm} failed with empty array"
    
    def test_search_algorithms_with_single_element_found(self):
        """Test that all search algorithms handle single element (found)."""
        visualizer = AlgorithmVisualizer()
        array = [42]
        target = 42
        
        search_algorithms = ['binary_search', 'linear_search', 'jump_search']
        
        for algorithm in search_algorithms:
            result = visualizer.visualize_search(array, target, algorithm=algorithm)
            assert result.steps[-1].found == True, \
                f"{algorithm} failed to find element in single-element array"
    
    def test_search_algorithms_with_single_element_not_found(self):
        """Test that all search algorithms handle single element (not found)."""
        visualizer = AlgorithmVisualizer()
        array = [42]
        target = 99
        
        search_algorithms = ['binary_search', 'linear_search', 'jump_search']
        
        for algorithm in search_algorithms:
            result = visualizer.visualize_search(array, target, algorithm=algorithm)
            assert result.steps[-1].found == False, \
                f"{algorithm} incorrectly found element in single-element array"


class TestInvalidAlgorithmHandling:
    """
    Test error handling for invalid algorithm names.
    
    Validates: Requirements 11.2
    """
    
    def test_invalid_sorting_algorithm_raises_value_error(self):
        """Test that invalid algorithm name raises ValueError with helpful message."""
        visualizer = AlgorithmVisualizer()
        
        with pytest.raises(ValueError) as exc_info:
            visualizer.visualize_sorting([1, 2, 3], algorithm='heap_sort')
        
        error_message = str(exc_info.value)
        assert 'Unsupported algorithm' in error_message
        assert 'heap_sort' in error_message
        assert 'Supported algorithms' in error_message
    
    def test_invalid_search_algorithm_raises_value_error(self):
        """Test that invalid search algorithm raises ValueError with helpful message."""
        visualizer = AlgorithmVisualizer()
        
        with pytest.raises(ValueError) as exc_info:
            visualizer.visualize_search([1, 2, 3], 2, algorithm='interpolation_search')
        
        error_message = str(exc_info.value)
        assert 'Unsupported algorithm' in error_message
        assert 'interpolation_search' in error_message
        assert 'Supported algorithms' in error_message
    
    def test_error_message_lists_all_supported_algorithms(self):
        """Test that error message lists all supported algorithms."""
        visualizer = AlgorithmVisualizer()
        
        with pytest.raises(ValueError) as exc_info:
            visualizer.visualize_sorting([1, 2, 3], algorithm='invalid')
        
        error_message = str(exc_info.value)
        
        # Check that all sorting algorithms are mentioned
        assert 'bubble_sort' in error_message
        assert 'quick_sort' in error_message
        assert 'merge_sort' in error_message
        assert 'insertion_sort' in error_message
        assert 'selection_sort' in error_message
        
        # Check that search algorithms are also mentioned
        assert 'binary_search' in error_message
        assert 'linear_search' in error_message
        assert 'jump_search' in error_message


class TestBackwardCompatibility:
    """
    Test backward compatibility with existing v0.4.7 algorithms.
    
    Validates: Requirements 11.2
    """
    
    def test_bubble_sort_still_works(self):
        """Test that existing bubble_sort code continues to work."""
        visualizer = AlgorithmVisualizer()
        array = [3, 1, 2]
        
        # This is how users would have called it in v0.4.7
        result = visualizer.visualize_sorting(array, algorithm='bubble_sort')
        
        assert result.final_array == [1, 2, 3]
        assert result.algorithm_name == 'bubble_sort'
        assert 'comparisons' in result.statistics
        assert 'swaps' in result.statistics
    
    def test_binary_search_still_works(self):
        """Test that existing binary_search code continues to work."""
        visualizer = AlgorithmVisualizer()
        array = [1, 2, 3, 4, 5]
        target = 3
        
        # This is how users would have called it in v0.4.7
        result = visualizer.visualize_search(array, target, algorithm='binary_search')
        
        assert result.steps[-1].found == True
        assert result.algorithm_name == 'binary_search'
        assert 'comparisons' in result.statistics
    
    def test_default_algorithm_is_bubble_sort(self):
        """Test that default sorting algorithm is still bubble_sort."""
        visualizer = AlgorithmVisualizer()
        array = [3, 1, 2]
        
        # Call without specifying algorithm (should default to bubble_sort)
        result = visualizer.visualize_sorting(array)
        
        assert result.algorithm_name == 'bubble_sort'
        assert result.final_array == [1, 2, 3]
    
    def test_default_search_algorithm_is_binary_search(self):
        """Test that default search algorithm is still binary_search."""
        visualizer = AlgorithmVisualizer()
        array = [1, 2, 3, 4, 5]
        target = 3
        
        # Call without specifying algorithm (should default to binary_search)
        result = visualizer.visualize_search(array, target)
        
        assert result.algorithm_name == 'binary_search'
        assert result.steps[-1].found == True
    
    def test_visualization_result_structure_unchanged(self):
        """Test that AlgorithmVisualization structure is backward compatible."""
        visualizer = AlgorithmVisualizer()
        result = visualizer.visualize_sorting([3, 1, 2])
        
        # Check that all expected attributes exist
        assert hasattr(result, 'steps')
        assert hasattr(result, 'statistics')
        assert hasattr(result, 'algorithm_name')
        assert hasattr(result, 'input_data')
        assert hasattr(result, 'final_array')  # New in v0.5.2
        
        # Check that statistics structure is unchanged
        assert 'comparisons' in result.statistics
        assert 'swaps' in result.statistics
        assert 'steps' in result.statistics


class TestAlgorithmVisualizerInitialization:
    """
    Test AlgorithmVisualizer initialization and configuration.
    
    Validates: Requirements 11.2
    """
    
    def test_visualizer_can_be_initialized_without_parameters(self):
        """Test that visualizer can be initialized without parameters."""
        visualizer = AlgorithmVisualizer()
        
        assert visualizer is not None
        assert hasattr(visualizer, 'supported_algorithms')
    
    def test_supported_algorithms_contains_all_algorithms(self):
        """Test that supported_algorithms dict contains all 8 algorithms."""
        visualizer = AlgorithmVisualizer()
        
        expected_algorithms = {
            'bubble_sort', 'quick_sort', 'merge_sort', 'insertion_sort', 
            'selection_sort', 'binary_search', 'linear_search', 'jump_search'
        }
        
        actual_algorithms = set(visualizer.supported_algorithms.keys())
        
        assert expected_algorithms == actual_algorithms, \
            f"Missing algorithms: {expected_algorithms - actual_algorithms}"
    
    def test_all_algorithm_functions_are_callable(self):
        """Test that all registered algorithm functions are callable."""
        visualizer = AlgorithmVisualizer()
        
        for algorithm_name, algorithm_func in visualizer.supported_algorithms.items():
            assert callable(algorithm_func), \
                f"Algorithm function for '{algorithm_name}' is not callable"


