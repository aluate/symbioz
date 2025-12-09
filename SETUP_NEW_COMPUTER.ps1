# ========================================
# Complete Development Environment Setup
# ========================================
# This script installs Python, Node.js, and all project dependencies
# Run this on a new computer to get everything set up automatically
#
# Usage: Right-click → "Run with PowerShell" (or double-click)
# ========================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Development Environment Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get the script directory (repo root)
$REPO_ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $REPO_ROOT

Write-Host "Repository root: $REPO_ROOT" -ForegroundColor Gray
Write-Host ""

# ========================================
# Step 0: Check for winget (Windows Package Manager)
# ========================================
Write-Host "Step 0: Checking for Windows Package Manager (winget)..." -ForegroundColor Yellow

$wingetAvailable = $false
try {
    $wingetVersion = winget --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ winget found: $wingetVersion" -ForegroundColor Green
        $wingetAvailable = $true
    }
} catch {
    # winget not available
}

if (-not $wingetAvailable) {
    Write-Host "⚠️  winget not found - will need manual installation" -ForegroundColor Yellow
    Write-Host "   (winget comes with Windows 10/11, but may need App Installer update)" -ForegroundColor Gray
}

Write-Host ""

# ========================================
# Step 1: Check and Install Python
# ========================================
Write-Host "Step 1: Checking Python..." -ForegroundColor Yellow

$pythonFound = $false
$pythonVersion = $null
$pythonCmd = $null

# Try 'python' command
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python 3\.(1[1-9]|[2-9]\d)") {
        Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
        $pythonFound = $true
        $pythonCmd = "python"
    }
} catch {
    # Try 'py' launcher
    try {
        $pythonVersion = py --version 2>&1
        if ($pythonVersion -match "Python 3\.(1[1-9]|[2-9]\d)") {
            Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
            $pythonFound = $true
            $pythonCmd = "py"
        }
    } catch {
        # Python not found
    }
}

if (-not $pythonFound) {
    Write-Host "❌ Python 3.11+ not found!" -ForegroundColor Red
    
    if ($wingetAvailable) {
        Write-Host ""
        Write-Host "Installing Python 3.11 automatically using winget..." -ForegroundColor Yellow
        Write-Host "This may take a few minutes..." -ForegroundColor Gray
        Write-Host ""
        
        # Install Python 3.11 silently
        winget install --id Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Python installed successfully!" -ForegroundColor Green
            Write-Host "   Refreshing PATH..." -ForegroundColor Gray
            
            # Refresh PATH in current session
            $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
            
            # Wait a moment for PATH to update
            Start-Sleep -Seconds 2
            
            # Try to find Python again
            try {
                $pythonVersion = python --version 2>&1
                if ($pythonVersion -match "Python 3\.(1[1-9]|[2-9]\d)") {
                    Write-Host "✅ Python now available: $pythonVersion" -ForegroundColor Green
                    $pythonFound = $true
                    $pythonCmd = "python"
                } else {
                    # Try py launcher
                    $pythonVersion = py --version 2>&1
                    if ($pythonVersion -match "Python 3\.(1[1-9]|[2-9]\d)") {
                        Write-Host "✅ Python now available: $pythonVersion" -ForegroundColor Green
                        $pythonFound = $true
                        $pythonCmd = "py"
                    }
                }
            } catch {
                Write-Host "⚠️  Python installed but not in PATH yet" -ForegroundColor Yellow
                Write-Host "   Please close and reopen PowerShell, then run this script again" -ForegroundColor Yellow
                Write-Host ""
                # Removed blocking prompt for automated execution
                exit 1
            }
        } else {
            Write-Host "❌ Failed to install Python automatically" -ForegroundColor Red
            Write-Host ""
            Write-Host "Please install Python 3.11 or higher manually:" -ForegroundColor Yellow
            Write-Host "  1. Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
            Write-Host "  2. During installation, CHECK 'Add Python to PATH'" -ForegroundColor Yellow
            Write-Host "  3. Run this script again after installation" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "Opening Python download page..." -ForegroundColor Gray
            Start-Process "https://www.python.org/downloads/"
            Write-Host ""
            # Removed blocking prompt for automated execution
            exit 1
        }
    } else {
        Write-Host ""
        Write-Host "Please install Python 3.11 or higher:" -ForegroundColor Yellow
        Write-Host "  1. Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
        Write-Host "  2. During installation, CHECK 'Add Python to PATH'" -ForegroundColor Yellow
        Write-Host "  3. Run this script again after installation" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Opening Python download page..." -ForegroundColor Gray
        Start-Process "https://www.python.org/downloads/"
        Write-Host ""
        Write-Host "Press any key to exit..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 1
    }
}

# Check if version is 3.11+
if ($pythonVersion -notmatch "Python 3\.(1[1-9]|[2-9]\d)") {
    Write-Host "⚠️  Warning: Python 3.11+ recommended (found: $pythonVersion)" -ForegroundColor Yellow
    Write-Host "   Continuing anyway..." -ForegroundColor Gray
}

