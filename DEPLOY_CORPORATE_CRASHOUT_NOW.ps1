# Deploy Corporate Crashout - PowerShell Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 Deploying Corporate Crashout" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Change to workspace root
$workspaceRoot = "g:\My Drive"
Set-Location $workspaceRoot

# Run the deployment script
Write-Host "Running deployment automation..." -ForegroundColor Gray
Write-Host ""

python tools/deploy_corporate_crashout.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Deployment script completed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Check your site at: https://achillies.vercel.app" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "❌ Deployment script failed" -ForegroundColor Red
    Write-Host "Check the error messages above" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
