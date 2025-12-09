"""BOM (Bill of Materials) expansion and calculations."""

import math
from typing import List, Dict, Any, Optional, Tuple
import pandas as pd
from .model import (
    MaterialTakeoff,
    AssemblyQuantity,
    PartQuantity,
    GeometryModel,
    GeometryInputs,
)


def generate_gable_panel_lengths(
    eave_height_ft: float,
    roof_pitch_ratio: float,  # e.g. 4/12 = 0.3333...
    building_width_ft: float,
    panel_coverage_width_ft: float = 3.0,
    extra_inches: float = 2.0,
) -> Dict[float, int]:
    """
    Generate panel lengths for a gable end wall.
    
    Returns a mapping {panel_length_in: quantity} for a single gable end.
    Assumes a symmetric gable roof, ridge at building_width_ft / 2.
    Quantity per length is per gable; caller can double for both ends.
    
    Algorithm:
    - For each panel position from eave toward ridge:
      - Calculate horizontal distance from eave
      - Calculate height at inner edge of panel
      - Panel length = height + extra_inches, rounded up to nearest 1"
      - Quantity = 2 (left and right sides)
    
    Args:
        eave_height_ft: Eave height in feet
        roof_pitch_ratio: Roof pitch as ratio (e.g., 4/12 = 0.3333...)
        building_width_ft: Building width (gable span) in feet
        panel_coverage_width_ft: Panel coverage width in feet (default 3.0 for 36")
        extra_inches: Extra length in inches above highest point (default 2.0)
        
    Returns:
        Dictionary mapping panel_length_in (inches) to quantity (per gable end)
    """
    half_span_ft = building_width_ft / 2.0
    length_counts: Dict[float, int] = {}
    
    n = 0
    while (n + 1) * panel_coverage_width_ft <= half_span_ft + 0.01:  # Small tolerance for floating point
        x_inner_ft = min((n + 1) * panel_coverage_width_ft, half_span_ft)
        height_inner_ft = eave_height_ft + roof_pitch_ratio * x_inner_ft
        panel_length_ft = height_inner_ft + extra_inches / 12.0
        
        # Convert to inches and round UP to nearest 1"
        panel_length_in = math.ceil(panel_length_ft * 12.0)
        
        # Add to dict (quantity = 2 for left/right)
        if panel_length_in in length_counts:
            length_counts[panel_length_in] += 2
        else:
            length_counts[panel_length_in] = 2
        
        n += 1
    
    return length_counts


def pack_segments_into_sticks(
    segments_in: List[float],
    stock_length_in: float = 120.0,
) -> int:
    """
    Pack J-channel segments into 10' stock sticks.
    
    Uses a greedy algorithm:
    - Sort segments descending by length
    - For each segment, try to fit it into an existing stick
    - If none fits, open a new stick
    
    Never underestimates: if a segment is exactly equal to remaining length, it fits.
    Assumes all segments_in values are <= stock_length_in.
    
    Args:
        segments_in: List of required segment lengths in inches
        stock_length_in: Stock stick length in inches (default 120" = 10')
        
    Returns:
        Number of stock sticks required
    """
    if not segments_in:
        return 0
    
    # Sort descending (longest first)
    segments = sorted(segments_in, reverse=True)
    
    # Track remaining length in each stick
    sticks: List[float] = []
    
    for segment in segments:
        if segment > stock_length_in:
            # This shouldn't happen, but handle gracefully
            # Open a new stick for this oversized segment
            sticks.append(stock_length_in - segment)
            continue
        
        # Try to fit into an existing stick
        fitted = False
        for i, remaining in enumerate(sticks):
            if remaining >= segment:
                # Fits! Use this stick
                sticks[i] = remaining - segment
                fitted = True
                break
        
        if not fitted:
            # Need a new stick
            sticks.append(stock_length_in - segment)
    
    return len(sticks)


def calculate_eave_top_j_segments(
    length_ft: float,
    has_side_overhang: bool,
) -> List[float]:
    """
    Calculate J-channel segments for the tops of eave walls.
    
    Returns a list of segment lengths in inches.
    For now, treat as a single bulk segment (2 * length_ft * 12 inches).
    The packing algorithm will break it into 10' sticks.
    
    Args:
        length_ft: Building length in feet (eave wall length)
        has_side_overhang: Whether there is a side overhang (requires J at eave top)
        
    Returns:
        List of segment lengths in inches (empty if no overhang)
    """
    if not has_side_overhang:
        return []
    
    # Total J needed along both eave walls
    total_inches = 2 * length_ft * 12.0
    
    # Return as a single segment (packing will break it into sticks)
    return [total_inches]


