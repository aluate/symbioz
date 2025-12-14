# Health check script for Otto API
# Reads OTTO_BASE_URL from environment variable or config/otto.json

$ErrorActionPreference = "Stop"

# Function to get Otto base URL
function Get-OttoBaseUrl {
    # Priority 1: Environment variable
    $envUrl = $env:OTTO_BASE_URL
    if ($envUrl) {
        return $envUrl.Trim()
    }
    
    # Priority 2: config/otto.json
    $configPath = Join-Path $PSScriptRoot "..\config\otto.json"
    if (Test-Path $configPath) {
        try {
            $config = Get-Content $configPath | ConvertFrom-Json
            $url = $config.otto_base_url
            if ($url -and $url -ne "https://REPLACE_ME" -and $url -ne "") {
                return $url.Trim()
            }
        } catch {
            Write-Warning "Failed to read config/otto.json: $_"
        }
    }
    
    return $null
}

# Get Otto URL
$ottoUrl = Get-OttoBaseUrl

if (-not $ottoUrl) {
    Write-Host "⚠️  Otto URL not configured" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To configure Otto URL, use one of:" -ForegroundColor Cyan
    Write-Host "  1. Set environment variable: `$env:OTTO_BASE_URL='https://your-otto-url.railway.app'" -ForegroundColor Gray
    Write-Host "  2. Edit config/otto.json and set 'otto_base_url'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "See docs/otto_url_setup.md for details" -ForegroundColor Cyan
    exit 0
}

# Get health path (default to /health)
$healthPath = "/health"
$configPath = Join-Path $PSScriptRoot "..\config\otto.json"
if (Test-Path $configPath) {
    try {
        $config = Get-Content $configPath | ConvertFrom-Json
        if ($config.health_path) {
            $healthPath = $config.health_path
        }
    } catch {
        # Use default
    }
}

# Build health check URL
$healthUrl = $ottoUrl.TrimEnd('/') + $healthPath

Write-Host "Checking Otto health..." -ForegroundColor Cyan
Write-Host "URL: $healthUrl" -ForegroundColor Gray
Write-Host ""

try {
    $response = Invoke-RestMethod -Uri $healthUrl -Method Get -TimeoutSec 10 -ErrorAction Stop
    
    Write-Host "✅ Otto is healthy" -ForegroundColor Green
    Write-Host "Response: $($response | ConvertTo-Json -Compress)" -ForegroundColor Gray
    
    exit 0
} catch {
    Write-Host "❌ Otto health check failed" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.Exception.Response) {
        $statusCode = $_.Exception.Response.StatusCode.value__
        Write-Host "HTTP Status: $statusCode" -ForegroundColor Yellow
    }
    
    exit 1
}


