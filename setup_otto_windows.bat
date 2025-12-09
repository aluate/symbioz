@echo off
setlocal

REM *** Setup Script - Install All Otto Dependencies ***
REM Run this once to set up Otto + Life OS
REM Grandma-friendly: just double-click this file

echo.
echo ========================================
echo   Setting Up Otto + Life OS
echo ========================================
echo.
echo This will install all dependencies needed.
echo.

REM Get the directory where this batch file is located (repo root)
set "REPO_ROOT=%~dp0"
if "%REPO_ROOT:~-1%"=="\" set "REPO_ROOT=%REPO_ROOT:~0,-1%"

echo Repo root: %REPO_ROOT%
echo.

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check for pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not installed
    echo Please install pip and try again
    pause
    exit /b 1
)

REM Check for Node.js (optional but recommended)
node --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Node.js not found. Frontend setup will be skipped.
    echo Install Node.js from https://nodejs.org/ if you want the frontend.
    set SKIP_FRONTEND=1
) else (
    set SKIP_FRONTEND=0
)

REM *** 1. Install Otto dependencies ***
echo.
echo [1/3] Installing Otto dependencies...
pushd "%REPO_ROOT%\apps\otto"
if exist "requirements.txt" (
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install Otto dependencies
        pause
        exit /b 1
    )
    echo ✓ Otto dependencies installed
) else (
    echo WARNING: requirements.txt not found in apps\otto
)
popd

REM *** 2. Install Life OS Backend dependencies ***
echo.
echo [2/3] Installing Life OS Backend dependencies...
pushd "%REPO_ROOT%\apps\life_os\backend"
if exist "requirements.txt" (
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install Life OS Backend dependencies
        pause
        exit /b 1
    )
    echo ✓ Life OS Backend dependencies installed
) else (
    echo WARNING: requirements.txt not found in apps\life_os\backend
)
popd

REM *** 3. Install Life OS Frontend dependencies ***
if "%SKIP_FRONTEND%"=="0" (
    echo.
    echo [3/3] Installing Life OS Frontend dependencies...
    pushd "%REPO_ROOT%\apps\life_os\frontend"
    if exist "package.json" (
        call npm install
        if errorlevel 1 (
            echo ERROR: Failed to install Life OS Frontend dependencies
            pause
            exit /b 1
        )
        echo ✓ Life OS Frontend dependencies installed
    ) else (
        echo WARNING: package.json not found in apps\life_os\frontend
    )
    popd
) else (
    echo.
    echo [3/3] Skipping Frontend (Node.js not found)
)

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Run START_OTTO_WINDOWS.bat to start everything
echo   2. Open http://localhost:3000/otto in your browser
echo   3. Start talking to Otto!
echo.
pause

endlocal

