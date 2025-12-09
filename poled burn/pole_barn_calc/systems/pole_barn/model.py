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
    overhead_total: float = 0.0  # Overhead applied at summary level (moved to end for dataclass ordering)


@dataclass
class PartQuantity:
    """A single part quantity in the BOM."""
    
    part_id: str
    part_name: str
    category: str
    export_category: str  # For Excel tab grouping
    unit: str
    qty: float
    unit_price: float
    ext_price: float
    length_in: Optional[float] = None  # For panels, lumber, etc. (length in inches)
    sheet_name: Optional[str] = None  # Logical "tab" name for CSV export
    notes: str = ""


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

