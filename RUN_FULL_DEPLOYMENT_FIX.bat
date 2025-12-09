@echo off
REM Run full deployment check and fix

cd /d "E:\My Drive"

echo Setting environment variables...
set VERCEL_TOKEN=n6QnE86DsiIcQXIdQp0SA34P
set CLOUDFLARE_API_TOKEN=bGTnYLVY3gIy7LDZCcguLD155EHH7_gJ3x6KmIJH

echo.
echo Running deployment script...
python tools\deploy_corporate_crashout.py

echo.
echo Deployment check complete!
pause
