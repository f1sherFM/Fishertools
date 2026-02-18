# Getting Started

Welcome to Fishertools! This guide will help you get up and running in just a few minutes.

## Installation

The quickest way to install Fishertools is using pip:

```bash
pip install fishertools
```

For detailed installation instructions for your operating system, see the [Installation](installation.md) guide.

## Your First Example

Let's start with the main feature of Fishertools - explaining Python errors:

```python
from fishertools import explain_error

try:
    numbers = [1, 2, 3]
    print(numbers[10])  # This will cause an error
except Exception as e:
    explain_error(e)
```

**Output:**
```
🚨 Error Python: IndexError

═══ Error Message ═══
  list index out of range

═══ What This Means ═══
  You're trying to access a list element by an index that doesn't exist.
  Indexes in Python start at 0, and the maximum index equals the list length minus 1.

═══ How to Fix ═══
  Check the list length before accessing an element or use safe methods.

═══ Example ═══
┌─ Correct Code ─┐
    numbers = [1, 2, 3]
    if len(numbers) > 10:
        print(numbers[10])
    else:
        print("Index is too large!")
└─────────────────┘
```

## Safe Utilities

Fishertools provides safe functions that prevent common errors:

```python
from fishertools.safe import safe_get, safe_divide

# Safe element access
numbers = [1, 2, 3]
result = safe_get(numbers, 10, "not found")  # Returns "not found"

# Safe division
result = safe_divide(10, 0, 0)  # Returns 0 instead of error
```

## Learning Python Concepts

Learn Python concepts with structured explanations:

```python
from fishertools.learn import explain

# Get explanation of a topic
explanation = explain("list")
print(explanation["description"])
print(explanation["when_to_use"])
print(explanation["example"])
```

## Unified Learning CLI

Fishertools also provides a unified learning CLI entrypoint:

```bash
fishertools learn topic variables
fishertools learn explain list
fishertools learn quiz variables --level beginner
fishertools learn repl
```

## What's Next?

- Explore [Features](features.md) to see all capabilities
- Check [Examples](examples.md) for more practical use cases
- Read [API Reference](api-reference.md) for complete documentation
- See [Installation](installation.md) for detailed setup instructions

## Need Help?

- Check the [Limitations](limitations.md) page for known issues
- Visit the [Contributing](contributing.md) page to report issues or contribute
- Return to [Documentation Index](index.md)

---

**Ready to explore more?** Check out the [Features](features.md) page to see what Fishertools can do!
