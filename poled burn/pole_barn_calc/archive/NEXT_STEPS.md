# Next Steps for Pole Barn Calculator

## Project Status Summary

✅ **Completed (First Pass)**
- Project structure created with all required directories
- Data models defined using dataclasses (GeometryInputs, MaterialInputs, PricingInputs, AssemblyInputs, PoleBarnInputs)
- CLI interface implemented with all input variables
- Control document created listing all variables
- Example CSV configuration files created
- Test stub files created
- README.md with project documentation

✅ **Completed (Phase 1 - Geometry)**
- `GeometryModel` dataclass created to hold derived geometry values
- All geometry calculation functions implemented:
  - `build_geometry_model()` - Main function that creates GeometryModel
  - `calculate_roof_area()` - Roof surface area with pitch and overhangs
  - `calculate_wall_area()` - Wall areas for all four sides
  - `calculate_floor_area()` - Footprint area
  - `calculate_door_window_openings()` - Opening areas
  - `calculate_roof_volume()` - Building volume
  - `get_geometry_summary()` - Complete geometry summary
- Comprehensive test suite with real numeric assertions
- CLI enhanced to display geometry results
- Pole count calculation intentionally deferred to assemblies.py

✅ **Completed (Phase 2 - Material Quantities)**
- `AssemblyQuantity` and `MaterialTakeoff` dataclasses created
- Main `calculate_material_quantities()` function implemented
- All material quantity calculations implemented:
  - Posts (count) - Based on frame lines
  - Trusses (count) - Based on truss spacing or frame lines
  - Girts (LF) - Sidewall and endwall girts based on girt spacing
  - Purlins (LF) - Roof purlins based on purlin spacing
  - Roof panels (SF) - Based on roof area from geometry
  - Wall panels (SF) - Sidewall and endwall panels
  - Trim (LF) - Eave, rake, base, and corner trim
  - Insulation (SF) - If specified
  - Ventilation (count) - If specified
- Legacy function signatures maintained for backward compatibility
- Comprehensive test suite with real numeric assertions
- CLI enhanced to display material quantities by category
- Fastener and concrete calculations intentionally deferred (require detailed specifications)

✅ **Completed (Phase 5 - Parts & Pricing Library)**
- Comprehensive parts catalog populated in `parts.example.csv`:
  - Framing: Posts, trusses, lumber (2x6)
  - Skin: Metal panels (29ga)
  - Trim: Eave, rake, base, corner, ridge cap
  - Fasteners: Metal screws
  - Concrete: Bag-equivalent pricing
  - Insulation: R-19 fiberglass batts
  - Ventilation: Ridge vent, gable vents
  - Soft costs: Delivery, permit, site prep
- Pricing data populated in `pricing.example.csv`:
  - Real pricing from Home Depot/Lowe's where available
  - Assumed pricing for trim and soft costs
  - All parts have unit prices
- Assembly mappings populated in `assemblies.example.csv`:
  - All current assembly names mapped to parts
  - Waste factors set (1.0-1.10 range, typically 1.05 for panels)
  - Labor per unit set (hours per unit of quantity)
  - Ready for fasteners and concrete when Phase 4 is implemented
- CSV schema updated to support:
  - Direct `part_id`, `waste_factor`, `labor_per_unit` columns
  - Backward compatible with old pipe-separated format
- Pricing logic verified to use waste factors and labor per unit
- Tests updated to verify waste factors and labor calculations
- Calculator ready for real-world testing with populated data

✅ **Completed (Phase 3 - Pricing & Costs)**
- `PricedLineItem` and `PricingSummary` dataclasses created
- CSV loaders implemented for parts, pricing, and assemblies configs
- Assembly mapping system to map quantities to parts
- `price_material_takeoff()` function implemented with:
  - Material cost calculation (quantity × unit_price)
  - Labor cost calculation (quantity × labor_per_unit × labor_rate)
  - Markup calculation (material + labor × markup_percent)
  - Tax calculation (material + markup × tax_rate)
  - Grand total with optional delivery, permit, site prep costs
- `PoleBarnCalculator` fully implemented with:
  - Config loading from CSV files
  - Complete calculation pipeline (geometry → quantities → pricing)
  - Summary generation
- CLI enhanced to display cost breakdown and totals
- Comprehensive test suite for pricing logic
- End-to-end tests for full calculator pipeline

## Recommended Next Steps

### Phase 1: Geometry Calculations ✅ COMPLETE
**Status**: Implemented and tested

**What was implemented:**
- `GeometryModel` dataclass with derived geometry values:
  - Core dimensions (length, width, heights, overhangs)
  - Bays and frame lines (calculated from bay spacing)
  - Areas (footprint, walls, roof)
  - Building volume
- All geometry functions now return real calculated values
- Tests validate calculations with known inputs/outputs
- CLI displays geometry results

