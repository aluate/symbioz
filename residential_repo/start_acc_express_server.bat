@echo off
REM ACC Express - Server Launcher
REM Starts the FastAPI server for LAN access (no auto-reload)
REM
REM This script is for SERVER deployment where the app runs 24/7
REM For local development/testing, use start_prime_order.bat instead

cd /d "%~dp0"

echo ========================================
echo ACC Express Server
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo.
    echo Please create it first:
    echo   py -m venv .venv
    echo   .\.venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo Activating virtual environment...
call .venv\Scripts\activate

if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    echo.
    pause
    exit /b 1
)

echo.
echo Starting ACC Express on port 8001...
echo Server will be accessible at: http://SERVER-NAME:8001/express-order
echo.
echo Press Ctrl+C to stop the server.
echo ========================================
echo.

uvicorn apps.web.prime_order_api:app --host 0.0.0.0 --port 8001

echo.
echo ========================================
echo ACC Express server has stopped.
echo ========================================
echo.
pause

