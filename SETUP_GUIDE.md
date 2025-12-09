# Development Environment Setup Guide

## What Happened on Your Other Computer

When you tried to set up your development environment on a new computer, you likely encountered these common issues:

### Common Problems:
1. **Python not installed** - Your batch files (`START_OTTO_WINDOWS.bat`, `LAUNCH_SYMBIOZ.bat`) check for Python but can't install it automatically
2. **Node.js not installed** - Required for frontend projects (Life OS, Symbioz Web)
3. **Programs not in PATH** - Even if installed, Python/Node might not be accessible from command line
4. **Missing dependencies** - Python packages and npm packages need to be installed
5. **Virtual environments not created** - Python projects need isolated environments
6. **Multiple requirements files** - Different projects have different dependencies scattered across folders

### Why Manual Setup is Hard:
- You have **9+ requirements.txt files** across different projects
- You have **11+ package.json files** for Node.js projects
- Each project needs its dependencies installed separately
- Virtual environments need to be created manually
- No single script to do everything at once

---

## Solution: One-Click Setup Script

I've created **`SETUP_NEW_COMPUTER.ps1`** - a comprehensive PowerShell script that does everything automatically!

### What It Does:

1. ✅ **Checks for Windows Package Manager (winget)**
   - Uses winget to automatically install Python and Node.js if missing
   - Falls back to manual installation if winget isn't available

2. ✅ **Checks and Installs Python 3.11+**
   - Verifies it's installed and in PATH
   - **Automatically installs Python 3.11 using winget if missing**
   - Falls back to opening download page if winget fails
   - Tests both `python` and `py` commands

3. ✅ **Checks and Installs Node.js**
   - Verifies installation
   - **Automatically installs Node.js LTS using winget if missing**
   - Falls back to opening download page if winget fails
   - Checks npm is available

3. ✅ **Upgrades pip** to latest version

4. ✅ **Finds and installs ALL Python dependencies**
   - Scans entire repo for `requirements.txt` files
   - Installs packages from each one
   - Handles virtual environments automatically

5. ✅ **Creates virtual environments**
   - For `apps\symbioz_cli`
   - For `apps\otto`
   - For `apps\life_os\backend`
   - Installs dependencies in each venv

6. ✅ **Finds and installs ALL Node.js dependencies**
   - Scans entire repo for `package.json` files
   - Runs `npm install` in each directory
   - Skips if already installed

7. ✅ **Verifies everything works**
   - Tests Python, Node.js, and npm
   - Reports success or issues

---

## How to Use

### On a New Computer:

1. **Copy the script to your new computer**
   - The script is at: `e:\My Drive\SETUP_NEW_COMPUTER.ps1`
   - Make sure your OneDrive/Drive is synced, or copy it manually

2. **Run the script:**
   - **Option A:** Right-click → "Run with PowerShell"
   - **Option B:** Open PowerShell, navigate to the script, run: `.\SETUP_NEW_COMPUTER.ps1`
   - **Option C:** Double-click (if PowerShell execution policy allows)

3. **The script will automatically:**
   - Install Python 3.11 if missing (using Windows Package Manager)
   - Install Node.js LTS if missing (using Windows Package Manager)
   - Install all dependencies
   - Set up virtual environments
   - **No manual installation needed!** (unless winget isn't available)

4. **Wait for completion:**
   - The script will show progress for each step
   - It may take 5-10 minutes depending on internet speed
   - You'll see a summary when done

---

## What Gets Installed

### Python Projects:
- **Otto** (`apps\otto`) - AI assistant
- **Life OS Backend** (`apps\life_os\backend`) - Task management API
- **Symbioz CLI** (`apps\symbioz_cli`) - Game CLI
- **Infra tools** (`infra`) - Infrastructure management
- Plus any other projects with `requirements.txt`

### Node.js Projects:
- **Life OS Frontend** (`apps\life_os\frontend`) - Next.js frontend
- **Symbioz Web** (`apps\symbioz_web`) - Web UI
- Plus any other projects with `package.json`

---

## After Setup

Once the script completes successfully, you can:

1. **Start Otto + Life OS:**
   ```batch
   START_OTTO_WINDOWS.bat
   ```

2. **Start Symbioz:**
   ```batch
   LAUNCH_SYMBIOZ.bat
   ```

3. **Run any Python scripts:**
   ```powershell
   python apps\otto\test_otto_phase3.py
   ```

---

## Troubleshooting

### "Execution Policy" Error
If PowerShell blocks the script:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Python/Node.js Not Found After Installation
- The script tries to automatically refresh PATH, but if it still doesn't work:
- Close and reopen PowerShell/terminal
- Run the script again
- If automatic installation failed, the script will open download pages for manual installation

### Some Packages Fail to Install
- Check your internet connection
- Some packages may require Visual C++ Build Tools (Windows)
- The script will continue even if some packages fail

### Virtual Environment Issues
- If venv creation fails, try: `python -m venv venv --clear`
- Make sure you have write permissions in the project folders

---

## Manual Alternative

If the script doesn't work, you can set up manually:

1. **Install Python 3.11+** from python.org (check "Add to PATH")
2. **Install Node.js LTS** from nodejs.org
3. **For each Python project:**
   ```powershell
   cd apps\otto
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. **For each Node.js project:**
   ```powershell
   cd apps\life_os\frontend
   npm install
   ```

But the script is much easier! 🚀

---

## Summary

**The Problem:** Setting up a new computer required manually installing Python, Node.js, and dozens of dependencies across multiple projects.

**The Solution:** `SETUP_NEW_COMPUTER.ps1` - one script that does everything automatically.

**To Use:** Just run the script on a new computer, and it will guide you through any missing prerequisites and install everything else automatically.
