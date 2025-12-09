# Pole Barn Calculator - Control Document

## Overview

This document lists and describes all variables collected for the pole barn calculator. The calculator is designed to compute material quantities, labor requirements, and total costs for pole barn construction projects.

## Variable Categories

The variables are organized into four main categories:
1. **Geometry Inputs** - Physical dimensions and layout
2. **Material Inputs** - Material specifications and preferences
3. **Pricing Inputs** - Cost and pricing parameters
4. **Assembly Inputs** - Construction method and assembly details

---

## 1. Geometry Inputs

### Core Dimensions

| Variable | Type | Unit | Description | Required |
|----------|------|------|-------------|----------|
| `length` | float | feet | Length of the barn along the long axis | Yes |
| `width` | float | feet | Width of the barn along the short axis | Yes |
| `eave_height` | float | feet | Height from ground to the eave (lowest point of roof) | Yes |
| `peak_height` | float | feet | Height from ground to the peak/ridge of the roof | Yes |
| `roof_pitch` | float | ratio | Roof pitch as a ratio (e.g., 4:12 = 0.333) | Yes |

### Overhangs

| Variable | Type | Unit | Description | Required |
|----------|------|------|-------------|----------|
| `overhang_front` | float | feet | Overhang distance on the front of the barn | No (default: 0.0) |
| `overhang_rear` | float | feet | Overhang distance on the rear of the barn | No (default: 0.0) |
| `overhang_sides` | float | feet | Overhang distance on both sides of the barn | No (default: 0.0) |

### Doors

| Variable | Type | Unit | Description | Required |
|----------|------|------|-------------|----------|
| `door_count` | int | count | Number of doors in the barn | No (default: 0) |
| `door_width` | float | feet | Width of each door | No (default: 0.0) |
| `door_height` | float | feet | Height of each door | No (default: 0.0) |

### Windows

| Variable | Type | Unit | Description | Required |
|----------|------|------|-------------|----------|
| `window_count` | int | count | Number of windows in the barn | No (default: 0) |
| `window_width` | float | feet | Width of each window | No (default: 0.0) |
| `window_height` | float | feet | Height of each window | No (default: 0.0) |

### Pole Configuration

| Variable | Type | Unit | Description | Required |
|----------|------|------|-------------|----------|
| `pole_spacing_length` | float | feet | Spacing between poles along the length dimension | Yes |
| `pole_spacing_width` | float | feet | Spacing between poles along the width dimension | Yes |
| `pole_diameter` | float | inches | Diameter of the poles | Yes |
| `pole_depth` | float | feet | Depth that poles are set into the ground | Yes |

---

## 2. Material Inputs

### Roofing Materials

| Variable | Type | Unit | Description | Required |
|----------|------|------|-------------|----------|
| `roof_material_type` | string | - | Type of roofing material (e.g., "metal", "shingle", "tile") | Yes |
| `roof_gauge` | float | gauge | Gauge/thickness for metal roofing (if applicable) | No |

### Wall Materials

| Variable | Type | Unit | Description | Required |
|----------|------|------|-------------|----------|
| `wall_material_type` | string | - | Type of wall material (e.g., "metal", "wood", "composite") | Yes |
| `wall_gauge` | float | gauge | Gauge/thickness for metal walls (if applicable) | No |

### Structural Components

| Variable | Type | Unit | Description | Required |
|----------|------|------|-------------|----------|
| `truss_type` | string | - | Type of truss (e.g., "scissor", "standard", "gambrel") | Yes |
| `truss_spacing` | float | feet | Spacing between trusses | Yes |
| `purlin_spacing` | float | feet | Spacing between purlins (horizontal roof supports) | Yes |
| `girt_spacing` | float | feet | Spacing between girts (horizontal wall supports) | Yes |

### Foundation

| Variable | Type | Unit | Description | Required |
|----------|------|------|-------------|----------|
| `foundation_type` | string | - | Type of foundation (e.g., "concrete_pad", "gravel", "none") | Yes |
| `concrete_thickness` | float | inches | Thickness of concrete (if applicable) | No |

### Insulation

| Variable | Type | Unit | Description | Required |
|----------|------|------|-------------|----------|
| `insulation_type` | string | - | Type of insulation (e.g., "fiberglass", "spray_foam", "none") | No |
| `insulation_r_value` | float | R-value | R-value rating of insulation (if applicable) | No |

