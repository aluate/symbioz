# ACC Express Order - Project Report

**Generated:** 2024-12-19  
**Last Updated:** 2024-12-19 (Phase 3 Complete + Self-Audit)  
**Status:** Active Development - Core Features Complete, Phase 3 (Pricing & Presets) Implemented

---

## 1. Overview

ACC Express is a web-based cabinet ordering application designed for quick-turn cabinet orders from a curated Express catalog. The application provides a guided, multi-step wizard interface that allows contractors and clients to:

- Define job information
- Select finishes from a color library (Paint, Stain, Melamine) or enter custom finishes
- Create rooms with room-level attributes (finish, door style, pull, crown, light valance, box material)
- Add cabinet line items from a catalog-driven selection
- Generate and download order packets as ZIP files containing CSV exports

**Tech Stack:**
- **Backend:** Python 3.x, FastAPI, Pydantic (data validation)
- **Frontend:** HTML5, Tailwind CSS (CDN), Vanilla JavaScript
- **Data Sources:** 
  - JSON catalog (`config/cabinets_catalog.json`)
  - CSV finish library (`config/finish_colors.csv`)
  - CSV pricing config (`config/express_pricing.csv`) - **NEW in Phase 3**
  - JSON presets (`config/express_presets.json`) - **NEW in Phase 3**
- **Output:** ZIP files containing `order.csv` and `room_schedule.csv` with pricing columns

---

## 2. Application Entry Points

### Running the Application

**Command:**
```bash
uvicorn apps.web.prime_order_api:app --reload --host 0.0.0.0 --port 8001
```

**FastAPI App Module:**
- Module: `apps.web.prime_order_api`
- Instance: `app` (FastAPI instance)

**Launcher Script:**
- **File:** `start_prime_order.bat` (Windows batch file)
- **Behavior:**
  1. Changes to repo root directory
  2. Starts uvicorn server in a new console window on port 8001
  3. Waits 3 seconds
  4. Opens default browser to `http://localhost:8001/express-order`
  5. Displays instructions to user

---

## 3. Routes

### Primary Routes (ACC Express)

| Method | Route | Purpose | Returns |
|--------|-------|---------|---------|
| `GET` | `/express-order` | Serve the ACC Express Order HTML form | HTML page |
| `GET` | `/express-order/catalog` | Return cabinet catalog as JSON | JSON object (29 families) |
| `GET` | `/express-order/finish-library` | Return finish colors library organized by medium | JSON: `{Paint: [...], Stain: [...], Melamine: [...]}` |
| `GET` | `/express-order/presets` | Return cabinet preset configurations | JSON object mapping preset codes to configurations |
| `POST` | `/express-order/submit` | Accept order JSON, generate CSVs, return ZIP | StreamingResponse (ZIP file) |

### Legacy Routes (Backward Compatibility)

| Method | Route | Purpose | Returns |
|--------|-------|---------|---------|
| `GET` | `/prime-order` | Serve HTML form (legacy) | HTML page (same as `/express-order`) |
| `GET` | `/prime-order/catalog` | Return catalog (legacy) | JSON object |
| `GET` | `/prime-order/finish-library` | Return finish library (legacy) | JSON object |
| `POST` | `/prime-order/submit` | Submit order (legacy) | StreamingResponse (ZIP file) |

### Static Assets

| Route | Purpose |
|-------|---------|
| `/static/advanced_logo.png` | ACC logo image (served via FastAPI StaticFiles) |

---

## 4. Data Models

### Pydantic Models (Backend Validation)

#### `JobInfo`
```python
class JobInfo(BaseModel):
    job_name: str
    job_number: Optional[str] = None
    client_name: str
    client_email: Optional[str] = None
    site_address: Optional[str] = None
    designer: Optional[str] = None
    delivery_or_pickup: Optional[str] = None
    requested_delivery_date: Optional[str] = None
    notes: Optional[str] = None
```

#### `FinishSlot`
```python
class FinishSlot(BaseModel):
    index: int  # 1-3
    finish_id: Optional[str] = None  # From finish_colors.csv
    label: str  # Human-readable label
    other_brand: Optional[str] = None  # For "Other" manual finishes
    other_name: Optional[str] = None   # For "Other" manual finishes
    other_code: Optional[str] = None   # For "Other" manual finishes
```

#### `FinishesInfo`
```python
class FinishesInfo(BaseModel):
    paint: Optional[List[FinishSlot]] = []
    stain: List[FinishSlot]
    melamine: List[FinishSlot]
```

