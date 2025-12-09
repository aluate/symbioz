@echo off
echo Starting Life OS Frontend (Mobile Accessible)...
echo.
echo Access from phone: http://YOUR_IP:3000
echo Make sure to replace YOUR_IP with your computer's IP address
echo.
cd /d %~dp0
npm run dev -- -H 0.0.0.0
pause

