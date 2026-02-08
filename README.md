# Fishertools

**Tools that make Python easier and safer for beginners**

Fishertools is a Python library designed specifically for beginner developers. It provides clear error explanations, safe utilities, learning tools, and powerful debugging features to help you master Python.

## 🚀 What's New in v0.4.9?

**Search Algorithms Release** - New search algorithms with comprehensive visualization:

- **🔍 Linear Search** - Sequential search through unsorted arrays with O(n) complexity
- **⚡ Jump Search** - Block-based search in sorted arrays with O(√n) complexity
- **📊 Enhanced Search Visualization** - Step-by-step tracking with jump size and block information
- **✅ Comprehensive Testing** - 166+ tests covering all search algorithms
- **🎯 Algorithm Correctness** - All 271 visualization tests passing (100% success rate)
- **🔄 Complete Algorithm Suite** - 5 sorting + 3 search algorithms fully implemented
- **✅ 100% Backward Compatible** - All existing code continues to work seamlessly

Previous releases:
- v0.4.8: 4 new sorting algorithms (Quick, Merge, Insertion, Selection)
- v0.4.7: Safe Network Operations, Enhanced Visualization, Multilingual Support
- v0.4.6: Async support, Performance improvements, PEP 561 compliance

[See full changelog →](CHANGELOG.md)

## Quick Start

```bash
pip install fishertools
```

## Quick Reference

| Task | Function | Module |
|------|----------|--------|
| Explain an error | `explain_error(e, language='ru')` | errors |
| **🆕 Translate error** | **`translate_error(e, lang='en')`** | **i18n** |
| **🆕 Detect language** | **`detect_language()`** | **i18n** |
| **🆕 HTTP request** | **`safe_request(url, timeout=10)`** | **network** |
| **🆕 Download file** | **`safe_download(url, path)`** | **network** |
| Get element safely | `safe_get(list, index, default)` | safe |
| Divide safely | `safe_divide(a, b, default)` | safe |
| Calculate average safely | `safe_average(numbers, default)` | safe |
| Format string safely | `safe_format(template, values, behavior)` | safe |
| Strip string safely | `safe_strip(text, default)` | safe |
| Split string safely | `safe_split(text, sep, default)` | safe |
| Join safely | `safe_join(sep, items)` | safe |
| Read file safely | `safe_read_file(path)` | safe |
| Async read file | `await async_safe_read_file(path)` | async_safe |
| Async write file | `await async_safe_write_file(path, content)` | async_safe |
| Async logger | `await logger.info(msg)` | async_logger |
| Learn Python concepts | `explain(topic)` | learn |
| Visualize data | `visualize(data, style='tree', colors=True)` | visualization |
| **🆕 Visualize algorithm** | **`visualize_sorting(array, 'quick_sort')`** | **visualization** |
| Validate types | `@validate_types` | validation |
| Debug step-by-step | `@debug_step_by_step` | debug |
| **🆕 Get version info** | **`get_version_info()`** | **main** |

## Core Features

### 🌐 Safe Network Operations (NEW in v0.4.7!)
Make HTTP requests and download files safely with proper timeout handling and error management.

```python
from fishertools import safe_request, safe_download

# Safe HTTP request with timeout
response = safe_request('https://api.example.com/data', timeout=10)
if response.success:
    print(response.data)
else:
    print(f"Error: {response.error}")

# Safe file download with progress tracking
def progress_callback(progress):
    print(f"Downloaded: {progress.percentage:.1f}%")

response = safe_download(
    'https://example.com/file.zip',
    'downloads/file.zip',
    progress_callback=progress_callback
)

if response.success:
    print(f"File saved to: {response.file_path}")
```

**Features:**
- Automatic timeout handling (default 10 seconds)
- Structured error responses (never raises exceptions)
- Progress tracking for downloads
- File conflict handling
- Cleanup on failure
- Disk space checking

### 🌍 Multilingual Error Explanations (NEW in v0.4.7!)
Get error explanations in your preferred language with automatic detection.

```python
from fishertools import explain_error, translate_error, detect_language

# Detect system language
lang = detect_language()  # Returns 'ru' or 'en'

try:
    result = 10 / 0
except ZeroDivisionError as e:
    # Explain in Russian (default)
    explain_error(e, language='ru')
    
    # Explain in English
    explain_error(e, language='en')
    
    # Auto-detect language
    explain_error(e, language='auto')
    
    # Get structured explanation
    explanation = translate_error(e, lang='en')
    print(explanation.explanation)
    print(explanation.suggestions)
```

