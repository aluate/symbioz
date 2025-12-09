@echo off
REM ============================================
REM ADMIN SETUP LAUNCHER
REM This requests admin and runs setup
REM ============================================

REM Check if already admin
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running with Administrator privileges...
    goto :run
)

REM Request admin elevation
echo Requesting Administrator privileges...
echo You will see a UAC prompt - click YES
echo.
powershell -Command "Start-Process '%~f0' -Verb RunAs"
exit /b

:run
echo ========================================
echo   FRAT DEV MACHINE SETUP (ADMIN)
echo ========================================
echo.
echo Running as Administrator - all features enabled.
echo.

REM Change to script directory
cd /d "%~dp0"

REM Run PowerShell script
powershell.exe -ExecutionPolicy Bypass -NoProfile -File ".\setup.ps1"

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
pause
