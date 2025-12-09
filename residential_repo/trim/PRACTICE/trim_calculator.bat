@echo off
cd /d "%~dp0"
python trim_calculator.py
if errorlevel 1 (
    echo.
    echo An error occurred. Press any key to exit...
    pause >nul
)

