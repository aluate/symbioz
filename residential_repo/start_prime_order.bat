@echo off
REM ACC Express - Local Development Launcher
REM Starts the FastAPI server with auto-reload for development
REM
REM This script is for LOCAL DEVELOPMENT/TESTING
REM For server deployment, use start_acc_express_server.bat instead

cd /d "%~dp0"

echo ========================================
echo ACC Express - Local Development
echo ========================================
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo WARNING: Virtual environment not found!
    echo.
    echo Please create it first:
    echo   py -m venv .venv
    echo   .\.venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo Starting ACC Express with auto-reload...
echo Server will be accessible at: http://localhost:8001/express-order
echo.
echo Press Ctrl+C in the server window to stop.
echo ========================================
echo.

start "ACC Express Server" cmd /k "cd /d %~dp0 && call .venv\Scripts\activate && uvicorn apps.web.prime_order_api:app --reload --host 0.0.0.0 --port 8001"

timeout /t 3 >nul
echo Opening browser...
start "" "http://localhost:8001/express-order"

echo.
echo Server is starting. The browser should open automatically.
echo To stop the server, close the "ACC Express Server" window.
pause
