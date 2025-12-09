# Pole Barn Calculator - Full Project Export

This document contains the complete project structure and code for review.

**Generated:** 1763939643.155

---

## Project Directory Tree

```
pole_barn_calc/
├── APP_WORKFLOW_GUIDE.md
├── apps
│   ├── __init__.py
│   ├── cli.py
│   └── gui.py
├── ASSEMBLIES_CHANGELOG.md
├── ASSEMBLIES_DESIGN.md
├── ASSEMBLIES_IMPLEMENTATION_SUMMARY.md
├── ASSEMBLIES_STATUS.md
├── build_exe.bat
├── build_exe.spec
├── config
│   ├── assemblies.example.csv
│   ├── parts.example.csv
│   ├── pricing.before_calibration.csv
│   └── pricing.example.csv
├── control
│   └── pole_barn_calculator.md
├── DESKTOP_APP_GUIDE.md
├── DESKTOP_APP_SUMMARY.md
├── GUI_CHANGELOG.md
├── GUI_VERIFICATION_GUIDE.md
├── IMPLEMENTATION_READINESS_SUMMARY.md
├── launch_gui_fresh.bat
├── MATERIALS_LIBRARY_EXPORT.md
├── NEXT_STEPS.md
├── PATH_B_IMPLEMENTATION_STATUS.md
├── PRICING_CALIBRATION.md
├── PROJECT_EXPORT_FULL.md
├── PROJECT_REVIEW.md
├── pyproject.toml
├── README.md
├── run_calculator.bat
├── run_calibration_tests.py
├── run_example.bat
├── run_gui.bat
├── SETUP_AND_FIXES.md
├── SNOW_LOAD_DATA_SOURCE.md
├── systems
│   ├── __init__.py
│   └── pole_barn
│       ├── __init__.py
│       ├── assemblies.py
│       ├── calculator.py
│       ├── geometry.py
│       ├── model.py
│       └── pricing.py
├── TESTING_READY_SUMMARY.md
├── tests
│   ├── test_assemblies.py
│   ├── test_end_to_end.py
│   ├── test_geometry.py
│   └── test_pricing.py
├── tools
│   ├── export_full_project.py
│   └── export_material_library.py
└── verify_gui_changes.py
```

---

## Core Code Files

### File: systems/pole_barn/model.py

```python
"""Data models for pole barn calculator inputs."""

from dataclasses import dataclass
from typing import Optional, List


@dataclass
class GeometryInputs:
    """Geometric dimensions and layout inputs for the pole barn."""
    
    # Required fields (no defaults) - must come first
    length: float  # Length of the barn in feet
    width: float  # Width of the barn in feet
    eave_height: float  # Height to the eave (lowest point of roof) in feet
    roof_pitch: float  # Roof pitch ratio (e.g., 4:12 = 4/12 = 0.333)
    overhang_front: float  # Front overhang in feet
    overhang_rear: float  # Rear overhang in feet
    overhang_sides: float  # Side overhangs in feet
    door_count: int  # Number of doors
    door_width: float  # Width of each door in feet
    door_height: float  # Height of each door in feet
    window_count: int  # Number of windows
    window_width: float  # Width of each window in feet
    window_height: float  # Height of each window in feet
    pole_spacing_length: float  # Spacing between poles along length in feet
    pole_spacing_width: float  # Spacing between poles along width in feet
    pole_diameter: float  # Diameter of poles in inches
    pole_depth: float  # Depth poles are set into ground in feet
    
    # Optional fields (with defaults) - must come after required fields
    peak_height: Optional[float] = None  # Height to the peak/ridge in feet (derived if not provided)
    roof_style: str = "gable"  # "gable" or "shed" (per changelog entry [1])
    ridge_position_ft_from_left: Optional[float] = None  # Ridge position from left eave in feet (per changelog entry [1])
    overhead_door_count: int = 0  # Number of overhead/roll-up doors (per changelog entry [17])
    overhead_door_type: str = "none"  # "none", "steel_rollup", "sectional" (per changelog entry [17])


@dataclass
class MaterialInputs:
    """Material specifications and preferences."""
    
    # Required fields (no defaults) - must come first
    roof_material_type: str  # e.g., "metal", "shingle", "tile"
    wall_material_type: str  # e.g., "metal", "wood", "composite"
    truss_type: str  # e.g., "scissor", "standard", "gambrel"
    truss_spacing: float  # Spacing between trusses in feet
    purlin_spacing: float  # Spacing between purlins in feet
    girt_spacing: float  # Spacing between girts in feet
    foundation_type: str  # e.g., "concrete_pad", "gravel", "none"
    
    # Optional fields (with defaults) - must come after required fields
    roof_gauge: Optional[float] = None  # Gauge for metal roofing
    wall_gauge: Optional[float] = None  # Gauge for metal walls
    concrete_thickness: Optional[float] = None  # Thickness of concrete in inches
    insulation_type: Optional[str] = None  # e.g., "fiberglass", "spray_foam", "none" (deprecated - use wall/roof_insulation_type)
    insulation_r_value: Optional[float] = None  # R-value if insulated (deprecated)
    exterior_finish_type: str = "metal_29ga"  # "metal_29ga", "metal_26ga", "lap_siding", "stucco"
    wall_insulation_type: str = "none"  # "none", "fiberglass_batts", "rock_wool", "rigid_board", "spray_foam"
    roof_insulation_type: str = "none"  # "none", "fiberglass_batts", "rock_wool", "rigid_board", "spray_foam"
    slab_thickness_in: Optional[float] = None  # Slab thickness in inches (if floor_type is "slab")
    slab_reinforcement: str = "none"  # "none", "mesh", "rebar"
    girt_type: str = "standard"  # "standard" or "commercial" (per changelog entry [5])
    wall_sheathing_type: str = "none"  # "none", "osb", "plywood" (per changelog entry [6])
    roof_sheathing_type: str = "none"  # "none", "osb", "plywood" (per changelog entry [7])
    floor_type: str = "none"  # "none", "slab", "gravel" (per changelog entry [8])


@dataclass
class PricingInputs:
    """Pricing and cost inputs."""
    
    # Legacy field for backward compatibility (material_markup as multiplier, e.g., 1.15 for 15%)
    material_markup: float  # Markup multiplier on materials (e.g., 1.15 for 15%)
    tax_rate: float  # Tax rate as decimal (e.g., 0.08 for 8%)
    labor_rate: float = 50.0  # Labor cost per hour (default, can be overridden via config)
    delivery_cost: Optional[float] = None  # Delivery cost if applicable
    permit_cost: Optional[float] = None  # Permit costs
    site_prep_cost: Optional[float] = None  # Site preparation costs
    # MEP allowances (per changelog entry [18])
    include_electrical: bool = False  # Include basic electrical
    electrical_allowance: float = 0.0  # Electrical allowance in dollars
    include_plumbing: bool = False  # Include plumbing
    plumbing_allowance: float = 0.0  # Plumbing allowance in dollars
    include_mechanical: bool = False  # Include mechanical (heat/vent)
    mechanical_allowance: float = 0.0  # Mechanical allowance in dollars
    # Granular markup controls (new fields)
    material_markup_pct: float = 15.0  # Material markup as percentage (e.g., 15.0 for 15%)
    labor_markup_pct: float = 10.0  # Labor markup as percentage (e.g., 10.0 for 10%)
    subcontractor_markup_pct: float = 10.0  # Subcontractor markup as percentage
    overhead_pct: float = 0.0  # Overhead as percentage of (material + labor) before profit


@dataclass
class AssemblyInputs:
    """Assembly and construction method inputs."""
    
    assembly_method: str  # e.g., "standard", "prefab", "custom"
    fastening_type: str  # e.g., "screws", "nails", "welded"
    weather_sealing: bool  # Whether to include weather sealing
    ventilation_type: Optional[str] = None  # e.g., "ridge_vent", "gable_vent", "none"
    ventilation_count: Optional[int] = None  # Number of ventilation units
    skylight_count: Optional[int] = None  # Number of skylights
    skylight_size: Optional[float] = None  # Size of skylights in square feet
    post_type: str = "pt_solid"  # "pt_solid" or "laminated" (per changelog entry [19])
    post_truss_connection_type: str = "notched"  # "notched" or "cleated" (per changelog entry [20])


@dataclass
class GeometryModel:
    """Derived geometry model with calculated dimensions and areas."""
    
    # Core dimensions (echoed from inputs for reference)
    overall_length_ft: float
    overall_width_ft: float
    eave_height_ft: float
    peak_height_ft: float
    sidewall_overhang_ft: float  # Overhang on sides
    endwall_overhang_front_ft: float  # Front overhang
    endwall_overhang_rear_ft: float  # Rear overhang
    
    # Bays / frames
    bay_spacing_ft: float  # Spacing between frame lines along length
    num_bays: int  # Number of bays
    num_frame_lines: int  # Number of frame lines (bays + 1)
    
    # Areas
    footprint_area_sqft: float  # Plan view area (length × width)
    sidewall_area_sqft: float  # Total area of both sidewalls
    endwall_area_sqft: float  # Total area of both endwalls
    total_wall_area_sqft: float  # Total wall area
    roof_area_sqft: float  # Roof surface area accounting for pitch
    
    # Volume (optional)
    building_volume_cuft: Optional[float] = None  # Building volume in cubic feet


@dataclass
class AssemblyQuantity:
    """A single material quantity item."""
    
    name: str  # e.g., "posts", "sidewall_girts", "roof_purlins"
    description: str  # Human-readable description
    category: str  # e.g., "framing", "roof", "wall", "trim", "foundation"
    quantity: float  # Numeric amount
    unit: str  # "ea", "lf", "sqft"
    notes: Optional[str] = None  # Optional notes


@dataclass
class MaterialTakeoff:
    """Container for all material quantities."""
    
    items: List[AssemblyQuantity]
    
    def get_by_category(self, category: str) -> List[AssemblyQuantity]:
        """Get all items in a specific category."""
        return [item for item in self.items if item.category == category]
    
    def get_by_name(self, name: str) -> Optional[AssemblyQuantity]:
        """Get an item by name."""
        for item in self.items:
            if item.name == name:
                return item
        return None


@dataclass
class PricedLineItem:
    """A fully priced line item with material, labor, and markup costs."""
    
    name: str  # e.g., "roof_panels", "sidewall_girts"
    description: str
    category: str  # "framing", "roof", "wall", "trim", "insulation", etc.
    quantity: float
    unit: str  # "ea", "lf", "sqft"
    part_id: Optional[str] = None  # Part ID if mapped
    unit_price: float = 0.0  # Material unit price (before markup)
    material_cost: float = 0.0
    labor_hours: float = 0.0
    labor_rate: float = 0.0
    labor_cost: float = 0.0
    markup_percent: float = 0.0
    markup_amount: float = 0.0
    total_cost: float = 0.0  # material_cost + labor_cost + markup_amount
    notes: Optional[str] = None


@dataclass
class PricingSummary:
    """Rollup totals for pricing."""
    
    material_subtotal: float
    labor_subtotal: float
    markup_total: float
    tax_total: float
    grand_total: float


@dataclass
class PoleBarnInputs:
    """Complete set of inputs for pole barn calculation."""
    
    geometry: GeometryInputs
    materials: MaterialInputs
    pricing: PricingInputs
    assemblies: AssemblyInputs
    project_name: Optional[str] = None  # Optional project identifier
    notes: Optional[str] = None  # Optional notes or special requirements
    # Project/Permit fields (per changelog entries [11], [12])
    build_type: str = "pole"  # "pole" or "stick_frame" (per changelog entry [12])
    construction_type: str = "new"  # "new" or "addition" (per changelog entry [12])
    building_type: str = "residential"  # "residential" or "commercial" (per changelog entry [11])
    building_use: Optional[str] = None  # Building use/description (per changelog entry [11])
    permitting_agency: Optional[str] = None  # Permitting agency (per changelog entry [11])
    required_snow_load_psf: Optional[float] = None  # Required snow load in psf (per changelog entry [11])
    requested_snow_load_psf: Optional[float] = None  # Requested snow load in psf (per changelog entry [11])
    snow_load_unknown: bool = False  # Flag if snow load needs lookup (per changelog entry [11])

```

---

### File: systems/pole_barn/geometry.py

```python
"""Geometry calculations for pole barn dimensions."""

import math
from typing import Dict, Any
from .model import GeometryInputs, GeometryModel


def _calculate_roof_slope_factor(roof_pitch: float) -> float:
    """
    Calculate the slope factor for roof area calculation.
    
    The roof_pitch is stored as a ratio (e.g., 0.333 for 4:12).
    Slope factor = sqrt(1 + (rise/run)^2)
    
    Args:
        roof_pitch: Roof pitch as a ratio (e.g., 0.333 for 4:12)
        
    Returns:
        Slope factor for calculating roof surface area
    """
    # roof_pitch is already a ratio (rise/run)
    # For 4:12, roof_pitch = 4/12 = 0.333
    return math.sqrt(1 + roof_pitch ** 2)


def build_geometry_model(inputs: GeometryInputs) -> GeometryModel:
    """
    Build a complete geometry model from geometry inputs.
    
    This is the main function that calculates all derived geometry values.
    
    Args:
        inputs: Geometry inputs containing dimensions
        
    Returns:
        GeometryModel with all calculated values
    """
    L = inputs.length
    W = inputs.width
    H = inputs.eave_height
    bay_spacing = inputs.pole_spacing_length  # Bay spacing along length
    
    # Overhangs
    oh_side = inputs.overhang_sides
    oh_front = inputs.overhang_front
    oh_rear = inputs.overhang_rear
    
    # Calculate bays and frames
    num_bays = math.ceil(L / bay_spacing) if bay_spacing > 0 else 0
    num_frame_lines = num_bays + 1
    
    # Footprint area (plan view, no overhangs)
    footprint_area_sqft = L * W
    
    # Wall areas (ignoring door/window cut-outs for now)
    sidewall_area_sqft = 2 * L * H  # Two sidewalls
    endwall_area_sqft = 2 * W * H  # Two endwalls
    total_wall_area_sqft = sidewall_area_sqft + endwall_area_sqft
    
    # Roof area with pitch and overhangs
    # Effective plan dimensions include overhangs
    L_eff = L + oh_front + oh_rear
    W_eff = W + 2 * oh_side
    
    # Calculate slope factor from roof pitch
    slope_factor = _calculate_roof_slope_factor(inputs.roof_pitch)
    
    # Plan area (with overhangs)
    plan_area_sqft = L_eff * W_eff
    
    # Roof surface area = plan area × slope factor
    roof_area_sqft = plan_area_sqft * slope_factor
    
    # Building volume (simple box approximation using eave height)
    building_volume_cuft = footprint_area_sqft * H
    
    # Derive peak height if not provided (per changelog entry [4])
    # For gable roof with centered ridge: rise = (width / 2) * roof_pitch
    if inputs.peak_height is None:
        # Calculate rise from roof pitch and building width
        # For a gable roof, the ridge is at the center, so run = width / 2
        run_ft = W / 2.0
        rise_ft = run_ft * inputs.roof_pitch
        peak_height_ft = H + rise_ft
    else:
        peak_height_ft = inputs.peak_height
    
    return GeometryModel(
        overall_length_ft=L,
        overall_width_ft=W,
        eave_height_ft=H,
        peak_height_ft=peak_height_ft,
        sidewall_overhang_ft=oh_side,
        endwall_overhang_front_ft=oh_front,
        endwall_overhang_rear_ft=oh_rear,
        bay_spacing_ft=bay_spacing,
        num_bays=num_bays,
        num_frame_lines=num_frame_lines,
        footprint_area_sqft=footprint_area_sqft,
        sidewall_area_sqft=sidewall_area_sqft,
        endwall_area_sqft=endwall_area_sqft,
        total_wall_area_sqft=total_wall_area_sqft,
        roof_area_sqft=roof_area_sqft,
        building_volume_cuft=building_volume_cuft,
    )


def calculate_roof_area(geometry: GeometryInputs) -> float:
    """
    Calculate the total roof area.
    
    Args:
        geometry: Geometry inputs containing dimensions
        
    Returns:
        Total roof area in square feet
    """
    model = build_geometry_model(geometry)
    return model.roof_area_sqft


def calculate_wall_area(geometry: GeometryInputs) -> Dict[str, float]:
    """
    Calculate wall areas for all four sides.
    
    Args:
        geometry: Geometry inputs containing dimensions
        
    Returns:
        Dictionary with keys: 'front', 'rear', 'left', 'right'
        Values are wall areas in square feet
    """
    model = build_geometry_model(geometry)
    L = model.overall_length_ft
    W = model.overall_width_ft
    H = model.eave_height_ft
    
    # Individual wall areas
    front_wall_area = W * H
    rear_wall_area = W * H
    left_wall_area = L * H
    right_wall_area = L * H
    
    return {
        'front': front_wall_area,
        'rear': rear_wall_area,
        'left': left_wall_area,
        'right': right_wall_area,
    }


def calculate_floor_area(geometry: GeometryInputs) -> float:
    """
    Calculate the floor area.
    
    Args:
        geometry: Geometry inputs containing dimensions
        
    Returns:
        Floor area in square feet
    """
    model = build_geometry_model(geometry)
    return model.footprint_area_sqft


def calculate_pole_count(geometry: GeometryInputs) -> int:
    """
    Calculate the number of poles required.
    
    NOTE: This is a placeholder stub. Actual pole counting will be
    implemented in assemblies.py in a later phase, as it depends on
    structural layout and material specifications.
    
    Args:
        geometry: Geometry inputs containing dimensions and pole spacing
        
    Returns:
        Placeholder value (0) - actual calculation deferred to assemblies
        
    Raises:
        NotImplementedError: Actual pole counting not yet implemented
    """
    # Pole counting is deferred to assemblies.py
    # It requires understanding the full structural layout
    raise NotImplementedError(
        "Pole count calculation is deferred to assemblies.py. "
        "It requires structural layout analysis beyond basic geometry."
    )


def calculate_door_window_openings(geometry: GeometryInputs) -> Dict[str, float]:
    """
    Calculate total area of door and window openings.
    
    Args:
        geometry: Geometry inputs containing door and window specifications
        
    Returns:
        Dictionary with 'door_area' and 'window_area' in square feet
    """
    door_area = geometry.door_count * geometry.door_width * geometry.door_height
    window_area = geometry.window_count * geometry.window_width * geometry.window_height
    
    return {
        'door_area': door_area,
        'window_area': window_area,
    }


def calculate_roof_volume(geometry: GeometryInputs) -> float:
    """
    Calculate the volume under the roof (attic/loft space).
    
    This uses a simple box approximation based on eave height.
    For more complex roof shapes (gables, etc.), this would need enhancement.
    
    Args:
        geometry: Geometry inputs containing dimensions
        
    Returns:
        Volume in cubic feet
    """
    model = build_geometry_model(geometry)
    return model.building_volume_cuft or 0.0


def get_geometry_summary(geometry: GeometryInputs) -> Dict[str, Any]:
    """
    Get a summary of all geometry calculations.
    
    Args:
        geometry: Geometry inputs
        
    Returns:
        Dictionary containing all geometry calculations
    """
    model = build_geometry_model(geometry)
    openings = calculate_door_window_openings(geometry)
    
    return {
        'dimensions': {
            'length_ft': model.overall_length_ft,
            'width_ft': model.overall_width_ft,
            'eave_height_ft': model.eave_height_ft,
            'peak_height_ft': model.peak_height_ft,
        },
        'overhangs': {
            'sidewall_ft': model.sidewall_overhang_ft,
            'endwall_front_ft': model.endwall_overhang_front_ft,
            'endwall_rear_ft': model.endwall_overhang_rear_ft,
        },
        'bays': {
            'bay_spacing_ft': model.bay_spacing_ft,
            'num_bays': model.num_bays,
            'num_frame_lines': model.num_frame_lines,
        },
        'areas': {
            'footprint_sqft': model.footprint_area_sqft,
            'sidewall_sqft': model.sidewall_area_sqft,
            'endwall_sqft': model.endwall_area_sqft,
            'total_wall_sqft': model.total_wall_area_sqft,
            'roof_sqft': model.roof_area_sqft,
        },
        'volume': {
            'building_volume_cuft': model.building_volume_cuft,
        },
        'openings': openings,
    }
```

---

### File: systems/pole_barn/assemblies.py

```python
"""Assembly and material quantity calculations."""

import math
from typing import Dict, Any, List, Tuple, Optional, TYPE_CHECKING
from .model import (
    PoleBarnInputs,
    MaterialInputs,
    AssemblyInputs,
    GeometryModel,
    AssemblyQuantity,
    MaterialTakeoff,
)

if TYPE_CHECKING:
    from .model import GeometryInputs

from . import geometry


def calculate_material_quantities(
    geometry_model: GeometryModel,
    material_inputs: MaterialInputs,
    assembly_inputs: AssemblyInputs,
    geometry_inputs: Optional['GeometryInputs'] = None,  # For door/window counts
) -> List[AssemblyQuantity]:
    """
    Calculate all material quantities based on geometry and material/assembly inputs.
    
    This is the main function that orchestrates all quantity calculations.
    
    Args:
        geometry_model: Derived geometry from Phase 1
        material_inputs: Material specifications and spacing
        assembly_inputs: Assembly method and preferences
        
    Returns:
        List of AssemblyQuantity items with all material quantities
    """
    quantities: List[AssemblyQuantity] = []
    
    # Posts (columns)
    post_count = _calculate_post_count(geometry_model)
    quantities.append(AssemblyQuantity(
        name="posts",
        description="Structural posts (columns)",
        category="framing",
        quantity=post_count,
        unit="ea",
        notes=f"One post per frame line on each sidewall ({geometry_model.num_frame_lines} frame lines × 2 sidewalls)",
    ))
    
    # Trusses
    truss_count = _calculate_truss_count(geometry_model, material_inputs)
    quantities.append(AssemblyQuantity(
        name="trusses",
        description=f"{material_inputs.truss_type.title()} trusses",
        category="framing",
        quantity=truss_count,
        unit="ea",
        notes=f"Truss spacing: {material_inputs.truss_spacing}ft",
    ))
    
    # Wall girts
    sidewall_girt_lf, endwall_girt_lf = _calculate_girt_quantities(geometry_model, material_inputs)
    quantities.append(AssemblyQuantity(
        name="sidewall_girts",
        description="Horizontal girts for sidewalls",
        category="framing",
        quantity=sidewall_girt_lf,
        unit="lf",
        notes=f"Girt spacing: {material_inputs.girt_spacing}ft, Height: {geometry_model.eave_height_ft}ft",
    ))
    if endwall_girt_lf > 0:
        quantities.append(AssemblyQuantity(
            name="endwall_girts",
            description="Horizontal girts for endwalls",
            category="framing",
            quantity=endwall_girt_lf,
            unit="lf",
            notes=f"Girt spacing: {material_inputs.girt_spacing}ft",
        ))
    
    # Roof purlins
    purlin_lf = _calculate_purlin_quantities(geometry_model, material_inputs)
    quantities.append(AssemblyQuantity(
        name="roof_purlins",
        description="Roof purlins (horizontal roof supports)",
        category="roof",
        quantity=purlin_lf,
        unit="lf",
        notes=f"Purlin spacing: {material_inputs.purlin_spacing}ft",
    ))
    
    # Roof panels (per changelog entry [15] - exterior finish type)
    # Branch on exterior_finish_type for metal gauge (29ga vs 26ga)
    # TODO: Add support for lap_siding and stucco
    roof_panel_sqft = geometry_model.roof_area_sqft
    if material_inputs.exterior_finish_type == "metal_26ga":
        panel_name = "roof_panels_26ga"  # Use different assembly name for 26ga
        panel_desc = "Roof panels (26ga metal)"
        panel_notes = "26ga metal panels"
    else:
        # Default to 29ga
        panel_name = "roof_panels"
        panel_desc = "Roof panels (29ga metal)"
        panel_notes = "29ga metal panels (default)"
    quantities.append(AssemblyQuantity(
        name=panel_name,
        description=panel_desc,
        category="roof",
        quantity=roof_panel_sqft,
        unit="sqft",
        notes=panel_notes,
    ))
    
    # Wall panels (per changelog entry [15] - exterior finish type)
    sidewall_panel_sqft = geometry_model.sidewall_area_sqft
    endwall_panel_sqft = geometry_model.endwall_area_sqft
    if material_inputs.exterior_finish_type == "metal_26ga":
        sidewall_name = "sidewall_panels_26ga"
        endwall_name = "endwall_panels_26ga"
        wall_panel_desc = "Sidewall panels (26ga metal)"
        wall_panel_notes = "26ga metal panels"
    elif material_inputs.exterior_finish_type in ["lap_siding", "stucco"]:
        # TODO: Implement lap siding and stucco assemblies
        sidewall_name = "sidewall_panels"
        endwall_name = "endwall_panels"
        wall_panel_desc = f"Sidewall panels ({material_inputs.exterior_finish_type})"
        wall_panel_notes = f"{material_inputs.exterior_finish_type} - TODO: implement"
    else:
        # Default to 29ga
        sidewall_name = "sidewall_panels"
        endwall_name = "endwall_panels"
        wall_panel_desc = "Sidewall panels (29ga metal)"
        wall_panel_notes = "29ga metal panels (default)"
    quantities.append(AssemblyQuantity(
        name=sidewall_name,
        description=wall_panel_desc,
        category="wall",
        quantity=sidewall_panel_sqft,
        unit="sqft",
        notes=wall_panel_notes,
    ))
    quantities.append(AssemblyQuantity(
        name=endwall_name,
        description=wall_panel_desc.replace("Sidewall", "Endwall"),
        category="wall",
        quantity=endwall_panel_sqft,
        unit="sqft",
        notes=wall_panel_notes,
    ))
    
    # Trim
    trim_quantities = _calculate_trim_quantities(geometry_model)
    quantities.extend(trim_quantities)
    
    # Door and window assemblies (per changelog entry [14])
    if geometry_inputs:
        door_window_quantities = _calculate_door_window_assemblies(geometry_model, geometry_inputs)
        quantities.extend(door_window_quantities)
    
    # Wall and roof insulation (per changelog entry [16])
    insulation_quantities = _calculate_insulation_quantities(geometry_model, material_inputs)
    quantities.extend(insulation_quantities)
    
    return quantities


def _calculate_door_window_assemblies(
    geometry_model: GeometryModel,
    geometry_inputs: 'GeometryInputs',
) -> List[AssemblyQuantity]:
    """
    Calculate door and window framing and trim quantities (per changelog entry [14]).
    
    Assumptions:
    - Standard door: 3' x 7' (36" x 84")
    - Standard window: 3' x 3' (36" x 36")
    - Door header: 2x8, length = door width + 6"
    - Window header: 2x6, length = window width + 6"
    - King studs: 2 per door/window (one each side)
    - Trimmers/jacks: 2 per door/window
    
    Args:
        geometry_model: Derived geometry
        geometry_inputs: Geometry inputs with door/window counts
        
    Returns:
        List of AssemblyQuantity items for door/window framing and trim
    """
    quantities: List[AssemblyQuantity] = []
    
    door_count = geometry_inputs.door_count
    window_count = geometry_inputs.window_count
    
    # Standard sizes (assumptions for estimator - can be made configurable later)
    STANDARD_DOOR_WIDTH_FT = 3.0  # 36"
    STANDARD_DOOR_HEIGHT_FT = 7.0  # 84"
    STANDARD_WINDOW_WIDTH_FT = 3.0  # 36"
    STANDARD_WINDOW_HEIGHT_FT = 3.0  # 36"
    
    # Door framing
    if door_count > 0:
        # Header: 2x8, length = door width + 6" = door width + 0.5'
        door_header_lf = door_count * (STANDARD_DOOR_WIDTH_FT + 0.5)
        # King studs: 2 per door, full height (use eave height as approximation)
        door_king_studs_lf = door_count * 2 * geometry_model.eave_height_ft
        # Trimmers: 2 per door, door height
        door_trimmers_lf = door_count * 2 * STANDARD_DOOR_HEIGHT_FT
        # Total door framing LF (2x6 equivalent - simplified)
        door_framing_lf = door_header_lf + door_king_studs_lf + door_trimmers_lf
        
        quantities.append(AssemblyQuantity(
            name="door_framing",
            description="Extra framing lumber for doors (headers, studs, trimmers)",
            category="framing",
            quantity=door_framing_lf,
            unit="lf",
            notes=f"Assumes {STANDARD_DOOR_WIDTH_FT}' x {STANDARD_DOOR_HEIGHT_FT}' doors",
        ))
        
        # Door trim: Head + 2 jambs = door width + 2 × door height
        door_trim_lf = door_count * (STANDARD_DOOR_WIDTH_FT + 2 * STANDARD_DOOR_HEIGHT_FT)
        quantities.append(AssemblyQuantity(
            name="door_trim",
            description="Exterior trim for doors (head + jambs)",
            category="trim",
            quantity=door_trim_lf,
            unit="lf",
            notes=f"Per door: {STANDARD_DOOR_WIDTH_FT}' head + 2 × {STANDARD_DOOR_HEIGHT_FT}' jambs",
        ))
    
    # Window framing
    if window_count > 0:
        # Header: 2x6, length = window width + 6" = window width + 0.5'
        window_header_lf = window_count * (STANDARD_WINDOW_WIDTH_FT + 0.5)
        # King studs: 2 per window, full height
        window_king_studs_lf = window_count * 2 * geometry_model.eave_height_ft
        # Trimmers: 2 per window, window height
        window_trimmers_lf = window_count * 2 * STANDARD_WINDOW_HEIGHT_FT
        # Total window framing LF
        window_framing_lf = window_header_lf + window_king_studs_lf + window_trimmers_lf
        
        quantities.append(AssemblyQuantity(
            name="window_framing",
            description="Extra framing lumber for windows (headers, studs, trimmers)",
            category="framing",
            quantity=window_framing_lf,
            unit="lf",
            notes=f"Assumes {STANDARD_WINDOW_WIDTH_FT}' x {STANDARD_WINDOW_HEIGHT_FT}' windows",
        ))
        
        # Window trim: Head + sill + 2 jambs = window width + window width + 2 × window height
        window_trim_lf = window_count * (STANDARD_WINDOW_WIDTH_FT + STANDARD_WINDOW_WIDTH_FT + 2 * STANDARD_WINDOW_HEIGHT_FT)
        quantities.append(AssemblyQuantity(
            name="window_trim",
            description="Exterior trim for windows (head + sill + jambs)",
            category="trim",
            quantity=window_trim_lf,
            unit="lf",
            notes=f"Per window: {STANDARD_WINDOW_WIDTH_FT}' head + {STANDARD_WINDOW_WIDTH_FT}' sill + 2 × {STANDARD_WINDOW_HEIGHT_FT}' jambs",
        ))
    
    return quantities


def _calculate_insulation_quantities(
    geometry_model: GeometryModel,
    material_inputs: MaterialInputs,
) -> List[AssemblyQuantity]:
    """
    Calculate wall and roof insulation quantities (per changelog entry [16]).
    
    Supports different insulation types:
    - fiberglass_batts: Standard fiberglass batts (R-19 typical)
    - rock_wool: Rock wool batts (R-19 equivalent)
    - rigid_board: Rigid board insulation (R-5 per inch)
    - spray_foam: Spray foam insulation (R-6 per inch, closed-cell)
    
    Args:
        geometry_model: Derived geometry
        material_inputs: Material specifications with insulation types
        
    Returns:
        List of AssemblyQuantity items for insulation
    """
    quantities: List[AssemblyQuantity] = []
    
    # Wall insulation
    if material_inputs.wall_insulation_type and material_inputs.wall_insulation_type != "none":
        wall_insulation_sqft = geometry_model.total_wall_area_sqft
        # TODO: Subtract door/window openings for more accuracy
        
        # Use type-specific assembly name for proper part mapping
        if material_inputs.wall_insulation_type == "rock_wool":
            assembly_name = "wall_insulation_rockwool"
        elif material_inputs.wall_insulation_type == "rigid_board":
            assembly_name = "wall_insulation_rigid"
        elif material_inputs.wall_insulation_type == "spray_foam":
            assembly_name = "wall_insulation_sprayfoam"
        else:
            # Default to fiberglass_batts
            assembly_name = "wall_insulation"
        
        quantities.append(AssemblyQuantity(
            name=assembly_name,
            description=f"Wall insulation ({material_inputs.wall_insulation_type})",
            category="insulation",
            quantity=wall_insulation_sqft,
            unit="sqft",
            notes=f"Insulation type: {material_inputs.wall_insulation_type}",
        ))
    
    # Roof insulation
    if material_inputs.roof_insulation_type and material_inputs.roof_insulation_type != "none":
        roof_insulation_sqft = geometry_model.roof_area_sqft
        
        # Use type-specific assembly name for proper part mapping
        if material_inputs.roof_insulation_type == "rock_wool":
            assembly_name = "roof_insulation_rockwool"
        elif material_inputs.roof_insulation_type == "rigid_board":
            assembly_name = "roof_insulation_rigid"
        elif material_inputs.roof_insulation_type == "spray_foam":
            assembly_name = "roof_insulation_sprayfoam"
        else:
            # Default to fiberglass_batts
            assembly_name = "roof_insulation"
        
        quantities.append(AssemblyQuantity(
            name=assembly_name,
            description=f"Roof insulation ({material_inputs.roof_insulation_type})",
            category="insulation",
            quantity=roof_insulation_sqft,
            unit="sqft",
            notes=f"Insulation type: {material_inputs.roof_insulation_type}",
        ))
    
    return quantities


def _calculate_post_count(geometry_model: GeometryModel) -> int:
    """
    Calculate the number of posts (columns) needed.
    
    Assumption: One post per frame line on each sidewall.
    This is a simplified calculation - actual post layout may vary.
    
    Args:
        geometry_model: Derived geometry
        
    Returns:
        Total number of posts
    """
    # One post per frame line on each sidewall
    return geometry_model.num_frame_lines * 2


def _calculate_truss_count(geometry_model: GeometryModel, material_inputs: MaterialInputs) -> int:
    """
    Calculate the number of trusses needed.
    
    If truss_spacing differs from bay spacing, use truss_spacing.
    Otherwise, use one truss per frame line.
    
    Args:
        geometry_model: Derived geometry
        material_inputs: Material specifications
        
    Returns:
        Number of trusses
    """
    # If truss spacing is significantly different from bay spacing, calculate based on truss spacing
    if abs(material_inputs.truss_spacing - geometry_model.bay_spacing_ft) > 0.5:
        # Calculate based on truss spacing
        truss_count = math.ceil(geometry_model.overall_length_ft / material_inputs.truss_spacing) + 1
    else:
        # One truss per frame line (typical post-frame construction)
        truss_count = geometry_model.num_frame_lines
    
    return truss_count


def _calculate_girt_quantities(
    geometry_model: GeometryModel,
    material_inputs: MaterialInputs,
) -> Tuple[float, float]:
    """
    Calculate girt quantities for sidewalls and endwalls.
    
    Args:
        geometry_model: Derived geometry
        material_inputs: Material specifications with girt_spacing
        
    Returns:
        Tuple of (sidewall_girt_lf, endwall_girt_lf)
    """
    girt_spacing = material_inputs.girt_spacing
    
    # Calculate number of girt rows based on eave height
    num_girt_rows = math.ceil(geometry_model.eave_height_ft / girt_spacing) if girt_spacing > 0 else 0
    
    # Sidewall girts: number of rows × length × 2 sidewalls
    sidewall_girt_lf = num_girt_rows * geometry_model.overall_length_ft * 2
    
    # Endwall girts: number of rows × width × 2 endwalls
    endwall_girt_lf = num_girt_rows * geometry_model.overall_width_ft * 2
    
    return sidewall_girt_lf, endwall_girt_lf


def _calculate_purlin_quantities(
    geometry_model: GeometryModel,
    material_inputs: MaterialInputs,
) -> float:
    """
    Calculate purlin quantities for roof.
    
    Args:
        geometry_model: Derived geometry
        material_inputs: Material specifications with purlin_spacing
        
    Returns:
        Total purlin linear feet
    """
    purlin_spacing = material_inputs.purlin_spacing
    
    # Approximate number of purlin rows based on roof width
    # For a gable roof, we approximate using the building width
    # This is simplified - actual purlin layout depends on truss design
    roof_run_approx = geometry_model.overall_width_ft / 2  # Half width for each slope
    
    num_purlin_rows = math.ceil(roof_run_approx / purlin_spacing) if purlin_spacing > 0 else 0
    
    # Effective length includes overhangs
    effective_length = (
        geometry_model.overall_length_ft +
        geometry_model.endwall_overhang_front_ft +
        geometry_model.endwall_overhang_rear_ft
    )
    
    # Purlin LF per slope × 2 slopes
    purlin_lf_per_slope = num_purlin_rows * effective_length
    total_purlin_lf = purlin_lf_per_slope * 2
    
    return total_purlin_lf


def _calculate_trim_quantities(geometry_model: GeometryModel) -> List[AssemblyQuantity]:
    """
    Calculate trim quantities (eave, rake, base, corner).
    
    Args:
        geometry_model: Derived geometry
        
    Returns:
        List of AssemblyQuantity items for trim
    """
    quantities: List[AssemblyQuantity] = []
    
    # Eave trim (along the length, both sides)
    eave_trim_lf = 2 * geometry_model.overall_length_ft
    quantities.append(AssemblyQuantity(
        name="eave_trim",
        description="Eave trim (along length)",
        category="trim",
        quantity=eave_trim_lf,
        unit="lf",
    ))
    
    # Rake trim (gable edges along width)
    rake_trim_lf = 2 * geometry_model.overall_width_ft
    quantities.append(AssemblyQuantity(
        name="rake_trim",
        description="Rake trim (gable edges)",
        category="trim",
        quantity=rake_trim_lf,
        unit="lf",
    ))
    
    # Base trim (perimeter at ground level)
    base_trim_lf = 2 * (geometry_model.overall_length_ft + geometry_model.overall_width_ft)
    quantities.append(AssemblyQuantity(
        name="base_trim",
        description="Base trim (perimeter)",
        category="trim",
        quantity=base_trim_lf,
        unit="lf",
    ))
    
    # Corner trim (vertical corners)
    # 4 corners × eave height
    corner_trim_lf = 4 * geometry_model.eave_height_ft
    quantities.append(AssemblyQuantity(
        name="corner_trim",
        description="Corner trim (vertical corners)",
        category="trim",
        quantity=corner_trim_lf,
        unit="lf",
    ))
    
    return quantities


def calculate_truss_quantity(inputs: PoleBarnInputs) -> int:
    """
    Calculate the number of trusses needed.
    
    Args:
        inputs: Complete pole barn inputs
        
    Returns:
        Number of trusses required
    """
    from . import geometry as geometry_module
    
    geom_model = geometry_module.build_geometry_model(inputs.geometry)
    return _calculate_truss_count(geom_model, inputs.materials)


def calculate_purlin_quantity(inputs: PoleBarnInputs) -> Dict[str, Any]:
    """
    Calculate purlin quantities and lengths.
    
    Args:
        inputs: Complete pole barn inputs
        
    Returns:
        Dictionary with purlin count, total length, and details
    """
    from . import geometry as geometry_module
    
    geom_model = geometry_module.build_geometry_model(inputs.geometry)
    purlin_lf = _calculate_purlin_quantities(geom_model, inputs.materials)
    
    return {
        "total_length_lf": purlin_lf,
        "purlin_spacing_ft": inputs.materials.purlin_spacing,
        "details": "Roof purlins for both slopes",
    }


def calculate_girt_quantity(inputs: PoleBarnInputs) -> Dict[str, Any]:
    """
    Calculate girt quantities and lengths.
    
    Args:
        inputs: Complete pole barn inputs
        
    Returns:
        Dictionary with girt count, total length, and details
    """
    from . import geometry as geometry_module
    
    geom_model = geometry_module.build_geometry_model(inputs.geometry)
    sidewall_girt_lf, endwall_girt_lf = _calculate_girt_quantities(geom_model, inputs.materials)
    
    return {
        "sidewall_length_lf": sidewall_girt_lf,
        "endwall_length_lf": endwall_girt_lf,
        "total_length_lf": sidewall_girt_lf + endwall_girt_lf,
        "girt_spacing_ft": inputs.materials.girt_spacing,
        "details": "Horizontal girts for walls",
    }


def calculate_roofing_material(inputs: PoleBarnInputs) -> Dict[str, Any]:
    """
    Calculate roofing material quantities.
    
    Args:
        inputs: Complete pole barn inputs
        
    Returns:
        Dictionary with material type, quantity, units, and details
    """
    from . import geometry as geometry_module
    
    geom_model = geometry_module.build_geometry_model(inputs.geometry)
    
    return {
        "material_type": inputs.materials.roof_material_type,
        "quantity": geom_model.roof_area_sqft,
        "unit": "sqft",
        "gauge": inputs.materials.roof_gauge,
        "details": f"Roof area including pitch and overhangs",
    }


def calculate_wall_material(inputs: PoleBarnInputs) -> Dict[str, Any]:
    """
    Calculate wall material quantities.
    
    Args:
        inputs: Complete pole barn inputs
        
    Returns:
        Dictionary with material type, quantity, units, and details
    """
    from . import geometry as geometry_module
    
    geom_model = geometry_module.build_geometry_model(inputs.geometry)
    
    return {
        "material_type": inputs.materials.wall_material_type,
        "sidewall_quantity": geom_model.sidewall_area_sqft,
        "endwall_quantity": geom_model.endwall_area_sqft,
        "total_quantity": geom_model.total_wall_area_sqft,
        "unit": "sqft",
        "gauge": inputs.materials.wall_gauge,
        "details": "Wall area (openings tracked separately)",
    }


def calculate_fasteners(inputs: PoleBarnInputs) -> Dict[str, Any]:
    """
    Calculate fastener quantities (screws, nails, etc.).
    
    NOTE: This is a placeholder. Actual fastener calculation requires
    detailed knowledge of fastening patterns and panel sizes.
    
    Args:
        inputs: Complete pole barn inputs
        
    Returns:
        Dictionary with fastener types and quantities
        
    Raises:
        NotImplementedError: Detailed fastener calculation not yet implemented
    """
    raise NotImplementedError(
        "Fastener calculation requires detailed fastening patterns and panel specifications. "
        "This will be implemented in a future phase."
    )


def calculate_concrete_quantity(inputs: PoleBarnInputs) -> Dict[str, Any]:
    """
    Calculate concrete quantities for foundation/pads.
    
    NOTE: This is a placeholder. Actual concrete calculation requires
    foundation design details and pole count/placement.
    
    Args:
        inputs: Complete pole barn inputs
        
    Returns:
        Dictionary with concrete volume, bags, or cubic yards
        
    Raises:
        NotImplementedError: Concrete calculation not yet implemented
    """
    raise NotImplementedError(
        "Concrete quantity calculation requires foundation design details. "
        "This will be implemented in a future phase."
    )


def calculate_insulation_quantity(inputs: PoleBarnInputs) -> Dict[str, Any]:
    """
    Calculate insulation material quantities.
    
    Args:
        inputs: Complete pole barn inputs
        
    Returns:
        Dictionary with insulation type, quantity, and details
    """
    from . import geometry as geometry_module
    
    if not inputs.materials.insulation_type or inputs.materials.insulation_type.lower() == "none":
        return {
            "insulation_type": "none",
            "quantity": 0.0,
            "unit": "sqft",
            "details": "No insulation specified",
        }
    
    geom_model = geometry_module.build_geometry_model(inputs.geometry)
    
    # Insulation for walls and roof
    total_insulation_sqft = geom_model.total_wall_area_sqft + geom_model.roof_area_sqft
    
    return {
        "insulation_type": inputs.materials.insulation_type,
        "quantity": total_insulation_sqft,
        "unit": "sqft",
        "r_value": inputs.materials.insulation_r_value,
        "details": f"Insulation for walls and roof",
    }


def calculate_ventilation_quantity(inputs: PoleBarnInputs) -> Dict[str, Any]:
    """
    Calculate ventilation components.
    
    Args:
        inputs: Complete pole barn inputs
        
    Returns:
        Dictionary with ventilation type, count, and details
    """
    if not inputs.assemblies.ventilation_type or inputs.assemblies.ventilation_type.lower() == "none":
        return {
            "ventilation_type": "none",
            "count": 0,
            "unit": "ea",
            "details": "No ventilation specified",
        }
    
    count = inputs.assemblies.ventilation_count or 0
    
    return {
        "ventilation_type": inputs.assemblies.ventilation_type,
        "count": count,
        "unit": "ea",
        "details": f"Ventilation units: {inputs.assemblies.ventilation_type}",
    }


def get_assembly_summary(inputs: PoleBarnInputs) -> Dict[str, Any]:
    """
    Get a summary of all assembly and material calculations.
    
    Args:
        inputs: Complete pole barn inputs
        
    Returns:
        Dictionary containing all assembly calculations
    """
    from . import geometry as geometry_module
    
    geom_model = geometry_module.build_geometry_model(inputs.geometry)
    quantities = calculate_material_quantities(geom_model, inputs.materials, inputs.assemblies)
    
    # Organize by category
    by_category: Dict[str, List[AssemblyQuantity]] = {}
    for item in quantities:
        if item.category not in by_category:
            by_category[item.category] = []
        by_category[item.category].append(item)
    
    # Convert to dictionaries for JSON serialization
    summary: Dict[str, Any] = {
        "total_items": len(quantities),
        "by_category": {},
    }
    
    for category, items in by_category.items():
        summary["by_category"][category] = [
            {
                "name": item.name,
                "description": item.description,
                "quantity": item.quantity,
                "unit": item.unit,
                "notes": item.notes,
            }
            for item in items
        ]
    
    return summary
```

