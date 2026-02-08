# Release Notes v0.4.8 - Algorithm Expansion

**Release Date:** February 8, 2026

## 🎉 Overview

Version 0.4.8 brings a major expansion to the algorithm visualization capabilities with **4 new sorting algorithms**, comprehensive testing, and enhanced data models. This release maintains 100% backward compatibility while significantly expanding educational features.

## 🚀 New Features

### 🔄 Quick Sort Algorithm
Fast divide-and-conquer sorting with visual partition tracking:
```python
from fishertools.visualization import AlgorithmVisualizer

visualizer = AlgorithmVisualizer()
result = visualizer.visualize_sorting([5, 2, 8, 1, 9], 'quick_sort')

print(f"Sorted: {result.final_array}")
print(f"Comparisons: {result.statistics['comparisons']}")
print(f"Swaps: {result.statistics['swaps']}")
```

**Features:**
- Partition visualization with pivot highlighting
- Average O(n log n) time complexity
- Step-by-step execution tracking
- `partition_index` in visualization steps

### 🔀 Merge Sort Algorithm
Stable sorting with merge range tracking:
```python
result = visualizer.visualize_sorting([5, 2, 8, 1, 9], 'merge_sort')
print(f"Sorted: {result.final_array}")
```

**Features:**
- Guaranteed O(n log n) time complexity
- Merge range visualization
- Division and merge process tracking
- `merge_range` in visualization steps

### 📥 Insertion Sort Algorithm
Efficient for small and nearly-sorted arrays:
```python
result = visualizer.visualize_sorting([5, 2, 8, 1, 9], 'insertion_sort')
print(f"Sorted: {result.final_array}")
```

**Features:**
- Sorted portion highlighting
- Best case O(n) for sorted arrays
- Element insertion visualization
- Efficient for small datasets

### 🔍 Selection Sort Algorithm
Simple minimum-finding algorithm:
```python
result = visualizer.visualize_sorting([5, 2, 8, 1, 9], 'selection_sort')
print(f"Sorted: {result.final_array}")
```

**Features:**
- Minimum search visualization
- Simple algorithm for learning
- Swap position highlighting
- O(n²) time complexity

## 🎯 Enhanced Features

### Final Array Attribute
Direct access to sorted results without manual extraction:
```python
result = visualizer.visualize_sorting([3, 1, 2], 'quick_sort')
sorted_array = result.final_array  # Direct access!
# No need to: result.steps[-1].array_state
```

### Enhanced Data Models
- `partition_index` field in SortingStep for quick sort
- `merge_range` field in SortingStep for merge sort
- Improved statistics tracking for all algorithms

## ✅ Testing & Quality

### Comprehensive Test Coverage
- **105+ tests** covering all sorting algorithms
- **Property-based tests** with Hypothesis (100+ iterations each)
- **Unit tests** for edge cases and specific behaviors
- **Integration tests** for algorithm visualizer

### Test Categories
1. **Correctness Tests** - Verify sorted output and element preservation
2. **Visualization Tests** - Verify step structure and highlighting
3. **Statistics Tests** - Verify comparison and swap counting
4. **Edge Case Tests** - Empty arrays, single elements, duplicates, negatives

## 📊 Algorithm Comparison

| Algorithm | Time Complexity | Space | Stable | Best For |
|-----------|----------------|-------|--------|----------|
| Quick Sort | O(n log n) avg | O(log n) | No | General purpose |
| Merge Sort | O(n log n) | O(n) | Yes | Guaranteed performance |
| Insertion Sort | O(n²) | O(1) | Yes | Small/nearly sorted |
| Selection Sort | O(n²) | O(1) | No | Learning/teaching |
| Bubble Sort | O(n²) | O(1) | Yes | Learning/teaching |

## 🔧 Technical Details

### Module Structure
```
fishertools/visualization/
├── algorithms/
│   ├── __init__.py
│   ├── sorting.py      # All sorting implementations
│   └── searching.py    # Search implementations
├── algorithm_visualizer.py
└── models.py
```

### API Compatibility
All existing code continues to work:
```python
# v0.4.7 code still works
result = visualizer.visualize_sorting(array, 'bubble_sort')

# v0.4.8 adds new algorithms
result = visualizer.visualize_sorting(array, 'quick_sort')
result = visualizer.visualize_sorting(array, 'merge_sort')
result = visualizer.visualize_sorting(array, 'insertion_sort')
result = visualizer.visualize_sorting(array, 'selection_sort')
```

## 📈 Statistics

### Code Metrics
- **+3,897 lines** of new code and tests
- **28 files** changed
- **105+ tests** added
- **100% backward compatible**

### Test Results
```
105 tests passed in 3.52 seconds
- Quick Sort: 30 tests (9 property + 21 unit)
- Merge Sort: 13 tests (3 property + 10 unit)
- Insertion Sort: 29 tests (9 property + 20 unit)
- Selection Sort: 33 tests (11 property + 22 unit)
```

## 🔄 Migration Guide

No migration needed! All existing code works without changes.

### Optional: Use New Algorithms
```python
# Before (v0.4.7)
result = visualizer.visualize_sorting(array, 'bubble_sort')

# After (v0.4.8) - try new algorithms
for algo in ['quick_sort', 'merge_sort', 'insertion_sort', 'selection_sort']:
    result = visualizer.visualize_sorting(array, algo)
    print(f"{algo}: {result.final_array}")
```

### Optional: Use Final Array Attribute
```python
# Before (v0.4.7)
result = visualizer.visualize_sorting(array, 'bubble_sort')
sorted_array = result.steps[-1].array_state if result.steps else array

# After (v0.4.8) - simpler!
result = visualizer.visualize_sorting(array, 'quick_sort')
sorted_array = result.final_array
```

## 🐛 Bug Fixes

No bug fixes in this release - pure feature expansion.

## 📚 Documentation

Updated documentation:
- README.md with new algorithm examples
- CHANGELOG.md with detailed changes
- Comprehensive docstrings for all new functions
- Type hints for all new components

## 🙏 Acknowledgments

Special thanks to the Python community for feedback on algorithm visualization features!

## 📦 Installation

```bash
pip install --upgrade fishertools
```

Or from source:
```bash
git clone https://github.com/f1sherFM/My_1st_library_python.git
cd My_1st_library_python
git checkout v0.4.8
pip install -e .
```

## 🔗 Links

- **GitHub Repository:** https://github.com/f1sherFM/My_1st_library_python
- **PyPI Package:** https://pypi.org/project/fishertools/
- **Documentation:** https://github.com/f1sherFM/My_1st_library_python/tree/main/docs
- **Issues:** https://github.com/f1sherFM/My_1st_library_python/issues

---

**Full Changelog:** https://github.com/f1sherFM/My_1st_library_python/compare/v0.4.7...v0.4.8