---

## 3. Pricing Inputs

### Labor and Markup

| Variable | Type | Unit | Description | Required |
|----------|------|------|-------------|----------|
| `labor_rate` | float | dollars/hour | Labor cost per hour | Yes |
| `material_markup` | float | multiplier | Markup on materials (e.g., 1.15 for 15% markup) | Yes |
| `tax_rate` | float | decimal | Tax rate as decimal (e.g., 0.08 for 8%) | Yes |

### Additional Costs

| Variable | Type | Unit | Description | Required |
|----------|------|------|-------------|----------|
| `delivery_cost` | float | dollars | Delivery cost for materials | No |
| `permit_cost` | float | dollars | Cost of building permits | No |
| `site_prep_cost` | float | dollars | Site preparation costs | No |

---

## 4. Assembly Inputs

### Construction Method

| Variable | Type | Unit | Description | Required |
|----------|------|------|-------------|----------|
| `assembly_method` | string | - | Assembly method (e.g., "standard", "prefab", "custom") | Yes |
| `fastening_type` | string | - | Type of fasteners (e.g., "screws", "nails", "welded") | Yes |
| `weather_sealing` | boolean | - | Whether to include weather sealing | No (default: False) |

### Ventilation

| Variable | Type | Unit | Description | Required |
|----------|------|------|-------------|----------|
| `ventilation_type` | string | - | Type of ventilation (e.g., "ridge_vent", "gable_vent", "none") | No |
| `ventilation_count` | int | count | Number of ventilation units | No |

### Skylights

| Variable | Type | Unit | Description | Required |
|----------|------|------|-------------|----------|
| `skylight_count` | int | count | Number of skylights | No |
| `skylight_size` | float | square feet | Size of each skylight | No |

---

## 5. Project Metadata

| Variable | Type | Unit | Description | Required |
|----------|------|------|-------------|----------|
| `project_name` | string | - | Optional project identifier or name | No |
| `notes` | string | - | Optional notes or special requirements | No |

---

## Variable Relationships

### Dependencies

- **Roof calculations** depend on: `length`, `width`, `roof_pitch`, `overhang_*`
- **Wall calculations** depend on: `length`, `width`, `eave_height`, `door_*`, `window_*`
- **Pole count** depends on: `length`, `width`, `pole_spacing_length`, `pole_spacing_width`
- **Truss quantity** depends on: `length`, `truss_spacing`
- **Material quantities** depend on: geometry calculations + material specifications
- **Costs** depend on: material quantities + pricing inputs

### Validation Rules

1. `peak_height` must be greater than `eave_height`
2. `roof_pitch` should be between 0 and 1 (0:12 to 12:12)
3. If `door_count > 0`, then `door_width` and `door_height` must be > 0
4. If `window_count > 0`, then `window_width` and `window_height` must be > 0
5. `pole_spacing_*` values should be reasonable (typically 8-12 feet)
6. `truss_spacing` typically ranges from 2-4 feet
7. `material_markup` should be >= 1.0
8. `tax_rate` should be between 0 and 1

---

## Calculation Outputs (Future)

The following outputs will be calculated from these inputs:

### Geometry Outputs
- Roof area (square feet)
- Wall areas (square feet per side)
- Floor area (square feet)
- Pole count
- Door/window opening areas
- Roof volume (cubic feet)

### Quantity Outputs
- Truss quantity
- Purlin quantity and lengths
- Girt quantity and lengths
- Roofing material quantity
- Wall material quantity
- Fastener quantities
- Concrete quantity
- Insulation quantity
- Ventilation components

### Cost Outputs
- Material costs (by category)
- Labor costs
- Subtotal
- Taxes
- Total project cost
- Cost breakdown by category

---

## Notes

- All linear dimensions are in **feet**
- All areas are in **square feet**
- All volumes are in **cubic feet**
- Pole diameter is in **inches** (industry standard)
- Concrete thickness is in **inches** (industry standard)
- Angles/pitches are expressed as **ratios** (not degrees)
- Costs are in **dollars** (USD)

---

*Document Version: 1.0*  
*Last Updated: Initial creation*

