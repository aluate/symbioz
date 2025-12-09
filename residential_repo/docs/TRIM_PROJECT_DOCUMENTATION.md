# Trim Take-Off Calculator - Project Documentation

## 1. PROJECT SUMMARY

### Project Name
Trim Take-Off Calculator

### Purpose
Desktop application that automates trim material estimation for construction projects. Calculates lineal feet (LF) and board feet (BF) requirements, applies industry-standard waste factors, and generates professional Excel invoices with pricing.

### Current Functionality
- Collects project measurements (walls, doors, windows) or accepts manual LF inputs per trim type
- Calculates LF requirements using TRIM TAKEOFF CONTROL DOCUMENT specifications
- Converts LF to BF using nominal stock thickness mapping
- Applies AWI-style waste factors from lookup tables
- Generates formatted Excel invoices with pricing calculations
- Supports multiple trim styles (Craftsman, Mitered, Built-Up, Sill/Apron Only) and finish levels (Economy, Standard, Luxury)

### Major Components
- **GUI Application**: Form-based input with validation, tabbed results display, export functionality
- **LF Calculation Engine**: Implements control document rules for all trim types and styles
- **BF Conversion Module**: Handles nominal thickness mapping, waste factor lookup, and BF calculations
- **Invoice Generator**: Creates formatted Excel files matching template structure with pricing
- **Configuration System**: Excel/CSV files for dimensions, waste factors, pricing, and species

### Key Development Milestones
- Initial form-based UI with measurement inputs
- Implementation of TRIM TAKEOFF CONTROL DOCUMENT calculation rules
- Integration of trim dimensions and AWI waste chart from Excel
- BF conversion with nominal stock thickness mapping
- Species selector and pricing integration
- Finishing toggle and finish type selection
- Manual LF input mode for pre-calculated takeoffs
- Excel invoice generation with formatting
- Output folder structure with automatic archiving

### Files in Repository

**Core Application**
- `trim_calculator.py` - Main GUI application with form inputs, validation, calculation orchestration, and export functions
- `trim_rules.py` - LF calculation engine implementing control document specifications for all trim types and styles
- `trim_bf_calculator.py` - BF conversion module with nominal thickness mapping, waste factor lookup, and species loading
- `invoice_generator.py` - Excel invoice generation with formatting, pricing calculations, and file management

**Configuration Data**
- `trim_dimensions.xlsx` - Board dimensions (width/thickness) by trim type, style, and finish level
- `awi_waste_chart.xlsx` - Waste factors by rip size and thickness category (4/4, 5/4, 6/4, 8/4)
- `lumber_species.csv` - Editable list of wood species for dropdown selection
- `bf_cost.xlsx` - Template for BF pricing by species and thickness (ready for pricing data)

**Output Structure**
- `Output/` - Contains latest generated invoice
- `Output/archive/` - Contains archived previous invoices

### Data Structures

**Input Data**
- Project measurements: interior/exterior wall linear feet, door/window counts, door height, finish level
- Manual LF mode: Direct LF values per trim type (base, casing, headers, sills, apron, jambs, dentils)
- Configuration: Species selection, wood-wrapped toggle, finishing requirements, pricing settings
- Invoice metadata: Job name, customer name, sales tax rate

**Internal Data Structures**
- LF results dictionary: `{trim_type: lineal_feet}`
- BF data dictionary: `{bf_raw, bf_with_waste, waste_factors, dimensions, nominal_thickness, thickness_category}`
- Pricing dictionary: `{linear_ft, bf_required, price_per_lf, line_total, setup_cost, etc.}`

### Outputs Generated

**CSV Export**
- Timestamped filename: `{script_name}_YYYYMMDD_HHMMSS.csv`
- Contains: Input summary, results by trim style with LF/BF breakdown, thickness information

**Excel Invoice**
- Timestamped filename: `Trim_Estimate_YYYYMMDD_HHMMSS_{JobName}.xlsx`
- Format: Matches Moulding Calculator Template structure
- Contains: Header information, line items with pricing, species subtotal, total with tax
- Location: Saved to `Output/` folder, previous files archived automatically

### External Integrations

**Excel Files (Read)**
- `trim_dimensions.xlsx` - Board size specifications
- `awi_waste_chart.xlsx` - Waste factor lookup table
- `bf_cost.xlsx` - Pricing data (when populated)

