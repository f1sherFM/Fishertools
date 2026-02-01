# Release Notes: Fishertools v0.4.4

**Release Date:** February 1, 2026

## 🎯 Overview

Version 0.4.4 represents a major code quality improvement release based on a comprehensive professional Code Review. This release focuses on type safety, security, performance, and developer experience improvements.

## ✨ Key Improvements

### 🔒 Enhanced Type Safety
- **Full type hints** with `TypeVar` and `ParamSpec` in `decorators.py`
- **Strict typing** for all decorator functions
- **Better IDE support** and autocomplete
- **Reduced runtime errors** through static type checking

### ✅ Better Input Validation
- **Parameter validation** in `ask_int()` and `ask_float()`
- **Protection against invalid ranges** (min_val > max_val)
- **Empty prompt detection**
- **Attempt limiting** to prevent infinite loops (default: 10 attempts)

### ⚡ Performance Optimizations
- **Pre-compiled regex patterns** in `helpers.py`
- **Reduced compilation overhead** for string operations
- **Faster email validation**
- **Optimized string cleaning**

### 📦 Improved Dependency Management
- **Fixed version pinning** in requirements.txt
  - `requests==2.31.0`
  - `click==8.3.1`
  - `pyyaml==6.0.1`
- **Optional dependencies** - pyyaml moved to `[config]` extra
- **Proper version ranges** in pyproject.toml (>=X.Y.Z,<X+1.0.0)

### 🛡️ Security Enhancements
- **DoS protection** - max_attempts parameter prevents infinite loops
- **Better error handling** - proper KeyboardInterrupt and EOFError handling
- **Input sanitization** - validation of all user inputs
- **Type safety** - prevents many runtime vulnerabilities

### 📚 Centralized Versioning
- **Single source of truth** - `fishertools/_version.py`
- **Consistent versioning** across setup.py, pyproject.toml, and __init__.py
- **Easier maintenance** - update version in one place

## 🔧 Technical Changes

### Modified Files
1. **fishertools/_version.py** (NEW)
   - Centralized version management
   
2. **fishertools/__init__.py**
   - Import version from _version.py
   
3. **fishertools/decorators.py**
   - Added TypeVar and ParamSpec for full type safety
   - Improved type hints for all decorators
   
4. **fishertools/helpers.py**
   - Pre-compiled regex patterns
   - Full type hints
   - Better error handling
   
5. **fishertools/input_utils.py**
   - Parameter validation (min_val, max_val, prompt)
   - max_attempts parameter (default: 10)
   - Better error messages with remaining attempts
   
6. **setup.py**
   - Import version from fishertools._version
   
7. **pyproject.toml**
   - Updated to version 0.4.4
   - Proper version ranges for dependencies
   - Optional [config] extra for pyyaml
   
8. **requirements.txt**
   - Fixed version pinning
   
9. **requirements-dev.txt**
   - Fixed version pinning

## 📊 Code Quality Metrics

### Issues Resolved from Code Review
- ✅ **HIGH:** Version inconsistency across files
- ✅ **HIGH:** Missing type hints in legacy modules
- ✅ **HIGH:** Lack of dependency version pinning
- ✅ **MEDIUM:** Insufficient input validation
- ✅ **MEDIUM:** Unoptimized regex patterns
- ✅ **LOW:** Missing parameter validation

### Test Coverage
- **815 tests** passing
- **90%+ code coverage** maintained
- **Property-based tests** with Hypothesis

## 🚀 Migration Guide

### For Users

No breaking changes! All existing code will continue to work.

**Optional improvements you can make:**

```python
# Old way (still works)
age = ask_int("Age: ", min=0, max=150)

# New way (with attempt limiting)
age = ask_int("Age: ", min_val=0, max_val=150, max_attempts=5)
```

### For Contributors

**Type hints are now required:**
```python
# Old
def my_function(x, y):
    return x + y

# New
def my_function(x: int, y: int) -> int:
    return x + y
```

**Use pre-compiled regex patterns:**
```python
# Old
import re
def clean(text):
    return re.sub(r'\s+', ' ', text)

# New
import re
_PATTERN = re.compile(r'\s+')
def clean(text: str) -> str:
    return _PATTERN.sub(' ', text)
```

## 📝 Upgrade Instructions

```bash
# Upgrade from PyPI
pip install --upgrade fishertools

# Or from source
git pull
pip install -e .
```

## 🔮 What's Next?

Version 0.4.5 will focus on:
- Further architecture improvements
- Splitting large modules (integration.py)
- More comprehensive documentation
- Additional performance optimizations

## 🙏 Acknowledgments

This release was made possible by:
- Comprehensive Code Review analysis
- Community feedback
- Automated testing with pytest and Hypothesis

## 📞 Support

- **Issues:** https://github.com/f1sherFM/My_1st_library_python/issues
- **Documentation:** See `docs/` folder
- **Changelog:** See `CHANGELOG.md`

---

**Fishertools v0.4.4** - Making Python safer, faster, and more reliable! 🐍✨