---

### File: systems/pole_barn/pricing.py

```python
"""Pricing and cost calculations."""

import csv
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
from .model import (
    PoleBarnInputs,
    PricingInputs,
    MaterialTakeoff,
    AssemblyQuantity,
    PricedLineItem,
    PricingSummary,
)


# Default paths for config files
DEFAULT_CONFIG_DIR = Path(__file__).parent.parent.parent / "config"
DEFAULT_PARTS_CSV = DEFAULT_CONFIG_DIR / "parts.example.csv"
DEFAULT_PRICING_CSV = DEFAULT_CONFIG_DIR / "pricing.example.csv"
DEFAULT_ASSEMBLIES_CSV = DEFAULT_CONFIG_DIR / "assemblies.example.csv"


def load_parts(path: Optional[Path] = None) -> pd.DataFrame:
    """
    Load parts catalog from CSV.
    
    Expected columns: part_id, part_name, category, unit, description
    
    Args:
        path: Path to parts CSV file. If None, uses default.
        
    Returns:
        DataFrame with parts data
    """
    if path is None:
        path = DEFAULT_PARTS_CSV
    
    try:
        df = pd.read_csv(path)
        # Ensure required columns exist
        required_cols = ["part_id", "part_name"]
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col} in {path}")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Parts CSV not found: {path}")
    except Exception as e:
        raise ValueError(f"Error loading parts CSV {path}: {e}")


def load_pricing(path: Optional[Path] = None) -> pd.DataFrame:
    """
    Load pricing data from CSV.
    
    Expected columns: part_id, unit_price, unit, notes
    
    Args:
        path: Path to pricing CSV file. If None, uses default.
        
    Returns:
        DataFrame with pricing data
    """
    if path is None:
        path = DEFAULT_PRICING_CSV
    
    try:
        df = pd.read_csv(path)
        # Ensure required columns exist
        required_cols = ["part_id", "unit_price"]
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col} in {path}")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Pricing CSV not found: {path}")
    except Exception as e:
        raise ValueError(f"Error loading pricing CSV {path}: {e}")


def load_assemblies(path: Optional[Path] = None) -> pd.DataFrame:
    """
    Load assembly mappings from CSV.
    
    Expected columns: assembly_id, assembly_name, parts, quantity_multiplier, notes
    
    Args:
        path: Path to assemblies CSV file. If None, uses default.
        
    Returns:
        DataFrame with assembly mappings
    """
    if path is None:
        path = DEFAULT_ASSEMBLIES_CSV
    
    try:
        df = pd.read_csv(path)
        # Ensure required columns exist
        required_cols = ["assembly_name"]
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col} in {path}")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Assemblies CSV not found: {path}")
    except Exception as e:
        raise ValueError(f"Error loading assemblies CSV {path}: {e}")


def find_assembly_mapping(
    assemblies_df: pd.DataFrame,
    assembly_name: str,
) -> Optional[Dict[str, Any]]:
    """
    Find assembly mapping for a given assembly name.
    
    Args:
        assemblies_df: DataFrame with assembly mappings
        assembly_name: Name of the assembly (matches AssemblyQuantity.name)
        
    Returns:
        Dictionary with mapping info (part_id, waste_factor, labor_per_unit, etc.)
        or None if not found
    """
    # Try exact match first
    matches = assemblies_df[assemblies_df["assembly_name"] == assembly_name]
    
    if len(matches) == 0:
        return None
    
    # Take first match
    row = matches.iloc[0]
    
    result: Dict[str, Any] = {
        "assembly_id": row.get("assembly_id", ""),
        "assembly_name": row.get("assembly_name", assembly_name),
        "category": row.get("category", ""),
    }
    
    # New schema: direct part_id column (preferred)
    if "part_id" in row and pd.notna(row["part_id"]):
        result["part_id"] = str(row["part_id"]).strip()
        result["parts"] = [result["part_id"]]  # For backward compatibility
    # Old schema: pipe-separated parts column (fallback)
    elif "parts" in row and pd.notna(row["parts"]):
        parts_str = str(row["parts"])
        parts_list = [p.strip() for p in parts_str.split("|") if p.strip()]
        result["parts"] = parts_list
        # Use first part as primary part_id
        result["part_id"] = parts_list[0] if parts_list else None
    else:
        result["parts"] = []
        result["part_id"] = None
    
    # New schema: direct waste_factor column (preferred)
    if "waste_factor" in row and pd.notna(row["waste_factor"]):
        try:
            result["waste_factor"] = float(row["waste_factor"])
        except (ValueError, TypeError):
            result["waste_factor"] = 1.0
    # Old schema: quantity_multiplier column (fallback)
    elif "quantity_multiplier" in row and pd.notna(row["quantity_multiplier"]):
        mult_str = str(row["quantity_multiplier"])
        mult_list = [float(m.strip()) for m in mult_str.split("|") if m.strip()]
        # Use first multiplier as waste factor (or 1.0 if none)
        result["waste_factor"] = mult_list[0] if mult_list else 1.0
    else:
        result["waste_factor"] = 1.0
    
    # New schema: direct labor_per_unit column (preferred)
    if "labor_per_unit" in row and pd.notna(row["labor_per_unit"]):
        try:
            result["labor_per_unit"] = float(row["labor_per_unit"])
        except (ValueError, TypeError):
            result["labor_per_unit"] = 0.0
    else:
        result["labor_per_unit"] = 0.0
    
    # Markup override (not in current CSV schema, but structure ready)
    result["markup_percent_override"] = None
    
    return result


def find_part_record(
    parts_df: pd.DataFrame,
    part_id: str,
) -> Optional[Dict[str, Any]]:
    """
    Find part record by part_id.
    
    Args:
        parts_df: DataFrame with parts data
        part_id: Part ID to look up
        
    Returns:
        Dictionary with part info or None if not found
    """
    matches = parts_df[parts_df["part_id"] == part_id]
    
    if len(matches) == 0:
        return None
    
    row = matches.iloc[0]
    return {
        "part_id": row.get("part_id", part_id),
        "part_name": row.get("part_name", ""),
        "category": row.get("category", ""),
        "unit": row.get("unit", ""),
        "description": row.get("description", ""),
    }


def find_unit_price(
    pricing_df: pd.DataFrame,
    part_id: str,
) -> Optional[float]:
    """
    Find unit price for a part.
    
    Args:
        pricing_df: DataFrame with pricing data
        part_id: Part ID to look up
        
    Returns:
        Unit price as float, or None if not found
    """
    matches = pricing_df[pricing_df["part_id"] == part_id]
    
    if len(matches) == 0:
        return None
    
    # Take first match (if multiple, could add date-based selection later)
    row = matches.iloc[0]
    unit_price = row.get("unit_price")
    
    if pd.isna(unit_price):
        return None
    
    try:
        return float(unit_price)
    except (ValueError, TypeError):
        return None


def _create_simple_assembly_mapping() -> Dict[str, str]:
    """
    Create a simple mapping from assembly names to part IDs.
    
    This is a fallback when assemblies CSV doesn't have a match.
    Maps common assembly names to likely part IDs.
    
    Returns:
        Dictionary mapping assembly_name -> part_id
    """
    return {
        "posts": "POST_6X6_PT",
        "trusses": "TRUSS_STD",
        "sidewall_girts": "LBR_2X6_LF",
        "endwall_girts": "LBR_2X6_LF",
        "roof_purlins": "LBR_2X6_LF",
        "roof_panels": "METAL_PANEL_29_SQFT",  # Default, may be overridden by assembly mapping
        "sidewall_panels": "METAL_PANEL_29_SQFT",  # Default, may be overridden by assembly mapping
        "endwall_panels": "METAL_PANEL_29_SQFT",  # Default, may be overridden by assembly mapping
        "eave_trim": "TRIM_EAVE",
        "rake_trim": "TRIM_RAKE",
        "base_trim": "TRIM_BASE",
        "corner_trim": "TRIM_CORNER",
        "door_trim": "TRIM_DOOR",
        "window_trim": "TRIM_WINDOW",
        "roof_fasteners": "SCREW_METAL",
        "wall_fasteners": "SCREW_METAL",
        "trim_fasteners": "SCREW_METAL",
        "post_concrete": "CONCRETE_CY",
        "slab_concrete": "CONCRETE_CY",
        "wall_insulation": "INS_R19_SQFT",  # Default fiberglass
        "wall_insulation_rockwool": "INS_ROCKWOOL_SQFT",
        "wall_insulation_rigid": "INS_RIGID_SQFT",
        "wall_insulation_sprayfoam": "INS_SPRAYFOAM_SQFT",
        "roof_insulation": "INS_R19_SQFT",  # Default fiberglass
        "roof_insulation_rockwool": "INS_ROCKWOOL_SQFT",
        "roof_insulation_rigid": "INS_RIGID_SQFT",
        "roof_insulation_sprayfoam": "INS_SPRAYFOAM_SQFT",
        "ridge_vent": "VENT_RIDGE",
        "gable_vent": "VENT_GABLE",
        "door_framing": "LBR_2X6_LF",
        "window_framing": "LBR_2X6_LF",
    }


def price_material_takeoff(
    takeoff: MaterialTakeoff,
    pricing_inputs: PricingInputs,
    parts_df: pd.DataFrame,
    pricing_df: pd.DataFrame,
    assemblies_df: pd.DataFrame,
) -> Tuple[List[PricedLineItem], PricingSummary]:
    """
    Price a material takeoff, returning priced line items and summary.
    
    Args:
        takeoff: Material takeoff with quantities
        pricing_inputs: Pricing parameters (markup, tax rate, labor rate)
        parts_df: DataFrame with parts catalog
        pricing_df: DataFrame with pricing data
        assemblies_df: DataFrame with assembly mappings
        
    Returns:
        Tuple of (list of PricedLineItem, PricingSummary)
    """
    priced_items: List[PricedLineItem] = []
    simple_mapping = _create_simple_assembly_mapping()
    
    # Get global pricing parameters
    labor_rate = pricing_inputs.labor_rate
    # Use material_markup_pct if provided, otherwise derive from legacy material_markup field
    if hasattr(pricing_inputs, 'material_markup_pct') and pricing_inputs.material_markup_pct > 0:
        material_markup_pct = pricing_inputs.material_markup_pct
    else:
        # Backward compatibility: convert 1.15 to 15%
        material_markup_pct = (pricing_inputs.material_markup - 1.0) * 100.0
    
    # Get other markup percentages (with defaults)
    labor_markup_pct = getattr(pricing_inputs, 'labor_markup_pct', 10.0)
    subcontractor_markup_pct = getattr(pricing_inputs, 'subcontractor_markup_pct', 10.0)
    overhead_pct = getattr(pricing_inputs, 'overhead_pct', 0.0)
    
    tax_rate = pricing_inputs.tax_rate * 100.0  # Convert 0.08 to 8%
    
    for assembly_qty in takeoff.items:
        # Find assembly mapping
        assembly_map = find_assembly_mapping(assemblies_df, assembly_qty.name)
        
        # Determine part_id
        part_id = None
        waste_factor = 1.0
        labor_per_unit = 0.0
        markup_override = None
        
        if assembly_map:
            part_id = assembly_map.get("part_id")
            waste_factor = assembly_map.get("waste_factor", 1.0)
            labor_per_unit = assembly_map.get("labor_per_unit", 0.0)
            markup_override = assembly_map.get("markup_percent_override")
        else:
            # Fallback to simple mapping
            part_id = simple_mapping.get(assembly_qty.name)
        
        # Effective quantity with waste
        effective_qty = assembly_qty.quantity * waste_factor
        
        # Find unit price
        unit_price = 0.0
        part_record = None
        notes_list = []
        
        if part_id:
            part_record = find_part_record(parts_df, part_id)
            unit_price = find_unit_price(pricing_df, part_id) or 0.0
            
            if unit_price == 0.0:
                notes_list.append(f"No price found for part {part_id}")
        else:
            notes_list.append(f"No part mapping for {assembly_qty.name}")
        
        # Calculate base costs
        material_cost = effective_qty * unit_price
        labor_hours = effective_qty * labor_per_unit
        labor_cost = labor_hours * labor_rate
        
        # Determine if this is a subcontractor item (future: check part category or assembly flag)
        is_subcontractor = False  # For now, no subcontractor items identified
        
        # Apply markups separately (overhead applied at summary level, not per line item)
        # Material markup (use override if available, else global)
        material_markup_pct_effective = markup_override if markup_override is not None else material_markup_pct
        material_markup_amount = material_cost * (material_markup_pct_effective / 100.0)
        
        # Labor markup (applies only to labor)
        labor_markup_amount = labor_cost * (labor_markup_pct / 100.0)
        
        # Subcontractor markup (if applicable)
        subcontractor_markup_amount = 0.0
        if is_subcontractor:
            subcontractor_markup_amount = (material_cost + labor_cost) * (subcontractor_markup_pct / 100.0)
        
        # Total markup for this line item (overhead will be added at summary level)
        markup_amount = material_markup_amount + labor_markup_amount + subcontractor_markup_amount
        
        # Total cost = base costs + markups (overhead added later at summary)
        total_cost = material_cost + labor_cost + markup_amount
        
        # Build priced line item
        priced_item = PricedLineItem(
            name=assembly_qty.name,
            description=assembly_qty.description,
            category=assembly_qty.category,
            quantity=effective_qty,
            unit=assembly_qty.unit,
            part_id=part_id,
            unit_price=unit_price,
            material_cost=material_cost,
            labor_hours=labor_hours,
            labor_rate=labor_rate,
            labor_cost=labor_cost,
            markup_percent=material_markup_pct_effective,  # Store material markup for display
            markup_amount=markup_amount,  # Total markup (material + labor + subcontractor)
            total_cost=total_cost,
            notes="; ".join(notes_list) if notes_list else assembly_qty.notes,
        )
        
        priced_items.append(priced_item)
    
    # Calculate summary totals
    material_subtotal = sum(item.material_cost for item in priced_items)
    labor_subtotal = sum(item.labor_cost for item in priced_items)
    markup_total = sum(item.markup_amount for item in priced_items)
    
    # Apply overhead at summary level (overhead is treated like profit - applied to material + labor)
    overhead_total = (material_subtotal + labor_subtotal) * (overhead_pct / 100.0)
    
    # Tax on material + markup (typical for construction)
    tax_total = (material_subtotal + markup_total) * (tax_rate / 100.0)
    
    # Grand total = materials + labor + markups + overhead + tax
    grand_total = material_subtotal + labor_subtotal + markup_total + overhead_total + tax_total
    
    # Add any additional costs from pricing_inputs
    if pricing_inputs.delivery_cost:
        grand_total += pricing_inputs.delivery_cost
    if pricing_inputs.permit_cost:
        grand_total += pricing_inputs.permit_cost
    if pricing_inputs.site_prep_cost:
        grand_total += pricing_inputs.site_prep_cost
    
    # MEP allowances (per changelog entry [18])
    mep_items: List[PricedLineItem] = []
    if pricing_inputs.include_electrical and pricing_inputs.electrical_allowance > 0:
        mep_items.append(PricedLineItem(
            name="electrical_allowance",
            description="Electrical allowance (basic lighting/outlets)",
            category="MEP",
            quantity=1.0,
            unit="lump",
            part_id=None,
            unit_price=pricing_inputs.electrical_allowance,
            material_cost=pricing_inputs.electrical_allowance,
            labor_hours=0.0,
            labor_rate=pricing_inputs.labor_rate,
            labor_cost=0.0,
            markup_percent=0.0,  # Allowances typically not marked up
            markup_amount=0.0,
            total_cost=pricing_inputs.electrical_allowance,
            notes="MEP allowance - not marked up",
        ))
        grand_total += pricing_inputs.electrical_allowance
    
    if pricing_inputs.include_plumbing and pricing_inputs.plumbing_allowance > 0:
        mep_items.append(PricedLineItem(
            name="plumbing_allowance",
            description="Plumbing allowance",
            category="MEP",
            quantity=1.0,
            unit="lump",
            part_id=None,
            unit_price=pricing_inputs.plumbing_allowance,
            material_cost=pricing_inputs.plumbing_allowance,
            labor_hours=0.0,
            labor_rate=pricing_inputs.labor_rate,
            labor_cost=0.0,
            markup_percent=0.0,
            markup_amount=0.0,
            total_cost=pricing_inputs.plumbing_allowance,
            notes="MEP allowance - not marked up",
        ))
        grand_total += pricing_inputs.plumbing_allowance
    
    if pricing_inputs.include_mechanical and pricing_inputs.mechanical_allowance > 0:
        mep_items.append(PricedLineItem(
            name="mechanical_allowance",
            description="Mechanical allowance (heat/vent)",
            category="MEP",
            quantity=1.0,
            unit="lump",
            part_id=None,
            unit_price=pricing_inputs.mechanical_allowance,
            material_cost=pricing_inputs.mechanical_allowance,
            labor_hours=0.0,
            labor_rate=pricing_inputs.labor_rate,
            labor_cost=0.0,
            markup_percent=0.0,
            markup_amount=0.0,
            total_cost=pricing_inputs.mechanical_allowance,
            notes="MEP allowance - not marked up",
        ))
        grand_total += pricing_inputs.mechanical_allowance
    
    # Add MEP items to priced items list
    priced_items.extend(mep_items)
    
    # Update summary to include MEP in material subtotal
    mep_total = sum(item.material_cost for item in mep_items)
    material_subtotal += mep_total
    
    summary = PricingSummary(
        material_subtotal=material_subtotal,
        labor_subtotal=labor_subtotal,
        markup_total=markup_total,
        tax_total=tax_total,
        grand_total=grand_total,
    )
    
    return priced_items, summary


# Legacy function stubs for backward compatibility
def calculate_material_costs(inputs: PoleBarnInputs) -> Dict[str, Any]:
    """
    Calculate material costs based on quantities and pricing.
    
    NOTE: This is a legacy function. Use price_material_takeoff() for new code.
    
    Args:
        inputs: Complete pole barn inputs
        
    Returns:
        Dictionary with material cost breakdown and total
        
    Raises:
        NotImplementedError: This function requires CSV configs to be loaded
    """
    raise NotImplementedError(
        "This function requires CSV configuration. "
        "Use PoleBarnCalculator.calculate() or price_material_takeoff() directly."
    )


def calculate_labor_costs(inputs: PoleBarnInputs) -> Dict[str, Any]:
    """
    Calculate labor costs based on assembly complexity and rates.
    
    NOTE: This is a legacy function. Use price_material_takeoff() for new code.
    
    Args:
        inputs: Complete pole barn inputs
        
    Returns:
        Dictionary with labor cost breakdown and total
        
    Raises:
        NotImplementedError: This function requires CSV configs to be loaded
    """
    raise NotImplementedError(
        "This function requires CSV configuration. "
        "Use PoleBarnCalculator.calculate() or price_material_takeoff() directly."
    )


def calculate_subtotal(inputs: PoleBarnInputs) -> float:
    """
    Calculate subtotal before taxes and fees.
    
    NOTE: This is a legacy function. Use price_material_takeoff() for new code.
    
    Args:
        inputs: Complete pole barn inputs
        
    Returns:
        Subtotal cost in dollars
        
    Raises:
        NotImplementedError: This function requires CSV configs to be loaded
    """
    raise NotImplementedError(
        "This function requires CSV configuration. "
        "Use PoleBarnCalculator.calculate() or price_material_takeoff() directly."
    )


def calculate_taxes(inputs: PoleBarnInputs, subtotal: float) -> float:
    """
    Calculate taxes on the subtotal.
    
    NOTE: This is a legacy function. Use price_material_takeoff() for new code.
    
    Args:
        inputs: Complete pole barn inputs
        subtotal: Subtotal amount before taxes
        
    Returns:
        Tax amount in dollars
        
    Raises:
        NotImplementedError: This function requires CSV configs to be loaded
    """
    raise NotImplementedError(
        "This function requires CSV configuration. "
        "Use PoleBarnCalculator.calculate() or price_material_takeoff() directly."
    )


def calculate_total_cost(inputs: PoleBarnInputs) -> Dict[str, Any]:
    """
    Calculate total project cost including all components.
    
    NOTE: This is a legacy function. Use price_material_takeoff() for new code.
    
    Args:
        inputs: Complete pole barn inputs
        
    Returns:
        Dictionary with cost breakdown and total
        
    Raises:
        NotImplementedError: This function requires CSV configs to be loaded
    """
    raise NotImplementedError(
        "This function requires CSV configuration. "
        "Use PoleBarnCalculator.calculate() or price_material_takeoff() directly."
    )


def get_cost_breakdown(inputs: PoleBarnInputs) -> Dict[str, Any]:
    """
    Get detailed cost breakdown by category.
    
    NOTE: This is a legacy function. Use price_material_takeoff() for new code.
    
    Args:
        inputs: Complete pole barn inputs
        
    Returns:
        Dictionary with detailed cost breakdown by category
        
    Raises:
        NotImplementedError: This function requires CSV configs to be loaded
    """
    raise NotImplementedError(
        "This function requires CSV configuration. "
        "Use PoleBarnCalculator.calculate() or price_material_takeoff() directly."
    )
```

