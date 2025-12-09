@echo off
REM Symbioz CLI - Game Launcher (from project root)
REM This batch file launches the Symbioz CLI game from the project root

echo ========================================
echo   SYMBIOZ - CLI Prototype MVP
echo ========================================
echo.

REM Get the directory where this batch file is located (project root)
set PROJECT_ROOT=%~dp0

REM Change to the CLI directory
cd /d "%PROJECT_ROOT%apps\symbioz_cli"

REM Check if the directory exists
if not exist "main.py" (
    echo ERROR: Could not find game files.
    echo Expected location: %PROJECT_ROOT%apps\symbioz_cli\main.py
    pause
    exit /b 1
)

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

