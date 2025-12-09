# Canonical Data Model

**Purpose:** Define the single source of truth data models that sit between PPak and INNERGY  
**Status:** Draft – Fields will be refined as we analyze actual PPak exports and INNERGY API

---

## Overview

The canonical data model serves as the **intermediate representation** between PPak (legacy) and INNERGY (new system). This allows us to:

- Transform PPak data once into a stable format
- Validate data before loading into INNERGY
- Support future integrations beyond PPak
- Maintain a clear mapping between systems

Both `CanonicalProject` and `CanonicalMaterial` include fields for:
- **Canonical fields** – Our source of truth
- **PPak identifiers** – For traceability back to source
- **INNERGY identifiers** – For tracking what's been imported

---

## CanonicalProject

Represents a single project/job in the canonical model.

### Core Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `project_number` | str | Unique project identifier (canonical) | "2024-001" |
| `name` | str | Project name/title | "Kitchen Remodel - Smith" |
| `customer_name` | str | Customer/client name | "Smith, John" |
| `customer_email` | str (optional) | Customer email | "john@example.com" |
| `customer_phone` | str (optional) | Customer phone | "555-1234" |
| `status` | str | Project status (canonical) | "in_progress" |
| `phase` | str | Current project phase | "fabrication" |
| `start_date` | date (optional) | Project start date | 2024-01-15 |
| `target_completion_date` | date (optional) | Target completion | 2024-03-30 |
| `actual_completion_date` | date (optional) | Actual completion | null |
| `created_at` | datetime | When record was created | 2024-01-10T10:00:00Z |
| `updated_at` | datetime | Last update timestamp | 2024-02-15T14:30:00Z |

### Identifiers (for mapping)

| Field | Type | Description |
|-------|------|-------------|
| `ppak_id` | str (optional) | Original PPak project ID | "PP-12345" |
| `ppak_job_number` | str (optional) | PPak job number | "JOB-2024-001" |
| `innergy_id` | str (optional) | INNERGY project ID (after import) | "proj_abc123" |
| `innergy_project_number` | str (optional) | INNERGY project number | "INN-2024-001" |

### Additional Metadata

| Field | Type | Description |
|-------|------|-------------|
| `notes` | str (optional) | Project notes/description | "Custom cabinets, island" |
| `address` | str (optional) | Project address | "123 Main St, City, ST" |
| `estimated_value` | decimal (optional) | Estimated project value | 45000.00 |
| `tags` | list[str] (optional) | Project tags/categories | ["kitchen", "residential"] |

### Status Values (Canonical)

Canonical status values (will be mapped from PPak and to INNERGY):

- `draft` – Project not yet started
- `quoted` – Quote sent, awaiting approval
- `approved` – Quote approved, ready to start
- `in_progress` – Active project
- `on_hold` – Temporarily paused
- `completed` – Project finished
- `cancelled` – Project cancelled

### Phase Values (Canonical)

Canonical phase values (will be mapped from PPak and to INNERGY):

- `design` – Design/planning phase
- `ordering` – Materials ordering
- `fabrication` – Manufacturing/fabrication
- `assembly` – Assembly phase
- `installation` – On-site installation
- `punch_list` – Final punch list items
- `completed` – All work complete

---

## CanonicalMaterial

Represents a single material/item in the canonical material library.

### Core Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `sku` | str | Stock Keeping Unit (canonical) | "CAB-DOOR-001" |
| `description` | str | Material description | "Shaker Door, 24x30" |
| `category` | str | Material category | "doors" |
| `subcategory` | str (optional) | Subcategory | "cabinet_doors" |
| `unit_of_measure` | str | UOM (e.g., "each", "sqft", "lf") | "each" |
| `vendor` | str (optional) | Primary vendor/supplier | "Vendor ABC" |
| `vendor_part_number` | str (optional) | Vendor's part number | "V-12345" |
| `cost_per_unit` | decimal (optional) | Cost per unit | 45.00 |
| `is_active` | bool | Whether material is active | true |
| `created_at` | datetime | When record was created | 2024-01-10T10:00:00Z |
| `updated_at` | datetime | Last update timestamp | 2024-02-15T14:30:00Z |

### Identifiers (for mapping)

