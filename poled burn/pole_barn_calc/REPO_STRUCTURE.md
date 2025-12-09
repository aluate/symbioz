# Repository Structure - Pole Barn Calculator

**Last Updated:** After Repository Cleanup

---

## 📁 Current Structure

```
pole_barn_calc/
├── ARCHITECTURE_OVERVIEW.md    ← NEW: Consolidated system architecture
├── DEVELOPMENT_LOG.md          ← Master development log
├── NEXT_STEPS_AND_GAPS.md      ← Current roadmap and gaps
├── PROJECT_EXPORT_FULL.md      ← Full codebase snapshot
├── README.md                    ← Project overview
├── REPO_STRUCTURE.md           ← This file
│
├── archive/                     ← Historical documentation
│   ├── APP_WORKFLOW_GUIDE.md
│   ├── ASSEMBLIES_*.md (4 files)
│   ├── BOM_IMPLEMENTATION_SUMMARY.md
│   ├── CRITICAL_REVIEW.md
│   ├── DESKTOP_APP_*.md (2 files)
│   ├── GUI_*.md (3 files)
│   ├── IMPLEMENTATION_READINESS_SUMMARY.md
│   ├── MARKUP_FLEXIBILITY_SUMMARY.md
│   ├── MATERIALS_LIBRARY_EXPORT.md
│   ├── NEXT_STEPS.md
│   ├── PATH_B_IMPLEMENTATION_STATUS.md
│   ├── PRICING_CALIBRATION.md
│   ├── PROJECT_REVIEW.md
│   ├── SETUP_AND_FIXES.md
│   ├── SNOW_LOAD_DATA_SOURCE.md
│   ├── TESTING_READY_SUMMARY.md
│   └── pricing.before_calibration.csv
│
├── config/                     ← CSV configuration files
│   ├── assemblies.example.csv
│   ├── parts.example.csv
│   └── pricing.example.csv
│
├── systems/                    ← Core calculation modules
│   └── pole_barn/
│       ├── __init__.py
│       ├── model.py            ← Data models
│       ├── geometry.py         ← Geometry calculations
│       ├── assemblies.py       ← Material quantity calculations
│       ├── bom.py              ← BOM expansion and packing
│       ├── pricing.py          ← Pricing and costing
│       ├── calculator.py       ← Main orchestrator
│       ├── export_excel.py     ← Excel BOM export
│       └── export_json.py      ← JSON project export
│
├── apps/                       ← User interfaces
│   ├── __init__.py
│   ├── cli.py                  ← Command-line interface
│   └── gui.py                  ← Tkinter GUI
│
├── tests/                      ← Test suite
│   ├── test_geometry.py
│   ├── test_assemblies.py
│   ├── test_pricing.py
│   └── test_end_to_end.py
│
├── tools/                       ← Utility scripts
│   ├── export_full_project.py
│   ├── export_material_library.py
│   └── run_test_buildings.py
│
├── test_exports/               ← Latest test building exports
│   ├── Test_A_SmallShop_bom.xlsx
│   ├── Test_A_SmallShop_project.json
│   ├── Test_B_40x60_bom.xlsx
│   ├── Test_B_40x60_project.json
│   ├── Test_C_50x80_Commercial_bom.xlsx
│   ├── Test_C_50x80_Commercial_project.json
│   ├── Test_D_36x48_Deluxe_bom.xlsx
│   └── Test_D_36x48_Deluxe_project.json
│
├── control/                     ← Control documents
│   └── pole_barn_calculator.md
│
├── pyproject.toml              ← Project metadata and dependencies
├── build_exe.bat               ← PyInstaller build script
├── build_exe.spec              ← PyInstaller spec file
├── run_gui.bat                 ← GUI launcher
├── run_test_buildings.bat      ← Test building generator
└── [other batch files]         ← Various utility scripts
```

---

## 📄 Key Documents

### Root Level (Current/Active):
- **ARCHITECTURE_OVERVIEW.md** - System architecture, data flow, design decisions
- **DEVELOPMENT_LOG.md** - Master development history and audit trail
- **NEXT_STEPS_AND_GAPS.md** - Current roadmap, priorities, and known gaps
- **PROJECT_EXPORT_FULL.md** - Full codebase snapshot for review
- **README.md** - Project overview and quick start

### Archive (Historical Reference):
- All design documents, implementation summaries, and changelogs
- Historical CSV backups
- Older status documents

---

## 🎯 Document Purpose Guide

**Need to understand the system?**
→ Read `ARCHITECTURE_OVERVIEW.md`

**Need to see what's been done?**
→ Read `DEVELOPMENT_LOG.md`

**Need to know what's next?**
→ Read `NEXT_STEPS_AND_GAPS.md`

**Need full codebase for review?**
→ Read `PROJECT_EXPORT_FULL.md`

**Need historical context?**
→ Check `/archive/` for specific documents

---

## ✅ Cleanup Verification

- ✅ All historical docs moved to `/archive/`
- ✅ Single architecture document created
- ✅ Master log updated with cleanup details
- ✅ Test exports contain only latest 4 buildings
- ✅ Config directory contains only current CSVs
- ✅ All code modules import successfully
- ✅ Repository structure is clean and professional

---

**Repository is now clean, organized, and ready for production development.**