**Supported Languages:**
- Russian (ru) - default
- English (en)
- Auto-detection based on system locale

### 🎨 Enhanced Visualization (NEW in v0.4.7!)
Visualize data with multiple styles, colors, and export options.

```python
from fishertools import visualize, EnhancedVisualizer, AlgorithmVisualizer

# Basic visualization (existing)
data = {"name": "Alice", "scores": [90, 85, 92]}
visualize(data)

# Enhanced visualization with tree style
enhanced_viz = EnhancedVisualizer()
result = enhanced_viz.visualize(
    data,
    style='tree',      # Tree-like hierarchical format
    colors=True,       # Color highlighting by data type
    max_depth=3,       # Limit nesting depth
    export='json'      # Export to JSON file
)

# Algorithm visualization - Sorting (5 algorithms available!)
algo_viz = AlgorithmVisualizer()
array = [3, 1, 4, 1, 5, 9, 2, 6]

# Try different sorting algorithms
for algorithm in ['bubble_sort', 'quick_sort', 'merge_sort', 'insertion_sort', 'selection_sort']:
    result = algo_viz.visualize_sorting(
        array.copy(),
        algorithm=algorithm,
        step_delay=0.5  # Delay between steps
    )
    print(f"\n{algorithm}:")
    print(f"  Comparisons: {result.statistics['comparisons']}")
    print(f"  Swaps: {result.statistics['swaps']}")
    print(f"  Final array: {result.final_array}")

# Algorithm visualization - Searching (NEW in v0.4.9!)
sorted_array = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Binary search (existing)
result = algo_viz.visualize_search(
    sorted_array,
    target=5,
    algorithm='binary_search'
)

# Linear search - works on unsorted arrays (NEW!)
unsorted_array = [3, 1, 4, 1, 5, 9, 2, 6]
result = algo_viz.visualize_search(
    unsorted_array,
    target=5,
    algorithm='linear_search'
)

# Jump search - efficient for sorted arrays (NEW!)
result = algo_viz.visualize_search(
    sorted_array,
    target=5,
    algorithm='jump_search'
)

for step in result.steps:
    print(f"Step {step.step_number}: {step.description}")
```

**Features:**
- Tree-style hierarchical rendering
- Color highlighting by data type
- Depth limiting for nested structures
- Export to JSON and HTML formats
- Algorithm step-by-step visualization
- **5 Sorting Algorithms:** bubble_sort, quick_sort, merge_sort, insertion_sort, selection_sort
- **3 Search Algorithms:** binary_search, linear_search (NEW!), jump_search (NEW!)
- Statistics tracking (comparisons, swaps, jumps, etc.)
- Direct access to final sorted array via `final_array` attribute

### 🔴 Error Explanation
Get clear explanations of Python errors with suggestions for fixing them.

```python
from fishertools import explain_error

try:
    result = 10 / 0
except Exception as e:
    explain_error(e)
```

### 🛡️ Safe Utilities
Functions like `safe_get()`, `safe_divide()`, `safe_average()`, `safe_format()` that prevent typical beginner errors.

```python
from fishertools import safe_get, safe_divide
from fishertools.safe import safe_strip, safe_split, safe_join, safe_average, safe_format, PlaceholderBehavior

# Safe dictionary access
value = safe_get(my_dict, "key", default="not found")

# Safe division (mathematically correct!)
result = safe_divide(10, 0)  # Returns None (undefined, not 0!)
result = safe_divide(10, 0, default=0)  # Explicitly set to 0

# Safe average calculation (NEW in v0.4.5!)
avg = safe_average([1, 2, 3])  # Returns 2.0
avg = safe_average([], default=0)  # Returns 0 for empty list
avg = safe_average([1, "text", 3, None, 2])  # Returns 2.0 (filters non-numeric)

# Safe string formatting with configurable behavior (NEW in v0.4.5!)
result = safe_format("Hello, {name}!", {})  
# Returns "Hello, [MISSING: name]!" (default behavior)

result = safe_format("Hello, {name}!", {}, behavior=PlaceholderBehavior.PRESERVE)
# Returns "Hello, {name}!" (preserves placeholder)

result = safe_format("Hello, {name}!", {}, behavior=PlaceholderBehavior.EMPTY)
# Returns "Hello, !" (replaces with empty string)

result = safe_format("Hello, {name}!", {"name": "World"})
# Returns "Hello, World!" (normal formatting)

# Safe string operations
text = safe_strip(None)  # Returns '' instead of error
items = safe_split("a,b,c", ",")  # Returns ['a', 'b', 'c']
joined = safe_join(", ", ["a", None, "b"])  # Returns 'a, b' (skips None)
```

