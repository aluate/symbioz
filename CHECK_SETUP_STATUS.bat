@echo off
echo ========================================
echo   SETUP STATUS CHECK
echo ========================================
echo.

echo Checking installed tools...
echo.

echo [1/6] Git...
git --version 2>nul
if errorlevel 1 (
    echo   [MISSING] Git
) else (
    echo   [OK] Git installed
)
echo.

echo [2/6] GitHub CLI...
gh --version 2>nul
if errorlevel 1 (
    echo   [MISSING] GitHub CLI
) else (
    echo   [OK] GitHub CLI installed
)
echo.

echo [3/6] VS Code...
code --version 2>nul
if errorlevel 1 (
    echo   [MISSING] VS Code
) else (
    echo   [OK] VS Code installed
)
echo.

echo [4/6] Docker...
docker --version 2>nul
if errorlevel 1 (
    echo   [MISSING] Docker
) else (
    echo   [OK] Docker installed
)
echo.

echo [5/6] Python...
python --version 2>nul
if errorlevel 1 (
    echo   [MISSING] Python - may need to restart terminal
) else (
    echo   [OK] Python installed
)
echo.

echo [6/6] Node.js...
node --version 2>nul
if errorlevel 1 (
    echo   [MISSING] Node.js - may need to restart terminal
) else (
    echo   [OK] Node.js installed
)
echo.

echo ========================================
echo   SUMMARY
echo ========================================
echo.
echo If tools show as MISSING:
echo   1. Wait for installer to finish (check the installer window)
echo   2. Close and reopen this terminal window
echo   3. Run this check again
echo.
echo If still missing after restart:
echo   - Run INSTALL_DEV_MACHINE_AS_ADMIN.bat again
echo.
pause
