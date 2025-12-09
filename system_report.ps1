# ============================================
# SYSTEM REPORT GENERATOR
# ============================================
# Generates a comprehensive system report
# Usage: .\system_report.ps1

Write-Host "🔍 FRAT DEV MACHINE - SYSTEM REPORT" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

$report = @{
    Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Windows = @{}
    WSL = @{}
    Tools = @{}
    Performance = @{}
}

# ============================================
# WINDOWS SYSTEM INFO
# ============================================
Write-Host "📊 Windows System Information..." -ForegroundColor Green

$report.Windows.OS = (Get-CimInstance Win32_OperatingSystem).Caption
$report.Windows.Version = (Get-CimInstance Win32_OperatingSystem).Version
$report.Windows.Build = (Get-CimInstance Win32_OperatingSystem).BuildNumber
$report.Windows.Architecture = (Get-CimInstance Win32_OperatingSystem).OSArchitecture

$report.Windows.RAM = [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 2)
$report.Windows.CPU = (Get-CimInstance Win32_Processor).Name
$report.Windows.Cores = (Get-CimInstance Win32_Processor).NumberOfCores

$report.Windows.Disk = @{}
$drives = Get-PSDrive -PSProvider FileSystem
foreach ($drive in $drives) {
    $disk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='$($drive.Name):'"
    if ($disk) {
        $report.Windows.Disk[$drive.Name] = @{
            Total = [math]::Round($disk.Size / 1GB, 2)
            Free = [math]::Round($disk.FreeSpace / 1GB, 2)
            Used = [math]::Round(($disk.Size - $disk.FreeSpace) / 1GB, 2)
        }
    }
}

# ============================================
# WSL INFORMATION
# ============================================
Write-Host "🐧 WSL Information..." -ForegroundColor Green

try {
    $wslVersion = wsl --version 2>&1
    $report.WSL.Version = $wslVersion
    $report.WSL.Installed = $true
    
    $wslList = wsl --list --verbose 2>&1
    $report.WSL.Distributions = $wslList
    
    # Try to get WSL info
    $wslInfo = wsl uname -a 2>&1
    if ($wslInfo) {
        $report.WSL.Kernel = $wslInfo
    }
} catch {
    $report.WSL.Installed = $false
    $report.WSL.Error = $_.Exception.Message
}

# ============================================
# INSTALLED TOOLS
# ============================================
Write-Host "🛠️  Checking installed tools..." -ForegroundColor Green

$tools = @(
    @{Name="Git"; Command="git"; Arg="--version"},
    @{Name="GitHub CLI"; Command="gh"; Arg="--version"},
    @{Name="Docker"; Command="docker"; Arg="--version"},
    @{Name="VS Code"; Command="code"; Arg="--version"},
    @{Name="Node.js"; Command="node"; Arg="--version"; WSL=$true},
    @{Name="npm"; Command="npm"; Arg="--version"; WSL=$true},
    @{Name="Python"; Command="python3"; Arg="--version"; WSL=$true},
    @{Name="Poetry"; Command="poetry"; Arg="--version"; WSL=$true}
)

$report.Tools = @{}

foreach ($tool in $tools) {
    try {
        if ($tool.WSL) {
            $output = wsl $tool.Command $tool.Arg 2>&1
        } else {
            $output = & $tool.Command $tool.Arg 2>&1
        }
        if ($LASTEXITCODE -eq 0 -or $output) {
            $report.Tools[$tool.Name] = $output -join "`n"
        } else {
            $report.Tools[$tool.Name] = "Not found"
        }
    } catch {
        $report.Tools[$tool.Name] = "Not found"
    }
}

# ============================================
# DEV FOLDER STRUCTURE
# ============================================
Write-Host "📁 Checking dev folder structure..." -ForegroundColor Green

$devFolders = @(
    "C:\dev\_projects",
    "C:\dev\_templates",
    "C:\dev\_repos"
)

$report.DevFolders = @{}
foreach ($folder in $devFolders) {
    if (Test-Path $folder) {
        $items = (Get-ChildItem $folder -ErrorAction SilentlyContinue).Count
        $report.DevFolders[$folder] = @{
            Exists = $true
            ItemCount = $items
        }
    } else {
        $report.DevFolders[$folder] = @{
            Exists = $false
        }
    }
}

# ============================================
# PERFORMANCE METRICS
# ============================================
Write-Host "⚡ Performance metrics..." -ForegroundColor Green

