# Installation

This guide covers installing Fishertools on different operating systems and configurations.

## System Requirements

- **Python:** 3.8 or higher
- **Operating System:** Linux, macOS, or Windows
- **Package Manager:** pip (comes with Python)

## Dependencies

Fishertools requires the following packages:

- requests >= 2.25.0
- click >= 8.0.0

These will be installed automatically when you install Fishertools.

## Quick Installation

The simplest way to install Fishertools is using pip:

```bash
pip install fishertools
```

## Installation by Operating System

### Linux and macOS

```bash
# Using pip (recommended)
pip install fishertools

# Using pip3 (if you have both Python 2 and 3)
pip3 install fishertools

# Using Homebrew (macOS only)
brew install python3
pip3 install fishertools
```

### Windows

```bash
# Using pip
pip install fishertools

# Using PowerShell
python -m pip install fishertools

# Using Anaconda (if you have Anaconda installed)
conda install -c conda-forge fishertools
```

## Installation from Source

If you want to install the latest development version:

```bash
# Clone the repository
git clone https://github.com/f1sherFM/My_1st_library_python.git
cd My_1st_library_python

# Install in development mode
pip install -e .
```

## Installation for Development

If you want to contribute to Fishertools:

```bash
# Clone the repository
git clone https://github.com/f1sherFM/My_1st_library_python.git
cd My_1st_library_python

# Install with development dependencies
pip install -e ".[dev]"
```

This installs additional tools for development:
- pytest >= 8.0.0 - Testing framework
- hypothesis >= 6.0.0 - Property-based testing
- black >= 24.0.0 - Code formatter
- ruff >= 0.1.0 - Linter
- mypy >= 1.8.0 - Type checker

## Verifying Installation

To verify that Fishertools is installed correctly:

```python
# Open Python interactive shell
python

# Try importing Fishertools
>>> from fishertools import explain_error
>>> print("Fishertools installed successfully!")
Fishertools installed successfully!

# Exit Python
>>> exit()
```

Or run this command:

```bash
python -c "from fishertools import explain_error; print('Fishertools installed successfully!')"
```

## Troubleshooting

### Problem: "pip: command not found"

**Solution:** Make sure Python and pip are installed and added to your PATH.

```bash
# Check Python version
python --version

# Check pip version
pip --version

# If pip is not found, install it
python -m ensurepip --upgrade
```

### Problem: "Permission denied" error

**Solution:** Use the `--user` flag to install for your user only:

```bash
pip install --user fishertools
```

Or use a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fishertools
```

### Problem: "No module named 'fishertools'"

**Solution:** Make sure Fishertools is installed in the correct Python environment:

```bash
# Check which Python is being used
which python  # On Windows: where python

# Check installed packages
pip list | grep fishertools

# Reinstall if necessary
pip install --upgrade fishertools
```

### Problem: Version conflicts

**Solution:** Use a virtual environment to isolate dependencies:

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Fishertools
pip install fishertools
```

## Virtual Environments (Recommended)

Using a virtual environment is the best practice for Python development:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install Fishertools
pip install fishertools

# Deactivate when done
deactivate
```

## Upgrading Fishertools

To upgrade to the latest version:

```bash
pip install --upgrade fishertools
```

## Uninstalling Fishertools

To remove Fishertools:

```bash
pip uninstall fishertools
```

## Version Information

**Current Status:**
- Latest version on PyPI: 0.2.1
- Development version: 0.3.1 (available from source)

To check your installed version:

```bash
pip show fishertools
```

## Next Steps

- [Getting Started](getting-started.md) - Quick start guide
- [Features](features.md) - Overview of features
- [Examples](examples.md) - Practical examples
- [API Reference](api-reference.md) - Complete API documentation

---

Return to [Documentation Index](index.md)