def calculate_opening_j_segments(
    door_count: int,
    door_width_ft: float,
    door_height_ft: float,
    window_count: int,
    window_width_ft: float,
    window_height_ft: float,
    door_fudge_in: float = 2.0,
    window_fudge_in: float = 2.0,
) -> List[float]:
    """
    Calculate J-channel segment lengths for doors and windows.
    
    Doors: J on two legs + one head (no bottom).
    Windows: J all the way around (4 sides).
    
    Each segment must come from a single 10' stick (no splicing within one piece).
    Offcuts can be reused for smaller segments.
    
    Args:
        door_count: Number of doors
        door_width_ft: Door width in feet
        door_height_ft: Door height in feet
        window_count: Number of windows
        window_width_ft: Window width in feet
        window_height_ft: Window height in feet
        door_fudge_in: Extra length per door segment (default 2")
        window_fudge_in: Extra length per window segment (default 2")
        
    Returns:
        Flat list of segment lengths in inches
    """
    segments: List[float] = []
    
    # Door segments
    for _ in range(door_count):
        # Two legs (vertical)
        leg_length = door_height_ft * 12.0 + door_fudge_in
        segments.append(leg_length)
        segments.append(leg_length)
        
        # One head (horizontal)
        head_length = door_width_ft * 12.0 + door_fudge_in
        segments.append(head_length)
    
    # Window segments
    for _ in range(window_count):
        # Two vertical sides
        vertical_length = window_height_ft * 12.0 + window_fudge_in
        segments.append(vertical_length)
        segments.append(vertical_length)
        
        # Two horizontal sides (top and bottom)
        horizontal_length = window_width_ft * 12.0 + window_fudge_in
        segments.append(horizontal_length)
        segments.append(horizontal_length)
    
    return segments


def split_lumber_into_stock_lengths(
    total_lf: float,
    stock_lengths_ft: Optional[List[float]] = None,
) -> Dict[float, int]:
    """
    Split total linear feet into stock length breakdown.
    
    Uses a greedy algorithm: use longest length as much as possible, then shorter ones.
    Always rounds up so we never under-order.
    
    Args:
        total_lf: Total linear feet required
        stock_lengths_ft: Available stock lengths in feet (default: [16, 14, 12, 10, 8])
        
    Returns:
        Dictionary mapping length_ft to count (number of pieces)
    """
    if stock_lengths_ft is None:
        stock_lengths_ft = [16.0, 14.0, 12.0, 10.0, 8.0]
    
    # Sort descending (longest first)
    stock_lengths_ft = sorted(stock_lengths_ft, reverse=True)
    
    remaining_lf = total_lf
    length_counts: Dict[float, int] = {}
    
    # Greedy: use longest length as much as possible
    for length_ft in stock_lengths_ft:
        if remaining_lf <= 0:
            break
        
        # How many pieces of this length can we use?
        pieces = math.ceil(remaining_lf / length_ft)
        length_counts[length_ft] = pieces
        
        # Subtract what we've accounted for
        remaining_lf -= pieces * length_ft
    
    # If there's still remaining (shouldn't happen with 8ft minimum, but safety check)
    if remaining_lf > 0:
        # Use shortest length for remainder
        shortest = min(stock_lengths_ft)
        extra_pieces = math.ceil(remaining_lf / shortest)
        if shortest in length_counts:
            length_counts[shortest] += extra_pieces
        else:
            length_counts[shortest] = extra_pieces
    
    return length_counts


