# ============================================
# DEV MACHINE BOOTSTRAP - Windows PowerShell
# ============================================
# This script configures a Windows PC for development
# Run as Administrator: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then: .\setup.ps1

param(
    [switch]$SkipWSL,
    [switch]$SkipChoco,
    [string]$GitName = "",
    [string]$GitEmail = ""
)

$ErrorActionPreference = "Stop"

Write-Host "FRAT DEV MACHINE SETUP - Starting..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Check for admin privileges
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "WARNING: Not running as Administrator. Some features may require elevation." -ForegroundColor Yellow
}

# ============================================
# 1. CREATE DEV FOLDER STRUCTURE
# ============================================
Write-Host "`nCreating dev folder structure..." -ForegroundColor Green

$devRoot = "C:\dev"
$folders = @(
    "$devRoot\_projects",
    "$devRoot\_templates",
    "$devRoot\_repos"
)

foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder -Force | Out-Null
        Write-Host "  [OK] Created: $folder" -ForegroundColor Gray
    } else {
        Write-Host "  [OK] Exists: $folder" -ForegroundColor Gray
    }
}

# ============================================
# 2. ENABLE WSL2
# ============================================
if (-not $SkipWSL) {
    Write-Host "`nConfiguring WSL2..." -ForegroundColor Green
    
    # Check if WSL is already installed
    $wslInstalled = Get-Command wsl -ErrorAction SilentlyContinue
    
    if (-not $wslInstalled) {
        Write-Host "  Installing WSL2..." -ForegroundColor Yellow
        wsl --install -d Ubuntu
        Write-Host "  WARNING: WSL installation requires restart. Please restart and run this script again." -ForegroundColor Yellow
        Write-Host "  After restart, WSL will continue setup automatically." -ForegroundColor Yellow
    } else {
        Write-Host "  [OK] WSL is installed" -ForegroundColor Gray
        $wslVersion = wsl --version 2>&1
        Write-Host "  $wslVersion" -ForegroundColor Gray
    }
    
    # Set WSL2 as default
    wsl --set-default-version 2 2>&1 | Out-Null
}

# ============================================
# 3. INSTALL PACKAGE MANAGERS
# ============================================
Write-Host "`nSetting up package managers..." -ForegroundColor Green

# Winget (usually pre-installed on Windows 11)
$wingetInstalled = Get-Command winget -ErrorAction SilentlyContinue
if ($wingetInstalled) {
    Write-Host "  [OK] winget is available" -ForegroundColor Gray
} else {
    Write-Host "  WARNING: winget not found. Install from Microsoft Store." -ForegroundColor Yellow
}

# Chocolatey (optional)
if (-not $SkipChoco) {
    $chocoInstalled = Get-Command choco -ErrorAction SilentlyContinue
    if (-not $chocoInstalled) {
        Write-Host "  Installing Chocolatey..." -ForegroundColor Yellow
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        Write-Host "  [OK] Chocolatey installed" -ForegroundColor Gray
    } else {
        Write-Host "  [OK] Chocolatey is installed" -ForegroundColor Gray
    }
}

# ============================================
# 4. INSTALL ESSENTIAL TOOLS
# ============================================
Write-Host "`nInstalling essential development tools..." -ForegroundColor Green

$tools = @(
    @{Name="Git.Git"; Manager="winget"},
    @{Name="GitHub.cli"; Manager="winget"},
    @{Name="Microsoft.VisualStudioCode"; Manager="winget"},
    @{Name="Docker.DockerDesktop"; Manager="winget"},
    @{Name="Python.Python.3.12"; Manager="winget"},
    @{Name="OpenJS.NodeJS.LTS"; Manager="winget"}
)

foreach ($tool in $tools) {
    Write-Host "  Checking $($tool.Name)..." -ForegroundColor Yellow
    if ($tool.Manager -eq "winget" -and $wingetInstalled) {
        # Check if already installed
        $checkOutput = winget list --id $tool.Name 2>&1 | Out-String
        if ($checkOutput -match $tool.Name -and $checkOutput -notmatch "No installed package") {
            Write-Host "    [OK] $($tool.Name) - already installed" -ForegroundColor Gray
        } else {
            # Try to install
            Write-Host "    Installing $($tool.Name)..." -ForegroundColor DarkYellow
            $installOutput = winget install --id $tool.Name --accept-package-agreements --accept-source-agreements 2>&1 | Out-String
            $exitCode = $LASTEXITCODE
            if ($exitCode -eq 0 -or $installOutput -match "already installed" -or $installOutput -match "No applicable update" -or $installOutput -match "Installer completed successfully") {
                Write-Host "    [OK] $($tool.Name) installed" -ForegroundColor Gray
            } else {
                Write-Host "    [WARNING] $($tool.Name) - exit code: $exitCode" -ForegroundColor Yellow
                # Check again after install attempt
                $checkAgain = winget list --id $tool.Name 2>&1 | Out-String
                if ($checkAgain -match $tool.Name) {
                    Write-Host "    [OK] $($tool.Name) - appears to be installed now" -ForegroundColor Gray
                }
            }
        }
    } elseif ($tool.Manager -eq "choco" -and (Get-Command choco -ErrorAction SilentlyContinue)) {
        choco install $tool.Name -y 2>&1 | Out-Null
        Write-Host "    [OK] $($tool.Name)" -ForegroundColor Gray
    }
}

