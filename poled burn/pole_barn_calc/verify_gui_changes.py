"""Diagnostic script to verify GUI changes are in place."""

import sys
from pathlib import Path

print("=" * 60)
print("GUI CHANGES VERIFICATION - Path B")
print("=" * 60)
print()

# Check 1: Verify we're in the right directory
current_dir = Path.cwd()
print(f"Current directory: {current_dir}")
expected_dir = Path(r"G:\My Drive\poled burn\pole_barn_calc")
if current_dir != expected_dir:
    print(f"⚠️  WARNING: Not in expected directory!")
    print(f"   Expected: {expected_dir}")
    print(f"   Actual:   {current_dir}")
else:
    print("✓ Correct directory")
print()

# Check 2: Verify GUI file exists and check its contents
gui_file = Path("apps/gui.py")
if not gui_file.exists():
    print("❌ ERROR: apps/gui.py not found!")
    sys.exit(1)

print(f"✓ GUI file found: {gui_file.absolute()}")
print()

# Check 3: Check for version string in title
gui_content = gui_file.read_text(encoding='utf-8')
if 'v0.2 (Path B)' in gui_content:
    print("✓ Version string found in GUI code")
else:
    print("❌ Version string NOT found - code may not be updated")
print()

# Check 4: Count input fields
if '("Peak Height (ft)", "peak_height"' in gui_content:
    print("❌ Peak Height input field still present!")
else:
    print("✓ Peak Height input field removed")

if '("Labor Rate ($/hr)", "labor_rate"' in gui_content:
    print("❌ Labor Rate input field still present!")
else:
    print("✓ Labor Rate input field removed")
print()

# Check 5: Verify run_calculation signature
if 'peak_height_var' in gui_content and 'def run_calculation(' in gui_content:
    # Check if peak_height_var is in the function signature
    run_calc_start = gui_content.find('def run_calculation(')
    if run_calc_start != -1:
        run_calc_sig = gui_content[run_calc_start:run_calc_start+500]
        if 'peak_height_var' in run_calc_sig:
            print("❌ peak_height_var still in run_calculation signature!")
        else:
            print("✓ peak_height_var removed from run_calculation")
        if 'labor_rate_var' in run_calc_sig:
            print("❌ labor_rate_var still in run_calculation signature!")
        else:
            print("✓ labor_rate_var removed from run_calculation")
print()

# Check 6: Try importing the module
print("Attempting to import GUI module...")
try:
    import apps.gui
    print(f"✓ Module imported successfully")
    print(f"  Module file: {apps.gui.__file__}")
    
    # Check if it's the right file
    if str(Path(apps.gui.__file__).absolute()) == str(gui_file.absolute()):
        print("✓ Imported from correct file location")
    else:
        print(f"⚠️  WARNING: Imported from different location!")
        print(f"   Expected: {gui_file.absolute()}")
        print(f"   Actual:   {Path(apps.gui.__file__).absolute()}")
        
except Exception as e:
    print(f"❌ Error importing module: {e}")
    import traceback
    traceback.print_exc()
print()

# Check 7: Verify model changes
print("Checking model changes...")
try:
    from systems.pole_barn.model import GeometryInputs, PricingInputs
    import inspect
    
    # Check GeometryInputs
    sig = inspect.signature(GeometryInputs)
    params = list(sig.parameters.keys())
    if 'peak_height' in params:
        param = sig.parameters['peak_height']
        if param.default == inspect.Parameter.empty:
            print("❌ peak_height is still required in GeometryInputs!")
        else:
            print("✓ peak_height is optional in GeometryInputs")
    else:
        print("❌ peak_height not found in GeometryInputs")
    
    # Check PricingInputs field order
    sig = inspect.signature(PricingInputs)
    params = list(sig.parameters.keys())
    if params[0] == 'material_markup' and params[1] == 'tax_rate':
        print("✓ PricingInputs has correct field order")
    else:
        print(f"⚠️  PricingInputs field order: {params}")
    
    if 'labor_rate' in params:
        param = sig.parameters['labor_rate']
        if param.default != inspect.Parameter.empty:
            print(f"✓ labor_rate has default value: {param.default}")
        else:
            print("❌ labor_rate has no default value")
    
except Exception as e:
    print(f"❌ Error checking models: {e}")
    import traceback
    traceback.print_exc()
print()

print("=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)
print()
print("If all checks passed, try running:")
print("  python -m apps.gui")
print()
print("You should see:")
print("  - Window title: 'Pole Barn Calculator - v0.2 (Path B)'")
print("  - 7 input fields (no Peak Height, no Labor Rate)")
print()

