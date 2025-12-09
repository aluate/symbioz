@echo off
REM Symbioz CLI - Game Launcher
REM This batch file launches the Symbioz CLI game

echo ========================================
echo   SYMBIOZ - CLI Prototype MVP
echo ========================================
echo.

REM Get the directory where this batch file is located
set SCRIPT_DIR=%~dp0

REM Change to the script directory
cd /d "%SCRIPT_DIR%"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.7+ and try again.
    pause
    exit /b 1
)

REM Run the game
echo Starting game...
echo.
python main.py

REM Pause at the end so user can see any error messages
if errorlevel 1 (
    echo.
    echo Game exited with an error.
    pause
) else (
    echo.
    echo Game exited normally.
    pause
)