def expand_to_parts(
    material_takeoff: MaterialTakeoff,
    assemblies_df: pd.DataFrame,
    parts_df: pd.DataFrame,
    pricing_df: pd.DataFrame,
    geometry_model: Optional[GeometryModel] = None,
    geometry_inputs: Optional[GeometryInputs] = None,
) -> List[PartQuantity]:
    """
    Expand assembly quantities into part quantities (BOM).
    
    Now handles:
    - Gable panel length breakdown (multiple lengths per part_id)
    - Lumber stock length packing (multiple lengths per part_id)
    - Panel units fixed (sqft → ea with per-panel pricing)
    - Sheathing, concrete, overhead doors
    
    Args:
        material_takeoff: Material takeoff with assembly-level quantities
        assemblies_df: DataFrame with assembly mappings
        parts_df: DataFrame with parts catalog
        pricing_df: DataFrame with pricing data
        geometry_model: Optional geometry model for dimensions
        geometry_inputs: Optional geometry inputs for roof pitch/style
        
    Returns:
        List of PartQuantity items (normalized BOM, may have multiple rows per part_id with different lengths)
    """
    bom_items: List[PartQuantity] = []
    
    # Dictionary keyed by (part_id, length_in) for length-based items
    # For non-length items, length_in = None
    part_quantities: Dict[Tuple[str, Optional[float]], float] = {}
    
    # Process each assembly quantity
    for assembly_qty in material_takeoff.items:
        # Find all part mappings for this assembly
        assembly_mappings = assemblies_df[assemblies_df["assembly_name"] == assembly_qty.name]
        
        if assembly_mappings.empty:
            continue
        
        for _, mapping in assembly_mappings.iterrows():
            part_id = mapping.get("part_id")
            if not part_id or pd.isna(part_id):
                continue
            
            quantity_multiplier = float(mapping.get("quantity_multiplier", 1.0))
            waste_factor = float(mapping.get("waste_factor", 1.0))
            
            # Base quantity from assembly
            base_qty = assembly_qty.quantity * quantity_multiplier
            
            # Get part record
            part_record = parts_df[parts_df["part_id"] == part_id]
            if part_record.empty:
                continue
            
            part_row = part_record.iloc[0]
            coverage_width = part_row.get("coverage_width_in")
            coverage_height = part_row.get("coverage_height_in")
            unit = part_row.get("unit", "")
            category = part_row.get("category", "")
            
            # Handle gable endwall panels with length breakdown
            if ("endwall" in assembly_qty.name.lower() and 
                "panel" in part_id.lower() and 
                geometry_model and 
                geometry_inputs and
                geometry_inputs.roof_style == "gable" and
                coverage_width is not None):
                
                # Generate gable panel lengths
                panel_coverage_width_ft = float(coverage_width) / 12.0
                gable_lengths = generate_gable_panel_lengths(
                    eave_height_ft=geometry_model.eave_height_ft,
                    roof_pitch_ratio=geometry_inputs.roof_pitch,
                    building_width_ft=geometry_model.overall_width_ft,
                    panel_coverage_width_ft=panel_coverage_width_ft,
                    extra_inches=2.0,
                )
                
                # Apply waste factor to quantities, then round to whole integers
                for length_in, qty in gable_lengths.items():
                    # Multiply by waste factor, then round up to ensure whole panels
                    effective_qty = math.ceil(qty * waste_factor)
                    key = (part_id, length_in)
                    if key in part_quantities:
                        part_quantities[key] += effective_qty
                    else:
                        part_quantities[key] = effective_qty
                continue
            
            # Handle sidewall/roof panels (constant length, no breakdown needed for now)
            # Note: Gable endwall panels are handled separately above
            if ("panel" in part_id.lower() or "panel" in assembly_qty.name.lower()) and coverage_width is not None:
                # Skip if this is an endwall panel (already handled with length breakdown)
                if "endwall" in assembly_qty.name.lower():
                    continue
                
                # Convert area to piece count
                length_ft = None
                height_ft = None
                
                if geometry_model:
                    if "sidewall" in assembly_qty.name.lower():
                        # Sidewall panels: count by width coverage along length
                        # Each panel runs full height (vertical installation)
                        length_ft = geometry_model.overall_length_ft
                        height_ft = geometry_model.eave_height_ft
                    elif "roof" in assembly_qty.name.lower():
                        # Roof panels: count by width coverage along length
                        length_ft = geometry_model.overall_length_ft
                
                # Calculate panel count based on width coverage ONLY (geometry-based, not area-based)
                coverage_ft = float(coverage_width) / 12.0
                if length_ft:
                    # Number of panels = length / coverage width (rounded up)
                    # This is geometry-based, not area-based
                    num_panels = math.ceil(length_ft / coverage_ft)
                    # Apply waste factor, then round up to whole integer
                    num_panels = math.ceil(num_panels * waste_factor)
                else:
                    # If we can't determine length from geometry, we should not be here
                    # But as a safety fallback, use the base quantity as a count (not area)
                    # This should rarely happen if geometry is correct
                    num_panels = math.ceil(base_qty * waste_factor)
                
                # Use constant length (eave height for sidewalls, or calculated for roof)
                length_in = None
                if geometry_model and "sidewall" in assembly_qty.name.lower():
                    length_in = geometry_model.eave_height_ft * 12.0  # Panel length = wall height
                elif geometry_model and "roof" in assembly_qty.name.lower():
                    # Roof panels: approximate length based on slope
                    if geometry_inputs:
                        slope_factor = math.sqrt(1 + geometry_inputs.roof_pitch ** 2)
                        # Approximate: half width × slope factor
                        length_in = (geometry_model.overall_width_ft / 2.0) * slope_factor * 12.0
                
                key = (part_id, length_in)
                if key in part_quantities:
                    part_quantities[key] += num_panels
                else:
                    part_quantities[key] = num_panels
                continue
            
            # Handle sheathing (4x8 sheets)
            if ("sheathing" in part_id.lower() or "sheathing" in assembly_qty.name.lower()) and coverage_width and coverage_height:
                sheet_width_ft = float(coverage_width) / 12.0
                sheet_height_ft = float(coverage_height) / 12.0
                sheet_area_sqft = sheet_width_ft * sheet_height_ft
                # Convert area to sheet count, apply waste, round up to whole sheets
                num_sheets = math.ceil((base_qty / sheet_area_sqft) * waste_factor)
                
                # Sheathing is always 4x8, so length_in = 96"
                length_in = float(coverage_height)  # 96" for 4x8
                # Note: unit will be changed to "ea" in the final PartQuantity build step
                key = (part_id, length_in)
                if key in part_quantities:
                    part_quantities[key] += num_sheets
                else:
                    part_quantities[key] = num_sheets
                continue
            
            # Handle J-channel - pack segments into 10' sticks
            # Check assembly quantity unit, not part unit
            if assembly_qty.name == "j_channel" and assembly_qty.unit == "in" and geometry_inputs:
                # Recalculate segments to do proper packing
                j_segments: List[float] = []
                
                # Eave-top J (if side overhang exists)
                has_side_overhang = geometry_inputs.overhang_sides > 0
                if has_side_overhang and geometry_model:
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
                
                # Validate segments don't exceed stock length
                stock_length_in = 120.0
                for seg in j_segments:
                    if seg > stock_length_in:
                        # This shouldn't happen, but log a warning
                        # For now, we'll just cap it (proper fix would be to handle oversized segments)
                        pass
                
                # Pack segments into sticks
                if j_segments:
                    stick_count = pack_segments_into_sticks(j_segments, stock_length_in)
                    
                    key = (part_id, stock_length_in)
                    if key in part_quantities:
                        part_quantities[key] += stick_count
                    else:
                        part_quantities[key] = stick_count
                continue
            
            # Handle lumber (2x4, 2x6, etc.) - split into stock lengths
            # Apply to ALL framing lumber, not just specific items
            if unit == "lf" and (category == "framing" or "framing" in category.lower() or 
                                  "girt" in assembly_qty.name.lower() or 
                                  "purlin" in assembly_qty.name.lower() or
                                  "door_framing" in assembly_qty.name.lower() or
                                  "window_framing" in assembly_qty.name.lower()):
                total_lf = base_qty * waste_factor
                stock_lengths = split_lumber_into_stock_lengths(total_lf)
                
                for length_ft, count in stock_lengths.items():
                    length_in = length_ft * 12.0
                    key = (part_id, length_in)
                    if key in part_quantities:
                        part_quantities[key] += count
                    else:
                        part_quantities[key] = count
                continue
            
            # Default: accumulate by part_id only (no length breakdown)
            effective_qty = base_qty * waste_factor
            key = (part_id, None)
            if key in part_quantities:
                part_quantities[key] += effective_qty
            else:
                part_quantities[key] = effective_qty
    
    # Build PartQuantity items
    for (part_id, length_in), total_qty in part_quantities.items():
        # Get part record
        part_record = parts_df[parts_df["part_id"] == part_id]
        if part_record.empty:
            continue
        
        part_row = part_record.iloc[0]
        part_name = part_row.get("part_name", part_id)
        category = part_row.get("category", "Misc")
        export_category = part_row.get("export_category", "Misc")
        unit = part_row.get("unit", "ea")
        notes = part_row.get("notes", "")
        
        # Fix panel units: if it was sqft, change to ea
        if "panel" in part_id.lower() and unit == "sqft":
            unit = "ea"
        
        # Fix sheathing units: if it was sqft, change to ea (sheets)
        if "sheathing" in part_id.lower() and unit == "sqft":
            unit = "ea"
        
        # Get unit price
        price_record = pricing_df[pricing_df["part_id"] == part_id]
        unit_price = 0.0
        if not price_record.empty:
            unit_price = float(price_record.iloc[0].get("unit_price", 0.0))
            
            # If panel was priced per sqft, convert to per-panel
            if "panel" in part_id.lower() and unit == "ea":
                coverage_width = part_row.get("coverage_width_in")
                if coverage_width and not pd.isna(coverage_width):
                    # Approximate panel area (coverage width × typical length)
                    # For pricing, use a standard 12' panel length
                    panel_length_ft = 12.0  # Standard assumption
                    panel_width_ft = float(coverage_width) / 12.0
                    panel_area_sqft = panel_length_ft * panel_width_ft
                    # Convert sqft price to per-panel price
                    unit_price = unit_price * panel_area_sqft
        
        ext_price = total_qty * unit_price
        
        # Add length info to notes if present
        if length_in is not None:
            length_ft = length_in / 12.0
            if notes:
                notes = f"{notes}; Length: {length_ft:.1f}ft ({length_in:.0f}\")"
            else:
                notes = f"Length: {length_ft:.1f}ft ({length_in:.0f}\")"
        
        # Set sheet_name based on export_category (logical tab name)
        sheet_name = export_category if export_category else category
        
        bom_items.append(PartQuantity(
            part_id=part_id,
            part_name=part_name,
            category=category,
            export_category=export_category,
            unit=unit,
            qty=total_qty,
            unit_price=unit_price,
            ext_price=ext_price,
            length_in=length_in,
            sheet_name=sheet_name,
            notes=notes,
        ))
    
    return bom_items


