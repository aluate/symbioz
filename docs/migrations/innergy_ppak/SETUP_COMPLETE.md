# Migration Setup Complete ✅

**Date:** January 2025  
**Status:** Documentation and code skeleton created, ready for iteration

---

## Files Created

### Documentation (`docs/migrations/innergy_ppak/`)

1. ✅ **ROADMAP.md** - High-level migration phases (0-4) with goals, deliverables, and success criteria
2. ✅ **DATA_MODEL.md** - Canonical model definitions (CanonicalProject, CanonicalMaterial) with field descriptions
3. ✅ **PROCESS_RUNBOOK.md** - Step-by-step guide for running migration cycles (human + Otto)

### Canonical Models (`integrations/canonical/`)

4. ✅ **models.py** - Pydantic models for CanonicalProject and CanonicalMaterial
5. ✅ **mappings/status_mapping.csv** - Status mapping table (PPak → Canonical → INNERGY)
6. ✅ **mappings/phase_mapping.csv** - Phase mapping table
7. ✅ **mappings/material_mapping.csv** - Material SKU mapping table
8. ✅ **health_check.py** - Health check script for migration validation

### PPak Integration (`integrations/ppak/`)

9. ✅ **schemas.py** - Pydantic models for PPak export rows (PPakProjectRow, PPakMaterialRow)
10. ✅ **etl/transform.py** - Transformation functions (PPak → Canonical)
11. ✅ **etl/run_migration.py** - CLI entry point for PPak ETL

### INNERGY Integration (`integrations/innergy/`)

12. ✅ **client.py** - Typed INNERGY API client (built from OpenAPI spec structure)
13. ✅ **openapi_innergy.json** - Placeholder OpenAPI spec (TODO: replace with actual)
14. ✅ **sync_materials.py** - CLI for syncing material library to INNERGY
15. ✅ **import_projects.py** - CLI for importing projects to INNERGY

### Infrastructure

16. ✅ **Makefile** - Otto-friendly targets for migration tasks
17. ✅ **integrations/README.md** - Quick start guide and structure overview

---

## How to Run PPak ETL CLI (Test)

### Prerequisites

1. Create directories:
   ```bash
   mkdir -p data/ppak_exports
   mkdir -p data/migration_output
   ```

2. Place PPak export CSV files in `data/ppak_exports/`:
   - `projects_2024-01-15.csv` (or similar)
   - `materials_2024-01-15.csv` (optional)

### Run ETL

```bash
python -m integrations.ppak.etl.run_migration \
  --ppak-export-dir "./data/ppak_exports" \
  --output-dir "./data/migration_output"
```

### Expected Output

- `data/migration_output/canonical_projects_YYYY-MM-DD.json` - Canonical project data
- `data/migration_output/canonical_materials_YYYY-MM-DD.json` - Canonical material data (if materials file provided)
- `data/migration_output/migration_summary_YYYY-MM-DD.md` - Summary report

### Console Output

```
✅ Migration complete!
   Projects: 10
   Materials: 25
   Errors: 0
   Report: data/migration_output/migration_summary_2024-01-15.md
```

---

## TODOs Requiring Specific Information

### 1. PPak Column Names

**Files to update:**
- `integrations/ppak/schemas.py` - Update field names to match actual PPak CSV columns
- `integrations/ppak/etl/transform.py` - Update field access based on actual column names

**Action:** Analyze a real PPak export CSV and update the schemas.

### 2. PPak Date Formats

**File to update:**
- `integrations/ppak/etl/transform.py` - `parse_date()` function

**Action:** Check actual date format in PPak exports (e.g., "2024-01-15", "01/15/2024", etc.)

### 3. INNERGY OpenAPI Spec

**File to update:**
- `integrations/innergy/openapi_innergy.json` - Replace placeholder with actual OpenAPI JSON

**Action:** Paste the actual OpenAPI spec JSON into this file.

### 4. INNERGY API Endpoints

**File to update:**
- `integrations/innergy/client.py` - Update endpoint paths and request/response structures

**TODOs in code:**
- `list_projects()` - Verify endpoint path (currently `/api/projects`)
- `get_project()` - Verify endpoint path
- `list_project_work_orders()` - Verify endpoint path
- `list_purchase_orders()` - Verify endpoint path
- `list_materials()` - Verify endpoint path
- `create_project()` - Verify request body structure
- `update_project()` - Verify request body structure
- Auth header format (currently `Bearer {api_key}`)

**Action:** Review OpenAPI spec and update all `TODO` comments in `client.py`.

### 5. Mapping Tables

**Files to update:**
- `integrations/canonical/mappings/status_mapping.csv` - Add actual PPak status values
- `integrations/canonical/mappings/phase_mapping.csv` - Add actual PPak phase values
- `integrations/canonical/mappings/material_mapping.csv` - Build as you discover PPak materials

**Action:** Run ETL on a sample PPak export, review warnings for unmapped values, add to mapping tables.

### 6. Material Library Master

**Action:** Create `MATERIAL_LIBRARY_MASTER` CSV/JSON file with canonical material library.

**Format:** Should match `CanonicalMaterial` model structure.

---

## Next Steps

### Immediate (Before First Test Run)

1. ✅ **Get PPak export sample** - Export a small CSV (5-10 projects) from PPak
2. ✅ **Analyze PPak columns** - Update `integrations/ppak/schemas.py` with actual column names
3. ✅ **Update date parsing** - Check PPak date format, update `parse_date()` if needed
4. ✅ **Run first ETL test** - Execute `run_migration.py` and review output

### Short Term (Before INNERGY Integration)

5. ✅ **Replace OpenAPI spec** - Paste actual `openapi_innergy.json`
6. ✅ **Update INNERGY client** - Fix all `TODO` comments in `client.py` based on OpenAPI spec
7. ✅ **Test INNERGY connection** - When API credentials available, test `list_projects()` and `list_materials()`

### Medium Term (Full Migration)

8. ✅ **Build material mapping table** - As you discover PPak materials, map them to canonical SKUs
9. ✅ **Test material sync** - Run `sync_materials.py` in dry-run mode
10. ✅ **Test project import** - Run `import_projects.py` in dry-run mode with a test project
11. ✅ **Run health checks** - Validate migration with `health_check.py`

### Long Term (Otto Integration)

12. ✅ **Define Otto skills** - Create skills that wrap these CLI commands:
    - `run_ppak_export_etl`
    - `sync_innergy_material_library`
    - `run_innergy_project_import`
    - `migration_health_check`
13. ✅ **Test Otto orchestration** - Have Otto run a full migration cycle

---

## Summary

✅ **Documentation:** Complete - ROADMAP, DATA_MODEL, PROCESS_RUNBOOK  
✅ **Code Structure:** Complete - Canonical models, PPak ETL, INNERGY client skeleton  
✅ **CLI Scripts:** Complete - All entry points created and ready for testing  
✅ **Makefile:** Complete - Otto-friendly targets defined  

⏳ **Next:** Analyze actual PPak exports and update schemas, then run first test ETL

---

## Questions?

- See `PROCESS_RUNBOOK.md` for detailed process steps
- See `DATA_MODEL.md` for canonical model field definitions
- See `ROADMAP.md` for overall migration plan
- See `integrations/README.md` for quick start guide

