# GUI Changelog - Testing Round 1

This document tracks requested changes during testing. Changes are numbered sequentially and will be implemented in batches.

---

### [1] Roof inputs: pitch format, roof style, and ridge position

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Geometry

- **Problem:**
  - Current GUI expects `roof_pitch` as a decimal ratio (e.g., 0.333), which is not how builders think or talk.
  - There is no way to specify roof style (gable vs shed).
  - For gable roofs, there is no way to specify ridge location (centered vs offset), which is critical for panel length/layout and proper material takeoff.

- **Change requested:**

  1. **Roof pitch input (builder-friendly)**
     - Replace the current numeric `roof_pitch` entry with a **text field** that accepts common formats:
       - `"4/12"`, `"3/12"`, `"2/12"` (rise/run)
       - `"4"` or `"3"` (assume `X/12` if no `/` is given)
       - Decimal ratios like `"0.333"` should still be accepted.
     - Parse this into the internal `roof_pitch_ratio` float used by the calculator:
       - If input contains `/`, parse `rise/run` and compute `rise / run`.
       - If input is a whole number, treat as `rise_per_12` → `rise / 12.0`.
       - If input is a float between 0 and 2, treat as a ratio directly.
     - Add clear label/placeholder text in the GUI, e.g.:
       - Label: `Roof Pitch`
       - Placeholder / helper: `e.g. 4/12 or 3/12`

  2. **Roof style selector**
     - Add a dropdown/select in the GUI for `roof_style` with at least:
       - `gable` (default)
       - `shed`
     - This value should be passed into the appropriate input dataclass (`MaterialInputs` or `GeometryInputs`, whichever is more appropriate) as a new field, e.g. `roof_style: str`.

  3. **Ridge position for gable roofs**
     - For `roof_style == "gable"`, add a numeric input:
       - Label: `Ridge position from left eave (ft)`
       - Behavior:
         - Default value should be **length / 2** (centered ridge).
         - User can override with any value from `0` to `length`.
       - This should be stored on the inputs as something like:
         - `ridge_position_ft_from_left: float`
     - For `roof_style == "shed"`, this field should be:
       - Disabled/greyed out in the GUI OR ignored by the calculator.
     - In a future step, geometry/assemblies will use `roof_style` + `ridge_position_ft_from_left` to control panel lengths and counts; for now, just make sure the values are captured and passed through the models cleanly.

- **Implementation notes:**
  - Update `apps/gui.py`:
    - Replace the existing roof pitch entry with a string-based pitch entry and a parsing helper function.
    - Add a `roof_style` dropdown with default `"gable"`.
    - Add a `ridge_position_ft_from_left` entry, defaulting dynamically to `length / 2` when length changes (at minimum, set it after initial defaults).
    - Wire these into the correct dataclasses when constructing `GeometryInputs` / `MaterialInputs` / `PoleBarnInputs`.
  - Update the relevant input model(s) in `systems/pole_barn/model.py` to include new fields:
    - `roof_style: str = "gable"`
    - `ridge_position_ft_from_left: float | None = None` (or similar default)
  - Add basic validation in the GUI:
    - If ridge position is provided, ensure it's between `0` and `length`.
    - Show a friendly error dialog if parsing the pitch fails.

- **Acceptance criteria:**
  1. In the GUI, I can enter `4/12`, `3/12`, `4`, or `0.333` for roof pitch and the calculator runs without error.
  2. `roof_style` appears as a dropdown with `gable` and `shed`; default is `gable`.
  3. When `roof_style = gable`, the ridge position field is enabled and saved into the inputs; when `roof_style = shed`, the field is disabled or ignored.
  4. Debug/logging or a temporary print shows that `roof_pitch_ratio`, `roof_style`, and `ridge_position_ft_from_left` are being passed into the calculator correctly.
  5. Existing calculations still work when I use the default values (no regression).

---

### [2] CSV Schema Mismatch: Missing `part_name` column in parts.example.csv

**STATUS: ✅ COMPLETE** (Fixed in Path B)

- **Area:** Config / CSV / Pricing

- **Problem:**
  When running the GUI, the app throws:
  > **Missing required column: `part_name` in parts.example.csv**

  This indicates that the current `parts.example.csv` schema in `/config/parts.example.csv` does **not** match what `pricing.py` expects. Modern schema requires:
  ```
  part_id, part_name, description, category, unit, vendor, source, notes
  ```
  But the file is missing **`part_name`**.

- **Severity:** Critical (calculator cannot load pricing)

- **Fix Required:**
  1. Add a `part_name` column to the CSV
  2. Populate `part_name` for each part (likely identical to description or simplified name).
  3. Ensure the header row exactly matches what the loader expects.

---

### [3] Standing Rule: CSV Schema Consistency Requirement

**STATUS: ✅ COMPLETE** (Documented in APP_WORKFLOW_GUIDE.md)

- **Area:** Workflow / Code Quality

- **Problem:**
  CSV schema mismatches (like entry [2]) are a recurring class of problems that can break the app at runtime. We need a standing rule to prevent this.

- **Change requested:**
  Add a standing instruction to Cursor (or any developer) to:
  1. Before implementing changes, scan all CSV loaders for required column names.
  2. Check all CSV files under `config/` for schema consistency.
  3. Fix any mismatches BEFORE writing code changes.

- **Implementation:**
  - Documented in `APP_WORKFLOW_GUIDE.md` as a standing rule.
  - Should be referenced before any code changes that touch CSV schemas.

---

### [4] Peak height should be derived, and labor/material costs must be separate

**STATUS: ✅ COMPLETE** (Fixed in Path B)