---

### File: systems/pole_barn/calculator.py

```python
"""Main calculator class that orchestrates all calculations."""

import sys
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List
import pandas as pd
from .model import (
    PoleBarnInputs,
    GeometryModel,
    MaterialTakeoff,
    PricedLineItem,
    PricingSummary,
)
from . import geometry
from . import assemblies
from . import pricing


def _get_default_config_dir() -> Path:
    """
    Get default config directory, handling both script and bundled exe modes.
    
    Returns:
        Path to config directory
    """
    if getattr(sys, 'frozen', False):
        # Running as bundled exe - config is next to exe
        return Path(sys.executable).parent / "config"
    else:
        # Running as script - config is in project root
        return Path(__file__).parent.parent.parent / "config"


class PoleBarnCalculator:
    """Main calculator for pole barn construction."""
    
    def __init__(
        self,
        inputs: Optional[PoleBarnInputs] = None,
        config_dir: Optional[Path] = None,
    ):
        """
        Initialize calculator with inputs and config directory.
        
        Args:
            inputs: Complete pole barn inputs (optional, can be set later)
            config_dir: Directory containing CSV config files. If None, uses default.
        """
        self.inputs = inputs
        self.config_dir = config_dir or _get_default_config_dir()
        
        # DataFrames for config data (loaded lazily)
        self.parts_df: Optional[pd.DataFrame] = None
        self.pricing_df: Optional[pd.DataFrame] = None
        self.assemblies_df: Optional[pd.DataFrame] = None
        self._config_loaded = False
    
    def load_config(self) -> None:
        """
        Load configuration data from CSV files.
        
        Raises:
            FileNotFoundError: If config files are not found
            ValueError: If config files are malformed
        """
        # Try parts.example.csv first, fall back to parts.csv
        parts_path = self.config_dir / "parts.example.csv"
        if not parts_path.exists():
            parts_path = self.config_dir / "parts.csv"
        
        pricing_path = self.config_dir / "pricing.example.csv"
        if not pricing_path.exists():
            pricing_path = self.config_dir / "pricing.csv"
        
        assemblies_path = self.config_dir / "assemblies.example.csv"
        if not assemblies_path.exists():
            assemblies_path = self.config_dir / "assemblies.csv"
        
        self.parts_df = pricing.load_parts(parts_path)
        self.pricing_df = pricing.load_pricing(pricing_path)
        self.assemblies_df = pricing.load_assemblies(assemblies_path)
        self._config_loaded = True
    
    def calculate(
        self,
        inputs: Optional[PoleBarnInputs] = None,
    ) -> Tuple[GeometryModel, MaterialTakeoff, List[PricedLineItem], PricingSummary]:
        """
        Run complete calculation pipeline: geometry → quantities → pricing.
        
        Args:
            inputs: Pole barn inputs. If None, uses self.inputs.
            
        Returns:
            Tuple of (GeometryModel, MaterialTakeoff, list of PricedLineItem, PricingSummary)
            
        Raises:
            ValueError: If inputs are not provided and self.inputs is None
            RuntimeError: If config is not loaded
        """
        if inputs is None:
            inputs = self.inputs
        
        if inputs is None:
            raise ValueError("PoleBarnInputs must be provided either in __init__ or calculate()")
        
        if not self._config_loaded:
            self.load_config()
        
        if self.parts_df is None or self.pricing_df is None or self.assemblies_df is None:
            raise RuntimeError("Configuration data not loaded. Call load_config() first.")
        
        # 1. Build geometry
        geom_model = geometry.build_geometry_model(inputs.geometry)
        
        # 2. Calculate quantities
        # Pass geometry_inputs for door/window counts (per changelog entry [14])
        quantities = assemblies.calculate_material_quantities(
            geom_model,
            inputs.materials,
            inputs.assemblies,
            geometry_inputs=inputs.geometry,  # For door/window assemblies
        )
        takeoff = MaterialTakeoff(items=quantities)
        
        # 3. Price the takeoff
        priced_items, summary = pricing.price_material_takeoff(
            takeoff,
            inputs.pricing,
            self.parts_df,
            self.pricing_df,
            self.assemblies_df,
        )
        
        return geom_model, takeoff, priced_items, summary
    
    def calculate_geometry(self) -> Dict[str, Any]:
        """
        Calculate all geometry-related values.
        
        Returns:
            Dictionary with geometry calculations
        """
        if self.inputs is None:
            raise ValueError("PoleBarnInputs must be set")
        
        geom_model = geometry.build_geometry_model(self.inputs.geometry)
        geom_summary = geometry.get_geometry_summary(self.inputs.geometry)
        
        return {
            "model": geom_model,
            "summary": geom_summary,
        }
    
    def calculate_quantities(self) -> Dict[str, Any]:
        """
        Calculate all material quantities.
        
        Returns:
            Dictionary with quantity calculations
        """
        if self.inputs is None:
            raise ValueError("PoleBarnInputs must be set")
        
        geom_model = geometry.build_geometry_model(self.inputs.geometry)
        quantities = assemblies.calculate_material_quantities(
            geom_model,
            self.inputs.materials,
            self.inputs.assemblies,
        )
        takeoff = MaterialTakeoff(items=quantities)
        
        return {
            "takeoff": takeoff,
            "summary": assemblies.get_assembly_summary(self.inputs),
        }
    
    def calculate_costs(self) -> Dict[str, Any]:
        """
        Calculate all costs.
        
        Returns:
            Dictionary with cost calculations
        """
        if self.inputs is None:
            raise ValueError("PoleBarnInputs must be set")
        
        if not self._config_loaded:
            self.load_config()
        
        if self.parts_df is None or self.pricing_df is None or self.assemblies_df is None:
            raise RuntimeError("Configuration data not loaded. Call load_config() first.")
        
        # Get quantities first
        geom_model = geometry.build_geometry_model(self.inputs.geometry)
        quantities = assemblies.calculate_material_quantities(
            geom_model,
            self.inputs.materials,
            self.inputs.assemblies,
        )
        takeoff = MaterialTakeoff(items=quantities)
        
        # Price them
        priced_items, summary = pricing.price_material_takeoff(
            takeoff,
            self.inputs.pricing,
            self.parts_df,
            self.pricing_df,
            self.assemblies_df,
        )
        
        return {
            "priced_items": priced_items,
            "summary": summary,
        }
    
    def calculate_all(self) -> Dict[str, Any]:
        """
        Run all calculations and return complete results.
        
        Returns:
            Dictionary with all calculations including geometry, quantities, and costs
        """
        geom_model, takeoff, priced_items, summary = self.calculate()
        
        return {
            "geometry": {
                "model": geom_model,
                "summary": geometry.get_geometry_summary(self.inputs.geometry),
            },
            "quantities": {
                "takeoff": takeoff,
                "summary": assemblies.get_assembly_summary(self.inputs),
            },
            "pricing": {
                "priced_items": priced_items,
                "summary": summary,
            },
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a human-readable summary of all calculations.
        
        Returns:
            Dictionary with formatted summary information
        """
        geom_model, takeoff, priced_items, summary = self.calculate()
        
        # Organize priced items by category
        by_category: Dict[str, List[PricedLineItem]] = {}
        for item in priced_items:
            if item.category not in by_category:
                by_category[item.category] = []
            by_category[item.category].append(item)
        
        return {
            "project_name": self.inputs.project_name if self.inputs else None,
            "geometry": {
                "dimensions": {
                    "length_ft": geom_model.overall_length_ft,
                    "width_ft": geom_model.overall_width_ft,
                    "eave_height_ft": geom_model.eave_height_ft,
                },
                "areas": {
                    "footprint_sqft": geom_model.footprint_area_sqft,
                    "roof_sqft": geom_model.roof_area_sqft,
                    "wall_sqft": geom_model.total_wall_area_sqft,
                },
            },
            "quantities": {
                "total_items": len(takeoff.items),
                "by_category": {
                    cat: len(items) for cat, items in by_category.items()
                },
            },
            "costs": {
                "material_subtotal": summary.material_subtotal,
                "labor_subtotal": summary.labor_subtotal,
                "markup_total": summary.markup_total,
                "tax_total": summary.tax_total,
                "grand_total": summary.grand_total,
            },
            "priced_items_by_category": {
                cat: [
                    {
                        "name": item.name,
                        "description": item.description,
                        "quantity": item.quantity,
                        "unit": item.unit,
                        "unit_price": item.unit_price,
                        "total_cost": item.total_cost,
                    }
                    for item in items
                ]
                for cat, items in by_category.items()
            },
        }
```

---

### File: apps/gui.py

```python
"""GUI application for Pole Barn Calculator using tkinter."""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import re
from pathlib import Path

# Add parent directory to path for imports when running as script
sys.path.insert(0, str(Path(__file__).parent.parent))

from systems.pole_barn.calculator import PoleBarnCalculator
from systems.pole_barn.model import (
    GeometryInputs,
    MaterialInputs,
    AssemblyInputs,
    PricingInputs,
    PoleBarnInputs,
)


def get_config_dir():
    """
    Get the config directory path.
    
    When running as a script, uses relative path.
    When bundled as exe, uses the exe's directory.
    """
    if getattr(sys, 'frozen', False):
        # Running as bundled exe
        base_path = Path(sys.executable).parent
    else:
        # Running as script
        base_path = Path(__file__).parent.parent
    
    return base_path / "config"


def parse_roof_pitch(pitch_str: str) -> float:
    """
    Parse roof pitch from various formats into a numeric ratio.
    
    Accepts:
    - "4/12", "3/12" (rise/run)
    - "4" or "3" (assumes X/12)
    - "0.333" (decimal ratio)
    
    Returns float ratio (e.g., 4/12 = 0.333...)
    """
    pitch_str = pitch_str.strip()
    
    # If it contains a slash, parse as rise/run
    if '/' in pitch_str:
        parts = pitch_str.split('/')
        if len(parts) == 2:
            try:
                rise = float(parts[0])
                run = float(parts[1])
                if run == 0:
                    raise ValueError("Run cannot be zero")
                return rise / run
            except ValueError:
                raise ValueError(f"Invalid pitch format: {pitch_str}")
    
    # Try parsing as a number
    try:
        pitch_num = float(pitch_str)
        # If it's a whole number or small decimal, assume it's rise per 12
        if pitch_num > 0 and pitch_num < 12:
            return pitch_num / 12.0
        # If it's between 0 and 2, treat as a ratio directly
        elif pitch_num > 0 and pitch_num < 2:
            return pitch_num
        else:
            raise ValueError(f"Pitch value {pitch_num} out of expected range")
    except ValueError:
        raise ValueError(f"Invalid pitch format: {pitch_str}")


def run_calculation(vars_dict, output_text, status_label):
    """Run the calculation and display results."""
    try:
        # Parse basic geometry inputs
        length = float(vars_dict["length"].get())
        width = float(vars_dict["width"].get())
        eave_height = float(vars_dict["eave_height"].get())
        roof_pitch_str = vars_dict["roof_pitch"].get()
        roof_pitch = parse_roof_pitch(roof_pitch_str)
        
        # Roof style and ridge position
        roof_style = vars_dict["roof_style"].get()
        ridge_position_str = vars_dict["ridge_position"].get()
        ridge_position = None
        if roof_style == "gable" and ridge_position_str.strip():
            ridge_position = float(ridge_position_str)
            if ridge_position < 0 or ridge_position > length:
                messagebox.showerror("Input Error", 
                    f"Ridge position must be between 0 and {length} feet.")
                return
        elif roof_style == "gable" and not ridge_position_str.strip():
            # Default to centered
            ridge_position = length / 2.0
        
        # Overhangs
        overhang_front = float(vars_dict.get("overhang_front", tk.StringVar(value="1.0")).get())
        overhang_rear = float(vars_dict.get("overhang_rear", tk.StringVar(value="1.0")).get())
        overhang_sides = float(vars_dict.get("overhang_sides", tk.StringVar(value="1.0")).get())
        
        # Doors and windows
        door_count = int(vars_dict.get("door_count", tk.StringVar(value="0")).get())
        door_width = float(vars_dict.get("door_width", tk.StringVar(value="0.0")).get())
        door_height = float(vars_dict.get("door_height", tk.StringVar(value="0.0")).get())
        window_count = int(vars_dict.get("window_count", tk.StringVar(value="0")).get())
        window_width = float(vars_dict.get("window_width", tk.StringVar(value="0.0")).get())
        window_height = float(vars_dict.get("window_height", tk.StringVar(value="0.0")).get())
        
        # Overhead doors
        overhead_door_count = int(vars_dict.get("overhead_door_count", tk.StringVar(value="0")).get())
        overhead_door_type = vars_dict.get("overhead_door_type", tk.StringVar(value="none")).get()
        
        # Pole spacing
        pole_spacing = float(vars_dict["pole_spacing"].get())
        
        # Pricing
        material_markup_str = vars_dict.get("material_markup", tk.StringVar(value="1.15")).get()
        material_markup_pct_str = vars_dict.get("material_markup_pct", tk.StringVar(value="15.0")).get()
        labor_markup_pct_str = vars_dict.get("labor_markup_pct", tk.StringVar(value="10.0")).get()
        subcontractor_markup_pct_str = vars_dict.get("subcontractor_markup_pct", tk.StringVar(value="10.0")).get()
        overhead_pct_str = vars_dict.get("overhead_pct", tk.StringVar(value="0.0")).get()
        tax_rate = float(vars_dict["tax_rate"].get())
        
        # Parse markup values (use percentage if provided, otherwise legacy multiplier)
        if material_markup_pct_str.strip():
            material_markup_pct = float(material_markup_pct_str)
            material_markup = 1.0 + (material_markup_pct / 100.0)  # Convert 15% to 1.15
        else:
            material_markup = float(material_markup_str)
            material_markup_pct = (material_markup - 1.0) * 100.0  # Convert 1.15 to 15%
        
        labor_markup_pct = float(labor_markup_pct_str) if labor_markup_pct_str.strip() else 10.0
        subcontractor_markup_pct = float(subcontractor_markup_pct_str) if subcontractor_markup_pct_str.strip() else 10.0
        overhead_pct = float(overhead_pct_str) if overhead_pct_str.strip() else 0.0
        
        # Validate inputs
        if length <= 0 or width <= 0 or eave_height <= 0:
            messagebox.showerror("Input Error", "Length, width, and eave height must be greater than 0.")
            return
        if material_markup < 1.0:
            messagebox.showerror("Input Error", "Material markup must be >= 1.0 (e.g., 1.15 for 15%).")
            return
        if tax_rate < 0 or tax_rate > 1:
            messagebox.showerror("Input Error", "Tax rate must be between 0 and 1 (e.g., 0.08 for 8%).")
            return
            
    except ValueError as e:
        messagebox.showerror("Input Error", f"Please enter valid numeric values.\n{str(e)}")
        return
    
    # Update status
    status_label.config(text="Calculating...", foreground="blue")
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "Calculating...\n\n")
    output_text.update()
    
    try:
        # Build geometry inputs
        geometry_inputs = GeometryInputs(
            length=length,
            width=width,
            eave_height=eave_height,
            peak_height=None,  # Will be derived
            roof_pitch=roof_pitch,
            roof_style=roof_style,
            ridge_position_ft_from_left=ridge_position,
            overhang_front=overhang_front,
            overhang_rear=overhang_rear,
            overhang_sides=overhang_sides,
            door_count=door_count,
            door_width=door_width,
            door_height=door_height,
            window_count=window_count,
            window_width=window_width,
            window_height=window_height,
            pole_spacing_length=pole_spacing,
            pole_spacing_width=8.0,
            pole_diameter=6.0,
            pole_depth=4.0,
            overhead_door_count=overhead_door_count,
            overhead_door_type=overhead_door_type,
        )
        
        # Build material inputs
        exterior_finish = vars_dict.get("exterior_finish", tk.StringVar(value="metal_29ga")).get()
        wall_insulation = vars_dict.get("wall_insulation", tk.StringVar(value="none")).get()
        roof_insulation = vars_dict.get("roof_insulation", tk.StringVar(value="none")).get()
        floor_type = vars_dict.get("floor_type", tk.StringVar(value="none")).get()
        slab_thickness = None
        slab_reinforcement = "none"
        if floor_type == "slab":
            slab_thickness_str = vars_dict.get("slab_thickness", tk.StringVar(value="4.0")).get()
            if slab_thickness_str.strip():
                slab_thickness = float(slab_thickness_str)
            slab_reinforcement = vars_dict.get("slab_reinforcement", tk.StringVar(value="none")).get()
        
        material_inputs = MaterialInputs(
            roof_material_type="metal",
            wall_material_type="metal",
            truss_type="standard",
            truss_spacing=pole_spacing,
            purlin_spacing=2.0,
            girt_spacing=2.0,
            foundation_type=floor_type if floor_type != "none" else "concrete_pad",
            roof_gauge=29.0 if exterior_finish.startswith("metal_29") else (26.0 if exterior_finish.startswith("metal_26") else None),
            wall_gauge=29.0 if exterior_finish.startswith("metal_29") else (26.0 if exterior_finish.startswith("metal_26") else None),
            concrete_thickness=slab_thickness,
            exterior_finish_type=exterior_finish,
            wall_insulation_type=wall_insulation,
            roof_insulation_type=roof_insulation,
            floor_type=floor_type,
            slab_thickness_in=slab_thickness,
            slab_reinforcement=slab_reinforcement,
            girt_type=vars_dict.get("girt_type", tk.StringVar(value="standard")).get(),
            wall_sheathing_type=vars_dict.get("wall_sheathing", tk.StringVar(value="none")).get(),
            roof_sheathing_type=vars_dict.get("roof_sheathing", tk.StringVar(value="none")).get(),
        )
        
        # Build assembly inputs
        assembly_inputs = AssemblyInputs(
            assembly_method="standard",
            fastening_type="screws",
            weather_sealing=False,
            ventilation_type=None,
            ventilation_count=None,
            skylight_count=None,
            skylight_size=None,
            post_type=vars_dict.get("post_type", tk.StringVar(value="pt_solid")).get(),
            post_truss_connection_type=vars_dict.get("connection_type", tk.StringVar(value="notched")).get(),
        )
        
        # Build pricing inputs
        pricing_inputs = PricingInputs(
            material_markup=material_markup,  # Legacy field for backward compatibility
            tax_rate=tax_rate,
            labor_rate=50.0,  # Default (config-based, not user-editable)
            delivery_cost=300.0,
            permit_cost=500.0,
            site_prep_cost=1000.0,
            include_electrical=vars_dict.get("include_electrical", tk.BooleanVar(value=False)).get(),
            electrical_allowance=float(vars_dict.get("electrical_allowance", tk.StringVar(value="0.0")).get()),
            include_plumbing=vars_dict.get("include_plumbing", tk.BooleanVar(value=False)).get(),
            plumbing_allowance=float(vars_dict.get("plumbing_allowance", tk.StringVar(value="0.0")).get()),
            include_mechanical=vars_dict.get("include_mechanical", tk.BooleanVar(value=False)).get(),
            mechanical_allowance=float(vars_dict.get("mechanical_allowance", tk.StringVar(value="0.0")).get()),
            material_markup_pct=material_markup_pct,
            labor_markup_pct=labor_markup_pct,
            subcontractor_markup_pct=subcontractor_markup_pct,
            overhead_pct=overhead_pct,
        )
        
        # Build complete inputs
        inputs = PoleBarnInputs(
            geometry=geometry_inputs,
            materials=material_inputs,
            pricing=pricing_inputs,
            assemblies=assembly_inputs,
            project_name=vars_dict.get("project_name", tk.StringVar(value="")).get() or "GUI Calculation",
            notes=None,
            build_type=vars_dict.get("build_type", tk.StringVar(value="pole")).get(),
            construction_type=vars_dict.get("construction_type", tk.StringVar(value="new")).get(),
            building_type=vars_dict.get("building_type", tk.StringVar(value="residential")).get(),
            building_use=vars_dict.get("building_use", tk.StringVar(value="")).get() or None,
            permitting_agency=vars_dict.get("permitting_agency", tk.StringVar(value="")).get() or None,
            required_snow_load_psf=float(vars_dict.get("required_snow_load", tk.StringVar(value="")).get()) if vars_dict.get("required_snow_load", tk.StringVar(value="")).get().strip() else None,
            requested_snow_load_psf=float(vars_dict.get("requested_snow_load", tk.StringVar(value="")).get()) if vars_dict.get("requested_snow_load", tk.StringVar(value="")).get().strip() else None,
            snow_load_unknown=vars_dict.get("snow_load_unknown", tk.BooleanVar(value=False)).get(),
        )
        
        # Create calculator and run
        config_dir = get_config_dir()
        calculator = PoleBarnCalculator(config_dir=config_dir)
        calculator.load_config()
        
        geom_model, takeoff, priced_items, summary = calculator.calculate(inputs)
        
        # Display results
        output_text.delete("1.0", tk.END)
        
        # Header
        output_text.insert(tk.END, "=" * 70 + "\n")
        output_text.insert(tk.END, "POLE BARN CALCULATOR - RESULTS\n")
        output_text.insert(tk.END, "=" * 70 + "\n\n")
        
        # Geometry summary
        output_text.insert(tk.END, "GEOMETRY:\n")
        output_text.insert(tk.END, f"  Dimensions: {length}ft × {width}ft\n")
        output_text.insert(tk.END, f"  Eave Height: {eave_height}ft\n")
        output_text.insert(tk.END, f"  Peak Height: {geom_model.peak_height_ft:.2f}ft (derived)\n")
        output_text.insert(tk.END, f"  Roof Style: {roof_style}\n")
        if roof_style == "gable" and ridge_position:
            output_text.insert(tk.END, f"  Ridge Position: {ridge_position:.1f}ft from left eave\n")
        output_text.insert(tk.END, f"  Footprint: {geom_model.footprint_area_sqft:.1f} sq ft\n")
        output_text.insert(tk.END, f"  Roof Area: {geom_model.roof_area_sqft:.1f} sq ft\n")
        output_text.insert(tk.END, f"  Wall Area: {geom_model.total_wall_area_sqft:.1f} sq ft\n")
        output_text.insert(tk.END, f"  Bays: {geom_model.num_bays} (Frame Lines: {geom_model.num_frame_lines})\n")
        output_text.insert(tk.END, "\n")
        
        # Cost summary
        output_text.insert(tk.END, "COST SUMMARY:\n")
        output_text.insert(tk.END, "-" * 70 + "\n")
        output_text.insert(tk.END, f"  Material Subtotal: ${summary.material_subtotal:,.2f}\n")
        output_text.insert(tk.END, f"  Labor Subtotal:    ${summary.labor_subtotal:,.2f}\n")
        output_text.insert(tk.END, f"  Markup Total:      ${summary.markup_total:,.2f}\n")
        output_text.insert(tk.END, f"  Tax Total:          ${summary.tax_total:,.2f}\n")
        output_text.insert(tk.END, "-" * 70 + "\n")
        output_text.insert(tk.END, f"  GRAND TOTAL:       ${summary.grand_total:,.2f}\n")
        output_text.insert(tk.END, "\n")
        
        # Top line items
        output_text.insert(tk.END, "TOP LINE ITEMS:\n")
        output_text.insert(tk.END, "-" * 70 + "\n")
        
        # Sort by total cost and show top 10
        sorted_items = sorted(priced_items, key=lambda i: i.total_cost, reverse=True)
        for i, item in enumerate(sorted_items[:10], 1):
            if item.total_cost > 0:
                output_text.insert(
                    tk.END,
                    f"  {i:2d}. {item.description:30s} "
                    f"{item.quantity:8.1f} {item.unit:4s} "
                    f"@ ${item.unit_price:6.2f} = ${item.total_cost:10,.2f}\n"
                )
        
        output_text.insert(tk.END, "\n")
        output_text.insert(tk.END, f"Total line items: {len(priced_items)}\n")
        
        status_label.config(text="Calculation complete", foreground="green")
        
    except FileNotFoundError as e:
        error_msg = f"Configuration files not found.\n\nExpected config directory: {config_dir}\n\n{str(e)}"
        messagebox.showerror("Configuration Error", error_msg)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"ERROR: {error_msg}\n")
        status_label.config(text="Error: Config files not found", foreground="red")
    except Exception as e:
        error_msg = f"Calculation error: {str(e)}"
        messagebox.showerror("Calculation Error", error_msg)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"ERROR: {error_msg}\n")
        import traceback
        output_text.insert(tk.END, "\nTraceback:\n")
        output_text.insert(tk.END, traceback.format_exc())
        status_label.config(text="Error during calculation", foreground="red")


def create_input_section(parent, title, row_start, vars_dict):
    """Create a labeled frame section for inputs."""
    frame = ttk.LabelFrame(parent, text=title, padding=5)
    frame.grid(row=row_start, column=0, columnspan=2, sticky="ew", pady=5, padx=5)
    frame.columnconfigure(1, weight=1)
    return frame, row_start


def add_input_row(frame, label, var_name, default_value, row, vars_dict, widget_type="entry", options=None):
    """Add a single input row to a frame."""
    ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", pady=2, padx=5)
    
    if widget_type == "entry":
        var = tk.StringVar(value=default_value)
        entry = ttk.Entry(frame, textvariable=var, width=15)
        entry.grid(row=row, column=1, sticky="ew", padx=5, pady=2)
        vars_dict[var_name] = var
    elif widget_type == "combobox":
        var = tk.StringVar(value=default_value)
        combo = ttk.Combobox(frame, textvariable=var, values=options, width=12, state="readonly")
        combo.grid(row=row, column=1, sticky="ew", padx=5, pady=2)
        vars_dict[var_name] = var
    elif widget_type == "checkbox":
        var = tk.BooleanVar(value=default_value)
        checkbox = ttk.Checkbutton(frame, variable=var)
        checkbox.grid(row=row, column=1, sticky="w", padx=5, pady=2)
        vars_dict[var_name] = var
    
    return row + 1


def main():
    """Create and run the GUI application."""
    root = tk.Tk()
    root.title("Pole Barn Calculator - v0.3 (UI Complete)")
    root.geometry("1200x800")
    
    # Configure grid weights
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=2)
    root.rowconfigure(0, weight=1)
    
    # Main container with scrollable canvas
    canvas = tk.Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")
    
    # Variables dictionary
    vars_dict = {}
    row = 0
    
    # Project / Permit Section
    project_frame, row = create_input_section(scrollable_frame, "Project / Permit Info", row, vars_dict)
    row = add_input_row(project_frame, "Project Name:", "project_name", "", row, vars_dict)
    row = add_input_row(project_frame, "Building Type:", "building_type", "residential", row, vars_dict, 
                       widget_type="combobox", options=["residential", "commercial"])
    row = add_input_row(project_frame, "Construction Type:", "construction_type", "new", row, vars_dict,
                       widget_type="combobox", options=["new", "addition"])
    row = add_input_row(project_frame, "Build Type:", "build_type", "pole", row, vars_dict,
                       widget_type="combobox", options=["pole", "stick_frame"])
    row = add_input_row(project_frame, "Building Use:", "building_use", "", row, vars_dict)
    row = add_input_row(project_frame, "Permitting Agency:", "permitting_agency", "", row, vars_dict)
    row = add_input_row(project_frame, "Required Snow Load (psf):", "required_snow_load", "", row, vars_dict)
    row = add_input_row(project_frame, "Requested Snow Load (psf):", "requested_snow_load", "", row, vars_dict)
    row = add_input_row(project_frame, "Snow Load Unknown:", "snow_load_unknown", False, row, vars_dict, widget_type="checkbox")
    row += 1
    
    # Geometry / Roof Section
    geometry_frame, row = create_input_section(scrollable_frame, "Geometry / Roof", row, vars_dict)
    row = add_input_row(geometry_frame, "Length (ft):", "length", "40", row, vars_dict)
    row = add_input_row(geometry_frame, "Width (ft):", "width", "30", row, vars_dict)
    row = add_input_row(geometry_frame, "Eave Height (ft):", "eave_height", "12", row, vars_dict)
    row = add_input_row(geometry_frame, "Roof Pitch:", "roof_pitch", "4/12", row, vars_dict)
    ttk.Label(geometry_frame, text="(e.g., 4/12, 3/12, or 0.333)", font=("TkDefaultFont", 7)).grid(row=row-1, column=2, sticky="w", padx=5)
    row = add_input_row(geometry_frame, "Roof Style:", "roof_style", "gable", row, vars_dict,
                       widget_type="combobox", options=["gable", "shed"])
    row = add_input_row(geometry_frame, "Ridge Position (ft):", "ridge_position", "", row, vars_dict)
    ttk.Label(geometry_frame, text="(from left eave, blank = centered)", font=("TkDefaultFont", 7)).grid(row=row-1, column=2, sticky="w", padx=5)
    row = add_input_row(geometry_frame, "Front Overhang (ft):", "overhang_front", "1.0", row, vars_dict)
    row = add_input_row(geometry_frame, "Rear Overhang (ft):", "overhang_rear", "1.0", row, vars_dict)
    row = add_input_row(geometry_frame, "Side Overhangs (ft):", "overhang_sides", "1.0", row, vars_dict)
    row = add_input_row(geometry_frame, "Pole Spacing (ft):", "pole_spacing", "10", row, vars_dict)
    row += 1
    
    # Framing & Shell Section
    framing_frame, row = create_input_section(scrollable_frame, "Framing & Shell", row, vars_dict)
    row = add_input_row(framing_frame, "Girt Type:", "girt_type", "standard", row, vars_dict,
                       widget_type="combobox", options=["standard", "commercial"])
    row = add_input_row(framing_frame, "Post Type:", "post_type", "pt_solid", row, vars_dict,
                       widget_type="combobox", options=["pt_solid", "laminated"])
    row = add_input_row(framing_frame, "Truss/Post Connection:", "connection_type", "notched", row, vars_dict,
                       widget_type="combobox", options=["notched", "cleated"])
    row = add_input_row(framing_frame, "Wall Sheathing:", "wall_sheathing", "none", row, vars_dict,
                       widget_type="combobox", options=["none", "osb", "plywood"])
    row = add_input_row(framing_frame, "Roof Sheathing:", "roof_sheathing", "none", row, vars_dict,
                       widget_type="combobox", options=["none", "osb", "plywood"])
    row = add_input_row(framing_frame, "Exterior Finish:", "exterior_finish", "metal_29ga", row, vars_dict,
                       widget_type="combobox", options=["metal_29ga", "metal_26ga", "lap_siding", "stucco"])
    row += 1
    
    # Openings Section
    openings_frame, row = create_input_section(scrollable_frame, "Openings", row, vars_dict)
    row = add_input_row(openings_frame, "Door Count:", "door_count", "0", row, vars_dict)
    row = add_input_row(openings_frame, "Door Width (ft):", "door_width", "0.0", row, vars_dict)
    row = add_input_row(openings_frame, "Door Height (ft):", "door_height", "0.0", row, vars_dict)
    row = add_input_row(openings_frame, "Window Count:", "window_count", "0", row, vars_dict)
    row = add_input_row(openings_frame, "Window Width (ft):", "window_width", "0.0", row, vars_dict)
    row = add_input_row(openings_frame, "Window Height (ft):", "window_height", "0.0", row, vars_dict)
    row = add_input_row(openings_frame, "Overhead Door Count:", "overhead_door_count", "0", row, vars_dict)
    row = add_input_row(openings_frame, "Overhead Door Type:", "overhead_door_type", "none", row, vars_dict,
                       widget_type="combobox", options=["none", "steel_rollup", "sectional"])
    row += 1
    
    # Floor / Slab Section
    floor_frame, row = create_input_section(scrollable_frame, "Floor / Slab", row, vars_dict)
    row = add_input_row(floor_frame, "Floor Type:", "floor_type", "none", row, vars_dict,
                       widget_type="combobox", options=["none", "slab", "gravel"])
    row = add_input_row(floor_frame, "Slab Thickness (in):", "slab_thickness", "4.0", row, vars_dict)
    row = add_input_row(floor_frame, "Slab Reinforcement:", "slab_reinforcement", "none", row, vars_dict,
                       widget_type="combobox", options=["none", "mesh", "rebar"])
    row += 1
    
    # Insulation Section
    insulation_frame, row = create_input_section(scrollable_frame, "Insulation", row, vars_dict)
    row = add_input_row(insulation_frame, "Wall Insulation:", "wall_insulation", "none", row, vars_dict,
                       widget_type="combobox", options=["none", "fiberglass_batts", "rock_wool", "rigid_board", "spray_foam"])
    row = add_input_row(insulation_frame, "Roof Insulation:", "roof_insulation", "none", row, vars_dict,
                       widget_type="combobox", options=["none", "fiberglass_batts", "rock_wool", "rigid_board", "spray_foam"])
    row += 1
    
    # MEP Allowances Section
    mep_frame, row = create_input_section(scrollable_frame, "MEP Allowances", row, vars_dict)
    row = add_input_row(mep_frame, "Include Electrical:", "include_electrical", False, row, vars_dict, widget_type="checkbox")
    row = add_input_row(mep_frame, "Electrical Allowance ($):", "electrical_allowance", "0.0", row, vars_dict)
    row = add_input_row(mep_frame, "Include Plumbing:", "include_plumbing", False, row, vars_dict, widget_type="checkbox")
    row = add_input_row(mep_frame, "Plumbing Allowance ($):", "plumbing_allowance", "0.0", row, vars_dict)
    row = add_input_row(mep_frame, "Include Mechanical:", "include_mechanical", False, row, vars_dict, widget_type="checkbox")
    row = add_input_row(mep_frame, "Mechanical Allowance ($):", "mechanical_allowance", "0.0", row, vars_dict)
    row += 1
    
    # Pricing Section
    pricing_frame, row = create_input_section(scrollable_frame, "Pricing", row, vars_dict)
    row = add_input_row(pricing_frame, "Tax Rate (decimal):", "tax_rate", "0.08", row, vars_dict)
    ttk.Label(pricing_frame, text="(e.g., 0.08 = 8%)", font=("TkDefaultFont", 7)).grid(row=row-1, column=2, sticky="w", padx=5)
    row += 1
    
    # Markup Settings Section
    markup_frame, row = create_input_section(scrollable_frame, "Markup Settings", row, vars_dict)
    row = add_input_row(markup_frame, "Material Markup (%):", "material_markup_pct", "15.0", row, vars_dict)
    ttk.Label(markup_frame, text="(e.g., 15.0 = 15%)", font=("TkDefaultFont", 7)).grid(row=row-1, column=2, sticky="w", padx=5)
    row = add_input_row(markup_frame, "Labor Markup (%):", "labor_markup_pct", "10.0", row, vars_dict)
    ttk.Label(markup_frame, text="(e.g., 10.0 = 10%)", font=("TkDefaultFont", 7)).grid(row=row-1, column=2, sticky="w", padx=5)
    row = add_input_row(markup_frame, "Subcontractor Markup (%):", "subcontractor_markup_pct", "10.0", row, vars_dict)
    ttk.Label(markup_frame, text="(e.g., 10.0 = 10%)", font=("TkDefaultFont", 7)).grid(row=row-1, column=2, sticky="w", padx=5)
    row = add_input_row(markup_frame, "Overhead (%):", "overhead_pct", "0.0", row, vars_dict)
    ttk.Label(markup_frame, text="(e.g., 5.0 = 5% of material+labor)", font=("TkDefaultFont", 7)).grid(row=row-1, column=2, sticky="w", padx=5)
    row += 1
    
    # Calculate button
    calc_button = ttk.Button(
        scrollable_frame,
        text="Calculate",
        command=lambda: run_calculation(vars_dict, output_text, status_label),
    )
    calc_button.grid(row=row, column=0, columnspan=2, pady=15, sticky="ew", padx=5)
    row += 1
    
    # Configure scrollable frame column
    scrollable_frame.columnconfigure(0, weight=1)
    
    # Right panel - Output
    output_frame = ttk.LabelFrame(root, text="Results", padding=10)
    output_frame.grid(row=0, column=2, sticky="nsew", padx=5)
    output_frame.columnconfigure(0, weight=1)
    output_frame.rowconfigure(0, weight=1)
    root.columnconfigure(2, weight=2)
    
    # Output text area with scrollbar
    output_text = scrolledtext.ScrolledText(
        output_frame,
        width=60,
        height=40,
        wrap=tk.WORD,
        font=("Consolas", 9),
    )
    output_text.grid(row=0, column=0, sticky="nsew")
    
    # Status label
    status_label = ttk.Label(root, text="Ready", foreground="gray")
    status_label.grid(row=1, column=0, columnspan=3, sticky="w", padx=10, pady=5)
    
    # Initial message
    output_text.insert(tk.END, "Pole Barn Calculator\n")
    output_text.insert(tk.END, "=" * 70 + "\n\n")
    output_text.insert(tk.END, "Enter your barn dimensions and click 'Calculate'.\n\n")
    output_text.insert(tk.END, "Default values are pre-filled. Adjust as needed.\n\n")
    output_text.insert(tk.END, "Note: Roof pitch accepts formats like '4/12', '3/12', or '0.333'.\n")
    output_text.insert(tk.END, "      Peak height is automatically calculated.\n")
    output_text.insert(tk.END, "      Labor rate: $50/hr (default, configurable).\n")
    
    root.mainloop()


if __name__ == "__main__":
    main()
```

