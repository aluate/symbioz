@echo off
REM Test script to verify paths

set "REPO_ROOT=%~dp0"
if "%REPO_ROOT:~-1%"=="\" set "REPO_ROOT=%REPO_ROOT:~0,-1%"

echo Repo root: %REPO_ROOT%
echo.

echo Checking paths:
echo.

if exist "%REPO_ROOT%\apps\otto" (
    echo [OK] Otto directory exists
) else (
    echo [FAIL] Otto directory NOT found: %REPO_ROOT%\apps\otto
)

if exist "%REPO_ROOT%\apps\life_os\backend" (
    echo [OK] Life OS backend directory exists
) else (
    echo [FAIL] Life OS backend directory NOT found: %REPO_ROOT%\apps\life_os\backend
)

if exist "%REPO_ROOT%\apps\life_os\frontend" (
    echo [OK] Life OS frontend directory exists
) else (
    echo [FAIL] Life OS frontend directory NOT found: %REPO_ROOT%\apps\life_os\frontend
)

echo.
echo Press any key to exit...
pause >nul

