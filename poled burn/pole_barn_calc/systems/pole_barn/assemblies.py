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
    
    # Wall and roof sheathing (per changelog entry [6], [7])
    sheathing_quantities = _calculate_sheathing_quantities(geometry_model, material_inputs)
    quantities.extend(sheathing_quantities)
    
    # Concrete slab (per changelog entry [8], [13])
    if geometry_inputs:
        concrete_quantities = _calculate_concrete_slab_quantities(geometry_model, material_inputs, geometry_inputs)
        quantities.extend(concrete_quantities)
    
    # Overhead doors (per changelog entry [17])
    if geometry_inputs:
        overhead_door_quantities = _calculate_overhead_door_quantities(geometry_inputs)
        quantities.extend(overhead_door_quantities)
    
    # J-channel trim (for metal panels with doors/windows/overhangs)
    if geometry_inputs and material_inputs.exterior_finish_type in ["metal_29ga", "metal_26ga"]:
        j_channel_quantities = _calculate_j_channel_quantities(
            geometry_model,
            material_inputs,
            geometry_inputs,
        )
        quantities.extend(j_channel_quantities)
    
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


def _calculate_sheathing_quantities(
    geometry_model: GeometryModel,
    material_inputs: MaterialInputs,
) -> List[AssemblyQuantity]:
    """
    Calculate wall and roof sheathing quantities (OSB or plywood).
    
    Args:
        geometry_model: Derived geometry
        material_inputs: Material specifications with sheathing types
        
    Returns:
        List of AssemblyQuantity items for sheathing
    """
    quantities: List[AssemblyQuantity] = []
    
    # Wall sheathing
    if material_inputs.wall_sheathing_type and material_inputs.wall_sheathing_type != "none":
        wall_sheathing_sqft = geometry_model.total_wall_area_sqft
        # TODO: Subtract door/window openings for more accuracy
        
        assembly_name = f"wall_sheathing_{material_inputs.wall_sheathing_type}"
        quantities.append(AssemblyQuantity(
            name=assembly_name,
            description=f"Wall sheathing ({material_inputs.wall_sheathing_type.upper()})",
            category="sheathing",
            quantity=wall_sheathing_sqft,
            unit="sqft",
            notes=f"{material_inputs.wall_sheathing_type.upper()} sheathing for walls",
        ))
    
    # Roof sheathing
    if material_inputs.roof_sheathing_type and material_inputs.roof_sheathing_type != "none":
        roof_sheathing_sqft = geometry_model.roof_area_sqft
        
        assembly_name = f"roof_sheathing_{material_inputs.roof_sheathing_type}"
        quantities.append(AssemblyQuantity(
            name=assembly_name,
            description=f"Roof sheathing ({material_inputs.roof_sheathing_type.upper()})",
            category="sheathing",
            quantity=roof_sheathing_sqft,
            unit="sqft",
            notes=f"{material_inputs.roof_sheathing_type.upper()} sheathing for roof",
        ))
    
    return quantities


def _calculate_concrete_slab_quantities(
    geometry_model: GeometryModel,
    material_inputs: MaterialInputs,
    geometry_inputs: 'GeometryInputs',
) -> List[AssemblyQuantity]:
    """
    Calculate concrete slab quantities (cubic yards and reinforcement).
    
    Args:
        geometry_model: Derived geometry
        material_inputs: Material specifications with slab details
        geometry_inputs: Geometry inputs for floor type
        
    Returns:
        List of AssemblyQuantity items for concrete slab
    """
    quantities: List[AssemblyQuantity] = []
    
    if material_inputs.floor_type == "slab":
        # Calculate cubic yards
        footprint_sqft = geometry_model.footprint_area_sqft
        thickness_ft = (material_inputs.slab_thickness_in or 4.0) / 12.0  # Default 4"
        volume_cuft = footprint_sqft * thickness_ft
        volume_cy = volume_cuft / 27.0  # Convert to cubic yards
        
        quantities.append(AssemblyQuantity(
            name="slab_concrete",
            description="Concrete for slab",
            category="concrete",
            quantity=volume_cy,
            unit="cuyd",
            notes=f"Slab: {footprint_sqft:.1f} sqft × {thickness_ft*12:.1f}\" thick",
        ))
        
        # Reinforcement
        if material_inputs.slab_reinforcement and material_inputs.slab_reinforcement != "none":
            if material_inputs.slab_reinforcement == "mesh":
                # Wire mesh: typically 5x10 or 6x6 sheets
                # Approximate: one sheet per 50 sqft
                mesh_sheets = math.ceil(footprint_sqft / 50.0)
                quantities.append(AssemblyQuantity(
                    name="slab_mesh",
                    description="Wire mesh for slab reinforcement",
                    category="concrete",
                    quantity=mesh_sheets,
                    unit="ea",
                    notes=f"Wire mesh sheets (5x10 or 6x6), ~50 sqft coverage per sheet",
                ))
            elif material_inputs.slab_reinforcement == "rebar":
                # Rebar: approximate grid pattern
                # Perimeter + interior grid (simplified)
                perimeter_ft = 2 * (geometry_model.overall_length_ft + geometry_model.overall_width_ft)
                # Interior grid: approximate based on spacing (assume 2' spacing)
                interior_lf = (geometry_model.overall_length_ft / 2.0) * (geometry_model.overall_width_ft / 2.0) * 2
                total_rebar_lf = perimeter_ft + interior_lf
                quantities.append(AssemblyQuantity(
                    name="slab_rebar",
                    description="Rebar for slab reinforcement",
                    category="concrete",
                    quantity=total_rebar_lf,
                    unit="lf",
                    notes=f"Rebar grid pattern, ~2' spacing",
                ))
    
    return quantities


