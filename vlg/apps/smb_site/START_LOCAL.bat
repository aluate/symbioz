@echo off
echo ========================================
echo   SMB Site - Starting Local Server
echo ========================================
echo.

REM Change to the script's directory
cd /d "%~dp0"

echo Current directory: %CD%
echo.

REM Check if Node.js is installed
echo Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed!
    echo.
    echo Please install Node.js from: https://nodejs.org/
    echo Download the LTS version and install it.
    echo.
    pause
    exit /b 1
)

echo Node.js found!
echo.

REM Check if dependencies are installed
echo Checking dependencies...
if not exist "node_modules" (
    echo Dependencies not found. Installing now...
    echo This may take a few minutes...
    echo.
    call npm install
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install dependencies!
        pause
        exit /b 1
    )
    echo.
    echo Dependencies installed successfully!
    echo.
) else (
    echo Dependencies already installed.
    echo.
)

REM Start the dev server
echo ========================================
echo   Starting development server...
echo ========================================
echo.
echo The site will open in your browser at:
echo   http://localhost:3000
echo.
echo Keep this window open while testing.
echo Press Ctrl+C to stop the server.
echo.

REM Wait a moment then open browser
start "" "http://localhost:3000"
timeout /t 3 /nobreak >nul

REM Start the dev server (this will keep running)
call npm run dev

pause