---

### File: apps/cli.py

```python
"""Command-line interface for pole barn calculator."""

import click
import json
from pathlib import Path
from systems.pole_barn.model import (
    PoleBarnInputs,
    GeometryInputs,
    MaterialInputs,
    PricingInputs,
    AssemblyInputs,
)
from systems.pole_barn.calculator import PoleBarnCalculator
from systems.pole_barn import geometry as geometry_module
from systems.pole_barn import assemblies as assemblies_module


def parse_roof_pitch(pitch_str: str) -> float:
    """
    Parse roof pitch from various formats into a numeric ratio.
    
    Accepts:
    - "4/12", "3/12" (rise/run)
    - "4" or "3" (assumes X/12)
    - "0.333" (decimal ratio)
    
    Returns float ratio (e.g., 4/12 = 0.333...)
    """
    pitch_str = pitch_str.strip()
    
    # If it contains a slash, parse as rise/run
    if '/' in pitch_str:
        parts = pitch_str.split('/')
        if len(parts) == 2:
            try:
                rise = float(parts[0])
                run = float(parts[1])
                if run == 0:
                    raise ValueError("Run cannot be zero")
                return rise / run
            except ValueError:
                raise ValueError(f"Invalid pitch format: {pitch_str}")
    
    # Try parsing as a number
    try:
        pitch_num = float(pitch_str)
        # If it's a whole number or small decimal, assume it's rise per 12
        if pitch_num > 0 and pitch_num < 12:
            return pitch_num / 12.0
        # If it's between 0 and 2, treat as a ratio directly
        elif pitch_num > 0 and pitch_num < 2:
            return pitch_num
        else:
            raise ValueError(f"Pitch value {pitch_num} out of expected range")
    except ValueError:
        raise ValueError(f"Invalid pitch format: {pitch_str}")


@click.command()
@click.option("--project-name", help="Project name or identifier")
@click.option("--length", type=float, required=True, help="Length of barn in feet")
@click.option("--width", type=float, required=True, help="Width of barn in feet")
@click.option("--eave-height", type=float, required=True, help="Eave height in feet")
@click.option("--peak-height", type=float, default=None, help="Peak height in feet (optional, will be derived if not provided)")
@click.option("--roof-pitch", type=str, required=True, help="Roof pitch (e.g., '4/12', '3/12', or 0.333)")
@click.option("--roof-style", type=click.Choice(["gable", "shed"]), default="gable", help="Roof style: gable or shed")
@click.option("--ridge-position", type=float, default=None, help="Ridge position from left eave in feet (default: centered)")
@click.option("--overhang-front", type=float, default=0.0, help="Front overhang in feet")
@click.option("--overhang-rear", type=float, default=0.0, help="Rear overhang in feet")
@click.option("--overhang-sides", type=float, default=0.0, help="Side overhangs in feet")
@click.option("--door-count", type=int, default=0, help="Number of doors")
@click.option("--door-width", type=float, default=0.0, help="Door width in feet")
@click.option("--door-height", type=float, default=0.0, help="Door height in feet")
@click.option("--window-count", type=int, default=0, help="Number of windows")
@click.option("--window-width", type=float, default=0.0, help="Window width in feet")
@click.option("--window-height", type=float, default=0.0, help="Window height in feet")
@click.option("--overhead-door-count", type=int, default=0, help="Number of overhead/roll-up doors")
@click.option("--overhead-door-type", type=click.Choice(["none", "steel_rollup", "sectional"]), default="none", help="Overhead door type")
@click.option("--pole-spacing-length", type=float, required=True, help="Pole spacing along length in feet")
@click.option("--pole-spacing-width", type=float, required=True, help="Pole spacing along width in feet")
@click.option("--pole-diameter", type=float, required=True, help="Pole diameter in inches")
@click.option("--pole-depth", type=float, required=True, help="Pole depth in ground in feet")
@click.option("--roof-material", type=str, required=True, help="Roof material type (e.g., metal, shingle)")
@click.option("--roof-gauge", type=float, help="Roof gauge (for metal roofing)")
@click.option("--wall-material", type=str, required=True, help="Wall material type (e.g., metal, wood)")
@click.option("--wall-gauge", type=float, help="Wall gauge (for metal walls)")
@click.option("--truss-type", type=str, required=True, help="Truss type (e.g., scissor, standard, gambrel)")
@click.option("--truss-spacing", type=float, required=True, help="Truss spacing in feet")
@click.option("--purlin-spacing", type=float, required=True, help="Purlin spacing in feet")
@click.option("--girt-spacing", type=float, required=True, help="Girt spacing in feet")
@click.option("--foundation-type", type=str, required=True, help="Foundation type (e.g., concrete_pad, gravel)")
@click.option("--concrete-thickness", type=float, help="Concrete thickness in inches")
@click.option("--insulation-type", type=str, help="Insulation type (e.g., fiberglass, spray_foam) [deprecated]")
@click.option("--insulation-r-value", type=float, help="Insulation R-value [deprecated]")
@click.option("--exterior-finish-type", type=click.Choice(["metal_29ga", "metal_26ga", "lap_siding", "stucco"]), default="metal_29ga", help="Exterior finish type")
@click.option("--wall-insulation-type", type=click.Choice(["none", "fiberglass_batts", "rock_wool", "rigid_board", "spray_foam"]), default="none", help="Wall insulation type")
@click.option("--roof-insulation-type", type=click.Choice(["none", "fiberglass_batts", "rock_wool", "rigid_board", "spray_foam"]), default="none", help="Roof insulation type")
@click.option("--girt-type", type=click.Choice(["standard", "commercial"]), default="standard", help="Girt type: standard or commercial")
@click.option("--wall-sheathing-type", type=click.Choice(["none", "osb", "plywood"]), default="none", help="Wall sheathing type")
@click.option("--roof-sheathing-type", type=click.Choice(["none", "osb", "plywood"]), default="none", help="Roof sheathing type")
@click.option("--floor-type", type=click.Choice(["none", "slab", "gravel"]), default="none", help="Floor type")
@click.option("--slab-thickness", type=float, default=None, help="Slab thickness in inches (if floor-type is slab)")
@click.option("--slab-reinforcement", type=click.Choice(["none", "mesh", "rebar"]), default="none", help="Slab reinforcement type")
@click.option("--post-type", type=click.Choice(["pt_solid", "laminated"]), default="pt_solid", help="Post type: pt_solid or laminated")
@click.option("--post-truss-connection", type=click.Choice(["notched", "cleated"]), default="notched", help="Truss/post connection type")
@click.option("--labor-rate", type=float, default=None, help="Labor rate per hour (optional, defaults to 50.0)")
@click.option("--material-markup", type=float, default=None, help="Material markup multiplier (e.g., 1.15 for 15%%) - legacy, use --material-markup-pct instead")
@click.option("--material-markup-pct", type=float, default=None, help="Material markup as percentage (e.g., 15.0 for 15%%)")
@click.option("--labor-markup-pct", type=float, default=None, help="Labor markup as percentage (e.g., 10.0 for 10%%)")
@click.option("--subcontractor-markup-pct", type=float, default=None, help="Subcontractor markup as percentage (e.g., 10.0 for 10%%)")
@click.option("--overhead-pct", type=float, default=None, help="Overhead as percentage of (material + labor) (e.g., 5.0 for 5%%)")
@click.option("--tax-rate", type=float, required=True, help="Tax rate as decimal (e.g., 0.08 for 8%%)")
@click.option("--delivery-cost", type=float, help="Delivery cost")
@click.option("--permit-cost", type=float, help="Permit cost")
@click.option("--site-prep-cost", type=float, help="Site preparation cost")
@click.option("--include-electrical", is_flag=True, help="Include basic electrical")
@click.option("--electrical-allowance", type=float, default=0.0, help="Electrical allowance in dollars")
@click.option("--include-plumbing", is_flag=True, help="Include plumbing")
@click.option("--plumbing-allowance", type=float, default=0.0, help="Plumbing allowance in dollars")
@click.option("--include-mechanical", is_flag=True, help="Include mechanical (heat/vent)")
@click.option("--mechanical-allowance", type=float, default=0.0, help="Mechanical allowance in dollars")
@click.option("--build-type", type=click.Choice(["pole", "stick_frame"]), default="pole", help="Build type: pole or stick_frame")
@click.option("--construction-type", type=click.Choice(["new", "addition"]), default="new", help="Construction type: new or addition")
@click.option("--building-type", type=click.Choice(["residential", "commercial"]), default="residential", help="Building type: residential or commercial")
@click.option("--building-use", type=str, default=None, help="Building use/description")
@click.option("--permitting-agency", type=str, default=None, help="Permitting agency")
@click.option("--required-snow-load", type=float, default=None, help="Required snow load in psf")
@click.option("--requested-snow-load", type=float, default=None, help="Requested snow load in psf")
@click.option("--snow-load-unknown", is_flag=True, help="Flag if snow load needs lookup")
@click.option("--assembly-method", type=str, required=True, help="Assembly method (e.g., standard, prefab)")
@click.option("--fastening-type", type=str, required=True, help="Fastening type (e.g., screws, nails)")
@click.option("--weather-sealing", is_flag=True, help="Include weather sealing")
@click.option("--ventilation-type", type=str, help="Ventilation type (e.g., ridge_vent, gable_vent)")
@click.option("--ventilation-count", type=int, help="Number of ventilation units")
@click.option("--skylight-count", type=int, help="Number of skylights")
@click.option("--skylight-size", type=float, help="Skylight size in square feet")
@click.option("--notes", type=str, help="Additional notes or special requirements")
@click.option("--output-format", type=click.Choice(["summary", "json", "detailed"]), default="summary", help="Output format")
def main(
    project_name,
    length,
    width,
    eave_height,
    peak_height,
    roof_pitch,
    roof_style,
    ridge_position,
    overhang_front,
    overhang_rear,
    overhang_sides,
    door_count,
    door_width,
    door_height,
    window_count,
    window_width,
    window_height,
    overhead_door_count,
    overhead_door_type,
    pole_spacing_length,
    pole_spacing_width,
    pole_diameter,
    pole_depth,
    roof_material,
    roof_gauge,
    wall_material,
    wall_gauge,
    truss_type,
    truss_spacing,
    purlin_spacing,
    girt_spacing,
    foundation_type,
    concrete_thickness,
    insulation_type,
    insulation_r_value,
    exterior_finish_type,
    wall_insulation_type,
    roof_insulation_type,
    girt_type,
    wall_sheathing_type,
    roof_sheathing_type,
    floor_type,
    slab_thickness,
    slab_reinforcement,
    post_type,
    post_truss_connection,
    labor_rate,
    material_markup,
    material_markup_pct,
    labor_markup_pct,
    subcontractor_markup_pct,
    overhead_pct,
    tax_rate,
    delivery_cost,
    permit_cost,
    site_prep_cost,
    include_electrical,
    electrical_allowance,
    include_plumbing,
    plumbing_allowance,
    include_mechanical,
    mechanical_allowance,
    build_type,
    construction_type,
    building_type,
    building_use,
    permitting_agency,
    required_snow_load,
    requested_snow_load,
    snow_load_unknown,
    assembly_method,
    fastening_type,
    weather_sealing,
    ventilation_type,
    ventilation_count,
    skylight_count,
    skylight_size,
    notes,
    output_format,
):
    """Pole Barn Calculator - Calculate materials and costs for pole barn construction."""
    
    # Parse roof pitch (can be "4/12", "3/12", or "0.333")
    try:
        roof_pitch_ratio = parse_roof_pitch(roof_pitch)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        return
    
    # Determine ridge position (default to centered if not provided for gable roofs)
    ridge_pos = ridge_position
    if roof_style == "gable" and ridge_pos is None:
        ridge_pos = length / 2.0
    
    # Build geometry inputs
    # Peak height is optional - will be derived if not provided (per changelog entry [4])
    geometry = GeometryInputs(
        length=length,
        width=width,
        eave_height=eave_height,
        peak_height=peak_height,  # None if not provided, will be derived
        roof_pitch=roof_pitch_ratio,
        roof_style=roof_style,
        ridge_position_ft_from_left=ridge_pos if roof_style == "gable" else None,
        overhang_front=overhang_front,
        overhang_rear=overhang_rear,
        overhang_sides=overhang_sides,
        door_count=door_count,
        door_width=door_width,
        door_height=door_height,
        window_count=window_count,
        window_width=window_width,
        window_height=window_height,
        pole_spacing_length=pole_spacing_length,
        pole_spacing_width=pole_spacing_width,
        pole_diameter=pole_diameter,
        pole_depth=pole_depth,
        overhead_door_count=overhead_door_count,
        overhead_door_type=overhead_door_type,
    )
    
    # Build material inputs
    materials = MaterialInputs(
        roof_material_type=roof_material,
        roof_gauge=roof_gauge,
        wall_material_type=wall_material,
        wall_gauge=wall_gauge,
        truss_type=truss_type,
        truss_spacing=truss_spacing,
        purlin_spacing=purlin_spacing,
        girt_spacing=girt_spacing,
        foundation_type=foundation_type if floor_type == "none" else floor_type,
        concrete_thickness=concrete_thickness if slab_thickness is None else slab_thickness,
        insulation_type=insulation_type,
        insulation_r_value=insulation_r_value,
        exterior_finish_type=exterior_finish_type,
        wall_insulation_type=wall_insulation_type,
        roof_insulation_type=roof_insulation_type,
        girt_type=girt_type,
        wall_sheathing_type=wall_sheathing_type,
        roof_sheathing_type=roof_sheathing_type,
        floor_type=floor_type,
        slab_thickness_in=slab_thickness,
        slab_reinforcement=slab_reinforcement,
    )
    
    # Build pricing inputs
    # Labor rate uses default if not provided (per changelog entry [4])
    # Handle material_markup: use material_markup_pct if provided, otherwise use legacy material_markup
    if material_markup_pct is not None:
        # New percentage-based markup
        material_markup_value = 1.0 + (material_markup_pct / 100.0)  # Convert 15% to 1.15 for backward compat
    elif material_markup is not None:
        # Legacy multiplier format
        material_markup_value = material_markup
    else:
        # Default to 15% if neither provided
        material_markup_value = 1.15
    
    pricing = PricingInputs(
        material_markup=material_markup_value,  # Legacy field for backward compatibility
        tax_rate=tax_rate,
        labor_rate=labor_rate if labor_rate is not None else 50.0,  # Default 50.0 if not provided
        delivery_cost=delivery_cost,
        permit_cost=permit_cost,
        site_prep_cost=site_prep_cost,
        include_electrical=include_electrical,
        electrical_allowance=electrical_allowance,
        include_plumbing=include_plumbing,
        plumbing_allowance=plumbing_allowance,
        include_mechanical=include_mechanical,
        mechanical_allowance=mechanical_allowance,
        material_markup_pct=material_markup_pct if material_markup_pct is not None else 15.0,
        labor_markup_pct=labor_markup_pct if labor_markup_pct is not None else 10.0,
        subcontractor_markup_pct=subcontractor_markup_pct if subcontractor_markup_pct is not None else 10.0,
        overhead_pct=overhead_pct if overhead_pct is not None else 0.0,
    )
    
    # Build assembly inputs
    assemblies = AssemblyInputs(
        assembly_method=assembly_method,
        fastening_type=fastening_type,
        weather_sealing=weather_sealing,
        ventilation_type=ventilation_type,
        ventilation_count=ventilation_count,
        skylight_count=skylight_count,
        skylight_size=skylight_size,
        post_type=post_type,
        post_truss_connection_type=post_truss_connection,
    )
    
    # Build complete inputs
    inputs = PoleBarnInputs(
        geometry=geometry,
        materials=materials,
        pricing=pricing,
        assemblies=assemblies,
        project_name=project_name,
        notes=notes,
        build_type=build_type,
        construction_type=construction_type,
        building_type=building_type,
        building_use=building_use,
        permitting_agency=permitting_agency,
        required_snow_load_psf=required_snow_load,
        requested_snow_load_psf=requested_snow_load,
        snow_load_unknown=snow_load_unknown,
    )
    
    # Create calculator and run full calculation
    # Use explicit config_dir for consistency
    config_dir = Path(__file__).parent.parent / "config"
    calculator = PoleBarnCalculator(config_dir=config_dir)
    
    try:
        calculator.load_config()
        geom_model, takeoff, priced_items, pricing_summary = calculator.calculate(inputs)
        openings = geometry_module.calculate_door_window_openings(geometry)
    except Exception as e:
        click.echo(f"Error during calculation: {e}", err=True)
        import traceback
        if output_format == "detailed":
            click.echo(traceback.format_exc(), err=True)
        return
    
    # Display input summary
    click.echo("=" * 60)
    click.echo("POLE BARN CALCULATOR")
    click.echo("=" * 60)
    
    if project_name:
        click.echo(f"\nProject: {project_name}")
    
    click.echo(f"\nDimensions: {length}ft x {width}ft")
    # Peak height is derived - get it from the geometry model
    click.echo(f"Height: Eave {eave_height}ft, Peak {geom_model.peak_height_ft:.2f}ft (derived)")
    click.echo(f"Roof Pitch: {roof_pitch} ({roof_pitch_ratio:.4f} ratio)")
    click.echo(f"Roof Style: {roof_style}")
    click.echo(f"Pole Spacing: {pole_spacing_length}ft x {pole_spacing_width}ft")
    click.echo(f"Materials: {roof_material} roof, {wall_material} walls")
    click.echo(f"Truss Type: {truss_type}")
    
    # Display geometry results (Phase 1)
    click.echo("\n" + "=" * 60)
    click.echo("GEOMETRY CALCULATIONS (Phase 1 - Implemented)")
    click.echo("=" * 60)
    click.echo(f"\nBays & Frames:")
    click.echo(f"  Bay Spacing: {geom_model.bay_spacing_ft}ft")
    click.echo(f"  Number of Bays: {geom_model.num_bays}")
    click.echo(f"  Number of Frame Lines: {geom_model.num_frame_lines}")
    
    click.echo(f"\nAreas:")
    click.echo(f"  Footprint: {geom_model.footprint_area_sqft:.2f} sq ft")
    click.echo(f"  Sidewalls: {geom_model.sidewall_area_sqft:.2f} sq ft")
    click.echo(f"  Endwalls: {geom_model.endwall_area_sqft:.2f} sq ft")
    click.echo(f"  Total Walls: {geom_model.total_wall_area_sqft:.2f} sq ft")
    click.echo(f"  Roof: {geom_model.roof_area_sqft:.2f} sq ft")
    
    if geom_model.building_volume_cuft:
        click.echo(f"\nVolume:")
        click.echo(f"  Building Volume: {geom_model.building_volume_cuft:.2f} cu ft")
    
    if openings['door_area'] > 0 or openings['window_area'] > 0:
        click.echo(f"\nOpenings:")
        if openings['door_area'] > 0:
            click.echo(f"  Door Area: {openings['door_area']:.2f} sq ft")
        if openings['window_area'] > 0:
            click.echo(f"  Window Area: {openings['window_area']:.2f} sq ft")
    
    # Display material quantities (Phase 2)
    if takeoff.items:
        click.echo("\n" + "=" * 60)
        click.echo("MATERIAL QUANTITIES (Phase 2 - Implemented)")
        click.echo("=" * 60)
        
        # Group by category
        by_category = {}
        for item in takeoff.items:
            if item.category not in by_category:
                by_category[item.category] = []
            by_category[item.category].append(item)
        
        # Display framing
        if "framing" in by_category:
            click.echo(f"\nFraming:")
            for item in by_category["framing"]:
                click.echo(f"  {item.description}: {item.quantity:.1f} {item.unit}")
        
        # Display roof
        if "roof" in by_category:
            click.echo(f"\nRoof:")
            for item in by_category["roof"]:
                click.echo(f"  {item.description}: {item.quantity:.1f} {item.unit}")
        
        # Display walls
        if "wall" in by_category:
            click.echo(f"\nWalls:")
            for item in by_category["wall"]:
                click.echo(f"  {item.description}: {item.quantity:.1f} {item.unit}")
        
        # Display trim
        if "trim" in by_category:
            click.echo(f"\nTrim:")
            for item in by_category["trim"]:
                click.echo(f"  {item.description}: {item.quantity:.1f} {item.unit}")
    
    # Display pricing (Phase 3)
    if priced_items:
        click.echo("\n" + "=" * 60)
        click.echo("COST BREAKDOWN (Phase 3 - Implemented)")
        click.echo("=" * 60)
        
        # Group priced items by category
        priced_by_category = {}
        for item in priced_items:
            if item.category not in priced_by_category:
                priced_by_category[item.category] = []
            priced_by_category[item.category].append(item)
        
        # Display major line items
        click.echo("\nMajor Line Items:")
        for category in ["framing", "roof", "wall", "trim"]:
            if category in priced_by_category:
                click.echo(f"\n{category.title()}:")
                for item in priced_by_category[category]:
                    if item.total_cost > 0:
                        click.echo(
                            f"  {item.description}: "
                            f"{item.quantity:.1f} {item.unit} @ ${item.unit_price:.2f}/{item.unit} = "
                            f"${item.total_cost:.2f}"
                        )
        
        # Display summary
        click.echo("\n" + "-" * 60)
        click.echo("COST SUMMARY")
        click.echo("-" * 60)
        click.echo(f"Material Subtotal: ${pricing_summary.material_subtotal:,.2f}")
        click.echo(f"Labor Subtotal:    ${pricing_summary.labor_subtotal:,.2f}")
        click.echo(f"Markup Total:      ${pricing_summary.markup_total:,.2f}")
        click.echo(f"Tax Total:         ${pricing_summary.tax_total:,.2f}")
        click.echo("-" * 60)
        click.echo(f"GRAND TOTAL:       ${pricing_summary.grand_total:,.2f}")
        click.echo("=" * 60)
    
    if output_format == "json":
        # Convert to dictionaries for JSON
        quantities_dict = [
            {
                "name": item.name,
                "description": item.description,
                "category": item.category,
                "quantity": item.quantity,
                "unit": item.unit,
                "notes": item.notes,
            }
            for item in takeoff.items
        ]
        
        priced_items_dict = [
            {
                "name": item.name,
                "description": item.description,
                "category": item.category,
                "quantity": item.quantity,
                "unit": item.unit,
                "part_id": item.part_id,
                "unit_price": item.unit_price,
                "material_cost": item.material_cost,
                "labor_hours": item.labor_hours,
                "labor_cost": item.labor_cost,
                "markup_percent": item.markup_percent,
                "markup_amount": item.markup_amount,
                "total_cost": item.total_cost,
                "notes": item.notes,
            }
            for item in priced_items
        ]
        
        click.echo("\n" + json.dumps({
            "project_name": project_name,
            "geometry": {
                "dimensions": {
                    "length_ft": length,
                    "width_ft": width,
                    "eave_height_ft": eave_height,
                    "peak_height_ft": peak_height,
                },
                "bays": {
                    "bay_spacing_ft": geom_model.bay_spacing_ft,
                    "num_bays": geom_model.num_bays,
                    "num_frame_lines": geom_model.num_frame_lines,
                },
                "areas": {
                    "footprint_sqft": geom_model.footprint_area_sqft,
                    "sidewall_sqft": geom_model.sidewall_area_sqft,
                    "endwall_sqft": geom_model.endwall_area_sqft,
                    "total_wall_sqft": geom_model.total_wall_area_sqft,
                    "roof_sqft": geom_model.roof_area_sqft,
                },
                "volume_cuft": geom_model.building_volume_cuft,
                "openings": openings,
            },
            "material_quantities": quantities_dict,
            "priced_items": priced_items_dict,
            "pricing_summary": {
                "material_subtotal": pricing_summary.material_subtotal,
                "labor_subtotal": pricing_summary.labor_subtotal,
                "markup_total": pricing_summary.markup_total,
                "tax_total": pricing_summary.tax_total,
                "grand_total": pricing_summary.grand_total,
            },
            "status": "all_phases_implemented",
        }, indent=2))
    elif output_format == "detailed":
        click.echo("\n" + "=" * 60)
        click.echo("DETAILED GEOMETRY SUMMARY")
        click.echo("=" * 60)
        click.echo(json.dumps(geom_summary, indent=2))


if __name__ == "__main__":
    main()

```

---

## Configuration Files

### File: config/parts.example.csv

```csv
part_id,part_name,description,category,unit,vendor,source,notes
POST_6X6_PT,6x6 PT Post,6x6 PT post,framing,ea,HomeDepot,real,Avg of 8-12 ft PT posts
LBR_2X6_LF,2x6 Lumber,2x6 SPF framing lumber,framing,lf,HomeDepot,real,Price derived from 2x6x12
METAL_PANEL_29_SQFT,Metal Panel 29ga,29ga metal roof/wall panel,skin,sqft,HomeDepot,real,12' panel covers 36 sqft
TRIM_EAVE,Eave Trim,Metal eave trim,trim,lf,Assumed,assumed,-
TRIM_RAKE,Rake Trim,Metal rake trim,trim,lf,Assumed,assumed,-
TRIM_BASE,Base Trim,Metal base trim,trim,lf,Assumed,assumed,-
TRIM_CORNER,Corner Trim,Metal corner trim,trim,lf,Assumed,assumed,-
RIDGE_CAP,Ridge Cap,Metal ridge cap,trim,lf,Assumed,assumed,-
SCREW_METAL,Metal Screw,Metal roofing screw,fasteners,ea,HomeDepot,real,Derived from 100-pack pricing
CONCRETE_CY,Concrete,Concrete (bag-equivalent),concrete,cuyd,HomeDepot,real,Derived from 80 lb Sakrete bags
INS_R19_SQFT,R-19 Insulation,R-19 fiberglass batt insulation,insulation,sqft,OwensCorning,real,E61 bag coverage
VENT_RIDGE,Ridge Vent,Continuous ridge vent,ventilation,lf,Assumed,assumed,-
VENT_GABLE,Gable Vent,Gable vent,ventilation,ea,Assumed,assumed,-
DELIVERY_LUMP,Delivery,Delivery allowance,soft_cost,lump,Assumed,assumed,-
PERMIT_LUMP,Permit,Permit allowance,soft_cost,lump,Assumed,assumed,-
SITE_PREP_LUMP,Site Prep,Site prep allowance,soft_cost,lump,Assumed,assumed,-
TRUSS_STD,Standard Truss,Engineered pole barn truss,framing,ea,Assumed,assumed,Typical 30-40 ft span truss
METAL_PANEL_26_SQFT,Metal Panel 26ga,26ga metal roof/wall panel,skin,sqft,HomeDepot,real,12' panel covers 36 sqft
TRIM_DOOR,Door Trim,Metal door trim,trim,lf,Assumed,assumed,-
TRIM_WINDOW,Window Trim,Metal window trim,trim,lf,Assumed,assumed,-
INS_ROCKWOOL_SQFT,Rock Wool Insulation,Rock wool batt insulation,insulation,sqft,Assumed,assumed,R-19 equivalent
INS_RIGID_SQFT,Rigid Board Insulation,Rigid board insulation,insulation,sqft,Assumed,assumed,R-5 per inch
INS_SPRAYFOAM_SQFT,Spray Foam Insulation,Spray foam insulation,insulation,sqft,Assumed,assumed,R-6 per inch (closed-cell)
SHEATHING_OSB_SQFT,OSB Sheathing,OSB sheathing 7/16",sheathing,sqft,HomeDepot,real,4' x 8' sheets
SHEATHING_PLY_SQFT,Plywood Sheathing,Plywood sheathing 1/2",sheathing,sqft,HomeDepot,real,4' x 8' sheets
OVERHEAD_DOOR,Overhead Door,Steel roll-up door unit,doors,ea,Assumed,assumed,8' x 7' typical
```

---

### File: config/pricing.example.csv