**Assumptions made:**
- Bays calculated using `ceil(length / bay_spacing)` where bay_spacing = `pole_spacing_length`
- Roof area uses slope factor: `sqrt(1 + pitch^2)` applied to plan area with overhangs
- Wall areas calculated without subtracting openings (openings tracked separately)
- Building volume uses simple box approximation (footprint × eave_height)
- Pole counting deferred to assemblies.py (requires structural analysis)

### Phase 2: Material Quantity Calculations ✅ COMPLETE
**Status**: Implemented and tested

**What was implemented:**
- `AssemblyQuantity` dataclass for individual material items
- `MaterialTakeoff` dataclass as container for all quantities
- `calculate_material_quantities()` main function that orchestrates all calculations
- Individual quantity calculations:
  - **Posts**: `num_frame_lines × 2` (one per frame line on each sidewall)
  - **Trusses**: Based on truss spacing or frame lines (one per frame line if spacing matches bay spacing)
  - **Girts**: Calculated from eave height and girt spacing for sidewalls and endwalls
  - **Purlins**: Calculated from roof dimensions and purlin spacing for both roof slopes
  - **Roof panels**: Uses roof area from geometry (SF)
  - **Wall panels**: Uses wall areas from geometry for sidewalls and endwalls (SF)
  - **Trim**: Eave, rake, base, and corner trim (LF)
  - **Insulation**: Wall + roof area if insulation type specified (SF)
  - **Ventilation**: Count from assembly inputs if specified
- Legacy function signatures maintained (`calculate_truss_quantity()`, etc.)
- Tests validate all quantity calculations
- CLI displays quantities organized by category

**Assumptions made:**
- Posts: One post per frame line on each sidewall (simplified - actual layouts may vary)
- Trusses: One per frame line if truss spacing matches bay spacing, otherwise calculated from truss spacing
- Girts: Number of rows = `ceil(eave_height / girt_spacing)`, applied to both sidewalls and endwalls
- Purlins: Approximated using roof width/2 for each slope, multiplied by effective length
- Panels: Direct use of geometry areas (no waste factors yet - Phase 3)
- Trim: Simple perimeter and corner calculations
- Wall panels: Gross area (openings tracked separately, not subtracted yet)

**Deferred to future phases:**
- Fastener calculations (require detailed fastening patterns)
- Concrete quantity calculations (require foundation design details)
- Waste factors for materials (will be added in Phase 3 with pricing)
- Panel count estimates (requires panel size specifications)

### Phase 3: Pricing Calculations ✅ COMPLETE
**Status**: Implemented and tested

**What was implemented:**
- **Pricing dataclasses:**
  - `PricedLineItem` - Fully priced line item with material, labor, markup costs
  - `PricingSummary` - Rollup totals for all costs
  
- **CSV configuration system:**
  - `load_parts()` - Loads parts catalog from CSV
  - `load_pricing()` - Loads pricing data from CSV
  - `load_assemblies()` - Loads assembly mappings from CSV
  - Default paths point to `config/` directory
  
- **Assembly mapping:**
  - `find_assembly_mapping()` - Maps assembly names to part IDs
  - Supports pipe-separated parts and quantity multipliers
  - Fallback simple mapping for common assemblies
  - Waste factor support (defaults to 1.0 if not specified)
  
- **Pricing logic:**
  - `price_material_takeoff()` - Main pricing function
  - Material cost = effective_quantity × unit_price
  - Labor cost = effective_quantity × labor_per_unit × labor_rate
  - Markup = (material + labor) × markup_percent
  - Tax = (material + markup) × tax_rate
  - Grand total includes delivery, permit, site prep costs
  
- **Calculator integration:**
  - `PoleBarnCalculator.calculate()` - Full pipeline
  - `PoleBarnCalculator.load_config()` - Loads CSV configs
  - `PoleBarnCalculator.get_summary()` - Human-readable summary
  
- **CLI enhancements:**
  - Displays cost breakdown by category
  - Shows major line items with quantities and prices
  - Displays cost summary (material, labor, markup, tax, grand total)
  - JSON output includes all priced items and summary

