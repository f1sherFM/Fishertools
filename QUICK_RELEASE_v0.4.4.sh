#!/bin/bash
# Quick Release Script for Fishertools v0.4.4
# Run this script to publish the new version

set -e  # Exit on error

echo "🚀 Fishertools v0.4.4 Release Script"
echo "===================================="
echo ""

# Step 1: Verify version
echo "📋 Step 1: Verifying version..."
VERSION=$(python -c "import fishertools; print(fishertools.__version__)")
if [ "$VERSION" != "0.4.4" ]; then
    echo "❌ Error: Version mismatch! Expected 0.4.4, got $VERSION"
    exit 1
fi
echo "✅ Version confirmed: $VERSION"
echo ""

# Step 2: Run tests
echo "🧪 Step 2: Running core tests..."
python -m pytest tests/test_safe/ tests/test_errors/ tests/test_learn/ tests/test_validation/ tests/test_visualization/ tests/test_debug/ tests/test_input_utils/ -q --tb=no
if [ $? -ne 0 ]; then
    echo "❌ Error: Tests failed!"
    exit 1
fi
echo "✅ All core tests passed!"
echo ""

# Step 3: Clean previous builds
echo "🧹 Step 3: Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info
echo "✅ Cleaned!"
echo ""

# Step 4: Build package
echo "📦 Step 4: Building package..."
python -m build
if [ $? -ne 0 ]; then
    echo "❌ Error: Build failed!"
    exit 1
fi
echo "✅ Package built!"
echo ""

# Step 5: Check package
echo "🔍 Step 5: Checking package..."
twine check dist/*
if [ $? -ne 0 ]; then
    echo "❌ Error: Package check failed!"
    exit 1
fi
echo "✅ Package is valid!"
echo ""

# Step 6: Upload to PyPI (with confirmation)
echo "📤 Step 6: Ready to upload to PyPI"
read -p "Do you want to upload to PyPI? (yes/no): " CONFIRM
if [ "$CONFIRM" = "yes" ]; then
    echo "Uploading to PyPI..."
    twine upload dist/*
    if [ $? -ne 0 ]; then
        echo "❌ Error: Upload failed!"
        exit 1
    fi
    echo "✅ Uploaded to PyPI!"
else
    echo "⏭️  Skipped PyPI upload"
fi
echo ""

# Step 7: Create Git tag
echo "🏷️  Step 7: Creating Git tag..."
read -p "Do you want to create Git tag v0.4.4? (yes/no): " CONFIRM_TAG
if [ "$CONFIRM_TAG" = "yes" ]; then
    git tag -a v0.4.4 -m "Release v0.4.4: Professional Code Quality Improvements"
    git push origin v0.4.4
    echo "✅ Git tag created and pushed!"
else
    echo "⏭️  Skipped Git tag"
fi
echo ""

# Step 8: Summary
echo "🎉 Release Complete!"
echo "==================="
echo ""
echo "Next steps:"
echo "1. Create GitHub Release at:"
echo "   https://github.com/f1sherFM/My_1st_library_python/releases/new"
echo ""
echo "2. Use content from RELEASE_v0.4.4.md"
echo ""
echo "3. Verify installation:"
echo "   pip install --upgrade fishertools"
echo "   python -c 'import fishertools; print(fishertools.__version__)'"
echo ""
echo "✨ Fishertools v0.4.4 is live!"
