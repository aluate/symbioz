# Setup and Fixes Summary

## ✅ Fixed Issues

### Dataclass Field Ordering (FIXED)
**Problem:** `MaterialInputs` had required fields (`wall_material_type`) after optional fields (`roof_gauge`), causing:
```
TypeError: non-default argument 'wall_material_type' follows default argument 'roof_gauge'
```

**Solution:** Reordered `MaterialInputs` in `systems/pole_barn/model.py`:
- All required fields (no defaults) moved to the top
- All optional fields (with defaults) moved to the bottom

**Status:** ✅ FIXED - All dataclasses now have correct field ordering

### Verified Dataclass Ordering
All dataclasses checked and confirmed correct:
- ✅ `GeometryInputs` - All required, no defaults
- ✅ `MaterialInputs` - **FIXED** - Required first, then optional
- ✅ `PricingInputs` - Required first, then optional
- ✅ `AssemblyInputs` - Required first, then optional
- ✅ `GeometryModel` - Required first, then optional
- ✅ `AssemblyQuantity` - Required first, then optional
- ✅ `MaterialTakeoff` - All required
- ✅ `PricedLineItem` - Required first, then optional
- ✅ `PricingSummary` - All required
- ✅ `PoleBarnInputs` - Required first, then optional

## ⚠️ Setup Required

### Install Dependencies
The calculator requires `pandas` which may not be installed. To install:

```powershell
cd "G:\My Drive\poled burn\pole_barn_calc"
pip install pandas click
```

Or install the project in development mode:
```powershell
pip install -e .
```

This will install all dependencies listed in `pyproject.toml`.

## 🚀 Running the Calculator

### Option 1: Batch File (Easiest)
1. Double-click `run_example.bat` in the `pole_barn_calc` folder
2. This will run a complete example calculation

### Option 2: Command Line
```powershell
cd "G:\My Drive\poled burn\pole_barn_calc"
python -m apps.cli --help
```

### Option 3: Full Example
```powershell
cd "G:\My Drive\poled burn\pole_barn_calc"
python -m apps.cli --project-name "Test Barn" --length 40 --width 30 --eave-height 12 --peak-height 16 --roof-pitch 0.333 --pole-spacing-length 10 --pole-spacing-width 8 --pole-diameter 6 --pole-depth 4 --roof-material metal --wall-material metal --truss-type standard --truss-spacing 10 --purlin-spacing 2 --girt-spacing 2 --foundation-type concrete_pad --labor-rate 50 --material-markup 1.15 --tax-rate 0.08 --assembly-method standard --fastening-type screws
```

## 📋 Next Steps

1. **Install dependencies** (if not already installed):
   ```powershell
   pip install pandas click
   ```

2. **Test the calculator**:
   - Run `run_example.bat` to see a full calculation
   - Adjust the example values in `run_example.bat` for your own tests

3. **Customize pricing**:
   - Edit `config/pricing.example.csv` with your vendor prices
   - Adjust waste factors in `config/assemblies.example.csv`

4. **Future enhancements** (Phase 4):
   - Add fastener quantity calculations
   - Add concrete quantity calculations
   - Fine-tune labor estimates

## 🔍 Troubleshooting

### "ModuleNotFoundError: No module named 'pandas'"
**Solution:** Install pandas: `pip install pandas`

### "ModuleNotFoundError: No module named 'apps'"
**Solution:** Make sure you're in the `pole_barn_calc` directory when running

### Batch file opens PowerShell but shows errors
**Solution:** 
1. Check that Python is installed: `python --version`
2. Install dependencies: `pip install pandas click`
3. Make sure you're running from the `pole_barn_calc` directory

