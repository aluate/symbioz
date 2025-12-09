# Run Corporate Crashout Deployment with Cloudflare Token
# This script sets the token and runs the deployment

$env:CLOUDFLARE_API_TOKEN = "bGTnYLVY3gIy7LDZCcguLD155EHH7_gJ3x6KmIJH"

Write-Host "🚀 Running Corporate Crashout Deployment..." -ForegroundColor Cyan
Write-Host "Cloudflare API token set for this session" -ForegroundColor Green
Write-Host ""

cd "E:\My Drive"
python tools/deploy_corporate_crashout.py

Write-Host ""
Write-Host "✅ Deployment script completed!" -ForegroundColor Green