#### `RoomInfo`
```python
class RoomInfo(BaseModel):
    name: str
    number: Optional[str] = None
    has_crown: bool = False
    has_light_valance: bool = False
    finish_type: Literal["Paint", "Stain", "Melamine"]
    finish_number: int  # 1-3 (references slot in FinishesInfo)
    pull: Literal["Black", "Satin Nickel", "None"] = "None"
    door_style: Optional[str] = None  # "Shaker", "Slim Shaker", "Slab MDF", "Slab"
    grain_direction: Optional[str] = None  # "Vertical Grain", "Horizontal Grain" (only for Melamine)
    box_material: str = "Melamine"  # "Melamine" or "Plywood"
```

#### `CabinetLineItem`
```python
class CabinetLineItem(BaseModel):
    line_id: int
    room: str  # References RoomInfo.name
    family_code: str  # References cabinets_catalog.json key
    width_in: float
    height_in: Optional[float] = None
    depth_in: Optional[float] = None
    quantity: int = 1
    hinge_side: Optional[str] = None
    rollout_trays_qty: int = 0
    trash_kit: Optional[str] = None
    applied_panels: int = 0  # 0, 1, or 2
    special_instructions: Optional[str] = None
```

#### `PrimeOrderRequest`
```python
class PrimeOrderRequest(BaseModel):
    job: JobInfo
    finishes: FinishesInfo
    rooms: List[RoomInfo]
    cabinets: List[CabinetLineItem]
```

---

## 5. Catalog & Finish Libraries

### Pricing Configuration (`config/express_pricing.csv`) - **NEW in Phase 3**

**Structure:**
- CSV file with 6 columns
- **Purpose:** Define pricing rules for families, finishes, and options

**Schema (columns):**
1. `key_type` - `family` | `finish` | `option`
2. `key` - Family code (e.g., `B_2D`), finish_id (e.g., `PAINT_SW_ALABASTER`), or option name (e.g., `rollout_tray`)
3. `description` - Human-readable description
4. `price_per_unit` - Numeric price value
5. `unit` - `per_inch_width` | `per_cabinet` | `per_rollout` | `per_trash_kit` | `per_applied_panel`
6. `active` - TRUE/FALSE (only TRUE rows are loaded)

**Loading:**
- Loaded via `load_pricing_config()` function
- Filters to `active == TRUE`
- Organized by key_type: `{family: {...}, finish: {...}, option: {...}}`
- Used by `calculate_cabinet_price()` during order submission

**Pricing Rules:**
- **Family pricing:** Base price per cabinet (per inch width or flat per cabinet)
- **Finish pricing:** Adder per cabinet based on `finish_id`
- **Option pricing:** Adders for rollouts, trash kits, applied panels, plywood upgrades

### Preset Configurations (`config/express_presets.json`) - **NEW in Phase 3**

**Structure:**
- JSON file mapping preset codes to configurations
- **Purpose:** Quick-load standard cabinet layouts

**Schema:**
```json
{
  "PRESET_CODE": {
    "label": "Human-readable name",
    "description": "Description of preset",
    "default_room_suffix": "Suffix for room name",
    "items": [
      {"family_code": "B_2D", "width_in": 30},
      ...
    ]
  }
}
```

**Loading:**
- Loaded via `GET /express-order/presets` endpoint
- Exposed to frontend for preset selection UI
- Used by `applyPreset()` function to add multiple cabinets at once

**Examples:**
- `KITCHEN_8FT_BASE` - 8-foot base run (sink + 2-door + 3-drawer)
- `BATH_60_VANITY` - 60" bath vanity (drawer-sink-drawer)
- `WALL_6FT` - 6-foot wall run (2-door + 2-door)

---

## 5. Catalog & Finish Libraries (Original)

### Cabinet Catalog (`config/cabinets_catalog.json`)

**Structure:**
- Top-level keys are family codes (e.g., `B_1D`, `B_2D`, `T_PANTRY`, `V_SINK_CENTER`)
- **Total Families:** 29

