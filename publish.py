#!/usr/bin/env python3
"""
Fishertools Publication Script

Publishes the package to PyPI and creates a GitHub release.
"""

import os
import sys
import subprocess
import re
from pathlib import Path


def run_command(cmd, description):
    """Run a shell command and handle errors."""
    print(f"\n{description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Details: {e.stderr}")
        return False


def get_version():
    """Extract version from setup.py."""
    setup_path = Path("setup.py")
    if not setup_path.exists():
        print("❌ Error: setup.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    with open(setup_path) as f:
        content = f.read()
        match = re.search(r'version="([^"]+)"', content)
        if match:
            return match.group(1)
    
    print("❌ Error: Could not find version in setup.py")
    sys.exit(1)


def main():
    """Main publication workflow."""
    print("🚀 Starting Fishertools publication process...")
    
    # Get version
    version = get_version()
    print(f"📦 Publishing version: {version}")
    
    # Clean up old builds
    if not run_command("rm -rf build/ dist/ *.egg-info", "🧹 Cleaning up old builds"):
        print("⚠️  Warning: Could not clean up old builds")
    
    # Build distribution packages
    if not run_command("python -m build", "🔨 Building distribution packages"):
        print("❌ Build failed. Make sure you have 'build' installed: pip install build")
        sys.exit(1)
    
    # Check if twine is installed
    result = subprocess.run("twine --version", shell=True, capture_output=True)
    if result.returncode != 0:
        print("⚠️  twine not found. Installing...")
        if not run_command("pip install twine", "📦 Installing twine"):
            sys.exit(1)
    
    # Upload to PyPI
    if not run_command("twine upload dist/*", "📤 Uploading to PyPI"):
        print("❌ Upload to PyPI failed")
        sys.exit(1)
    
    # Git operations
    print("\n🔧 Preparing git operations...")
    
    # Check if git is available
    result = subprocess.run("git --version", shell=True, capture_output=True)
    if result.returncode != 0:
        print("⚠️  Git not found. Skipping git operations.")
        print("✅ Package published to PyPI successfully!")
        print(f"📚 Available at: https://pypi.org/project/fishertools/{version}/")
        return
    
    # Add and commit
    run_command("git add -A", "📝 Staging changes")
    run_command(f'git commit -m "Release v{version}"', "💾 Committing changes")
    
    # Create tag
    run_command(f'git tag -a "v{version}" -m "Release version {version}"', "🏷️  Creating git tag")
    
    # Push to GitHub
    run_command("git push origin main", "📤 Pushing to GitHub (main branch)")
    run_command(f'git push origin "v{version}"', "📤 Pushing tag to GitHub")
    
    # Success message
    print("\n" + "="*60)
    print("✅ Publication complete!")
    print("="*60)
    print(f"\n📚 Package is now available at:")
    print(f"   PyPI: https://pypi.org/project/fishertools/{version}/")
    print(f"   GitHub: https://github.com/f1sherFM/My_1st_library_python/releases/tag/v{version}")
    print("\n🎉 Thank you for using Fishertools!")


if __name__ == "__main__":
    main()
