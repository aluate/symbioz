# Otto + Life OS Control Panel
# PowerShell script with menu for starting/stopping servers

function Show-Menu {
    Clear-Host
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "   Otto + Life OS Control Panel" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. Start All Servers" -ForegroundColor Green
    Write-Host "2. Stop All Servers" -ForegroundColor Red
    Write-Host "3. Show My IP Address" -ForegroundColor Yellow
    Write-Host "4. Check Server Status" -ForegroundColor Magenta
    Write-Host "5. Exit" -ForegroundColor Gray
    Write-Host ""
}

function Start-AllServers {
    Write-Host "Starting all servers..." -ForegroundColor Green
    
    $repoRoot = Split-Path -Parent $PSScriptRoot
    
    # Start Otto API
    Start-Process cmd -ArgumentList "/k", "cd /d `"$repoRoot\apps\otto`" && otto server --host 0.0.0.0 --port 8001" -WindowStyle Normal
    
    Start-Sleep -Seconds 2
    
    # Start Life OS Backend
    Start-Process cmd -ArgumentList "/k", "cd /d `"$repoRoot\apps\life_os\backend`" && uvicorn main:app --reload --host 0.0.0.0 --port 8000" -WindowStyle Normal
    
    Start-Sleep -Seconds 2
    
    # Start Life OS Frontend
    Start-Process cmd -ArgumentList "/k", "cd /d `"$repoRoot\apps\life_os\frontend`" && npm run dev -- -H 0.0.0.0" -WindowStyle Normal
    
    Write-Host "All servers started!" -ForegroundColor Green
    Write-Host "Three windows will open - one for each server." -ForegroundColor Yellow
    Start-Sleep -Seconds 2
}

function Stop-AllServers {
    Write-Host "Stopping all servers..." -ForegroundColor Red
    
    # Kill processes on ports
    $ports = @(8001, 8000, 3000)
    foreach ($port in $ports) {
        $processes = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
        foreach ($pid in $processes) {
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
        }
    }
    
    # Also kill by window title
    Get-Process | Where-Object { $_.MainWindowTitle -like "*Otto API*" -or $_.MainWindowTitle -like "*Life OS*" } | Stop-Process -Force -ErrorAction SilentlyContinue
    
    Write-Host "All servers stopped!" -ForegroundColor Green
    Start-Sleep -Seconds 1
}

function Show-MyIP {
    Write-Host ""
    Write-Host "Your IP Addresses:" -ForegroundColor Cyan
    Write-Host ""
    
    $adapters = Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.254.*" }
    
    foreach ($adapter in $adapters) {
        $ip = $adapter.IPAddress
        Write-Host "  IP: $ip" -ForegroundColor Yellow
        Write-Host "    Life OS: http://$ip`:3000" -ForegroundColor Green
        Write-Host "    Otto API: http://$ip`:8001" -ForegroundColor Green
        Write-Host ""
    }
    
    Write-Host "Press any key to continue..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

function Check-ServerStatus {
    Write-Host ""
    Write-Host "Server Status:" -ForegroundColor Cyan
    Write-Host ""
    
    $ports = @{
        "Otto API" = 8001
        "Life OS Backend" = 8000
        "Life OS Frontend" = 3000
    }
    
    foreach ($server in $ports.Keys) {
        $port = $ports[$server]
        $connection = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
        
        if ($connection) {
            Write-Host "  $server (Port $port): " -NoNewline
            Write-Host "RUNNING" -ForegroundColor Green
        } else {
            Write-Host "  $server (Port $port): " -NoNewline
            Write-Host "STOPPED" -ForegroundColor Red
        }
    }
    
    Write-Host ""
    Write-Host "Press any key to continue..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

# Main loop
do {
    Show-Menu
    $choice = Read-Host "Select an option"
    
    switch ($choice) {
        "1" { Start-AllServers }
        "2" { Stop-AllServers }
        "3" { Show-MyIP }
        "4" { Check-ServerStatus }
        "5" { 
            Write-Host "Goodbye!" -ForegroundColor Cyan
            exit
        }
        default {
            Write-Host "Invalid option. Please try again." -ForegroundColor Red
            Start-Sleep -Seconds 1
        }
    }
} while ($choice -ne "5")

