# Materials Library Export

This document contains a full export of all parts, pricing, and assemblies.
**Auto-generated** - Regenerate using `tools/export_material_library.py`

---

## Parts & Pricing by Category

### concrete

| Part ID | Part Name | Description | Unit | Unit Price | Vendor | Notes |
|---------|-----------|-------------|------|------------|--------|-------|
| CONCRETE_CY | Concrete | Concrete (bag-equivalent) | cuyd | $270.00 | HomeDepot | Derived from 80 lb Sakrete bags |

### doors

| Part ID | Part Name | Description | Unit | Unit Price | Vendor | Notes |
|---------|-----------|-------------|------|------------|--------|-------|
| OVERHEAD_DOOR | Overhead Door | Steel roll-up door unit | ea | $1062.50 | Assumed | 8' x 7' typical |

### fasteners

| Part ID | Part Name | Description | Unit | Unit Price | Vendor | Notes |
|---------|-----------|-------------|------|------------|--------|-------|
| SCREW_METAL | Metal Screw | Metal roofing screw | ea | $0.17 | HomeDepot | Derived from 100-pack pricing |

### framing

| Part ID | Part Name | Description | Unit | Unit Price | Vendor | Notes |
|---------|-----------|-------------|------|------------|--------|-------|
| POST_6X6_PT | 6x6 PT Post | 6x6 PT post | ea | $75.00 | HomeDepot | Avg of 8-12 ft PT posts |
| LBR_2X6_LF | 2x6 Lumber | 2x6 SPF framing lumber | lf | $1.16 | HomeDepot | Price derived from 2x6x12 |
| TRUSS_STD | Standard Truss | Engineered pole barn truss | ea | $312.50 | Assumed | Typical 30-40 ft span truss |

### insulation

| Part ID | Part Name | Description | Unit | Unit Price | Vendor | Notes |
|---------|-----------|-------------|------|------------|--------|-------|
| INS_R19_SQFT | R-19 Insulation | R-19 fiberglass batt insulation | sqft | $0.83 | OwensCorning | E61 bag coverage |
| INS_ROCKWOOL_SQFT | Rock Wool Insulation | Rock wool batt insulation | sqft | $1.15 | Assumed | R-19 equivalent |
| INS_RIGID_SQFT | Rigid Board Insulation | Rigid board insulation | sqft | $1.50 | Assumed | R-5 per inch |
| INS_SPRAYFOAM_SQFT | Spray Foam Insulation | Spray foam insulation | sqft | $2.25 | Assumed | R-6 per inch (closed-cell) |

### sheathing

| Part ID | Part Name | Description | Unit | Unit Price | Vendor | Notes |
|---------|-----------|-------------|------|------------|--------|-------|
| SHEATHING_OSB_SQFT | OSB Sheathing | OSB sheathing 7/16" | sqft | $0.75 | HomeDepot | 4' x 8' sheets |
| SHEATHING_PLY_SQFT | Plywood Sheathing | Plywood sheathing 1/2" | sqft | $1.10 | HomeDepot | 4' x 8' sheets |

### skin

| Part ID | Part Name | Description | Unit | Unit Price | Vendor | Notes |
|---------|-----------|-------------|------|------------|--------|-------|
| METAL_PANEL_29_SQFT | Metal Panel 29ga | 29ga metal roof/wall panel | sqft | $1.45 | HomeDepot | 12' panel covers 36 sqft |
| METAL_PANEL_26_SQFT | Metal Panel 26ga | 26ga metal roof/wall panel | sqft | $1.81 | HomeDepot | 12' panel covers 36 sqft |

### soft_cost

| Part ID | Part Name | Description | Unit | Unit Price | Vendor | Notes |
|---------|-----------|-------------|------|------------|--------|-------|
| DELIVERY_LUMP | Delivery | Delivery allowance | lump | $300.00 | Assumed | - |
| PERMIT_LUMP | Permit | Permit allowance | lump | $500.00 | Assumed | - |
| SITE_PREP_LUMP | Site Prep | Site prep allowance | lump | $1000.00 | Assumed | - |

### trim

