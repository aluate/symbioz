@echo off
REM Fresh GUI Launcher - Clears cache and launches GUI
REM Use this if run_gui.bat still shows old version

cd /d "%~dp0"

echo ========================================
echo Pole Barn Calculator - Fresh Launch
echo ========================================
echo.

echo Step 1: Clearing ALL Python cache...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
for /r . %%f in (*.pyc) do @if exist "%%f" del /q "%%f" 2>nul
echo Cache cleared!
echo.

echo Step 2: Verifying GUI file...
if exist "apps\gui.py" (
    echo ✓ GUI file found: apps\gui.py
    findstr /C:"v0.2" "apps\gui.py" >nul 2>&1
    if errorlevel 1 (
        echo ⚠ WARNING: Version string not found in GUI file!
    ) else (
        echo ✓ Version string found in GUI file
    )
) else (
    echo ✗ ERROR: apps\gui.py not found!
    pause
    exit /b 1
)
echo.

echo Step 3: Checking Python...
python --version
if errorlevel 1 (
    echo ✗ ERROR: Python not found!
    pause
    exit /b 1
)
echo.

echo Step 4: Launching GUI...
echo You should see window title: "Pole Barn Calculator - v0.2 (Path B)"
echo You should see 7 input fields (no Peak Height, no Labor Rate)
echo.
python -m apps.gui

if errorlevel 1 (
    echo.
    echo ERROR: Failed to launch GUI
    pause
)

