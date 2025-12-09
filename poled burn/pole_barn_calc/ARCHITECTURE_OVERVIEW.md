# Architecture Overview - Pole Barn Calculator

**Purpose:** High-level system architecture, data flow, and design decisions for the pole barn estimator.

**Last Updated:** After J-Channel Implementation

---

## 🏗️ System Architecture

### High-Level Pipeline

```
User Inputs → Geometry → Assemblies → BOM → Pricing → Export
```

**Flow:**
1. **Inputs** (`PoleBarnInputs`) - User enters dimensions, materials, pricing preferences
2. **Geometry** (`GeometryModel`) - Calculates derived dimensions, areas, volumes, bay counts
3. **Assemblies** (`MaterialTakeoff`) - Calculates material quantities in engineering units (ea, LF, SF)
4. **BOM** (`List[PartQuantity]`) - Expands assemblies into specific parts with piece counts and lengths
5. **Pricing** (`PricedLineItem[]`, `PricingSummary`) - Applies unit prices, labor, markup, tax
6. **Export** - Excel BOM with category tabs, JSON project state

---

## 📊 Data Models

### Input Models (`systems/pole_barn/model.py`)

**GeometryInputs:**
- Core dimensions (length, width, eave_height, roof_pitch)
- Overhangs (front, rear, sides)
- Door/window counts and sizes
- Pole spacing and dimensions
- Roof style (gable/shed) and ridge position

**MaterialInputs:**
- Exterior finish type (metal_29ga, metal_26ga, lap_siding, stucco)
- Insulation types (wall and roof: fiberglass, rock wool, rigid, spray foam)
- Sheathing types (wall and roof: OSB, plywood, none)
- Floor type (slab, gravel, none) with slab details
- Girt type (standard, commercial)
- Spacing values (girt, purlin, truss)

**PricingInputs:**
- Granular markups (material, labor, subcontractor, overhead)
- Tax rate
- Pricing profile

**AssemblyInputs:**
- Post type (PT solid, laminated)
- Truss/post connection type (notched, cleated)
- Ventilation preferences

### Output Models

**GeometryModel:**
- Derived dimensions (overall_length_ft, overall_width_ft, eave_height_ft, peak_height_ft)
- Bay and frame counts (num_bays, num_frame_lines)
- Areas (footprint, sidewall, endwall, roof)
- Volume (building_volume_cuft)

**AssemblyQuantity:**
- Assembly-level quantities (e.g., "posts", "sidewall_girts", "roof_panels")
- Quantity in engineering units (ea, lf, sqft)
- Category and description

**PartQuantity:**
- Specific part with part_id
- Quantity in purchasable units (ea, lf, cuyd, etc.)
- Length tracking (`length_in`) for length-based items
- Unit price and extended price
- Export category for Excel grouping

**PricingSummary:**
- Material subtotal
- Labor subtotal
- Markup totals (material, labor, subcontractor)
- Overhead
- Tax
- Grand total

---

## 🔧 Core Systems

### Geometry System (`systems/pole_barn/geometry.py`)

**Purpose:** Calculate all derived geometric values from inputs.

**Key Functions:**
- `build_geometry_model()` - Main function, creates complete GeometryModel
- `_calculate_roof_slope_factor()` - Converts roof pitch ratio to slope factor
- `calculate_roof_area()` - Roof surface area accounting for pitch and overhangs
- `calculate_wall_area()` - Total wall area (sidewalls + endwalls)
- `calculate_door_window_openings()` - Opening areas for doors and windows

**Assumptions:**
- Gable roofs: symmetric, ridge at center (unless ridge_position specified)
- Overhangs: included in roof area calculations
- Peak height: derived from eave height, width, and roof pitch

---

### Assemblies System (`systems/pole_barn/assemblies.py`)

**Purpose:** Calculate material quantities in engineering units.

