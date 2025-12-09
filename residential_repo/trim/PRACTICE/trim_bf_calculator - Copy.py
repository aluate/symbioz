"""
Board Feet (BF) calculation module.
Reads trim dimensions and AWI waste chart from Excel files.
Converts lineal feet to board feet and applies waste factors.
"""

import os
import pandas as pd

# Cache for loaded Excel data
_trim_dimensions_df = None
_awi_waste_df = None


def load_trim_dimensions():
    """Load trim dimensions from Excel file"""
    global _trim_dimensions_df
    if _trim_dimensions_df is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        excel_path = os.path.join(script_dir, 'trim_dimensions.xlsx')
        _trim_dimensions_df = pd.read_excel(excel_path)
    return _trim_dimensions_df


def load_awi_waste_chart():
    """Load AWI waste chart from Excel file"""
    global _awi_waste_df
    if _awi_waste_df is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        excel_path = os.path.join(script_dir, 'awi_waste_chart.xlsx')
        _awi_waste_df = pd.read_excel(excel_path)
    return _awi_waste_df


def get_trim_dimensions(trim_style, trim_type, finish_level):
    """
    Get width and thickness for a trim piece.
    
    Args:
        trim_style: 'craftsman', 'craftsman_plus' (built_up), 'mitered', 'sill_apron_only'
        trim_type: 'base', 'casing', 'headers', 'sills', 'apron', 'jambs', 'dentils'
        finish_level: 'Economy', 'Standard', 'Luxury'
    
    Returns:
        tuple: (width_inches, thickness_inches) or (None, None) if not found
    """
    df = load_trim_dimensions()
    
    # Map our trim styles to Excel styles
    style_map = {
        'craftsman': 'CRAFTSMAN',
        'built_up': 'CRAFTSMAN PLUS',
        'craftsman_plus': 'CRAFTSMAN PLUS',
        'mitered': 'MITERED',
        'sill_apron_only': 'CRAFTSMAN'  # Uses same dimensions as Craftsman
    }
    excel_style = style_map.get(trim_style, 'CRAFTSMAN')
    
    # Map our trim types to Excel parts
    part_map = {
        'base': 'BASE',
        'casing': 'CASE',
        'headers': 'HEADER',
        'sills': 'SILL',
        'apron': 'APRON',
        'jambs': 'INT JAMB',  # Will handle window jamb separately
        'dentils': 'DENTIL'
    }
    excel_part = part_map.get(trim_type, 'BASE')
    
    # Special handling for jambs (window vs door)
    # Note: Our LF calculation combines window and door jambs, so we use WINDOW JAMB
    # when available (it's typically larger, more conservative estimate)
    if trim_type == 'jambs':
        # Try WINDOW JAMB first (for Craftsman/Craftsman Plus), fall back to INT JAMB
        if excel_style in ['CRAFTSMAN', 'CRAFTSMAN PLUS']:
            # Check if WINDOW JAMB exists for this style
            window_jamb_check = df[(df['STYLE'] == excel_style) & (df['PART'] == 'WINDOW JAMB')]
            if not window_jamb_check.empty:
                excel_part = 'WINDOW JAMB'
            else:
                excel_part = 'INT JAMB'
        else:
            excel_part = 'INT JAMB'
    
    # Filter by style and part
    filtered = df[(df['STYLE'] == excel_style) & (df['PART'] == excel_part)]
    
    if filtered.empty:
        # Fallback: try without style filter
        filtered = df[df['PART'] == excel_part]
    
    if filtered.empty:
        return None, None
    
    row = filtered.iloc[0]
    
    # Map finish level to column names (Excel uses 'UPGRADE' for Luxury)
    if finish_level == 'Economy':
        width = row['ECONOMY WIDTH']
        thickness = row['ECONOMY THICKNESS']
    elif finish_level == 'Standard':
        width = row['STANDARD WIDTH']
        thickness = row['STANDARD THICKNESS']
    else:  # Luxury (mapped to UPGRADE in Excel)
        width = row['UPGRADE WIDTH']
        thickness = row['UPGRADE THICKNESS']
    
    return float(width), float(thickness)


def get_waste_factor(rip_size, thickness_category='4/4'):
    """
    Get waste factor from AWI waste chart.
    
    Args:
        rip_size: The actual width in inches (after planing)
        thickness_category: '4/4', '5/4', '6/4', or '8/4'
    
    Returns:
        float: Waste factor (e.g., 0.111 = 11.1% waste)
    """
    df = load_awi_waste_chart()
    
    # Find closest rip size (round to nearest 0.125)
    rip_size_rounded = round(rip_size * 8) / 8  # Round to nearest 1/8"
    
    # Find matching row
    matches = df[df['RIP SIZE'] == rip_size_rounded]
    
    if matches.empty:
        # Find closest match
        df['diff'] = abs(df['RIP SIZE'] - rip_size_rounded)
        closest_idx = df['diff'].idxmin()
        matches = df.loc[[closest_idx]]
    
    if matches.empty:
        return 0.0  # Default no waste if not found
    
    row = matches.iloc[0]
    waste_factor = row[thickness_category]
    
    return float(waste_factor)


def calculate_bf_from_lf(linear_ft, width_inches, nominal_thickness_inches):
    """
    Calculate board feet from lineal feet using NOMINAL stock thickness.
    
    Formula: BF = (Nominal Thickness × Width × LF) / 12
    
    Args:
        linear_ft: Lineal feet (finished LF after project waste)
        width_inches: Width in inches (finished/rip size)
        nominal_thickness_inches: Nominal stock thickness in inches (what we order: 1.0, 1.25, 1.5, 2.0)
    
    Returns:
        float: Board feet
    """
    if linear_ft == 0 or width_inches == 0 or nominal_thickness_inches == 0:
        return 0.0
    
    # Use NOMINAL stock thickness for BF calculation (not finished thickness)
    bf = (nominal_thickness_inches * width_inches * linear_ft) / 12.0
    return bf