**Schema (per family):**
```json
{
  "FAMILY_CODE": {
    "display_name": "Human-readable name",
    "category": "Base | Wall | Tall | Vanity | Accessory",
    "default_height_in": 34.5,
    "default_depth_in": 24.0,
    "allowed_widths_in": [9, 12, 15, ...],
    "allowed_heights_in": [34.5],
    "allowed_depths_in": [12, 18, 24],  // Optional, for accessories
    "code_pattern": "B1D-{width}",  // Template for generating cabinet_code
    "cv_assembly": "B1D",  // Cabinet Vision assembly reference
    "cnc_program": "B1D_STD",  // CNC program reference
    "options": {
      "supports_rollouts": true,
      "max_rollouts": 3,
      "supports_trash_kit": false,
      "supports_spice_pullout": false,
      "supports_applied_panels": true
    }
  }
}
```

**Loading:**
- Loaded at startup via `load_catalog()` function
- Cached in global `_catalog` variable
- Exposed via `/express-order/catalog` endpoint

### Finish Colors Library (`config/finish_colors.csv`)

**Structure:**
- CSV file with 20 columns
- **Total Rows:** 9 (all active)
- **Mediums:** Paint (3), Stain (3), Melamine (3)

**Schema (columns):**
1. `finish_id` - Unique identifier (e.g., `PAINT_SW_ALABASTER`)
2. `color_brand` - Brand name (e.g., "Sherwin-Williams")
3. `color_collection` - Collection/line name
4. `color_name` - Color name (e.g., "Alabaster")
5. `color_code` - Color code (e.g., "SW 7008")
6. `color_chip_url` - URL to color swatch image (optional)
7. `medium` - Paint | Stain | Melamine
8. `substrate` - Material (e.g., "MDF", "Select Alder")
9. `shop_product_line` - Shop product line
10. `shop_sku` - Shop SKU
11. `vendor` - Vendor name
12. `vendor_sku` - Vendor SKU
13. `cost_per_unit` - Cost per unit
14. `cost_unit` - Unit (e.g., "per_gallon")
15. `waste_factor` - Waste factor (decimal)
16. `eligible_for_prime` - TRUE/FALSE
17. `recommended_slot` - Recommended slot (PAINT/STAIN/MEL)
18. `max_sheen` - Maximum sheen level
19. `notes` - Notes
20. `active` - TRUE/FALSE (only TRUE rows are loaded)

**Loading:**
- Loaded via `load_finish_library()` function
- Filters to `active == TRUE`
- Normalizes `medium` values (case-insensitive, title-cased)
- Organized by medium: `{Paint: [...], Stain: [...], Melamine: [...]}`
- Exposed via `/express-order/finish-library` endpoint

---

## 6. Frontend Flow

### Multi-Step Wizard

The frontend is a single-page application (`apps/web/templates/prime_order.html`) with 5 steps:

#### **Step 1: Job Info**
- **Fields:** Job name, job number, client name, client email, site address, designer, delivery/pickup, requested delivery date
- **Validation:** Job name and client name required
- **Next Button:** Enabled when required fields filled

#### **Step 2: Finishes**
- **UI Pattern:** "One finish at a time" - dynamic rows
- **Finish Types:** Paint, Stain, Melamine, Other (Manual Entry)
- **Library Selection:** Dropdown populated from `/express-order/finish-library`
- **Manual Entry:** For "Other" type, shows fields for Brand, Color Name, Color Code, Medium
- **Max Finishes:** Up to 6 total (3 Paint + 3 Stain + 3 Melamine)
- **State:** `jobFinishes` array (global)
- **Key Functions:**
  - `loadFinishLibrary()` - Fetches library on page load
  - `addFinishRow()` - Adds new finish row
  - `removeFinishRow(id)` - Removes finish row
  - `updateFinishRowType()` - Handles type change
  - `updateFinishRowColor()` - Handles color selection
  - `getDefinedFinishes()` - Builds backend-compatible `finishes` object

#### **Step 3: Rooms**
- **Fields:** Room name, room number (optional), finish type, finish number, pull, door style, grain direction (conditional), crown checkbox, light valance checkbox, box material checkbox
- **Dynamic Logic:**
  - Door style options change based on finish type:
    - Paint/Stain: "Shaker", "Slim Shaker", "Slab MDF"
    - Melamine: "Slab" (auto-selected), shows grain direction dropdown
  - Finish number dropdown only shows defined slots for selected type
- **State:** `rooms` array (global)
- **Key Functions:**
  - `addRoom()` - Adds room to array
  - `updateRoomsList()` - Renders rooms table with Edit/Duplicate/Remove buttons
  - `openEditRoomModal(index)` - Opens edit modal
  - `saveEditedRoom()` - Updates room and related cabinets
  - `duplicateRoom(index)` - Duplicates a room with "(Copy)" suffix (NEW in Phase 3)
  - `removeRoom(index)` - Removes room (with confirmation if cabinets exist)
  - `updateRoomFinishNumberDropdown()` - Populates finish number options
  - `updateRoomDoorStyleDropdown()` - Populates door style options

