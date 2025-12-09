@echo off
REM Start all Otto services
REM This starts: Otto API, Life OS Backend, Life OS Frontend

echo Starting Otto + Life OS services...
echo.

REM Get the directory where this batch file is located (repo root)
set "REPO_ROOT=%~dp0"
if "%REPO_ROOT:~-1%"=="\" set "REPO_ROOT=%REPO_ROOT:~0,-1%"

REM Start Otto API (port 8001)
echo [1/3] Starting Otto API on port 8001...
start "Otto API" cmd /k "cd /d %REPO_ROOT%\apps\otto && python -m otto.cli server"
timeout /t 2 /nobreak >nul

REM Start Life OS Backend (port 8000)
echo [2/3] Starting Life OS Backend on port 8000...
start "Life OS Backend" cmd /k "cd /d %REPO_ROOT%\apps\life_os\backend && python -m uvicorn main:app --reload --port 8000"
timeout /t 2 /nobreak >nul

REM Start Life OS Frontend (port 3000)
echo [3/3] Starting Life OS Frontend on port 3000...
start "Life OS Frontend" cmd /k "cd /d %REPO_ROOT%\apps\life_os\frontend && npm run dev"
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo   All services starting!
echo ========================================
echo.
echo Services:
echo   - Otto API: http://localhost:8001
echo   - Life OS Backend: http://localhost:8000
echo   - Life OS Frontend: http://localhost:3000
echo   - Otto Console: http://localhost:3000/otto
echo.
echo Press any key to open the Otto Console in your browser...
pause >nul

start http://localhost:3000/otto

echo.
echo All services are running in separate windows.
echo Close those windows to stop the services.
echo.

