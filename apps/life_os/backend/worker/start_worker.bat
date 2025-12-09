@echo off
echo Starting Otto Worker...
cd /d %~dp0..
python -m worker.otto_worker
pause