**Key Functions:**
- `calculate_material_quantities()` - Main orchestrator
- `_calculate_post_count()` - Posts based on frame lines
- `_calculate_truss_count()` - Trusses based on spacing
- `_calculate_girt_quantities()` - Wall girts (sidewall and endwall)
- `_calculate_purlin_quantities()` - Roof purlins
- `_calculate_trim_quantities()` - Basic trim (eave, rake, base, corner)
- `_calculate_door_window_assemblies()` - Extra framing and trim for openings
- `_calculate_insulation_quantities()` - Wall and roof insulation
- `_calculate_sheathing_quantities()` - Wall and roof sheathing
- `_calculate_concrete_slab_quantities()` - Slab concrete and reinforcement
- `_calculate_overhead_door_quantities()` - Overhead doors
- `_calculate_j_channel_quantities()` - J-channel trim for openings and eave tops

**Output:**
- List of `AssemblyQuantity` items
- Each item has: name, description, category, quantity, unit

---

### BOM System (`systems/pole_barn/bom.py`)

**Purpose:** Expand assembly quantities into specific parts with piece counts and lengths.

**Key Functions:**
- `expand_to_parts()` - Main BOM expansion function
- `generate_gable_panel_lengths()` - Calculates stepped panel lengths for gable endwalls
- `split_lumber_into_stock_lengths()` - Packs LF into stock lengths (8, 10, 12, 14, 16 ft)
- `pack_segments_into_sticks()` - Packs J-channel segments into 10' sticks
- `calculate_eave_top_j_segments()` - J-channel for eave tops
- `calculate_opening_j_segments()` - J-channel for doors and windows

**BOM Rules:**

1. **Panel Length Breakdown:**
   - Gable endwall panels: Multiple stepped lengths based on roof pitch and eave height
   - Sidewall/roof panels: Constant length based on wall height or roof slope
   - Units: "ea" (each panel), not "sqft"
   - Pricing: Converted from per-sqft to per-panel using actual panel dimensions

2. **Lumber Stock Length Packing:**
   - All lumber (2x4, 2x6, etc.) packed into stock lengths
   - Greedy algorithm: Use longest length first, then shorter
   - Stock lengths: 16', 14', 12', 10', 8'
   - Units: "ea" with `length_in` specified

3. **Sheathing Sheet Counts:**
   - 4×8 sheets (48" × 96")
   - Calculated from area using sheet coverage
   - Units: "ea" (sheets), `length_in = 96`

4. **J-Channel Packing:**
   - Segments calculated for doors, windows, eave tops
   - Packed into 10' (120") sticks
   - No splicing within a single piece
   - Offcuts reused for smaller segments
   - Units: "ea" (sticks), `length_in = 120`

5. **Concrete:**
   - Cubic yards calculated from footprint and thickness
   - Reinforcement (mesh or rebar) calculated separately
   - Units: "cuyd" for concrete, "ea" for mesh sheets, "lf" for rebar

**Output:**
- List of `PartQuantity` items
- Each item has: part_id, part_name, category, unit, qty, length_in (if applicable), unit_price, ext_price

---

### Pricing System (`systems/pole_barn/pricing.py`)

**Purpose:** Apply unit prices, labor, markup, and tax to material takeoff.

**Key Functions:**
- `load_parts()` - Load parts catalog from CSV
- `load_pricing()` - Load pricing data from CSV
- `load_assemblies()` - Load assembly mappings from CSV
- `price_material_takeoff()` - Main pricing function

**Pricing Logic:**
1. For each `AssemblyQuantity`:
   - Find part mapping in assemblies CSV
   - Apply quantity multiplier and waste factor
   - Look up unit price from pricing CSV
   - Calculate material cost = effective_qty × unit_price
   - Calculate labor hours = effective_qty × labor_per_unit
   - Calculate labor cost = labor_hours × labor_rate
   - Apply markup (material markup to material, labor markup to labor)
2. Sum all items:
   - Material subtotal
   - Labor subtotal
   - Markup totals (material, labor, subcontractor)
   - Apply overhead percentage to (material + labor)
   - Calculate tax on (material + markup)
   - Grand total = material + labor + markups + overhead + tax

**Markup Rules:**
- Material markup: Applied only to material costs
- Labor markup: Applied only to labor costs
- Subcontractor markup: Applied to subcontractor costs (if implemented)
- Overhead: Applied to (material + labor) before profit
- Tax: Applied to (material + markup)

---

### Export System

**Excel Export (`systems/pole_barn/export_excel.py`):**
- Multi-tab workbook (one tab per export_category)
- Tabs: Framing, Metal, Doors_Windows, Insulation, Concrete, MEP, Misc
- Columns: Part ID, Part Name, Description, Length (in), Unit, Qty, Unit Price, Ext Price, Notes
- Summary sheet with category totals