| Field | Type | Description |
|-------|------|-------------|
| `ppak_sku` | str (optional) | Original PPak SKU | "PP-DOOR-001" |
| `ppak_id` | str (optional) | PPak material ID | "MAT-12345" |
| `innergy_id` | str (optional) | INNERGY material ID (after sync) | "mat_abc123" |
| `innergy_sku` | str (optional) | INNERGY SKU | "INN-DOOR-001" |

### Additional Metadata

| Field | Type | Description |
|-------|------|-------------|
| `notes` | str (optional) | Material notes | "White finish, soft close" |
| `lead_time_days` | int (optional) | Typical lead time | 14 |
| `minimum_order_quantity` | int (optional) | MOQ | 1 |
| `tags` | list[str] (optional) | Material tags | ["cabinet", "door", "white"] |

### Category Values (Canonical)

Common material categories:

- `doors` – Cabinet doors
- `drawers` – Drawer components
- `hardware` – Hinges, pulls, etc.
- `panels` – Cabinet panels/sides
- `trim` – Molding, trim pieces
- `finish` – Finish materials
- `fasteners` – Screws, nails, etc.
- `other` – Miscellaneous

---

## Mapping Tables

Mapping tables translate values between PPak, canonical, and INNERGY formats.

### status_mapping.csv

Maps project statuses across systems.

| ppak_status | canonical_status | innergy_status | notes |
|-------------|------------------|----------------|-------|
| "Draft" | "draft" | "draft" | Project not started |
| "Quoted" | "quoted" | "quoted" | Quote sent |
| "Approved" | "approved" | "approved" | Ready to start |
| "In Progress" | "in_progress" | "active" | Active project |
| "On Hold" | "on_hold" | "on_hold" | Paused |
| "Complete" | "completed" | "completed" | Finished |
| "Cancelled" | "cancelled" | "cancelled" | Cancelled |

**TODO:** Fill in actual PPak status values once we analyze exports.

### phase_mapping.csv

Maps project phases across systems.

| ppak_phase | canonical_phase | innergy_phase | notes |
|------------|-----------------|---------------|-------|
| "Design" | "design" | "design" | Planning phase |
| "Ordering" | "ordering" | "ordering" | Materials ordering |
| "Fab" | "fabrication" | "fabrication" | Manufacturing |
| "Assembly" | "assembly" | "assembly" | Assembly |
| "Install" | "installation" | "installation" | On-site install |
| "Punch" | "punch_list" | "punch_list" | Final items |
| "Complete" | "completed" | "completed" | All done |

**TODO:** Fill in actual PPak phase values once we analyze exports.

### material_mapping.csv

Maps material SKUs between PPak and canonical (and optionally to INNERGY).

| ppak_sku | canonical_sku | innergy_sku | notes |
|----------|--------------|-------------|-------|
| "PP-DOOR-001" | "CAB-DOOR-001" | "INN-DOOR-001" | Shaker door mapping |
| "PP-HW-123" | "CAB-HW-123" | "INN-HW-123" | Hardware mapping |

**TODO:** Build this mapping table as we discover PPak materials and match them to canonical library.

---

## Implementation Notes

### Pydantic Models

The canonical models will be implemented as Pydantic models in `integrations/canonical/models.py`:

```python
from pydantic import BaseModel
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List

class CanonicalProject(BaseModel):
    # Core fields
    project_number: str
    name: str
    customer_name: str
    # ... (all fields above)
    
    class Config:
        # Allow extra fields for future extensibility
        extra = "allow"
```

### Validation Rules

- `project_number` must be unique within canonical dataset
- `sku` must be unique within canonical material library
- `status` and `phase` must be valid canonical values (or mapped)
- Dates must be valid (start_date <= target_completion_date)

### Data Quality Checks

During ETL, we'll validate:
- Required fields are present
- Status/phase values can be mapped
- Material SKUs exist in canonical library (or flag for review)
- Dates are in valid format and ranges

---

## Future Extensions

As we discover more fields needed:
- Add to canonical models (with `extra = "allow"` for flexibility)
- Update mapping tables
- Document in this file

The canonical model should be **stable** (changes require migration), but flexible enough to capture all necessary data.

