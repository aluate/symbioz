@echo off
REM ============================================
REM DEV MACHINE SETUP LAUNCHER (ADMIN VERSION)
REM This version requests Administrator privileges
REM ============================================

REM Check for admin privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running with Administrator privileges...
    goto :run
) else (
    echo Requesting Administrator privileges...
    echo.
    REM Re-run as admin
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:run
echo ========================================
echo   FRAT DEV MACHINE SETUP (ADMIN)
echo ========================================
echo.
echo This will install:
echo   - WSL2 (Ubuntu)
echo   - Node.js, Python, Docker
echo   - Git, VS Code, GitHub CLI
echo   - Development tools and CLI utilities
echo.
echo Running as Administrator - all features enabled.
echo.
pause

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo.
echo Starting installation...
echo This may take several minutes.
echo.

REM Run the setup script with execution policy bypass
powershell -ExecutionPolicy Bypass -NoProfile -File "%SCRIPT_DIR%setup.ps1"

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. If WSL was installed, RESTART your computer
echo   2. After restart, open WSL and run: bash setup_wsl.sh
echo   3. Run CHECK_INSTALLED_TOOLS.bat to verify
echo.
pause