**JSON Export (`systems/pole_barn/export_json.py`):**
- Full project state serialization
- Includes: inputs, geometry, takeoff, BOM, pricing summary
- Useful for integrations, debugging, project versioning

---

## 🖥️ User Interfaces

### CLI (`apps/cli.py`)
- Command-line interface using Click
- Accepts all input parameters as CLI arguments
- Supports `--export-bom-excel` and `--export-json` flags
- Outputs geometry summary, material quantities, and pricing summary

### GUI (`apps/gui.py`)
- Tkinter-based desktop application
- Organized input sections (Geometry, Materials, Pricing, etc.)
- Results pane with cost breakdown
- Export buttons for Excel and JSON
- File dialogs for save locations

---

## 📁 Configuration System

### CSV Configuration Files (`config/`)

**parts.example.csv:**
- Parts catalog with: part_id, part_name, description, category, unit
- Coverage dimensions: coverage_width_in, coverage_height_in
- Waste factors and export categories
- Source: Home Depot/Lowe's pricing or assumed values

**pricing.example.csv:**
- Unit prices by part_id and pricing_profile
- Can have multiple pricing profiles (e.g., "Default", "Premium")

**assemblies.example.csv:**
- Maps assembly names to part_ids
- Quantity multipliers
- Waste factors
- Labor per unit (hours)

**Path Resolution:**
- Script mode: `config/` relative to project root
- Bundled exe: `config/` next to executable
- Falls back to `.csv` if `.example.csv` not found

---

## 🔄 Calculation Pipeline

### Main Calculator (`systems/pole_barn/calculator.py`)

**PoleBarnCalculator.calculate():**
1. Build geometry model from inputs
2. Calculate material quantities (assemblies)
3. Price the takeoff
4. Expand to BOM (parts with lengths)
5. Return: (geometry, takeoff, priced_items, summary, bom_items)

**Error Handling:**
- Validates config files exist
- Handles missing parts gracefully (unit_price = 0.0, notes warning)
- Validates input ranges where applicable

---

## 🚧 Current Limitations

### Not Yet Implemented:
- **Other Trim Pieces:** Rake, eave, ridge, base, corner trim still in LF (not packed like J-channel)
- **Fastener Quantities:** Not calculated per SF/LF
- **MEP Auto-Calculation:** Toggles exist but no formula-based allowances
- **Interior Framing:** Office, bathroom, mezzanine modules
- **Multiple Door/Window Sizes:** Currently assumes all same size
- **Lap Siding/Stucco:** Exterior finish types not fully implemented
- **Ridge Offset:** Input exists but not fully used in panel calculations
- **Shed Roof Logic:** May need separate calculation path

### Known Gaps:
- Regional pricing adjustments
- Volume discounts
- Subcontractor line items
- Vendor API integrations

---

## 🗺️ Roadmap

See `NEXT_STEPS_AND_GAPS.md` for detailed roadmap. High-level priorities:

1. **Validate BOM Accuracy** (Current Phase)
   - Review test building BOMs
   - Fix any quantity discrepancies

2. **Complete Trim System**
   - Implement packing for rake, eave, ridge, base, corner trim
   - Similar to J-channel logic

3. **MEP Auto-Calculation**
   - Formula-based electrical, plumbing, mechanical allowances
   - Based on building size, door count, code minimums

4. **Interior Framing Modules**
   - Office, bathroom, mezzanine assemblies
   - Full framing, drywall, insulation

5. **Pricing Override UI**
   - Per-project price adjustments
   - Without editing CSVs

6. **Vendor Integrations** (Future)
   - API feeds for pricing
   - Direct BOM submission

---

## 📚 Related Documentation

- `DEVELOPMENT_LOG.md` - Complete development history
- `NEXT_STEPS_AND_GAPS.md` - Detailed roadmap and gaps
- `PROJECT_EXPORT_FULL.md` - Full codebase snapshot
- `/archive/` - Historical design documents

---

**This architecture supports a production-ready pole barn estimator with accurate material takeoff, realistic BOM generation, and flexible pricing.**

