# Publishing Fishertools

This document describes how to publish Fishertools to PyPI and GitHub.

## Prerequisites

Before publishing, ensure you have:

1. **Python 3.8+** installed
2. **Build tools** installed:
   ```bash
   pip install build twine
   ```
3. **PyPI account** with credentials configured in `~/.pypirc`:
   ```ini
   [distutils]
   index-servers =
       pypi

   [pypi]
   repository = https://upload.pypi.org/legacy/
   username = __token__
   password = pypi-...
   ```
4. **Git** configured with GitHub access

## Publishing Steps

### Option 1: Automated Script (Recommended)

Run the automated publication script:

```bash
python publish.py
```

This script will:
1. Clean up old builds
2. Build distribution packages
3. Upload to PyPI
4. Create a git tag
5. Push to GitHub

### Option 2: Manual Steps

If you prefer to do it manually:

#### 1. Update Version

Update the version in both files:
- `setup.py`: `version="X.Y.Z"`
- `pyproject.toml`: `version = "X.Y.Z"`

#### 2. Build Distribution

```bash
python -m build
```

This creates:
- `dist/fishertools-X.Y.Z.tar.gz` (source distribution)
- `dist/fishertools-X.Y.Z-py3-none-any.whl` (wheel)

#### 3. Upload to PyPI

```bash
twine upload dist/*
```

You'll be prompted for your PyPI credentials.

#### 4. Create Git Tag

```bash
git add -A
git commit -m "Release v0.4.0"
git tag -a "v0.4.0" -m "Release version 0.4.0"
```

#### 5. Push to GitHub

```bash
git push origin main
git push origin v0.4.0
```

## Verification

After publishing, verify the package:

1. **Check PyPI**: https://pypi.org/project/fishertools/
2. **Install from PyPI**:
   ```bash
   pip install --upgrade fishertools
   ```
3. **Test the installation**:
   ```python
   import fishertools
   print(fishertools.__version__)
   ```

## Troubleshooting

### "Invalid distribution" error

Ensure your `setup.py` and `pyproject.toml` are properly configured and versions match.

### "Authentication failed" error

Check your PyPI credentials in `~/.pypirc` or use token-based authentication.

### "Tag already exists" error

If the tag already exists, delete it first:
```bash
git tag -d v0.4.0
git push origin :refs/tags/v0.4.0
```

## Release Notes

When publishing a new version:

1. Update `CHANGELOG.md` with changes
2. Update version numbers in `setup.py` and `pyproject.toml`
3. Run tests to ensure everything works:
   ```bash
   pytest
   ```
4. Run the publication script

## Current Version

Current version: **0.4.0**

Latest features:
- Knowledge Engine Interactive REPL for learning Python
- Safe code execution sandbox
- Session persistence and progress tracking
- Comprehensive error explanations
- Safe utility functions for beginners
