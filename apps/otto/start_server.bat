@echo off
echo Starting Otto API Server...
cd /d %~dp0
python -m otto.cli server
pause