- **Area:** GUI / Inputs / Pricing / Geometry

- **Problem:**
  1. The GUI currently asks for **Peak Height (ft)** as an input. For a normal barn, peak height is a **dependent value** that can be derived from eave height, building width, roof pitch, and (for gable roofs) ridge position. Having it as an editable field invites bad/contradictory inputs.
  2. The GUI currently has a **Labor Rate ($/hr)** input. In practice, labor and material should be handled separately and consistently:
     - Labor rate is a company/config-level setting, not something we want changed per job on the front end.
     - Labor and material costs should be clearly separated in the results.
     - Markup should **not** blur the line between labor and material.

- **Change requested:**
  1. **Peak height: derived, not entered**
     - Remove the editable `Peak Height (ft)` input from the GUI.
     - Instead, show peak height as a **read-only derived value** in the results (and optionally in a non-editable field in the input panel).
     - Compute peak height based on:
       - `eave_height_ft`
       - `width_ft` (or the relevant span for the roof style)
       - `roof_pitch_ratio`
       - `roof_style` and `ridge_position_ft_from_left` (once implemented from Change [1])
     - For now (until more advanced roof logic is implemented), use:
       - For `roof_style == "gable"` with centered ridge:
         - `rise = (width_ft / 2.0) * roof_pitch_ratio`
         - `peak_height_ft = eave_height_ft + rise`
       - For other cases, we can approximate using the same logic or simply not show peak height until we formalize it; the important part is that the user **does not type** the peak height.
     - Ensure the internal models (e.g. `GeometryInputs` and `GeometryModel`) do not require peak height to be manually provided where it can be derived.

  2. **Labor rate removed from form; pricing separation clarified**
     - Remove `Labor Rate ($/hr)` from the GUI inputs.
     - Set labor rate as a configuration value instead:
       - Either a constant default in `PricingInputs` or loaded from a config file (e.g. a new `config/settings.example.csv`), but **not** user-editable from the main form.
     - Make sure the pricing logic keeps **labor and material costs fully separate**:
       - Material subtotal
       - Labor subtotal
       - Markup total
       - Tax total
       - Soft costs (delivery, permit, site prep)
     - Update the markup behavior so that:
       - **Material markup applies only to material costs**, not labor.
       - i.e. `markup = material_subtotal * (material_markup_factor - 1.0)`
     - Labor should be shown as its own bucket without additional markup baked into it.
     - The results pane should clearly show these categories on separate lines so it's obvious what is material vs labor vs markup.

- **Implementation notes:**
  - Update `apps/gui.py`:
    - Remove the peak height input field and the labor rate input field.
    - Ensure `GeometryInputs` is constructed without needing user-entered peak height.
    - Pass a fixed or config-derived labor rate into `PricingInputs` instead of reading it from the form.
    - Add a derived peak height display in the results block (e.g. as part of the geometry summary).
  - Update models and pricing:
    - If any model currently stores peak height as an input-only field, convert to derived where appropriate.
    - Adjust pricing logic (likely in `pricing.py` or `calculator.py`) so that markup is applied only to material subtotal, not (material + labor).
    - Optionally introduce a simple config source for labor rate so it can still be tuned without rebuilding the app.

- **Acceptance criteria:**
  1. The GUI no longer has an editable `Peak Height` field; peak height is shown only as a derived value.
  2. The GUI no longer asks for `Labor Rate ($/hr)`; the calculator still runs using a default/configured labor rate.
  3. The results clearly show:
     - Material subtotal
     - Labor subtotal
     - Markup total
     - Tax total
     - Grand total
  4. Markup is applied only to the material subtotal (not labor), and this is reflected correctly in the numbers.
  5. Existing tests pass or are updated to match the new pricing behavior.

---

### [5] Girt type selector (standard vs commercial)

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Assemblies

- **Problem:**
  Girt systems vary significantly between standard residential pole barns and commercial/post-frame buildings. The GUI assumes only one type, but quantity logic and cost change drastically depending on the framing system.

- **Change requested:**
  Add a dropdown to the GUI:
  - Label: "Girt Type"
  - Options:
    - `standard` (default)
    - `commercial` (bookshelf/blocking style)
  - Pass this into `MaterialInputs` or `AssemblyInputs` as a new field `girt_type: str`.
  - The assemblies layer will eventually use `girt_type` to select different quantity rules.

- **Acceptance criteria:**
  - GUI shows a new selector for girt type.
  - Default = `standard`.
  - Value is passed correctly into `PoleBarnInputs`.
  - Existing calculations remain unchanged until assembly logic is updated in a future entry.

---

### [6] Wall sheathing toggle (None / OSB / Plywood)

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Assemblies

- **Problem:**
  Currently the app assumes metal-only exterior walls. Many buildings require wall sheathing—OSB or plywood—before metal or instead of metal. This dramatically affects material takeoff.

- **Change requested:**
  Add a dropdown to the GUI:
  - Label: "Wall Sheathing"
  - Options:
    - `none` (default)
    - `osb`
    - `plywood`
  Add field to `MaterialInputs`: `wall_sheathing_type: str`.

- **Acceptance criteria:**
  - GUI includes new wall sheathing selector.
  - Value stored in inputs.
  - Does not yet change quantities until a future assembly update.

---

### [7] Roof sheathing toggle (None / OSB / Plywood)

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Assemblies

- **Problem:**
  Roof sheathing (OSB or plywood) is common for some builds and required for shingle systems. Current GUI cannot capture this.

- **Change requested:**
  Add a dropdown:
  - Label: "Roof Sheathing"
  - Options: `none`, `osb`, `plywood`
  Add field to `MaterialInputs`: `roof_sheathing_type: str`.

