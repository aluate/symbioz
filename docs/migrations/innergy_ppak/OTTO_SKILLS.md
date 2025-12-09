# Otto Skills for PPak-INNERGY Migration

**Purpose:** Define Otto skills for orchestrating the PPak → INNERGY migration  
**Status:** Ready for Implementation  
**Last Updated:** January 2025

---

## Overview

Otto can orchestrate the complete migration cycle by calling the CLI scripts we've built. Each skill wraps a Python CLI command and provides structured input/output for Otto's task system.

---

## Skill Definitions

### 1. `run_ppak_export_etl`

**Description:** Transform PPak export files into canonical format.

**Command:** `python -m integrations.ppak.etl.run_migration`

**Parameters:**
- `ppak_export_dir` (string, required): Directory containing PPak CSV exports
- `output_dir` (string, required): Directory for canonical output files
- `date_range` (string, optional): Filter by date range (format: "YYYY-MM-DD,YYYY-MM-DD")
- `mappings_dir` (string, optional): Directory with mapping CSV files (default: `integrations/canonical/mappings`)

**Returns:**
- `summary_report_path` (string): Path to migration summary markdown file
- `projects_count` (integer): Number of projects processed
- `materials_count` (integer): Number of materials processed
- `errors_count` (integer): Number of errors/warnings
- `canonical_projects_file` (string): Path to canonical projects JSON
- `canonical_materials_file` (string): Path to canonical materials JSON

**Example Otto Task:**
```json
{
  "task_type": "migration.run_ppak_etl",
  "parameters": {
    "ppak_export_dir": "./data/ppak_exports",
    "output_dir": "./data/migration_output",
    "date_range": "2024-01-01,2024-12-31"
  }
}
```

**Otto Implementation:**
```python
# Otto would call:
result = subprocess.run([
    "python", "-m", "integrations.ppak.etl.run_migration",
    "--ppak-export-dir", params["ppak_export_dir"],
    "--output-dir", params["output_dir"],
    "--date-range", params.get("date_range", "")
], capture_output=True, text=True)

# Parse output for summary stats
# Return structured result
```

---

### 2. `sync_innergy_material_library`

**Description:** Sync canonical material library to INNERGY (computes diff and syncs changes).

**Command:** `python -m integrations.innergy.sync_materials`

**Parameters:**
- `material_library` (string, required): Path to canonical material library file (JSON or CSV)
- `api_key` (string, optional): INNERGY API key (or use `INNERGY_API_KEY` env var)
- `api_url` (string, optional): INNERGY API base URL (or use `INNERGY_API_BASE_URL` env var)
- `dry_run` (boolean, default: true): If true, only report changes without applying them

**Returns:**
- `new_materials_count` (integer): Number of new materials to create
- `updated_materials_count` (integer): Number of materials to update
- `inactive_materials_count` (integer): Number of materials to deactivate
- `sync_summary` (string): Human-readable summary
- `success` (boolean): Whether sync completed successfully

**Example Otto Task:**
```json
{
  "task_type": "migration.sync_materials",
  "parameters": {
    "material_library": "./data/material_library_master.csv",
    "dry_run": true
  }
}
```

**Safety Note:** Always runs in dry-run mode by default. Otto should require explicit confirmation before running with `dry_run: false`.

---

### 3. `run_innergy_project_import`

**Description:** Import canonical projects into INNERGY.

**Command:** `python -m integrations.innergy.import_projects`

**Parameters:**
- `canonical_file` (string, required): Path to canonical projects JSON file
- `api_key` (string, optional): INNERGY API key (or use `INNERGY_API_KEY` env var)
- `api_url` (string, optional): INNERGY API base URL (or use `INNERGY_API_BASE_URL` env var)
- `dry_run` (boolean, default: true): If true, only validate without importing
- `update_canonical` (boolean, default: false): If true, update canonical file with `innergy_id` values after import