**Assumptions made:**
- **Part mapping:** Uses simple fallback mapping when assemblies CSV doesn't have a match
- **Waste factors:** Defaults to 1.0 (no waste) if not specified in assemblies CSV
- **Labor:** Defaults to 0.0 hours per unit (assemblies CSV doesn't include labor_per_unit yet)
- **Markup:** Applied to material + labor costs
- **Tax:** Applied to material + markup (typical construction practice)
- **Unit prices:** Uses first match in pricing CSV (no date-based selection yet)
- **Missing parts:** Creates priced items with $0 cost and notes about missing mapping

**Configuration files used:**
- `config/parts.example.csv` - Part catalog (part_id, part_name, category, unit, description)
- `config/pricing.example.csv` - Pricing data (part_id, unit_price, unit, notes)
- `config/assemblies.example.csv` - Assembly mappings (assembly_name, parts, quantity_multiplier)

**Known limitations:**
- No waste factors in assemblies CSV yet (defaults to 1.0)
- No labor_per_unit in assemblies CSV yet (defaults to 0.0)
- Simple part mapping (uses first part if multiple parts in assembly)
- No date-based pricing selection (uses first match)
- Trim items don't have part mappings in example CSVs

1. **Implement `pricing.py` functions:**
   - `calculate_material_costs()` - Multiply quantities by unit prices from pricing.example.csv
   - `calculate_labor_costs()` - Estimate labor hours based on assembly complexity
   - `calculate_subtotal()` - Sum material and labor costs
   - `calculate_taxes()` - Apply tax rate to subtotal
   - `calculate_total_cost()` - Include all costs (materials, labor, taxes, delivery, permits, site prep)
   - `get_cost_breakdown()` - Detailed breakdown by category

2. **Labor estimation:**
   - Create labor hour estimates based on:
     - Square footage
     - Assembly method complexity
     - Material types (some materials install faster)
     - Foundation type
   - Consider creating a labor estimation table or formula

3. **Markup application:**
   - Apply material_markup to material costs
   - Consider if markup applies to all materials or just certain categories

### Phase 4: Calculator Integration (Priority: Medium)
**Goal**: Wire everything together in the main calculator class.

1. **Implement `calculator.py` methods:**
   - `calculate_geometry()` - Call all geometry functions
   - `calculate_quantities()` - Call all assembly/quantity functions
   - `calculate_costs()` - Call all pricing functions
   - `calculate_all()` - Run complete calculation pipeline
   - `get_summary()` - Format results for human-readable output

2. **Error handling:**
   - Add try/except blocks for calculation errors
   - Provide meaningful error messages
   - Validate inputs before calculations

3. **Result formatting:**
   - Create formatted output for CLI
   - Support JSON output for programmatic use
   - Create detailed breakdown reports

### Phase 5: Configuration System (Priority: Low)
**Goal**: Make configuration files functional and extensible.

1. **CSV loading:**
   - Create functions to load and parse CSV files
   - Validate CSV structure
   - Handle missing or malformed data

2. **Configuration management:**
   - Allow users to specify custom config files
   - Support environment-specific pricing
   - Allow override of default values

### Phase 6: CLI Enhancements (Priority: Low)
**Goal**: Improve user experience.

1. **Input validation:**
   - Validate all inputs before creating calculator
   - Provide helpful error messages
   - Suggest corrections for common mistakes

2. **Output formats:**
   - Enhanced summary format
   - Detailed report format
   - Export to CSV/Excel
   - Export to PDF (optional)

3. **Interactive mode:**
   - Prompt for inputs if not provided
   - Save/load project configurations
   - Support configuration presets

### Phase 7: Testing and Documentation (Priority: Medium)
**Goal**: Ensure reliability and usability.

1. **Comprehensive testing:**
   - Unit tests for all calculation functions
   - Integration tests for full workflows
   - Edge case testing
   - Performance testing for large projects

2. **Documentation:**
   - API documentation
   - User guide
   - Calculation methodology documentation
   - Examples and use cases

3. **Code quality:**
   - Type hints throughout
   - Docstrings for all functions
   - Code review and refactoring

## Technical Considerations

### Calculation Accuracy
- **Waste factors**: Industry standard waste factors should be researched and applied
- **Material sizing**: Account for standard material sizes (e.g., 4x8 sheets, standard lumber lengths)
- **Rounding**: Decide on rounding rules (round up for materials, round to 2 decimals for costs)

### Structural Engineering
- **Note**: This calculator does NOT perform structural engineering calculations
- Consider adding warnings about:
  - Local building codes
  - Wind/snow load requirements
  - Professional engineering review for large structures
  - Permits and inspections

### Data Sources
- Research current material prices (they vary by region)
- Consider integrating with pricing APIs (future enhancement)
- Allow for regional pricing variations

### Extensibility
- Design for easy addition of new material types
- Support custom assemblies
- Allow plugin-style extensions for specialized calculations

## Quick Start for Next Developer

1. **Start with geometry.py:**
   ```python
   # Example: calculate_roof_area()
   # Roof area = (length + overhangs) × (width + overhangs) × pitch_factor
   # pitch_factor accounts for the slope (use Pythagorean theorem)
   ```

2. **Test as you go:**
   - Run `pytest tests/test_geometry.py` after each function
   - Use known examples (e.g., 40x30 barn with 4:12 pitch)

3. **Reference the control document:**
   - `control/pole_barn_calculator.md` has all variable definitions
   - Use it to understand relationships between variables

4. **Follow the pattern:**
   - Functions return dictionaries with structured data
   - Include units in return values
   - Add docstrings explaining calculations

## Questions to Resolve

1. **Waste factors**: What are industry-standard waste percentages?
2. **Labor estimation**: How to estimate labor hours accurately?
3. **Material sizes**: What are standard sizes for common materials?
4. **Regional variations**: How to handle different building codes/requirements?
5. **Validation rules**: What are acceptable ranges for inputs?

---

*This document should be updated as the project progresses.*