- **Acceptance criteria:**
  - GUI displays the selector.
  - Default is `none`.
  - Value is present in `PoleBarnInputs`.

---

### [8] Floor type selector (Slab / Gravel / None)

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Pricing / Assemblies

- **Problem:**
  The current form does not capture floor type. A concrete slab, gravel pad, or no floor at all changes quantities, pricing, and even some structural assumptions.

- **Change requested:**
  Add a dropdown:
  - Label: "Floor Type"
  - Options:
    - `slab`
    - `gravel`
    - `none`
  Add new field: `floor_type: str`.

- **Acceptance criteria:**
  - Selector appears in GUI.
  - Default = `none`.
  - Passed cleanly into the inputs.
  - Does not modify quantities yet (future entry).

---

### [9] Door count input (integer)

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Geometry

- **Problem:**
  GUI defaults doors or ignores door count. Need ability to specify number of doors (later sizes per door).

- **Change requested:**
  Add integer input:
  - Label: "Number of Doors"
  - Default: 0
  - Field wired into `GeometryInputs.door_count`.

- **Acceptance criteria:**
  - Input is present, validates as integer.
  - Default is 0.
  - Value passed correctly.

---

### [10] Window count input (integer)

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Geometry

- **Problem:**
  Window counts currently hard-coded or ignored in GUI.

- **Change requested:**
  Add integer input:
  - Label: "Number of Windows"
  - Default: 0
  - Field wired into `GeometryInputs.window_count`.

- **Acceptance criteria:**
  - Input appears and validates.
  - Default is 0.
  - Passed correctly into geometry.

---

### [11] Permit & Snow Load inputs

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Project Metadata / Structural

- **Problem:**
  The engineer form includes permit and snow load information that affects structural design and code compliance. Current GUI does not capture this.

- **Change requested:**
  Add inputs for:
  - Building type: `residential` / `commercial` (dropdown)
  - Building use/description (text field)
  - Permitting agency (text field)
  - Required snow load (psf) (numeric)
  - Requested snow load (psf) (numeric, optional)
  - Checkbox: "Snow load unknown / needs lookup"

- **Acceptance criteria:**
  - All fields appear in GUI.
  - Values stored in `PoleBarnInputs` or appropriate model.
  - For now, informational only (not yet used in calculations).

---

### [12] Build type and construction type selectors

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Project

- **Problem:**
  The engineer form distinguishes between:
  - New construction vs addition
  - Pole frame vs stick frame
  These affect design assumptions and potentially quantities.

- **Change requested:**
  Add dropdowns:
  - "Build Type": `pole` (default) / `stick_frame`
  - "Construction Type": `new` (default) / `addition`
  Add fields to `PoleBarnInputs` or appropriate model.

- **Acceptance criteria:**
  - Both selectors appear in GUI.
  - Defaults are `pole` and `new`.
  - Values stored correctly.

---

### [13] Slab details (thickness and reinforcement)

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Foundation

- **Problem:**
  When floor type is "slab", we need additional details for accurate material takeoff and pricing.

- **Change requested:**
  Add inputs (shown only when floor_type == "slab"):
  - Slab thickness (inches) - numeric
  - Slab reinforcement - dropdown: `none`, `mesh`, `rebar`
  Add fields to `MaterialInputs`: `slab_thickness_in`, `slab_reinforcement`.

- **Acceptance criteria:**
  - Fields appear when slab is selected.
  - Defaults: 4" thickness, `none` reinforcement.
  - Values stored correctly.

---

### [14] Door & window assemblies must include framing lumber and trim

- **Area:** Assemblies / Quantities / GUI Inputs

- **Problem:**
  Current door and window handling only counts openings; it does not account for:
  - Extra framing around openings (king studs, trimmers/jacks, headers, sill plates, blocking).
  - Exterior trim around doors and windows.
  This underestimates both lumber and trim. We already have good trim logic in the trim calculator that we should eventually reuse.

- **Change requested:**
  1. Treat each door and window opening as an assembly that includes:
     - Additional studs and headers per opening, based on opening size and wall height.
     - Exterior trim LF.
     - Exterior trim LF.
  2. In the short term:
     - Add hooks in the assemblies layer so that for each door/window opening, we can:
       - Compute an "extra framing LF/BF" quantity.
       - Compute a "door/window trim LF" quantity.
       - Map these to distinct assembly names (e.g. `door_framing`, `window_framing`, `door_trim`, `window_trim`) so they can be priced separately.
  3. Long term:
     - Reuse or mirror the existing trim calculator logic where practical for trim LF around openings.

