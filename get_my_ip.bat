@echo off
echo.
echo ========================================
echo   Your IP Address for Phone Access
echo ========================================
echo.

REM Get IPv4 address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
    set IP=%%a
    set IP=!IP:~1!
    echo.
    echo Your IP Address: !IP!
    echo.
    echo Access Life OS from your phone:
    echo   http://!IP!:3000
    echo.
    echo Access Otto API directly:
    echo   http://!IP!:8001
    echo.
    echo ========================================
    echo.
)

if not defined IP (
    echo Could not find IP address. Make sure you're connected to Wi-Fi.
    echo.
)

pause

