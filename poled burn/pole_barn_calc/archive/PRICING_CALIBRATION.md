# Pricing Calibration Document

## Purpose

This document tracks the calibration of pole barn calculator pricing against real-world public benchmarks. The goal is to ensure our baseline shell pricing sits in a realistic range for simple pole barns.

**Scope:**
- We are calibrating to **shell pricing only** (no interior finishes, MEP beyond basic allowances, etc.)
- We are using publicly available benchmark ranges from national providers and cost guides
- We are **not** scraping proprietary configurators or violating ToS
- We are only tuning **price data** in `config/pricing.example.csv`, not the structural logic or material takeoff quantities

**What we are NOT changing:**
- Overall pricing architecture or formulas (markup, tax, etc.)
- Material takeoff logic — quantities are assumed correct for now
- Assembly calculations

---

## Phase 1: Standard Test Buildings

### TEST A — "Basic 30x40 Shop"

**Inputs:**
- Dimensions: 30' × 40' footprint
- Eave height: 12'
- Roof: Gable, 4/12 pitch (roof_pitch = 4/12 = 0.333)
- Exterior finish: 29ga metal roof and walls
- Doors: 1 man door (3/0 × 6/8), 1 overhead door (10' × 10')
- Windows: 0
- Insulation: None
- Floor type: Gravel
- Interior build-out: None
- MEP: None (allowances = 0)
- Pole spacing: 10' along length
- Overhangs: 1' front, 1' rear, 1' sides

**Expected scope:** Shell only — framing, metal, trim, basic foundation

---

### TEST B — "Standard 40x60 Shop"

**Inputs:**
- Dimensions: 40' × 60' footprint
- Eave height: 12'
- Roof: Gable, 4/12 pitch
- Exterior finish: 29ga metal roof and walls
- Doors: 2 man doors (3/0 × 6/8 each), 2 overhead doors (10' × 10' each)
- Windows: 0
- Insulation: None
- Floor type: Gravel
- Interior build-out: None
- MEP: None (allowances = 0)
- Pole spacing: 10' along length
- Overhangs: 1' front, 1' rear, 1' sides

**Expected scope:** Shell only — larger version of TEST A

---

### TEST C — "Insulated 40x60"

**Inputs:**
- Dimensions: 40' × 60' footprint
- Eave height: 12'
- Roof: Gable, 4/12 pitch
- Exterior finish: 29ga metal roof and walls
- Doors: 2 man doors (3/0 × 6/8), 2 overhead doors (10' × 10')
- Windows: 3 windows (3' × 2' each)
- Insulation: Fiberglass batts (walls and roof)
- Floor type: Gravel
- Interior build-out: None
- MEP: None (allowances = 0)
- Pole spacing: 10' along length
- Overhangs: 1' front, 1' rear, 1' sides

**Expected scope:** Shell + insulation

---

### TEST D — "Large 40x80 Shop" (Optional sanity check)

**Inputs:**
- Dimensions: 40' × 80' footprint
- Eave height: 12'
- Roof: Gable, 4/12 pitch
- Exterior finish: 29ga metal roof and walls
- Doors: 3 man doors, 3 overhead doors (10' × 10')
- Windows: 0
- Insulation: None
- Floor type: Gravel
- Interior build-out: None
- MEP: None
- Pole spacing: 10' along length
- Overhangs: 1' front, 1' rear, 1' sides

**Expected scope:** Shell only — larger building for scale check

---

## Phase 2: Our Current Estimates

### Test Results (Before Calibration)

| Test | Dimensions | Total Cost | Cost per sq ft | Notes |
|------|------------|------------|----------------|-------|
| TEST A | 30×40 (1,200 sq ft) | $17,237 | $14.36/sqft | Basic shell |
| TEST B | 40×60 (2,400 sq ft) | $27,443 | $11.43/sqft | Standard shell |
| TEST C | 40×60 (2,400 sq ft) | $38,440 | $16.02/sqft | Insulated shell |
| TEST D | 40×80 (3,200 sq ft) | $34,709 | $10.85/sqft | Large shell |

**Breakdown (TEST B - Standard 40x60):**
- Material: $12,646
- Labor: $11,737
- Markup: $1,897
- Tax: $1,163

---

## Phase 3: Public Benchmark Data

### Benchmark Sources

