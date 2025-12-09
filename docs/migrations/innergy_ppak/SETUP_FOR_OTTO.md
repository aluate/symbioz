# Setup Guide: PPak-INNERGY Migration for Otto

**Purpose:** Complete setup guide to get the migration system ready for Otto to run  
**Status:** Ready for Implementation  
**Last Updated:** January 2025

---

## Quick Start Checklist

- [ ] Install Python dependencies
- [ ] Set up directory structure
- [ ] Configure environment variables
- [ ] Get INNERGY API credentials (or use placeholder)
- [ ] Test PPak ETL with sample data
- [ ] Test INNERGY client connection (if API access available)
- [ ] Create initial material library master file
- [ ] Set up mapping tables
- [ ] Test individual scripts
- [ ] Configure Otto skills
- [ ] Run full test cycle

---

## Step 1: Install Dependencies

### Python Requirements

Create `integrations/requirements.txt` (if it doesn't exist):

```txt
pydantic>=2.0.0
httpx>=0.25.0
python-dotenv>=1.0.0
```

Install:

```bash
pip install -r integrations/requirements.txt
```

---

## Step 2: Set Up Directory Structure

Create the following directories:

```bash
mkdir -p data/ppak_exports
mkdir -p data/migration_output
mkdir -p logs
```

**Directory purposes:**
- `data/ppak_exports/`: Drop PPak CSV export files here
- `data/migration_output/`: Canonical files and reports written here
- `logs/`: Script logs (optional, scripts also log to stdout)

---

## Step 3: Configure Environment Variables

Create `.env` file in repo root (or set in Otto's environment):

```bash
# INNERGY API Configuration
INNERGY_API_BASE_URL=https://app.innergy.com/api  # Update based on OpenAPI spec
INNERGY_API_KEY=your_api_key_here  # Get from INNERGY Profile → API

# PPak Export Location
PPAK_EXPORT_DIR=./data/ppak_exports

# Migration Output
MIGRATION_OUTPUT_DIR=./data/migration_output

# Material Library
MATERIAL_LIBRARY_MASTER=./data/material_library_master.csv
```

**Note:** If you don't have INNERGY API access yet, you can still:
- Run PPak ETL (doesn't need INNERGY)
- Test canonical transformation
- Prepare material library
- Set up mapping tables

---

## Step 4: Get INNERGY API Credentials

### If You Have Access

1. Log into INNERGY
2. Go to **Profile → API**
3. Generate or copy your API key
4. Update `INNERGY_API_KEY` in `.env`
5. Verify base URL from OpenAPI spec (should be `https://app.innergy.com/api`)

### If You Don't Have Access Yet

That's okay! You can still:
- ✅ Run PPak ETL and create canonical files
- ✅ Build and test the material library
- ✅ Set up mapping tables
- ✅ Test the INNERGY client with mock data

When you get API access, just update the `.env` file and test the connection.

---

## Step 5: Create Initial Material Library Master

Create `data/material_library_master.csv` with this structure:

```csv
sku,description,category,subcategory,unit_of_measure,cost_per_unit,vendor,vendor_part_number,is_active,notes
CAB-DOOR-001,Shaker Door 24x30,doors,cabinet_doors,each,45.00,Vendor ABC,V-12345,true,White finish
CAB-HW-123,Soft Close Hinge,hardware,hinges,each,12.50,Vendor XYZ,V-67890,true,Standard soft close
```

**This becomes your source of truth** for materials. Edit this file to add/update materials, then sync to INNERGY.

---

## Step 6: Set Up Mapping Tables

Update mapping CSV files in `integrations/canonical/mappings/`:

### `status_mapping.csv`

```csv
ppak_status,canonical_status,innergy_status,notes
Draft,draft,draft,Project not started
Quoted,quoted,quoted,Quote sent
Approved,approved,approved,Ready to start
In Progress,in_progress,active,Active project
On Hold,on_hold,on_hold,Paused
Complete,completed,completed,Finished
Cancelled,cancelled,cancelled,Cancelled
```

**TODO:** Update `ppak_status` values once you analyze actual PPak exports.

### `phase_mapping.csv`

```csv
ppak_phase,canonical_phase,innergy_phase,notes
Design,design,design,Planning phase
Ordering,ordering,ordering,Materials ordering
Fab,fabrication,fabrication,Manufacturing
Assembly,assembly,assembly,Assembly
Install,installation,installation,On-site install
Punch,punch_list,punch_list,Final items
Complete,completed,completed,All done
```

**TODO:** Update `ppak_phase` values once you analyze actual PPak exports.

### `material_mapping.csv`

```csv
ppak_sku,canonical_sku,innergy_sku,notes
PP-DOOR-001,CAB-DOOR-001,INN-DOOR-001,Shaker door mapping
PP-HW-123,CAB-HW-123,INN-HW-123,Hardware mapping
```

**TODO:** Build this mapping as you discover PPak materials and match them to canonical library.

---

## Step 7: Test PPak ETL (No INNERGY Needed)

### Prepare Test Data

1. Export a small sample from PPak (5-10 projects)
2. Save to `data/ppak_exports/projects_test.csv`
3. (Optional) Export materials to `data/ppak_exports/materials_test.csv`

### Run ETL

```bash
python -m integrations.ppak.etl.run_migration \
  --ppak-export-dir ./data/ppak_exports \
  --output-dir ./data/migration_output
```

### Check Results

- ✅ `data/migration_output/canonical_projects_YYYY-MM-DD.json` created
- ✅ `data/migration_output/migration_summary_YYYY-MM-DD.md` created
- ✅ Review summary report for any mapping issues
- ✅ Update mapping tables if needed
- ✅ Re-run ETL to verify fixes

---

## Step 8: Test INNERGY Client (If API Access Available)

### Test Connection

```python
# Quick test script
from integrations.innergy.client import INNERGYClient
import os

api_key = os.getenv('INNERGY_API_KEY')
api_url = os.getenv('INNERGY_API_BASE_URL')

client = INNERGYClient(api_key=api_key, base_url=api_url)

# Test list_projects
projects = client.list_projects()
print(f"Found {len(projects)} projects")

client.close()
```

### Test Material Sync (Dry-Run)

```bash
python -m integrations.innergy.sync_materials \
  --material-library ./data/material_library_master.csv \
  --dry-run
```

Should report: "Would create X new materials, update Y materials, etc."

---

## Step 9: Configure Otto Skills

### Option A: If Otto Uses YAML Config

Add to Otto's skill configuration file:

```yaml
skills:
  migration:
    run_ppak_etl:
      command: python -m integrations.ppak.etl.run_migration
      description: "Transform PPak exports to canonical format"
      parameters:
        - name: ppak_export_dir
          type: string
          required: true
        - name: output_dir
          type: string
          required: true
        - name: date_range
          type: string
          required: false
    sync_materials:
      command: python -m integrations.innergy.sync_materials
      description: "Sync material library to INNERGY"
      parameters:
        - name: material_library
          type: string
          required: true
        - name: dry_run
          type: boolean
          default: true
    import_projects:
      command: python -m integrations.innergy.import_projects
      description: "Import canonical projects to INNERGY"
      parameters:
        - name: canonical_file
          type: string
          required: true
        - name: dry_run
          type: boolean
          default: true
    health_check:
      command: python -m integrations.canonical.health_check
      description: "Run migration health checks"
      parameters:
        - name: canonical_file
          type: string
          required: true
```

### Option B: If Otto Uses Python/JSON

See `OTTO_SKILLS.md` for detailed skill definitions.

---

## Step 10: Run Full Test Cycle

### Test with Small Dataset

1. **Export 5-10 test projects from PPak**
2. **Run ETL:**
   ```bash
   python -m integrations.ppak.etl.run_migration \
     --ppak-export-dir ./data/ppak_exports \
     --output-dir ./data/migration_output
   ```
3. **Review canonical files** - verify data looks correct
4. **Sync materials (dry-run):**
   ```bash
   python -m integrations.innergy.sync_materials \
     --material-library ./data/material_library_master.csv \
     --dry-run
   ```
5. **Import projects (dry-run):**
   ```bash
   python -m integrations.innergy.import_projects \
     --canonical-file ./data/migration_output/canonical_projects_YYYY-MM-DD.json \
     --dry-run
   ```
6. **Review dry-run results** - verify what would happen
7. **If everything looks good, run live:**
   ```bash
   # Sync materials (live)
   python -m integrations.innergy.sync_materials \
     --material-library ./data/material_library_master.csv \
     --no-dry-run
   
   # Import projects (live)
   python -m integrations.innergy.import_projects \
     --canonical-file ./data/migration_output/canonical_projects_YYYY-MM-DD.json \
     --no-dry-run \
     --update-canonical
   ```
8. **Run health check:**
   ```bash
   python -m integrations.canonical.health_check \
     --canonical-file ./data/migration_output/canonical_projects_YYYY-MM-DD.json
   ```

---

## Step 11: Otto Integration

### Test Otto Skills Individually

```bash
# Test via Otto (example - adjust to your Otto's interface)
otto run migration.run_ppak_etl \
  --ppak-export-dir ./data/ppak_exports \
  --output-dir ./data/migration_output
```

### Test Full Cycle via Otto

```bash
otto run migration.run_full_cycle \
  --ppak-export-dir ./data/ppak_exports \
  --output-dir ./data/migration_output \
  --material_library ./data/material_library_master.csv \
  --dry-run
```

---

## Troubleshooting

### Issue: "Module not found: integrations.ppak"

**Solution:** Make sure you're running from repo root, or add repo root to `PYTHONPATH`:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Issue: "INNERGY API returned 401 Unauthorized"

**Solution:** 
- Check `INNERGY_API_KEY` in `.env` or environment
- Verify API key is valid in INNERGY Profile → API
- Check base URL matches OpenAPI spec

### Issue: "Unknown PPak status: 'In Progress'"

**Solution:** Add mapping to `integrations/canonical/mappings/status_mapping.csv`, then re-run ETL.

### Issue: "Material SKU 'PP-DOOR-001' not found in canonical library"

**Solution:** 
- Add material to `data/material_library_master.csv`
- Or add mapping to `integrations/canonical/mappings/material_mapping.csv`
- Re-run ETL

---

## Next Steps After Setup

1. ✅ **Analyze real PPak exports** - Update schemas and mapping tables
2. ✅ **Build complete material library** - Add all materials to master file
3. ✅ **Test with larger dataset** - Run ETL on 50-100 projects
4. ✅ **Get INNERGY API access** - If not already available
5. ✅ **Run full migration** - With Otto orchestrating the cycle
6. ✅ **Monitor and iterate** - Fix issues, update mappings, re-run

---

## Files Created/Modified

After setup, you should have:

```
integrations/
├── canonical/
│   ├── models.py                    ✅ Already exists
│   ├── health_check.py              ⏳ Needs implementation
│   └── mappings/
│       ├── status_mapping.csv       ✅ Update with real PPak values
│       ├── phase_mapping.csv        ✅ Update with real PPak values
│       └── material_mapping.csv    ✅ Build as you discover materials
├── ppak/
│   ├── schemas.py                   ✅ Update with real PPak columns
│   └── etl/
│       ├── transform.py            ✅ Already exists
│       └── run_migration.py        ✅ Already exists
└── innergy/
    ├── client.py                    ✅ Update with real OpenAPI spec
    ├── sync_materials.py           ✅ Already exists
    └── import_projects.py          ✅ Already exists

data/
├── ppak_exports/                    ✅ Create and add PPak CSVs
├── migration_output/                 ✅ Created by ETL
└── material_library_master.csv      ✅ Create with your materials

docs/migrations/innergy_ppak/
├── ROADMAP.md                       ✅ Already exists
├── DATA_MODEL.md                    ✅ Already exists
├── PROCESS_RUNBOOK.md               ✅ Already exists
├── OTTO_SKILLS.md                   ✅ Just created
└── SETUP_FOR_OTTO.md                ✅ This file
```

---

## Success Criteria

You're ready for Otto when:

- ✅ All Python scripts run without errors
- ✅ PPak ETL produces canonical files
- ✅ Mapping tables cover all known PPak values
- ✅ Material library master file exists
- ✅ INNERGY client can connect (or ready to test when API access available)
- ✅ All scripts work in dry-run mode
- ✅ Otto can call scripts via skill definitions
- ✅ Full test cycle completes successfully

---

## Questions?

- Check `PROCESS_RUNBOOK.md` for detailed process steps
- Check `OTTO_SKILLS.md` for skill definitions
- Check `ROADMAP.md` for high-level migration plan
- Review script logs for detailed error messages

