# Post-Frame Construction Assemblies Design Document

## Overview

This document defines the assemblies, parts, and quantity logic for post-frame (pole barn) construction estimation. It serves as the design reference for implementing realistic material takeoffs in the calculator.

**Scope:** This is an estimator tool, not an engineering tool. We focus on quantities and costs based on typical industry practice, not structural engineering calculations.

---

## Post-Frame Construction Basics

Post-frame construction uses vertical posts (poles) embedded in the ground or on concrete piers as the primary structural system. The frame consists of:

- **Posts** - Primary vertical load-bearing members
- **Girts** - Horizontal wall framing members attached to posts
- **Trusses** - Roof framing members spanning between posts
- **Purlins** - Horizontal roof framing members attached to trusses
- **Panels** - Exterior cladding (metal, wood, etc.)
- **Sheathing** - Optional structural sheathing (OSB, plywood)
- **Insulation** - Optional thermal insulation
- **Openings** - Doors and windows with associated framing and trim

**Sources:**
- Post-Frame Building Design Manual (National Frame Builders Association)
- IRC Section R301 (International Residential Code) - general construction practices
- Industry standard spacing practices (documented in manufacturer literature)

---

## Assembly Categories

### 1. Posts (Columns)

**Parts Involved:**
- Pressure-treated (PT) solid posts (typically 6x6 or 8x8)
- Laminated posts (engineered, typically 6x6 or larger)
- Concrete for post holes/footings

**Spacing/Usage:**
- Typical spacing: 8-12 feet on center along length
- One post per frame line on each sidewall
- Posts extend from ground (or footing) to truss connection point
- Depth in ground: typically 4-6 feet (varies by soil conditions and code)

**Material Takeoff Units:**
- Posts: **EA** (each)
- Post concrete: **CY** (cubic yards) or **EA** (per post hole)

**Standard vs Commercial:**
- Standard: PT solid posts, typically 6x6
- Commercial: May use laminated posts for larger spans or higher loads
- Commercial may have different spacing requirements

**Code References:**
- IRC R301.1 - General construction requirements
- Typical post sizing based on span and load (industry practice, not code-mandated for this estimator)

---

### 2. Girts (Wall Horizontal Framing)

**Parts Involved:**
- 2x6 or 2x8 lumber (SPF, SYP, or similar)
- Fasteners (screws or nails)
- Metal brackets (for commercial/bookshelf style)

**Spacing/Usage:**
- **Standard girts:** Horizontal members attached to outside face of posts
  - Typical spacing: 24" on center vertically
  - Run full length of wall between posts
  - One row per spacing interval from grade to eave height
  
- **Commercial/Bookshelf girts:** Horizontal members with blocking between posts
  - Similar spacing (24" o.c. typical)
  - Additional blocking lumber between posts
  - May use metal brackets for connections

**Material Takeoff Units:**
- Girt lumber: **LF** (linear feet)
- Blocking (commercial): **LF** or **BF** (board feet)
- Fasteners: **EA** (each)

**Standard vs Commercial:**
- Standard: Simple horizontal girts, minimal blocking
- Commercial: Bookshelf style with blocking between posts, may use metal brackets
- Commercial typically requires more lumber and fasteners

**Sources:**
- Typical girt spacing: 24" o.c. per industry practice (NFBA guidelines)
- Commercial bookshelf girts: Additional blocking at 24" o.c. between posts

---

### 3. Purlins (Roof Horizontal Framing)

**Parts Involved:**
- 2x6 or 2x8 lumber
- Fasteners (screws or nails)
- Metal brackets (for some connection types)

**Spacing/Usage:**
- Horizontal members attached to top of trusses
- Typical spacing: 24" on center along roof slope
- Run perpendicular to trusses, spanning building width (with overhangs)
- Number of rows = roof run / spacing (rounded up)

**Material Takeoff Units:**
- Purlin lumber: **LF** (linear feet)
- Fasteners: **EA** (each)

**Standard vs Commercial:**
- Similar spacing typically
- Commercial may use larger lumber sizes for longer spans

**Sources:**
- Typical purlin spacing: 24" o.c. per industry practice
- Roof run calculation: Based on building width, pitch, and overhangs

---

### 4. Roof and Wall Panels (Metal Cladding)

**Parts Involved:**
- Metal panels (29ga or 26ga steel)
- Panel fasteners (screws with washers)
- Ridge cap (for roof)
- Trim pieces (eave, rake, base, corner)

**Spacing/Usage:**
- Panels typically 36" wide coverage (actual panel width ~38" with overlap)
- Standard panel lengths: 8', 10', 12', 14', 16', 20', 24'
- Panels run vertically on walls, horizontally on roof
- Waste factor: 5-10% typical (cutting, end pieces, mistakes)