### 📚 Learning Tools
Structured explanations of Python concepts with examples and best practices.

```python
from fishertools.learn import generate_example, show_best_practice

example = generate_example("list comprehension")
best_practice = show_best_practice("error handling")
```

### 🎯 Ready-made Patterns
Templates for common tasks like menus, file storage, logging, and CLI applications.

### 📊 Data Visualization
Visualize data structures in a human-readable format with proper formatting and indentation.

```python
from fishertools.visualization import visualize

# Visualize lists
numbers = [10, 20, 30, 40, 50]
visualize(numbers)
# Output:
# 📊 Visualization:
# [0] → 10
# [1] → 20
# [2] → 30
# [3] → 40
# [4] → 50

# Visualize dictionaries
user = {"name": "Alice", "age": 25, "email": "alice@example.com"}
visualize(user, title="User Data")
# Output:
# 📊 User Data:
# {
#   'name' → 'Alice'
#   'age' → 25
#   'email' → 'alice@example.com'
# }

# Visualize nested structures
data = {"users": [{"name": "Alice"}, {"name": "Bob"}]}
visualize(data, max_depth=3)
```

**Basic Features:**
- List visualization with indices
- Dictionary visualization with keys
- Nested structure support with depth control
- Item limiting for large datasets
- Clean formatting with arrows and indentation

**Enhanced Features (v0.4.7):**
- Tree-style hierarchical rendering
- Color highlighting by data type
- Export to JSON and HTML
- Algorithm visualization (sorting, searching)
- Step-by-step execution tracking

### ✅ Type Validation (v0.4.1+)
Validate function arguments and data structures with clear error messages.

```python
from fishertools.validation import validate_types, validate_email, ValidationError

# Type checking via decorator
@validate_types
def create_user(name: str, age: int, email: str) -> dict:
    return {"name": name, "age": age, "email": email}

user = create_user("Alice", 25, "alice@example.com")  # ✅ Works
# create_user("Bob", "thirty", "bob@example.com")     # ❌ ValidationError

# Email validation
try:
    validate_email("user@example.com")  # ✅ Valid
except ValidationError as e:
    print(f"Error: {e}")

# Number validation
from fishertools.validation import validate_number
validate_number(42, min_val=0, max_val=100)  # ✅ Valid

# Structure validation
from fishertools.validation import validate_structure
schema = {"name": str, "age": int}
data = {"name": "Alice", "age": 25}
validate_structure(data, schema)  # ✅ Valid
```

**Features:**
- Type checking via `@validate_types` decorator
- Email and URL validation
- Number range validation
- String validation with length and pattern checks
- Data structure validation against schemas
- Clear, actionable error messages

### 🔍 Step-by-Step Debugging (v0.4.1+)
Debug functions with step-by-step execution and function call tracing.

```python
from fishertools.debug import debug_step_by_step, trace, set_breakpoint

# Step-by-step debugging
@debug_step_by_step
def calculate_average(numbers):
    total = sum(numbers)
    average = total / len(numbers)
    return average

result = calculate_average([1, 2, 3, 4, 5])
# Output:
# 🔍 Debugging: calculate_average
# Step 1: numbers = [1, 2, 3, 4, 5]
# Step 2: return 3.0
# ✅ Result: 3.0

# Function call tracing
@trace
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = fibonacci(4)
# Shows all function calls with indentation

# Breakpoints
x = 10
set_breakpoint("Check x value")
y = x * 2
# 🔴 Breakpoint: Check x value
#    at script.py:2
```

**Features:**
- Step-by-step execution with variable values
- Function call tracing with indentation
- Breakpoints for pausing execution
- Exception handling with detailed information
- Recursive function support

