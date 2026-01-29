#!/bin/bash

# Fishertools Publication Script
# Publishes to GitHub and PyPI

set -e

echo "🚀 Starting Fishertools publication process..."

# Check if we're in the right directory
if [ ! -f "setup.py" ]; then
    echo "❌ Error: setup.py not found. Please run this script from the project root."
    exit 1
fi

# Get version from setup.py
VERSION=$(grep "version=" setup.py | head -1 | sed 's/.*version="\([^"]*\)".*/\1/')
echo "📦 Publishing version: $VERSION"

# Clean up old builds
echo "🧹 Cleaning up old builds..."
rm -rf build/ dist/ *.egg-info

# Build distribution packages
echo "🔨 Building distribution packages..."
python -m build

# Check if twine is installed
if ! command -v twine &> /dev/null; then
    echo "⚠️  twine not found. Installing..."
    pip install twine
fi

# Upload to PyPI
echo "📤 Uploading to PyPI..."
twine upload dist/*

# Create git tag
echo "🏷️  Creating git tag..."
git add -A
git commit -m "Release v$VERSION" || true
git tag -a "v$VERSION" -m "Release version $VERSION" || true

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin main
git push origin "v$VERSION" || true

echo "✅ Publication complete!"
echo "📚 Package is now available at:"
echo "   - PyPI: https://pypi.org/project/fishertools/$VERSION/"
echo "   - GitHub: https://github.com/f1sherFM/My_1st_library_python/releases/tag/v$VERSION"
