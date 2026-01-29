# Features

Fishertools provides a comprehensive set of features designed to make Python easier and safer for beginners.

## 🚨 Error Explanation

Get clear, understandable explanations of Python errors with suggestions for fixing them.

**Supported Error Types:**
- TypeError - Type mismatch errors
- ValueError - Invalid value errors
- IndexError - List index out of range
- KeyError - Dictionary key not found
- NameError - Undefined variable or name
- AttributeError - Attribute not found
- ImportError - Module import problems
- FileNotFoundError - File not found
- ZeroDivisionError - Division by zero
- SyntaxError - Syntax errors (with limitations)

**Example:**
```python
from fishertools import explain_error

try:
    result = 10 / 0
except Exception as e:
    explain_error(e)
```

See [Examples](examples.md) for more error explanation examples.

## 🛡️ Safe Utilities

Functions that prevent common beginner mistakes:

### safe_get()
Safely access list or dictionary elements without IndexError or KeyError:
```python
from fishertools.safe import safe_get

numbers = [1, 2, 3]
result = safe_get(numbers, 10, "default")  # Returns "default"
```

### safe_divide()
Divide numbers safely without ZeroDivisionError:
```python
from fishertools.safe import safe_divide

result = safe_divide(10, 0, 0)  # Returns 0 instead of error
```

### safe_read_file()
Read files safely without FileNotFoundError:
```python
from fishertools.safe import safe_read_file

content = safe_read_file("file.txt", default="file not found")
```

### ensure_dir()
Create directories recursively without errors:
```python
from fishertools.safe import ensure_dir

path = ensure_dir("./data/nested/directory")  # Creates all intermediate folders
```

### get_file_hash()
Calculate file hash (SHA256 by default):
```python
from fishertools.safe import get_file_hash

file_hash = get_file_hash("data.txt")
md5_hash = get_file_hash("data.txt", algorithm='md5')
```

### read_last_lines()
Read the last N lines of a file:
```python
from fishertools.safe import read_last_lines

last_lines = read_last_lines("log.txt", n=10)  # Last 10 lines
```

See [API Reference](api-reference.md) for complete safe utilities documentation.

## 📚 Learning Tools

### explain() - Python Concept Explanations

Get structured explanations of 30+ Python concepts:

```python
from fishertools.learn import explain

explanation = explain("list")
print(explanation["description"])    # What it is
print(explanation["when_to_use"])    # When to use it
print(explanation["example"])        # Code example
```

**Supported Topics:**
- Basic Types: int, float, str, bool, list, tuple, set, dict
- Control Flow: if, for, while, break, continue
- Functions: function, return, lambda, *args, **kwargs
- Error Handling: try, except, finally, raise
- File Operations: open, read, write, with
- Advanced: slice, list_comprehension, enumerate, import

### Knowledge Engine - Educational System

Access 35+ Python concepts with detailed explanations:

```python
from fishertools.learn import get_topic, list_topics, search_topics

# Get information about a topic
topic = get_topic("Lists")
print(topic["description"])
print(topic["common_mistakes"])

# List all available topics
all_topics = list_topics()

# Search for topics
results = search_topics("loop")
```

See [Examples](examples.md) for more learning tool examples.

## 🔧 Ready-made Patterns

### simple_menu() - Interactive Menu

Create interactive console menus easily:

```python
from fishertools.patterns import simple_menu

simple_menu({
    "Option 1": lambda: print("Selected option 1"),
    "Option 2": lambda: print("Selected option 2")
})
```

### JSONStorage - Data Persistence

Save and load data in JSON format:

```python
from fishertools.patterns import JSONStorage

storage = JSONStorage("data.json")
storage.save({"name": "Alice", "age": 30})
loaded_data = storage.load()
```

### SimpleLogger - Logging

Add logging to your application:

```python
from fishertools.patterns import SimpleLogger

logger = SimpleLogger("app.log")
logger.info("Application started")
logger.warning("Low memory")
logger.error("Connection failed")
```

### SimpleCLI - Command Line Interface

Create CLI applications easily:

```python
from fishertools.patterns import SimpleCLI

cli = SimpleCLI("myapp", "My Application")

@cli.command("greet", "Greet a user")
def greet(name):
    print(f"Hello, {name}!")

cli.run()
```

See [Examples](examples.md) for more pattern examples.

## 🔄 Backward Compatibility

All useful functions from previous versions are preserved:

```python
from fishertools.legacy import hash_string, generate_password, QuickConfig

password = generate_password(12)
hash_value = hash_string("my_string")
config = QuickConfig({"debug": True})
```

## Summary

Fishertools provides:

| Feature | Purpose | Example |
|---------|---------|---------|
| Error Explanation | Understand Python errors | `explain_error(e)` |
| Safe Utilities | Prevent common mistakes | `safe_get(list, index, default)` |
| Learning Tools | Learn Python concepts | `explain("list")` |
| Ready Patterns | Common programming tasks | `simple_menu({...})` |
| Backward Compatibility | Legacy function support | `generate_password(12)` |

---

**Ready to dive deeper?** Check out the [Examples](examples.md) page for practical use cases or the [API Reference](api-reference.md) for complete documentation.

Return to [Documentation Index](index.md)