| Source | Link/Reference | Size | Scope | Price Range | Implied $/sqft | Notes |
|--------|----------------|------|-------|-------------|----------------|-------|
| HomeGuide | homeguide.com | 40×60 | Installed | $36,000 - $96,000 | $15 - $40 | National averages, includes labor |
| Mueller Inc. | muellerinc.com | 40×60×14 | Kit only | $12,995 | ~$5.41 | Materials only, no labor |
| Builder's Discount | buildersdiscount.net | 40×60 | Kit only | $10,518 | ~$4.38 | Materials only |
| New Holland Supply | newhollandsupply.com | 40×60×12 | Kit | $20,949 | ~$8.73 | Kit with doors |
| Fixr.com | fixr.com | 40×60 | Installed | $48,000 - $144,000 | $20 - $60 | Post-frame construction |
| Summertown Metals | summertownmetals.com | 40×60 | Installed | $55,200 (AL) | $23 | State-specific average |
| Summertown Metals | summertownmetals.com | 40×60 | Installed | $76,800 (CA) | $32 | State-specific average |

### Typical Price Ranges (from research)

**40×60 Pole Barns (2,400 sq ft):**
- **Kit only (materials):** $10,500 - $21,000 ($4.38 - $8.75/sqft)
- **Installed (shell):** $36,000 - $96,000 ($15 - $40/sqft)
- **Typical installed range:** $15 - $25/sqft for basic shell

**30×40 Pole Barns (1,200 sq ft):**
- **Estimated from 40×60 ratios:**
  - Kit only: ~$5,250 - $10,500 ($4.38 - $8.75/sqft)
  - Installed: ~$18,000 - $48,000 ($15 - $40/sqft)
  - Typical installed: $15 - $25/sqft

**Insulated 40×60:**
- **Estimated:** Add $2-5/sqft for insulation
- **Typical range:** $17 - $30/sqft (shell + insulation)

**Key Findings:**
- Material-only kits: $4-9/sqft
- Installed shell (with labor): $15-40/sqft
- Our estimates include labor, so we should compare to "installed" ranges
- Target range for our shell pricing: $15-25/sqft

---

## Phase 4: Comparison & Calibration Summary

### Calibration Analysis

| Test | Our $/sqft | Benchmark Range | Deviation | Status | Notes |
|------|------------|----------------|-----------|--------|-------|
| TEST A | $14.36 | $15 - $25 | -4.3% | **BELOW** | Slightly below low end |
| TEST B | $11.43 | $15 - $25 | -23.8% | **TOO LOW** | Well below typical range |
| TEST C | $16.02 | $17 - $30 | -5.8% | **BELOW** | Close to low end for insulated |
| TEST D | $10.85 | $15 - $25 | -27.7% | **TOO LOW** | Well below typical range |

**Analysis:**
- **TEST A (30×40):** At $14.36/sqft, we're just below the typical $15-25/sqft range. This is acceptable but could be slightly higher.
- **TEST B (40×60):** At $11.43/sqft, we're **23.8% below** the low end of typical pricing. This suggests our material or labor costs are too low.
- **TEST C (40×60 insulated):** At $16.02/sqft, we're close to the low end for insulated buildings ($17-30/sqft). Reasonable but could be slightly higher.
- **TEST D (40×80):** At $10.85/sqft, we're **27.7% below** typical. Similar issue to TEST B.

**Target:** Our prices should fall within $15-25/sqft for basic shell, $17-30/sqft for insulated. We need to increase material costs by approximately **20-30%** to reach the target range.

---

## Phase 5: Proposed Pricing Adjustments

### Adjustment Strategy

Based on comparison results, we will propose adjustments to `config/pricing.example.csv`:

**Focus areas:**
- Core structural components: posts, trusses, purlins, girts
- Metal panels (roof and wall)
- Insulation materials
- Trim and fasteners

**What we will NOT change:**
- Soft costs (delivery, permit, site prep)
- MEP allowances (handled separately)
- Markup percentages (business logic)

### Recommended Adjustments

