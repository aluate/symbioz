@echo off
echo Starting Life OS Backend...
echo.
echo Access from phone: http://YOUR_IP:8000
echo.
cd /d %~dp0
uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause

