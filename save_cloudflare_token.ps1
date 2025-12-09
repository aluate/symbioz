# Save Cloudflare API Token to .env file
# Run this: .\save_cloudflare_token.ps1

$token = "bGTnYLVY3gIy7LDZCcguLD155EHH7_gJ3x6KmIJH"
$envPath = ".env"

# Check if .env exists, if not create it
if (-not (Test-Path $envPath)) {
    New-Item -ItemType File -Path $envPath | Out-Null
}

# Read existing .env content
$content = ""
if (Test-Path $envPath) {
    $content = Get-Content $envPath -Raw
}

# Check if CLOUDFLARE_API_TOKEN already exists
if ($content -match "CLOUDFLARE_API_TOKEN") {
    # Replace existing token
    $content = $content -replace "CLOUDFLARE_API_TOKEN=.*", "CLOUDFLARE_API_TOKEN=$token"
    Write-Host "✅ Updated existing CLOUDFLARE_API_TOKEN in .env" -ForegroundColor Green
} else {
    # Add new token
    if ($content -and -not $content.EndsWith("`n")) {
        $content += "`n"
    }
    $content += "`n# Cloudflare API Token`n"
    $content += "CLOUDFLARE_API_TOKEN=$token`n"
    Write-Host "✅ Added CLOUDFLARE_API_TOKEN to .env" -ForegroundColor Green
}

# Write back to file
Set-Content -Path $envPath -Value $content -NoNewline

Write-Host "`nToken saved to .env file (not committed to git - safe!)" -ForegroundColor Cyan
