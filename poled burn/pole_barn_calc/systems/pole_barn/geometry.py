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
