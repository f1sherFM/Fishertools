# Phase 1 Modules (v0.5.0)

## Overview

Version 0.5.0 introduces three powerful core modules for data visualization, type validation, and step-by-step debugging. These modules are designed to help both beginners and experienced developers write better code.

## 📊 Visualization Module

### Purpose
Visualize data structures in a human-readable format with proper formatting and indentation.

### Key Features
- **List visualization** with indices
- **Dictionary visualization** with keys
- **Nested structure support** with depth control
- **Item limiting** for large datasets
- **Clean formatting** with arrows and indentation

### Quick Start

```python
from fishertools.visualization import visualize

# Visualize a list
numbers = [10, 20, 30, 40, 50]
visualize(numbers)
# Output:
# 📊 Visualization:
# [0] → 10
# [1] → 20
# [2] → 30
# [3] → 40
# [4] → 50

# Visualize a dictionary
user = {"name": "Alice", "age": 25, "email": "alice@example.com"}
visualize(user, title="User Data")
# Output:
# 📊 User Data:
# {
#   'name' → 'Alice'
#   'age' → 25
#   'email' → 'alice@example.com'
# }

# Limit items for large datasets
big_list = list(range(1000))
visualize(big_list, max_items=5)
# Output:
# 📊 Visualization:
# [0] → 0
# [1] → 1
# [2] → 2
# [3] → 3
# [4] → 4
# ... and 995 more items
```

### API Reference

#### `visualize(data, title=None, colors=True, max_depth=5, max_items=None)`

Visualize a data structure.

**Parameters:**
- `data` (Any): Data to visualize
- `title` (str, optional): Title for the visualization
- `colors` (bool): Use colored output (default: True)
- `max_depth` (int): Maximum nesting depth (default: 5)
- `max_items` (int, optional): Maximum items to show

**Returns:** Formatted visualization string

#### `Visualizer` Class

```python
from fishertools.visualization import Visualizer

viz = Visualizer(colors=True, max_depth=3, max_items=10)
result = viz.visualize(data, title="My Data")
viz.print(data, title="My Data")  # Print directly to console
```

---

## ✅ Validation Module

### Purpose
Validate function arguments, data types, and data structures with clear error messages.

### Key Features
- **Type checking** via decorators
- **Email validation** with regex
- **URL validation** with regex
- **Number range validation**
- **String validation** with length and pattern checks
- **Structure validation** against schemas
- **Clear error messages** for debugging

### Quick Start

```python
from fishertools.validation import (
    validate_types,
    validate_email,
    validate_number,
    validate_structure,
    ValidationError
)

# Type validation with decorator
@validate_types
def create_user(name: str, age: int, email: str) -> dict:
    return {"name": name, "age": age, "email": email}

user = create_user("Alice", 25, "alice@example.com")  # ✅ Works
# user = create_user("Bob", "thirty", "bob@example.com")  # ❌ ValidationError

# Email validation
try:
    validate_email("user@example.com")  # ✅ Valid
    validate_email("invalid-email")     # ❌ ValidationError
except ValidationError as e:
    print(f"Error: {e}")

# Number validation
try:
    validate_number(42, min_val=0, max_val=100)  # ✅ Valid
    validate_number(150, min_val=0, max_val=100) # ❌ ValidationError
except ValidationError as e:
    print(f"Error: {e}")

# Structure validation
schema = {"name": str, "age": int, "active": bool}
data = {"name": "Alice", "age": 25, "active": True}
validate_structure(data, schema)  # ✅ Valid
```

### API Reference

#### `@validate_types`

Decorator for automatic type checking based on type hints.

```python
@validate_types
def my_function(x: int, y: str) -> bool:
    return len(y) > x

result = my_function(5, "hello")  # ✅ Works
# my_function(5, 123)  # ❌ ValidationError
```

#### `validate_email(email: str)`

Validate email format.

```python
validate_email("user@example.com")  # ✅ Valid
validate_email("invalid")           # ❌ ValidationError
```

#### `validate_url(url: str)`

Validate URL format.

```python
validate_url("https://example.com")  # ✅ Valid
validate_url("not-a-url")            # ❌ ValidationError
```

#### `validate_number(value, min_val=None, max_val=None)`

Validate number is within range.

```python
validate_number(42, min_val=0, max_val=100)  # ✅ Valid
validate_number(150, min_val=0, max_val=100) # ❌ ValidationError
```

#### `validate_string(value, min_length=None, max_length=None, pattern=None)`

Validate string properties.

```python
validate_string("hello", min_length=3, max_length=10)  # ✅ Valid
validate_string("hi", min_length=3)                    # ❌ ValidationError
validate_string("123", pattern=r"^\d+$")               # ✅ Valid
```

#### `validate_structure(data: dict, schema: dict)`

Validate data structure against schema.

```python
schema = {"name": str, "age": int}
data = {"name": "Alice", "age": 25}
validate_structure(data, schema)  # ✅ Valid
```

#### `ValidationError`

Exception raised when validation fails.

```python
try:
    validate_email("invalid")
except ValidationError as e:
    print(f"Validation failed: {e}")
```

---

## 🔍 Debug Module

### Purpose
Debug functions with step-by-step execution tracing and breakpoints.

