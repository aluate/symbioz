# Assemblies Implementation Status

## Overview

This document tracks the implementation status of post-frame construction assemblies based on the deep dive research and design work.

**Date:** Assemblies Deep Dive Implementation  
**Phase:** Research + Limited Implementation (Path B continuation)

---

## ✅ Completed Implementation

### 1. Door & Window Assemblies (Changelog Entry [14])

**Status:** ✅ IMPLEMENTED

**Changes:**
- Added `_calculate_door_window_assemblies()` function in `assemblies.py`
- Calculates extra framing lumber for doors and windows:
  - Door framing: Headers (2x8), king studs, trimmers
  - Window framing: Headers (2x6), king studs, trimmers
- Calculates exterior trim for doors and windows:
  - Door trim: Head + 2 jambs
  - Window trim: Head + sill + 2 jambs

**Assumptions:**
- Standard door: 3' x 7' (36" x 84")
- Standard window: 3' x 3' (36" x 36")
- These can be made configurable in future phases

**New Assemblies:**
- `door_framing` - Extra framing lumber for doors (LF)
- `window_framing` - Extra framing lumber for windows (LF)
- `door_trim` - Exterior trim for doors (LF)
- `window_trim` - Exterior trim for windows (LF)

**CSV Updates:**
- Added to `assemblies.example.csv` with mappings to `LBR_2X6_LF` and trim parts
- Added `TRIM_DOOR` and `TRIM_WINDOW` to `parts.example.csv`
- Added pricing for door/window trim

**Tests:** Need to add tests verifying door/window counts increase these quantities

---

### 2. Exterior Finish Structure (Changelog Entry [15])

**Status:** ✅ PARTIALLY IMPLEMENTED (Structure only, no GUI)

**Changes:**
- Added `exterior_finish_type` field to `MaterialInputs` (default: `"metal_29ga"`)
- Updated roof/wall panel logic to branch on `exterior_finish_type`
- Supports:
  - `metal_29ga` (default) - Uses `roof_panels`, `sidewall_panels`, `endwall_panels`
  - `metal_26ga` - Uses `roof_panels_26ga`, `sidewall_panels_26ga`, `endwall_panels_26ga`
  - `lap_siding` - TODO placeholder
  - `stucco` - TODO placeholder

**New Parts:**
- `METAL_PANEL_26_SQFT` - 26ga metal panels (added to parts and pricing CSVs)

**New Assemblies:**
- `roof_panels_26ga` - 26ga roof panels
- `sidewall_panels_26ga` - 26ga sidewall panels
- `endwall_panels_26ga` - 26ga endwall panels

**TODOs:**
- Implement lap siding assemblies
- Implement stucco assemblies
- Wire GUI dropdown (deferred to future phase)

**Tests:** Need to add tests verifying 26ga vs 29ga selection works

---

### 3. Insulation Types - Wall/Roof Split (Changelog Entry [16])

**Status:** ✅ IMPLEMENTED

**Changes:**
- Added `wall_insulation_type` and `roof_insulation_type` fields to `MaterialInputs` (default: `"none"`)
- Updated `_calculate_insulation_quantities()` to handle separate wall/roof insulation
- Supports insulation types:
  - `fiberglass_batts` - Standard fiberglass (R-19 typical)
  - `rock_wool` - Rock wool batts
  - `rigid_board` - Rigid board insulation
  - `spray_foam` - Spray foam insulation

**New Parts:**
- `INS_ROCKWOOL_SQFT` - Rock wool insulation
- `INS_RIGID_SQFT` - Rigid board insulation
- `INS_SPRAYFOAM_SQFT` - Spray foam insulation

**New Assemblies:**
- `wall_insulation` - Wall fiberglass (default)
- `wall_insulation_rockwool` - Wall rock wool
- `wall_insulation_rigid` - Wall rigid board
- `wall_insulation_sprayfoam` - Wall spray foam
- `roof_insulation` - Roof fiberglass (default)
- `roof_insulation_rockwool` - Roof rock wool
- `roof_insulation_rigid` - Roof rigid board
- `roof_insulation_sprayfoam` - Roof spray foam

