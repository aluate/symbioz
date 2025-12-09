@echo off
REM Example Pole Barn Calculator Run
REM This runs a complete example calculation

cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

REM Check if pandas is installed
python -c "import pandas" >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: pandas module not found
    echo Installing required dependencies...
    pip install pandas click
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        echo Please run: pip install pandas click
        pause
        exit /b 1
    )
    echo Dependencies installed successfully.
    echo.
)

echo ========================================
echo   POLE BARN CALCULATOR - EXAMPLE RUN
echo ========================================
echo.

python -m apps.cli ^
  --project-name "Example Barn" ^
  --length 40 ^
  --width 30 ^
  --eave-height 12 ^
  --peak-height 16 ^
  --roof-pitch 0.333 ^
  --overhang-front 1 ^
  --overhang-rear 1 ^
  --overhang-sides 1 ^
  --door-count 2 ^
  --door-width 12 ^
  --door-height 10 ^
  --window-count 4 ^
  --window-width 3 ^
  --window-height 2 ^
  --pole-spacing-length 10 ^
  --pole-spacing-width 8 ^
  --pole-diameter 6 ^
  --pole-depth 4 ^
  --roof-material metal ^
  --roof-gauge 29 ^
  --wall-material metal ^
  --wall-gauge 29 ^
  --truss-type standard ^
  --truss-spacing 10 ^
  --purlin-spacing 2 ^
  --girt-spacing 2 ^
  --foundation-type concrete_pad ^
  --concrete-thickness 4 ^
  --insulation-type fiberglass ^
  --insulation-r-value 19 ^
  --labor-rate 50 ^
  --material-markup 1.15 ^
  --tax-rate 0.08 ^
  --delivery-cost 300 ^
  --permit-cost 500 ^
  --site-prep-cost 1000 ^
  --assembly-method standard ^
  --fastening-type screws ^
  --weather-sealing ^
  --ventilation-type ridge_vent ^
  --ventilation-count 1

echo.
pause