#### **Step 4: Cabinets**
- **Presets Panel (NEW in Phase 3):**
  - Preset selector dropdown (populated from `/express-order/presets`)
  - Room selector for applying preset
  - "Apply Preset to Room" button - adds all preset cabinets to selected room
- **Fields:** Category, family, width, height (conditional), depth (conditional), quantity, room, hinge side, rollout trays, trash kit, applied panels (conditional), special instructions
- **Dynamic Logic:**
  - Category dropdown filters family options
  - Family dropdown populated from catalog
  - Height/depth shown based on family requirements
  - Applied panels shown only for families with `supports_applied_panels: true`
- **State:** `cabinets` array (global), `catalog` object (global), `presets` object (global)
- **Key Functions:**
  - `loadCatalog()` - Fetches catalog on page load
  - `loadPresets()` - Fetches presets on page load
  - `applyPreset()` - Applies selected preset to selected room
  - `populateCabinetFamilyDropdown()` - Populates family dropdown
  - `setupCabinetFormListeners()` - Sets up event listeners
  - `addCabinetToOrder()` - Validates and adds cabinet
  - `updateOrderList()` - Renders cabinets table with duplicate buttons
  - `duplicateCabinet(index)` - Duplicates a cabinet line item
  - `removeCabinet(index)` - Removes cabinet

#### **Step 5: Review & Export**
- **Display:** Summary of job info, finishes, rooms, cabinets, pricing summary (NEW in Phase 3)
- **Pricing Summary (NEW in Phase 3):**
  - Shows note that pricing is calculated server-side
  - Lists pricing breakdown items (unit prices, line totals, room totals)
  - Marked as "Express Estimate Only"
- **Action:** "Download Express Order Packet" button
- **Key Functions:**
  - `populateReviewPage()` - Fills review step with current data and pricing summary
  - `submitOrder()` - Submits order to `/express-order/submit`

### Navigation

- **Step Indicator:** Visual breadcrumb at top showing current step
- **Navigation Functions:**
  - `goToStep(step)` - Shows/hides step sections, updates indicator
  - `updateStepValidation()` - Enables/disables "Next" buttons based on validation
- **State:** `currentStep` (global, 1-5)

### Global State

```javascript
let catalog = {};  // Cabinet catalog from API
let finishLibrary = {Paint: [], Stain: [], Melamine: []};  // Finish library from API
let rooms = [];  // Room objects
let cabinets = [];  // Cabinet line items
let lineIdCounter = 1;  // Auto-incrementing ID for cabinets
let currentStep = 1;  // Current wizard step
let editingRoomIndex = -1;  // Index of room being edited
let jobFinishes = [];  // Dynamic finish rows
let finishRowCounter = 1;  // Auto-incrementing ID for finish rows
```

---

## 7. Output / CSV Generation

### Order CSV (`order.csv`)

**Header (37 columns - updated in Phase 3):**
```
job_name, job_number, client_name, client_email, site_address,
designer, delivery_or_pickup, requested_delivery_date,
room, cabinet_type, cabinet_code, family_code,
width_in, height_in, depth_in, quantity,
finish_type, finish_number, finish_label, finish_id,
color_brand, color_name, color_code, medium,
shop_product_line, shop_sku, vendor,
door_style, grain_direction, box_material,
hinge_side, rollout_trays_qty, trash_kit, applied_panels,
special_instructions,
unit_price, line_total
```

**New Columns (Phase 3):**
- `unit_price` - Price per single cabinet (before quantity multiplier)
- `line_total` - Total price for this line (unit_price × quantity)

**Row Generation:**
- One row per cabinet line item
- Job fields from `JobInfo` model
- Cabinet fields from `CabinetLineItem` + catalog lookup
- Finish fields derived from room's `finish_type` + `finish_number`:
  - Looks up slot in `FinishesInfo`
  - If `finish_id` exists, looks up metadata in finish library
  - If "Other" finish, uses `other_brand`, `other_name`, `other_code` from slot
- Room-level fields (`door_style`, `grain_direction`, `box_material`) from `RoomInfo`

### Room Schedule CSV (`room_schedule.csv`)