- **Implementation notes:**
  - Do not change the GUI right now (we'll later add more detailed door/window sizing); rely on existing `door_count` and `window_count` as the drivers.
  - Add new assembly calculation functions that:
     - Use `door_count`, `window_count`, and wall height to approximate extra studs/headers.
     - Produce trim LF per opening, even if initially based on a standard size assumption.
     - Wire these new assemblies into `assemblies.example.csv` and `parts/pricing` so they show up as separate line items.

- **Acceptance criteria:**
  1. Material takeoff includes distinct quantities for:
     - Door framing lumber
     - Window framing lumber
     - Door trim
     - Window trim
  2. Priced output shows these as separate line items.
  3. Total lumber and trim costs increase when door/window counts increase, even before we implement detailed opening sizes.

---

### [15] Exterior finish selector (metal gauge, lap siding, stucco)

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Assemblies

- **Problem:**
  The app currently assumes a single exterior finish (29ga metal). In practice, exterior finish may be:
  - 29ga metal (default)
  - 26ga metal
  - Lap siding
  - Stucco (with appropriate sheathing/backing)
  These choices significantly change the assemblies and pricing.

- **Change requested:**
  - Add a dropdown to the GUI:
    - Label: "Exterior Finish"
    - Options (strings):
      - `metal_29ga` (default)
      - `metal_26ga`
      - `lap_siding`
      - `stucco`
  - Add a field to `MaterialInputs`: `exterior_finish_type: str = "metal_29ga"`.
  - In the assemblies layer, route wall-skin quantities through this flag, even if initially only used to:
    - Switch between 29ga vs 26ga metal parts.
    - Leave lap/stucco as future TODOs with placeholder assemblies.

- **Acceptance criteria:**
  1. GUI displays an "Exterior Finish" dropdown with the four options.
  2. `exterior_finish_type` flows correctly into `PoleBarnInputs`.
  3. Wall skin assembly selection can branch on this flag without breaking existing metal-29 behavior.

---

### [16] Insulation type selector for walls and roof (batts, rock wool, rigid, spray foam)

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Assemblies / Pricing

- **Problem:**
  Current insulation handling is too generic. In practice:
  - Walls and roof are often insulated differently.
  - Common types include: standard fiberglass batts, rock wool, rigid board, and spray foam. Each has very different cost and assembly patterns.

- **Change requested:**
  1. In the GUI, add two selectors:
     - "Wall Insulation Type": `none`, `fiberglass_batts`, `rock_wool`, `rigid_board`, `spray_foam`
     - "Roof Insulation Type": `none`, `fiberglass_batts`, `rock_wool`, `rigid_board`, `spray_foam`
  2. Add fields to `MaterialInputs`:
     - `wall_insulation_type: str = "none"`
     - `roof_insulation_type: str = "none"`
  3. Assemblies layer:
     - Use these fields to create separate insulation assemblies for walls vs roof, even if initial logic is simple (e.g. SF × type).
     - Map to appropriate parts in `parts/pricing/assemblies` so each type is priced differently.

- **Acceptance criteria:**
  1. GUI exposes separate insulation choices for walls and roof.
  2. Setting wall/roof insulation to something other than `none` produces visible insulation line items with distinct costs for each type.
  3. Turning insulation off (`none`) zeroes those quantities and costs cleanly.

---

### [17] Roll-up / overhead door type selector

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Assemblies / Pricing

- **Problem:**
  Door counts are tracked but door TYPE is not. Roll-up/overhead doors have very different cost and sometimes framing/trim assumptions vs swing or slider doors.

- **Change requested:**
  - Add a selector for primary large doors:
    - Label: "Overhead / Roll-up Doors"
    - Fields:
      - `overhead_door_count` (integer, default 0)
      - `overhead_door_type` dropdown (e.g. `steel_rollup`, `sectional`, `none`)
  - For now we can treat all overhead doors as a single size category or apply a standard cost per door.
  - Assemblies:
    - Introduce an `overhead_door` assembly driven by `overhead_door_count`.
    - Map to appropriate parts in the pricing CSVs.

- **Acceptance criteria:**
  1. GUI allows specifying how many roll-up/overhead doors there are.
  2. Material takeoff includes an overhead-door assembly quantity based on that count.
  3. Priced output shows a distinct "Overhead / Roll-up Door" line item.

---

### [18] MEP (Mechanical, Electrical, Plumbing) allowance toggles

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Pricing / Scope definition

- **Problem:**
  The current calculator completely ignores MEP. In reality:
  - Basic electrical and lighting are often code-required.
  - Plumbing and mechanical systems (heaters, bathroom groups, welders, etc.) can heavily affect scope and pricing. Even if we don't fully engineer MEP, we need at least:
    - Scope flags showing what's included.
    - Allowance-level pricing buckets for MEP.

- **Change requested:**
  1. Add simple scope toggles in the GUI:
     - Electrical:
       - Checkbox: "Include basic electrical" (lights / outlets per code)
       - Optional numeric: "Electrical allowance ($)" (default 0 or a configurable standard)
     - Plumbing:
       - Checkbox: "Include plumbing"
       - Optional numeric: "Plumbing allowance ($)"
     - Mechanical:
       - Checkbox: "Include mechanical (heat/vent)"
       - Optional numeric: "Mechanical allowance ($)"
  2. Add fields to `PricingInputs`:
     - `include_electrical: bool`
     - `electrical_allowance: float`
     - `include_plumbing: bool`
     - `plumbing_allowance: float`
     - `include_mechanical: bool`
     - `mechanical_allowance: float`
  3. Pricing:
     - Treat these as **allowance buckets** added on top of building shell costs.
     - Show them as separate line items in the priced summary (e.g., "Electrical allowance", etc.).

- **Acceptance criteria:**
  1. GUI clearly shows on/off toggles for Electrical, Plumbing, Mechanical, each with an associated allowance field.
  2. When a toggle is on and the allowance is > 0, a corresponding line item appears in the priced output.
  3. Turning a toggle off or setting allowance to 0 removes that cost.
  4. MEP allowances are included in the grand total but remain visually distinct so they're easy to adjust during budgeting.

---

### [19] Post type selector (PT solid vs laminated)

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Assemblies

- **Problem:**
  The engineer form specifies post type (PT Hem-Fir solid vs laminated). This affects:
  - Material cost
  - Structural capacity
  - Availability and lead times

- **Change requested:**
  Add a dropdown to the GUI:
  - Label: "Post Type"
  - Options:
    - `pt_solid` (default) - Pressure-treated solid posts
    - `laminated` - Laminated posts
  - Add field to `AssemblyInputs`: `post_type: str = "pt_solid"`

- **Implementation notes:**
  - Store value in input models
  - For now, informational only
  - Future: Use to select different part IDs and pricing for solid vs laminated posts

- **Acceptance criteria:**
  1. GUI displays post type selector
  2. Default is `pt_solid`
  3. Value stored in `AssemblyInputs`
  4. Value passed through to calculator
  5. No breaking changes to existing calculations

---

### [20] Truss/post connection type selector

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Assemblies

- **Problem:**
  The engineer form specifies truss/post connection type (notched vs cleated). This affects:
  - Fastener quantities
  - Labor hours
  - Additional framing lumber (for cleated connections)
  - Structural behavior

- **Change requested:**
  Add a dropdown to the GUI:
  - Label: "Truss/Post Connection"
  - Options:
    - `notched` (default) - Trusses sit in notches cut into posts
    - `cleated` - Trusses attached with metal cleats/brackets
  - Add field to `AssemblyInputs`: `post_truss_connection_type: str = "notched"`

- **Implementation notes:**
  - Store value in input models
  - For now, informational only
  - Future: Use to adjust fastener quantities and labor hours in assemblies
  - Future: Cleated connections may require additional lumber for blocking

- **Acceptance criteria:**
  1. GUI displays connection type selector
  2. Default is `notched`
  3. Value stored in `AssemblyInputs`
  4. Value passed through to calculator
  5. No breaking changes to existing calculations

---

### [21] Multiple door sizes and types (future enhancement)

- **Area:** GUI / Inputs / Geometry / Assemblies

- **Problem:**
  Current implementation only tracks door count. The engineer form supports:
  - Multiple door sizes (width × height)
  - Multiple door types (overhead, walk, barn, slider)
  - Different quantities per size/type
  This is needed for accurate framing and trim calculations.

- **Change requested:**
  **Note:** This is a future enhancement, not for immediate implementation. Log for Phase 2.
  
  Add support for multiple door entries:
  - Table/list interface in GUI with rows for each door
  - Each row: door type, width, height, quantity
  - Door types: `overhead`, `walk`, `barn`, `slider`
  - Update `GeometryInputs` to support list of door specifications instead of single count

- **Implementation notes:**
  - Defer to Phase 2 after core functionality is stable
  - Will require refactoring door/window handling in assemblies
  - Will enable more accurate framing and trim calculations per opening size

- **Acceptance criteria:**
  - Documented for future implementation
  - No immediate changes required

---

### [22] Lean-to / shed module support (future enhancement)

- **Area:** GUI / Inputs / Geometry / Assemblies

- **Problem:**
  The engineer form allows separate lean-to/shed geometry with:
  - Separate dimensions (length, width)
  - Different bay spacing
  - Different pitch
  - Enclosed toggle
  - Separate slab, sheathing, insulation options
  This is a complex feature that requires separate geometry calculations.

- **Change requested:**
  **Note:** This is a Phase 2 feature, not for immediate implementation.
  
  Add support for optional lean-to/shed:
  - Toggle: "Include lean-to / shed"
  - When enabled, show additional input section:
    - Lean-to dimensions (length, width)
    - Bay spacing
    - Roof pitch
    - Enclosed yes/no
    - Slab yes/no
    - Sheathing options
    - Insulation options
  - Calculate lean-to quantities separately and add to main building totals

- **Implementation notes:**
  - Defer to Phase 2
  - Will require separate geometry model for lean-to
  - Will need to merge quantities from main building + lean-to
  - Complex feature - best implemented after core is stable

- **Acceptance criteria:**
  - Documented for future implementation
  - No immediate changes required

---

### [23] Exterior man door sizing assumptions & options

- **Area:** Assemblies / Doors / Future GUI enhancement

- **Problem:**

  Right now, all "man doors" are treated as generic openings. For assemblies and framing/trim, we need:

  - A clear default assumed size for "standard" man doors.

  - A set of *allowed* exterior door sizes so framing/trim can be accurately calculated when we later support per-door sizing.

- **Change requested:**

  1. **Assumed default size (for current logic):**

     - All man doors are assumed to be **3/0 x 6/8** (36" wide x 80" tall) unless a more detailed door-sizing UI is implemented.

  2. **Allowed exterior door sizes (for future use):**

     - Heights allowed: **6/8, 7/0, 8/0**

     - Widths allowed: **2/10, 3/0, 5/0, 6/0**

  3. Document this in:

     - `ASSEMBLIES_DESIGN.md` (door assemblies section)

     - A comment in the door assembly logic noting that current framing/trim math assumes 3/0 x 6/8 for now.

- **Acceptance criteria:**

  1. Door assemblies clearly document that all man doors are treated as 3/0 x 6/8 for the moment.

  2. The allowed size list is captured in design docs for future UI/logic expansion (multiple door sizes).

---

### [24] Interior build-out framing (bathroom, office, mezzanine)

- **Area:** GUI / Assemblies / Interior framing

- **Problem:**

  The current estimator only covers the shell. Real projects often include interior framing for:

  - Bathrooms

  - Offices

  - Mezzanines / lofts

  These add studs, plates, sheathing, and sometimes floor framing that should be represented as assemblies.

- **Change requested:**

  1. Add an **"Interior Build-Out"** section in the GUI with:

     - Checkbox: "Include bathroom framing" + integer "Number of bathrooms"

     - Checkbox: "Include office framing" + numeric "Office area (sq ft)"

     - Checkbox: "Include mezzanine/loft" + numeric "Mezzanine area (sq ft)"

  2. In `ASSEMBLIES_DESIGN.md`, define simple rules of thumb for:

     - Bathroom framing LF/BF per bathroom (e.g., wall LF per bathroom based on a standard footprint).

     - Office framing based on office area (e.g., wall LF per sq ft).

     - Mezzanine framing: joists + beams + posts per sq ft or per bay.

  3. Add new interior framing assemblies:

     - `bathroom_framing`

     - `office_framing`

     - `mezzanine_framing`

     mapped to parts and pricing (even if initial numbers are rough).

- **Acceptance criteria:**

  1. GUI exposes the interior build-out questions.

  2. Material takeoff includes separate line items for interior framing when enabled.

  3. Assumptions for LF/BF per bathroom/office/sq ft are documented in `ASSEMBLIES_DESIGN.md`.

---

### [25] Roof pitch input simplification (integer → X/12)

- **Area:** GUI / CLI / Geometry

- **Problem:**

  The current UI accepts a flexible roof pitch string (`4/12`, `0.333`, etc.), but in real use the user is only going to enter the "X" in "X/12" (e.g., 2, 3, 4). Allowing arbitrary formats complicates the UI and error handling.

- **Change requested:**

  1. **GUI:**

     - Replace the free-form pitch field with an **integer-only input** or dropdown for `Roof Pitch (X in X/12)`.

     - Valid values (for now): **1–12**.

     - Internal numeric ratio = `pitch_integer / 12.0`.

  2. **CLI:**

     - Keep the flexible parser for backward compatibility (accepts `4/12`, `0.333`, `4`).

     - But document that the **recommended** CLI usage is to pass simple integers representing X for X/12.

  3. **Validation:**

     - Reject 0 or negative pitches in GUI.

     - Show a friendly error if the pitch is outside 1–12.

- **Acceptance criteria:**

  1. GUI only allows roof pitch as an integer X representing X/12.

  2. Internally, the derived numeric ratio is used consistently in geometry.

  3. CLI continues to work for existing patterns but encourages integer X.

---

### [26] MEP allowances scaled from building size & door count

- **Area:** Pricing / MEP / Defaults

- **Problem:**

  Current MEP allowances are flat numbers the user types in. A better estimator starts with **reasonable default allowances** based on building size and basic features, then allows user override.

- **Change requested:**

  1. Define simple default formulas for allowances based on:

     - Building footprint (length × width)

     - Number of exterior man doors

     - Possibly number of overhead doors

  2. Examples (to be refined and documented in `ASSEMBLIES_DESIGN.md` or a new `MEP_DEFAULTS.md`):

     - Electrical:

       - Base outlets/lighting per X sq ft + one exterior light per man door.

       - Convert that to a rough dollar allowance using assumed fixture and labor costs.

     - Plumbing:

       - Base allowance per bathroom count.

     - Mechanical:

       - Base allowance per sq ft and climate assumption.

  3. Implementation behavior:

     - If the user **leaves MEP allowance fields blank or zero**, compute defaults from size & door counts.

     - If the user enters a non-zero allowance, treat that as an override.

  4. (Optional future) Provide a breakdown in the summary: "Based on size, we assumed N outlets, M lights, L ft of wire", even if pricing is still through a single allowance bucket.

- **Acceptance criteria:**

  1. For a blank MEP allowance, the estimator produces non-zero MEP allowances derived from building size/door count.

  2. User-entered allowances override the defaults.

  3. Default formulas and assumptions are documented.

---

### [27] Convert areas (sq ft) to real purchasable parts (panels & sheets)

- **Area:** Assemblies / Parts / Config

- **Problem:**

  The material list currently uses square footage for roof panels, wall panels, and sheathing. In practice, material is ordered in:

  - Metal panels with a fixed coverage width (e.g., 36" coverage).

  - Sheathing sheets (e.g., 4x8, 4x10).

  Estimator users need counts of actual pieces, not just sq ft.

- **Change requested:**

  1. Introduce **coverage dimensions** for panel and sheet products in config:

     - For each relevant `part_id` in `parts/pricing` (metal panels, OSB, plywood), add fields for:

       - `coverage_width_in` and `coverage_height_in` OR a normalized "coverage area per piece" and "orientation rule".

     - If schema change is too disruptive, document the assumed coverage sizes in `ASSEMBLIES_DESIGN.md` and hard-code them in the assemblies logic initially.

  2. Update assemblies logic so that for:

     - Wall metal:

       - Compute number of vertical sheets per wall: `ceil(wall_length_ft * 12 / coverage_width_in)`.

       - Panel length per sheet derived from wall height (plus overhang/trim assumptions).

     - Roof metal:

       - Compute number of sheets per slope based on horizontal run and coverage width.

     - Sheathing (walls/roof):

       - Convert required sq ft into counts of 4x8 (or other) sheets: `ceil(area_sqft / sheet_coverage_sqft)`.

  3. Maintain sq ft in the summary for reference, but make **the priced quantity be the count of pieces (EA)**.

- **Acceptance criteria:**

  1. Material takeoff includes:

     - "Metal roof panels" as a count of panels (EA), not just sq ft.

     - "Metal wall panels" as a count of panels (EA).

     - Sheathing as "X sheets" of OSB/plywood.

  2. Pricing is based on the piece counts.

  3. Basic coverage assumptions (e.g., 36" metal, 4x8 sheets) are documented in design docs and/or config.

---

### [28] Material list export system (Excel with category tabs)

- **Area:** Export / Material List / Output

- **Problem:**

  The current estimator shows material quantities in the UI, but there is no way to export a **shopping list** that can be edited and sent to suppliers. The material list needs to be:

  - A separate, editable file (not just on-screen display)

  - Organized by category (Framing, Doors_Windows, Metal, Insulation, Concrete, MEP, Misc)

  - Human-readable and vendor-ready

  - Editable by the user before sending to suppliers

- **Change requested:**

  1. **Export format:**

     - Primary export: Excel file (`material_list.xlsx`)

     - Inside workbook, create separate tabs:

       - `Framing` (posts, studs, beams, plates, girts, purlins)

       - `Doors_Windows` (man doors, overhead doors, windows, trim)

       - `Metal` (roof panels, wall panels, trim, fasteners)

       - `Insulation` (batts, rigid, spray foam, etc.)

       - `Concrete` (concrete, rebar, mesh)

       - `MEP` (electrical, plumbing, mechanical allowances/parts)

       - `Misc` (anything else)

  2. **Column schema per row:**

     - `category` (Framing / Metal / Insulation / etc.)

     - `sub_category` (e.g., "wall girts", "roof purlins", "door trim")

     - `part_id` (matches `parts.example.csv`)

     - `part_name` (short human name)

     - `description` (longer vendor-readable description)

     - `unit` (LF, EA, SQFT, SHEET, etc.)

     - `qty` (count/length required)

     - `unit_price` (from pricing library)

     - `ext_price` (qty × unit_price)

     - `vendor` (optional default from parts.csv)

     - `notes` (color, gauge, location, size assumptions, etc.)

  3. **Export functionality:**

     - Add "Export Material List" button to GUI

     - Generate Excel file with all tabs populated

     - File should be saved to a user-specified location (or default to project directory)

     - File should be named with project name/timestamp if available

- **Acceptance criteria:**

  1. Clicking "Export Material List" generates a valid Excel file.

  2. Excel file contains all expected category tabs.

  3. Each tab contains only parts from that category.

  4. All columns are populated correctly.

  5. File can be opened and edited in Excel.

  6. All `part_id`s in the export match entries in `parts.example.csv`.

---

### [29] Category mapping column in parts.csv

- **Area:** Config / Parts / Export

- **Problem:**

  To organize the material list export into category tabs, we need to know which category each part belongs to. Currently, parts have a `category` field, but it may not align with the export categories we want (Framing, Doors_Windows, Metal, etc.).

- **Change requested:**

  1. Add a new column to `parts.example.csv`:

     - Column name: `export_category`

     - Values: `Framing`, `Doors_Windows`, `Metal`, `Insulation`, `Concrete`, `MEP`, `Misc`

  2. **Mapping rules:**

     - Posts, studs, beams, plates, girts, purlins → `Framing`

     - Man doors, overhead doors, windows, door/window trim → `Doors_Windows`

     - Roof panels, wall panels, metal trim, fasteners → `Metal`

     - Batts, rigid board, spray foam → `Insulation`

     - Concrete, rebar, mesh → `Concrete`

     - Electrical allowance, plumbing allowance, mechanical allowance, panels, fixtures → `MEP`

     - Anything else → `Misc`

  3. Populate `export_category` for all existing parts in `parts.example.csv`.

  4. Update the material list export logic to use `export_category` from parts.csv to determine which tab each part goes into.

- **Acceptance criteria:**

  1. `parts.example.csv` has an `export_category` column.

  2. All existing parts have a valid `export_category` value.

  3. Material list export uses `export_category` to organize parts into tabs.

  4. No parts are missing from the export due to missing category.

---

### [30] Material export must use pricing library only (no loose prices)

- **Area:** Export / Pricing / Data integrity

- **Problem:**

  To maintain data integrity and ensure the material list is always accurate, all prices must come from the same source (the pricing library). We cannot allow ad-hoc prices or hard-coded values that don't match the parts/pricing CSVs.

- **Change requested:**

  1. **Enforcement rule:**

     - Every row in the material list export MUST have a valid `part_id` that exists in `parts.example.csv`.

     - Every `unit_price` MUST come from `pricing.example.csv` (looked up by `part_id` and pricing profile).

     - No hard-coded prices or "mystery items" are allowed in the export.

  2. **Validation:**

     - Before generating the export, validate that:

       - All `part_id`s in the takeoff exist in `parts.example.csv`.

       - All `part_id`s have a corresponding price in `pricing.example.csv` for the active pricing profile.

     - If validation fails:

       - Log a warning with the missing `part_id`s.

       - Still generate the export, but mark missing prices as `0.00` or `TBD` with a note.

  3. **Code structure:**

     - The material list export function should:

       - Take `PricedLineItem[]` as input (which already has `part_id` and `unit_price` from the pricing library).

       - Map each item to the export schema.

       - Never inject prices from anywhere other than the `PricedLineItem` data.

  4. **Documentation:**

     - Add a comment/rule in the export code:

       > "Material list export is generated exclusively from the same `part_id`s and `unit_price`s defined in `parts.example.csv` and `pricing.example.csv`. No ad-hoc prices allowed."

- **Acceptance criteria:**

  1. Material list export contains only `part_id`s that exist in `parts.example.csv`.

  2. All `unit_price` values in the export match values from `pricing.example.csv`.

  3. If a part is missing from pricing, it appears in the export with `unit_price = 0.00` and a note indicating it needs pricing.

  4. No hard-coded prices appear in the export code.

---

### [31] Panel and sheet coverage assumptions (baseline standards)

- **Area:** Assemblies / Config / Material calculations

- **Problem:**

  To convert area-based quantities (sq ft) into purchasable parts (panels, sheets), we need standard coverage assumptions. Without these, we can't generate accurate piece counts for ordering.

- **Change requested:**

  1. **Standard coverage assumptions (hard-coded or config):**

     - **Metal wall panels (29ga and 26ga):**

       - Coverage width: **36 inches** (standard)

       - Orientation: Vertical (panels run vertically up the wall)

       - Note: Some panels are 16", 24", or other widths, but 36" is the baseline assumption.

     - **Metal roof panels:**

       - Coverage width: **36 inches** (standard)

       - Orientation: Horizontal (panels run horizontally along the roof slope)

     - **OSB / Plywood sheathing:**

       - Sheet size: **4x8 feet** (48" × 96" = 32 sq ft per sheet)

       - Alternative sizes (4x10, etc.) can be added later, but 4x8 is the baseline.

  2. **Documentation:**

     - Document these assumptions in `ASSEMBLIES_DESIGN.md`:

       - "Standard metal panels = 36" coverage width unless otherwise specified."

       - "Standard sheathing = 4x8 sheets (32 sq ft) unless otherwise specified."

  3. **Calculation logic:**

     - Wall metal:

       - Number of vertical sheets per wall = `ceil(wall_length_ft * 12 / 36)`

       - Panel length per sheet = wall height + overhang (if applicable)

     - Roof metal:

       - Number of sheets per slope = based on horizontal run × coverage width

       - Panel length per sheet = roof slope length

     - Sheathing:

       - Number of sheets = `ceil(area_sqft / 32.0)` (for 4x8 sheets)

  4. **Future flexibility:**

     - These assumptions can later be moved to config or parts.csv if needed.

     - For now, hard-coding is acceptable to establish the baseline.

- **Acceptance criteria:**

  1. Assemblies logic uses 36" coverage for metal panels.

  2. Assemblies logic uses 4x8 (32 sq ft) for sheathing sheets.

  3. Material takeoff shows panel/sheet counts (EA), not just sq ft.

  4. Assumptions are documented in `ASSEMBLIES_DESIGN.md`.

---

### [32] UI display vs export separation (summary vs full list)

- **Area:** GUI / Display / User experience

- **Problem:**

  The current UI may show too much detail in the results pane. Clients don't need to see every stud and screw—they need high-level totals for comparison. The full material list should be a separate export, not cluttering the on-screen summary.

- **Change requested:**

  1. **UI Results Pane (on-screen summary):**

     - Show per-category totals only:

       - "Framing: $X,XXX ($X.XX/sqft)"

       - "Metal: $X,XXX ($X.XX/sqft)"

       - "Insulation: $X,XXX ($X.XX/sqft)"

       - "Concrete: $X,XXX ($X.XX/sqft)"

       - "MEP: $X,XXX ($X.XX/sqft)"

       - "Misc: $X,XXX ($X.XX/sqft)"

     - Show grand total and cost per sq ft.

     - Remove or minimize the detailed line-item list (or move it to a collapsible section).

  2. **Export Button:**

     - Add a prominent "Export Material List" button in the results pane.

     - Button generates the Excel file with full detail (per entry [28]).

     - Button label: "Download Shopping List" or "Export Material List"

  3. **Separation of concerns:**

     - UI = high-level summary for client presentation and apples-to-apples comparison.

     - Export = detailed shopping list for ordering and supplier communication.

- **Acceptance criteria:**

  1. UI results pane shows category totals with $/sqft, not individual parts.

  2. "Export Material List" button is visible and functional.

  3. Export file contains full detail (all parts, all columns).

  4. UI remains clean and focused on totals.

---

### [33] MEP default formulas based on building size and features

- **Area:** Pricing / MEP / Defaults

- **Problem:**

  Entry [26] requested MEP allowances scaled from building size, but we need to define the actual formulas and rules of thumb. Without concrete formulas, the estimator can't compute reasonable defaults.

- **Change requested:**

  1. **Define default formulas (to be documented in `MEP_DEFAULTS.md` or `ASSEMBLIES_DESIGN.md`):**

     - **Electrical:**

       - Base outlets: Assume 1 outlet per 100 sq ft of floor area (minimum 4 outlets).

       - Base lighting: Assume 1 light fixture per 200 sq ft of floor area (minimum 2 lights).

       - Exterior lights: 1 exterior light per man door.

       - Overhead door circuits: 1 circuit per overhead door (for opener).

       - Wire: Estimate based on outlet/light count and building dimensions (rough rule: 10 LF of wire per outlet/light).

       - Convert to dollar allowance: Use assumed fixture costs ($50/light, $20/outlet, $2/LF wire, $100/panel, labor at configured rate).

     - **Plumbing:**

       - Base allowance per bathroom: $2,000 per bathroom (includes rough-in, fixtures, labor).

       - If no bathrooms specified: $0 (no plumbing).

     - **Mechanical:**

       - Base allowance: $2.00 per sq ft of floor area (for basic heating/ventilation).

       - Minimum: $500.

  2. **Implementation behavior:**

     - If MEP allowance fields are blank or zero in GUI, compute defaults using these formulas.

     - If user enters a non-zero allowance, use that as an override (ignore defaults).

     - Show a breakdown in the export notes: "Based on X sqft, Y doors, Z bathrooms, we assumed..."

  3. **Documentation:**

     - Create `MEP_DEFAULTS.md` with:

       - All formulas

       - Assumed unit costs

       - Rationale/notes

       - Future refinement guidance

- **Acceptance criteria:**

  1. For a 40×30 building with 3 doors and 1 bathroom:

     - Electrical default is computed (not zero).

     - Plumbing default = $2,000.

     - Mechanical default is computed based on sq ft.

  2. User-entered allowances override defaults.

  3. Formulas are documented in `MEP_DEFAULTS.md`.

  4. Export notes include breakdown of assumptions.