```csv
part_id,pricing_profile,unit_price
POST_6X6_PT,Default,75.00
LBR_2X6_LF,Default,1.16
METAL_PANEL_29_SQFT,Default,1.45
TRIM_EAVE,Default,3.13
TRIM_RAKE,Default,3.13
TRIM_BASE,Default,3.13
TRIM_CORNER,Default,3.13
RIDGE_CAP,Default,3.75
SCREW_METAL,Default,0.17
CONCRETE_CY,Default,270.00
INS_R19_SQFT,Default,0.83
VENT_RIDGE,Default,4.00
VENT_GABLE,Default,80.00
DELIVERY_LUMP,Default,300.00
PERMIT_LUMP,Default,500.00
SITE_PREP_LUMP,Default,1000.00
TRUSS_STD,Default,312.50
METAL_PANEL_26_SQFT,Default,1.81
TRIM_DOOR,Default,3.13
TRIM_WINDOW,Default,3.13
INS_ROCKWOOL_SQFT,Default,1.15
INS_RIGID_SQFT,Default,1.50
INS_SPRAYFOAM_SQFT,Default,2.25
SHEATHING_OSB_SQFT,Default,0.75
SHEATHING_PLY_SQFT,Default,1.10
OVERHEAD_DOOR,Default,1062.50
```

---

### File: config/assemblies.example.csv

```csv
assembly_name,category,part_id,waste_factor,labor_per_unit
posts,framing,POST_6X6_PT,1.00,0.25
trusses,framing,TRUSS_STD,1.00,0.35
sidewall_girts,framing,LBR_2X6_LF,1.05,0.02
endwall_girts,framing,LBR_2X6_LF,1.05,0.02
roof_purlins,framing,LBR_2X6_LF,1.05,0.02
roof_panels,skin,METAL_PANEL_29_SQFT,1.05,0.03
sidewall_panels,skin,METAL_PANEL_29_SQFT,1.05,0.03
endwall_panels,skin,METAL_PANEL_29_SQFT,1.05,0.03
roof_panels_26ga,skin,METAL_PANEL_26_SQFT,1.05,0.03
sidewall_panels_26ga,skin,METAL_PANEL_26_SQFT,1.05,0.03
endwall_panels_26ga,skin,METAL_PANEL_26_SQFT,1.05,0.03
eave_trim,trim,TRIM_EAVE,1.10,0.02
rake_trim,trim,TRIM_RAKE,1.10,0.02
base_trim,trim,TRIM_BASE,1.10,0.02
corner_trim,trim,TRIM_CORNER,1.10,0.03
roof_fasteners,fasteners,SCREW_METAL,1.05,0.00
wall_fasteners,fasteners,SCREW_METAL,1.05,0.00
trim_fasteners,fasteners,SCREW_METAL,1.05,0.00
post_concrete,concrete,CONCRETE_CY,1.05,0.00
slab_concrete,concrete,CONCRETE_CY,1.05,0.00
wall_insulation,insulation,INS_R19_SQFT,1.00,0.02
wall_insulation_rockwool,insulation,INS_ROCKWOOL_SQFT,1.00,0.02
wall_insulation_rigid,insulation,INS_RIGID_SQFT,1.05,0.02
wall_insulation_sprayfoam,insulation,INS_SPRAYFOAM_SQFT,1.00,0.02
roof_insulation,insulation,INS_R19_SQFT,1.00,0.02
roof_insulation_rockwool,insulation,INS_ROCKWOOL_SQFT,1.00,0.02
roof_insulation_rigid,insulation,INS_RIGID_SQFT,1.05,0.02
roof_insulation_sprayfoam,insulation,INS_SPRAYFOAM_SQFT,1.00,0.02
ridge_vent,ventilation,VENT_RIDGE,1.00,0.03
gable_vent,ventilation,VENT_GABLE,1.00,0.25
delivery,soft_cost,DELIVERY_LUMP,1.00,0.00
permit,soft_cost,PERMIT_LUMP,1.00,0.00
site_prep,soft_cost,SITE_PREP_LUMP,1.00,0.00
door_framing,framing,LBR_2X6_LF,1.05,0.05
window_framing,framing,LBR_2X6_LF,1.05,0.05
door_trim,trim,TRIM_DOOR,1.10,0.02
window_trim,trim,TRIM_WINDOW,1.10,0.02
```

---

## Documentation Files

### File: README.md

# Pole Barn Calculator

A Python calculator for pole barn construction materials, quantities, and costs.

## Project Status

**Current Phase: First Pass - Structure and Data Models**

This is the initial structure of the project. All calculation functions are currently stubbed with `NotImplementedError`. The focus of this phase is:

- ✅ Project structure and organization
- ✅ Data model definitions (dataclasses)
- ✅ CLI interface for accepting inputs
- ✅ Function stubs for all calculations
- ✅ Control document listing all variables
- ⏳ **Next**: Implement actual calculation logic

## Project Structure

```
pole_barn_calc/
├── README.md
├── pyproject.toml
├── config/
│   ├── parts.example.csv
│   ├── pricing.example.csv
│   └── assemblies.example.csv
├── systems/
│   ├── __init__.py
│   └── pole_barn/
│       ├── __init__.py
│       ├── model.py          # Data models (dataclasses)
│       ├── geometry.py       # Geometry calculations (stubbed)
│       ├── assemblies.py     # Material quantity calculations (stubbed)
│       ├── pricing.py        # Cost calculations (stubbed)
│       └── calculator.py     # Main calculator class (stubbed)
├── apps/
│   ├── __init__.py
│   └── cli.py                # Command-line interface
├── control/
│   └── pole_barn_calculator.md  # Control document with all variables
└── tests/
    ├── test_geometry.py
    ├── test_assemblies.py
    └── test_end_to_end.py
```

## Installation

```bash
# Install in development mode
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"
```

## Usage

### Command Line Interface

The CLI accepts all input variables as command-line options. Example:

```bash
pole-barn-calc \
  --project-name "My Barn" \
  --length 40 \
  --width 30 \
  --eave-height 12 \
  --peak-height 16 \
  --roof-pitch 0.333 \
  --pole-spacing-length 8 \
  --pole-spacing-width 8 \
  --pole-diameter 6 \
  --pole-depth 4 \
  --roof-material metal \
  --roof-gauge 29 \
  --wall-material metal \
  --wall-gauge 29 \
  --truss-type standard \
  --truss-spacing 2 \
  --purlin-spacing 2 \
  --girt-spacing 2 \
  --foundation-type concrete_pad \
  --labor-rate 50 \
  --material-markup 1.15 \
  --tax-rate 0.08 \
  --assembly-method standard \
  --fastening-type screws
```

### Python API

```python
from systems.pole_barn import PoleBarnInputs, GeometryInputs, MaterialInputs, PricingInputs, AssemblyInputs
from systems.pole_barn import PoleBarnCalculator

# Create inputs
geometry = GeometryInputs(
    length=40.0,
    width=30.0,
    eave_height=12.0,
    peak_height=16.0,
    # ... other geometry inputs
)

materials = MaterialInputs(
    roof_material_type="metal",
    wall_material_type="metal",
    # ... other material inputs
)

pricing = PricingInputs(
    labor_rate=50.0,
    material_markup=1.15,
    tax_rate=0.08,
)

assemblies = AssemblyInputs(
    assembly_method="standard",
    fastening_type="screws",
)

inputs = PoleBarnInputs(
    geometry=geometry,
    materials=materials,
    pricing=pricing,
    assemblies=assemblies,
)

# Create calculator (calculations not yet implemented)
calculator = PoleBarnCalculator(inputs)
```

## Data Models

The project uses dataclasses to define input structures:

- `GeometryInputs` - Physical dimensions and layout
- `MaterialInputs` - Material specifications
- `PricingInputs` - Cost parameters
- `AssemblyInputs` - Construction method details
- `PoleBarnInputs` - Complete input set

See `control/pole_barn_calculator.md` for a complete list of all variables.

## Configuration Files

