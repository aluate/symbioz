@echo off
REM Symbioz Game Launcher
REM Starts API server, then opens web UI

echo ========================================
echo   SYMBIOZ - Game Launcher
echo ========================================
echo.

REM Get the directory where this batch file is located (repo root)
set "REPO_ROOT=%~dp0"
if "%REPO_ROOT:~-1%"=="\" set "REPO_ROOT=%REPO_ROOT:~0,-1%"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    pause
    exit /b 1
)

echo [1/3] Installing Python dependencies...
cd /d "%REPO_ROOT%\apps\symbioz_cli"
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)

echo [2/3] Installing Node.js dependencies...
cd /d "%REPO_ROOT%\apps\symbioz_web"
if not exist "node_modules" (
    echo Installing npm packages...
    call npm install
    if errorlevel 1 (
        echo ERROR: Failed to install Node.js dependencies
        pause
        exit /b 1
    )
)

echo [3/3] Starting services...
echo.

REM Start API server in new window
echo Starting API server on port 8002...
start "Symbioz API Server" cmd /k "cd /d %REPO_ROOT%\apps\symbioz_cli && call venv\Scripts\activate.bat && python api_server.py"
timeout /t 3 /nobreak >nul

REM Start web UI in new window
echo Starting web UI on port 3001...
start "Symbioz Web UI" cmd /k "cd /d %REPO_ROOT%\apps\symbioz_web && set PORT=3001 && npm run dev"
timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo   Services Starting!
echo ========================================
echo.
echo API Server: http://localhost:8002
echo Web UI: http://localhost:3001
echo.
echo Press any key to open the game in your browser...
pause >nul

start http://localhost:3001

echo.
echo All services are running in separate windows.
echo Close those windows to stop the services.
echo.

