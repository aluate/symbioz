# Otto Environment Setup Script for PowerShell
# This script helps you set environment variables for Otto
# 
# Usage:
#   1. Edit the values below with your actual keys
#   2. Run: .\infra\setup-env.ps1
#   3. Or source it: . .\infra\setup-env.ps1 (to keep vars in current session)

Write-Host "=== Otto Environment Setup ===" -ForegroundColor Cyan
Write-Host ""

# ============================================
# EDIT THESE VALUES WITH YOUR ACTUAL KEYS
# ============================================

# Render API Key (from Render Dashboard → Account Settings → API Keys)
$Env:RENDER_API_KEY = "YOUR_RENDER_API_KEY_HERE"

# GitHub Personal Access Token (from GitHub → Settings → Developer Settings → Personal Access Tokens)
$Env:GITHUB_TOKEN = "YOUR_GITHUB_TOKEN_HERE"

# Stripe Secret Key - TEST MODE ONLY (from Stripe Dashboard → Developers → API Keys → TEST MODE)
$Env:STRIPE_SECRET_KEY = "sk_test_YOUR_STRIPE_TEST_KEY_HERE"

# Stripe Publishable Key - TEST MODE ONLY
$Env:NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY = "pk_test_YOUR_PUBLISHABLE_KEY_HERE"

# Supabase Credentials (from Supabase Dashboard → Settings → API)
$Env:SUPABASE_URL = "https://YOUR_PROJECT_REF.supabase.co"
$Env:SUPABASE_SERVICE_KEY = "YOUR_SERVICE_ROLE_KEY_HERE"
$Env:SUPABASE_ANON_KEY = "YOUR_ANON_KEY_HERE"
$Env:SUPABASE_JWT_SECRET = "YOUR_JWT_SECRET_HERE"

# Optional: Vercel Token (only if using Vercel)
$Env:VERCEL_TOKEN = "YOUR_VERCEL_TOKEN_HERE"

# ============================================
# END OF VALUES TO EDIT
# ============================================

Write-Host "Environment variables set for current PowerShell session." -ForegroundColor Green
Write-Host ""
Write-Host "To verify, run:" -ForegroundColor Yellow
Write-Host "  Get-ChildItem Env: | Where-Object { `$_.Name -match 'RENDER|GITHUB|STRIPE|SUPABASE|VERCEL' }" -ForegroundColor Gray
Write-Host ""
Write-Host "To test Otto in dry-run mode:" -ForegroundColor Yellow
Write-Host "  python tools/infra.py diag --env=prod --dry-run" -ForegroundColor Gray
Write-Host ""
Write-Host "NOTE: These variables are only set for THIS PowerShell session." -ForegroundColor Yellow
Write-Host "To persist them, either:" -ForegroundColor Yellow
Write-Host "  1. Create a .env file (recommended - see infra/.env.example)" -ForegroundColor Gray
Write-Host "  2. Set them as system/user environment variables" -ForegroundColor Gray
Write-Host ""

# Quick validation
$missing = @()
if ($Env:RENDER_API_KEY -eq "YOUR_RENDER_API_KEY_HERE") { $missing += "RENDER_API_KEY" }
if ($Env:GITHUB_TOKEN -eq "YOUR_GITHUB_TOKEN_HERE") { $missing += "GITHUB_TOKEN" }
if ($Env:STRIPE_SECRET_KEY -eq "sk_test_YOUR_STRIPE_TEST_KEY_HERE") { $missing += "STRIPE_SECRET_KEY" }
if ($Env:SUPABASE_URL -eq "https://YOUR_PROJECT_REF.supabase.co") { $missing += "SUPABASE_URL" }

if ($missing.Count -gt 0) {
    Write-Host "⚠️  Warning: The following variables still have placeholder values:" -ForegroundColor Yellow
    foreach ($var in $missing) {
        Write-Host "  - $var" -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "Please edit this script and replace the placeholder values." -ForegroundColor Yellow
} else {
    Write-Host "✅ All environment variables appear to be configured!" -ForegroundColor Green
}