## 📖 Documentation

Complete documentation is available in the `docs/` folder:

- **[Getting Started](docs/getting-started.md)** - Quick start guide with installation and first example
- **[Features](docs/features.md)** - Overview of all features and capabilities
- **[Installation](docs/installation.md)** - Detailed installation instructions for different operating systems
- **[API Reference](docs/api-reference.md)** - Complete API documentation with all functions and classes
- **[v0.4.1 Modules](docs/modules-v0.4.1.md)** - Detailed documentation for new Visualization, Validation, and Debug modules
- **[Examples](docs/examples.md)** - Practical examples from basic to advanced usage
- **[Limitations](docs/limitations.md)** - Known limitations and performance considerations
- **[Contributing](docs/contributing.md)** - How to contribute to the project

## 🎯 Who Should Use Fishertools?

- **Beginners** - Just starting to learn Python
- **Students** - Learning Python in a classroom
- **Educators** - Teaching Python to others
- **Professionals** - Want safer, more readable code

## 🔄 Integration Examples

### Network + Visualization + I18n (v0.4.7)

```python
from fishertools import safe_request, visualize, explain_error

# Fetch data from API
response = safe_request('https://api.example.com/users', timeout=5)

# Visualize the response
visualize(response.__dict__, title="API Response")

# Handle errors with multilingual explanations
if not response.success:
    try:
        raise ConnectionError(response.error)
    except Exception as e:
        explain_error(e, language='en')
```

### Algorithm Visualization + Debug

```python
from fishertools.visualization import AlgorithmVisualizer
from fishertools.debug import debug_step_by_step

@debug_step_by_step
def sort_and_analyze(numbers):
    visualizer = AlgorithmVisualizer()
    result = visualizer.visualize_sorting(numbers, 'bubble_sort')
    return result.statistics

stats = sort_and_analyze([5, 2, 8, 1, 9])
print(f"Comparisons: {stats['comparisons']}")
```

### Multilingual Error Handling

```python
from fishertools import explain_error, detect_language, safe_divide

# Detect user's language
user_lang = detect_language()

# Perform operation
result = safe_divide(10, 0)

if result is None:
    try:
        raise ZeroDivisionError("Division by zero")
    except Exception as e:
        # Explain in user's language
        explain_error(e, language=user_lang)
```

### Visualization + Validation

```python
from fishertools.validation import validate_types
from fishertools.visualization import visualize

@validate_types
def process_users(users: list) -> dict:
    visualize(users, title="Input Users")
    result = {"count": len(users), "users": users}
    visualize(result, title="Output")
    return result

users = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]
result = process_users(users)
```

### Validation + Debug

```python
from fishertools.validation import validate_types
from fishertools.debug import debug_step_by_step

@validate_types
@debug_step_by_step
def calculate_total(prices: list) -> float:
    total = sum(prices)
    tax = total * 0.1
    final = total + tax
    return final

result = calculate_total([10.0, 20.0, 30.0])
```

### All Three Modules

```python
from fishertools.validation import validate_types, validate_structure
from fishertools.visualization import visualize
from fishertools.debug import debug_step_by_step

@validate_types
@debug_step_by_step
def analyze_data(data: dict) -> dict:
    schema = {"name": str, "values": list}
    validate_structure(data, schema)
    
    visualize(data, title="Input")
    
    result = {
        "name": data["name"],
        "count": len(data["values"]),
        "sum": sum(data["values"])
    }
    
    visualize(result, title="Output")
    return result

data = {"name": "Test", "values": [1, 2, 3, 4, 5]}
result = analyze_data(data)
```

## 📊 Version History

### v0.4.8 (Current - February 2026)
- 🔄 **Quick Sort Algorithm** - Fast divide-and-conquer sorting with partition visualization
- 🔀 **Merge Sort Algorithm** - Stable O(n log n) sorting with merge range tracking
- 📥 **Insertion Sort Algorithm** - Efficient for small arrays with sorted portion highlighting
- 🔍 **Selection Sort Algorithm** - Simple minimum-finding with search visualization
- 🎯 **Final Array Attribute** - Direct access to sorted results via `result.final_array`
- ✅ **105+ Tests** - Comprehensive property-based and unit tests for all algorithms
- 📊 **Enhanced Statistics** - Detailed tracking of comparisons, swaps, and steps
- ✅ **100% Backward Compatible** - All existing code continues to work