| Part ID | Part Name | Old Unit Price | New Unit Price | Justification |
|---------|-----------|----------------|----------------|---------------|
| POST_6X6_PT | 6x6 PT Post | $60.00 | $75.00 | Core structural component, 25% increase to align with market |
| TRUSS_STD | Standard Truss | $250.00 | $312.50 | Major cost driver, 25% increase |
| METAL_PANEL_29_SQFT | Metal Panel 29ga | $1.16 | $1.45 | Large quantity item, 25% increase |
| METAL_PANEL_26_SQFT | Metal Panel 26ga | $1.45 | $1.81 | Large quantity item, 25% increase |
| LBR_2X6_LF | 2x6 Lumber | $0.93 | $1.16 | Framing lumber, 25% increase |
| TRIM_EAVE | Eave Trim | $2.50 | $3.13 | Trim components, 25% increase |
| TRIM_RAKE | Rake Trim | $2.50 | $3.13 | Trim components, 25% increase |
| TRIM_BASE | Base Trim | $2.50 | $3.13 | Trim components, 25% increase |
| TRIM_CORNER | Corner Trim | $2.50 | $3.13 | Trim components, 25% increase |
| TRIM_DOOR | Door Trim | $2.50 | $3.13 | Trim components, 25% increase |
| TRIM_WINDOW | Window Trim | $2.50 | $3.13 | Trim components, 25% increase |
| RIDGE_CAP | Ridge Cap | $3.00 | $3.75 | Trim component, 25% increase |
| OVERHEAD_DOOR | Overhead Door | $850.00 | $1,062.50 | Major component, 25% increase |

**Adjustment Strategy:**
- Applied 25% increase to core structural and skin materials (posts, trusses, metal panels, lumber, trim, doors)
- This should bring TEST B from $11.43/sqft to approximately $14.30/sqft (within target range)
- Soft costs (delivery, permit, site prep) unchanged
- Concrete and insulation prices unchanged (less impact on total)
- Fasteners and ventilation unchanged (smaller cost items)

---

## Phase 6: After Calibration Results

### Test Results (After Calibration)

| Test | Dimensions | Total Cost | Cost per sq ft | Change from Before |
|------|------------|------------|----------------|-------------------|
| TEST A | 30×40 (1,200 sq ft) | $19,745 | $16.45/sqft | +14.6% |
| TEST B | 40×60 (2,400 sq ft) | $31,365 | $13.07/sqft | +14.4% |
| TEST C | 40×60 (2,400 sq ft) | $42,422 | $17.68/sqft | +10.4% |
| TEST D | 40×80 (3,200 sq ft) | $39,664 | $12.40/sqft | +14.3% |

**Calibration Results:**
- **TEST A:** Now at $16.45/sqft - **WITHIN** target range ($15-25/sqft) ✅
- **TEST B:** Now at $13.07/sqft - Still **BELOW** target range ($15-25/sqft), but improved
- **TEST C:** Now at $17.68/sqft - **WITHIN** target range for insulated ($17-30/sqft) ✅
- **TEST D:** Now at $12.40/sqft - Still **BELOW** target range ($15-25/sqft)

**Analysis:**
- The 25% increase on core materials brought TEST A and TEST C into acceptable ranges
- TEST B and TEST D (larger buildings) are still below target, suggesting economies of scale may be affecting the calculation, or additional adjustments may be needed
- Overall improvement: All tests increased by 10-15%, bringing us closer to market pricing

---

## Next Steps for Review

Items for Karl to review:

1. **Part-specific pricing:**
   - Which parts/prices feel off relative to local supplier knowledge?
   - Are there regional price differences we should account for?

2. **Local vendor overrides:**
   - Suggestions for creating a "local vendor override" pricing file
   - How to structure vendor-specific pricing profiles

3. **Calibration validation:**
   - Do the adjusted prices feel realistic for your market?
   - Are there specific components that need further tuning?

---

## Notes

- Backup of original pricing file: `config/pricing.before_calibration.csv`
- All adjustments are documented in this file
- Pricing can be reverted using the backup file if needed

## Calibration Summary

**Status:** ✅ **PARTIALLY COMPLETE**

**What was done:**
1. ✅ Defined 4 standard test buildings
2. ✅ Ran calculator on all test cases
3. ✅ Gathered public benchmark data from multiple sources
4. ✅ Compared our estimates to benchmarks
5. ✅ Applied 25% increase to core structural materials
6. ✅ Re-ran tests and validated improvements

**Results:**
- TEST A (30×40): Now within target range ($16.45/sqft vs $15-25/sqft)
- TEST B (40×60): Improved but still below target ($13.07/sqft vs $15-25/sqft)
- TEST C (40×60 insulated): Now within target range ($17.68/sqft vs $17-30/sqft)
- TEST D (40×80): Improved but still below target ($12.40/sqft vs $15-25/sqft)

**Next Steps for Review:**
1. Review TEST B and TEST D - consider additional 10-15% increase on materials if needed
2. Validate pricing against local supplier knowledge
3. Consider regional pricing adjustments if applicable
4. Test with real project data when available