**Returns:**
- `created_count` (integer): Number of projects created
- `updated_count` (integer): Number of projects updated
- `failed_count` (integer): Number of projects that failed to import
- `errors` (array of strings): List of error messages
- `import_summary` (string): Human-readable summary
- `success` (boolean): Whether import completed successfully

**Example Otto Task:**
```json
{
  "task_type": "migration.import_projects",
  "parameters": {
    "canonical_file": "./data/migration_output/canonical_projects_2024-01-15.json",
    "dry_run": true,
    "update_canonical": true
  }
}
```

**Safety Note:** Always runs in dry-run mode by default. Otto should require explicit confirmation before running with `dry_run: false`.

---

### 4. `migration_health_check`

**Description:** Validate migration and check for issues.

**Command:** `python -m integrations.canonical.health_check`

**Parameters:**
- `canonical_file` (string, required): Path to canonical projects JSON file
- `innergy_api_url` (string, optional): INNERGY API base URL (for validation)
- `innergy_api_key` (string, optional): INNERGY API key (for validation)

**Returns:**
- `health_check_report_path` (string): Path to health check markdown report
- `projects_missing_innergy_id` (integer): Count of projects without `innergy_id`
- `materials_not_found` (integer): Count of materials referenced but not in INNERGY
- `unmapped_statuses` (array of strings): List of unmapped status values
- `unmapped_phases` (array of strings): List of unmapped phase values
- `data_quality_issues` (array of strings): List of data quality problems
- `overall_health` (string): "healthy", "warnings", or "errors"

**Example Otto Task:**
```json
{
  "task_type": "migration.health_check",
  "parameters": {
    "canonical_file": "./data/migration_output/canonical_projects_2024-01-15.json"
  }
}
```

---

### 5. `run_full_migration_cycle`

**Description:** Orchestrate a complete migration cycle (ETL → Sync Materials → Import Projects → Health Check).

**This is a composite skill that calls other skills in sequence.**

**Parameters:**
- `ppak_export_dir` (string, required): Directory with PPak exports
- `output_dir` (string, required): Directory for canonical output
- `material_library` (string, required): Path to canonical material library
- `date_range` (string, optional): Filter by date range
- `dry_run` (boolean, default: true): Run in dry-run mode
- `skip_material_sync` (boolean, default: false): Skip material sync step
- `skip_health_check` (boolean, default: false): Skip health check step

**Returns:**
- `etl_result` (object): Result from `run_ppak_export_etl`
- `material_sync_result` (object): Result from `sync_innergy_material_library` (if not skipped)
- `import_result` (object): Result from `run_innergy_project_import`
- `health_check_result` (object): Result from `migration_health_check` (if not skipped)
- `overall_success` (boolean): Whether entire cycle completed successfully
- `cycle_summary` (string): Human-readable summary of entire cycle

**Example Otto Task:**
```json
{
  "task_type": "migration.run_full_cycle",
  "parameters": {
    "ppak_export_dir": "./data/ppak_exports",
    "output_dir": "./data/migration_output",
    "material_library": "./data/material_library_master.csv",
    "date_range": "2024-01-01,2024-12-31",
    "dry_run": true
  }
}
```

**Otto Implementation:**
```python
# Otto would:
# 1. Call run_ppak_export_etl
etl_result = call_skill("migration.run_ppak_etl", {...})

# 2. Call sync_innergy_material_library (if not skipped)
if not params.get("skip_material_sync"):
    sync_result = call_skill("migration.sync_materials", {...})

# 3. Call run_innergy_project_import
import_result = call_skill("migration.import_projects", {
    "canonical_file": etl_result["canonical_projects_file"],
    ...
})

# 4. Call migration_health_check (if not skipped)
if not params.get("skip_health_check"):
    health_result = call_skill("migration.health_check", {...})

# 5. Combine results and return
```

---

## Otto Integration Points

### Environment Variables

Otto should have access to these environment variables (or read from `.env` file):

