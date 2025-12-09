# ⚡ WINDOWS OPTIMIZATION GUIDE

**Performance tuning for your dev machine.**

This guide covers optional optimizations to maximize your development workstation performance.

---

## 🚀 Quick Optimizations

### 1. Enable Long Paths (Already in setup.ps1)

```powershell
# Run as Administrator
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

**Restart required.**

---

### 2. Windows Defender Exceptions

Add dev folders to exclusions:

```powershell
# Run as Administrator
Add-MpPreference -ExclusionPath "C:\dev"
Add-MpPreference -ExclusionProcess "node.exe"
Add-MpPreference -ExclusionProcess "docker.exe"
```

---

### 3. Power Mode: Performance

```powershell
# Set power plan to High Performance
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
```

Or via Settings:
- Settings > System > Power & battery
- Power mode: **Best performance**

---

### 4. Disable Hibernate (Free Disk Space)

```powershell
# Run as Administrator
powercfg /hibernate off
```

**Frees ~4-8GB disk space** (size of RAM).

---

## 💾 Memory Optimization

### Virtual Memory (Pagefile) Configuration

**Recommended for 16GB+ RAM:**

```powershell
# Run as Administrator
# Set pagefile to 2GB initial, 4GB max
$pagefile = Get-WmiObject Win32_PageFileSetting
$pagefile.InitialSize = 2048
$pagefile.MaximumSize = 4096
$pagefile.Put()
```

**For 8GB RAM:**
- Initial: 4096 MB
- Maximum: 8192 MB

**Adjust via:**
- System Properties > Advanced > Performance Settings > Advanced > Virtual Memory

---

### Memory Compression

Windows 10/11 compresses memory by default. To disable (if causing issues):

```powershell
# Run as Administrator
Disable-MMAgent -MemoryCompression
```

**Note:** Only disable if you have performance issues. Memory compression is generally beneficial.

---

## 🗑️ Remove Bloatware

### Uninstall Pre-installed Apps

```powershell
# List all apps
Get-AppxPackage | Select Name, PackageFullName

# Remove specific app (example: Xbox)
Get-AppxPackage *xbox* | Remove-AppxPackage
```

**Common bloatware to remove:**
- Xbox (if not gaming)
- Candy Crush
- Microsoft News
- Weather
- Get Office

**Be careful:** Don't remove essential Windows components.

---

### Disable Startup Programs

```powershell
# Open Task Manager > Startup tab
# Or use:
Get-CimInstance Win32_StartupCommand | Select Name, Command, Location
```

Disable unnecessary startup apps via:
- Settings > Apps > Startup
- Or Task Manager > Startup tab

---

## 🐳 Docker Optimization

### Docker Desktop Settings

**Recommended settings:**

1. **Resources:**
   - CPUs: 50-75% of available cores
   - Memory: 4-8GB (if you have 16GB+)
   - Disk image size: 64GB minimum

2. **WSL Integration:**
   - Enable integration with Ubuntu
   - Enable integration with other distros (if needed)

3. **General:**
   - Start Docker Desktop when you log in: **Off** (optional)
   - Use the WSL 2 based engine: **On**

---

## 🪟 WSL2 Performance

### Use WSL Filesystem for Active Development

**Faster file I/O:**
- Use `~/dev` instead of `/mnt/c/dev` for active projects
- Copy to `/mnt/c/dev` when done

**Example:**
```bash
# Fast (WSL filesystem)
cd ~/dev/my-project

