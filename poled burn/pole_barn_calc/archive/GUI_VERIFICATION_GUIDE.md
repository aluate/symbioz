# GUI Verification Guide - Path B Changes

## Quick Verification Steps

### Step 1: Check Window Title
When you launch the GUI, the window title should now show:
**"Pole Barn Calculator - v0.2 (Path B)"**

If it still shows just "Pole Barn Calculator", you're running an old version.

---

### Step 2: Count Input Fields
The GUI should now have **7 input fields** (not 9):

1. Length (ft)
2. Width (ft)
3. Eave Height (ft)
4. Roof Pitch (ratio)
5. Pole Spacing (ft)
6. Material Markup
7. Tax Rate (decimal)

**Missing fields (should NOT appear):**
- ❌ Peak Height (ft) - REMOVED
- ❌ Labor Rate ($/hr) - REMOVED

---

### Step 3: Check Results Display
After clicking "Calculate", the results should show:
- **Peak Height: XX.XXft (derived)** - in the geometry summary
- Peak height should be calculated automatically

---

## Troubleshooting

### If GUI Still Shows Old Fields

**Option A: Clear Python Cache**
```powershell
cd "G:\My Drive\poled burn\pole_barn_calc"
# Remove Python cache files
Get-ChildItem -Path . -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -Path . -Recurse -Filter "*.pyc" | Remove-Item -Force
```

**Option B: Run Directly (Bypass Batch)**
```powershell
cd "G:\My Drive\poled burn\pole_barn_calc"
python -m apps.gui
```

**Option C: Verify File Location**
1. Open `apps/gui.py` in Cursor
2. Check line 233 - should say: `root.title("Pole Barn Calculator - v0.2 (Path B)")`
3. Check line 253-261 - should have only 7 items in the `inputs` list

**Option D: Check for Multiple Copies**
- Search your computer for other `pole_barn_calc` folders
- Make sure you're editing/running the one in `G:\My Drive\poled burn\pole_barn_calc`

---

## Expected Behavior

### Before Path B:
- 9 input fields (including Peak Height and Labor Rate)
- Window title: "Pole Barn Calculator"

### After Path B:
- 7 input fields (Peak Height and Labor Rate removed)
- Window title: "Pole Barn Calculator - v0.2 (Path B)"
- Peak height appears in results as "(derived)"
- Labor rate uses default $50/hr (not user-editable)

---

## Verification Command

Run this to verify the code is updated:

```powershell
cd "G:\My Drive\poled burn\pole_barn_calc"
python -c "import apps.gui; print('GUI module loaded'); print('Title check:', 'v0.2' in open('apps/gui.py').read())"
```

This will confirm:
1. The GUI module can be imported
2. The version string exists in the file

---

*Created to help verify Path B changes are active*