Write-Host ""

# ========================================
# Step 2: Check and Install Node.js
# ========================================
Write-Host "Step 2: Checking Node.js..." -ForegroundColor Yellow

$nodeFound = $false
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green
    $nodeFound = $true
} catch {
    Write-Host "❌ Node.js not found!" -ForegroundColor Red
}

if (-not $nodeFound) {
    if ($wingetAvailable) {
        Write-Host ""
        Write-Host "Installing Node.js LTS automatically using winget..." -ForegroundColor Yellow
        Write-Host "This may take a few minutes..." -ForegroundColor Gray
        Write-Host ""
        
        # Install Node.js LTS silently
        winget install --id OpenJS.NodeJS.LTS --silent --accept-package-agreements --accept-source-agreements
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Node.js installed successfully!" -ForegroundColor Green
            Write-Host "   Refreshing PATH..." -ForegroundColor Gray
            
            # Refresh PATH in current session
            $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
            
            # Wait a moment for PATH to update
            Start-Sleep -Seconds 2
            
            # Try to find Node.js again
            try {
                $nodeVersion = node --version
                Write-Host "✅ Node.js now available: $nodeVersion" -ForegroundColor Green
                $nodeFound = $true
            } catch {
                Write-Host "⚠️  Node.js installed but not in PATH yet" -ForegroundColor Yellow
                Write-Host "   Please close and reopen PowerShell, then run this script again" -ForegroundColor Yellow
                Write-Host ""
                # Removed blocking prompt for automated execution
                exit 1
            }
        } else {
            Write-Host "❌ Failed to install Node.js automatically" -ForegroundColor Red
            Write-Host ""
            Write-Host "Please install Node.js manually:" -ForegroundColor Yellow
            Write-Host "  1. Download LTS version from: https://nodejs.org/" -ForegroundColor Yellow
            Write-Host "  2. Run the installer (default options are fine)" -ForegroundColor Yellow
            Write-Host "  3. Run this script again after installation" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "Opening Node.js download page..." -ForegroundColor Gray
            Start-Process "https://nodejs.org/"
            Write-Host ""
            # Removed blocking prompt for automated execution
            exit 1
        }
    } else {
        Write-Host ""
        Write-Host "Please install Node.js:" -ForegroundColor Yellow
        Write-Host "  1. Download LTS version from: https://nodejs.org/" -ForegroundColor Yellow
        Write-Host "  2. Run the installer (default options are fine)" -ForegroundColor Yellow
        Write-Host "  3. Run this script again after installation" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Opening Node.js download page..." -ForegroundColor Gray
        Start-Process "https://nodejs.org/"
        Write-Host ""
        Write-Host "Press any key to exit..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 1
    }
}

