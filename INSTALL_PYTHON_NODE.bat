@echo off
REM ============================================
REM QUICK INSTALL: Python and Node.js
REM ============================================

echo ========================================
echo   Installing Python and Node.js
echo ========================================
echo.

REM Check for admin
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running with Administrator privileges...
) else (
    echo WARNING: Not running as Administrator.
    echo Some installations may require admin rights.
    echo.
)

REM Check if winget is available
winget --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: winget is not available!
    echo Please install winget from Microsoft Store.
    pause
    exit /b 1
)

echo.
echo Installing Python 3.12...
winget install --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements --silent
if errorlevel 1 (
    echo   [WARNING] Python installation had issues - may already be installed
) else (
    echo   [OK] Python installed
)

echo.
echo Installing Node.js LTS...
winget install --id OpenJS.NodeJS.LTS --accept-package-agreements --accept-source-agreements --silent
if errorlevel 1 (
    echo   [WARNING] Node.js installation had issues - may already be installed
) else (
    echo   [OK] Node.js installed
)

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo NOTE: You may need to restart your terminal
echo       or close and reopen PowerShell/CMD
echo       for the new tools to be available.
echo.
echo Verifying installations...
echo.

python --version 2>nul
if errorlevel 1 (
    echo   [MISSING] Python - restart terminal and try again
) else (
    echo   [OK] Python is available
)

node --version 2>nul
if errorlevel 1 (
    echo   [MISSING] Node.js - restart terminal and try again
) else (
    echo   [OK] Node.js is available
)

echo.
pause
