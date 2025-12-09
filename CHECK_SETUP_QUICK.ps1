# Quick Setup Check Script
# This runs the setup and outputs to a file

$ErrorActionPreference = "Continue"
$outputFile = Join-Path $PSScriptRoot "setup_results.txt"

function Write-Log {
    param($Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] $Message"
    Write-Host $logMessage
    Add-Content -Path $outputFile -Value $logMessage
}

Write-Log "========================================"
Write-Log "Starting Setup Check..."
Write-Log "========================================"
Write-Log ""

# Check Python
Write-Log "Checking Python..."
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python") {
        Write-Log "✅ Python found: $pythonVersion"
    } else {
        Write-Log "❌ Python not found or error: $pythonVersion"
    }
} catch {
    Write-Log "❌ Python check failed: $_"
}

# Check py launcher
try {
    $pyVersion = py --version 2>&1
    if ($pyVersion -match "Python") {
        Write-Log "✅ py launcher found: $pyVersion"
    }
} catch {
    Write-Log "⚠️  py launcher not available"
}

Write-Log ""

# Check Node.js
Write-Log "Checking Node.js..."
try {
    $nodeVersion = node --version 2>&1
    Write-Log "✅ Node.js found: $nodeVersion"
} catch {
    Write-Log "❌ Node.js not found"
}

# Check npm
Write-Log "Checking npm..."
try {
    $npmVersion = npm --version 2>&1
    Write-Log "✅ npm found: $npmVersion"
} catch {
    Write-Log "❌ npm not found"
}

Write-Log ""

# Check winget
Write-Log "Checking winget..."
try {
    $wingetVersion = winget --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Log "✅ winget found: $wingetVersion"
    } else {
        Write-Log "❌ winget not available"
    }
} catch {
    Write-Log "❌ winget check failed"
}

Write-Log ""
Write-Log "========================================"
Write-Log "Setup Check Complete!"
Write-Log "Results saved to: $outputFile"
Write-Log "========================================"