Example CSV files in `config/` demonstrate the structure for:
- **parts.example.csv** - Part catalog with IDs and descriptions
- **pricing.example.csv** - Pricing data for parts
- **assemblies.example.csv** - Assembly definitions

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black .
ruff check .
```

## Next Steps

See the summary section below for recommended next steps in development.

## License

MIT


---

### File: NEXT_STEPS.md

# Next Steps for Pole Barn Calculator

## Project Status Summary

✅ **Completed (First Pass)**
- Project structure created with all required directories
- Data models defined using dataclasses (GeometryInputs, MaterialInputs, PricingInputs, AssemblyInputs, PoleBarnInputs)
- CLI interface implemented with all input variables
- Control document created listing all variables
- Example CSV configuration files created
- Test stub files created
- README.md with project documentation

✅ **Completed (Phase 1 - Geometry)**
- `GeometryModel` dataclass created to hold derived geometry values
- All geometry calculation functions implemented:
  - `build_geometry_model()` - Main function that creates GeometryModel
  - `calculate_roof_area()` - Roof surface area with pitch and overhangs
  - `calculate_wall_area()` - Wall areas for all four sides
  - `calculate_floor_area()` - Footprint area
  - `calculate_door_window_openings()` - Opening areas
  - `calculate_roof_volume()` - Building volume
  - `get_geometry_summary()` - Complete geometry summary
- Comprehensive test suite with real numeric assertions
- CLI enhanced to display geometry results
- Pole count calculation intentionally deferred to assemblies.py

✅ **Completed (Phase 2 - Material Quantities)**
- `AssemblyQuantity` and `MaterialTakeoff` dataclasses created
- Main `calculate_material_quantities()` function implemented
- All material quantity calculations implemented:
  - Posts (count) - Based on frame lines
  - Trusses (count) - Based on truss spacing or frame lines
  - Girts (LF) - Sidewall and endwall girts based on girt spacing
  - Purlins (LF) - Roof purlins based on purlin spacing
  - Roof panels (SF) - Based on roof area from geometry
  - Wall panels (SF) - Sidewall and endwall panels
  - Trim (LF) - Eave, rake, base, and corner trim
  - Insulation (SF) - If specified
  - Ventilation (count) - If specified
- Legacy function signatures maintained for backward compatibility
- Comprehensive test suite with real numeric assertions
- CLI enhanced to display material quantities by category
- Fastener and concrete calculations intentionally deferred (require detailed specifications)

✅ **Completed (Phase 5 - Parts & Pricing Library)**
- Comprehensive parts catalog populated in `parts.example.csv`:
  - Framing: Posts, trusses, lumber (2x6)
  - Skin: Metal panels (29ga)
  - Trim: Eave, rake, base, corner, ridge cap
  - Fasteners: Metal screws
  - Concrete: Bag-equivalent pricing
  - Insulation: R-19 fiberglass batts
  - Ventilation: Ridge vent, gable vents
  - Soft costs: Delivery, permit, site prep
- Pricing data populated in `pricing.example.csv`:
  - Real pricing from Home Depot/Lowe's where available
  - Assumed pricing for trim and soft costs
  - All parts have unit prices
- Assembly mappings populated in `assemblies.example.csv`:
  - All current assembly names mapped to parts
  - Waste factors set (1.0-1.10 range, typically 1.05 for panels)
  - Labor per unit set (hours per unit of quantity)
  - Ready for fasteners and concrete when Phase 4 is implemented
- CSV schema updated to support:
  - Direct `part_id`, `waste_factor`, `labor_per_unit` columns
  - Backward compatible with old pipe-separated format
- Pricing logic verified to use waste factors and labor per unit
- Tests updated to verify waste factors and labor calculations
- Calculator ready for real-world testing with populated data

✅ **Completed (Phase 3 - Pricing & Costs)**
- `PricedLineItem` and `PricingSummary` dataclasses created
- CSV loaders implemented for parts, pricing, and assemblies configs
- Assembly mapping system to map quantities to parts
- `price_material_takeoff()` function implemented with:
  - Material cost calculation (quantity × unit_price)
  - Labor cost calculation (quantity × labor_per_unit × labor_rate)
  - Markup calculation (material + labor × markup_percent)
  - Tax calculation (material + markup × tax_rate)
  - Grand total with optional delivery, permit, site prep costs
- `PoleBarnCalculator` fully implemented with:
  - Config loading from CSV files
  - Complete calculation pipeline (geometry → quantities → pricing)
  - Summary generation
- CLI enhanced to display cost breakdown and totals
- Comprehensive test suite for pricing logic
- End-to-end tests for full calculator pipeline

## Recommended Next Steps

### Phase 1: Geometry Calculations ✅ COMPLETE
**Status**: Implemented and tested

**What was implemented:**
- `GeometryModel` dataclass with derived geometry values:
  - Core dimensions (length, width, heights, overhangs)
  - Bays and frame lines (calculated from bay spacing)
  - Areas (footprint, walls, roof)
  - Building volume
- All geometry functions now return real calculated values
- Tests validate calculations with known inputs/outputs
- CLI displays geometry results

**Assumptions made:**
- Bays calculated using `ceil(length / bay_spacing)` where bay_spacing = `pole_spacing_length`
- Roof area uses slope factor: `sqrt(1 + pitch^2)` applied to plan area with overhangs
- Wall areas calculated without subtracting openings (openings tracked separately)
- Building volume uses simple box approximation (footprint × eave_height)
- Pole counting deferred to assemblies.py (requires structural analysis)

### Phase 2: Material Quantity Calculations ✅ COMPLETE
**Status**: Implemented and tested

**What was implemented:**
- `AssemblyQuantity` dataclass for individual material items
- `MaterialTakeoff` dataclass as container for all quantities
- `calculate_material_quantities()` main function that orchestrates all calculations
- Individual quantity calculations:
  - **Posts**: `num_frame_lines × 2` (one per frame line on each sidewall)
  - **Trusses**: Based on truss spacing or frame lines (one per frame line if spacing matches bay spacing)
  - **Girts**: Calculated from eave height and girt spacing for sidewalls and endwalls
  - **Purlins**: Calculated from roof dimensions and purlin spacing for both roof slopes
  - **Roof panels**: Uses roof area from geometry (SF)
  - **Wall panels**: Uses wall areas from geometry for sidewalls and endwalls (SF)
  - **Trim**: Eave, rake, base, and corner trim (LF)
  - **Insulation**: Wall + roof area if insulation type specified (SF)
  - **Ventilation**: Count from assembly inputs if specified
- Legacy function signatures maintained (`calculate_truss_quantity()`, etc.)
- Tests validate all quantity calculations
- CLI displays quantities organized by category

**Assumptions made:**
- Posts: One post per frame line on each sidewall (simplified - actual layouts may vary)
- Trusses: One per frame line if truss spacing matches bay spacing, otherwise calculated from truss spacing
- Girts: Number of rows = `ceil(eave_height / girt_spacing)`, applied to both sidewalls and endwalls
- Purlins: Approximated using roof width/2 for each slope, multiplied by effective length
- Panels: Direct use of geometry areas (no waste factors yet - Phase 3)
- Trim: Simple perimeter and corner calculations
- Wall panels: Gross area (openings tracked separately, not subtracted yet)

**Deferred to future phases:**
- Fastener calculations (require detailed fastening patterns)
- Concrete quantity calculations (require foundation design details)
- Waste factors for materials (will be added in Phase 3 with pricing)
- Panel count estimates (requires panel size specifications)

### Phase 3: Pricing Calculations ✅ COMPLETE
**Status**: Implemented and tested

**What was implemented:**
- **Pricing dataclasses:**
  - `PricedLineItem` - Fully priced line item with material, labor, markup costs
  - `PricingSummary` - Rollup totals for all costs
  
- **CSV configuration system:**
  - `load_parts()` - Loads parts catalog from CSV
  - `load_pricing()` - Loads pricing data from CSV
  - `load_assemblies()` - Loads assembly mappings from CSV
  - Default paths point to `config/` directory
  
- **Assembly mapping:**
  - `find_assembly_mapping()` - Maps assembly names to part IDs
  - Supports pipe-separated parts and quantity multipliers
  - Fallback simple mapping for common assemblies
  - Waste factor support (defaults to 1.0 if not specified)
  
- **Pricing logic:**
  - `price_material_takeoff()` - Main pricing function
  - Material cost = effective_quantity × unit_price
  - Labor cost = effective_quantity × labor_per_unit × labor_rate
  - Markup = (material + labor) × markup_percent
  - Tax = (material + markup) × tax_rate
  - Grand total includes delivery, permit, site prep costs
  
- **Calculator integration:**
  - `PoleBarnCalculator.calculate()` - Full pipeline
  - `PoleBarnCalculator.load_config()` - Loads CSV configs
  - `PoleBarnCalculator.get_summary()` - Human-readable summary
  
- **CLI enhancements:**
  - Displays cost breakdown by category
  - Shows major line items with quantities and prices
  - Displays cost summary (material, labor, markup, tax, grand total)
  - JSON output includes all priced items and summary

**Assumptions made:**
- **Part mapping:** Uses simple fallback mapping when assemblies CSV doesn't have a match
- **Waste factors:** Defaults to 1.0 (no waste) if not specified in assemblies CSV
- **Labor:** Defaults to 0.0 hours per unit (assemblies CSV doesn't include labor_per_unit yet)
- **Markup:** Applied to material + labor costs
- **Tax:** Applied to material + markup (typical construction practice)
- **Unit prices:** Uses first match in pricing CSV (no date-based selection yet)
- **Missing parts:** Creates priced items with $0 cost and notes about missing mapping

**Configuration files used:**
- `config/parts.example.csv` - Part catalog (part_id, part_name, category, unit, description)
- `config/pricing.example.csv` - Pricing data (part_id, unit_price, unit, notes)
- `config/assemblies.example.csv` - Assembly mappings (assembly_name, parts, quantity_multiplier)

**Known limitations:**
- No waste factors in assemblies CSV yet (defaults to 1.0)
- No labor_per_unit in assemblies CSV yet (defaults to 0.0)
- Simple part mapping (uses first part if multiple parts in assembly)
- No date-based pricing selection (uses first match)
- Trim items don't have part mappings in example CSVs

1. **Implement `pricing.py` functions:**
   - `calculate_material_costs()` - Multiply quantities by unit prices from pricing.example.csv
   - `calculate_labor_costs()` - Estimate labor hours based on assembly complexity
   - `calculate_subtotal()` - Sum material and labor costs
   - `calculate_taxes()` - Apply tax rate to subtotal
   - `calculate_total_cost()` - Include all costs (materials, labor, taxes, delivery, permits, site prep)
   - `get_cost_breakdown()` - Detailed breakdown by category

2. **Labor estimation:**
   - Create labor hour estimates based on:
     - Square footage
     - Assembly method complexity
     - Material types (some materials install faster)
     - Foundation type
   - Consider creating a labor estimation table or formula

3. **Markup application:**
   - Apply material_markup to material costs
   - Consider if markup applies to all materials or just certain categories

### Phase 4: Calculator Integration (Priority: Medium)
**Goal**: Wire everything together in the main calculator class.

1. **Implement `calculator.py` methods:**
   - `calculate_geometry()` - Call all geometry functions
   - `calculate_quantities()` - Call all assembly/quantity functions
   - `calculate_costs()` - Call all pricing functions
   - `calculate_all()` - Run complete calculation pipeline
   - `get_summary()` - Format results for human-readable output

2. **Error handling:**
   - Add try/except blocks for calculation errors
   - Provide meaningful error messages
   - Validate inputs before calculations

3. **Result formatting:**
   - Create formatted output for CLI
   - Support JSON output for programmatic use
   - Create detailed breakdown reports

### Phase 5: Configuration System (Priority: Low)
**Goal**: Make configuration files functional and extensible.

1. **CSV loading:**
   - Create functions to load and parse CSV files
   - Validate CSV structure
   - Handle missing or malformed data

2. **Configuration management:**
   - Allow users to specify custom config files
   - Support environment-specific pricing
   - Allow override of default values

### Phase 6: CLI Enhancements (Priority: Low)
**Goal**: Improve user experience.

1. **Input validation:**
   - Validate all inputs before creating calculator
   - Provide helpful error messages
   - Suggest corrections for common mistakes

2. **Output formats:**
   - Enhanced summary format
   - Detailed report format
   - Export to CSV/Excel
   - Export to PDF (optional)

3. **Interactive mode:**
   - Prompt for inputs if not provided
   - Save/load project configurations
   - Support configuration presets

### Phase 7: Testing and Documentation (Priority: Medium)
**Goal**: Ensure reliability and usability.

1. **Comprehensive testing:**
   - Unit tests for all calculation functions
   - Integration tests for full workflows
   - Edge case testing
   - Performance testing for large projects

2. **Documentation:**
   - API documentation
   - User guide
   - Calculation methodology documentation
   - Examples and use cases

3. **Code quality:**
   - Type hints throughout
   - Docstrings for all functions
   - Code review and refactoring

## Technical Considerations

### Calculation Accuracy
- **Waste factors**: Industry standard waste factors should be researched and applied
- **Material sizing**: Account for standard material sizes (e.g., 4x8 sheets, standard lumber lengths)
- **Rounding**: Decide on rounding rules (round up for materials, round to 2 decimals for costs)

### Structural Engineering
- **Note**: This calculator does NOT perform structural engineering calculations
- Consider adding warnings about:
  - Local building codes
  - Wind/snow load requirements
  - Professional engineering review for large structures
  - Permits and inspections

### Data Sources
- Research current material prices (they vary by region)
- Consider integrating with pricing APIs (future enhancement)
- Allow for regional pricing variations

### Extensibility
- Design for easy addition of new material types
- Support custom assemblies
- Allow plugin-style extensions for specialized calculations

## Quick Start for Next Developer

1. **Start with geometry.py:**
   ```python
   # Example: calculate_roof_area()
   # Roof area = (length + overhangs) × (width + overhangs) × pitch_factor
   # pitch_factor accounts for the slope (use Pythagorean theorem)
   ```

2. **Test as you go:**
   - Run `pytest tests/test_geometry.py` after each function
   - Use known examples (e.g., 40x30 barn with 4:12 pitch)

3. **Reference the control document:**
   - `control/pole_barn_calculator.md` has all variable definitions
   - Use it to understand relationships between variables

4. **Follow the pattern:**
   - Functions return dictionaries with structured data
   - Include units in return values
   - Add docstrings explaining calculations

## Questions to Resolve

1. **Waste factors**: What are industry-standard waste percentages?
2. **Labor estimation**: How to estimate labor hours accurately?
3. **Material sizes**: What are standard sizes for common materials?
4. **Regional variations**: How to handle different building codes/requirements?
5. **Validation rules**: What are acceptable ranges for inputs?

---

*This document should be updated as the project progresses.*


---

### File: GUI_CHANGELOG.md

# GUI Changelog - Testing Round 1

This document tracks requested changes during testing. Changes are numbered sequentially and will be implemented in batches.

---

### [1] Roof inputs: pitch format, roof style, and ridge position

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Geometry

- **Problem:**
  - Current GUI expects `roof_pitch` as a decimal ratio (e.g., 0.333), which is not how builders think or talk.
  - There is no way to specify roof style (gable vs shed).
  - For gable roofs, there is no way to specify ridge location (centered vs offset), which is critical for panel length/layout and proper material takeoff.

- **Change requested:**

  1. **Roof pitch input (builder-friendly)**
     - Replace the current numeric `roof_pitch` entry with a **text field** that accepts common formats:
       - `"4/12"`, `"3/12"`, `"2/12"` (rise/run)
       - `"4"` or `"3"` (assume `X/12` if no `/` is given)
       - Decimal ratios like `"0.333"` should still be accepted.
     - Parse this into the internal `roof_pitch_ratio` float used by the calculator:
       - If input contains `/`, parse `rise/run` and compute `rise / run`.
       - If input is a whole number, treat as `rise_per_12` → `rise / 12.0`.
       - If input is a float between 0 and 2, treat as a ratio directly.
     - Add clear label/placeholder text in the GUI, e.g.:
       - Label: `Roof Pitch`
       - Placeholder / helper: `e.g. 4/12 or 3/12`

  2. **Roof style selector**
     - Add a dropdown/select in the GUI for `roof_style` with at least:
       - `gable` (default)
       - `shed`
     - This value should be passed into the appropriate input dataclass (`MaterialInputs` or `GeometryInputs`, whichever is more appropriate) as a new field, e.g. `roof_style: str`.

  3. **Ridge position for gable roofs**
     - For `roof_style == "gable"`, add a numeric input:
       - Label: `Ridge position from left eave (ft)`
       - Behavior:
         - Default value should be **length / 2** (centered ridge).
         - User can override with any value from `0` to `length`.
       - This should be stored on the inputs as something like:
         - `ridge_position_ft_from_left: float`
     - For `roof_style == "shed"`, this field should be:
       - Disabled/greyed out in the GUI OR ignored by the calculator.
     - In a future step, geometry/assemblies will use `roof_style` + `ridge_position_ft_from_left` to control panel lengths and counts; for now, just make sure the values are captured and passed through the models cleanly.

- **Implementation notes:**
  - Update `apps/gui.py`:
    - Replace the existing roof pitch entry with a string-based pitch entry and a parsing helper function.
    - Add a `roof_style` dropdown with default `"gable"`.
    - Add a `ridge_position_ft_from_left` entry, defaulting dynamically to `length / 2` when length changes (at minimum, set it after initial defaults).
    - Wire these into the correct dataclasses when constructing `GeometryInputs` / `MaterialInputs` / `PoleBarnInputs`.
  - Update the relevant input model(s) in `systems/pole_barn/model.py` to include new fields:
    - `roof_style: str = "gable"`
    - `ridge_position_ft_from_left: float | None = None` (or similar default)
  - Add basic validation in the GUI:
    - If ridge position is provided, ensure it's between `0` and `length`.
    - Show a friendly error dialog if parsing the pitch fails.

- **Acceptance criteria:**
  1. In the GUI, I can enter `4/12`, `3/12`, `4`, or `0.333` for roof pitch and the calculator runs without error.
  2. `roof_style` appears as a dropdown with `gable` and `shed`; default is `gable`.
  3. When `roof_style = gable`, the ridge position field is enabled and saved into the inputs; when `roof_style = shed`, the field is disabled or ignored.
  4. Debug/logging or a temporary print shows that `roof_pitch_ratio`, `roof_style`, and `ridge_position_ft_from_left` are being passed into the calculator correctly.
  5. Existing calculations still work when I use the default values (no regression).

---

### [2] CSV Schema Mismatch: Missing `part_name` column in parts.example.csv

**STATUS: ✅ COMPLETE** (Fixed in Path B)

- **Area:** Config / CSV / Pricing

- **Problem:**
  When running the GUI, the app throws:
  > **Missing required column: `part_name` in parts.example.csv**

  This indicates that the current `parts.example.csv` schema in `/config/parts.example.csv` does **not** match what `pricing.py` expects. Modern schema requires:
  ```
  part_id, part_name, description, category, unit, vendor, source, notes
  ```
  But the file is missing **`part_name`**.

- **Severity:** Critical (calculator cannot load pricing)

- **Fix Required:**
  1. Add a `part_name` column to the CSV
  2. Populate `part_name` for each part (likely identical to description or simplified name).
  3. Ensure the header row exactly matches what the loader expects.

---

### [3] Standing Rule: CSV Schema Consistency Requirement

**STATUS: ✅ COMPLETE** (Documented in APP_WORKFLOW_GUIDE.md)

- **Area:** Workflow / Code Quality

- **Problem:**
  CSV schema mismatches (like entry [2]) are a recurring class of problems that can break the app at runtime. We need a standing rule to prevent this.

- **Change requested:**
  Add a standing instruction to Cursor (or any developer) to:
  1. Before implementing changes, scan all CSV loaders for required column names.
  2. Check all CSV files under `config/` for schema consistency.
  3. Fix any mismatches BEFORE writing code changes.

- **Implementation:**
  - Documented in `APP_WORKFLOW_GUIDE.md` as a standing rule.
  - Should be referenced before any code changes that touch CSV schemas.

---

### [4] Peak height should be derived, and labor/material costs must be separate

**STATUS: ✅ COMPLETE** (Fixed in Path B)

- **Area:** GUI / Inputs / Pricing / Geometry

- **Problem:**
  1. The GUI currently asks for **Peak Height (ft)** as an input. For a normal barn, peak height is a **dependent value** that can be derived from eave height, building width, roof pitch, and (for gable roofs) ridge position. Having it as an editable field invites bad/contradictory inputs.
  2. The GUI currently has a **Labor Rate ($/hr)** input. In practice, labor and material should be handled separately and consistently:
     - Labor rate is a company/config-level setting, not something we want changed per job on the front end.
     - Labor and material costs should be clearly separated in the results.
     - Markup should **not** blur the line between labor and material.

- **Change requested:**
  1. **Peak height: derived, not entered**
     - Remove the editable `Peak Height (ft)` input from the GUI.
     - Instead, show peak height as a **read-only derived value** in the results (and optionally in a non-editable field in the input panel).
     - Compute peak height based on:
       - `eave_height_ft`
       - `width_ft` (or the relevant span for the roof style)
       - `roof_pitch_ratio`
       - `roof_style` and `ridge_position_ft_from_left` (once implemented from Change [1])
     - For now (until more advanced roof logic is implemented), use:
       - For `roof_style == "gable"` with centered ridge:
         - `rise = (width_ft / 2.0) * roof_pitch_ratio`
         - `peak_height_ft = eave_height_ft + rise`
       - For other cases, we can approximate using the same logic or simply not show peak height until we formalize it; the important part is that the user **does not type** the peak height.
     - Ensure the internal models (e.g. `GeometryInputs` and `GeometryModel`) do not require peak height to be manually provided where it can be derived.

  2. **Labor rate removed from form; pricing separation clarified**
     - Remove `Labor Rate ($/hr)` from the GUI inputs.
     - Set labor rate as a configuration value instead:
       - Either a constant default in `PricingInputs` or loaded from a config file (e.g. a new `config/settings.example.csv`), but **not** user-editable from the main form.
     - Make sure the pricing logic keeps **labor and material costs fully separate**:
       - Material subtotal
       - Labor subtotal
       - Markup total
       - Tax total
       - Soft costs (delivery, permit, site prep)
     - Update the markup behavior so that:
       - **Material markup applies only to material costs**, not labor.
       - i.e. `markup = material_subtotal * (material_markup_factor - 1.0)`
     - Labor should be shown as its own bucket without additional markup baked into it.
     - The results pane should clearly show these categories on separate lines so it's obvious what is material vs labor vs markup.

- **Implementation notes:**
  - Update `apps/gui.py`:
    - Remove the peak height input field and the labor rate input field.
    - Ensure `GeometryInputs` is constructed without needing user-entered peak height.
    - Pass a fixed or config-derived labor rate into `PricingInputs` instead of reading it from the form.
    - Add a derived peak height display in the results block (e.g. as part of the geometry summary).
  - Update models and pricing:
    - If any model currently stores peak height as an input-only field, convert to derived where appropriate.
    - Adjust pricing logic (likely in `pricing.py` or `calculator.py`) so that markup is applied only to material subtotal, not (material + labor).
    - Optionally introduce a simple config source for labor rate so it can still be tuned without rebuilding the app.

- **Acceptance criteria:**
  1. The GUI no longer has an editable `Peak Height` field; peak height is shown only as a derived value.
  2. The GUI no longer asks for `Labor Rate ($/hr)`; the calculator still runs using a default/configured labor rate.
  3. The results clearly show:
     - Material subtotal
     - Labor subtotal
     - Markup total
     - Tax total
     - Grand total
  4. Markup is applied only to the material subtotal (not labor), and this is reflected correctly in the numbers.
  5. Existing tests pass or are updated to match the new pricing behavior.

---

### [5] Girt type selector (standard vs commercial)

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Assemblies

- **Problem:**
  Girt systems vary significantly between standard residential pole barns and commercial/post-frame buildings. The GUI assumes only one type, but quantity logic and cost change drastically depending on the framing system.

- **Change requested:**
  Add a dropdown to the GUI:
  - Label: "Girt Type"
  - Options:
    - `standard` (default)
    - `commercial` (bookshelf/blocking style)
  - Pass this into `MaterialInputs` or `AssemblyInputs` as a new field `girt_type: str`.
  - The assemblies layer will eventually use `girt_type` to select different quantity rules.

- **Acceptance criteria:**
  - GUI shows a new selector for girt type.
  - Default = `standard`.
  - Value is passed correctly into `PoleBarnInputs`.
  - Existing calculations remain unchanged until assembly logic is updated in a future entry.

---

### [6] Wall sheathing toggle (None / OSB / Plywood)

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Assemblies

- **Problem:**
  Currently the app assumes metal-only exterior walls. Many buildings require wall sheathing—OSB or plywood—before metal or instead of metal. This dramatically affects material takeoff.

- **Change requested:**
  Add a dropdown to the GUI:
  - Label: "Wall Sheathing"
  - Options:
    - `none` (default)
    - `osb`
    - `plywood`
  Add field to `MaterialInputs`: `wall_sheathing_type: str`.

- **Acceptance criteria:**
  - GUI includes new wall sheathing selector.
  - Value stored in inputs.
  - Does not yet change quantities until a future assembly update.

---

### [7] Roof sheathing toggle (None / OSB / Plywood)

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Assemblies

- **Problem:**
  Roof sheathing (OSB or plywood) is common for some builds and required for shingle systems. Current GUI cannot capture this.

- **Change requested:**
  Add a dropdown:
  - Label: "Roof Sheathing"
  - Options: `none`, `osb`, `plywood`
  Add field to `MaterialInputs`: `roof_sheathing_type: str`.

- **Acceptance criteria:**
  - GUI displays the selector.
  - Default is `none`.
  - Value is present in `PoleBarnInputs`.

---

### [8] Floor type selector (Slab / Gravel / None)

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Pricing / Assemblies

- **Problem:**
  The current form does not capture floor type. A concrete slab, gravel pad, or no floor at all changes quantities, pricing, and even some structural assumptions.

- **Change requested:**
  Add a dropdown:
  - Label: "Floor Type"
  - Options:
    - `slab`
    - `gravel`
    - `none`
  Add new field: `floor_type: str`.

- **Acceptance criteria:**
  - Selector appears in GUI.
  - Default = `none`.
  - Passed cleanly into the inputs.
  - Does not modify quantities yet (future entry).

---

### [9] Door count input (integer)

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Geometry

- **Problem:**
  GUI defaults doors or ignores door count. Need ability to specify number of doors (later sizes per door).

- **Change requested:**
  Add integer input:
  - Label: "Number of Doors"
  - Default: 0
  - Field wired into `GeometryInputs.door_count`.

- **Acceptance criteria:**
  - Input is present, validates as integer.
  - Default is 0.
  - Value passed correctly.

---

### [10] Window count input (integer)

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Geometry

- **Problem:**
  Window counts currently hard-coded or ignored in GUI.

- **Change requested:**
  Add integer input:
  - Label: "Number of Windows"
  - Default: 0
  - Field wired into `GeometryInputs.window_count`.

- **Acceptance criteria:**
  - Input appears and validates.
  - Default is 0.
  - Passed correctly into geometry.

---

### [11] Permit & Snow Load inputs

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Project Metadata / Structural

- **Problem:**
  The engineer form includes permit and snow load information that affects structural design and code compliance. Current GUI does not capture this.

- **Change requested:**
  Add inputs for:
  - Building type: `residential` / `commercial` (dropdown)
  - Building use/description (text field)
  - Permitting agency (text field)
  - Required snow load (psf) (numeric)
  - Requested snow load (psf) (numeric, optional)
  - Checkbox: "Snow load unknown / needs lookup"

- **Acceptance criteria:**
  - All fields appear in GUI.
  - Values stored in `PoleBarnInputs` or appropriate model.
  - For now, informational only (not yet used in calculations).

---

### [12] Build type and construction type selectors

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Project

- **Problem:**
  The engineer form distinguishes between:
  - New construction vs addition
  - Pole frame vs stick frame
  These affect design assumptions and potentially quantities.

- **Change requested:**
  Add dropdowns:
  - "Build Type": `pole` (default) / `stick_frame`
  - "Construction Type": `new` (default) / `addition`
  Add fields to `PoleBarnInputs` or appropriate model.

- **Acceptance criteria:**
  - Both selectors appear in GUI.
  - Defaults are `pole` and `new`.
  - Values stored correctly.

---

### [13] Slab details (thickness and reinforcement)

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Foundation

- **Problem:**
  When floor type is "slab", we need additional details for accurate material takeoff and pricing.

- **Change requested:**
  Add inputs (shown only when floor_type == "slab"):
  - Slab thickness (inches) - numeric
  - Slab reinforcement - dropdown: `none`, `mesh`, `rebar`
  Add fields to `MaterialInputs`: `slab_thickness_in`, `slab_reinforcement`.

- **Acceptance criteria:**
  - Fields appear when slab is selected.
  - Defaults: 4" thickness, `none` reinforcement.
  - Values stored correctly.

---

### [14] Door & window assemblies must include framing lumber and trim

- **Area:** Assemblies / Quantities / GUI Inputs

- **Problem:**
  Current door and window handling only counts openings; it does not account for:
  - Extra framing around openings (king studs, trimmers/jacks, headers, sill plates, blocking).
  - Exterior trim around doors and windows.
  This underestimates both lumber and trim. We already have good trim logic in the trim calculator that we should eventually reuse.

- **Change requested:**
  1. Treat each door and window opening as an assembly that includes:
     - Additional studs and headers per opening, based on opening size and wall height.
     - Exterior trim LF.
     - Exterior trim LF.
  2. In the short term:
     - Add hooks in the assemblies layer so that for each door/window opening, we can:
       - Compute an "extra framing LF/BF" quantity.
       - Compute a "door/window trim LF" quantity.
       - Map these to distinct assembly names (e.g. `door_framing`, `window_framing`, `door_trim`, `window_trim`) so they can be priced separately.
  3. Long term:
     - Reuse or mirror the existing trim calculator logic where practical for trim LF around openings.

- **Implementation notes:**
  - Do not change the GUI right now (we'll later add more detailed door/window sizing); rely on existing `door_count` and `window_count` as the drivers.
  - Add new assembly calculation functions that:
     - Use `door_count`, `window_count`, and wall height to approximate extra studs/headers.
     - Produce trim LF per opening, even if initially based on a standard size assumption.
     - Wire these new assemblies into `assemblies.example.csv` and `parts/pricing` so they show up as separate line items.

- **Acceptance criteria:**
  1. Material takeoff includes distinct quantities for:
     - Door framing lumber
     - Window framing lumber
     - Door trim
     - Window trim
  2. Priced output shows these as separate line items.
  3. Total lumber and trim costs increase when door/window counts increase, even before we implement detailed opening sizes.

---

### [15] Exterior finish selector (metal gauge, lap siding, stucco)

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Assemblies

- **Problem:**
  The app currently assumes a single exterior finish (29ga metal). In practice, exterior finish may be:
  - 29ga metal (default)
  - 26ga metal
  - Lap siding
  - Stucco (with appropriate sheathing/backing)
  These choices significantly change the assemblies and pricing.

- **Change requested:**
  - Add a dropdown to the GUI:
    - Label: "Exterior Finish"
    - Options (strings):
      - `metal_29ga` (default)
      - `metal_26ga`
      - `lap_siding`
      - `stucco`
  - Add a field to `MaterialInputs`: `exterior_finish_type: str = "metal_29ga"`.
  - In the assemblies layer, route wall-skin quantities through this flag, even if initially only used to:
    - Switch between 29ga vs 26ga metal parts.
    - Leave lap/stucco as future TODOs with placeholder assemblies.

- **Acceptance criteria:**
  1. GUI displays an "Exterior Finish" dropdown with the four options.
  2. `exterior_finish_type` flows correctly into `PoleBarnInputs`.
  3. Wall skin assembly selection can branch on this flag without breaking existing metal-29 behavior.

---

### [16] Insulation type selector for walls and roof (batts, rock wool, rigid, spray foam)

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Assemblies / Pricing

- **Problem:**
  Current insulation handling is too generic. In practice:
  - Walls and roof are often insulated differently.
  - Common types include: standard fiberglass batts, rock wool, rigid board, and spray foam. Each has very different cost and assembly patterns.

- **Change requested:**
  1. In the GUI, add two selectors:
     - "Wall Insulation Type": `none`, `fiberglass_batts`, `rock_wool`, `rigid_board`, `spray_foam`
     - "Roof Insulation Type": `none`, `fiberglass_batts`, `rock_wool`, `rigid_board`, `spray_foam`
  2. Add fields to `MaterialInputs`:
     - `wall_insulation_type: str = "none"`
     - `roof_insulation_type: str = "none"`
  3. Assemblies layer:
     - Use these fields to create separate insulation assemblies for walls vs roof, even if initial logic is simple (e.g. SF × type).
     - Map to appropriate parts in `parts/pricing/assemblies` so each type is priced differently.

- **Acceptance criteria:**
  1. GUI exposes separate insulation choices for walls and roof.
  2. Setting wall/roof insulation to something other than `none` produces visible insulation line items with distinct costs for each type.
  3. Turning insulation off (`none`) zeroes those quantities and costs cleanly.

---

### [17] Roll-up / overhead door type selector

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Assemblies / Pricing

- **Problem:**
  Door counts are tracked but door TYPE is not. Roll-up/overhead doors have very different cost and sometimes framing/trim assumptions vs swing or slider doors.

- **Change requested:**
  - Add a selector for primary large doors:
    - Label: "Overhead / Roll-up Doors"
    - Fields:
      - `overhead_door_count` (integer, default 0)
      - `overhead_door_type` dropdown (e.g. `steel_rollup`, `sectional`, `none`)
  - For now we can treat all overhead doors as a single size category or apply a standard cost per door.
  - Assemblies:
    - Introduce an `overhead_door` assembly driven by `overhead_door_count`.
    - Map to appropriate parts in the pricing CSVs.

- **Acceptance criteria:**
  1. GUI allows specifying how many roll-up/overhead doors there are.
  2. Material takeoff includes an overhead-door assembly quantity based on that count.
  3. Priced output shows a distinct "Overhead / Roll-up Door" line item.

---

### [18] MEP (Mechanical, Electrical, Plumbing) allowance toggles

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Pricing / Scope definition

- **Problem:**
  The current calculator completely ignores MEP. In reality:
  - Basic electrical and lighting are often code-required.
  - Plumbing and mechanical systems (heaters, bathroom groups, welders, etc.) can heavily affect scope and pricing. Even if we don't fully engineer MEP, we need at least:
    - Scope flags showing what's included.
    - Allowance-level pricing buckets for MEP.

- **Change requested:**
  1. Add simple scope toggles in the GUI:
     - Electrical:
       - Checkbox: "Include basic electrical" (lights / outlets per code)
       - Optional numeric: "Electrical allowance ($)" (default 0 or a configurable standard)
     - Plumbing:
       - Checkbox: "Include plumbing"
       - Optional numeric: "Plumbing allowance ($)"
     - Mechanical:
       - Checkbox: "Include mechanical (heat/vent)"
       - Optional numeric: "Mechanical allowance ($)"
  2. Add fields to `PricingInputs`:
     - `include_electrical: bool`
     - `electrical_allowance: float`
     - `include_plumbing: bool`
     - `plumbing_allowance: float`
     - `include_mechanical: bool`
     - `mechanical_allowance: float`
  3. Pricing:
     - Treat these as **allowance buckets** added on top of building shell costs.
     - Show them as separate line items in the priced summary (e.g., "Electrical allowance", etc.).

- **Acceptance criteria:**
  1. GUI clearly shows on/off toggles for Electrical, Plumbing, Mechanical, each with an associated allowance field.
  2. When a toggle is on and the allowance is > 0, a corresponding line item appears in the priced output.
  3. Turning a toggle off or setting allowance to 0 removes that cost.
  4. MEP allowances are included in the grand total but remain visually distinct so they're easy to adjust during budgeting.

---

### [19] Post type selector (PT solid vs laminated)

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Assemblies

- **Problem:**
  The engineer form specifies post type (PT Hem-Fir solid vs laminated). This affects:
  - Material cost
  - Structural capacity
  - Availability and lead times

- **Change requested:**
  Add a dropdown to the GUI:
  - Label: "Post Type"
  - Options:
    - `pt_solid` (default) - Pressure-treated solid posts
    - `laminated` - Laminated posts
  - Add field to `AssemblyInputs`: `post_type: str = "pt_solid"`

- **Implementation notes:**
  - Store value in input models
  - For now, informational only
  - Future: Use to select different part IDs and pricing for solid vs laminated posts

- **Acceptance criteria:**
  1. GUI displays post type selector
  2. Default is `pt_solid`
  3. Value stored in `AssemblyInputs`
  4. Value passed through to calculator
  5. No breaking changes to existing calculations

---

### [20] Truss/post connection type selector

**STATUS: ✅ COMPLETE** (UI implementation complete)

- **Area:** GUI / Inputs / Assemblies

- **Problem:**
  The engineer form specifies truss/post connection type (notched vs cleated). This affects:
  - Fastener quantities
  - Labor hours
  - Additional framing lumber (for cleated connections)
  - Structural behavior

- **Change requested:**
  Add a dropdown to the GUI:
  - Label: "Truss/Post Connection"
  - Options:
    - `notched` (default) - Trusses sit in notches cut into posts
    - `cleated` - Trusses attached with metal cleats/brackets
  - Add field to `AssemblyInputs`: `post_truss_connection_type: str = "notched"`

- **Implementation notes:**
  - Store value in input models
  - For now, informational only
  - Future: Use to adjust fastener quantities and labor hours in assemblies
  - Future: Cleated connections may require additional lumber for blocking

- **Acceptance criteria:**
  1. GUI displays connection type selector
  2. Default is `notched`
  3. Value stored in `AssemblyInputs`
  4. Value passed through to calculator
  5. No breaking changes to existing calculations

---

### [21] Multiple door sizes and types (future enhancement)

- **Area:** GUI / Inputs / Geometry / Assemblies

- **Problem:**
  Current implementation only tracks door count. The engineer form supports:
  - Multiple door sizes (width × height)
  - Multiple door types (overhead, walk, barn, slider)
  - Different quantities per size/type
  This is needed for accurate framing and trim calculations.

- **Change requested:**
  **Note:** This is a future enhancement, not for immediate implementation. Log for Phase 2.
  
  Add support for multiple door entries:
  - Table/list interface in GUI with rows for each door
  - Each row: door type, width, height, quantity
  - Door types: `overhead`, `walk`, `barn`, `slider`
  - Update `GeometryInputs` to support list of door specifications instead of single count

- **Implementation notes:**
  - Defer to Phase 2 after core functionality is stable
  - Will require refactoring door/window handling in assemblies
  - Will enable more accurate framing and trim calculations per opening size

- **Acceptance criteria:**
  - Documented for future implementation
  - No immediate changes required

---

### [22] Lean-to / shed module support (future enhancement)

- **Area:** GUI / Inputs / Geometry / Assemblies

- **Problem:**
  The engineer form allows separate lean-to/shed geometry with:
  - Separate dimensions (length, width)
  - Different bay spacing
  - Different pitch
  - Enclosed toggle
  - Separate slab, sheathing, insulation options
  This is a complex feature that requires separate geometry calculations.

- **Change requested:**
  **Note:** This is a Phase 2 feature, not for immediate implementation.
  
  Add support for optional lean-to/shed:
  - Toggle: "Include lean-to / shed"
  - When enabled, show additional input section:
    - Lean-to dimensions (length, width)
    - Bay spacing
    - Roof pitch
    - Enclosed yes/no
    - Slab yes/no
    - Sheathing options
    - Insulation options
  - Calculate lean-to quantities separately and add to main building totals

- **Implementation notes:**
  - Defer to Phase 2
  - Will require separate geometry model for lean-to
  - Will need to merge quantities from main building + lean-to
  - Complex feature - best implemented after core is stable

- **Acceptance criteria:**
  - Documented for future implementation
  - No immediate changes required

---

### [23] Exterior man door sizing assumptions & options

- **Area:** Assemblies / Doors / Future GUI enhancement

- **Problem:**

  Right now, all "man doors" are treated as generic openings. For assemblies and framing/trim, we need:

  - A clear default assumed size for "standard" man doors.

  - A set of *allowed* exterior door sizes so framing/trim can be accurately calculated when we later support per-door sizing.

- **Change requested:**

  1. **Assumed default size (for current logic):**

     - All man doors are assumed to be **3/0 x 6/8** (36" wide x 80" tall) unless a more detailed door-sizing UI is implemented.

  2. **Allowed exterior door sizes (for future use):**

     - Heights allowed: **6/8, 7/0, 8/0**

     - Widths allowed: **2/10, 3/0, 5/0, 6/0**

  3. Document this in:

     - `ASSEMBLIES_DESIGN.md` (door assemblies section)

     - A comment in the door assembly logic noting that current framing/trim math assumes 3/0 x 6/8 for now.

- **Acceptance criteria:**

  1. Door assemblies clearly document that all man doors are treated as 3/0 x 6/8 for the moment.

  2. The allowed size list is captured in design docs for future UI/logic expansion (multiple door sizes).

---

### [24] Interior build-out framing (bathroom, office, mezzanine)

- **Area:** GUI / Assemblies / Interior framing

- **Problem:**

  The current estimator only covers the shell. Real projects often include interior framing for:

  - Bathrooms

  - Offices

  - Mezzanines / lofts

  These add studs, plates, sheathing, and sometimes floor framing that should be represented as assemblies.

- **Change requested:**

  1. Add an **"Interior Build-Out"** section in the GUI with:

     - Checkbox: "Include bathroom framing" + integer "Number of bathrooms"

     - Checkbox: "Include office framing" + numeric "Office area (sq ft)"

     - Checkbox: "Include mezzanine/loft" + numeric "Mezzanine area (sq ft)"

  2. In `ASSEMBLIES_DESIGN.md`, define simple rules of thumb for:

     - Bathroom framing LF/BF per bathroom (e.g., wall LF per bathroom based on a standard footprint).

     - Office framing based on office area (e.g., wall LF per sq ft).

     - Mezzanine framing: joists + beams + posts per sq ft or per bay.

  3. Add new interior framing assemblies:

     - `bathroom_framing`

     - `office_framing`

     - `mezzanine_framing`

     mapped to parts and pricing (even if initial numbers are rough).

- **Acceptance criteria:**

  1. GUI exposes the interior build-out questions.

  2. Material takeoff includes separate line items for interior framing when enabled.

  3. Assumptions for LF/BF per bathroom/office/sq ft are documented in `ASSEMBLIES_DESIGN.md`.

---

### [25] Roof pitch input simplification (integer → X/12)

- **Area:** GUI / CLI / Geometry

- **Problem:**

  The current UI accepts a flexible roof pitch string (`4/12`, `0.333`, etc.), but in real use the user is only going to enter the "X" in "X/12" (e.g., 2, 3, 4). Allowing arbitrary formats complicates the UI and error handling.

- **Change requested:**

  1. **GUI:**

     - Replace the free-form pitch field with an **integer-only input** or dropdown for `Roof Pitch (X in X/12)`.

     - Valid values (for now): **1–12**.

     - Internal numeric ratio = `pitch_integer / 12.0`.

  2. **CLI:**

     - Keep the flexible parser for backward compatibility (accepts `4/12`, `0.333`, `4`).

     - But document that the **recommended** CLI usage is to pass simple integers representing X for X/12.

  3. **Validation:**

     - Reject 0 or negative pitches in GUI.

     - Show a friendly error if the pitch is outside 1–12.

- **Acceptance criteria:**

  1. GUI only allows roof pitch as an integer X representing X/12.

  2. Internally, the derived numeric ratio is used consistently in geometry.

  3. CLI continues to work for existing patterns but encourages integer X.

---

### [26] MEP allowances scaled from building size & door count

- **Area:** Pricing / MEP / Defaults

- **Problem:**

  Current MEP allowances are flat numbers the user types in. A better estimator starts with **reasonable default allowances** based on building size and basic features, then allows user override.

- **Change requested:**

  1. Define simple default formulas for allowances based on:

     - Building footprint (length × width)

     - Number of exterior man doors

     - Possibly number of overhead doors

  2. Examples (to be refined and documented in `ASSEMBLIES_DESIGN.md` or a new `MEP_DEFAULTS.md`):

     - Electrical:

       - Base outlets/lighting per X sq ft + one exterior light per man door.

       - Convert that to a rough dollar allowance using assumed fixture and labor costs.

     - Plumbing:

       - Base allowance per bathroom count.

     - Mechanical:

       - Base allowance per sq ft and climate assumption.

  3. Implementation behavior:

     - If the user **leaves MEP allowance fields blank or zero**, compute defaults from size & door counts.

     - If the user enters a non-zero allowance, treat that as an override.

  4. (Optional future) Provide a breakdown in the summary: "Based on size, we assumed N outlets, M lights, L ft of wire", even if pricing is still through a single allowance bucket.

- **Acceptance criteria:**

  1. For a blank MEP allowance, the estimator produces non-zero MEP allowances derived from building size/door count.

  2. User-entered allowances override the defaults.

  3. Default formulas and assumptions are documented.

---

### [27] Convert areas (sq ft) to real purchasable parts (panels & sheets)

- **Area:** Assemblies / Parts / Config

- **Problem:**

  The material list currently uses square footage for roof panels, wall panels, and sheathing. In practice, material is ordered in:

  - Metal panels with a fixed coverage width (e.g., 36" coverage).

  - Sheathing sheets (e.g., 4x8, 4x10).

  Estimator users need counts of actual pieces, not just sq ft.

- **Change requested:**

  1. Introduce **coverage dimensions** for panel and sheet products in config:

     - For each relevant `part_id` in `parts/pricing` (metal panels, OSB, plywood), add fields for:

       - `coverage_width_in` and `coverage_height_in` OR a normalized "coverage area per piece" and "orientation rule".

     - If schema change is too disruptive, document the assumed coverage sizes in `ASSEMBLIES_DESIGN.md` and hard-code them in the assemblies logic initially.

  2. Update assemblies logic so that for:

     - Wall metal:

       - Compute number of vertical sheets per wall: `ceil(wall_length_ft * 12 / coverage_width_in)`.

       - Panel length per sheet derived from wall height (plus overhang/trim assumptions).

     - Roof metal:

       - Compute number of sheets per slope based on horizontal run and coverage width.

     - Sheathing (walls/roof):

       - Convert required sq ft into counts of 4x8 (or other) sheets: `ceil(area_sqft / sheet_coverage_sqft)`.

  3. Maintain sq ft in the summary for reference, but make **the priced quantity be the count of pieces (EA)**.

- **Acceptance criteria:**

  1. Material takeoff includes:

     - "Metal roof panels" as a count of panels (EA), not just sq ft.

     - "Metal wall panels" as a count of panels (EA).

     - Sheathing as "X sheets" of OSB/plywood.

  2. Pricing is based on the piece counts.

  3. Basic coverage assumptions (e.g., 36" metal, 4x8 sheets) are documented in design docs and/or config.

---

### [28] Material list export system (Excel with category tabs)

- **Area:** Export / Material List / Output

- **Problem:**

  The current estimator shows material quantities in the UI, but there is no way to export a **shopping list** that can be edited and sent to suppliers. The material list needs to be:

  - A separate, editable file (not just on-screen display)

  - Organized by category (Framing, Doors_Windows, Metal, Insulation, Concrete, MEP, Misc)

  - Human-readable and vendor-ready

  - Editable by the user before sending to suppliers

- **Change requested:**

  1. **Export format:**

     - Primary export: Excel file (`material_list.xlsx`)

     - Inside workbook, create separate tabs:

       - `Framing` (posts, studs, beams, plates, girts, purlins)

       - `Doors_Windows` (man doors, overhead doors, windows, trim)

       - `Metal` (roof panels, wall panels, trim, fasteners)

       - `Insulation` (batts, rigid, spray foam, etc.)

       - `Concrete` (concrete, rebar, mesh)

       - `MEP` (electrical, plumbing, mechanical allowances/parts)

       - `Misc` (anything else)

  2. **Column schema per row:**

     - `category` (Framing / Metal / Insulation / etc.)

     - `sub_category` (e.g., "wall girts", "roof purlins", "door trim")

     - `part_id` (matches `parts.example.csv`)

     - `part_name` (short human name)

     - `description` (longer vendor-readable description)

     - `unit` (LF, EA, SQFT, SHEET, etc.)

     - `qty` (count/length required)

     - `unit_price` (from pricing library)

     - `ext_price` (qty × unit_price)

     - `vendor` (optional default from parts.csv)

     - `notes` (color, gauge, location, size assumptions, etc.)

  3. **Export functionality:**

     - Add "Export Material List" button to GUI

     - Generate Excel file with all tabs populated

     - File should be saved to a user-specified location (or default to project directory)

     - File should be named with project name/timestamp if available

- **Acceptance criteria:**

  1. Clicking "Export Material List" generates a valid Excel file.

  2. Excel file contains all expected category tabs.

  3. Each tab contains only parts from that category.

  4. All columns are populated correctly.

  5. File can be opened and edited in Excel.

  6. All `part_id`s in the export match entries in `parts.example.csv`.

---

### [29] Category mapping column in parts.csv

- **Area:** Config / Parts / Export

- **Problem:**

  To organize the material list export into category tabs, we need to know which category each part belongs to. Currently, parts have a `category` field, but it may not align with the export categories we want (Framing, Doors_Windows, Metal, etc.).

- **Change requested:**

  1. Add a new column to `parts.example.csv`:

     - Column name: `export_category`

     - Values: `Framing`, `Doors_Windows`, `Metal`, `Insulation`, `Concrete`, `MEP`, `Misc`

  2. **Mapping rules:**

     - Posts, studs, beams, plates, girts, purlins → `Framing`

     - Man doors, overhead doors, windows, door/window trim → `Doors_Windows`

     - Roof panels, wall panels, metal trim, fasteners → `Metal`

     - Batts, rigid board, spray foam → `Insulation`

     - Concrete, rebar, mesh → `Concrete`

     - Electrical allowance, plumbing allowance, mechanical allowance, panels, fixtures → `MEP`

     - Anything else → `Misc`

  3. Populate `export_category` for all existing parts in `parts.example.csv`.

  4. Update the material list export logic to use `export_category` from parts.csv to determine which tab each part goes into.

- **Acceptance criteria:**

  1. `parts.example.csv` has an `export_category` column.

  2. All existing parts have a valid `export_category` value.

  3. Material list export uses `export_category` to organize parts into tabs.

  4. No parts are missing from the export due to missing category.

---

### [30] Material export must use pricing library only (no loose prices)

- **Area:** Export / Pricing / Data integrity

- **Problem:**

  To maintain data integrity and ensure the material list is always accurate, all prices must come from the same source (the pricing library). We cannot allow ad-hoc prices or hard-coded values that don't match the parts/pricing CSVs.

- **Change requested:**

  1. **Enforcement rule:**

     - Every row in the material list export MUST have a valid `part_id` that exists in `parts.example.csv`.

     - Every `unit_price` MUST come from `pricing.example.csv` (looked up by `part_id` and pricing profile).

     - No hard-coded prices or "mystery items" are allowed in the export.

  2. **Validation:**

     - Before generating the export, validate that:

       - All `part_id`s in the takeoff exist in `parts.example.csv`.

       - All `part_id`s have a corresponding price in `pricing.example.csv` for the active pricing profile.

     - If validation fails:

       - Log a warning with the missing `part_id`s.

       - Still generate the export, but mark missing prices as `0.00` or `TBD` with a note.

  3. **Code structure:**

     - The material list export function should:

       - Take `PricedLineItem[]` as input (which already has `part_id` and `unit_price` from the pricing library).

       - Map each item to the export schema.

       - Never inject prices from anywhere other than the `PricedLineItem` data.

  4. **Documentation:**

     - Add a comment/rule in the export code:

       > "Material list export is generated exclusively from the same `part_id`s and `unit_price`s defined in `parts.example.csv` and `pricing.example.csv`. No ad-hoc prices allowed."

- **Acceptance criteria:**

  1. Material list export contains only `part_id`s that exist in `parts.example.csv`.

  2. All `unit_price` values in the export match values from `pricing.example.csv`.

  3. If a part is missing from pricing, it appears in the export with `unit_price = 0.00` and a note indicating it needs pricing.

  4. No hard-coded prices appear in the export code.

---

### [31] Panel and sheet coverage assumptions (baseline standards)

- **Area:** Assemblies / Config / Material calculations

- **Problem:**

  To convert area-based quantities (sq ft) into purchasable parts (panels, sheets), we need standard coverage assumptions. Without these, we can't generate accurate piece counts for ordering.

- **Change requested:**

  1. **Standard coverage assumptions (hard-coded or config):**

     - **Metal wall panels (29ga and 26ga):**

       - Coverage width: **36 inches** (standard)

       - Orientation: Vertical (panels run vertically up the wall)

       - Note: Some panels are 16", 24", or other widths, but 36" is the baseline assumption.

     - **Metal roof panels:**

       - Coverage width: **36 inches** (standard)

       - Orientation: Horizontal (panels run horizontally along the roof slope)

     - **OSB / Plywood sheathing:**

       - Sheet size: **4x8 feet** (48" × 96" = 32 sq ft per sheet)

       - Alternative sizes (4x10, etc.) can be added later, but 4x8 is the baseline.

  2. **Documentation:**

     - Document these assumptions in `ASSEMBLIES_DESIGN.md`:

       - "Standard metal panels = 36" coverage width unless otherwise specified."

       - "Standard sheathing = 4x8 sheets (32 sq ft) unless otherwise specified."

  3. **Calculation logic:**

     - Wall metal:

       - Number of vertical sheets per wall = `ceil(wall_length_ft * 12 / 36)`

       - Panel length per sheet = wall height + overhang (if applicable)

     - Roof metal:

       - Number of sheets per slope = based on horizontal run × coverage width

       - Panel length per sheet = roof slope length

     - Sheathing:

       - Number of sheets = `ceil(area_sqft / 32.0)` (for 4x8 sheets)

  4. **Future flexibility:**

     - These assumptions can later be moved to config or parts.csv if needed.

     - For now, hard-coding is acceptable to establish the baseline.

- **Acceptance criteria:**

  1. Assemblies logic uses 36" coverage for metal panels.

  2. Assemblies logic uses 4x8 (32 sq ft) for sheathing sheets.

  3. Material takeoff shows panel/sheet counts (EA), not just sq ft.

  4. Assumptions are documented in `ASSEMBLIES_DESIGN.md`.

---

### [32] UI display vs export separation (summary vs full list)

- **Area:** GUI / Display / User experience

- **Problem:**

  The current UI may show too much detail in the results pane. Clients don't need to see every stud and screw—they need high-level totals for comparison. The full material list should be a separate export, not cluttering the on-screen summary.

- **Change requested:**

  1. **UI Results Pane (on-screen summary):**

     - Show per-category totals only:

       - "Framing: $X,XXX ($X.XX/sqft)"

       - "Metal: $X,XXX ($X.XX/sqft)"

       - "Insulation: $X,XXX ($X.XX/sqft)"

       - "Concrete: $X,XXX ($X.XX/sqft)"

       - "MEP: $X,XXX ($X.XX/sqft)"

       - "Misc: $X,XXX ($X.XX/sqft)"

     - Show grand total and cost per sq ft.

     - Remove or minimize the detailed line-item list (or move it to a collapsible section).

  2. **Export Button:**

     - Add a prominent "Export Material List" button in the results pane.

     - Button generates the Excel file with full detail (per entry [28]).

     - Button label: "Download Shopping List" or "Export Material List"

  3. **Separation of concerns:**

     - UI = high-level summary for client presentation and apples-to-apples comparison.

     - Export = detailed shopping list for ordering and supplier communication.

- **Acceptance criteria:**

  1. UI results pane shows category totals with $/sqft, not individual parts.

  2. "Export Material List" button is visible and functional.

  3. Export file contains full detail (all parts, all columns).

  4. UI remains clean and focused on totals.

---

### [33] MEP default formulas based on building size and features

- **Area:** Pricing / MEP / Defaults

- **Problem:**

  Entry [26] requested MEP allowances scaled from building size, but we need to define the actual formulas and rules of thumb. Without concrete formulas, the estimator can't compute reasonable defaults.

- **Change requested:**

  1. **Define default formulas (to be documented in `MEP_DEFAULTS.md` or `ASSEMBLIES_DESIGN.md`):**

     - **Electrical:**

       - Base outlets: Assume 1 outlet per 100 sq ft of floor area (minimum 4 outlets).

       - Base lighting: Assume 1 light fixture per 200 sq ft of floor area (minimum 2 lights).

       - Exterior lights: 1 exterior light per man door.

       - Overhead door circuits: 1 circuit per overhead door (for opener).

       - Wire: Estimate based on outlet/light count and building dimensions (rough rule: 10 LF of wire per outlet/light).

       - Convert to dollar allowance: Use assumed fixture costs ($50/light, $20/outlet, $2/LF wire, $100/panel, labor at configured rate).

     - **Plumbing:**

       - Base allowance per bathroom: $2,000 per bathroom (includes rough-in, fixtures, labor).

       - If no bathrooms specified: $0 (no plumbing).

     - **Mechanical:**

       - Base allowance: $2.00 per sq ft of floor area (for basic heating/ventilation).

       - Minimum: $500.

  2. **Implementation behavior:**

     - If MEP allowance fields are blank or zero in GUI, compute defaults using these formulas.

     - If user enters a non-zero allowance, use that as an override (ignore defaults).

     - Show a breakdown in the export notes: "Based on X sqft, Y doors, Z bathrooms, we assumed..."

  3. **Documentation:**

     - Create `MEP_DEFAULTS.md` with:

       - All formulas

       - Assumed unit costs

       - Rationale/notes

       - Future refinement guidance

- **Acceptance criteria:**

  1. For a 40×30 building with 3 doors and 1 bathroom:

     - Electrical default is computed (not zero).

     - Plumbing default = $2,000.

     - Mechanical default is computed based on sq ft.

  2. User-entered allowances override defaults.

  3. Formulas are documented in `MEP_DEFAULTS.md`.

  4. Export notes include breakdown of assumptions.

---

### File: PRICING_CALIBRATION.md

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


---

### File: ASSEMBLIES_DESIGN.md

# Post-Frame Construction Assemblies Design Document

## Overview

This document defines the assemblies, parts, and quantity logic for post-frame (pole barn) construction estimation. It serves as the design reference for implementing realistic material takeoffs in the calculator.

**Scope:** This is an estimator tool, not an engineering tool. We focus on quantities and costs based on typical industry practice, not structural engineering calculations.

---

## Post-Frame Construction Basics

Post-frame construction uses vertical posts (poles) embedded in the ground or on concrete piers as the primary structural system. The frame consists of:

- **Posts** - Primary vertical load-bearing members
- **Girts** - Horizontal wall framing members attached to posts
- **Trusses** - Roof framing members spanning between posts
- **Purlins** - Horizontal roof framing members attached to trusses
- **Panels** - Exterior cladding (metal, wood, etc.)
- **Sheathing** - Optional structural sheathing (OSB, plywood)
- **Insulation** - Optional thermal insulation
- **Openings** - Doors and windows with associated framing and trim

**Sources:**
- Post-Frame Building Design Manual (National Frame Builders Association)
- IRC Section R301 (International Residential Code) - general construction practices
- Industry standard spacing practices (documented in manufacturer literature)

---

## Assembly Categories

### 1. Posts (Columns)

**Parts Involved:**
- Pressure-treated (PT) solid posts (typically 6x6 or 8x8)
- Laminated posts (engineered, typically 6x6 or larger)
- Concrete for post holes/footings

**Spacing/Usage:**
- Typical spacing: 8-12 feet on center along length
- One post per frame line on each sidewall
- Posts extend from ground (or footing) to truss connection point
- Depth in ground: typically 4-6 feet (varies by soil conditions and code)

**Material Takeoff Units:**
- Posts: **EA** (each)
- Post concrete: **CY** (cubic yards) or **EA** (per post hole)

**Standard vs Commercial:**
- Standard: PT solid posts, typically 6x6
- Commercial: May use laminated posts for larger spans or higher loads
- Commercial may have different spacing requirements

**Code References:**
- IRC R301.1 - General construction requirements
- Typical post sizing based on span and load (industry practice, not code-mandated for this estimator)

---

### 2. Girts (Wall Horizontal Framing)

**Parts Involved:**
- 2x6 or 2x8 lumber (SPF, SYP, or similar)
- Fasteners (screws or nails)
- Metal brackets (for commercial/bookshelf style)

**Spacing/Usage:**
- **Standard girts:** Horizontal members attached to outside face of posts
  - Typical spacing: 24" on center vertically
  - Run full length of wall between posts
  - One row per spacing interval from grade to eave height
  
- **Commercial/Bookshelf girts:** Horizontal members with blocking between posts
  - Similar spacing (24" o.c. typical)
  - Additional blocking lumber between posts
  - May use metal brackets for connections

**Material Takeoff Units:**
- Girt lumber: **LF** (linear feet)
- Blocking (commercial): **LF** or **BF** (board feet)
- Fasteners: **EA** (each)

**Standard vs Commercial:**
- Standard: Simple horizontal girts, minimal blocking
- Commercial: Bookshelf style with blocking between posts, may use metal brackets
- Commercial typically requires more lumber and fasteners

**Sources:**
- Typical girt spacing: 24" o.c. per industry practice (NFBA guidelines)
- Commercial bookshelf girts: Additional blocking at 24" o.c. between posts

---

### 3. Purlins (Roof Horizontal Framing)

**Parts Involved:**
- 2x6 or 2x8 lumber
- Fasteners (screws or nails)
- Metal brackets (for some connection types)

**Spacing/Usage:**
- Horizontal members attached to top of trusses
- Typical spacing: 24" on center along roof slope
- Run perpendicular to trusses, spanning building width (with overhangs)
- Number of rows = roof run / spacing (rounded up)

**Material Takeoff Units:**
- Purlin lumber: **LF** (linear feet)
- Fasteners: **EA** (each)

**Standard vs Commercial:**
- Similar spacing typically
- Commercial may use larger lumber sizes for longer spans

**Sources:**
- Typical purlin spacing: 24" o.c. per industry practice
- Roof run calculation: Based on building width, pitch, and overhangs

---

### 4. Roof and Wall Panels (Metal Cladding)

**Parts Involved:**
- Metal panels (29ga or 26ga steel)
- Panel fasteners (screws with washers)
- Ridge cap (for roof)
- Trim pieces (eave, rake, base, corner)

**Spacing/Usage:**
- Panels typically 36" wide coverage (actual panel width ~38" with overlap)
- Standard panel lengths: 8', 10', 12', 14', 16', 20', 24'
- Panels run vertically on walls, horizontally on roof
- Waste factor: 5-10% typical (cutting, end pieces, mistakes)

**Material Takeoff Units:**
- Panels: **SF** (square feet) or **EA** (panel count)
- Fasteners: **EA** (typically 1 fastener per 1-2 sq ft)
- Trim: **LF** (linear feet)

**29ga vs 26ga:**
- 29ga: Thinner, lighter, lower cost (typical residential)
- 26ga: Thicker, heavier, higher cost (commercial, high-wind areas)
- Same coverage area, different material cost

**Sources:**
- Panel coverage: 36" typical per manufacturer specifications
- Waste factor: 5-10% typical per industry practice
- Fastener spacing: 1 per 1-2 sq ft per manufacturer recommendations

---

### 5. Wall & Roof Sheathing (OSB/Plywood)

**Parts Involved:**
- OSB (Oriented Strand Board) sheets
- Plywood sheets
- Fasteners (nails or screws)
- Vapor barrier (if required)

**Spacing/Usage:**
- Standard sheet size: 4' x 8' = 32 sq ft
- Applied to wall or roof before exterior finish
- Typical thickness: 7/16" or 1/2" for walls, 5/8" or 3/4" for roof
- Waste factor: 10-15% typical (cutting, end pieces)

**Material Takeoff Units:**
- Sheathing: **SF** (square feet) or **EA** (sheet count)
- Fasteners: **EA** (typically 1 fastener per 6-8 inches along edges)

**OSB vs Plywood:**
- OSB: Lower cost, typical for non-structural sheathing
- Plywood: Higher cost, may be required for structural sheathing
- Same coverage area, different material cost

**Sources:**
- Standard sheet size: 4' x 8' per industry standard
- Waste factor: 10-15% typical per construction practice
- Thickness varies by application (manufacturer specifications)

---

### 6. Insulation (Walls vs Roof)

**Parts Involved:**
- Fiberglass batts (R-19, R-30, etc.)
- Rock wool batts
- Rigid board insulation (polyiso, XPS, EPS)
- Spray foam (closed-cell or open-cell)
- Vapor barrier (for some types)

**Spacing/Usage:**
- **Walls:** Applied between girts or in wall cavity
  - Batt insulation: Sized to fit between framing (typically 24" o.c. spacing)
  - Rigid board: Applied to exterior or interior face
  - Spray foam: Applied in cavity or as continuous layer
  
- **Roof:** Applied between purlins or as continuous layer
  - Similar types and applications as walls
  - May require different R-values

**Material Takeoff Units:**
- Insulation: **SF** (square feet) - based on wall or roof area
- Vapor barrier: **SF** (if separate)

**Types:**
- **Fiberglass batts:** Typical R-19 for walls, R-30+ for roof
- **Rock wool:** Similar R-values, higher cost, better fire resistance
- **Rigid board:** R-5 to R-7 per inch, applied as continuous layer
- **Spray foam:** R-6 to R-7 per inch (closed-cell), applied in place

**Sources:**
- R-value requirements: IRC Section R402 (Energy Code) - varies by climate zone
- Typical R-values: R-19 walls, R-30+ roof per industry practice
- Coverage: Based on wall/roof area with minimal waste (batts cut to fit)

---

### 7. Doors and Windows (Openings)

**Parts Involved:**
- Extra framing lumber (king studs, trimmers/jacks, headers, sill plates)
- Exterior trim (jambs, head, sill)
- Fasteners

**Spacing/Usage:**
- **Door framing:**
  - King studs: 2 per door (one each side)
  - Trimmers/jacks: 2 per door (support header)
  - Header: 1 per door (typically 2x8 or 2x10, length = door width + 6")
  - Sill plate: 1 per door (if not slab-on-grade)
  
- **Window framing:**
  - Similar to doors but typically smaller headers
  - Sill plate: 1 per window
  - Header: Typically 2x6 or 2x8

- **Trim:**
  - Door trim: Head + 2 jambs = ~(door width + 2 × door height)
  - Window trim: Head + sill + 2 jambs = ~(window width + 2 × window height + window width)

**Material Takeoff Units:**
- Framing lumber: **BF** (board feet) or **LF** (linear feet)
- Trim: **LF** (linear feet)

**Assumptions (for estimator):**
- Standard door: 3' x 7' (36" x 84")
- Standard window: 3' x 3' (36" x 36")
- Header size: 2x8 for doors, 2x6 for windows
- These can be made configurable later

**Sources:**
- Typical door sizes: 3' x 7' standard per industry practice
- Header sizing: Based on span and load (simplified for estimator)
- Trim coverage: Based on perimeter of opening

---

### 8. Overhead/Roll-Up Doors

**Parts Involved:**
- Door unit (steel roll-up or sectional)
- Track and hardware
- Operator (if motorized)
- Framing reinforcement (if required)

**Spacing/Usage:**
- Typically 8' to 16' wide, 7' to 14' high
- One door per opening
- May require additional framing around opening

**Material Takeoff Units:**
- Door unit: **EA** (each) - typically priced as complete unit
- Additional framing: **BF** or **LF** (if required)

**Types:**
- **Steel roll-up:** Lower cost, typical for storage/agricultural
- **Sectional:** Higher cost, typical for residential/commercial
- Motorized operator: Additional cost

**Sources:**
- Typical sizes: 8' x 7' to 16' x 14' per manufacturer catalogs
- Pricing: Typically as complete unit (door + track + hardware)

---

### 9. Floor (Slab vs Gravel vs None)

**Parts Involved:**
- **Slab:**
  - Concrete (typically 4" to 6" thick)
  - Reinforcement (wire mesh or rebar)
  - Vapor barrier
  - Edge forms
  
- **Gravel:**
  - Base gravel (typically 4" to 6" thick)
  - Compaction

- **None:**
  - Native soil (may require grading)

**Spacing/Usage:**
- Slab: Full building footprint area
- Gravel: Full building footprint area
- Thickness: 4" typical for residential, 6" for commercial/heavy use

**Material Takeoff Units:**
- Concrete: **CY** (cubic yards) = (area × thickness) / 27
- Reinforcement: **SF** (wire mesh) or **LB** (rebar)
- Gravel: **CY** (cubic yards)

**Sources:**
- Typical slab thickness: 4" residential, 6" commercial per IRC
- Concrete volume: Area × thickness / 27 (conversion to cubic yards)
- Reinforcement: Wire mesh typical for 4" slab, rebar for 6"+

---

### 10. MEP (Mechanical, Electrical, Plumbing) - Allowances Only

**Parts Involved:**
- Electrical: Basic lighting, outlets, service panel
- Plumbing: Basic fixtures, water/sewer connections
- Mechanical: Basic heating/ventilation

**Spacing/Usage:**
- **Electrical (code minimum):**
  - Outlets: 1 per 12 linear feet of wall (IRC E3801.2)
  - Lighting: Minimum 1 per room/area
  - Service: 100A typical for small buildings
  
- **Plumbing:**
  - Basic fixtures if bathroom/kitchen included
  - Water/sewer connections
  
- **Mechanical:**
  - Basic ventilation (may be code-required)
  - Heating (if enclosed/conditioned)

**Material Takeoff Units:**
- **Allowance-based only** (not detailed takeoff)
- Units: **$** (dollar allowance per category)

**Note:** This estimator treats MEP as cost allowances, not detailed material takeoffs. Detailed MEP design is beyond the scope of this tool.

**Sources:**
- IRC E3801.2 - Outlet spacing requirements
- Typical allowances: Based on building size and use (industry practice)

---

## Mapping to Existing Code Structure

### `systems/pole_barn/assemblies.py`

**Current Structure:**
- `calculate_material_quantities()` - Main function
- Helper functions: `_calculate_post_count()`, `_calculate_truss_count()`, `_calculate_girt_quantities()`, etc.

**Additions Needed:**
- `_calculate_door_framing()` - Extra lumber for doors
- `_calculate_window_framing()` - Extra lumber for windows
- `_calculate_door_trim()` - Trim LF for doors
- `_calculate_window_trim()` - Trim LF for windows
- `_calculate_wall_insulation()` - Wall insulation SF
- `_calculate_roof_insulation()` - Roof insulation SF
- `_calculate_slab_concrete()` - Concrete CY for slab
- Branching logic for exterior finish type (29ga vs 26ga)

### `config/assemblies.example.csv`

**Current Columns:**
- `assembly_name`, `part_id`, `waste_factor`, `labor_per_unit`, `notes`

**Additions Needed:**
- Door/window framing assemblies
- Door/window trim assemblies
- Wall/roof insulation assemblies (by type)
- Slab concrete assembly
- Exterior finish variants (29ga vs 26ga)

### `config/parts.example.csv`

**Current Parts:**
- Basic framing, panels, trim, fasteners, concrete, insulation

**Additions Needed:**
- 26ga metal panels (separate from 29ga)
- OSB sheathing
- Plywood sheathing
- Door/window framing lumber (or use existing 2x6)
- Door/window trim (or use existing trim parts)
- Different insulation types (fiberglass, rock wool, rigid, spray foam)
- Overhead door units

### `config/pricing.example.csv`

**Additions Needed:**
- Unit prices for all new parts
- Pricing for overhead doors (as complete units)

---

## Implementation Notes

### Assumptions Documented in Code

1. **Door/Window Sizes (for framing calculations):**
   - Standard door: 3' x 7' (36" x 84")
   - Standard window: 3' x 3' (36" x 36")
   - These are assumptions for quantity estimation; actual sizes can vary

2. **Girt/Purlin Spacing:**
   - Default: 24" on center
   - Can be overridden by user input

3. **Waste Factors:**
   - Panels: 5-10% (use 5% = 1.05)
   - Trim: 10% (use 1.10)
   - Sheathing: 10-15% (use 10% = 1.10)
   - Lumber: 5-10% (use 5% = 1.05)

4. **Insulation Coverage:**
   - Based on wall/roof area
   - Minimal waste for batts (cut to fit)
   - Waste factor: 1.0 for batts, 1.05 for rigid board

5. **Concrete Slab:**
   - Default thickness: 4" (residential)
   - Can be overridden by user input
   - Volume = area × thickness / 27 (cubic yards)

---

## References and Sources

1. **Post-Frame Construction:**
   - National Frame Builders Association (NFBA) - General construction practices
   - Industry standard spacing and sizing practices

2. **Building Codes:**
   - IRC (International Residential Code) - General construction requirements
   - IRC Section R301 - General requirements
   - IRC Section R402 - Energy code (insulation R-values)
   - IRC Section E3801.2 - Electrical outlet spacing

3. **Material Specifications:**
   - Manufacturer literature (metal panels, insulation, etc.)
   - Industry standard sheet sizes (OSB, plywood: 4' x 8')

4. **Construction Practices:**
   - Typical spacing: 24" o.c. for girts/purlins (industry practice)
   - Typical waste factors: 5-15% depending on material (construction practice)
   - Typical door/window sizes: Industry standard sizes

**Note:** This document summarizes industry practices and typical construction methods. It does not reproduce copyrighted code text but paraphrases common practices that are widely known in the construction industry.

---

*Document created: Assemblies Deep Dive - Research Phase*


---

### File: ASSEMBLIES_STATUS.md

# Assemblies Implementation Status

## Overview

This document tracks the implementation status of post-frame construction assemblies based on the deep dive research and design work.

**Date:** Assemblies Deep Dive Implementation  
**Phase:** Research + Limited Implementation (Path B continuation)

---

## ✅ Completed Implementation

### 1. Door & Window Assemblies (Changelog Entry [14])

**Status:** ✅ IMPLEMENTED

**Changes:**
- Added `_calculate_door_window_assemblies()` function in `assemblies.py`
- Calculates extra framing lumber for doors and windows:
  - Door framing: Headers (2x8), king studs, trimmers
  - Window framing: Headers (2x6), king studs, trimmers
- Calculates exterior trim for doors and windows:
  - Door trim: Head + 2 jambs
  - Window trim: Head + sill + 2 jambs

**Assumptions:**
- Standard door: 3' x 7' (36" x 84")
- Standard window: 3' x 3' (36" x 36")
- These can be made configurable in future phases

**New Assemblies:**
- `door_framing` - Extra framing lumber for doors (LF)
- `window_framing` - Extra framing lumber for windows (LF)
- `door_trim` - Exterior trim for doors (LF)
- `window_trim` - Exterior trim for windows (LF)

**CSV Updates:**
- Added to `assemblies.example.csv` with mappings to `LBR_2X6_LF` and trim parts
- Added `TRIM_DOOR` and `TRIM_WINDOW` to `parts.example.csv`
- Added pricing for door/window trim

**Tests:** Need to add tests verifying door/window counts increase these quantities

---

### 2. Exterior Finish Structure (Changelog Entry [15])

**Status:** ✅ PARTIALLY IMPLEMENTED (Structure only, no GUI)

**Changes:**
- Added `exterior_finish_type` field to `MaterialInputs` (default: `"metal_29ga"`)
- Updated roof/wall panel logic to branch on `exterior_finish_type`
- Supports:
  - `metal_29ga` (default) - Uses `roof_panels`, `sidewall_panels`, `endwall_panels`
  - `metal_26ga` - Uses `roof_panels_26ga`, `sidewall_panels_26ga`, `endwall_panels_26ga`
  - `lap_siding` - TODO placeholder
  - `stucco` - TODO placeholder

**New Parts:**
- `METAL_PANEL_26_SQFT` - 26ga metal panels (added to parts and pricing CSVs)

**New Assemblies:**
- `roof_panels_26ga` - 26ga roof panels
- `sidewall_panels_26ga` - 26ga sidewall panels
- `endwall_panels_26ga` - 26ga endwall panels

**TODOs:**
- Implement lap siding assemblies
- Implement stucco assemblies
- Wire GUI dropdown (deferred to future phase)

**Tests:** Need to add tests verifying 26ga vs 29ga selection works

---

### 3. Insulation Types - Wall/Roof Split (Changelog Entry [16])

**Status:** ✅ IMPLEMENTED

**Changes:**
- Added `wall_insulation_type` and `roof_insulation_type` fields to `MaterialInputs` (default: `"none"`)
- Updated `_calculate_insulation_quantities()` to handle separate wall/roof insulation
- Supports insulation types:
  - `fiberglass_batts` - Standard fiberglass (R-19 typical)
  - `rock_wool` - Rock wool batts
  - `rigid_board` - Rigid board insulation
  - `spray_foam` - Spray foam insulation

**New Parts:**
- `INS_ROCKWOOL_SQFT` - Rock wool insulation
- `INS_RIGID_SQFT` - Rigid board insulation
- `INS_SPRAYFOAM_SQFT` - Spray foam insulation

**New Assemblies:**
- `wall_insulation` - Wall fiberglass (default)
- `wall_insulation_rockwool` - Wall rock wool
- `wall_insulation_rigid` - Wall rigid board
- `wall_insulation_sprayfoam` - Wall spray foam
- `roof_insulation` - Roof fiberglass (default)
- `roof_insulation_rockwool` - Roof rock wool
- `roof_insulation_rigid` - Roof rigid board
- `roof_insulation_sprayfoam` - Roof spray foam

**CSV Updates:**
- Added all insulation type assemblies to `assemblies.example.csv`
- Added all insulation parts to `parts.example.csv` and `pricing.example.csv`

**TODOs:**
- Wire GUI dropdowns for wall/roof insulation (deferred to future phase)
- Subtract door/window openings from wall insulation area (for accuracy)

**Tests:** Need to add tests verifying insulation types produce correct quantities

---

### 4. MEP Allowances (Changelog Entry [18])

**Status:** ✅ IMPLEMENTED

**Changes:**
- Added MEP allowance fields to `PricingInputs`:
  - `include_electrical: bool = False`
  - `electrical_allowance: float = 0.0`
  - `include_plumbing: bool = False`
  - `plumbing_allowance: float = 0.0`
  - `include_mechanical: bool = False`
  - `mechanical_allowance: float = 0.0`
- Updated `price_material_takeoff()` to create MEP allowance line items
- MEP allowances are:
  - Added as separate `PricedLineItem` entries with category "MEP"
  - Included in material subtotal and grand total
  - NOT marked up (markup_percent = 0.0)

**New Line Items:**
- `electrical_allowance` - Electrical allowance (if enabled and > 0)
- `plumbing_allowance` - Plumbing allowance (if enabled and > 0)
- `mechanical_allowance` - Mechanical allowance (if enabled and > 0)

**TODOs:**
- Wire GUI toggles and allowance inputs (deferred to future phase)
- Consider code-minimum calculations (e.g., outlet spacing per IRC)

**Tests:** Need to add tests verifying MEP allowances appear when enabled

---

## 📋 Files Modified

### Core Models
- `systems/pole_barn/model.py`
  - Added `exterior_finish_type`, `wall_insulation_type`, `roof_insulation_type` to `MaterialInputs`
  - Added MEP allowance fields to `PricingInputs`

### Assemblies Logic
- `systems/pole_barn/assemblies.py`
  - Added `_calculate_door_window_assemblies()` function
  - Added `_calculate_insulation_quantities()` function (enhanced)
  - Updated `calculate_material_quantities()` to accept `geometry_inputs` parameter
  - Updated roof/wall panel logic to branch on `exterior_finish_type`

### Pricing Logic
- `systems/pole_barn/pricing.py`
  - Updated `price_material_takeoff()` to create MEP allowance line items
  - Updated `_create_simple_assembly_mapping()` with new assemblies

### Calculator
- `systems/pole_barn/calculator.py`
  - Updated to pass `geometry_inputs` to `calculate_material_quantities()`

### Configuration Files
- `config/parts.example.csv`
  - Added: `METAL_PANEL_26_SQFT`, `TRIM_DOOR`, `TRIM_WINDOW`
  - Added: `INS_ROCKWOOL_SQFT`, `INS_RIGID_SQFT`, `INS_SPRAYFOAM_SQFT`
  - Added: `SHEATHING_OSB_SQFT`, `SHEATHING_PLY_SQFT`, `OVERHEAD_DOOR`

- `config/pricing.example.csv`
  - Added unit prices for all new parts

- `config/assemblies.example.csv`
  - Added: `door_framing`, `window_framing`, `door_trim`, `window_trim`
  - Added: `roof_panels_26ga`, `sidewall_panels_26ga`, `endwall_panels_26ga`
  - Added: All insulation type variants (wall and roof)

---

## 🟡 Partially Addressed Changelog Entries

### Entry [14] - Door & Window Assemblies
- ✅ Framing and trim calculations implemented
- ⏳ GUI wiring deferred (no GUI changes in this phase)
- ⏳ Multiple door/window sizes deferred (using standard sizes for now)

### Entry [15] - Exterior Finish
- ✅ Structure implemented (29ga vs 26ga)
- ⏳ Lap siding implementation deferred
- ⏳ Stucco implementation deferred
- ⏳ GUI wiring deferred

### Entry [16] - Insulation Types
- ✅ Wall/roof split implemented
- ✅ All insulation types supported
- ⏳ GUI wiring deferred
- ⏳ Opening subtraction for accuracy deferred

### Entry [18] - MEP Allowances
- ✅ Allowance structure implemented
- ⏳ GUI wiring deferred
- ⏳ Code-minimum calculations deferred

---

## 🔴 Not Yet Implemented (Future Phases)

### Entry [17] - Roll-up Doors
- Structure not yet implemented
- Needs overhead door assembly logic
- Part `OVERHEAD_DOOR` added to CSV but not used

### Entry [19] - Post Type Selector
- Structure not yet implemented
- Needs branching logic for PT vs laminated

### Entry [20] - Truss/Post Connection Type
- Structure not yet implemented
- Needs logic for notched vs cleated (affects fasteners/labor)

### Entry [21] - Multiple Door Sizes
- Deferred to Phase 2
- Currently uses standard sizes

### Entry [22] - Lean-to Module
- Deferred to Phase 2
- Complex feature requiring separate geometry

---

## 📝 Assumptions Documented

### Door/Window Sizes
- Standard door: 3' x 7' (36" x 84")
- Standard window: 3' x 3' (36" x 36")
- **Source:** Industry standard sizes (documented in ASSEMBLIES_DESIGN.md)

### Framing Details
- Door header: 2x8, length = door width + 6"
- Window header: 2x6, length = window width + 6"
- King studs: 2 per opening
- Trimmers: 2 per opening
- **Source:** Typical construction practice (documented in ASSEMBLIES_DESIGN.md)

### Insulation Coverage
- Based on wall/roof area
- Waste factor: 1.0 for batts (cut to fit), 1.05 for rigid board
- **Source:** Construction practice (documented in ASSEMBLIES_DESIGN.md)

### MEP Allowances
- Treated as cost buckets only (not detailed takeoff)
- Not marked up (markup_percent = 0.0)
- **Source:** Estimator practice (documented in ASSEMBLIES_DESIGN.md)

---

## 🧪 Testing Status

### Tests Needed
- [ ] Door/window framing quantities increase with door/window counts
- [ ] Door/window trim quantities increase with door/window counts
- [ ] 26ga panels use correct part_id when `exterior_finish_type == "metal_26ga"`
- [ ] Wall insulation appears when `wall_insulation_type != "none"`
- [ ] Roof insulation appears when `roof_insulation_type != "none"`
- [ ] Different insulation types map to correct parts
- [ ] MEP allowances appear in priced output when enabled
- [ ] MEP allowances are included in grand total but not marked up

### Existing Tests
- Should still pass (no breaking changes)
- May need updates for new field defaults

---

## 📚 Research Sources

All assumptions and design decisions are documented in:
- **`ASSEMBLIES_DESIGN.md`** - Complete design document with sources

Key sources referenced:
- Post-Frame Building Design Manual (NFBA)
- IRC Section R301, R402, E3801.2
- Industry standard spacing practices (24" o.c. typical)
- Manufacturer specifications (panel coverage, etc.)
- Construction practice (waste factors, typical sizes)

---

## 🎯 Next Steps

1. **Add Tests:**
   - Test door/window assemblies
   - Test exterior finish branching
   - Test insulation type selection
   - Test MEP allowances

2. **GUI Wiring (Future Phase):**
   - Add exterior finish dropdown
   - Add wall/roof insulation dropdowns
   - Add MEP toggles and allowance inputs

3. **Enhancements (Future Phases):**
   - Implement lap siding and stucco
   - Implement roll-up doors
   - Implement post type and connection type logic
   - Add multiple door/window sizes
   - Subtract openings from insulation area

---

*Status document created: Assemblies Deep Dive Implementation*


---

### File: control/pole_barn_calculator.md

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


---

## Test Files

### File: tests/test_geometry.py

```python
"""Tests for geometry calculations."""

