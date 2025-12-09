@echo off
REM ============================================
REM DEV MACHINE SETUP LAUNCHER
REM Double-click this file to start installation
REM ============================================

echo ========================================
echo   FRAT DEV MACHINE SETUP
echo ========================================
echo.
echo This will install:
echo   - WSL2 (Ubuntu)
echo   - Node.js, Python, Docker
echo   - Git, VS Code, GitHub CLI
echo   - Development tools and CLI utilities
echo.
echo NOTE: Some steps require Administrator privileges.
echo.
echo TIP: For full installation, right-click this file and
echo      choose "Run as administrator" OR use:
echo      INSTALL_DEV_MACHINE_AS_ADMIN.bat
echo.
pause

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Check if PowerShell is available
powershell -Command "Write-Host 'Checking PowerShell...'" >nul 2>&1
if errorlevel 1 (
    echo ERROR: PowerShell is not available!
    echo Please ensure PowerShell is installed.
    pause
    exit /b 1
)

echo.
echo Starting installation...
echo This may take several minutes.
echo.
echo A PowerShell window will open to show progress.
echo.

REM Run the setup script with execution policy bypass
powershell -ExecutionPolicy Bypass -NoProfile -File "%SCRIPT_DIR%setup.ps1"

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Run CHECK_INSTALLED_TOOLS.bat to verify what installed
echo   2. If tools are missing, run INSTALL_DEV_MACHINE_AS_ADMIN.bat
echo   3. If WSL was installed, RESTART your computer
echo   4. After restart, open WSL and run: bash setup_wsl.sh
echo   5. Run verification_checklist.md tests
echo.
pause