### v0.4.7 (February 2026)
- 🌐 **Safe Network Operations** - HTTP requests and file downloads with timeout handling
- 🎨 **Enhanced Visualization** - Tree-style rendering, colors, and export to JSON/HTML
- 📊 **Algorithm Visualization** - Step-by-step sorting and searching visualization
- 🌍 **Multilingual Support** - Error explanations in Russian and English
- ⚙️ **Configuration Management** - Persistent settings for all modules
- 📊 **Version Information** - New `get_version_info()` function
- ✅ **56 Integration Tests** - Comprehensive testing of all new features
- ✅ **100% Backward Compatible** - All existing code continues to work

### v0.4.6
- ⚡ **Async Support** - AsyncSimpleLogger and async safe utilities
- 🔒 **Thread Safety** - Thread-safe SimpleLogger with automatic locking
- 💾 **Smart Caching** - LRU cache for 10,000x faster repeated calls
- 📝 **Type Hints** - Full PEP 561 support with py.typed marker

### v0.4.5.1
- 🐛 **Critical Bug Fixes** - Fixed learning module FileNotFoundError
- 🔧 **Better Error Messages** - Clear ValidationError messages for type mismatches
- 📖 **Contextual Explanations** - New `explain_error()` for educational error messages
- 🎨 **Enhanced safe_format()** - Configurable placeholder behavior (PRESERVE, MISSING, EMPTY)
- ➕ **New safe_average()** - Safe average calculation with automatic filtering
- 🛡️ **Comprehensive Error Handling** - Educational messages for all common Python errors
- ✅ **100% Backward Compatible** - All existing code continues to work

### v0.4.5
- Same as v0.4.5.1 (re-release for PyPI)

### v0.4.4
- � **Enhanced Type Safety** - Full type hints with TypeVar and ParamSpec
- ✅ **Better Input Validation** - Parameter validation and attempt limiting
- ⚡ **Performance Optimizations** - Pre-compiled regex patterns
- 📦 **Improved Dependencies** - Fixed version pinning and optional extras
- 🛡️ **Security Enhancements** - DoS protection and better error handling
- 📚 **Centralized Versioning** - Single source of truth in _version.py

### v0.4.3
- � **Code Quality Refactoring** - Fixed "spaghetti code"
- ✨ **Implemented safe_string_operations** - 6 new string utilities
- 🔢 **Fixed safe_divide mathematics** - Now returns None for 10/0 (correct!)
- 🐍 **Simplified error handling** - Pythonic EAFP approach
- 📦 **Refactored collection functions** - Cleaner, simpler code
- ✅ 82/82 tests passing
- 📉 -150 lines of unnecessary code
- 📈 +6 new useful functions

### v0.4.1
- ✨ **NEW:** Visualization module for data structure visualization
- ✨ **NEW:** Validation module for type checking and data validation
- ✨ **NEW:** Debug module for step-by-step execution and tracing
- 📈 65+ new tests with 90%+ code coverage
- 📚 Complete documentation for all new modules

### v0.4.0
- 🎓 Knowledge Engine Interactive REPL
- 📚 Extended documentation system

### v0.3.x
- 🛡️ Safe utilities module
- 📚 Learning tools
- 🔴 Error explanation system

## 🧪 Testing

All modules are thoroughly tested:

```bash
# Run all tests
pytest tests/ -v

# Run specific module tests
pytest tests/test_visualization/ -v
pytest tests/test_validation/ -v
pytest tests/test_debug/ -v

# Run with coverage
pytest tests/ --cov=fishertools --cov-report=html
```

**Test Coverage:** 90%+ across all modules

## 📦 Installation

### From PyPI (Recommended)

```bash
pip install fishertools
```

### From Source

```bash
git clone https://github.com/f1sherFM/My_1st_library_python.git
cd My_1st_library_python
pip install -e .
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on:
- How to report bugs
- How to suggest features
- How to submit pull requests
- Code style guidelines

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

Fishertools is built with ❤️ for the Python community, especially for beginners learning to code.

---

**Fishertools** - Making Python easier, safer, and more fun for everyone! 🐍✨

**Current Version:** 0.4.8 | **Last Updated:** February 8, 2026
