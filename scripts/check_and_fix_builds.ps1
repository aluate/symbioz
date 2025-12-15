# Check and Fix Builds - Auto-detect and fix Render/Vercel build failures
# This script will check for issues, fix them, push, and loop until both pass

$ErrorActionPreference = "Stop"

Write-Host "🔍 Checking Build Status and Fixing Issues..." -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if Otto is available
function Get-OttoBaseUrl {
    $envUrl = $env:OTTO_BASE_URL
    if ($envUrl) {
        return $envUrl.Trim()
    }
    
    $configPath = Join-Path $PSScriptRoot "..\config\otto.json"
    if (Test-Path $configPath) {
        try {
            $config = Get-Content $configPath | ConvertFrom-Json
            $url = $config.otto_base_url
            if ($url -and $url -ne "https://REPLACE_ME" -and $url -ne "") {
                return $url.Trim()
            }
        } catch {
            # Ignore
        }
    }
    return $null
}

$ottoUrl = Get-OttoBaseUrl

if ($ottoUrl) {
    Write-Host "✅ Otto is available at: $ottoUrl" -ForegroundColor Green
    Write-Host "Triggering Otto's fix_and_monitor loop..." -ForegroundColor Cyan
    Write-Host ""
    
    try {
        $fixAndMonitorUrl = "$ottoUrl/actions/fix_and_monitor"
        $body = @{
            mode = "pr"
            maxIterations = 10
            dryRun = $false
        } | ConvertTo-Json
        
        $response = Invoke-RestMethod -Uri $fixAndMonitorUrl -Method Post -Body $body -ContentType "application/json" -TimeoutSec 600 -ErrorAction Stop
        
        Write-Host "✅ Otto Fix and Monitor Result:" -ForegroundColor Green
        Write-Host "Status: $($response.status)" -ForegroundColor $(if ($response.status -eq "success") { "Green" } else { "Yellow" })
        Write-Host "Message: $($response.message)" -ForegroundColor Gray
        
        if ($response.data) {
            if ($response.data.render_fix) {
                $fix = $response.data.render_fix
                if ($fix.fixed) {
                    Write-Host "✅ Render runtime fixed: $($fix.message)" -ForegroundColor Green
                }
            }
            
            if ($response.data.iterations) {
                Write-Host "Iterations: $($response.data.iterations)" -ForegroundColor Cyan
            }
            
            if ($response.data.vercel -and $response.data.render) {
                Write-Host ""
                Write-Host "Final Status:" -ForegroundColor Cyan
                Write-Host "  Vercel: $($response.data.vercel.status)" -ForegroundColor $(if ($response.data.vercel.status -eq "success") { "Green" } else { "Red" })
                Write-Host "  Render: $($response.data.render.status)" -ForegroundColor $(if ($response.data.render.status -eq "success") { "Green" } else { "Red" })
            }
        }
        
        exit 0
    } catch {
        Write-Host "⚠️  Otto API call failed: $($_.Exception.Message)" -ForegroundColor Yellow
        Write-Host "Falling back to manual checks..." -ForegroundColor Yellow
        Write-Host ""
    }
} else {
    Write-Host "⚠️  Otto not available - checking for common issues manually..." -ForegroundColor Yellow
    Write-Host ""
}

# Step 2: Manual checks and fixes
$repoRoot = Join-Path $PSScriptRoot ".."
Set-Location $repoRoot

$fixesApplied = @()
$needsCommit = $false

# Check 1: Otto Dockerfile
Write-Host "Checking Otto Dockerfile..." -ForegroundColor Cyan
$dockerfilePath = Join-Path $repoRoot "apps\otto\Dockerfile"
if (Test-Path $dockerfilePath) {
    $dockerfile = Get-Content $dockerfilePath -Raw
    $issues = @()
    
    # Check for apps/otto/ prefix in COPY (wrong for root_dir=apps/otto)
    if ($dockerfile -match "COPY\s+apps/otto/") {
        Write-Host "  ⚠️  Found apps/otto/ prefix in COPY commands (incorrect for Render)" -ForegroundColor Yellow
        $issues += "COPY paths have apps/otto/ prefix"
    }
    
    # Check for hardcoded port in CMD
    if ($dockerfile -match 'CMD.*--port\s+8001' -and $dockerfile -notmatch '\$PORT') {
        Write-Host "  ⚠️  CMD uses hardcoded port instead of \$PORT" -ForegroundColor Yellow
        $issues += "Hardcoded port in CMD"
    }
    
    if ($issues.Count -eq 0) {
        Write-Host "  ✅ Dockerfile looks correct" -ForegroundColor Green
    }
} else {
    Write-Host "  ❌ Dockerfile not found!" -ForegroundColor Red
    $fixesApplied += "Dockerfile missing"
}

# Check 2: Symbioz-web package.json
Write-Host "Checking Symbioz-web package.json..." -ForegroundColor Cyan
$packageJsonPath = Join-Path $repoRoot "apps\symbioz-web\package.json"
if (Test-Path $packageJsonPath) {
    $packageJson = Get-Content $packageJsonPath | ConvertFrom-Json
    $issues = @()
    
    # Check if scripts use npx
    $scripts = $packageJson.scripts
    foreach ($scriptName in @("dev", "build", "start", "lint")) {
        if ($scripts.$scriptName -and $scripts.$scriptName -notmatch "npx next") {
            Write-Host "  ⚠️  Script '$scriptName' doesn't use 'npx next'" -ForegroundColor Yellow
            $issues += "$scriptName script"
        }
    }
    
    if ($issues.Count -eq 0) {
        Write-Host "  ✅ package.json scripts look correct" -ForegroundColor Green
    }
} else {
    Write-Host "  ❌ package.json not found!" -ForegroundColor Red
    $fixesApplied += "package.json missing"
}

# Check 3: Required files exist
Write-Host "Checking required files..." -ForegroundColor Cyan
$requiredFiles = @(
    "apps\otto\requirements.txt",
    "apps\otto\otto",
    "apps\otto\otto_config.yaml"
)

foreach ($file in $requiredFiles) {
    $fullPath = Join-Path $repoRoot $file
    if (Test-Path $fullPath) {
        Write-Host "  ✅ $file exists" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file missing!" -ForegroundColor Red
        $fixesApplied += "$file missing"
    }
}

# Step 3: Commit and push if needed
if ($fixesApplied.Count -gt 0) {
    Write-Host ""
    Write-Host "⚠️  Found issues that need fixing:" -ForegroundColor Yellow
    foreach ($fix in $fixesApplied) {
        Write-Host "  - $fix" -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "Note: Some fixes may require manual intervention or Otto auto-repair." -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "✅ No obvious issues found in codebase" -ForegroundColor Green
    Write-Host ""
    Write-Host "If builds are still failing, check:" -ForegroundColor Cyan
    Write-Host '  1. Vercel Dashboard - Latest deployment - Build logs' -ForegroundColor Gray
    Write-Host '  2. Render Dashboard - Latest deploy - Logs' -ForegroundColor Gray
    Write-Host '  3. Set RENDER_SERVICE_ID_OTTO and deploy Otto to enable auto-fix' -ForegroundColor Gray
}

Write-Host ""
Write-Host 'To enable Otto auto-fix:' -ForegroundColor Cyan
Write-Host '  1. Deploy Otto on Render' -ForegroundColor Gray
Write-Host '  2. Set OTTO_BASE_URL environment variable or config/otto.json' -ForegroundColor Gray
Write-Host '  3. Run: .\scripts\run_otto_fix_and_monitor.ps1' -ForegroundColor Gray

