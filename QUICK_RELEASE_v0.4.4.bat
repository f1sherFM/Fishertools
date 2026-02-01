@echo off
REM Quick Release Script for Fishertools v0.4.4 (Windows)
REM Run this script to publish the new version

echo.
echo ========================================
echo    Fishertools v0.4.4 Release Script
echo ========================================
echo.

REM Step 1: Verify version
echo [Step 1] Verifying version...
python -c "import fishertools; print(f'Version: {fishertools.__version__}')"
python -c "import fishertools; exit(0 if fishertools.__version__ == '0.4.4' else 1)"
if errorlevel 1 (
    echo [ERROR] Version mismatch! Expected 0.4.4
    exit /b 1
)
echo [OK] Version confirmed: 0.4.4
echo.

REM Step 2: Run tests
echo [Step 2] Running core tests...
python -m pytest tests/test_safe/ tests/test_errors/ tests/test_learn/ tests/test_validation/ tests/test_visualization/ tests/test_debug/ tests/test_input_utils/ -q --tb=no
if errorlevel 1 (
    echo [ERROR] Tests failed!
    exit /b 1
)
echo [OK] All core tests passed!
echo.

REM Step 3: Clean previous builds
echo [Step 3] Cleaning previous builds...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.egg-info rmdir /s /q *.egg-info
echo [OK] Cleaned!
echo.

REM Step 4: Build package
echo [Step 4] Building package...
python -m build
if errorlevel 1 (
    echo [ERROR] Build failed!
    exit /b 1
)
echo [OK] Package built!
echo.

REM Step 5: Check package
echo [Step 5] Checking package...
twine check dist/*
if errorlevel 1 (
    echo [ERROR] Package check failed!
    exit /b 1
)
echo [OK] Package is valid!
echo.

REM Step 6: Upload to PyPI (with confirmation)
echo [Step 6] Ready to upload to PyPI
set /p CONFIRM="Do you want to upload to PyPI? (yes/no): "
if /i "%CONFIRM%"=="yes" (
    echo Uploading to PyPI...
    twine upload dist/*
    if errorlevel 1 (
        echo [ERROR] Upload failed!
        exit /b 1
    )
    echo [OK] Uploaded to PyPI!
) else (
    echo [SKIP] PyPI upload skipped
)
echo.

REM Step 7: Create Git tag
echo [Step 7] Creating Git tag...
set /p CONFIRM_TAG="Do you want to create Git tag v0.4.4? (yes/no): "
if /i "%CONFIRM_TAG%"=="yes" (
    git tag -a v0.4.4 -m "Release v0.4.4: Professional Code Quality Improvements"
    git push origin v0.4.4
    echo [OK] Git tag created and pushed!
) else (
    echo [SKIP] Git tag skipped
)
echo.

REM Step 8: Summary
echo ========================================
echo    Release Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Create GitHub Release at:
echo    https://github.com/f1sherFM/My_1st_library_python/releases/new
echo.
echo 2. Use content from RELEASE_v0.4.4.md
echo.
echo 3. Verify installation:
echo    pip install --upgrade fishertools
echo    python -c "import fishertools; print(fishertools.__version__)"
echo.
echo Fishertools v0.4.4 is live!
echo.
pause
