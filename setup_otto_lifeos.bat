@echo off
setlocal

REM *** Setup Script - Install Dependencies ***
REM Run this once before using start_otto_lifeos_mobile.bat

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
) else (
    echo WARNING: requirements.txt not found in apps\life_os\backend
)
popd

REM *** 3. Install Life OS Frontend dependencies ***
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
) else (
    echo WARNING: package.json not found in apps\life_os\frontend
)
popd

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo You can now use start_otto_lifeos_mobile.bat to start everything.
echo.
pause

endlocal