**Excel Files (Write)**
- Invoice files to `Output/` folder

**CSV Files**
- `lumber_species.csv` - Species list for dropdown

### Dependencies
- `tkinter` - GUI framework (Python standard library)
- `pandas` - Excel file reading/writing
- `openpyxl` - Excel file manipulation and formatting
- `csv` - CSV file handling (Python standard library)
- `datetime` - Timestamp generation (Python standard library)
- `os` - File system operations (Python standard library)

### Known Limitations
- PDF schedule parser not implemented (uses assumptions when schedule not provided)
- Setup costs are hardcoded (should be configurable)
- Manual LF mode uses Craftsman dimensions for all styles
- Window jamb and door jamb use same dimensions (may need separation)
- Finish pricing uses simplified multiplier (1.15x) - may need granular pricing

---

## 2. RULES & STANDARDS DOCUMENT

### Naming Conventions

**Files**
- Snake_case for Python files: `trim_calculator.py`, `trim_bf_calculator.py`
- Descriptive names indicating module purpose

**Functions**
- Snake_case: `calculate_trim()`, `get_trim_dimensions()`, `format_description()`
- Verb-noun pattern for actions: `load_*()`, `calculate_*()`, `get_*()`, `generate_*()`

**Variables**
- Snake_case: `linear_ft`, `bf_required`, `finish_level`
- Descriptive names: `int_walls_linear_ft`, `nominal_thickness`, `sales_tax_rate`

**Classes**
- PascalCase: `TrimCalculatorApp`

**Constants**
- UPPER_SNAKE_CASE: `TRIM_STYLES`, `FINISH_LEVELS`, `DOOR_HEIGHTS`, `RUNNING_WASTE`

### File Structure & Organization

**Module Separation**
- UI logic in `trim_calculator.py`
- Calculation rules in `trim_rules.py`
- BF conversion in `trim_bf_calculator.py`
- Invoice generation in `invoice_generator.py`

**Configuration Files**
- Excel files for structured data (dimensions, waste, pricing)
- CSV for simple lists (species)
- All config files in same directory as application

**Output Management**
- All invoices in `Output/` folder
- Archive folder: `Output/archive/`
- Automatic archiving before new invoice creation

**File Responsibilities**
- Each module handles one concern (UI, calculations, BF, invoices)
- No cross-dependencies between calculation modules
- Configuration data externalized to Excel/CSV

### Input & Output Standards

**Input Validation**
- Numeric fields: 0 to 10,000 range
- Real-time validation on keypress
- Error messages for out-of-range values

**Units**
- Linear feet: Decimal format (e.g., 123.45)
- Board feet: Decimal format with 2 decimal places
- Dimensions: Inches as decimals (e.g., 5.25, 0.75)
- Thickness categories: String format ('4/4', '5/4', '6/4', '8/4')
- Currency: Dollar format with 2 decimals ($1,234.56)
- Percentages: Decimal format (0.06 = 6%)

**Excel Format Standards**
- Headers: Arial 10pt bold, right-aligned
- Numbers: Right-aligned with appropriate number formats
- Text: Left-aligned
- Borders: Thin borders on all data cells
- Column widths: Optimized for readability

**CSV Format**
- UTF-8 encoding
- Comma-separated
- Headers in first row
- Sections separated by empty rows

**File Naming**
- Invoices: `Trim_Estimate_YYYYMMDD_HHMMSS_{JobName}.xlsx`
- CSV exports: `{script_name}_YYYYMMDD_HHMMSS.csv`
- Timestamps: 24-hour format, no spaces

### Business Rules & Logic

**LF Calculation Rules**
- Baseboard: Interior walls × 2 + Exterior walls, then style multiplier
- Window casing: Height × 2 legs × quantity
- Window header: (Width + 1 foot) × quantity
- Window sill: Width × quantity (non-sliders only)
- Window apron: Matches sill LF
- Window jamb: 3 sides (Craftsman) or 4 sides (Mitered)
- Door casing: Height × legs (1 for exterior, 2 for interior) × quantity
- Door header: (Width × legs + 1 foot) × quantity
- Door jamb: Height × 2 × quantity (barn/pocket doors only)

**Style Overrides**
- Mitered: Removes sill/apron/header, adds to casing; full-perimeter jamb
- Built-Up: Adds dentil (2× header LF)
- Sill/Apron Only: Only sill and apron for windows