import pytest
import math
from systems.pole_barn.model import GeometryInputs, GeometryModel
from systems.pole_barn import geometry


def test_geometry_inputs_creation():
    """Test that GeometryInputs can be created with required fields."""
    geometry_inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=2.0,
        overhang_rear=2.0,
        overhang_sides=1.0,
        door_count=2,
        door_width=12.0,
        door_height=10.0,
        window_count=4,
        window_width=3.0,
        window_height=2.0,
        pole_spacing_length=8.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    assert geometry_inputs.length == 40.0
    assert geometry_inputs.width == 30.0
    assert geometry_inputs.eave_height == 12.0
    assert geometry_inputs.peak_height == 16.0  # Can still be provided explicitly


def test_peak_height_derivation():
    """Test that peak height is derived when not provided."""
    geometry_inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=None,  # Not provided - should be derived
        roof_pitch=0.333,  # 4:12 pitch
        overhang_front=0.0,
        overhang_rear=0.0,
        overhang_sides=0.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=10.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    model = geometry.build_geometry_model(geometry_inputs)
    
    # For 30ft width, 4:12 pitch, centered ridge:
    # run = 30 / 2 = 15ft
    # rise = 15 * 0.333 = 5ft
    # peak_height = 12 + 5 = 17ft
    expected_peak = 12.0 + (30.0 / 2.0) * 0.333
    assert model.peak_height_ft == pytest.approx(expected_peak, rel=1e-2)
    assert model.peak_height_ft > geometry_inputs.eave_height


def test_build_geometry_model():
    """Test building a complete geometry model."""
    inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,  # 4:12 pitch
        overhang_front=1.0,
        overhang_rear=1.0,
        overhang_sides=1.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=10.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    model = geometry.build_geometry_model(inputs)
    
    # Check dimensions
    assert model.overall_length_ft == 40.0
    assert model.overall_width_ft == 30.0
    assert model.eave_height_ft == 12.0
    assert model.peak_height_ft == 16.0
    
    # Check overhangs
    assert model.sidewall_overhang_ft == 1.0
    assert model.endwall_overhang_front_ft == 1.0
    assert model.endwall_overhang_rear_ft == 1.0
    
    # Check bays
    assert model.bay_spacing_ft == 10.0
    assert model.num_bays == 4  # ceil(40 / 10) = 4
    assert model.num_frame_lines == 5  # bays + 1
    
    # Check footprint area
    assert model.footprint_area_sqft == pytest.approx(1200.0)  # 40 * 30
    
    # Check wall areas
    sidewall_area_expected = 2 * 40.0 * 12.0  # 2 sidewalls
    endwall_area_expected = 2 * 30.0 * 12.0  # 2 endwalls
    assert model.sidewall_area_sqft == pytest.approx(sidewall_area_expected)
    assert model.endwall_area_sqft == pytest.approx(endwall_area_expected)
    assert model.total_wall_area_sqft == pytest.approx(
        sidewall_area_expected + endwall_area_expected
    )
    
    # Check roof area (with pitch and overhangs)
    # Effective length: 40 + 1 + 1 = 42
    # Effective width: 30 + 2*1 = 32
    # Plan area: 42 * 32 = 1344
    # Slope factor for 4:12 (0.333): sqrt(1 + 0.333^2) = sqrt(1.111) ≈ 1.054
    # Roof area: 1344 * 1.054 ≈ 1416.6
    L_eff = 40.0 + 1.0 + 1.0
    W_eff = 30.0 + 2 * 1.0
    plan_area = L_eff * W_eff
    slope_factor = math.sqrt(1 + 0.333 ** 2)
    expected_roof_area = plan_area * slope_factor
    assert model.roof_area_sqft == pytest.approx(expected_roof_area, rel=1e-3)
    
    # Check volume
    expected_volume = 40.0 * 30.0 * 12.0
    assert model.building_volume_cuft == pytest.approx(expected_volume)


