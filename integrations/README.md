# Integrations

This directory contains integration code for migrating data between PPak (legacy system) and INNERGY (new system).

## Structure

```
integrations/
├── canonical/           # Canonical data models (single source of truth)
│   ├── models.py       # CanonicalProject, CanonicalMaterial
│   └── mappings/       # Mapping tables (status, phase, material)
│
├── ppak/               # PPak integration (extract & transform)
│   ├── schemas.py      # PPak export row models
│   └── etl/            # ETL pipeline
│       ├── transform.py
│       └── run_migration.py
│
└── innergy/            # INNERGY integration (load)
    ├── client.py       # Typed API client
    ├── openapi_innergy.json  # OpenAPI spec (replace with actual)
    ├── sync_materials.py
    └── import_projects.py
```

## Quick Start

### 1. Set Environment Variables

```bash
export INNERGY_API_BASE_URL=https://api.innergy.example.com
export INNERGY_API_KEY=your_api_key
export PPAK_EXPORT_DIR=./data/ppak_exports
export MIGRATION_OUTPUT_DIR=./data/migration_output
export MATERIAL_LIBRARY_MASTER=./data/material_library_master.csv
```

### 2. Run PPak ETL

```bash
python -m integrations.ppak.etl.run_migration \
  --ppak-export-dir "$PPAK_EXPORT_DIR" \
  --output-dir "$MIGRATION_OUTPUT_DIR"
```

### 3. Sync Materials (Dry Run)

```bash
python -m integrations.innergy.sync_materials \
  --material-library "$MATERIAL_LIBRARY_MASTER" \
  --dry-run
```

### 4. Import Projects (Dry Run)

```bash
python -m integrations.innergy.import_projects \
  --canonical-file "$MIGRATION_OUTPUT_DIR/canonical_projects_YYYY-MM-DD.json" \
  --dry-run
```

### 5. Run Health Checks

```bash
python -m integrations.canonical.health_check \
  --canonical-file "$MIGRATION_OUTPUT_DIR/canonical_projects_YYYY-MM-DD.json"
```

## Using Makefile

See `Makefile` in repo root for convenient targets:

```bash
make ppak-migrate-latest
make innergy-sync-materials
make migration-health-check
```

## Documentation

See `docs/migrations/innergy_ppak/` for:
- `ROADMAP.md` - Migration phases and plan
- `DATA_MODEL.md` - Canonical model definitions
- `PROCESS_RUNBOOK.md` - Step-by-step process guide

## TODO

- [ ] Replace `openapi_innergy.json` with actual OpenAPI spec
- [ ] Update PPak schemas with actual column names from exports
- [ ] Update INNERGY client methods with actual endpoint paths
- [ ] Fill in mapping tables with real PPak values
- [ ] Test with actual PPak export files
- [ ] Test INNERGY API connection (when credentials available)