| Part ID | Part Name | Description | Unit | Unit Price | Vendor | Notes |
|---------|-----------|-------------|------|------------|--------|-------|
| TRIM_EAVE | Eave Trim | Metal eave trim | lf | $3.13 | Assumed | - |
| TRIM_RAKE | Rake Trim | Metal rake trim | lf | $3.13 | Assumed | - |
| TRIM_BASE | Base Trim | Metal base trim | lf | $3.13 | Assumed | - |
| TRIM_CORNER | Corner Trim | Metal corner trim | lf | $3.13 | Assumed | - |
| RIDGE_CAP | Ridge Cap | Metal ridge cap | lf | $3.75 | Assumed | - |
| TRIM_DOOR | Door Trim | Metal door trim | lf | $3.13 | Assumed | - |
| TRIM_WINDOW | Window Trim | Metal window trim | lf | $3.13 | Assumed | - |

### ventilation

| Part ID | Part Name | Description | Unit | Unit Price | Vendor | Notes |
|---------|-----------|-------------|------|------------|--------|-------|
| VENT_RIDGE | Ridge Vent | Continuous ridge vent | lf | $4.00 | Assumed | - |
| VENT_GABLE | Gable Vent | Gable vent | ea | $80.00 | Assumed | - |

---

## Assembly Mappings

| Assembly Name | Part ID | Waste Factor | Labor/Unit | Notes |
|---------------|---------|--------------|------------|-------|
| posts | POST_6X6_PT | 1.0 | 0.25 |  |
| trusses | TRUSS_STD | 1.0 | 0.35 |  |
| sidewall_girts | LBR_2X6_LF | 1.05 | 0.02 |  |
| endwall_girts | LBR_2X6_LF | 1.05 | 0.02 |  |
| roof_purlins | LBR_2X6_LF | 1.05 | 0.02 |  |
| roof_panels | METAL_PANEL_29_SQFT | 1.05 | 0.03 |  |
| sidewall_panels | METAL_PANEL_29_SQFT | 1.05 | 0.03 |  |
| endwall_panels | METAL_PANEL_29_SQFT | 1.05 | 0.03 |  |
| roof_panels_26ga | METAL_PANEL_26_SQFT | 1.05 | 0.03 |  |
| sidewall_panels_26ga | METAL_PANEL_26_SQFT | 1.05 | 0.03 |  |
| endwall_panels_26ga | METAL_PANEL_26_SQFT | 1.05 | 0.03 |  |
| eave_trim | TRIM_EAVE | 1.1 | 0.02 |  |
| rake_trim | TRIM_RAKE | 1.1 | 0.02 |  |
| base_trim | TRIM_BASE | 1.1 | 0.02 |  |
| corner_trim | TRIM_CORNER | 1.1 | 0.03 |  |
| roof_fasteners | SCREW_METAL | 1.05 | 0.0 |  |
| wall_fasteners | SCREW_METAL | 1.05 | 0.0 |  |
| trim_fasteners | SCREW_METAL | 1.05 | 0.0 |  |
| post_concrete | CONCRETE_CY | 1.05 | 0.0 |  |
| slab_concrete | CONCRETE_CY | 1.05 | 0.0 |  |
| wall_insulation | INS_R19_SQFT | 1.0 | 0.02 |  |
| wall_insulation_rockwool | INS_ROCKWOOL_SQFT | 1.0 | 0.02 |  |
| wall_insulation_rigid | INS_RIGID_SQFT | 1.05 | 0.02 |  |
| wall_insulation_sprayfoam | INS_SPRAYFOAM_SQFT | 1.0 | 0.02 |  |
| roof_insulation | INS_R19_SQFT | 1.0 | 0.02 |  |
| roof_insulation_rockwool | INS_ROCKWOOL_SQFT | 1.0 | 0.02 |  |
| roof_insulation_rigid | INS_RIGID_SQFT | 1.05 | 0.02 |  |
| roof_insulation_sprayfoam | INS_SPRAYFOAM_SQFT | 1.0 | 0.02 |  |
| ridge_vent | VENT_RIDGE | 1.0 | 0.03 |  |
| gable_vent | VENT_GABLE | 1.0 | 0.25 |  |
| delivery | DELIVERY_LUMP | 1.0 | 0.0 |  |
| permit | PERMIT_LUMP | 1.0 | 0.0 |  |
| site_prep | SITE_PREP_LUMP | 1.0 | 0.0 |  |
| door_framing | LBR_2X6_LF | 1.05 | 0.05 |  |
| window_framing | LBR_2X6_LF | 1.05 | 0.05 |  |
| door_trim | TRIM_DOOR | 1.1 | 0.02 |  |
| window_trim | TRIM_WINDOW | 1.1 | 0.02 |  |

---

**Generated:** 2025-11-23 15:13:36.242186
**Total Parts:** 26
**Total Pricing Entries:** 26
**Total Assemblies:** 37
