# Trim Take-Off Calculator - Project Log

## Completed Tasks

### Phase 1 — Manual LF Mode Improvements (v0.3)

#### Task 1A — Manual Trim Style Dropdown
- Added "Manual Trim Style" dropdown next to Manual LF fields in `trim_calculator.py`
- Populated with existing TRIM_STYLES list (Craftsman, Mitered, Built-Up, Sill/Apron Only)
- Default selection: "Craftsman"
- Dropdown is enabled when manual LF mode is active, disabled otherwise
- Integrated into `toggle_lf_input_mode()` function

#### Task 1B — Use Selected Trim Style for BF Calculations
- Modified `calculate()` function to retrieve `manual_trim_style` from dropdown when `has_lf_takeoffs=True`
- Replaced hardcoded `'craftsman'` argument in `calculate_bf_with_waste()` with selected trim style
- Added fallback to "Craftsman" with warning logging if style is missing or invalid
- Updated `display_results()` to show the trim style applied for BF calculations in manual LF mode

### Phase 2 — Config Validation Layer (v0.3)

#### Task 2A — Create Validation Module
- Created `config_validator.py` module with comprehensive validation functions
- Implemented `validate_config_files()` function that checks:
  - `trim_dimensions.xlsx` schema (STYLE, PART, ECONOMY/STANDARD/UPGRADE columns)
  - `awi_waste_chart.xlsx` schema (RIP SIZE, 4/4, 5/4, 6/4, 8/4 columns)
  - `lumber_species.csv` schema (Species column or first column)
  - `bf_cost.xlsx` schema (Species, 4/4, 5/4, 6/4, 8/4 columns)
  - `Finish Rates.xlsx` (optional, basic validation)
  - `setup_costs.xlsx` (optional, basic validation)
  - `finish_pricing.xlsx` (optional, basic validation)
- Validation rules:
  - All required columns must be present
  - Empty files trigger warnings
  - Missing required files trigger Tkinter error dialogs and block calculations
- Uses human-readable messageboxes (no crashes)

#### Task 2B — Integrate Config Validation
- Added `validate_configuration()` method to `TrimCalculatorApp` class
- Called `validate_config_files()` on app startup in `__init__()`
- Added validation check in `calculate()` method before performing calculations
- Blocks calculations if configuration files are invalid
- Stores validation state in `self.config_valid` attribute

### Phase 3 — Output Polish & Invoice Cleanup (v0.3)

#### Task 3A — Results Panel Formatting
- Ensured LF & BF values are rounded to 2 decimal places in `display_results()`
- Improved display to show trim style applied for BF calculations in manual LF mode
- Enhanced results output with clearer formatting

#### Task 3B — Invoice Formatting Improvements
- Updated `format_description()` function to use new format: "Base – Paint – 5.5" – 128 LF – 42.37 BF – Clear Finish"
- Made descriptions more human-readable with proper capitalization
- Ensured all numbers are right-aligned (already implemented via `number_alignment`)
- Rounded all totals to 2 decimals:
  - Line item totals: `round(p['line_total'], 2)`
  - Subtotal: `round(sum(...), 2)`
  - Tax amount: `round(total_subtotal * sales_tax_rate, 2)`
  - Final total: `round(total_subtotal + tax_amount, 2)`
- Rounded all pricing values in line items to 2 decimals

## Assumptions Made

### Phase 1
- Manual trim style dropdown uses the same style labels as the main results tabs
- When manual LF mode is active, all trim styles in results tabs use the same manual LF values but with different BF calculations based on the selected trim style
- Default trim style for manual mode is "Craftsman" (most common use case)

### Phase 2
- Configuration validation should block calculations if critical files are missing or invalid
- Optional files (Finish Rates.xlsx, setup_costs.xlsx, finish_pricing.xlsx) generate warnings but don't block functionality
- Validation should be performed on startup and before each calculation (as a safety check)

### Phase 3
- Invoice descriptions should include LF and BF values for clarity
- All monetary values should be rounded to 2 decimal places for consistency
- Description format should be human-readable with proper capitalization

## Version History

### v0.3 (Current)
**Date**: 2024-12-19
**Phase**: Manual LF Mode Improvements, Config Validation, Output Polish

**Changes**:
- Added Manual Trim Style dropdown for manual LF input mode
- Integrated selected trim style into BF calculations for manual mode
- Created comprehensive configuration validation system
- Improved results panel formatting and display
- Enhanced invoice descriptions and number formatting
- Added validation checks on startup and before calculations

**Files Modified**:
- `trim_calculator.py` - Added manual trim style dropdown, validation integration, improved results display
- `config_validator.py` - New file for configuration validation
- `invoice_generator.py` - Improved description formatting and number rounding

### v0.2
**Phase**: Finish Pricing Library Integration
- Integrated finish pricing library
- Added finish type selection
- Enhanced pricing calculations

### v0.1
**Phase**: Initial Implementation
- Basic trim calculation functionality
- LF and BF calculations
- Excel invoice generation
- Manual LF input mode