def _calculate_overhead_door_quantities(
    geometry_inputs: 'GeometryInputs',
) -> List[AssemblyQuantity]:
    """
    Calculate overhead door quantities.
    
    Args:
        geometry_inputs: Geometry inputs with overhead door count and type
        
    Returns:
        List of AssemblyQuantity items for overhead doors
    """
    quantities: List[AssemblyQuantity] = []
    
    if geometry_inputs.overhead_door_count > 0 and geometry_inputs.overhead_door_type != "none":
        quantities.append(AssemblyQuantity(
            name="overhead_doors",
            description=f"Overhead doors ({geometry_inputs.overhead_door_type})",
            category="doors",
            quantity=float(geometry_inputs.overhead_door_count),
            unit="ea",
            notes=f"{geometry_inputs.overhead_door_type} overhead doors, 8' x 7' typical",
        ))
    
    return quantities


def _calculate_j_channel_quantities(
    geometry_model: GeometryModel,
    material_inputs: MaterialInputs,
    geometry_inputs: 'GeometryInputs',
) -> List[AssemblyQuantity]:
    """
    Calculate J-channel quantities for doors, windows, and eave tops.
    
    J-channel comes in 10' sticks (120"). Segments are calculated and will be
    packed into sticks in the BOM expansion phase.
    
    Args:
        geometry_model: Derived geometry
        material_inputs: Material specifications
        geometry_inputs: Geometry inputs with door/window counts and overhangs
        
    Returns:
        List of AssemblyQuantity items for J-channel (as total inches needed)
    """
    from .bom import (
        calculate_eave_top_j_segments,
        calculate_opening_j_segments,
    )
    
    quantities: List[AssemblyQuantity] = []
    
    # Collect all J-channel segments
    j_segments: List[float] = []
    
    # Eave-top J (if side overhang exists)
    has_side_overhang = geometry_inputs.overhang_sides > 0
    if has_side_overhang:
        eave_segments = calculate_eave_top_j_segments(
            length_ft=geometry_model.overall_length_ft,
            has_side_overhang=has_side_overhang,
        )
        j_segments.extend(eave_segments)
    
    # Door and window J
    if geometry_inputs.door_count > 0 or geometry_inputs.window_count > 0:
        opening_segments = calculate_opening_j_segments(
            door_count=geometry_inputs.door_count,
            door_width_ft=geometry_inputs.door_width,
            door_height_ft=geometry_inputs.door_height,
            window_count=geometry_inputs.window_count,
            window_width_ft=geometry_inputs.window_width,
            window_height_ft=geometry_inputs.window_height,
            door_fudge_in=2.0,
            window_fudge_in=2.0,
        )
        j_segments.extend(opening_segments)
    
    # If we have any segments, create an assembly quantity
    # The BOM expansion will pack these into sticks
    if j_segments:
        total_inches = sum(j_segments)
        quantities.append(AssemblyQuantity(
            name="j_channel",
            description="J-channel trim (doors, windows, eave tops)",
            category="trim",
            quantity=total_inches,
            unit="in",  # Will be converted to sticks in BOM expansion
            notes=f"J-channel segments: {len(j_segments)} pieces, total {total_inches:.1f}\"",
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
