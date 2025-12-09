# INNERGY-PPak Migration Roadmap

**Purpose:** High-level phases for migrating from PPak (legacy system) to INNERGY (new system)  
**Status:** Planning Phase  
**Last Updated:** January 2025

---

## Overview

This migration establishes a **canonical data model** that sits between PPak and INNERGY, enabling a repeatable ETL pipeline:

```
PPak ➜ Canonical (your truth) ➜ INNERGY
```

This approach allows us to:
- Validate data transformations before loading into INNERGY
- Maintain a single source of truth (canonical model)
- Support future integrations beyond PPak
- Enable automation agent (Otto) to orchestrate the migration

---

## Phase 0 – Alignment & Guardrails

**Goal:** Establish the foundation and constraints before building.

### Key Decisions
- **Canonical model is the source of truth** – PPak and INNERGY are endpoints
- **ETL is repeatable** – Can run multiple times safely (idempotent where possible)
- **Otto-friendly design** – All scripts are CLI-based, non-interactive, with clear logging
- **Dry-run capability** – Validate before actual writes to INNERGY

### Deliverables
- ✅ Documentation structure (this file, DATA_MODEL.md, PROCESS_RUNBOOK.md)
- ✅ Code skeleton with clear separation of concerns
- ✅ Environment variable configuration plan
- ✅ Mapping table structure

### Constraints
- PPak data may be incomplete or inconsistent
- INNERGY API access/permissions may be limited initially
- Material library needs to be maintained separately from project data
- Migration must be reversible (or at least auditable)

---

## Phase 1 – Discover & Model Both Worlds

**Goal:** Understand PPak exports and INNERGY API structure, then define canonical models.

### Key Activities
1. **Analyze PPak exports**
   - Identify all CSV columns and their meanings
   - Document data quality issues
   - Map PPak statuses, phases, material SKUs to canonical equivalents

2. **Analyze INNERGY OpenAPI spec**
   - Identify required vs optional fields
   - Understand project, work order, purchase order structures
   - Document material library endpoints

3. **Define canonical models**
   - `CanonicalProject` – Single source of truth for project data
   - `CanonicalMaterial` – Single source of truth for material data
   - Include fields for both PPak and INNERGY IDs (for mapping)

### Deliverables
- ✅ `DATA_MODEL.md` with complete field definitions
- ✅ Mapping tables (status, phase, material SKU)
- ✅ PPak schema definitions (`integrations/ppak/schemas.py`)
- ✅ INNERGY client with typed models (`integrations/innergy/client.py`)

### Success Criteria
- Can parse a PPak export into canonical models
- Can read from INNERGY API and map to canonical models
- Mapping tables cover all known status/phase/material variations

---

## Phase 2 – PPak → Canonical → INNERGY Pipeline

**Goal:** Build the ETL pipeline that transforms PPak data into INNERGY format.

### Key Activities
1. **PPak ETL (`integrations/ppak/etl/`)**
   - Read PPak CSV exports
   - Transform rows to `CanonicalProject` / `CanonicalMaterial`
   - Apply mapping tables (status, phase, materials)
   - Write canonical format to `MIGRATION_OUTPUT_DIR`

2. **INNERGY Import (`integrations/innergy/`)**
   - Read canonical project/material files
   - Validate against INNERGY API requirements
   - Generate INNERGY import CSVs OR call API directly
   - Support dry-run mode (validate only, no writes)

3. **Error Handling & Reporting**
   - Log mapping failures (unknown status, missing materials)
   - Generate summary reports (job count, success/failure)
   - Track which projects have been imported (avoid duplicates)

### Deliverables
- ✅ `integrations/ppak/etl/run_migration.py` CLI
- ✅ `integrations/innergy/sync_materials.py` CLI (or equivalent)
- ✅ `integrations/innergy/import_projects.py` CLI (or equivalent)
- ✅ Summary report generation

### Success Criteria
- Can run `python -m integrations.ppak.etl.run_migration` and produce canonical files
- Can validate canonical data against INNERGY API (dry-run)
- Can import a test project into INNERGY (when API access is ready)
- All errors are logged and reported clearly

---

## Phase 3 – Replace PPak Material Library with Master Canonical Library

**Goal:** Maintain a single canonical material library that syncs to INNERGY.

### Key Activities
1. **Master Material Library**
   - Create/maintain `MATERIAL_LIBRARY_MASTER` (CSV or Sheet)
   - This becomes the source of truth (not PPak exports)

2. **Sync Process**
   - Compare canonical materials vs INNERGY `/api/materials` GET
   - Compute diff: new materials, updated materials, should-be-inactive
   - Sync changes to INNERGY (via CSV import or API)

3. **Material Mapping**
   - Map PPak material SKUs to canonical SKUs during project ETL
   - Handle cases where PPak SKU doesn't exist in canonical library

### Deliverables
- ✅ `integrations/innergy/sync_materials.py` CLI
- ✅ Material diff/comparison logic
- ✅ Process to update `MATERIAL_LIBRARY_MASTER` from canonical sources

### Success Criteria
- Material library sync runs automatically (or via Otto)
- New materials added to master library appear in INNERGY
- PPak project ETL correctly maps to canonical materials

---

## Phase 4 – Cut-Over & Steady-State Operation

**Goal:** Complete migration and establish ongoing processes.

### Key Activities
1. **Full Migration Run**
   - Migrate all historical PPak projects
   - Verify data integrity (health checks)
   - Handle edge cases and data quality issues

2. **Health Checks**
   - `migration_health_check` script
   - Verify all canonical projects have `innergy_id` after import
   - Check for unmapped materials or statuses
   - Generate markdown reports for review

3. **Otto Integration**
   - Define Otto skills:
     - `run_ppak_export_etl`
     - `run_innergy_project_import`
     - `sync_innergy_material_library`
     - `migration_health_check`
   - Test Otto can orchestrate a full migration cycle

4. **Documentation & Runbooks**
   - Complete `PROCESS_RUNBOOK.md` with real examples
   - Document common issues and solutions
   - Create troubleshooting guide

### Deliverables
- ✅ All historical data migrated
- ✅ Health check reports showing clean migration
- ✅ Otto skills implemented and tested
- ✅ Complete runbook documentation

### Success Criteria
- All PPak projects successfully imported to INNERGY
- Material library is synced and maintained
- Otto can run migration cycles autonomously
- Process is documented and repeatable

---

## Ongoing Maintenance

After cut-over:
- **New projects:** Enter directly into INNERGY (or via canonical if needed)
- **Material updates:** Update `MATERIAL_LIBRARY_MASTER`, then sync to INNERGY
- **Historical queries:** PPak exports remain available for reference, but canonical is source of truth

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| PPak data quality issues | Validate and log during ETL, manual review of failures |
| INNERGY API changes | Version the client, test against OpenAPI spec |
| Missing mappings | Log all unmapped values, update mapping tables iteratively |
| Duplicate imports | Track `innergy_id` in canonical models, check before import |
| Material library drift | Regular sync runs, diff reports |

---

## Next Steps

1. ✅ Complete documentation skeleton (this file)
2. ⏳ Define canonical models (`DATA_MODEL.md`)
3. ⏳ Create code skeleton
4. ⏳ Analyze first PPak export sample
5. ⏳ Test INNERGY API connection (when credentials available)

