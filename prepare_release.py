#!/usr/bin/env python3
"""
Prepare release script - checks everything before publishing.
"""

import os
import sys
import subprocess
from pathlib import Path


def check_file_exists(path, description):
    """Check if a file exists."""
    if Path(path).exists():
        print(f"✅ {description}: {path}")
        return True
    else:
        print(f"❌ {description} not found: {path}")
        return False


def check_version_consistency():
    """Check that versions match in setup.py and pyproject.toml."""
    print("\n🔍 Checking version consistency...")
    
    # Read setup.py
    with open("setup.py", encoding="utf-8") as f:
        setup_content = f.read()
        import re
        setup_match = re.search(r'version="([^"]+)"', setup_content)
        setup_version = setup_match.group(1) if setup_match else None
    
    # Read pyproject.toml
    with open("pyproject.toml", encoding="utf-8") as f:
        pyproject_content = f.read()
        pyproject_match = re.search(r'version = "([^"]+)"', pyproject_content)
        pyproject_version = pyproject_match.group(1) if pyproject_match else None
    
    if setup_version == pyproject_version:
        print(f"✅ Versions match: {setup_version}")
        return True, setup_version
    else:
        print(f"❌ Version mismatch!")
        print(f"   setup.py: {setup_version}")
        print(f"   pyproject.toml: {pyproject_version}")
        return False, setup_version


def check_tests():
    """Run tests to ensure everything works."""
    print("\n🧪 Running tests...")
    
    result = subprocess.run(
        "pytest tests/ -v --tb=short",
        shell=True,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ All tests passed!")
        return True
    else:
        print("❌ Some tests failed!")
        print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
        return False


def check_dependencies():
    """Check if required tools are installed."""
    print("\n📦 Checking dependencies...")
    
    tools = {
        "python": "python --version",
        "pip": "pip --version",
        "git": "git --version",
    }
    
    all_ok = True
    for tool, cmd in tools.items():
        result = subprocess.run(cmd, shell=True, capture_output=True)
        if result.returncode == 0:
            print(f"✅ {tool} is installed")
        else:
            print(f"❌ {tool} is not installed")
            all_ok = False
    
    # Check for build and twine
    print("\n📦 Checking build tools...")
    
    try:
        import build
        print("✅ build is installed")
    except ImportError:
        print("⚠️  build is not installed. Install with: pip install build")
        all_ok = False
    
    try:
        import twine
        print("✅ twine is installed")
    except ImportError:
        print("⚠️  twine is not installed. Install with: pip install twine")
        all_ok = False
    
    return all_ok


def main():
    """Run all checks."""
    print("=" * 60)
    print("🚀 Fishertools Release Preparation Checklist")
    print("=" * 60)
    
    checks = []
    
    # Check files
    print("\n📁 Checking required files...")
    checks.append(check_file_exists("README.md", "Main README"))
    checks.append(check_file_exists("setup.py", "Setup file"))
    checks.append(check_file_exists("pyproject.toml", "Project config"))
    checks.append(check_file_exists("LICENSE", "License file"))
    checks.append(check_file_exists("CHANGELOG.md", "Changelog"))
    checks.append(check_file_exists("fishertools/__init__.py", "Package init"))
    
    # Check version consistency
    version_ok, version = check_version_consistency()
    checks.append(version_ok)
    
    # Check dependencies
    checks.append(check_dependencies())
    
    # Run tests (optional)
    print("\n🧪 Running tests (this may take a moment)...")
    try:
        test_ok = check_tests()
        checks.append(test_ok)
    except Exception as e:
        print(f"⚠️  Could not run tests: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    if all(checks):
        print("✅ All checks passed! Ready to publish.")
        print(f"\n📦 Version to publish: {version}")
        print("\nNext steps:")
        print("1. Review changes: git log --oneline -5")
        print("2. Run: python publish.py")
        print("3. Verify on PyPI: https://pypi.org/project/fishertools/")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