def test_calculate_roof_area():
    """Test roof area calculation."""
    inputs = GeometryInputs(
        length=60.0,
        width=40.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,  # 4:12
        overhang_front=2.0,
        overhang_rear=2.0,
        overhang_sides=1.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=10.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    roof_area = geometry.calculate_roof_area(inputs)
    
    # Manual calculation
    L_eff = 60.0 + 2.0 + 2.0  # 64
    W_eff = 40.0 + 2 * 1.0  # 42
    plan_area = L_eff * W_eff  # 2688
    slope_factor = math.sqrt(1 + 0.333 ** 2)
    expected = plan_area * slope_factor
    
    assert roof_area == pytest.approx(expected, rel=1e-3)
    assert roof_area > plan_area  # Roof area should be larger than plan area


def test_calculate_wall_area():
    """Test wall area calculation."""
    inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=0.0,
        overhang_rear=0.0,
        overhang_sides=0.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=8.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    wall_areas = geometry.calculate_wall_area(inputs)
    
    assert wall_areas['front'] == pytest.approx(30.0 * 12.0)
    assert wall_areas['rear'] == pytest.approx(30.0 * 12.0)
    assert wall_areas['left'] == pytest.approx(40.0 * 12.0)
    assert wall_areas['right'] == pytest.approx(40.0 * 12.0)


def test_calculate_floor_area():
    """Test floor area calculation."""
    inputs = GeometryInputs(
        length=50.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=0.0,
        overhang_rear=0.0,
        overhang_sides=0.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=10.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    floor_area = geometry.calculate_floor_area(inputs)
    assert floor_area == pytest.approx(50.0 * 30.0)


def test_calculate_door_window_openings():
    """Test door and window opening calculations."""
    inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=0.0,
        overhang_rear=0.0,
        overhang_sides=0.0,
        door_count=2,
        door_width=12.0,
        door_height=10.0,
        window_count=4,
        window_width=3.0,
        window_height=2.0,
        pole_spacing_length=8.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    openings = geometry.calculate_door_window_openings(inputs)
    
    expected_door_area = 2 * 12.0 * 10.0  # 240
    expected_window_area = 4 * 3.0 * 2.0  # 24
    
    assert openings['door_area'] == pytest.approx(expected_door_area)
    assert openings['window_area'] == pytest.approx(expected_window_area)


def test_calculate_roof_volume():
    """Test roof volume calculation."""
    inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=0.0,
        overhang_rear=0.0,
        overhang_sides=0.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=8.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    volume = geometry.calculate_roof_volume(inputs)
    expected = 40.0 * 30.0 * 12.0
    assert volume == pytest.approx(expected)


def test_get_geometry_summary():
    """Test geometry summary function."""
    inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=1.0,
        overhang_rear=1.0,
        overhang_sides=1.0,
        door_count=1,
        door_width=10.0,
        door_height=8.0,
        window_count=2,
        window_width=2.0,
        window_height=2.0,
        pole_spacing_length=10.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    summary = geometry.get_geometry_summary(inputs)
    
    assert 'dimensions' in summary
    assert 'overhangs' in summary
    assert 'bays' in summary
    assert 'areas' in summary
    assert 'volume' in summary
    assert 'openings' in summary
    
    assert summary['dimensions']['length_ft'] == 40.0
    assert summary['bays']['num_bays'] == 4
    assert summary['openings']['door_area'] == pytest.approx(80.0)


def test_pole_count_raises_not_implemented():
    """Test that pole count calculation still raises NotImplementedError."""
    inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=0.0,
        overhang_rear=0.0,
        overhang_sides=0.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=8.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    with pytest.raises(NotImplementedError):
        geometry.calculate_pole_count(inputs)


def test_bay_calculation_edge_cases():
    """Test bay calculations with edge cases."""
    # Test exact division
    inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=0.0,
        overhang_rear=0.0,
        overhang_sides=0.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=10.0,  # Exactly divides 40
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    model = geometry.build_geometry_model(inputs)
    assert model.num_bays == 4
    assert model.num_frame_lines == 5
    
    # Test non-exact division (should round up)
    inputs.pole_spacing_length = 7.0  # 40/7 = 5.71, should round up to 6
    model = geometry.build_geometry_model(inputs)
    assert model.num_bays == 6
    assert model.num_frame_lines == 7
```

---

### File: tests/test_assemblies.py

```python
"""Tests for assembly and material quantity calculations."""

import pytest
from systems.pole_barn.model import (
    PoleBarnInputs,
    GeometryInputs,
    MaterialInputs,
    PricingInputs,
    AssemblyInputs,
    AssemblyQuantity,
    MaterialTakeoff,
)
from systems.pole_barn import assemblies
from systems.pole_barn import geometry


def test_calculate_material_quantities():
    """Test the main material quantities calculation function."""
    # Build geometry model
    geometry_inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,  # 4:12
        overhang_front=1.0,
        overhang_rear=1.0,
        overhang_sides=1.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=10.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    geom_model = geometry.build_geometry_model(geometry_inputs)
    
    material_inputs = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,  # Same as bay spacing
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
    )
    
    assembly_inputs = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    quantities = assemblies.calculate_material_quantities(
        geom_model, material_inputs, assembly_inputs
    )
    
    # Should have multiple items
    assert len(quantities) > 0
    
    # Check for key categories
    categories = {item.category for item in quantities}
    assert "framing" in categories
    assert "roof" in categories
    assert "wall" in categories
    assert "trim" in categories
    
    # Check for specific items
    names = {item.name for item in quantities}
    assert "posts" in names
    assert "trusses" in names
    assert "sidewall_girts" in names
    assert "roof_purlins" in names
    assert "roof_panels" in names
    assert "sidewall_panels" in names
    assert "endwall_panels" in names
    assert "eave_trim" in names
    assert "rake_trim" in names
    assert "base_trim" in names
    assert "corner_trim" in names


def test_post_count_calculation():
    """Test post count calculation."""
    geometry_inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=0.0,
        overhang_rear=0.0,
        overhang_sides=0.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=10.0,  # 40/10 = 4 bays, 5 frame lines
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    geom_model = geometry.build_geometry_model(geometry_inputs)
    material_inputs = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
    )
    assembly_inputs = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    quantities = assemblies.calculate_material_quantities(
        geom_model, material_inputs, assembly_inputs
    )
    
    posts_item = next((item for item in quantities if item.name == "posts"), None)
    assert posts_item is not None
    assert posts_item.quantity == 10  # 5 frame lines × 2 sidewalls
    assert posts_item.unit == "ea"
    assert posts_item.category == "framing"


def test_truss_count_calculation():
    """Test truss count calculation."""
    geometry_inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=0.0,
        overhang_rear=0.0,
        overhang_sides=0.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=10.0,  # 4 bays, 5 frame lines
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    geom_model = geometry.build_geometry_model(geometry_inputs)
    material_inputs = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,  # Same as bay spacing
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
    )
    assembly_inputs = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    quantities = assemblies.calculate_material_quantities(
        geom_model, material_inputs, assembly_inputs
    )
    
    trusses_item = next((item for item in quantities if item.name == "trusses"), None)
    assert trusses_item is not None
    assert trusses_item.quantity == 5  # One per frame line
    assert trusses_item.unit == "ea"


def test_girt_calculation():
    """Test girt quantity calculation."""
    geometry_inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,  # 12ft height
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=0.0,
        overhang_rear=0.0,
        overhang_sides=0.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=10.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    geom_model = geometry.build_geometry_model(geometry_inputs)
    material_inputs = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,  # 12ft / 2ft = 6 rows
        foundation_type="concrete_pad",
    )
    assembly_inputs = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    quantities = assemblies.calculate_material_quantities(
        geom_model, material_inputs, assembly_inputs
    )
    
    sidewall_girts_item = next(
        (item for item in quantities if item.name == "sidewall_girts"), None
    )
    assert sidewall_girts_item is not None
    # 6 rows × 40ft × 2 sidewalls = 480 LF
    assert sidewall_girts_item.quantity == pytest.approx(480.0)
    assert sidewall_girts_item.unit == "lf"


def test_roof_panel_calculation():
    """Test roof panel quantity calculation."""
    geometry_inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=1.0,
        overhang_rear=1.0,
        overhang_sides=1.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=10.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    geom_model = geometry.build_geometry_model(geometry_inputs)
    material_inputs = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
    )
    assembly_inputs = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    quantities = assemblies.calculate_material_quantities(
        geom_model, material_inputs, assembly_inputs
    )
    
    roof_panels_item = next(
        (item for item in quantities if item.name == "roof_panels"), None
    )
    assert roof_panels_item is not None
    assert roof_panels_item.quantity == pytest.approx(geom_model.roof_area_sqft)
    assert roof_panels_item.unit == "sqft"
    assert roof_panels_item.category == "roof"


def test_wall_panel_calculation():
    """Test wall panel quantity calculation."""
    geometry_inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=0.0,
        overhang_rear=0.0,
        overhang_sides=0.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=10.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    geom_model = geometry.build_geometry_model(geometry_inputs)
    material_inputs = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
    )
    assembly_inputs = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    quantities = assemblies.calculate_material_quantities(
        geom_model, material_inputs, assembly_inputs
    )
    
    sidewall_panels_item = next(
        (item for item in quantities if item.name == "sidewall_panels"), None
    )
    assert sidewall_panels_item is not None
    assert sidewall_panels_item.quantity == pytest.approx(960.0)  # 2 × 40 × 12
    assert sidewall_panels_item.unit == "sqft"
    
    endwall_panels_item = next(
        (item for item in quantities if item.name == "endwall_panels"), None
    )
    assert endwall_panels_item is not None
    assert endwall_panels_item.quantity == pytest.approx(720.0)  # 2 × 30 × 12
    assert endwall_panels_item.unit == "sqft"


def test_trim_calculation():
    """Test trim quantity calculations."""
    geometry_inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=0.0,
        overhang_rear=0.0,
        overhang_sides=0.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=10.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    geom_model = geometry.build_geometry_model(geometry_inputs)
    material_inputs = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
    )
    assembly_inputs = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    quantities = assemblies.calculate_material_quantities(
        geom_model, material_inputs, assembly_inputs
    )
    
    # Check trim items
    eave_trim = next((item for item in quantities if item.name == "eave_trim"), None)
    assert eave_trim is not None
    assert eave_trim.quantity == pytest.approx(80.0)  # 2 × 40
    assert eave_trim.unit == "lf"
    
    rake_trim = next((item for item in quantities if item.name == "rake_trim"), None)
    assert rake_trim is not None
    assert rake_trim.quantity == pytest.approx(60.0)  # 2 × 30
    assert rake_trim.unit == "lf"
    
    base_trim = next((item for item in quantities if item.name == "base_trim"), None)
    assert base_trim is not None
    assert base_trim.quantity == pytest.approx(140.0)  # 2 × (40 + 30)
    assert base_trim.unit == "lf"
    
    corner_trim = next((item for item in quantities if item.name == "corner_trim"), None)
    assert corner_trim is not None
    assert corner_trim.quantity == pytest.approx(48.0)  # 4 × 12
    assert corner_trim.unit == "lf"


def test_legacy_functions():
    """Test that legacy function signatures still work."""
    geometry_inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=0.0,
        overhang_rear=0.0,
        overhang_sides=0.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=10.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    materials = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
    )
    
    pricing = PricingInputs(
        material_markup=1.15,
        tax_rate=0.08,
        labor_rate=50.0,
    )
    
    assemblies_input = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    inputs = PoleBarnInputs(
        geometry=geometry_inputs,
        materials=materials,
        pricing=pricing,
        assemblies=assemblies_input,
    )
    
    # Test legacy functions
    truss_count = assemblies.calculate_truss_quantity(inputs)
    assert truss_count == 5
    
    purlin_result = assemblies.calculate_purlin_quantity(inputs)
    assert "total_length_lf" in purlin_result
    assert purlin_result["total_length_lf"] > 0
    
    girt_result = assemblies.calculate_girt_quantity(inputs)
    assert "total_length_lf" in girt_result
    assert girt_result["total_length_lf"] > 0
    
    roofing_result = assemblies.calculate_roofing_material(inputs)
    assert "quantity" in roofing_result
    assert roofing_result["quantity"] > 0
    
    wall_result = assemblies.calculate_wall_material(inputs)
    assert "total_quantity" in wall_result
    assert wall_result["total_quantity"] > 0


def test_insulation_calculation():
    """Test insulation quantity calculation."""
    geometry_inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=0.0,
        overhang_rear=0.0,
        overhang_sides=0.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=10.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    materials = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
        insulation_type="fiberglass",
        insulation_r_value=19.0,
    )
    
    pricing = PricingInputs(
        material_markup=1.15,
        tax_rate=0.08,
        labor_rate=50.0,
    )
    
    assemblies_input = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    inputs = PoleBarnInputs(
        geometry=geometry_inputs,
        materials=materials,
        pricing=pricing,
        assemblies=assemblies_input,
    )
    
    insulation_result = assemblies.calculate_insulation_quantity(inputs)
    assert insulation_result["insulation_type"] == "fiberglass"
    assert insulation_result["quantity"] > 0
    assert insulation_result["r_value"] == 19.0


def test_ventilation_calculation():
    """Test ventilation quantity calculation."""
    geometry_inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=0.0,
        overhang_rear=0.0,
        overhang_sides=0.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=10.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    materials = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
    )
    
    pricing = PricingInputs(
        material_markup=1.15,
        tax_rate=0.08,
        labor_rate=50.0,
    )
    
    assemblies_input = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
        ventilation_type="ridge_vent",
        ventilation_count=2,
    )
    
    inputs = PoleBarnInputs(
        geometry=geometry_inputs,
        materials=materials,
        pricing=pricing,
        assemblies=assemblies_input,
    )
    
    ventilation_result = assemblies.calculate_ventilation_quantity(inputs)
    assert ventilation_result["ventilation_type"] == "ridge_vent"
    assert ventilation_result["count"] == 2


def test_get_assembly_summary():
    """Test assembly summary function."""
    geometry_inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=0.0,
        overhang_rear=0.0,
        overhang_sides=0.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=10.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    materials = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
    )
    
    pricing = PricingInputs(
        material_markup=1.15,
        tax_rate=0.08,
        labor_rate=50.0,
    )
    
    assemblies_input = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    inputs = PoleBarnInputs(
        geometry=geometry_inputs,
        materials=materials,
        pricing=pricing,
        assemblies=assemblies_input,
    )
    
    summary = assemblies.get_assembly_summary(inputs)
    
    assert "total_items" in summary
    assert "by_category" in summary
    assert summary["total_items"] > 0
    assert "framing" in summary["by_category"]
    assert "roof" in summary["by_category"]
    assert "wall" in summary["by_category"]
    assert "trim" in summary["by_category"]
```

---

### File: tests/test_pricing.py

```python
"""Tests for pricing calculations."""

import pytest
from pathlib import Path
from systems.pole_barn.model import (
    MaterialTakeoff,
    AssemblyQuantity,
    PricingInputs,
    PricedLineItem,
    PricingSummary,
)
from systems.pole_barn import pricing


def test_load_parts():
    """Test loading parts CSV."""
    parts_df = pricing.load_parts()
    
    assert len(parts_df) > 0
    assert "part_id" in parts_df.columns
    assert "part_name" in parts_df.columns
    
    # Check for expected parts
    part_ids = parts_df["part_id"].tolist()
    assert "POST_6X6_PT" in part_ids
    assert "METAL_PANEL_29_SQFT" in part_ids


def test_load_pricing():
    """Test loading pricing CSV."""
    pricing_df = pricing.load_pricing()
    
    assert len(pricing_df) > 0
    assert "part_id" in pricing_df.columns
    assert "unit_price" in pricing_df.columns
    
    # Check for expected pricing
    pricing_dict = dict(zip(pricing_df["part_id"], pricing_df["unit_price"]))
    assert "POST_6X6_PT" in pricing_dict
    assert pricing_dict["POST_6X6_PT"] > 0


def test_load_assemblies():
    """Test loading assemblies CSV."""
    assemblies_df = pricing.load_assemblies()
    
    assert len(assemblies_df) > 0
    assert "assembly_name" in assemblies_df.columns


def test_find_assembly_mapping():
    """Test finding assembly mapping."""
    assemblies_df = pricing.load_assemblies()
    
    # Test finding an existing assembly
    mapping = pricing.find_assembly_mapping(assemblies_df, "ROOF-STANDARD")
    assert mapping is not None
    assert "part_id" in mapping
    assert "waste_factor" in mapping
    
    # Test non-existent assembly
    mapping = pricing.find_assembly_mapping(assemblies_df, "NONEXISTENT")
    assert mapping is None


def test_find_part_record():
    """Test finding part record."""
    parts_df = pricing.load_parts()
    
    part_record = pricing.find_part_record(parts_df, "POST_6X6_PT")
    assert part_record is not None
    assert part_record["part_id"] == "POST_6X6_PT"
    assert "part_name" in part_record
    
    # Test non-existent part
    part_record = pricing.find_part_record(parts_df, "NONEXISTENT")
    assert part_record is None


def test_find_unit_price():
    """Test finding unit price."""
    pricing_df = pricing.load_pricing()
    
    unit_price = pricing.find_unit_price(pricing_df, "POST_6X6_PT")
    assert unit_price is not None
    assert unit_price > 0
    
    # Test non-existent part
    unit_price = pricing.find_unit_price(pricing_df, "NONEXISTENT")
    assert unit_price is None


def test_price_material_takeoff():
    """Test pricing a material takeoff."""
    # Create a simple takeoff
    takeoff = MaterialTakeoff(items=[
        AssemblyQuantity(
            name="posts",
            description="Structural posts",
            category="framing",
            quantity=10.0,
            unit="ea",
        ),
        AssemblyQuantity(
            name="roof_panels",
            description="Roof panels",
            category="roof",
            quantity=1000.0,
            unit="sqft",
        ),
    ])
    
    pricing_inputs = PricingInputs(
        material_markup=1.15,  # 15% markup
        tax_rate=0.08,  # 8% tax
        labor_rate=50.0,  # Default labor rate
    )
    
    parts_df = pricing.load_parts()
    pricing_df = pricing.load_pricing()
    assemblies_df = pricing.load_assemblies()
    
    priced_items, summary = pricing.price_material_takeoff(
        takeoff, pricing_inputs, parts_df, pricing_df, assemblies_df
    )
    
    # Should have priced items
    assert len(priced_items) == 2
    
    # Check posts item
    posts_item = next((item for item in priced_items if item.name == "posts"), None)
    assert posts_item is not None
    # Posts have waste_factor 1.0, so effective quantity = 10.0
    assert posts_item.quantity == pytest.approx(10.0)
    assert posts_item.unit == "ea"
    assert posts_item.material_cost > 0
    assert posts_item.total_cost > 0
    
    # Check roof panels item
    roof_item = next((item for item in priced_items if item.name == "roof_panels"), None)
    assert roof_item is not None
    # Roof panels have waste_factor 1.05, so effective quantity = 1000 * 1.05 = 1050
    assert roof_item.quantity == pytest.approx(1050.0)
    assert roof_item.unit == "sqft"
    assert roof_item.material_cost > 0
    assert roof_item.total_cost > 0
    
    # Check summary
    assert summary.material_subtotal > 0
    assert summary.markup_total > 0
    assert summary.tax_total > 0
    assert summary.grand_total > 0
    
    # Verify totals match
    calculated_material = sum(item.material_cost for item in priced_items)
    calculated_markup = sum(item.markup_amount for item in priced_items)
    assert summary.material_subtotal == pytest.approx(calculated_material)
    assert summary.markup_total == pytest.approx(calculated_markup)


def test_price_material_takeoff_with_markup():
    """Test that markup is applied correctly (ONLY to material, not labor - per changelog entry [4])."""
    takeoff = MaterialTakeoff(items=[
        AssemblyQuantity(
            name="roof_panels",
            description="Roof panels",
            category="roof",
            quantity=100.0,
            unit="sqft",
        ),
    ])
    
    # 20% markup
    pricing_inputs = PricingInputs(
        material_markup=1.20,
        tax_rate=0.0,
        labor_rate=50.0,  # Non-zero labor rate to verify markup doesn't apply to labor
    )
    
    parts_df = pricing.load_parts()
    pricing_df = pricing.load_pricing()
    assemblies_df = pricing.load_assemblies()
    
    priced_items, summary = pricing.price_material_takeoff(
        takeoff, pricing_inputs, parts_df, pricing_df, assemblies_df
    )
    
    item = priced_items[0]
    # Markup should be 20% of material cost ONLY, not labor
    expected_markup = item.material_cost * 0.20
    assert item.markup_percent == pytest.approx(20.0)
    assert item.markup_amount == pytest.approx(expected_markup)
    # Total cost = material + labor + markup (markup does NOT include labor)
    assert item.total_cost == pytest.approx(item.material_cost + item.labor_cost + item.markup_amount)
    
    # Verify markup is NOT applied to labor
    # If markup included labor, it would be: (material + labor) * 0.20
    # But it should be: material * 0.20
    markup_with_labor = (item.material_cost + item.labor_cost) * 0.20
    assert item.markup_amount < markup_with_labor  # Should be less if labor > 0


def test_price_material_takeoff_with_waste_factor():
    """Test that waste_factor is applied to quantities."""
    takeoff = MaterialTakeoff(items=[
        AssemblyQuantity(
            name="roof_panels",
            description="Roof panels",
            category="roof",
            quantity=100.0,  # Base quantity
            unit="sqft",
        ),
    ])
    
    pricing_inputs = PricingInputs(
        material_markup=1.0,  # No markup for simplicity
        tax_rate=0.0,
        labor_rate=0.0,  # No labor for this test
    )
    
    parts_df = pricing.load_parts()
    pricing_df = pricing.load_pricing()
    assemblies_df = pricing.load_assemblies()
    
    priced_items, summary = pricing.price_material_takeoff(
        takeoff, pricing_inputs, parts_df, pricing_df, assemblies_df
    )
    
    item = priced_items[0]
    # Waste factor for roof_panels should be 1.05 (5% waste)
    # So effective quantity should be 100 * 1.05 = 105
    assert item.quantity == pytest.approx(105.0)  # 100 * 1.05
    # Unit price is 1.16, so material cost should be 105 * 1.16 = 121.80
    assert item.material_cost == pytest.approx(105.0 * 1.16)


def test_price_material_takeoff_with_labor():
    """Test that labor_per_unit is used to calculate labor costs."""
    takeoff = MaterialTakeoff(items=[
        AssemblyQuantity(
            name="posts",
            description="Posts",
            category="framing",
            quantity=10.0,
            unit="ea",
        ),
    ])
    
    pricing_inputs = PricingInputs(
        material_markup=1.0,
        tax_rate=0.0,
        labor_rate=50.0,  # $50/hour
    )
    
    parts_df = pricing.load_parts()
    pricing_df = pricing.load_pricing()
    assemblies_df = pricing.load_assemblies()
    
    priced_items, summary = pricing.price_material_takeoff(
        takeoff, pricing_inputs, parts_df, pricing_df, assemblies_df
    )
    
    item = priced_items[0]
    # Labor per unit for posts is 0.25 hours/post
    # Waste factor is 1.0, so effective quantity = 10
    # Labor hours = 10 * 0.25 = 2.5 hours
    # Labor cost = 2.5 * 50 = $125
    assert item.labor_hours == pytest.approx(2.5)
    assert item.labor_cost == pytest.approx(125.0)
    assert item.labor_rate == 50.0


def test_price_material_takeoff_with_tax():
    """Test that tax is calculated correctly."""
    takeoff = MaterialTakeoff(items=[
        AssemblyQuantity(
            name="roof_panels",
            description="Roof panels",
            category="roof",
            quantity=100.0,
            unit="sqft",
        ),
    ])
    
    # 10% tax
    pricing_inputs = PricingInputs(
        material_markup=1.0,  # No markup
        tax_rate=0.10,  # 10% tax
        labor_rate=0.0,
    )
    
    parts_df = pricing.load_parts()
    pricing_df = pricing.load_pricing()
    assemblies_df = pricing.load_assemblies()
    
    priced_items, summary = pricing.price_material_takeoff(
        takeoff, pricing_inputs, parts_df, pricing_df, assemblies_df
    )
    
    # Tax should be 10% of (material + markup)
    expected_tax = (summary.material_subtotal + summary.markup_total) * 0.10
    assert summary.tax_total == pytest.approx(expected_tax)
    assert summary.grand_total == pytest.approx(
        summary.material_subtotal + summary.markup_total + summary.tax_total
    )


def test_price_material_takeoff_with_labor():
    """Test that labor costs are calculated when labor_per_unit is set."""
    # Note: Current assemblies CSV doesn't have labor_per_unit,
    # so this tests the structure but labor will be 0
    takeoff = MaterialTakeoff(items=[
        AssemblyQuantity(
            name="roof_panels",
            description="Roof panels",
            category="roof",
            quantity=100.0,
            unit="sqft",
        ),
    ])
    
    pricing_inputs = PricingInputs(
        material_markup=1.0,
        tax_rate=0.0,
        labor_rate=50.0,  # $50/hour
    )
    
    parts_df = pricing.load_parts()
    pricing_df = pricing.load_pricing()
    assemblies_df = pricing.load_assemblies()
    
    priced_items, summary = pricing.price_material_takeoff(
        takeoff, pricing_inputs, parts_df, pricing_df, assemblies_df
    )
    
    # Labor should be 0 since assemblies CSV doesn't specify labor_per_unit
    assert summary.labor_subtotal == 0.0


def test_price_material_takeoff_missing_part():
    """Test handling of missing part mappings."""
    takeoff = MaterialTakeoff(items=[
        AssemblyQuantity(
            name="nonexistent_assembly",
            description="Non-existent assembly",
            category="other",
            quantity=10.0,
            unit="ea",
        ),
    ])
    
    pricing_inputs = PricingInputs(
        material_markup=1.0,
        tax_rate=0.0,
        labor_rate=0.0,
    )
    
    parts_df = pricing.load_parts()
    pricing_df = pricing.load_pricing()
    assemblies_df = pricing.load_assemblies()
    
    priced_items, summary = pricing.price_material_takeoff(
        takeoff, pricing_inputs, parts_df, pricing_df, assemblies_df
    )
    
    # Should still create a priced item, but with 0 cost
    assert len(priced_items) == 1
    item = priced_items[0]
    assert item.unit_price == 0.0
    assert item.material_cost == 0.0
    assert item.total_cost == 0.0
    assert item.notes is not None  # Should have a note about missing mapping


def test_assemblies_csv_schema():
    """Test that assemblies CSV has the expected schema."""
    assemblies_df = pricing.load_assemblies()
    
    # Check for required columns
    assert "assembly_name" in assemblies_df.columns
    assert "category" in assemblies_df.columns
    assert "part_id" in assemblies_df.columns
    assert "waste_factor" in assemblies_df.columns
    assert "labor_per_unit" in assemblies_df.columns
    
    # Check that we have mappings for key assemblies
    assembly_names = assemblies_df["assembly_name"].tolist()
    assert "posts" in assembly_names
    assert "roof_panels" in assembly_names
    assert "sidewall_panels" in assembly_names
    
    # Check that waste_factor values are reasonable
    waste_factors = assemblies_df["waste_factor"].tolist()
    assert all(1.0 <= wf <= 1.20 for wf in waste_factors)  # Waste should be 0-20%
    
    # Check that labor_per_unit values are reasonable
    labor_values = assemblies_df["labor_per_unit"].tolist()
    assert all(0.0 <= lv <= 1.0 for lv in labor_values)  # Labor should be reasonable hours

```

---

### File: tests/test_end_to_end.py

```python
"""End-to-end tests for the pole barn calculator."""

import pytest
from systems.pole_barn.model import (
    PoleBarnInputs,
    GeometryInputs,
    MaterialInputs,
    PricingInputs,
    AssemblyInputs,
)
from systems.pole_barn.calculator import PoleBarnCalculator
from systems.pole_barn import geometry
from systems.pole_barn import assemblies
from pathlib import Path


def test_calculator_initialization():
    """Test that PoleBarnCalculator can be initialized."""
    geometry = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=0.0,
        overhang_rear=0.0,
        overhang_sides=0.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=8.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    materials = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=2.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
    )
    
    pricing = PricingInputs(
        material_markup=1.15,
        tax_rate=0.08,
        labor_rate=50.0,
    )
    
    assemblies = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    inputs = PoleBarnInputs(
        geometry=geometry,
        materials=materials,
        pricing=pricing,
        assemblies=assemblies,
        project_name="Test Barn",
    )
    
    calculator = PoleBarnCalculator(inputs)
    assert calculator.inputs == inputs
    assert calculator.inputs.project_name == "Test Barn"


def test_calculator_methods_not_implemented():
    """Test that calculator methods raise NotImplementedError."""
    geometry = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=0.0,
        overhang_rear=0.0,
        overhang_sides=0.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=8.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    materials = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=2.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
    )
    
    pricing = PricingInputs(
        material_markup=1.15,
        tax_rate=0.08,
        labor_rate=50.0,
    )
    
    assemblies = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    inputs = PoleBarnInputs(
        geometry=geometry,
        materials=materials,
        pricing=pricing,
        assemblies=assemblies,
    )
    
    calculator = PoleBarnCalculator(inputs)
    
    with pytest.raises(NotImplementedError):
        calculator.calculate_geometry()
    
    with pytest.raises(NotImplementedError):
        calculator.calculate_quantities()
    
    with pytest.raises(NotImplementedError):
        calculator.calculate_costs()
    
    with pytest.raises(NotImplementedError):
        calculator.calculate_all()
    
    with pytest.raises(NotImplementedError):
        calculator.get_summary()


def test_geometry_with_pole_barn_inputs():
    """Test that geometry calculations work with PoleBarnInputs."""
    geometry_inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,  # 4:12 pitch
        overhang_front=1.0,
        overhang_rear=1.0,
        overhang_sides=1.0,
        door_count=2,
        door_width=12.0,
        door_height=10.0,
        window_count=4,
        window_width=3.0,
        window_height=2.0,
        pole_spacing_length=10.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    materials = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=2.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
    )
    
    pricing = PricingInputs(
        material_markup=1.15,
        tax_rate=0.08,
        labor_rate=50.0,
    )
    
    assemblies = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    inputs = PoleBarnInputs(
        geometry=geometry_inputs,
        materials=materials,
        pricing=pricing,
        assemblies=assemblies,
        project_name="Test Barn",
    )
    
    # Test that we can build geometry model from PoleBarnInputs
    model = geometry.build_geometry_model(inputs.geometry)
    
    assert model.overall_length_ft == 40.0
    assert model.overall_width_ft == 30.0
    assert model.num_bays == 4  # ceil(40/10) = 4
    assert model.footprint_area_sqft == pytest.approx(1200.0)  # 40 * 30
    
    # Test that geometry summary works
    summary = geometry.get_geometry_summary(inputs.geometry)
    assert 'areas' in summary
    assert summary['areas']['footprint_sqft'] == pytest.approx(1200.0)
    
    # Test door/window openings
    openings = geometry.calculate_door_window_openings(inputs.geometry)
    assert openings['door_area'] == pytest.approx(240.0)  # 2 * 12 * 10
    assert openings['window_area'] == pytest.approx(24.0)  # 4 * 3 * 2


def test_assemblies_with_pole_barn_inputs():
    """Test that assembly calculations work with PoleBarnInputs."""
    geometry_inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,  # 4:12 pitch
        overhang_front=1.0,
        overhang_rear=1.0,
        overhang_sides=1.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=10.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    materials = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
    )
    
    pricing = PricingInputs(
        material_markup=1.15,
        tax_rate=0.08,
        labor_rate=50.0,
    )
    
    assemblies_input = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    inputs = PoleBarnInputs(
        geometry=geometry_inputs,
        materials=materials,
        pricing=pricing,
        assemblies=assemblies_input,
        project_name="Test Barn",
    )
    
    # Build geometry model
    geom_model = geometry.build_geometry_model(inputs.geometry)
    
    # Calculate material quantities
    quantities = assemblies.calculate_material_quantities(
        geom_model, inputs.materials, inputs.assemblies
    )
    
    # Should have multiple items
    assert len(quantities) > 0
    
    # Check for key items
    names = {item.name for item in quantities}
    assert "posts" in names
    assert "trusses" in names
    assert "roof_panels" in names
    assert "sidewall_panels" in names
    
    # Test assembly summary
    summary = assemblies.get_assembly_summary(inputs)
    assert summary["total_items"] > 0
    assert "by_category" in summary
    
    # Test that quantities are reasonable
    posts_item = next((item for item in quantities if item.name == "posts"), None)
    assert posts_item is not None
    assert posts_item.quantity > 0
    assert posts_item.unit == "ea"


def test_full_calculator_pipeline():
    """Test the complete calculator pipeline from inputs to costs."""
    geometry_inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=1.0,
        overhang_rear=1.0,
        overhang_sides=1.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=10.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    materials = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
    )
    
    pricing_inputs = PricingInputs(
        labor_rate=50.0,
        material_markup=1.15,  # 15% markup
        tax_rate=0.08,  # 8% tax
    )
    
    assemblies_input = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    inputs = PoleBarnInputs(
        geometry=geometry_inputs,
        materials=materials,
        pricing=pricing_inputs,
        assemblies=assemblies_input,
        project_name="Test Barn",
    )
    
    # Create calculator and run full calculation
    calculator = PoleBarnCalculator(inputs)
    calculator.load_config()
    
    geom_model, takeoff, priced_items, summary = calculator.calculate()
    
    # Verify geometry
    assert geom_model is not None
    assert geom_model.overall_length_ft == 40.0
    assert geom_model.overall_width_ft == 30.0
    
    # Verify quantities
    assert len(takeoff.items) > 0
    assert any(item.name == "posts" for item in takeoff.items)
    assert any(item.name == "roof_panels" for item in takeoff.items)
    
    # Verify pricing
    assert len(priced_items) > 0
    assert summary.material_subtotal > 0
    assert summary.grand_total > 0
    
    # Verify totals are consistent
    calculated_material = sum(item.material_cost for item in priced_items)
    assert summary.material_subtotal == pytest.approx(calculated_material)
    
    # Verify grand total includes all components
    expected_total = (
        summary.material_subtotal +
        summary.labor_subtotal +
        summary.markup_total +
        summary.tax_total
    )
    assert summary.grand_total == pytest.approx(expected_total)


def test_calculator_summary():
    """Test calculator summary method."""
    geometry_inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=0.0,
        overhang_rear=0.0,
        overhang_sides=0.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=10.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    materials = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
    )
    
    pricing_inputs = PricingInputs(
        labor_rate=50.0,
        material_markup=1.15,
        tax_rate=0.08,
    )
    
    assemblies_input = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    inputs = PoleBarnInputs(
        geometry=geometry_inputs,
        materials=materials,
        pricing=pricing_inputs,
        assemblies=assemblies_input,
        project_name="Summary Test",
    )
    
    calculator = PoleBarnCalculator(inputs)
    calculator.load_config()
    
    summary = calculator.get_summary()
    
    assert "geometry" in summary
    assert "quantities" in summary
    assert "costs" in summary
    assert summary["costs"]["grand_total"] > 0
    assert summary["project_name"] == "Summary Test"

```

---


## End of Export