### Key Features
- **Step-by-step execution** with variable values
- **Function call tracing** with indentation
- **Breakpoints** for pausing execution
- **Exception handling** with detailed info
- **Recursive function support**

### Quick Start

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
# Output:
# 🔍 Tracing: fibonacci
# → fibonacci(4)
#   → fibonacci(3)
#     → fibonacci(2)
#       → fibonacci(1) = 1
#       → fibonacci(0) = 0
#     ← fibonacci(2) = 1
#     → fibonacci(1) = 1
#   ← fibonacci(3) = 2
#   → fibonacci(2)
#     → fibonacci(1) = 1
#     → fibonacci(0) = 0
#   ← fibonacci(2) = 1
# ← fibonacci(4) = 3

# Breakpoints
x = 10
y = 20
set_breakpoint("Check values")
z = x + y
# Output:
# 🔴 Breakpoint: Check values
#    at script.py:5
```

### API Reference

#### `@debug_step_by_step`

Decorator for step-by-step function execution.

```python
@debug_step_by_step
def my_function(x, y):
    result = x + y
    return result

my_function(2, 3)
# Output:
# 🔍 Debugging: my_function
# Step 1: x = 2
# Step 2: y = 3
# Step 3: return 5
# ✅ Result: 5
```

#### `@trace`

Decorator for tracing function calls and returns.

```python
@trace
def my_function(x):
    return x * 2

my_function(5)
# Output:
# 🔍 Tracing: my_function
# → my_function(x=5)
# ← my_function(x=5) = 10
# ✅ Result: 10
```

#### `set_breakpoint(message="Breakpoint")`

Set a breakpoint for debugging.

```python
x = 10
set_breakpoint("Check x value")
y = x * 2
# Output:
# 🔴 Breakpoint: Check x value
#    at script.py:2
```

---

## Integration Examples

### Example 1: Validation + Visualization

```python
from fishertools.validation import validate_types
from fishertools.visualization import visualize

@validate_types
def process_users(users: list) -> dict:
    """Process a list of users."""
    visualize(users, title="Input Users")
    
    result = {
        "count": len(users),
        "users": users
    }
    
    visualize(result, title="Output")
    return result

users = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30}
]

result = process_users(users)
```

### Example 2: Validation + Debug

```python
from fishertools.validation import validate_types
from fishertools.debug import debug_step_by_step

@validate_types
@debug_step_by_step
def calculate_total(prices: list) -> float:
    """Calculate total price."""
    total = sum(prices)
    tax = total * 0.1
    final = total + tax
    return final

result = calculate_total([10.0, 20.0, 30.0])
```

### Example 3: All Three Modules

```python
from fishertools.validation import validate_types, validate_number
from fishertools.visualization import visualize
from fishertools.debug import debug_step_by_step

@validate_types
@debug_step_by_step
def analyze_scores(scores: list) -> dict:
    """Analyze test scores."""
    
    # Validate each score
    for score in scores:
        validate_number(score, min_val=0, max_val=100)
    
    # Visualize input
    visualize(scores, title="Input Scores")
    
    # Calculate statistics
    average = sum(scores) / len(scores)
    max_score = max(scores)
    min_score = min(scores)
    
    result = {
        "average": average,
        "max": max_score,
        "min": min_score,
        "count": len(scores)
    }
    
    # Visualize output
    visualize(result, title="Statistics")
    
    return result

scores = [85, 90, 78, 92, 88]
result = analyze_scores(scores)
```

---

## Testing

All modules include comprehensive test suites:

```bash
# Run all tests
pytest tests/test_visualization/ tests/test_validation/ tests/test_debug/ -v

# Run specific module tests
pytest tests/test_visualization/ -v
pytest tests/test_validation/ -v
pytest tests/test_debug/ -v

# Run with coverage
pytest tests/ --cov=fishertools --cov-report=html
```

**Test Coverage:**
- 56+ tests total
- 90%+ code coverage
- Property-based tests with Hypothesis
- Integration tests

---

## Performance Considerations

### Visualization Module
- Minimal overhead for small datasets
- Efficient for datasets up to 10,000 items
- Use `max_items` parameter for very large datasets

### Validation Module
- Type checking adds ~1-2% overhead
- Email/URL validation uses compiled regex
- Structure validation is O(n) where n = number of keys

### Debug Module
- `@debug_step_by_step` adds minimal overhead
- `@trace` adds more overhead due to frame inspection
- Use only during development, not in production

---

## Best Practices

### Visualization
1. Use titles for clarity
2. Limit items for large datasets
3. Use `max_depth` for deeply nested structures

### Validation
1. Use `@validate_types` for public APIs
2. Validate early in functions
3. Provide clear error messages

### Debug
1. Use `@debug_step_by_step` for simple functions
2. Use `@trace` for recursive functions
3. Use `set_breakpoint()` for specific points

---

## Roadmap

**Phase 2 (v0.6.0):**
- Performance module - analyze function performance
- Algorithms module - analyze algorithm complexity
- Comparison module - compare different approaches

**Phase 3 (v0.7.0+):**
- IDE plugins (VS Code, PyCharm)
- Git integration
- Advanced profiling
- Extended REPL

---

## Contributing

Found a bug or have a feature request? Please open an issue on GitHub!

---

## License

MIT License - see LICENSE file for details