def get_nominal_stock_thickness(finished_thickness_inches):
    """
    Map finished thickness to next available nominal stock thickness.
    Hardwoods are sold in 4/4, 5/4, 6/4, 8/4 increments.
    
    Rule: Order the next thickest size that can be planed down to finished thickness.
    
    Args:
        finished_thickness_inches: Finished thickness in inches (e.g., 0.5, 0.75, 1.0)
    
    Returns:
        tuple: (nominal_thickness_inches, thickness_category)
            - nominal_thickness_inches: The stock thickness to order (0.75, 1.0, 1.25, 1.5, 2.0)
            - thickness_category: '4/4', '5/4', '6/4', or '8/4'
    """
    # Nominal stock thicknesses (what we order):
    # 4/4 = 1.0" nominal (planes to ~0.75" finished)
    # 5/4 = 1.25" nominal (planes to ~1.0" finished)
    # 6/4 = 1.5" nominal (planes to ~1.25" finished)
    # 8/4 = 2.0" nominal (planes to ~1.5" finished)
    
    # Map finished thickness to next available stock size
    if finished_thickness_inches <= 0.75:
        return (1.0, '4/4')  # 4/4 stock
    elif finished_thickness_inches <= 1.0:
        return (1.25, '5/4')  # 5/4 stock
    elif finished_thickness_inches <= 1.25:
        return (1.5, '6/4')  # 6/4 stock
    else:
        return (2.0, '8/4')  # 8/4 stock


def determine_thickness_category(thickness_inches):
    """
    Determine thickness category from finished thickness (for AWI waste lookup).
    This maps to the AWI chart columns.
    
    Args:
        thickness_inches: Finished thickness in inches
    
    Returns:
        str: '4/4', '5/4', '6/4', or '8/4' (for AWI chart lookup)
    """
    # AWI chart uses these categories based on finished thickness
    if thickness_inches <= 0.75:
        return '4/4'
    elif thickness_inches <= 1.0:
        return '5/4'
    elif thickness_inches <= 1.25:
        return '6/4'
    else:
        return '8/4'


def load_lumber_species():
    """Load lumber species list from CSV file"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'lumber_species.csv')
    
    if not os.path.exists(csv_path):
        # Return default list if file doesn't exist
        return ['Poplar', 'Maple', 'Oak', 'Cherry', 'Walnut']
    
    try:
        df = pd.read_csv(csv_path)
        if 'Species' in df.columns:
            return df['Species'].tolist()
        return df.iloc[:, 0].tolist()  # Use first column
    except Exception:
        return ['Poplar', 'Maple', 'Oak', 'Cherry', 'Walnut']


def calculate_bf_with_waste(lf_results, trim_style, finish_level):
    """
    Convert LF results to BF and apply waste factors.
    
    Args:
        lf_results: Dictionary of trim_type -> lineal feet
        trim_style: Trim style string
        finish_level: Finish level string
    
    Returns:
        dict: {
            'bf_raw': {trim_type: bf},
            'bf_with_waste': {trim_type: bf_with_waste},
            'waste_factors': {trim_type: waste_factor},
            'dimensions': {trim_type: (width, finished_thickness)},
            'nominal_thickness': {trim_type: nominal_thickness_inches},
            'thickness_category': {trim_type: '4/4'|'5/4'|'6/4'|'8/4'}
        }
    """
    bf_raw = {}
    bf_with_waste = {}
    waste_factors = {}
    dimensions = {}
    nominal_thicknesses = {}
    thickness_categories = {}
    
    for trim_type, linear_ft in lf_results.items():
        if linear_ft == 0:
            bf_raw[trim_type] = 0.0
            bf_with_waste[trim_type] = 0.0
            waste_factors[trim_type] = 0.0
            dimensions[trim_type] = (0.0, 0.0)
            nominal_thicknesses[trim_type] = 0.0
            thickness_categories[trim_type] = ''
            continue
        
        # Get dimensions (finished width and thickness)
        width, finished_thickness = get_trim_dimensions(trim_style, trim_type, finish_level)
        
        if width is None or finished_thickness is None:
            # No dimensions found, skip
            bf_raw[trim_type] = 0.0
            bf_with_waste[trim_type] = 0.0
            waste_factors[trim_type] = 0.0
            dimensions[trim_type] = (0.0, 0.0)
            nominal_thicknesses[trim_type] = 0.0
            thickness_categories[trim_type] = ''
            continue
        
        dimensions[trim_type] = (width, finished_thickness)
        
        # Map finished thickness to nominal stock thickness (next size up)
        nominal_thickness, thickness_category = get_nominal_stock_thickness(finished_thickness)
        nominal_thicknesses[trim_type] = nominal_thickness
        thickness_categories[trim_type] = thickness_category
        
        # Calculate BF using NOMINAL stock thickness (not finished thickness)
        bf = calculate_bf_from_lf(linear_ft, width, nominal_thickness)
        bf_raw[trim_type] = bf
        
        # Get waste factor from AWI chart (using rip size and thickness category)
        waste_factor = get_waste_factor(width, thickness_category)
        waste_factors[trim_type] = waste_factor
        
        # Apply waste: BF_with_waste = BF * (1 + waste_factor)
        bf_with_waste[trim_type] = bf * (1 + waste_factor)
    
    return {
        'bf_raw': bf_raw,
        'bf_with_waste': bf_with_waste,
        'waste_factors': waste_factors,
        'dimensions': dimensions,
        'nominal_thickness': nominal_thicknesses,
        'thickness_category': thickness_categories
    }