**Material Takeoff Units:**
- Panels: **SF** (square feet) or **EA** (panel count)
- Fasteners: **EA** (typically 1 fastener per 1-2 sq ft)
- Trim: **LF** (linear feet)

**29ga vs 26ga:**
- 29ga: Thinner, lighter, lower cost (typical residential)
- 26ga: Thicker, heavier, higher cost (commercial, high-wind areas)
- Same coverage area, different material cost

**Sources:**
- Panel coverage: 36" typical per manufacturer specifications
- Waste factor: 5-10% typical per industry practice
- Fastener spacing: 1 per 1-2 sq ft per manufacturer recommendations

---

### 5. Wall & Roof Sheathing (OSB/Plywood)

**Parts Involved:**
- OSB (Oriented Strand Board) sheets
- Plywood sheets
- Fasteners (nails or screws)
- Vapor barrier (if required)

**Spacing/Usage:**
- Standard sheet size: 4' x 8' = 32 sq ft
- Applied to wall or roof before exterior finish
- Typical thickness: 7/16" or 1/2" for walls, 5/8" or 3/4" for roof
- Waste factor: 10-15% typical (cutting, end pieces)

**Material Takeoff Units:**
- Sheathing: **SF** (square feet) or **EA** (sheet count)
- Fasteners: **EA** (typically 1 fastener per 6-8 inches along edges)

**OSB vs Plywood:**
- OSB: Lower cost, typical for non-structural sheathing
- Plywood: Higher cost, may be required for structural sheathing
- Same coverage area, different material cost

**Sources:**
- Standard sheet size: 4' x 8' per industry standard
- Waste factor: 10-15% typical per construction practice
- Thickness varies by application (manufacturer specifications)

---

### 6. Insulation (Walls vs Roof)

**Parts Involved:**
- Fiberglass batts (R-19, R-30, etc.)
- Rock wool batts
- Rigid board insulation (polyiso, XPS, EPS)
- Spray foam (closed-cell or open-cell)
- Vapor barrier (for some types)