**CSV Updates:**
- Added all insulation type assemblies to `assemblies.example.csv`
- Added all insulation parts to `parts.example.csv` and `pricing.example.csv`

**TODOs:**
- Wire GUI dropdowns for wall/roof insulation (deferred to future phase)
- Subtract door/window openings from wall insulation area (for accuracy)

**Tests:** Need to add tests verifying insulation types produce correct quantities

---

### 4. MEP Allowances (Changelog Entry [18])

**Status:** ✅ IMPLEMENTED

**Changes:**
- Added MEP allowance fields to `PricingInputs`:
  - `include_electrical: bool = False`
  - `electrical_allowance: float = 0.0`
  - `include_plumbing: bool = False`
  - `plumbing_allowance: float = 0.0`
  - `include_mechanical: bool = False`
  - `mechanical_allowance: float = 0.0`
- Updated `price_material_takeoff()` to create MEP allowance line items
- MEP allowances are:
  - Added as separate `PricedLineItem` entries with category "MEP"
  - Included in material subtotal and grand total
  - NOT marked up (markup_percent = 0.0)

**New Line Items:**
- `electrical_allowance` - Electrical allowance (if enabled and > 0)
- `plumbing_allowance` - Plumbing allowance (if enabled and > 0)
- `mechanical_allowance` - Mechanical allowance (if enabled and > 0)

**TODOs:**
- Wire GUI toggles and allowance inputs (deferred to future phase)
- Consider code-minimum calculations (e.g., outlet spacing per IRC)

**Tests:** Need to add tests verifying MEP allowances appear when enabled

---

## 📋 Files Modified

### Core Models
- `systems/pole_barn/model.py`
  - Added `exterior_finish_type`, `wall_insulation_type`, `roof_insulation_type` to `MaterialInputs`
  - Added MEP allowance fields to `PricingInputs`

### Assemblies Logic
- `systems/pole_barn/assemblies.py`
  - Added `_calculate_door_window_assemblies()` function
  - Added `_calculate_insulation_quantities()` function (enhanced)
  - Updated `calculate_material_quantities()` to accept `geometry_inputs` parameter
  - Updated roof/wall panel logic to branch on `exterior_finish_type`

### Pricing Logic
- `systems/pole_barn/pricing.py`
  - Updated `price_material_takeoff()` to create MEP allowance line items
  - Updated `_create_simple_assembly_mapping()` with new assemblies

### Calculator
- `systems/pole_barn/calculator.py`
  - Updated to pass `geometry_inputs` to `calculate_material_quantities()`

### Configuration Files
- `config/parts.example.csv`
  - Added: `METAL_PANEL_26_SQFT`, `TRIM_DOOR`, `TRIM_WINDOW`
  - Added: `INS_ROCKWOOL_SQFT`, `INS_RIGID_SQFT`, `INS_SPRAYFOAM_SQFT`
  - Added: `SHEATHING_OSB_SQFT`, `SHEATHING_PLY_SQFT`, `OVERHEAD_DOOR`

- `config/pricing.example.csv`
  - Added unit prices for all new parts

- `config/assemblies.example.csv`
  - Added: `door_framing`, `window_framing`, `door_trim`, `window_trim`
  - Added: `roof_panels_26ga`, `sidewall_panels_26ga`, `endwall_panels_26ga`
  - Added: All insulation type variants (wall and roof)

---

## 🟡 Partially Addressed Changelog Entries

### Entry [14] - Door & Window Assemblies
- ✅ Framing and trim calculations implemented
- ⏳ GUI wiring deferred (no GUI changes in this phase)
- ⏳ Multiple door/window sizes deferred (using standard sizes for now)

