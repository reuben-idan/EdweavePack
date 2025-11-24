@echo off
echo ========================================
echo EdweavePack Registration Test
echo ========================================

:: Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

:: Check if backend is running
echo Checking if backend is running...
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Backend server is not running
    echo Please start the backend server first:
    echo   cd backend
    echo   uvicorn main:app --reload
    pause
    exit /b 1
)

echo Backend server is running ✓

:: Run registration tests
echo.
echo Running comprehensive registration tests...
python test-registration.py --url http://localhost:8000 --save-report

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ✅ All registration tests passed!
    echo Registration system is working properly for all user types.
    echo ========================================
) else (
    echo.
    echo ========================================
    echo ❌ Some registration tests failed!
    echo Please check the output above for details.
    echo ========================================
)

echo.
echo Test report saved to registration_test_report.json
pause