# Migration Process Runbook

**Purpose:** Step-by-step guide for running a migration cycle from PPak to INNERGY  
**Audience:** Human operators and automation agent (Otto)  
**Last Updated:** January 2025

---

## Overview

This runbook describes how to execute a complete migration cycle:

1. **Extract** – Get PPak export files
2. **Transform** – Convert PPak data to canonical format
3. **Load** – Import canonical data into INNERGY
4. **Validate** – Run health checks and verify migration

The process is designed to be **repeatable** and **Otto-friendly** (non-interactive CLI commands).

---

## Prerequisites

### Environment Variables

Set the following environment variables (or use `.env` file):

```bash
# INNERGY API Configuration
INNERGY_API_BASE_URL=https://api.innergy.example.com  # From OpenAPI spec
INNERGY_API_KEY=your_api_key_here  # When available

# PPak Export Location
PPAK_EXPORT_DIR=./data/ppak_exports  # Where PPak CSV files are dropped

# Migration Output
MIGRATION_OUTPUT_DIR=./data/migration_output  # Where canonical files are written

# Material Library
MATERIAL_LIBRARY_MASTER=./data/material_library_master.csv  # Canonical material library
```

### Directory Structure

Create the following directories:

```bash
mkdir -p data/ppak_exports
mkdir -p data/migration_output
mkdir -p data/material_library_master
```

### Dependencies

Install Python dependencies:

```bash
pip install -r requirements.txt  # Or use the project's dependency file
```

Required packages:
- `pydantic` – Data validation
- `httpx` – HTTP client for INNERGY API
- `pandas` (optional) – CSV handling
- `python-dotenv` – Environment variable loading

---

## Migration Cycle Steps

### Step 1: Prepare PPak Export Files

**Human Action:** Export data from PPak system.

1. Export projects/jobs from PPak (CSV format)
2. Export materials from PPak (CSV format, if available)
3. Place files in `PPAK_EXPORT_DIR`:
   ```
   data/ppak_exports/
   ├── projects_2024-01-15.csv
   ├── materials_2024-01-15.csv
   └── work_orders_2024-01-15.csv  # If available
   ```

**File Naming Convention:**
- Use date stamps: `{entity}_{YYYY-MM-DD}.csv`
- Keep historical exports for audit trail

---

### Step 2: Run PPak ETL (Transform to Canonical)

**Command:** Run the PPak ETL script to transform exports into canonical format.

```bash
python -m integrations.ppak.etl.run_migration \
  --ppak-export-dir "$PPAK_EXPORT_DIR" \
  --output-dir "$MIGRATION_OUTPUT_DIR" \
  --date-range "2024-01-01,2024-01-31"  # Optional: filter by date
```

**What it does:**
1. Reads all CSV files from `PPAK_EXPORT_DIR`
2. Parses PPak rows using `integrations/ppak/schemas.py`
3. Transforms to `CanonicalProject` / `CanonicalMaterial` using `integrations/ppak/etl/transform.py`
4. Applies mapping tables (`status_mapping.csv`, `phase_mapping.csv`, `material_mapping.csv`)
5. Writes canonical data to `MIGRATION_OUTPUT_DIR`:
   ```
   data/migration_output/
   ├── canonical_projects_2024-01-15.json
   ├── canonical_materials_2024-01-15.json
   └── migration_summary_2024-01-15.md
   ```

**Output:**
- Canonical JSON/CSV files
- Migration summary report (job count, mapping errors, warnings)
- Log file with detailed transformation steps

**Error Handling:**
- Unknown status/phase values → Logged as warnings, use default or skip
- Missing material SKUs → Logged, project still processed
- Invalid dates → Logged, use null or default

---

### Step 3: Sync Material Library (Optional, but Recommended)

**Command:** Sync canonical material library to INNERGY.

```bash
python -m integrations.innergy.sync_materials \
  --material-library "$MATERIAL_LIBRARY_MASTER" \
  --dry-run  # Remove for actual sync
```

**What it does:**
1. Reads canonical material library from `MATERIAL_LIBRARY_MASTER`
2. Fetches current materials from INNERGY API (`GET /api/materials`)
3. Computes diff:
   - **New materials** – Not in INNERGY, need to create
   - **Updated materials** – Changed in canonical, need to update
   - **Inactive materials** – Marked inactive in canonical, deactivate in INNERGY
4. In **dry-run mode**: Reports what would change (no writes)
5. In **real mode**: Creates/updates materials via INNERGY API or CSV import

**Output:**
- Diff report (new/updated/inactive counts)
- Sync summary (success/failure for each material)
- Log file

**When to run:**
- Before importing projects (ensures materials exist)
- After updating `MATERIAL_LIBRARY_MASTER`
- On a schedule (weekly/monthly) to keep INNERGY in sync

---

### Step 4: Import Projects to INNERGY

**Command:** Import canonical projects into INNERGY.

```bash
python -m integrations.innergy.import_projects \
  --canonical-file "$MIGRATION_OUTPUT_DIR/canonical_projects_2024-01-15.json" \
  --dry-run  # Remove for actual import
```

