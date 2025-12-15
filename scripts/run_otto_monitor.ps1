# Run Otto Deploy Monitor
# One-button command to trigger Otto's monitor/repair/redeploy loop

$ErrorActionPreference = "Stop"

# Get Otto URL from environment or config
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
    Write-Host "  1. Set environment variable: `$env:OTTO_BASE_URL='https://your-otto-url.onrender.com'" -ForegroundColor Gray
    Write-Host "  2. Edit config/otto.json and set 'otto_base_url'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "See docs/otto_url_setup.md for details" -ForegroundColor Cyan
    exit 1
}

# Check capabilities first
Write-Host "Checking Otto capabilities..." -ForegroundColor Cyan
try {
    $capabilitiesUrl = "$ottoUrl/capabilities"
    $capabilities = Invoke-RestMethod -Uri $capabilitiesUrl -Method Get -TimeoutSec 10 -ErrorAction Stop
    
    Write-Host "Otto Capabilities:" -ForegroundColor Green
    Write-Host "  GitHub Token: $($capabilities.github_token)" -ForegroundColor $(if ($capabilities.github_token) { "Green" } else { "Red" })
    Write-Host "  Vercel Token: $($capabilities.vercel_token)" -ForegroundColor $(if ($capabilities.vercel_token) { "Green" } else { "Red" })
    Write-Host "  Render API Key: $($capabilities.render_api_key)" -ForegroundColor $(if ($capabilities.render_api_key) { "Green" } else { "Red" })
    Write-Host ""
    
    if (-not $capabilities.github_token -or -not $capabilities.vercel_token -or -not $capabilities.render_api_key) {
        Write-Host "⚠️  Warning: Some tokens are missing. Auto-repair may not work fully." -ForegroundColor Yellow
        Write-Host ""
    }
} catch {
    Write-Host "❌ Failed to check capabilities: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Is Otto deployed and accessible at $ottoUrl ?" -ForegroundColor Yellow
    exit 1
}

# Ask for dry-run preference
$dryRun = $false
$response = Read-Host "Run in dry-run mode first? (y/n) [y]"
if ($response -eq "" -or $response.ToLower() -eq "y") {
    $dryRun = $true
    Write-Host "Running in DRY-RUN mode (no changes will be committed)" -ForegroundColor Yellow
} else {
    Write-Host "Running in LIVE mode (will commit and push fixes)" -ForegroundColor Green
}
Write-Host ""

# Run monitor
Write-Host "Triggering Otto monitor/repair/redeploy loop..." -ForegroundColor Cyan
Write-Host "Otto URL: $ottoUrl" -ForegroundColor Gray
Write-Host ""

try {
    $monitorUrl = "$ottoUrl/actions/run_deploy_monitor"
    $body = @{
        mode = "pr"
        maxIterations = 5
        dryRun = $dryRun
    } | ConvertTo-Json
    
    $response = Invoke-RestMethod -Uri $monitorUrl -Method Post -Body $body -ContentType "application/json" -TimeoutSec 300 -ErrorAction Stop
    
    Write-Host "✅ Monitor loop completed" -ForegroundColor Green
    Write-Host ""
    Write-Host "Status: $($response.status)" -ForegroundColor $(if ($response.status -eq "success") { "Green" } else { "Yellow" })
    Write-Host "Message: $($response.message)" -ForegroundColor Gray
    Write-Host ""
    
    if ($response.data) {
        $data = $response.data
        
        if ($data.iterations) {
            Write-Host "Iterations: $($data.iterations)" -ForegroundColor Cyan
        }
        
        if ($data.results) {
            Write-Host "Results:" -ForegroundColor Cyan
            foreach ($result in $data.results) {
                $target = $result.target
                $status = $result.status
                $color = switch ($status) {
                    "success" { "Green" }
                    "failed" { "Red" }
                    "building" { "Yellow" }
                    default { "Gray" }
                }
                Write-Host "  $target : $status" -ForegroundColor $color
            }
        }
        
        if ($data.dry_run -and $data.diff) {
            Write-Host ""
            Write-Host "Proposed Changes (dry-run):" -ForegroundColor Cyan
            Write-Host $data.diff -ForegroundColor Gray
        }
        
        if ($data.files_changed) {
            Write-Host ""
            Write-Host "Files Changed:" -ForegroundColor Cyan
            foreach ($file in $data.files_changed) {
                Write-Host "  - $file" -ForegroundColor Gray
            }
        }
        
        if ($data.commit_message) {
            Write-Host ""
            Write-Host "Commit: $($data.commit_message)" -ForegroundColor Cyan
        }
    }
    
    Write-Host ""
    if ($dryRun) {
        Write-Host "This was a dry-run. Run again without dry-run to apply fixes." -ForegroundColor Yellow
    } else {
        Write-Host "Check GitHub for the PR link, or check Render/Vercel dashboards for deployment status." -ForegroundColor Cyan
    }
    
} catch {
    Write-Host "❌ Monitor loop failed" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.Exception.Response) {
        $statusCode = $_.Exception.Response.StatusCode.value__
        Write-Host "HTTP Status: $statusCode" -ForegroundColor Yellow
        
        # Try to read error response
        try {
            $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
            $responseBody = $reader.ReadToEnd()
            Write-Host "Response: $responseBody" -ForegroundColor Gray
        } catch {
            # Ignore
        }
    }
    
    exit 1
}