# Check npm
try {
    $npmVersion = npm --version
    Write-Host "✅ npm found: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ npm not found! (should come with Node.js)" -ForegroundColor Red
    Write-Host "   Please reinstall Node.js" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# ========================================
# Step 3: Upgrade pip
# ========================================
Write-Host "Step 3: Upgrading pip..." -ForegroundColor Yellow
try {
    & $pythonCmd -m pip install --upgrade pip --quiet
    Write-Host "✅ pip upgraded" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Could not upgrade pip (continuing anyway)" -ForegroundColor Yellow
}
Write-Host ""

# ========================================
# Step 4: Install Python Dependencies
# ========================================
Write-Host "Step 4: Installing Python dependencies..." -ForegroundColor Yellow
Write-Host ""

# Find all requirements.txt files
$requirementsFiles = Get-ChildItem -Path $REPO_ROOT -Recurse -Filter "requirements.txt" | Where-Object {
    $_.FullName -notmatch "node_modules|venv|\.venv|__pycache__|temp_|\.git"
}

if ($requirementsFiles.Count -eq 0) {
    Write-Host "⚠️  No requirements.txt files found" -ForegroundColor Yellow
} else {
    Write-Host "Found $($requirementsFiles.Count) requirements.txt file(s):" -ForegroundColor Gray
    
    foreach ($reqFile in $requirementsFiles) {
        $relativePath = $reqFile.FullName.Replace($REPO_ROOT, "").TrimStart("\")
        Write-Host "  - $relativePath" -ForegroundColor Gray
        
        $reqDir = $reqFile.DirectoryName
        Set-Location $reqDir
        
        # Check if there's a venv directory
        $venvPath = Join-Path $reqDir "venv"
        $hasVenv = Test-Path $venvPath
        
        if ($hasVenv) {
            Write-Host "    Using existing virtual environment..." -ForegroundColor Gray
            & "$venvPath\Scripts\python.exe" -m pip install -q -r $reqFile.Name
        } else {
            Write-Host "    Installing to global Python..." -ForegroundColor Gray
            & $pythonCmd -m pip install -q -r $reqFile.Name
        }
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "    ✅ Installed" -ForegroundColor Green
        } else {
            Write-Host "    ⚠️  Some packages may have failed" -ForegroundColor Yellow
        }
    }
}

Write-Host ""

# ========================================
# Step 5: Create Virtual Environments
# ========================================
Write-Host "Step 5: Setting up virtual environments..." -ForegroundColor Yellow

# Projects that need venv
$venvProjects = @(
    @{Path = "apps\symbioz_cli"; Name = "Symbioz CLI"},
    @{Path = "apps\otto"; Name = "Otto"},
    @{Path = "apps\life_os\backend"; Name = "Life OS Backend"}
)

foreach ($project in $venvProjects) {
    $projectPath = Join-Path $REPO_ROOT $project.Path
    if (Test-Path $projectPath) {
        $venvPath = Join-Path $projectPath "venv"
        
        if (-not (Test-Path $venvPath)) {
            Write-Host "  Creating venv for $($project.Name)..." -ForegroundColor Gray
            Set-Location $projectPath
            & $pythonCmd -m venv venv
            if ($LASTEXITCODE -eq 0) {
                Write-Host "    ✅ Created" -ForegroundColor Green
                
                # Install requirements if they exist
                $reqFile = Join-Path $projectPath "requirements.txt"
                if (Test-Path $reqFile) {
                    Write-Host "    Installing dependencies..." -ForegroundColor Gray
                    & "$venvPath\Scripts\python.exe" -m pip install -q --upgrade pip
                    & "$venvPath\Scripts\python.exe" -m pip install -q -r $reqFile
                    if ($LASTEXITCODE -eq 0) {
                        Write-Host "    ✅ Dependencies installed" -ForegroundColor Green
                    }
                }
            } else {
                Write-Host "    ⚠️  Failed to create venv" -ForegroundColor Yellow
            }
        } else {
            Write-Host "  ✅ $($project.Name) venv already exists" -ForegroundColor Green
        }
    }
}

Write-Host ""

# ========================================
# Step 6: Install Node.js Dependencies
# ========================================
Write-Host "Step 6: Installing Node.js dependencies..." -ForegroundColor Yellow
Write-Host ""

# Find all package.json files
$packageFiles = Get-ChildItem -Path $REPO_ROOT -Recurse -Filter "package.json" | Where-Object {
    $_.FullName -notmatch "node_modules|\.git|temp_"
}

if ($packageFiles.Count -eq 0) {
    Write-Host "⚠️  No package.json files found" -ForegroundColor Yellow
} else {
    Write-Host "Found $($packageFiles.Count) package.json file(s):" -ForegroundColor Gray
    
    foreach ($pkgFile in $packageFiles) {
        $relativePath = $pkgFile.FullName.Replace($REPO_ROOT, "").TrimStart("\")
        Write-Host "  - $relativePath" -ForegroundColor Gray
        
        $pkgDir = $pkgFile.DirectoryName
        Set-Location $pkgDir
        
        # Check if node_modules exists
        $nodeModulesPath = Join-Path $pkgDir "node_modules"
        if (-not (Test-Path $nodeModulesPath)) {
            Write-Host "    Installing npm packages..." -ForegroundColor Gray
            npm install --silent
            if ($LASTEXITCODE -eq 0) {
                Write-Host "    ✅ Installed" -ForegroundColor Green
            } else {
                Write-Host "    ⚠️  Some packages may have failed" -ForegroundColor Yellow
            }
        } else {
            Write-Host "    ✅ Already installed" -ForegroundColor Green
        }
    }
}

Write-Host ""

# ========================================
# Step 7: Verify Installation
# ========================================
Write-Host "Step 7: Verifying installation..." -ForegroundColor Yellow
Write-Host ""

$allGood = $true

# Test Python
try {
    $testPython = & $pythonCmd -c "import sys; print(f'Python {sys.version_info.major}.{sys.version_info.minor}')" 2>&1
    Write-Host "✅ Python working: $testPython" -ForegroundColor Green
} catch {
    Write-Host "❌ Python test failed" -ForegroundColor Red
    $allGood = $false
}

# Test Node.js
try {
    $testNode = node --version
    Write-Host "✅ Node.js working: $testNode" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js test failed" -ForegroundColor Red
    $allGood = $false
}

# Test npm
try {
    $testNpm = npm --version
    Write-Host "✅ npm working: $testNpm" -ForegroundColor Green
} catch {
    Write-Host "❌ npm test failed" -ForegroundColor Red
    $allGood = $false
}

Write-Host ""

# ========================================
# Summary
# ========================================
Write-Host "========================================" -ForegroundColor Cyan
if ($allGood) {
    Write-Host "  ✅ Setup Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "You can now run:" -ForegroundColor Green
    Write-Host "  - START_OTTO_WINDOWS.bat (to start Otto + Life OS)" -ForegroundColor Gray
    Write-Host "  - LAUNCH_SYMBIOZ.bat (to start Symbioz)" -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host "  ⚠️  Setup completed with warnings" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Some components may need manual attention." -ForegroundColor Yellow
    Write-Host ""
}

# Removed blocking prompt for automated execution
# Write-Host "Press any key to exit..."
# $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
