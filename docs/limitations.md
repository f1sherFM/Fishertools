# Limitations

This page documents known limitations and constraints of Fishertools.

## explain_error() and SyntaxError

### The Problem

`explain_error()` cannot explain `SyntaxError` before code execution. This is because syntax errors are detected during the parsing phase (code analysis), which happens **before** the program runs. This means you cannot catch `SyntaxError` in a try-except block because the program won't execute at all.

### Example

```python
# This causes SyntaxError BEFORE execution
try:
    x = 5 +  # Syntax error - incomplete expression
except SyntaxError as e:
    explain_error(e)  # This code never runs
```

### Workaround

You can explain other types of errors that occur during execution:

```python
# This works - error occurs during execution
try:
    result = 10 / 0  # ZeroDivisionError
except Exception as e:
    explain_error(e)  # Works correctly
```

### Why This Limitation Exists

Python's parsing happens in two phases:
1. **Parsing Phase** - Code is analyzed for syntax errors (happens before execution)
2. **Execution Phase** - Code is run and runtime errors can be caught

Since `SyntaxError` occurs in phase 1, it prevents the program from even starting, so phase 2 never happens.

---

## explain() and Object-Oriented Programming

### The Problem

The `explain()` function currently does not support explaining object-oriented programming (OOP) concepts such as:

- Classes and objects
- Inheritance
- Polymorphism
- Encapsulation
- Class methods and properties
- Decorators
- Metaclasses

### Current Capabilities

`explain()` works with:

```python
from fishertools.learn import explain

# These work
explain("list")        # Data types
explain("for")         # Control flow
explain("function")    # Functions
explain("try")         # Error handling

# These are not supported yet
# explain("class")      # Classes
# explain("inheritance") # Inheritance
# explain("polymorphism") # Polymorphism
```

### Why This Limitation Exists

OOP concepts are more complex and require:
- Understanding of class hierarchies
- Method resolution order (MRO)
- Descriptor protocol
- Metaclass mechanics

These topics require more sophisticated explanations than the current system provides.

### Future Plans

OOP support is planned for future versions of Fishertools. The development team is working on:
- Comprehensive OOP explanations
- Interactive class diagrams
- Inheritance visualization
- Design pattern examples

---

## Performance Limitations

### Large File Operations

Reading very large files with `read_last_lines()` may be slow:

```python
from fishertools.safe import read_last_lines

# This might be slow for very large files (> 1GB)
last_lines = read_last_lines("huge_log_file.log", n=100)
```

**Workaround:** For very large files, consider using specialized tools or reading in chunks.

### Hash Calculation

Calculating file hashes for very large files takes time proportional to file size:

```python
from fishertools.safe import get_file_hash

# This might take a while for large files
hash_value = get_file_hash("large_video.mp4")
```

**Workaround:** Cache hash values and only recalculate when needed.

---

## Platform-Specific Limitations

### Windows Path Handling

Some functions may behave differently on Windows due to path separator differences:

```python
from fishertools.safe import ensure_dir

# Works on all platforms
path = ensure_dir("./data/nested/directory")

# May have issues on Windows
path = ensure_dir("C:\\Users\\Name\\data")  # Use forward slashes instead
path = ensure_dir("C:/Users/Name/data")     # Better
```

### File Encoding

Default encoding is UTF-8, which may cause issues with non-UTF-8 files:

```python
from fishertools.safe import safe_read_file

# Works for UTF-8 files
content = safe_read_file("file.txt")

# For other encodings, specify explicitly
content = safe_read_file("file.txt", encoding='latin-1')
```

---

## Python Version Compatibility

### Minimum Version

Fishertools requires Python 3.8 or higher. Features from newer Python versions may not work:

```python
# Python 3.8+ required
from fishertools import explain_error

# Some features may require Python 3.9+
# Check documentation for specific version requirements
```

### Deprecated Features

Some Python features are deprecated and may be removed in future versions:

```python
# These still work but may be removed in future Python versions
from fishertools.legacy import hash_string, generate_password
```

---

## Dependency Limitations

### External Dependencies

Fishertools depends on external packages that may have their own limitations:

- **requests** - Network-related limitations
- **click** - CLI framework limitations

### Version Conflicts

Using incompatible versions of dependencies may cause issues:

```bash
# Ensure compatible versions
pip install fishertools
# This installs compatible versions automatically
```

---

## Error Explanation Limitations

### Incomplete Error Messages

Some error messages may not be fully explained if they're custom or unusual:

```python
from fishertools import explain_error

try:
    # Custom error from third-party library
    raise ValueError("Custom error message")
except Exception as e:
    explain_error(e)  # May provide generic explanation
```

### Localization

Error explanations are currently in English only. Russian language support is planned for future versions.

---

## Storage Limitations

### JSONStorage Size

Very large JSON files may cause memory issues:

```python
from fishertools.patterns import JSONStorage

storage = JSONStorage("huge_data.json")
# Loading very large JSON files into memory may be slow
data = storage.load()
```

**Workaround:** For large datasets, consider using a database instead.

### File Permissions

JSONStorage respects file system permissions:

```python
from fishertools.patterns import JSONStorage

# May fail if you don't have write permissions
storage = JSONStorage("/root/protected/data.json")
```

---

## Logging Limitations

### SimpleLogger Performance

Logging to disk may be slow for high-frequency logging:

```python
from fishertools.patterns import SimpleLogger

logger = SimpleLogger("app.log")

# This might be slow if called millions of times
for i in range(1000000):
    logger.info(f"Message {i}")
```

**Workaround:** Use buffering or batch logging for high-frequency operations.

### Log File Size

Log files grow indefinitely and are not automatically rotated:

```python
from fishertools.patterns import SimpleLogger

logger = SimpleLogger("app.log")
# Log file will grow without limit
logger.info("Message")
```

**Workaround:** Implement log rotation manually or use a more advanced logging library.

---

## Known Issues

### Issue 1: Unicode Characters in Error Messages

Some Unicode characters may not display correctly in certain terminals:

**Status:** Known issue, workaround available
**Workaround:** Use a terminal that supports UTF-8

### Issue 2: Relative Paths in ensure_dir()

Relative paths may behave unexpectedly in some contexts:

**Status:** Known issue
**Workaround:** Use absolute paths when possible

### Issue 3: File Encoding Detection

Automatic encoding detection is not implemented:

**Status:** Known limitation
**Workaround:** Specify encoding explicitly

---

## Reporting Issues

If you encounter limitations not listed here or have suggestions for improvements:

1. Check the [Contributing](contributing.md) page
2. Visit the [GitHub Issues](https://github.com/f1sherFM/My_1st_library_python/issues)
3. Create a detailed issue report

---

Return to [Documentation Index](index.md)
