@echo off
echo.
echo ========================================
echo   Stopping Otto + Life OS Stack
echo ========================================
echo.

REM Kill Otto API (port 8001)
echo Stopping Otto API...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8001 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)

REM Kill Life OS Backend (port 8000)
echo Stopping Life OS Backend...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)

REM Kill Life OS Frontend (port 3000)
echo Stopping Life OS Frontend...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a >nul 2>&1
)

REM Also try to kill by window title
taskkill /FI "WINDOWTITLE eq Otto API*" /T >nul 2>&1
taskkill /FI "WINDOWTITLE eq Life OS Backend*" /T >nul 2>&1
taskkill /FI "WINDOWTITLE eq Life OS Frontend*" /T >nul 2>&1

echo.
echo All servers stopped!
echo.
timeout /t 2 /nobreak >nul