- `INNERGY_API_KEY`: INNERGY API key
- `INNERGY_API_BASE_URL`: INNERGY API base URL (from OpenAPI spec)
- `PPAK_EXPORT_DIR`: Default directory for PPak exports
- `MIGRATION_OUTPUT_DIR`: Default directory for canonical output
- `MATERIAL_LIBRARY_MASTER`: Default path to canonical material library

### Directory Structure

Otto expects this directory structure:

```
data/
├── ppak_exports/          # PPak CSV files go here
├── migration_output/      # Canonical files written here
└── material_library_master.csv  # Canonical material library
```

### Error Handling

All skills should:
- Return structured error information
- Log detailed errors to files
- Never crash Otto (catch all exceptions)
- Provide human-readable error messages

### Dry-Run Safety

**Critical:** All write operations (material sync, project import) default to `dry_run: true`. Otto should:
- Always show what would happen in dry-run mode
- Require explicit confirmation before running with `dry_run: false`
- Log all operations (dry-run and real)

---

## Example: Complete Migration Workflow

### Step 1: Human exports PPak data

Human action: Export projects and materials from PPak, save to `data/ppak_exports/`.

### Step 2: Otto runs ETL

```bash
# Otto task
{
  "task_type": "migration.run_ppak_etl",
  "parameters": {
    "ppak_export_dir": "./data/ppak_exports",
    "output_dir": "./data/migration_output"
  }
}
```

Otto calls: `python -m integrations.ppak.etl.run_migration --ppak-export-dir ./data/ppak_exports --output-dir ./data/migration_output`

Result: Canonical files created in `data/migration_output/`.

### Step 3: Otto syncs materials (dry-run)

```bash
# Otto task
{
  "task_type": "migration.sync_materials",
  "parameters": {
    "material_library": "./data/material_library_master.csv",
    "dry_run": true
  }
}
```

Otto reports: "Would create 15 new materials, update 3 materials, deactivate 2 materials."

### Step 4: Human reviews and approves

Human reviews dry-run results, then tells Otto: "Go ahead with material sync."

### Step 5: Otto syncs materials (live)

```bash
# Otto task
{
  "task_type": "migration.sync_materials",
  "parameters": {
    "material_library": "./data/material_library_master.csv",
    "dry_run": false
  }
}
```

### Step 6: Otto imports projects (dry-run)

```bash
# Otto task
{
  "task_type": "migration.import_projects",
  "parameters": {
    "canonical_file": "./data/migration_output/canonical_projects_2024-01-15.json",
    "dry_run": true
  }
}
```

### Step 7: Human reviews and approves

Human reviews dry-run results, then tells Otto: "Go ahead with project import."

### Step 8: Otto imports projects (live)

```bash
# Otto task
{
  "task_type": "migration.import_projects",
  "parameters": {
    "canonical_file": "./data/migration_output/canonical_projects_2024-01-15.json",
    "dry_run": false,
    "update_canonical": true
  }
}
```

### Step 9: Otto runs health check

```bash
# Otto task
{
  "task_type": "migration.health_check",
  "parameters": {
    "canonical_file": "./data/migration_output/canonical_projects_2024-01-15.json"
  }
}
```

Otto reports: Health check results, any issues found.

---

## Next Steps

1. **Implement Otto skill handlers** that wrap these CLI commands
2. **Add skill definitions to Otto's skill registry** (wherever that lives in your Otto setup)
3. **Test each skill individually** with dry-run mode
4. **Test full migration cycle** with a small sample dataset
5. **Document any Otto-specific configuration** needed

---

## Notes for Otto Developers

- All Python scripts are in `integrations/` directory
- Scripts use `argparse` for CLI arguments
- Scripts write logs to stdout/stderr (Otto can capture these)
- Scripts return exit codes: 0 = success, non-zero = failure
- All scripts support environment variables for configuration
- Scripts are designed to be non-interactive (Otto-friendly)

