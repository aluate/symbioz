@echo off
REM Pole Barn Calculator Launcher
REM This batch file runs the pole barn calculator CLI

cd /d "%~dp0"

echo ========================================
echo   POLE BARN CALCULATOR
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

REM Check if pandas is installed
python -c "import pandas" >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: pandas module not found
    echo Installing required dependencies...
    pip install pandas click
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        echo Please run: pip install pandas click
        pause
        exit /b 1
    )
    echo Dependencies installed successfully.
    echo.
)

REM If no arguments provided, show help
if "%~1"=="" (
    echo Running calculator with --help...
    echo.
    python -m apps.cli --help
    echo.
    echo ========================================
    echo   EXAMPLE COMMAND
    echo ========================================
    echo.
    echo To run a calculation, use:
    echo.
    echo python -m apps.cli ^
    echo   --project-name "Test Barn" ^
    echo   --length 40 ^
    echo   --width 30 ^
    echo   --eave-height 12 ^
    echo   --peak-height 16 ^
    echo   --roof-pitch 0.333 ^
    echo   --pole-spacing-length 10 ^
    echo   --pole-spacing-width 8 ^
    echo   --pole-diameter 6 ^
    echo   --pole-depth 4 ^
    echo   --roof-material metal ^
    echo   --wall-material metal ^
    echo   --truss-type standard ^
    echo   --truss-spacing 10 ^
    echo   --purlin-spacing 2 ^
    echo   --girt-spacing 2 ^
    echo   --foundation-type concrete_pad ^
    echo   --labor-rate 50 ^
    echo   --material-markup 1.15 ^
    echo   --tax-rate 0.08 ^
    echo   --assembly-method standard ^
    echo   --fastening-type screws
    echo.
) else (
    REM Run with provided arguments
    python -m apps.cli %*
)

echo.
pause

