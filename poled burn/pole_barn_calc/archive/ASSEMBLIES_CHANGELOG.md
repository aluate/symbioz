# Assemblies Changelog - Research & Implementation

This document tracks changes to assemblies logic, with sources for all findings and assumptions.

---

## Research Phase - Sources

### Primary Sources

1. **Post-Frame Construction Practices**
   - **Source:** National Frame Builders Association (NFBA) - General construction guidelines
   - **Use:** Typical spacing, sizing, and assembly practices
   - **Note:** Summarized industry practices, not copyrighted material

2. **Building Codes**
   - **Source:** International Residential Code (IRC)
     - Section R301 - General construction requirements
     - Section R402 - Energy code (insulation R-values)
     - Section E3801.2 - Electrical outlet spacing requirements
   - **Use:** Code minimums for MEP, general construction practices
   - **Note:** Referenced for requirements, not reproduced verbatim

3. **Material Specifications**
   - **Source:** Manufacturer literature (metal panels, insulation, etc.)
   - **Use:** Panel coverage, sheet sizes, R-values
   - **Note:** Industry standard specifications

4. **Construction Practices**
   - **Source:** Industry standard practices (widely known)
   - **Use:** Waste factors, typical sizes, spacing conventions
   - **Note:** Common knowledge in construction industry

---

## Implementation Changes

### Change 1: Door & Window Assemblies (Entry [14])

**Date:** Assemblies Deep Dive Implementation  
**Source:** ASSEMBLIES_DESIGN.md (based on industry practice)

**What Changed:**
- Added door and window framing calculations
- Added door and window trim calculations

**Assumptions:**
- Standard door: 3' x 7' (36" x 84") - **Source:** Industry standard sizes
- Standard window: 3' x 3' (36" x 36") - **Source:** Industry standard sizes
- Door header: 2x8, length = door width + 6" - **Source:** Typical construction practice
- Window header: 2x6, length = window width + 6" - **Source:** Typical construction practice
- King studs: 2 per opening - **Source:** Standard framing practice
- Trimmers: 2 per opening - **Source:** Standard framing practice

**Files Modified:**
- `systems/pole_barn/assemblies.py` - Added `_calculate_door_window_assemblies()`
- `systems/pole_barn/calculator.py` - Pass geometry_inputs to assemblies
- `config/assemblies.example.csv` - Added door/window assemblies
- `config/parts.example.csv` - Added door/window trim parts
- `config/pricing.example.csv` - Added trim pricing

**References:**
- ASSEMBLIES_DESIGN.md - Section 7: Doors and Windows

---

### Change 2: Exterior Finish Structure (Entry [15])

**Date:** Assemblies Deep Dive Implementation  
**Source:** ASSEMBLIES_DESIGN.md (based on material specifications)

**What Changed:**
- Added `exterior_finish_type` field to `MaterialInputs`
- Updated panel logic to branch on finish type (29ga vs 26ga)

**Assumptions:**
- 29ga panels: Standard residential - **Source:** Manufacturer catalogs
- 26ga panels: Commercial/high-wind areas - **Source:** Manufacturer catalogs
- Panel coverage: 36" typical - **Source:** Manufacturer specifications
- Waste factor: 5% (1.05) - **Source:** Construction practice

**Files Modified:**
- `systems/pole_barn/model.py` - Added `exterior_finish_type` field
- `systems/pole_barn/assemblies.py` - Updated panel logic
- `config/parts.example.csv` - Added `METAL_PANEL_26_SQFT`
- `config/pricing.example.csv` - Added 26ga pricing
- `config/assemblies.example.csv` - Added 26ga panel assemblies

**References:**
- ASSEMBLIES_DESIGN.md - Section 4: Roof and Wall Panels

**TODOs:**
- Implement lap siding assemblies
- Implement stucco assemblies
- **Source for future:** Manufacturer specifications for lap siding and stucco systems

---

### Change 3: Insulation Types - Wall/Roof Split (Entry [16])

**Date:** Assemblies Deep Dive Implementation  
**Source:** ASSEMBLIES_DESIGN.md (based on IRC and manufacturer specs)

**What Changed:**
- Added `wall_insulation_type` and `roof_insulation_type` fields
- Implemented separate wall and roof insulation calculations
- Added support for multiple insulation types

**Assumptions:**
- Fiberglass batts: R-19 typical for walls, R-30+ for roof - **Source:** IRC R402, manufacturer specs
- Rock wool: Similar R-values, higher cost - **Source:** Manufacturer specifications
- Rigid board: R-5 to R-7 per inch - **Source:** Manufacturer specifications
- Spray foam: R-6 to R-7 per inch (closed-cell) - **Source:** Manufacturer specifications
- Waste factor: 1.0 for batts (cut to fit), 1.05 for rigid board - **Source:** Construction practice