# Slower (Windows filesystem)
cd /mnt/c/dev/_projects/my-project
```

---

### WSL2 Memory Limit

Create `%UserProfile%\.wslconfig`:

```ini
[wsl2]
memory=8GB
processors=4
swap=2GB
localhostForwarding=true
```

**Adjust based on your RAM:**
- 16GB RAM: `memory=8GB`
- 32GB RAM: `memory=16GB`

**Restart WSL:**
```powershell
wsl --shutdown
```

---

## 🔧 Node.js Optimization

### npm Configuration

```bash
# In WSL
npm config set fetch-retries 3
npm config set fetch-retry-mintimeout 20000
npm config set fetch-retry-maxtimeout 120000
```

### Increase Node Memory (if needed)

```bash
# For large projects
export NODE_OPTIONS="--max-old-space-size=4096"
```

Add to `~/.bashrc`:
```bash
export NODE_OPTIONS="--max-old-space-size=4096"
```

---

## 🐍 Python Optimization

### pip Configuration

```bash
# In WSL
mkdir -p ~/.pip
cat > ~/.pip/pip.conf << EOF
[global]
cache-dir = ~/.cache/pip
timeout = 60
retries = 3
EOF
```

---

## 📦 Package Manager Optimization

### npm Cache Location

```bash
# Use WSL filesystem for cache (faster)
npm config set cache ~/.npm
```

### Poetry Cache

```bash
# Poetry already uses ~/.cache/poetry (WSL filesystem)
# No changes needed
```

---

## 🎯 Visual Studio Code Optimization

### Settings for Performance

Add to VS Code settings (`settings.json`):

```json
{
  "files.watcherExclude": {
    "**/node_modules/**": true,
    "**/.git/**": true,
    "**/dist/**": true,
    "**/build/**": true
  },
  "search.exclude": {
    "**/node_modules": true,
    "**/dist": true,
    "**/build": true
  },
  "files.exclude": {
    "**/.git": false
  }
}
```

---

## 🔍 Windows Search Optimization

### Exclude Dev Folders from Indexing

```powershell
# Run as Administrator
Add-MpPreference -ExclusionPath "C:\dev"
```

Or via Settings:
- Settings > Search > Searching Windows
- Add exclusion: `C:\dev`

---

## 🚫 Disable Unnecessary Services

**Be careful!** Only disable services you understand.

```powershell
# Run as Administrator
# Example: Disable Windows Search (if not using)
Stop-Service -Name "WSearch" -Force
Set-Service -Name "WSearch" -StartupType Disabled
```

**Common services to consider disabling:**
- Windows Search (if using Everything or similar)
- Print Spooler (if no printer)
- Bluetooth Support (if no Bluetooth devices)

**Don't disable:**
- Windows Update
- Windows Defender
- WSL services

---

## 📊 Performance Monitoring

### Check Current Performance

```powershell
# Run system report
.\system_report.ps1
```

### Task Manager

Monitor:
- CPU usage
- Memory usage
- Disk I/O
- Network activity

**Hotkey:** `Ctrl + Shift + Esc`

---

## 🎛️ BIOS/UEFI Optimizations

**If you have access to BIOS:**

1. **Enable Virtualization:**
   - Intel: Enable "Intel Virtualization Technology"
   - AMD: Enable "AMD-V" or "SVM"

2. **Disable Fast Boot:**
   - Can cause issues with WSL2

3. **Set Power Mode:**
   - High Performance (if available)

---

## ✅ Optimization Checklist

- [ ] Long paths enabled
- [ ] Windows Defender exceptions added
- [ ] Power mode set to Performance
- [ ] Hibernate disabled (if needed)
- [ ] Pagefile configured
- [ ] Bloatware removed
- [ ] Startup programs optimized
- [ ] Docker resources configured
- [ ] WSL2 memory limit set
- [ ] npm cache optimized
- [ ] VS Code settings optimized
- [ ] Dev folders excluded from Windows Search

---

## 🚨 Before Making Changes

1. **Create a restore point:**
   ```powershell
   # Run as Administrator
   Checkpoint-Computer -Description "Before Dev Optimizations"
   ```

2. **Test changes incrementally:**
   - Make one change at a time
   - Test performance
   - Revert if issues occur

3. **Document your changes:**
   - Keep notes on what you changed
   - Save configuration files

---

## 📝 Recommended Settings Summary

**For 16GB RAM, 8-core CPU:**

- Pagefile: 2GB initial, 4GB max
- WSL2 memory: 8GB
- Docker memory: 6GB
- Docker CPUs: 4 cores
- Power mode: High Performance
- Long paths: Enabled
- Hibernate: Disabled

---

## 🎉 After Optimization

Run verification tests:

```bash
# In WSL
node --version
python3 --version
docker run hello-world
```

Check system report:

```powershell
.\system_report.ps1
```

---

**Remember:** Optimization is about balance. Don't disable essential Windows features. Test changes and revert if you encounter issues.

---

**Last Updated:** 2024  
**Version:** 1.0