**Spacing/Usage:**
- **Walls:** Applied between girts or in wall cavity
  - Batt insulation: Sized to fit between framing (typically 24" o.c. spacing)
  - Rigid board: Applied to exterior or interior face
  - Spray foam: Applied in cavity or as continuous layer
  
- **Roof:** Applied between purlins or as continuous layer
  - Similar types and applications as walls
  - May require different R-values

**Material Takeoff Units:**
- Insulation: **SF** (square feet) - based on wall or roof area
- Vapor barrier: **SF** (if separate)

**Types:**
- **Fiberglass batts:** Typical R-19 for walls, R-30+ for roof
- **Rock wool:** Similar R-values, higher cost, better fire resistance
- **Rigid board:** R-5 to R-7 per inch, applied as continuous layer
- **Spray foam:** R-6 to R-7 per inch (closed-cell), applied in place

**Sources:**
- R-value requirements: IRC Section R402 (Energy Code) - varies by climate zone
- Typical R-values: R-19 walls, R-30+ roof per industry practice
- Coverage: Based on wall/roof area with minimal waste (batts cut to fit)

---

### 7. Doors and Windows (Openings)

**Parts Involved:**
- Extra framing lumber (king studs, trimmers/jacks, headers, sill plates)
- Exterior trim (jambs, head, sill)
- Fasteners

**Spacing/Usage:**
- **Door framing:**
  - King studs: 2 per door (one each side)
  - Trimmers/jacks: 2 per door (support header)
  - Header: 1 per door (typically 2x8 or 2x10, length = door width + 6")
  - Sill plate: 1 per door (if not slab-on-grade)
  
- **Window framing:**
  - Similar to doors but typically smaller headers
  - Sill plate: 1 per window
  - Header: Typically 2x6 or 2x8

- **Trim:**
  - Door trim: Head + 2 jambs = ~(door width + 2 × door height)
  - Window trim: Head + sill + 2 jambs = ~(window width + 2 × window height + window width)

**Material Takeoff Units:**
- Framing lumber: **BF** (board feet) or **LF** (linear feet)
- Trim: **LF** (linear feet)

**Assumptions (for estimator):**
- Standard door: 3' x 7' (36" x 84")
- Standard window: 3' x 3' (36" x 36")
- Header size: 2x8 for doors, 2x6 for windows
- These can be made configurable later

**Sources:**
- Typical door sizes: 3' x 7' standard per industry practice
- Header sizing: Based on span and load (simplified for estimator)
- Trim coverage: Based on perimeter of opening

---

### 8. Overhead/Roll-Up Doors

**Parts Involved:**
- Door unit (steel roll-up or sectional)
- Track and hardware
- Operator (if motorized)
- Framing reinforcement (if required)

**Spacing/Usage:**
- Typically 8' to 16' wide, 7' to 14' high
- One door per opening
- May require additional framing around opening

**Material Takeoff Units:**
- Door unit: **EA** (each) - typically priced as complete unit
- Additional framing: **BF** or **LF** (if required)

**Types:**
- **Steel roll-up:** Lower cost, typical for storage/agricultural
- **Sectional:** Higher cost, typical for residential/commercial
- Motorized operator: Additional cost

**Sources:**
- Typical sizes: 8' x 7' to 16' x 14' per manufacturer catalogs
- Pricing: Typically as complete unit (door + track + hardware)

---

### 9. Floor (Slab vs Gravel vs None)

**Parts Involved:**
- **Slab:**
  - Concrete (typically 4" to 6" thick)
  - Reinforcement (wire mesh or rebar)
  - Vapor barrier
  - Edge forms
  
- **Gravel:**
  - Base gravel (typically 4" to 6" thick)
  - Compaction

- **None:**
  - Native soil (may require grading)

**Spacing/Usage:**
- Slab: Full building footprint area
- Gravel: Full building footprint area
- Thickness: 4" typical for residential, 6" for commercial/heavy use

**Material Takeoff Units:**
- Concrete: **CY** (cubic yards) = (area × thickness) / 27
- Reinforcement: **SF** (wire mesh) or **LB** (rebar)
- Gravel: **CY** (cubic yards)

**Sources:**
- Typical slab thickness: 4" residential, 6" commercial per IRC
- Concrete volume: Area × thickness / 27 (conversion to cubic yards)
- Reinforcement: Wire mesh typical for 4" slab, rebar for 6"+

---

### 10. MEP (Mechanical, Electrical, Plumbing) - Allowances Only

**Parts Involved:**
- Electrical: Basic lighting, outlets, service panel
- Plumbing: Basic fixtures, water/sewer connections
- Mechanical: Basic heating/ventilation

**Spacing/Usage:**
- **Electrical (code minimum):**
  - Outlets: 1 per 12 linear feet of wall (IRC E3801.2)
  - Lighting: Minimum 1 per room/area
  - Service: 100A typical for small buildings
  
- **Plumbing:**
  - Basic fixtures if bathroom/kitchen included
  - Water/sewer connections
  
- **Mechanical:**
  - Basic ventilation (may be code-required)
  - Heating (if enclosed/conditioned)

**Material Takeoff Units:**
- **Allowance-based only** (not detailed takeoff)
- Units: **$** (dollar allowance per category)

**Note:** This estimator treats MEP as cost allowances, not detailed material takeoffs. Detailed MEP design is beyond the scope of this tool.

**Sources:**
- IRC E3801.2 - Outlet spacing requirements
- Typical allowances: Based on building size and use (industry practice)

---

## Mapping to Existing Code Structure

### `systems/pole_barn/assemblies.py`

**Current Structure:**
- `calculate_material_quantities()` - Main function
- Helper functions: `_calculate_post_count()`, `_calculate_truss_count()`, `_calculate_girt_quantities()`, etc.

**Additions Needed:**
- `_calculate_door_framing()` - Extra lumber for doors
- `_calculate_window_framing()` - Extra lumber for windows
- `_calculate_door_trim()` - Trim LF for doors
- `_calculate_window_trim()` - Trim LF for windows
- `_calculate_wall_insulation()` - Wall insulation SF
- `_calculate_roof_insulation()` - Roof insulation SF
- `_calculate_slab_concrete()` - Concrete CY for slab
- Branching logic for exterior finish type (29ga vs 26ga)

### `config/assemblies.example.csv`

**Current Columns:**
- `assembly_name`, `part_id`, `waste_factor`, `labor_per_unit`, `notes`

**Additions Needed:**
- Door/window framing assemblies
- Door/window trim assemblies
- Wall/roof insulation assemblies (by type)
- Slab concrete assembly
- Exterior finish variants (29ga vs 26ga)

### `config/parts.example.csv`

**Current Parts:**
- Basic framing, panels, trim, fasteners, concrete, insulation

**Additions Needed:**
- 26ga metal panels (separate from 29ga)
- OSB sheathing
- Plywood sheathing
- Door/window framing lumber (or use existing 2x6)
- Door/window trim (or use existing trim parts)
- Different insulation types (fiberglass, rock wool, rigid, spray foam)
- Overhead door units

### `config/pricing.example.csv`

**Additions Needed:**
- Unit prices for all new parts
- Pricing for overhead doors (as complete units)

---

## Implementation Notes

### Assumptions Documented in Code

1. **Door/Window Sizes (for framing calculations):**
   - Standard door: 3' x 7' (36" x 84")
   - Standard window: 3' x 3' (36" x 36")
   - These are assumptions for quantity estimation; actual sizes can vary

2. **Girt/Purlin Spacing:**
   - Default: 24" on center
   - Can be overridden by user input

3. **Waste Factors:**
   - Panels: 5-10% (use 5% = 1.05)
   - Trim: 10% (use 1.10)
   - Sheathing: 10-15% (use 10% = 1.10)
   - Lumber: 5-10% (use 5% = 1.05)

4. **Insulation Coverage:**
   - Based on wall/roof area
   - Minimal waste for batts (cut to fit)
   - Waste factor: 1.0 for batts, 1.05 for rigid board

5. **Concrete Slab:**
   - Default thickness: 4" (residential)
   - Can be overridden by user input
   - Volume = area × thickness / 27 (cubic yards)

---

## References and Sources

1. **Post-Frame Construction:**
   - National Frame Builders Association (NFBA) - General construction practices
   - Industry standard spacing and sizing practices

2. **Building Codes:**
   - IRC (International Residential Code) - General construction requirements
   - IRC Section R301 - General requirements
   - IRC Section R402 - Energy code (insulation R-values)
   - IRC Section E3801.2 - Electrical outlet spacing

3. **Material Specifications:**
   - Manufacturer literature (metal panels, insulation, etc.)
   - Industry standard sheet sizes (OSB, plywood: 4' x 8')

4. **Construction Practices:**
   - Typical spacing: 24" o.c. for girts/purlins (industry practice)
   - Typical waste factors: 5-15% depending on material (construction practice)
   - Typical door/window sizes: Industry standard sizes

**Note:** This document summarizes industry practices and typical construction methods. It does not reproduce copyrighted code text but paraphrases common practices that are widely known in the construction industry.

---

*Document created: Assemblies Deep Dive - Research Phase*