**Files Modified:**
- `systems/pole_barn/model.py` - Added insulation type fields
- `systems/pole_barn/assemblies.py` - Enhanced `_calculate_insulation_quantities()`
- `config/parts.example.csv` - Added insulation type parts
- `config/pricing.example.csv` - Added insulation pricing
- `config/assemblies.example.csv` - Added insulation type assemblies

**References:**
- ASSEMBLIES_DESIGN.md - Section 6: Insulation
- IRC Section R402 - Energy code requirements

**TODOs:**
- Subtract door/window openings from wall insulation area
- **Source for future:** More accurate area calculations

---

### Change 4: MEP Allowances (Entry [18])

**Date:** Assemblies Deep Dive Implementation  
**Source:** ASSEMBLIES_DESIGN.md (based on IRC and estimator practice)

**What Changed:**
- Added MEP allowance fields to `PricingInputs`
- Implemented MEP allowance line items in pricing

**Assumptions:**
- Electrical: Code minimum outlets (1 per 12 LF of wall) - **Source:** IRC E3801.2
- Plumbing: Basic fixtures if bathroom/kitchen - **Source:** Typical estimator practice
- Mechanical: Basic ventilation/heating - **Source:** Typical estimator practice
- Allowances not marked up - **Source:** Estimator practice (allowances are cost buckets)

**Files Modified:**
- `systems/pole_barn/model.py` - Added MEP fields to `PricingInputs`
- `systems/pole_barn/pricing.py` - Added MEP allowance logic

**References:**
- ASSEMBLIES_DESIGN.md - Section 10: MEP Allowances
- IRC Section E3801.2 - Outlet spacing requirements

**TODOs:**
- Add code-minimum calculations (e.g., outlet count based on wall length)
- **Source for future:** IRC E3801.2 for detailed electrical calculations

---

## Design Decisions

### Decision 1: Standard Door/Window Sizes

**Decision:** Use fixed standard sizes (3' x 7' doors, 3' x 3' windows) for now

**Rationale:**
- Simplifies initial implementation
- Can be made configurable later (Entry [21])
- Standard sizes cover majority of cases

**Source:** Industry standard sizes (documented in ASSEMBLIES_DESIGN.md)

---

### Decision 2: Insulation Waste Factors

**Decision:** 
- Batts: 1.0 (cut to fit, minimal waste)
- Rigid board: 1.05 (cutting waste)

**Rationale:**
- Batts are cut to fit between framing, minimal waste
- Rigid board requires cutting, typical 5% waste

**Source:** Construction practice (documented in ASSEMBLIES_DESIGN.md)

---

### Decision 3: MEP as Allowances Only

**Decision:** Treat MEP as cost allowances, not detailed material takeoffs

**Rationale:**
- Detailed MEP design is beyond estimator scope
- Allowances are standard practice in construction estimating
- Can be enhanced later with code-minimum calculations

**Source:** Estimator practice (documented in ASSEMBLIES_DESIGN.md)

---

### Decision 4: Exterior Finish - 26ga vs 29ga

**Decision:** Use separate assembly names (`roof_panels_26ga` vs `roof_panels`)

**Rationale:**
- Allows assemblies CSV to map to different part IDs
- Keeps pricing logic simple
- Can extend to other finish types later

**Source:** Design decision for clean separation

---

## Future Enhancements (With Sources)

### Enhancement 1: Lap Siding

**Status:** TODO  
**Source Needed:**
- Manufacturer specifications for lap siding coverage
- Typical waste factors for lap siding
- Installation labor rates

**Implementation Notes:**
- Will need separate assembly names
- May require different coverage calculations than metal panels

---

### Enhancement 2: Stucco

**Status:** TODO  
**Source Needed:**
- Stucco system specifications
- Base/sheathing requirements
- Coverage rates and waste factors

**Implementation Notes:**
- May require sheathing as prerequisite
- Different coverage calculations than panels

---

### Enhancement 3: Code-Minimum MEP Calculations

**Status:** TODO  
**Source:**
- IRC E3801.2 - Outlet spacing (1 per 12 LF of wall)
- IRC Section R303 - Ventilation requirements
- Local plumbing code requirements

**Implementation Notes:**
- Can calculate minimum outlet count from wall length
- Can calculate minimum ventilation from building volume
- Still treated as allowances, but calculated from code minimums

---

## Testing References

All test assumptions should reference:
- ASSEMBLIES_DESIGN.md for design decisions
- This changelog for implementation details
- Source citations for all assumptions

---

*Changelog created: Assemblies Deep Dive Implementation*

