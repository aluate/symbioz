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
        overhead_total=overhead_total,
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
