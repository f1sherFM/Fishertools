# Contributing

Thank you for your interest in contributing to Fishertools! This guide will help you get started.

## How to Contribute

There are many ways to contribute to Fishertools:

- **Report bugs** - Found an issue? Let us know!
- **Suggest features** - Have an idea? We'd love to hear it!
- **Write code** - Fix bugs or implement new features
- **Improve documentation** - Help make docs clearer and more complete
- **Write tests** - Improve test coverage
- **Share examples** - Show how you use Fishertools

## Getting Started

### 1. Fork the Repository

```bash
# Visit https://github.com/f1sherFM/My_1st_library_python
# Click "Fork" button
```

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/My_1st_library_python.git
cd My_1st_library_python
```

### 3. Create a Branch

```bash
# Create a branch for your feature or fix
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 4. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

## Development Workflow

### Code Style

Fishertools follows PEP 8 style guidelines. Use Black for formatting:

```bash
# Format code
black fishertools tests

# Check style
ruff check fishertools
```

### Type Hints

Use type hints in your code:

```python
def safe_get(collection: list, index: int, default: any) -> any:
    """Get element safely from collection."""
    try:
        return collection[index]
    except (IndexError, KeyError):
        return default
```

### Documentation

Write docstrings for all functions and classes:

```python
def explain_error(exception: Exception) -> None:
    """
    Explain a Python error in clear language.
    
    Args:
        exception: The exception object to explain
        
    Returns:
        None (prints explanation to console)
        
    Example:
        >>> try:
        ...     x = [1, 2, 3][10]
        ... except Exception as e:
        ...     explain_error(e)
    """
    pass
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_safe.py

# Run with coverage
pytest --cov=fishertools

# Run property-based tests
pytest -k "property"
```

### Writing Tests

Write both unit tests and property-based tests:

```python
# Unit test
def test_safe_get_with_valid_index():
    """Test safe_get with valid index."""
    result = safe_get([1, 2, 3], 0, "default")
    assert result == 1

# Property-based test
from hypothesis import given
from hypothesis import strategies as st

@given(st.lists(st.integers()), st.integers())
def test_safe_get_never_raises(items, index):
    """Test that safe_get never raises an exception."""
    result = safe_get(items, index, "default")
    assert result is not None
```

### Test Coverage

Aim for high test coverage:

```bash
# Check coverage
pytest --cov=fishertools --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Commit Guidelines

### Commit Messages

Write clear, descriptive commit messages:

```bash
# Good
git commit -m "Add safe_get function for list access"
git commit -m "Fix IndexError in explain_error"
git commit -m "Improve documentation for API reference"

# Avoid
git commit -m "Fix stuff"
git commit -m "Update"
```

### Commit Size

Keep commits focused and reasonably sized:

```bash
# Good - one feature per commit
git commit -m "Add safe_divide function"

# Avoid - too many changes
git commit -m "Add safe_divide, fix bugs, update docs, refactor code"
```

## Pull Request Process

### 1. Push Your Branch

```bash
git push origin feature/your-feature-name
```

### 2. Create Pull Request

- Go to GitHub repository
- Click "New Pull Request"
- Select your branch
- Fill in the PR template

### 3. PR Description

Include:

- **What** - What does this PR do?
- **Why** - Why is this change needed?
- **How** - How does it work?
- **Tests** - What tests were added?
- **Checklist** - Verify all items

### 4. PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Related Issues
Fixes #123

## Testing
- [ ] Added unit tests
- [ ] Added property-based tests
- [ ] All tests pass
- [ ] Coverage maintained

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Commit messages are clear
```

### 5. Code Review

- Maintainers will review your PR
- Address feedback and make changes
- Push updates to the same branch
- PR will be merged when approved

## Reporting Issues

### Bug Reports

Include:

1. **Description** - What's the problem?
2. **Steps to Reproduce** - How to reproduce the bug?
3. **Expected Behavior** - What should happen?
4. **Actual Behavior** - What actually happens?
5. **Environment** - Python version, OS, etc.
6. **Code Example** - Minimal code that reproduces the issue

### Feature Requests

Include:

1. **Description** - What feature do you want?
2. **Use Case** - Why do you need it?
3. **Example** - How would you use it?
4. **Alternatives** - Any alternatives you considered?

## Documentation Contributions

### Improving Docs

1. Fork the repository
2. Edit documentation files in `docs/`
3. Test locally: `sphinx-build -b html docs docs/_build`
4. Create a pull request

### Adding Examples

1. Add example to `docs/examples.md`
2. Include explanation and output
3. Test that code actually works
4. Create a pull request

## Code Review Guidelines

When reviewing code:

- **Be respectful** - Treat contributors with respect
- **Be constructive** - Provide helpful feedback
- **Be specific** - Point out exact issues
- **Be encouraging** - Acknowledge good work

## Community Guidelines

### Be Respectful

- Treat all contributors with respect
- Welcome diverse perspectives
- Avoid harassment or discrimination

### Be Constructive

- Provide helpful feedback
- Suggest improvements
- Help others learn

### Be Inclusive

- Welcome new contributors
- Help beginners get started
- Create a welcoming environment

## Development Tools

### Useful Commands

```bash
# Format code
black fishertools tests

# Check style
ruff check fishertools

# Type checking
mypy fishertools

# Run tests
pytest

# Run with coverage
pytest --cov=fishertools

# Build documentation
sphinx-build -b html docs docs/_build
```

### IDE Setup

**VS Code:**
```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true
}
```

**PyCharm:**
- Settings → Project → Python Code Style → Code Style
- Set to PEP 8
- Enable Black integration

## Release Process

### Version Numbering

Fishertools uses semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR** - Breaking changes
- **MINOR** - New features (backward compatible)
- **PATCH** - Bug fixes

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG updated
- [ ] Version number updated
- [ ] Tag created
- [ ] Package published to PyPI

## Getting Help

- **Questions?** - Open a discussion on GitHub
- **Issues?** - Create an issue on GitHub
- **Ideas?** - Start a discussion
- **Chat?** - Join our community

## Recognition

Contributors are recognized in:

- `CONTRIBUTORS.md` file
- Release notes
- GitHub contributors page

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## Quick Reference

| Task | Command |
|------|---------|
| Fork repo | Click "Fork" on GitHub |
| Clone fork | `git clone <your-fork-url>` |
| Create branch | `git checkout -b feature/name` |
| Install dev deps | `pip install -e ".[dev]"` |
| Format code | `black fishertools tests` |
| Check style | `ruff check fishertools` |
| Run tests | `pytest` |
| Check coverage | `pytest --cov=fishertools` |
| Push changes | `git push origin feature/name` |
| Create PR | Go to GitHub and click "New Pull Request" |

---

Thank you for contributing to Fishertools! 🙏

Return to [Documentation Index](index.md)
