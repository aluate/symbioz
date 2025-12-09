@echo off
echo ========================================
echo Running SETUP_NEW_COMPUTER.ps1
echo ========================================
echo.

cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -NoProfile -File "SETUP_NEW_COMPUTER.ps1"

echo.
echo ========================================
echo Setup script completed
echo ========================================
echo.
echo Checking installations...
echo.

python --version 2>nul && echo Python: OK || echo Python: NOT FOUND
node --version 2>nul && echo Node.js: OK || echo Node.js: NOT FOUND
npm --version 2>nul && echo npm: OK || echo npm: NOT FOUND

echo.
pause