$report.Performance.CPUUsage = [math]::Round((Get-Counter '\Processor(_Total)\% Processor Time').CounterSamples[0].CookedValue, 2)
$report.Performance.MemoryUsage = [math]::Round((Get-CimInstance Win32_OperatingSystem).TotalVisibleMemorySize / 1MB - (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB, 2)

# ============================================
# OUTPUT REPORT
# ============================================
Write-Host ""
Write-Host "📋 SYSTEM REPORT" -ForegroundColor Cyan
Write-Host "================" -ForegroundColor Cyan
Write-Host ""

Write-Host "🪟 WINDOWS" -ForegroundColor Yellow
Write-Host "  OS: $($report.Windows.OS)"
Write-Host "  Version: $($report.Windows.Version)"
Write-Host "  Architecture: $($report.Windows.Architecture)"
Write-Host "  RAM: $($report.Windows.RAM) GB"
Write-Host "  CPU: $($report.Windows.CPU)"
Write-Host "  Cores: $($report.Windows.Cores)"
Write-Host ""

Write-Host "💾 DISK SPACE" -ForegroundColor Yellow
foreach ($drive in $report.Windows.Disk.Keys) {
    $disk = $report.Windows.Disk[$drive]
    Write-Host "  $drive`: $($disk.Free) GB free / $($disk.Total) GB total"
}
Write-Host ""

Write-Host "🐧 WSL" -ForegroundColor Yellow
if ($report.WSL.Installed) {
    Write-Host "  Status: Installed"
    if ($report.WSL.Kernel) {
        Write-Host "  Kernel: $($report.WSL.Kernel)"
    }
} else {
    Write-Host "  Status: Not installed"
}
Write-Host ""

Write-Host "🛠️  TOOLS" -ForegroundColor Yellow
foreach ($tool in $report.Tools.Keys) {
    $version = $report.Tools[$tool]
    if ($version -ne "Not found") {
        Write-Host "  ✓ $tool`: $version" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $tool`: Not installed" -ForegroundColor Red
    }
}
Write-Host ""

Write-Host "📁 DEV FOLDERS" -ForegroundColor Yellow
foreach ($folder in $report.DevFolders.Keys) {
    $info = $report.DevFolders[$folder]
    if ($info.Exists) {
        Write-Host "  ✓ $folder ($($info.ItemCount) items)" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $folder (missing)" -ForegroundColor Red
    }
}
Write-Host ""

Write-Host "⚡ PERFORMANCE" -ForegroundColor Yellow
Write-Host "  CPU Usage: $($report.Performance.CPUUsage)%"
Write-Host "  Memory Usage: $($report.Performance.MemoryUsage) GB"
Write-Host ""

# ============================================
# RECOMMENDATIONS
# ============================================
Write-Host "💡 RECOMMENDATIONS" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan
Write-Host ""

$recommendations = @()

# Check RAM
if ($report.Windows.RAM -lt 8) {
    $recommendations += "⚠️  RAM is below 8GB. Consider upgrading for better performance."
}

# Check disk space
foreach ($drive in $report.Windows.Disk.Keys) {
    $disk = $report.Windows.Disk[$drive]
    $freePercent = ($disk.Free / $disk.Total) * 100
    if ($freePercent -lt 10) {
        $recommendations += "⚠️  $drive`: Low disk space ($([math]::Round($freePercent, 1))% free). Consider cleaning up."
    }
}

# Check WSL
if (-not $report.WSL.Installed) {
    $recommendations += "⚠️  WSL not installed. Run setup.ps1 to install."
}

# Check tools
$missingTools = @()
foreach ($tool in $report.Tools.Keys) {
    if ($report.Tools[$tool] -eq "Not found") {
        $missingTools += $tool
    }
}
if ($missingTools.Count -gt 0) {
    $recommendations += "⚠️  Missing tools: $($missingTools -join ', '). Run setup scripts to install."
}

if ($recommendations.Count -eq 0) {
    Write-Host "✅ System looks good! No critical issues found." -ForegroundColor Green
} else {
    foreach ($rec in $recommendations) {
        Write-Host $rec -ForegroundColor Yellow
    }
}

Write-Host ""

# ============================================
# SAVE REPORT
# ============================================
$reportFile = "C:\dev\system_report_$(Get-Date -Format 'yyyyMMdd_HHmmss').json"
$report | ConvertTo-Json -Depth 10 | Out-File $reportFile
Write-Host "📄 Full report saved to: $reportFile" -ForegroundColor Cyan
Write-Host ""

Write-Host "✅ Report complete!" -ForegroundColor Green

