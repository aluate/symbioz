@echo off
REM Build Pole Barn Calculator Executable
REM This script builds a standalone .exe using PyInstaller

cd /d "%~dp0"

echo ========================================
echo   BUILDING POLE BARN CALCULATOR EXE
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if PyInstaller is installed
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
)

REM Check if pandas is installed
python -c "import pandas" >nul 2>&1
if errorlevel 1 (
    echo pandas not found. Installing...
    pip install pandas
)

echo.
echo Building executable...
echo This may take a few minutes...
echo.

REM Build using spec file if it exists, otherwise use command line
if exist build_exe.spec (
    echo Using build_exe.spec...
    pyinstaller build_exe.spec
) else (
    echo Using command-line options...
    pyinstaller ^
      --onefile ^
      --windowed ^
      --name PoleBarnCalculator ^
      --add-data "config;config" ^
      --hidden-import pandas ^
      --hidden-import click ^
      --hidden-import tkinter ^
      apps/gui.py
)

if errorlevel 1 (
    echo.
    echo ERROR: Build failed
    echo Check the output above for details
    pause
    exit /b 1
)

echo.
echo ========================================
echo   BUILD COMPLETE
echo ========================================
echo.
echo Executable created in: dist\PoleBarnCalculator.exe
echo.
echo You can now:
echo   1. Test the exe by running it
echo   2. Create an installer using Inno Setup
echo   3. Distribute the exe or installer
echo.
pause

