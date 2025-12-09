# Desktop App Conversion Guide

## Overview

This guide documents the conversion of the Pole Barn Calculator from a CLI tool to a standalone Windows desktop application.

## ✅ Completed: GUI Implementation

### What Was Done

1. **Created `apps/gui.py`** - Full tkinter GUI application
   - Input fields for key dimensions and pricing parameters
   - Real-time calculation with error handling
   - Results display showing:
     - Geometry summary (dimensions, areas, bays)
     - Cost breakdown (material, labor, markup, tax, grand total)
     - Top 10 line items by cost
   - Status indicators and error messages
   - Configurable via `run_gui.bat`

2. **Enhanced `PoleBarnCalculator.load_config()`**
   - Added fallback to look for `parts.csv`, `pricing.csv`, `assemblies.csv` if `.example.csv` files not found
   - Better path handling for bundled executables

3. **Created `run_gui.bat`**
   - Launches GUI with dependency checking
   - Auto-installs pandas/click if missing

### GUI Features

**Input Fields:**
- Length, Width (ft)
- Eave Height, Peak Height (ft)
- Roof Pitch (ratio, e.g., 0.333 for 4:12)
- Pole Spacing (ft)
- Labor Rate ($/hr)
- Material Markup (e.g., 1.15 for 15%)
- Tax Rate (decimal, e.g., 0.08 for 8%)

**Output Display:**
- Geometry calculations (footprint, roof area, wall area, bays)
- Complete cost breakdown
- Top 10 line items sorted by cost
- Error messages with traceback for debugging

**Default Values:**
- Pre-filled with sensible defaults (40×30 barn, 12ft eave, etc.)
- Easy to adjust for testing

### Testing the GUI

**From Command Line:**
```powershell
cd "G:\My Drive\poled burn\pole_barn_calc"
python -m apps.gui
```

**From Batch File:**
- Double-click `run_gui.bat` in the `pole_barn_calc` folder

---

## 📋 Next Steps: PyInstaller Bundle

### Step 1: Install PyInstaller

```powershell
cd "G:\My Drive\poled burn\pole_barn_calc"
pip install pyinstaller
```

### Step 2: Create PyInstaller Spec File

Create `build_exe.spec` (or use command line directly):

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['apps/gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config', 'config'),  # Bundle config directory
    ],
    hiddenimports=['pandas', 'click'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PoleBarnCalculator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window for GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Can add .ico file here later
)
```

### Step 3: Build the Executable

**Option A: Using spec file:**
```powershell
pyinstaller build_exe.spec
```

**Option B: Direct command:**
```powershell
pyinstaller ^
  --onefile ^
  --windowed ^
  --name PoleBarnCalculator ^
  --add-data "config;config" ^
  --hidden-import pandas ^
  --hidden-import click ^
  apps/gui.py
```

**Key Parameters:**
- `--onefile` - Single executable file
- `--windowed` - No console window (GUI only)
- `--name PoleBarnCalculator` - Output exe name
- `--add-data "config;config"` - Bundle config folder (Windows uses `;` separator)
- `--hidden-import` - Ensure pandas/click are included

### Step 4: Test the Executable

The executable will be created in `dist/PoleBarnCalculator.exe`

1. Copy `dist/PoleBarnCalculator.exe` to a test location
2. Make sure the `config` folder is in the same directory (PyInstaller should handle this)
3. Double-click to run
4. Test with various inputs

**Note:** First run may be slow as Windows Defender scans the new exe.

---

## 📋 Next Steps: Windows Installer (Inno Setup)

### Step 1: Install Inno Setup

Download from: https://jrsoftware.org/isdl.php

### Step 2: Create Installer Script

Create `installer/PoleBarnCalculator.iss`:

```ini
[Setup]
AppName=Pole Barn Calculator
AppVersion=1.0.0
AppPublisher=Your Company Name
AppPublisherURL=
DefaultDirName={pf}\Pole Barn Calculator
DefaultGroupName=Pole Barn Calculator
OutputDir=dist\installer
OutputBaseFilename=PoleBarnCalculatorSetup
Compression=lzma
SolidCompression=yes
SetupIconFile=
LicenseFile=
WizardImageFile=
WizardSmallImageFile=

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1

[Files]
Source: "dist\PoleBarnCalculator.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "config\*"; DestDir: "{app}\config"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Pole Barn Calculator"; Filename: "{app}\PoleBarnCalculator.exe"
Name: "{commondesktop}\Pole Barn Calculator"; Filename: "{app}\PoleBarnCalculator.exe"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\Pole Barn Calculator"; Filename: "{app}\PoleBarnCalculator.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\PoleBarnCalculator.exe"; Description: "{cm:LaunchProgram,Pole Barn Calculator}"; Flags: nowait postinstall skipifsilent
```

### Step 3: Build Installer

1. Open Inno Setup Compiler
2. File → Open → Select `installer/PoleBarnCalculator.iss`
3. Build → Compile
4. Installer will be created in `dist/installer/PoleBarnCalculatorSetup.exe`

### Step 4: Test Installation

1. Run `PoleBarnCalculatorSetup.exe` on a test machine
2. Verify installation to Program Files
3. Check desktop shortcut creation
4. Verify app launches and calculates correctly

---

## 🔧 Development Workflow

### While Developing

1. **Use CLI for testing logic:**
   ```powershell
   python -m apps.cli --help
   ```

2. **Use GUI for testing UI:**
   ```powershell
   python -m apps.gui
   # Or double-click run_gui.bat
   ```

3. **Keep Tinker for code editing**

### When Ready to Release

1. **Test GUI thoroughly:**
   - Test with various inputs
   - Verify error handling
   - Check all calculations

2. **Build executable:**
   ```powershell
   pyinstaller build_exe.spec
   ```

3. **Test executable:**
   - Copy to clean test location
   - Verify it runs standalone
   - Test on different Windows versions if possible

4. **Build installer:**
   - Update version number in `.iss` file
   - Build installer in Inno Setup
   - Test installation on clean machine

5. **Ship installer:**
   - Distribute `PoleBarnCalculatorSetup.exe`
   - Users install and run - no Python required!

---

## 📝 Notes

### Config File Handling

- When bundled, config files are included in the exe's data directory
- PyInstaller extracts them to a temp directory at runtime
- The GUI's `get_config_dir()` function handles this automatically

### Dependencies

- **tkinter** - Built into Python (no install needed)
- **pandas** - Bundled by PyInstaller
- **click** - Bundled by PyInstaller (though GUI doesn't use it directly)

### File Sizes

- Expected exe size: ~50-100 MB (includes Python runtime + pandas)
- Installer size: Similar (compressed)

### Future Enhancements

- Add icon file (.ico) for the exe
- Add more input fields to GUI (doors, windows, overhangs, etc.)
- Add export to PDF/Excel
- Add save/load project files
- Add print functionality

---

## 🐛 Troubleshooting

### GUI won't launch
- Check Python is installed: `python --version`
- Install dependencies: `pip install pandas click`
- Check for import errors in console

### PyInstaller build fails
- Ensure all dependencies are installed
- Check that `config` directory exists
- Try building with `--debug=all` for more info

### Exe runs but can't find config files
- Verify `--add-data "config;config"` is in PyInstaller command
- Check that config files exist in source `config/` directory
- Test with `--debug=all` to see where it's looking

### Exe is very large
- This is normal - includes Python runtime
- Can use `--exclude-module` to remove unused modules
- Consider `--onedir` instead of `--onefile` for smaller size (but multiple files)

---

*Last Updated: After GUI implementation*