**BF Calculation Rules**
- Nominal thickness mapping: Finished thickness → next stock size (0.5" → 4/4, 0.75" → 4/4, 1.0" → 5/4, 1.25" → 6/4, >1.25" → 8/4)
- BF formula: (Nominal Thickness × Width × LF) / 12
- Use nominal stock thickness, not finished thickness

**Waste Application**
- Running waste (10%): Baseboard, sills, aprons, headers, dentil
- Standing waste (15%): Casing, jamb
- AWI waste: Looked up by rip size and thickness category from chart
- Applied after raw BF calculation: `BF_with_waste = BF × (1 + waste_factor)`

**Pricing Rules**
- Base LF Price = (BF Cost with Markup / LF) + LF Cost per Foot
- Finish multiplier: 1.15x if finishing, 1.0x if not
- Final LF Price = Base LF Price × Finish Multiplier
- Line Total = (Final LF Price × LF) + Setup Cost
- Total = Subtotal + (Subtotal × Sales Tax Rate)

**Assumptions**
- Window dimensions (no schedule): Width = 48", Height = Door Height - 40"
- Door width: 36" standard
- Wood-wrapped: Defaults to True
- Setup costs: Fixed per trim type (Base: 725, Casing: 525, Header: 725, Sill: 925, Apron: 725, Jamb: 675, Dentil: 800)

### UI/UX Standards

**Form Layout**
- Label on left, input on right
- Grouped related fields in labeled frames
- Consistent padding (5px) and spacing
- Input validation feedback via error dialogs

**Input Restrictions**
- Numeric fields: 0-10,000 range enforced
- Dropdowns: Read-only to prevent invalid selections
- Toggle visibility: Show/hide dependent fields based on selections

**Results Display**
- Tabbed interface: One tab per trim style
- Columns: Trim Type | LF Needed | BF Required | Thickness (Stock) | Width
- Totals row at bottom
- Read-only text widgets (prevents accidental editing)

**Button Organization**
- Action buttons grouped horizontally
- Primary action (Calculate) first, secondary actions follow

### Error Handling & Edge Cases

**Validation**
- All numeric inputs validated on entry (0-10,000)
- Error dialogs for invalid ranges
- Separate validation for manual vs standard input modes

**File Operations**
- Checks for file existence before reading
- Graceful fallback to defaults if config files missing
- Error dialogs for file operation failures

**Calculation Edge Cases**
- Zero values handled (returns 0.0, not error)
- Missing dimensions: Returns None, skips calculation
- Empty inputs: Treated as 0
- Division by zero: Checked before calculation

**Default Values**
- Door height: 6/8 (6'8")
- Finish level: Standard
- Species: First in list
- Wood-wrapped: True
- LF cost per foot: $0.85
- BF markup: 20%
- Sales tax: 6%

### Integration Behavior

**Excel File Reading**
- Uses pandas for data loading
- Caches loaded data to avoid repeated file reads
- Handles missing files gracefully

**Excel File Writing**
- Uses openpyxl for formatting control
- Preserves template structure and cell positions
- Applies number formats, fonts, alignment, borders

**CSV Export**
- Standard CSV format, UTF-8 encoding
- Includes all calculation results
- Timestamped filenames

**File Archiving**
- Moves existing invoices to archive before creating new
- Adds timestamp to archived files if name collision
- Silent failure on archive errors (non-critical)

### TODO List / Known Gaps

**Unimplemented Features**
- PDF schedule parser for door/window dimensions
- Configurable setup costs table (currently hardcoded)
- Real-time vendor pricing API integration
- Multi-species support in single invoice
- Style-specific dimensions in manual LF mode

**Inconsistencies**
- Window jamb vs door jamb use same dimensions (may need separation)
- Manual LF mode always uses Craftsman dimensions regardless of style selection
- Finish pricing simplified to 1.15x multiplier (may need size-based pricing)

**Recommended Improvements**
- Make setup costs configurable via Excel file
- Add window/door dimension inputs for manual entry
- Implement PDF parser for schedule files
- Add validation for Excel file structure/format
- Create setup/installation documentation

**Technical Debt**
- Some hardcoded values should be moved to configuration
- Error handling could be more granular
- Unit tests not yet implemented
- Documentation could be expanded for end users

