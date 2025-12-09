@echo off
setlocal

REM *** Start Otto + Life OS Stack for Mobile Access ***
REM This starts all three servers needed to use Otto from your phone

echo.
echo ========================================
echo   Starting Otto + Life OS Stack
echo ========================================
echo.
echo This will start:
echo   1. Otto API (port 8001)
echo   2. Life OS Backend (port 8000)
echo   3. Life OS Frontend (port 3000)
echo.
echo To access from your phone:
echo   1. Find your IP: ipconfig
echo   2. Go to: http://YOUR_IP:3000
echo.
echo ========================================
echo.

REM Get the directory where this batch file is located (repo root)
set "REPO_ROOT=%~dp0"
REM Remove trailing backslash
if "%REPO_ROOT:~-1%"=="\" set "REPO_ROOT=%REPO_ROOT:~0,-1%"

echo Repo root: %REPO_ROOT%
echo.

REM *** 1. Start Otto API server ***
echo Starting Otto API...
REM Check if Otto is installed
pushd "%REPO_ROOT%\apps\otto"
python -m otto.cli --help >nul 2>&1
if errorlevel 1 (
    echo WARNING: Otto may not be installed. Run setup_otto_lifeos.bat first.
    echo Continuing anyway...
)
popd
start "Otto API - Port 8001" /d "%REPO_ROOT%\apps\otto" cmd /k "python -m otto.cli server --host 0.0.0.0 --port 8001"

REM Wait a moment for Otto to start
timeout /t 2 /nobreak >nul

REM *** 2. Start Life OS backend (FastAPI) ***
echo Starting Life OS Backend...
REM Check if uvicorn is available
where uvicorn >nul 2>&1
if errorlevel 1 (
    echo WARNING: uvicorn may not be installed. Run setup_otto_lifeos.bat first.
    echo Continuing anyway...
)
start "Life OS Backend - Port 8000" /d "%REPO_ROOT%\apps\life_os\backend" cmd /k "uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a moment for backend to start
timeout /t 2 /nobreak >nul

REM *** 3. Start Life OS frontend (Next.js) ***
echo Starting Life OS Frontend...
REM Check if node_modules exists, if not install dependencies
if not exist "%REPO_ROOT%\apps\life_os\frontend\node_modules" (
    echo Installing frontend dependencies (first time only)...
    pushd "%REPO_ROOT%\apps\life_os\frontend"
    call npm install
    popd
)
start "Life OS Frontend - Port 3000" /d "%REPO_ROOT%\apps\life_os\frontend" cmd /k "npm run dev -- -H 0.0.0.0"

echo.
echo ========================================
echo   All servers starting!
echo ========================================
echo.
echo Three windows will open - one for each server.
echo.
echo To find your IP address for phone access:
echo   Run: ipconfig
echo   Look for "IPv4 Address"
echo.
echo Then on your phone (same Wi-Fi):
echo   Go to: http://YOUR_IP:3000
echo.
echo Press any key to close this window...
pause >nul

endlocal