def create_material_takeoff_from_bom(
    bom_items: List[PartQuantity],
) -> MaterialTakeoff:
    """
    Create a MaterialTakeoff from BOM items, aggregating by part_id and length.
    
    This ensures material_takeoff matches the BOM exactly, using the same
    packed quantities (sticks, sheets, stock lengths) rather than raw inches/sqft.
    
    Args:
        bom_items: List of PartQuantity items from BOM
        
    Returns:
        MaterialTakeoff with AssemblyQuantity items matching BOM structure
    """
    from .model import AssemblyQuantity, MaterialTakeoff
    
    # Aggregate by (part_id, length_in) to match BOM grouping
    aggregated: Dict[tuple, Dict[str, Any]] = {}
    
    for item in bom_items:
        key = (item.part_id, item.length_in)
        if key not in aggregated:
            aggregated[key] = {
                "name": item.part_id.lower().replace("_", " "),
                "description": item.part_name,
                "category": item.category,
                "quantity": 0.0,
                "unit": item.unit,
                "notes": item.notes or "",
            }
        
        aggregated[key]["quantity"] += item.qty
    
    # Convert to AssemblyQuantity items
    assembly_items = []
    for (part_id, length_in), data in aggregated.items():
        # Add length info to notes if present
        notes = data["notes"]
        if length_in is not None:
            length_ft = length_in / 12.0
            if notes:
                notes = f"{notes}; Length: {length_ft:.1f}ft"
            else:
                notes = f"Length: {length_ft:.1f}ft"
        
        assembly_items.append(AssemblyQuantity(
            name=data["name"],
            description=data["description"],
            category=data["category"],
            quantity=data["quantity"],
            unit=data["unit"],
            notes=notes,
        ))
    
    return MaterialTakeoff(items=assembly_items)
