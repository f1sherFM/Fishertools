# Release v0.5.1: Algorithm Expansion & API Unification

## 🎯 Overview

Version 0.5.1 is a major feature release that completes the algorithm visualization suite and unifies the network API with the popular requests library. This release includes 8 total algorithms, requests-compatible API methods, and context-aware error explanations.

## 🚀 Major Features

### 🔌 Network Module Enhancements

**requests-Compatible API**
- `NetworkResponse.json()` - Get JSON data (requests library compatibility)
- `NetworkResponse.content` - Get raw bytes representation
- `NetworkResponse.text` - Get string representation
- Full backward compatibility with existing `.data` attribute

**Timeout Support for Downloads**
- `safe_download()` now accepts `timeout` parameter
- Control download timeout for slow connections
- Validation of timeout values
- Descriptive error messages on timeout

```python
from fishertools import safe_request, safe_download

# requests-compatible API
response = safe_request('https://api.example.com/data')
data = response.json()  # Just like requests!
raw_bytes = response.content
text = response.text

# Download with timeout
response = safe_download(
    'https://example.com/file.zip',
    'downloads/file.zip',
    timeout=60.0  # 60 second timeout
)
```

### 📊 Complete Algorithm Suite (8 Algorithms)

**5 Sorting Algorithms:**
- `bubble_sort` - Simple comparison-based sorting (existing)
- `quick_sort` - Fast divide-and-conquer with partition visualization
- `merge_sort` - Stable O(n log n) with merge range tracking
- `insertion_sort` - Efficient for small arrays with sorted portion highlighting
- `selection_sort` - Simple minimum-finding with search visualization

**3 Search Algorithms:**
- `binary_search` - O(log n) search in sorted arrays (existing)
- `linear_search` - O(n) sequential search (works on unsorted arrays)
- `jump_search` - O(√n) block-based search in sorted arrays

**Direct Result Access**
- New `final_array` attribute on `AlgorithmVisualization`
- Automatically computed from last step
- Returns a copy to prevent mutations

```python
from fishertools.visualization import AlgorithmVisualizer

viz = AlgorithmVisualizer()
array = [3, 1, 4, 1, 5, 9, 2, 6]

# All sorting algorithms
for algo in ['bubble_sort', 'quick_sort', 'merge_sort', 'insertion_sort', 'selection_sort']:
    result = viz.visualize_sorting(array.copy(), algo)
    print(f"{algo}: {result.final_array}")  # Direct access!

# All search algorithms
sorted_array = [1, 2, 3, 4, 5, 6, 7, 8, 9]
for algo in ['binary_search', 'linear_search', 'jump_search']:
    result = viz.visualize_search(sorted_array, target=5, algorithm=algo)
    print(f"{algo}: Found={result.statistics['found']}")
```

### 🌍 Enhanced Error Explanations

**Context-Aware Explanations**
- `explain_error()` now accepts `context` parameter
- Operation-specific guidance (list_access, dict_access, division, etc.)
- Variable name references in explanations
- Detailed information about valid ranges and available keys

```python
from fishertools import explain_error

try:
    my_list = [1, 2, 3]
    value = my_list[10]
except IndexError as e:
    explain_error(e, language='en', context={
        'operation': 'list_access',
        'variable_name': 'my_list',
        'index': 10
    })
    # Output includes:
    # - Variable name 'my_list' mentioned
    # - Valid index range (0 to 2)
    # - Operation-specific guidance
```

## ✅ Quality & Testing

### Comprehensive Test Coverage
- **1637+ total tests** across all modules
- **306 visualization tests** for all algorithms
- **118 compatibility tests** ensuring no breaking changes
- **Property-based tests** with Hypothesis for correctness validation
- **Unit tests** for edge cases and error conditions
- **Integration tests** for cross-module functionality

### 100% Backward Compatible
- All v0.4.x code continues to work without modifications
- Existing APIs maintain identical behavior
- All enhancements are additive, not breaking
- NetworkResponse.data still works alongside new methods
- explain_error() works without context parameter

## 📊 Enhanced Statistics

**Algorithm Tracking Improvements:**
- Partition indices for quick_sort
- Merge ranges for merge_sort
- Jump sizes and block starts for jump_search
- Detailed step-by-step information
- Comprehensive statistics for all algorithms

## 🔧 Technical Improvements

- Full type hints for all new functions and methods
- Detailed docstrings with usage examples
- PEP 8 compliance throughout
- Performance optimizations for algorithms
- Clean, maintainable architecture
- Comprehensive error handling

## 📚 Documentation

- Updated README with v0.5.1 examples
- Usage examples for all new features
- Migration guide from requests library
- Context parameter documentation
- Algorithm complexity information

## 🎯 Migration Guide

### From requests to fishertools

```python
# Before (requests)
import requests
response = requests.get('https://api.example.com/data')
data = response.json()
content = response.content
text = response.text

# After (fishertools) - Same API!
from fishertools import safe_request
response = safe_request('https://api.example.com/data')
data = response.json()  # Same method!
content = response.content  # Same property!
text = response.text  # Same property!
```

### Using Context in Error Explanations

```python
# Before (v0.4.x)
try:
    value = my_list[index]
except IndexError as e:
    explain_error(e, language='en')

# After (v0.5.1) - More specific!
try:
    value = my_list[index]
except IndexError as e:
    explain_error(e, language='en', context={
        'operation': 'list_access',
        'variable_name': 'my_list',
        'index': index
    })
```

## 📦 Installation

```bash
pip install --upgrade fishertools
```

## 🔗 Links

- **GitHub Repository:** https://github.com/f1sherFM/My_1st_library_python
- **PyPI Package:** https://pypi.org/project/fishertools/
- **Documentation:** See README.md and docs/ folder
- **Issues:** https://github.com/f1sherFM/My_1st_library_python/issues

## 🙏 Acknowledgments

Thank you to all users who provided feedback and helped shape this release. Special thanks to the Python community for their continued support!

## 📝 Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete details of all changes.

---

**Fishertools v0.5.1** - Making Python easier, safer, and more fun for everyone! 🐍✨

