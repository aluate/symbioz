@echo off
echo ========================================
echo   CHECKING INSTALLED TOOLS
echo ========================================
echo.

echo Checking Git...
git --version 2>nul
if errorlevel 1 (
    echo   [MISSING] Git is not installed
) else (
    echo   [OK] Git is installed
)
echo.

echo Checking GitHub CLI...
gh --version 2>nul
if errorlevel 1 (
    echo   [MISSING] GitHub CLI is not installed
) else (
    echo   [OK] GitHub CLI is installed
)
echo.

echo Checking VS Code...
code --version 2>nul
if errorlevel 1 (
    echo   [MISSING] VS Code is not installed
) else (
    echo   [OK] VS Code is installed
)
echo.

echo Checking Docker...
docker --version 2>nul
if errorlevel 1 (
    echo   [MISSING] Docker is not installed
) else (
    echo   [OK] Docker is installed
)
echo.

echo Checking winget...
winget --version 2>nul
if errorlevel 1 (
    echo   [MISSING] winget is not available
) else (
    echo   [OK] winget is available
)
echo.

echo ========================================
pause