**What it does:**
1. Reads canonical project file
2. Validates each project against INNERGY API requirements
3. In **dry-run mode**: Reports validation results (no writes)
4. In **real mode**:
   - Creates new projects via INNERGY API (`POST /api/projects`)
   - Updates existing projects if `innergy_id` is present (`PUT /api/projects/{id}`)
   - Maps work orders if available
5. Updates canonical file with `innergy_id` values after import

**Output:**
- Import summary (created/updated/skipped counts)
- Per-project results (success/failure with reasons)
- Updated canonical file with `innergy_id` fields
- Log file

**Error Handling:**
- Missing required fields → Skip project, log error
- API errors → Retry with exponential backoff, log failures
- Duplicate projects → Skip or update based on `innergy_id`

---

### Step 5: Run Health Checks

**Command:** Validate the migration and check for issues.

```bash
python -m integrations.canonical.health_check \
  --canonical-file "$MIGRATION_OUTPUT_DIR/canonical_projects_2024-01-15.json" \
  --innergy-api-url "$INNERGY_API_BASE_URL"
```

**What it does:**
1. Reads canonical project file
2. Checks that all projects have `innergy_id` after import
3. Validates that materials referenced in projects exist in INNERGY
4. Checks for unmapped status/phase values
5. Generates health check report

**Output:**
- Health check report (markdown):
  ```
  data/migration_output/
  └── health_check_2024-01-15.md
  ```
- Report includes:
  - Projects missing `innergy_id`
  - Materials not found in INNERGY
  - Unmapped status/phase values
  - Data quality issues

---

## Otto Integration

### How Otto Calls These Scripts

Otto will have skills that wrap these CLI commands:

1. **`run_ppak_export_etl`** skill
   - Calls: `python -m integrations.ppak.etl.run_migration`
   - Parameters: date range, export dir, output dir
   - Returns: Summary report path

2. **`sync_innergy_material_library`** skill
   - Calls: `python -m integrations.innergy.sync_materials`
   - Parameters: material library path, dry-run flag
   - Returns: Sync summary

3. **`run_innergy_project_import`** skill
   - Calls: `python -m integrations.innergy.import_projects`
   - Parameters: canonical file path, dry-run flag
   - Returns: Import summary

4. **`migration_health_check`** skill
   - Calls: `python -m integrations.canonical.health_check`
   - Parameters: canonical file path
   - Returns: Health check report path

### Example Otto Task

```json
{
  "task_type": "migration.run_full_cycle",
  "parameters": {
    "ppak_export_dir": "./data/ppak_exports",
    "date_range": "2024-01-01,2024-01-31",
    "dry_run": false
  }
}
```

Otto would:
1. Call `run_ppak_export_etl` → Get canonical files
2. Call `sync_innergy_material_library` → Ensure materials exist
3. Call `run_innergy_project_import` → Import projects
4. Call `migration_health_check` → Validate results
5. Return combined summary report

---

## Troubleshooting

### Common Issues

**Issue:** "Unknown status value: 'In Progress'"
- **Solution:** Add mapping to `status_mapping.csv`, re-run ETL

**Issue:** "Material SKU 'PP-DOOR-001' not found in canonical library"
- **Solution:** Add material to `MATERIAL_LIBRARY_MASTER`, then sync to INNERGY

**Issue:** "INNERGY API returned 401 Unauthorized"
- **Solution:** Check `INNERGY_API_KEY` environment variable

**Issue:** "Project import failed: Missing required field 'customer_name'"
- **Solution:** Review PPak export, add default value or skip project

**Issue:** "Duplicate project detected"
- **Solution:** Check if project already has `innergy_id`, use update instead of create

### Log Files

All scripts write logs to:
- `logs/ppak_etl_YYYY-MM-DD.log`
- `logs/innergy_sync_YYYY-MM-DD.log`
- `logs/innergy_import_YYYY-MM-DD.log`
- `logs/health_check_YYYY-MM-DD.log`

Review logs for detailed error messages and stack traces.

---

## Best Practices

1. **Always run dry-run first** – Validate before actual writes
2. **Keep historical exports** – Don't delete PPak exports, archive them
3. **Update mapping tables iteratively** – Add mappings as you discover new values
4. **Run health checks after each import** – Catch issues early
5. **Version control canonical files** – Track changes to canonical data
6. **Document data quality issues** – Note any PPak data problems for future reference

---

## Next Steps

After initial setup:
1. ✅ Test with a small PPak export (5-10 projects)
2. ✅ Verify canonical transformation looks correct
3. ✅ Test INNERGY API connection (dry-run)
4. ✅ Import test project and verify in INNERGY UI
5. ✅ Run full migration cycle with Otto

---

## Appendix: Makefile Targets

For convenience, use Makefile targets:

```bash
make ppak-migrate-latest    # Run ETL on latest PPak exports
make innergy-sync-materials # Sync material library
make innergy-import-projects # Import latest canonical projects
make migration-health-check  # Run health checks
```

See `Makefile` in repo root for implementation.