**Header (18 columns - updated in Phase 3):**
```
room_name, room_number, finish_code, finish_label, finish_id,
color_brand, color_name, color_code, medium, pull,
door_style, grain_direction, box_material,
has_crown, has_light_valance, cabinet_count, accessory_count,
room_total
```

**New Column (Phase 3):**
- `room_total` - Total price for all cabinets in this room

**Row Generation:**
- One row per room
- Room fields from `RoomInfo` model
- Finish fields derived same as order.csv
- Counts computed by iterating through cabinets array:
  - `cabinet_count`: Non-accessory cabinets for this room
  - `accessory_count`: Accessory cabinets for this room

### ZIP File

- **Name:** `ACC_Express_Order_{job_name}.zip`
- **Contents:**
  - `order.csv`
  - `room_schedule.csv`
- **Generation:** In-memory using `zipfile.ZipFile` and `BytesIO`
- **Response:** `StreamingResponse` with `application/zip` media type

---

## 8. Testing

### Automated Tests

**Smoke Test (`test_express_smoke.py`):**
- Validates app import and route structure
- Tests `/express-order/catalog`, `/express-order/finish-library`, `/express-order/presets` endpoints
- End-to-end submission test with minimal payload
- Verifies ZIP generation and CSV structure
- Checks pricing columns (`unit_price`, `line_total`, `room_total`)
- Validates hinge logic (1-door vs 2-door)
- Verifies tall cabinet 15" width support

**Four-Room Scenario Test (`tests/test_express_scenario_four_rooms.py`):**
- Realistic 4-room job test (Wilson Residence)
- Tests multiple finish types (Paint, Stain, Melamine)
- Validates room-level attributes (door style, grain direction, box material)
- Exercises hinge logic across multiple cabinet families
- Tests tall cabinet with 15" width
- Verifies pricing integration
- Validates all 4 rooms appear in room_schedule.csv
- Confirms applied panels, rollouts, and other options

**Test Requirements:**
- `httpx` package required for TestClient: `pip install httpx`
- Run smoke test: `python test_express_smoke.py`
- Run scenario test: `python tests/test_express_scenario_four_rooms.py`

### Test Coverage

