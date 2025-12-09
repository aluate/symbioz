@echo off
REM Pole Barn Calculator GUI Launcher
REM This batch file launches the GUI application

cd /d "%~dp0"

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

echo Clearing Python cache to ensure latest code is used...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
for /r . %%f in (*.pyc) do @if exist "%%f" del /q "%%f" 2>nul
echo Cache cleared.
echo.

echo Launching Pole Barn Calculator GUI...
echo.

python -m apps.gui

if errorlevel 1 (
    echo.
    echo ERROR: Failed to launch GUI
    pause
)

