# Best Practices for Interactive Examples

This guide provides best practices for creating high-quality interactive examples for Fishertools documentation.

## Overview

Interactive examples are a crucial part of the documentation. They help users understand how to use Fishertools by showing real, working code. This guide ensures all examples are clear, correct, and helpful.

## Code Quality

### 1. Keep Examples Simple

**Good**: Focus on one concept per example
```python
from fishertools.safe import safe_get

data = {"name": "Alice"}
result = safe_get(data, "name")
print(result)  # Output: Alice
```

**Avoid**: Multiple concepts in one example
```python
from fishertools.safe import safe_get
from fishertools.errors import explain_error
import json

data = json.loads('{"name": "Alice"}')
result = safe_get(data, "name")
try:
    value = data["missing"]
except KeyError as e:
    explain_error(e)
```

### 2. Make Code Executable

**Good**: Code that runs without external dependencies
```python
from fishertools.errors import explain_error

try:
    x = 1 / 0
except ZeroDivisionError as e:
    explain_error(e)
```

**Avoid**: Code that requires external setup
```python
# This requires a database connection
result = database.query("SELECT * FROM users")
```

### 3. Show Expected Output

**Good**: Include output so users can verify
```python
from fishertools.safe import safe_divide

result = safe_divide(10, 2)
print(result)  # Output: 5.0
```

**Avoid**: Code without output
```python
from fishertools.safe import safe_divide

result = safe_divide(10, 2)
```

### 4. Use Comments Wisely

**Good**: Comments explain the "why"
```python
from fishertools.safe import safe_get

# Use safe_get to avoid KeyError when accessing nested data
data = {"user": {"name": "Alice"}}
name = safe_get(data, "user.name", default="Unknown")
print(name)  # Output: Alice
```

**Avoid**: Obvious comments
```python
# Get the name
name = safe_get(data, "name")
```

## Explanation Quality

### 1. Use Simple Language

**Good**: Clear, beginner-friendly explanation
```
The safe_divide() function performs division safely. If you try to divide by zero,
instead of crashing with an error, it returns a default value (usually 0).
This is useful when you're processing data and want to handle division by zero gracefully.
```

**Avoid**: Technical jargon
```
The safe_divide() function implements exception handling for ZeroDivisionError
by utilizing a default parameter mechanism to return a fallback value.
```

### 2. Explain the "Why"

**Good**: Explains when and why to use this
```
Use safe_divide() when:
- Processing data from external sources where division by zero might occur
- You want to avoid try-except blocks for simple operations
- You need a default value instead of an error
```

**Avoid**: Just describing what it does
```
safe_divide() divides two numbers.
```

### 3. Start with Basics

**Good**: Progressive complexity
```
# Basic usage
result = safe_divide(10, 2)  # Output: 5.0

# With zero division
result = safe_divide(10, 0)  # Output: 0

# With custom default
result = safe_divide(10, 0, default=-1)  # Output: -1
```

**Avoid**: Complex examples first
```
# Advanced usage with custom error handling
result = safe_divide(
    calculate_value(data),
    get_divisor(config),
    default=handle_error()
)
```

## Organization

### 1. One Concept Per Example

**Good**: Focused examples
- `safe-division.md` - How to use safe_divide()
- `safe-get-nested.md` - How to access nested data safely
- `error-explanation.md` - How to understand errors

**Avoid**: Mixed concepts
- `safe-operations-and-error-handling.md` - Too broad

### 2. Progressive Difficulty

**Good**: Order by complexity
1. Beginner: Basic usage
2. Intermediate: Common patterns
3. Advanced: Edge cases and optimization

**Avoid**: Random ordering

### 3. Consistent Formatting

**Good**: Follow the template
```markdown
# Example: [Title]

**Module**: [module]
**Difficulty**: [level]
**Tags**: [tags]

## Code
...

## Expected Output
...

## Explanation
...
```

**Avoid**: Inconsistent structure

### 4. Appropriate Tags

**Good**: Specific, searchable tags
```
**Tags**: division, error-handling, safe-operations, numeric
```

**Avoid**: Vague tags
```
**Tags**: stuff, things, examples
```

## Testing Examples

### 1. Test Locally

Before submitting an example:
1. Copy the code into a Python file
2. Run it to verify it works
3. Check that output matches expected output
4. Test with different inputs if applicable

### 2. Verify Syntax

```bash
python -m py_compile example.py
```

### 3. Check for Errors

```bash
python example.py
```

## Common Mistakes

### 1. Incomplete Output

**Wrong**:
```python
from fishertools.safe import safe_get

data = {"name": "Alice"}
result = safe_get(data, "name")
print(result)
```

**Right**:
```python
from fishertools.safe import safe_get

data = {"name": "Alice"}
result = safe_get(data, "name")
print(result)  # Output: Alice
```

### 2. Missing Explanation

**Wrong**: Just code with no explanation

**Right**: Code with clear explanation of what it does and why

### 3. Too Complex

**Wrong**: Example that tries to show too many features

**Right**: Example that focuses on one feature

### 4. Incorrect Output

**Wrong**: Expected output that doesn't match actual output

**Right**: Verified output that matches actual execution

## Module-Specific Guidelines

### Errors Module

Examples should show:
- How to use `explain_error()` to understand errors
- Common error types and their meanings
- How to handle different error scenarios

### Safe Module

Examples should show:
- How to use safe operations to prevent errors
- When to use safe operations vs try-except
- Default values and error handling

### Learn Module

Examples should show:
- How to use learning tools
- How to track learning progress
- How to use learning patterns

### Patterns Module

Examples should show:
- Common design patterns
- How to implement patterns
- When to use each pattern

### Config Module

Examples should show:
- How to configure Fishertools
- Configuration options and their effects
- How to load and save configurations

### Documentation Module

Examples should show:
- How to generate documentation
- How to customize documentation
- How to integrate documentation with your project

## Accessibility

### 1. Use Descriptive Titles

**Good**: "Safe Division with Default Values"
**Avoid**: "Example 1"

### 2. Include Alt Text for Diagrams

If your example includes diagrams, provide alt text:
```markdown
![Diagram showing safe_divide() flow](diagram.png)
*Alt text: Flow diagram showing how safe_divide() handles division by zero*
```

### 3. Use Semantic Formatting

**Good**: Use markdown formatting appropriately
```markdown
- Use **bold** for emphasis
- Use `code` for code references
- Use > for important notes
```

### 4. Provide Context

Always explain:
- What the example demonstrates
- When to use this pattern
- How it relates to other examples

## Review Checklist

Before submitting an example, verify:

- [ ] Code is syntactically correct
- [ ] Code runs without errors
- [ ] Output matches expected output
- [ ] Explanation is clear and beginner-friendly
- [ ] Example focuses on one concept
- [ ] Tags are appropriate and searchable
- [ ] Difficulty level is accurate
- [ ] Module is correct
- [ ] Template structure is followed
- [ ] No external dependencies required
- [ ] Comments are helpful, not obvious
- [ ] Related examples are linked

## Questions?

If you have questions about creating examples:
1. Check the [Example Template](../interactive-examples/TEMPLATE.md)
2. Review existing examples in your module
3. Ask in the community

## Contributing

To contribute examples:
1. Create a new markdown file following the template
2. Ensure code is tested and working
3. Follow the best practices in this guide
4. Submit for review

Thank you for helping improve Fishertools documentation!