**Validated Features:**
- ✅ Hinge side logic (only B_1D, W_1D, W_1D_GLASS require hinge)
- ✅ Tall cabinet widths (T_PANTRY, T_UTILITY support 15")
- ✅ Pricing engine (unit_price, line_total, room_total)
- ✅ Finish library integration (Paint, Stain, Melamine)
- ✅ Presets system (read-only)
- ✅ Room-level attributes (door_style, grain_direction, box_material)
- ✅ Applied panels, rollouts, trash kits
- ✅ ZIP generation with both CSVs
- ✅ Multi-room job handling

---

## 9. Known Issues / TODOs

### ✅ FIXED: `/express-order/submit` Crash

**Issue:**
- Frontend error: "Unexpected token 'I', 'Internal S' is not valid JSON"
- Backend was returning 500 Internal Server Error HTML page

**Root Cause:**
- **Critical Indentation Bug:** Lines 389-693 were not properly indented inside the `try` block
- This caused a `NameError` when trying to access variables (`rooms`, `cabinets`, etc.) that were defined inside the try block but used outside
- The error was caught by FastAPI's default exception handler, which returned an HTML error page instead of JSON

**Fix Applied:**
- Fixed indentation: All CSV generation code (lines 389-693) now properly indented inside the `try` block
- Added comprehensive error handling with logging
- Added validation for request structure
- Added default values for missing fields (`box_material`, `applied_panels`)

**Status:** ✅ **RESOLVED** (2024-12-19)

### Phase 2 Features (Not Yet Implemented)

1. **Email Delivery**
   - SMTP configuration via environment variables
   - Background task to send ZIP file via email
   - Email templates

2. **Builder Login + Job History**
   - SQLite database with User and ExpressJob models
   - Session-based authentication
   - Dashboard showing job history
   - Ability to re-download order packets

3. **Finish Swatches**
   - Display `color_chip_url` from finish library in Step 2
   - Visual color selection with swatch images

### Current Limitations

- No pricing logic (prices not calculated)
- No drag-and-drop room layout UI
- No preset configurations
- No integration with Cabinet Vision or other CAD systems
- No validation of cabinet dimensions against actual shop capabilities
- No multi-user collaboration features

---

## 9. File Structure

### Backend Core
- `apps/web/prime_order_api.py` - FastAPI application (693 lines)
  - Route handlers
  - Pydantic models
  - Catalog/finish library loaders
  - CSV/ZIP generation logic

### Frontend Template
- `apps/web/templates/prime_order.html` - Single-page application (2,290 lines)
  - HTML structure
  - Tailwind CSS styling
  - JavaScript for wizard flow, form handling, API calls

### Catalog/Config Files
- `config/cabinets_catalog.json` - Cabinet family definitions (29 families)
- `config/finish_colors.csv` - Finish library (9 active rows)
- `config/express_pricing.csv` - Pricing rules (family, finish, option rates) - **NEW in Phase 3**
- `config/express_presets.json` - Preset cabinet configurations - **NEW in Phase 3**

### Static Assets
- `apps/web/static/advanced_logo.png` - ACC logo image

### Launch Scripts / Tooling
- `start_prime_order.bat` - Windows one-click launcher

---

## 10. How to Refresh This Report

To update this project report in a future Cursor session:

1. **Re-scan the repo:**
   - List directories: `apps/web/`, `config/`, `docs/`
   - Count files and lines of code
   - Check for new routes, models, or features

2. **Re-open this file:**
   - Read `docs/acc_express_project_report.md`
   - Identify sections that need updates

3. **Update sections:**
   - **Routes:** Check `@app.get` and `@app.post` decorators in `prime_order_api.py`
   - **Data Models:** Check Pydantic `class` definitions
   - **Frontend Flow:** Review JavaScript functions in `prime_order.html`
   - **Known Issues:** Add new bugs or completed TODOs

4. **Add new issues:**
   - Document any new crashes, bugs, or limitations
   - Include stack traces, file names, and line numbers
   - Note any architectural changes or new features

5. **Version the report:**
   - Update the "Generated" date at the top
   - Add changelog entries for significant updates

---

## 11. Testing Checklist

### Manual Testing Steps

1. **Start the server:**
   ```bash
   uvicorn apps.web.prime_order_api:app --reload --host 0.0.0.0 --port 8001
   ```

2. **Test Step 1 (Job Info):**
   - Fill required fields (job name, client name)
   - Verify "Next" button enables
   - Navigate to Step 2

3. **Test Step 2 (Finishes):**
   - Add a Paint finish (select from library)
   - Add a Stain finish (select from library)
   - Add an "Other" finish (manual entry)
   - Verify finish rows display correctly
   - Navigate to Step 3

4. **Test Step 3 (Rooms):**
   - Add a room with Paint finish
   - Verify door style options (Shaker, Slim Shaker, Slab MDF)
   - Add a room with Melamine finish
   - Verify door style is "Slab" and grain direction appears
   - Edit a room (change finish, pull, etc.)
   - Navigate to Step 4

5. **Test Step 4 (Cabinets):**
   - Select category (Base)
   - Select family (B_1D)
   - Enter width, quantity
   - Select room
   - Add cabinet
   - Verify cabinet appears in list
   - Navigate to Step 5

6. **Test Step 5 (Review & Export):**
   - Verify all data displays correctly
   - Click "Download Express Order Packet"
   - Verify ZIP file downloads
   - Extract ZIP and verify CSV files
   - Check CSV headers and data

### Error Scenarios to Test

- Submit with no rooms → Should show validation error
- Submit with no cabinets → Should show validation error
- Submit with no finishes → Should show validation error
- Submit with invalid family code → Should skip gracefully
- Submit with room that has no finish defined → Should use defaults

---

## 12. Architecture Notes

### Design Decisions

1. **Room-Level Attributes:** Finish, door style, pull, crown, light valance, and box material are defined at the room level, not per cabinet. This matches real-world workflows where an entire room shares these attributes.

2. **Catalog-Driven UI:** The frontend dynamically populates options based on the catalog. This allows the catalog to be the single source of truth for available cabinet families and their options.

3. **Finish Library Integration:** Finishes are selected from a CSV library, ensuring consistency and enabling future features like pricing, vendor integration, and color swatches.

4. **Multi-Step Wizard:** The UI guides users through a sequential flow, preventing errors and improving UX compared to a single overwhelming form.

5. **Backward Compatibility:** Legacy `/prime-order/*` routes are maintained alongside new `/express-order/*` routes to avoid breaking existing integrations.

### Future Enhancements

- **Phase 3:** Pricing engine, preset configurations, drag-and-drop layout
- **Phase 4:** Email delivery, builder login, job history dashboard
- **Phase 5:** Finish swatches, Cabinet Vision integration, multi-user collaboration

---

**End of Report**