### Entry [15] - Exterior Finish
- ✅ Structure implemented (29ga vs 26ga)
- ⏳ Lap siding implementation deferred
- ⏳ Stucco implementation deferred
- ⏳ GUI wiring deferred

### Entry [16] - Insulation Types
- ✅ Wall/roof split implemented
- ✅ All insulation types supported
- ⏳ GUI wiring deferred
- ⏳ Opening subtraction for accuracy deferred

### Entry [18] - MEP Allowances
- ✅ Allowance structure implemented
- ⏳ GUI wiring deferred
- ⏳ Code-minimum calculations deferred

---

## 🔴 Not Yet Implemented (Future Phases)

### Entry [17] - Roll-up Doors
- Structure not yet implemented
- Needs overhead door assembly logic
- Part `OVERHEAD_DOOR` added to CSV but not used

### Entry [19] - Post Type Selector
- Structure not yet implemented
- Needs branching logic for PT vs laminated

### Entry [20] - Truss/Post Connection Type
- Structure not yet implemented
- Needs logic for notched vs cleated (affects fasteners/labor)

### Entry [21] - Multiple Door Sizes
- Deferred to Phase 2
- Currently uses standard sizes

### Entry [22] - Lean-to Module
- Deferred to Phase 2
- Complex feature requiring separate geometry

---

## 📝 Assumptions Documented

### Door/Window Sizes
- Standard door: 3' x 7' (36" x 84")
- Standard window: 3' x 3' (36" x 36")
- **Source:** Industry standard sizes (documented in ASSEMBLIES_DESIGN.md)

### Framing Details
- Door header: 2x8, length = door width + 6"
- Window header: 2x6, length = window width + 6"
- King studs: 2 per opening
- Trimmers: 2 per opening
- **Source:** Typical construction practice (documented in ASSEMBLIES_DESIGN.md)

### Insulation Coverage
- Based on wall/roof area
- Waste factor: 1.0 for batts (cut to fit), 1.05 for rigid board
- **Source:** Construction practice (documented in ASSEMBLIES_DESIGN.md)

### MEP Allowances
- Treated as cost buckets only (not detailed takeoff)
- Not marked up (markup_percent = 0.0)
- **Source:** Estimator practice (documented in ASSEMBLIES_DESIGN.md)

---

## 🧪 Testing Status

### Tests Needed
- [ ] Door/window framing quantities increase with door/window counts
- [ ] Door/window trim quantities increase with door/window counts
- [ ] 26ga panels use correct part_id when `exterior_finish_type == "metal_26ga"`
- [ ] Wall insulation appears when `wall_insulation_type != "none"`
- [ ] Roof insulation appears when `roof_insulation_type != "none"`
- [ ] Different insulation types map to correct parts
- [ ] MEP allowances appear in priced output when enabled
- [ ] MEP allowances are included in grand total but not marked up

### Existing Tests
- Should still pass (no breaking changes)
- May need updates for new field defaults

---

## 📚 Research Sources

All assumptions and design decisions are documented in:
- **`ASSEMBLIES_DESIGN.md`** - Complete design document with sources

Key sources referenced:
- Post-Frame Building Design Manual (NFBA)
- IRC Section R301, R402, E3801.2
- Industry standard spacing practices (24" o.c. typical)
- Manufacturer specifications (panel coverage, etc.)
- Construction practice (waste factors, typical sizes)

---

## 🎯 Next Steps

1. **Add Tests:**
   - Test door/window assemblies
   - Test exterior finish branching
   - Test insulation type selection
   - Test MEP allowances

2. **GUI Wiring (Future Phase):**
   - Add exterior finish dropdown
   - Add wall/roof insulation dropdowns
   - Add MEP toggles and allowance inputs

3. **Enhancements (Future Phases):**
   - Implement lap siding and stucco
   - Implement roll-up doors
   - Implement post type and connection type logic
   - Add multiple door/window sizes
   - Subtract openings from insulation area

---

*Status document created: Assemblies Deep Dive Implementation*