# ============================================
# 5. VERIFY PYTHON AND NODE INSTALLATIONS
# ============================================
Write-Host "`nVerifying Python and Node.js..." -ForegroundColor Green

$pythonInstalled = Get-Command python -ErrorAction SilentlyContinue
if ($pythonInstalled) {
    $pythonVersion = python --version 2>&1
    Write-Host "  [OK] Python: $pythonVersion" -ForegroundColor Gray
} else {
    Write-Host "  [WARNING] Python not found in PATH. May need to restart terminal." -ForegroundColor Yellow
}

$nodeInstalled = Get-Command node -ErrorAction SilentlyContinue
if ($nodeInstalled) {
    $nodeVersion = node --version 2>&1
    Write-Host "  [OK] Node.js: $nodeVersion" -ForegroundColor Gray
} else {
    Write-Host "  [WARNING] Node.js not found in PATH. May need to restart terminal." -ForegroundColor Yellow
}

# ============================================
# 6. CONFIGURE GIT
# ============================================
Write-Host "`nConfiguring Git..." -ForegroundColor Green

$gitInstalled = Get-Command git -ErrorAction SilentlyContinue
if ($gitInstalled) {
    if ($GitName -and $GitEmail) {
        git config --global user.name $GitName
        git config --global user.email $GitEmail
        Write-Host "  [OK] Git identity configured: $GitName <$GitEmail>" -ForegroundColor Gray
    } else {
        Write-Host "  WARNING: Git identity not set. Run:" -ForegroundColor Yellow
        Write-Host "     git config --global user.name 'Your Name'" -ForegroundColor Yellow
        Write-Host "     git config --global user.email 'your.email@example.com'" -ForegroundColor Yellow
    }
    
    # Configure Git for Windows
    git config --global init.defaultBranch main
    git config --global core.autocrlf true
    git config --global core.longpaths true
    Write-Host "  [OK] Git defaults configured" -ForegroundColor Gray
} else {
    Write-Host "  WARNING: Git not found. Install it first." -ForegroundColor Yellow
}

# ============================================
# 7. CONFIGURE SSH KEYS
# ============================================
Write-Host "`nSetting up SSH keys..." -ForegroundColor Green

$sshDir = "$env:USERPROFILE\.ssh"
if (-not (Test-Path $sshDir)) {
    New-Item -ItemType Directory -Path $sshDir -Force | Out-Null
}

$sshKeyPath = "$sshDir\id_ed25519"
if (-not (Test-Path $sshKeyPath)) {
    Write-Host "  Generating SSH key for GitHub..." -ForegroundColor Yellow
    if ($GitEmail) {
        ssh-keygen -t ed25519 -C $GitEmail -f $sshKeyPath -N '""' 2>&1 | Out-Null
    } else {
        ssh-keygen -t ed25519 -C "dev@localhost" -f $sshKeyPath -N '""' 2>&1 | Out-Null
    }
    Write-Host "  [OK] SSH key generated at $sshKeyPath" -ForegroundColor Gray
    Write-Host "  Add this public key to GitHub:" -ForegroundColor Cyan
    Get-Content "$sshKeyPath.pub" | Write-Host -ForegroundColor Yellow
} else {
    Write-Host "  [OK] SSH key already exists" -ForegroundColor Gray
}

# ============================================
# 8. WINDOWS OPTIMIZATIONS
# ============================================
Write-Host "`nApplying Windows optimizations..." -ForegroundColor Green

# Enable long paths
try {
    New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force | Out-Null
    Write-Host "  [OK] Long paths enabled" -ForegroundColor Gray
} catch {
    Write-Host "  WARNING: Could not enable long paths (requires admin)" -ForegroundColor Yellow
}

# Add Defender exception for dev folder
try {
    Add-MpPreference -ExclusionPath "C:\dev" -ErrorAction SilentlyContinue
    Write-Host "  [OK] Windows Defender exception added for C:\dev" -ForegroundColor Gray
} catch {
    Write-Host "  WARNING: Could not add Defender exception (requires admin)" -ForegroundColor Yellow
}

# ============================================
# 9. CREATE SETUP COMPLETION MARKER
# ============================================
$setupMarker = "$devRoot\.setup_complete"
"Windows setup completed at: $(Get-Date)" | Out-File $setupMarker
Write-Host "`n[SUCCESS] Windows bootstrap complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "  1. Restart if WSL was installed" -ForegroundColor White
Write-Host "  2. Run setup_wsl.sh inside WSL" -ForegroundColor White
Write-Host "  3. Run verification_checklist.md tests" -ForegroundColor White
Write-Host "`nWelcome to FRAT OPS!" -ForegroundColor Cyan
