"""
Trim calculation rules configuration.
This file implements the TRIM TAKEOFF CONTROL DOCUMENT specifications.
All calculations follow the exact rules defined in the control document.

Current Assumptions:
- Window dimensions (when no schedule):
  - Window width: 4' (48 inches)
  - Window height: door height minus 40"
- Wood-wrapped windows: Configurable via UI toggle (defaults to True)
- Door width: Using default 36" (3 feet)
- Barn/Pocket doors: Using 'trimmed_openings' field as proxy
- Schedule file: File upload available, but parser not yet implemented (uses assumptions)

Future enhancements:
- Implement PDF/Excel parser for door and window schedules
- Add individual window/door dimension inputs for manual entry
"""

# Trim types
TRIM_TYPES = [
    'base',
    'casing',
    'sills',
    'headers',
    'jambs',
    'apron',
    'dentils'
]

# Trim styles (matching control document)
TRIM_STYLES = [
    'craftsman',
    'mitered',
    'built_up',
    'sill_apron_only'
]

# Finish levels
FINISH_LEVELS = [
    'Standard',
    'Luxury',
    'Economy'
]

# Door heights in feet (6/8 = 6'8", 7/0 = 7'0", 8/0 = 8'0")
DOOR_HEIGHTS = {
    '6/8': 6.67,  # 6 feet 8 inches = 80 inches / 12
    '7/0': 7.0,   # 7 feet = 84 inches / 12
    '8/0': 8.0    # 8 feet = 96 inches / 12
}

# Waste factors (to be configured - these are defaults)
RUNNING_WASTE = 0.10  # 10% waste for baseboard, sills, aprons, headers, dentil
STANDING_WASTE = 0.15  # 15% waste for casing, jamb

# Default window dimensions (in inches) - used when not provided
# Window width: 4' (48 inches)
# Window height: door height minus 40" (when no schedule provided)
DEFAULT_WINDOW_WIDTH_INCHES = 48   # 4 feet
WINDOW_HEIGHT_OFFSET_INCHES = 40   # Subtract 40" from door height

# Default door width (in inches)
DEFAULT_DOOR_WIDTH_INCHES = 36  # 3 feet

# Wood-wrapped windows toggle (default True)
# If False, window jamb = 0
DEFAULT_WOOD_WRAPPED = True


def inches_to_feet(inches):
    """Convert inches to feet"""
    return inches / 12.0


def apply_running_waste(linear_ft):
    """Apply running waste factor"""
    return linear_ft * (1 + RUNNING_WASTE)


def apply_standing_waste(linear_ft):
    """Apply standing waste factor"""
    return linear_ft * (1 + STANDING_WASTE)


def get_window_height_ft(inputs):
    """
    Calculate window height in feet.
    If schedule is provided, use door height (for now, until parser is implemented).
    If no schedule, use door height minus 40 inches.
    """
    door_height_ft = DOOR_HEIGHTS.get(inputs['door_height'], 7.0)
    has_schedule = inputs.get('has_schedule', False)
    
    if has_schedule:
        # When schedule is provided, use door height (will be replaced by parser later)
        return door_height_ft
    else:
        # No schedule: window height = door height minus 40"
        return door_height_ft - inches_to_feet(WINDOW_HEIGHT_OFFSET_INCHES)


def get_window_width_ft(inputs):
    """
    Get window width in feet.
    If schedule is provided, use default (will be replaced by parser later).
    If no schedule, use 4' (48 inches).
    """
    has_schedule = inputs.get('has_schedule', False)
    
    if has_schedule:
        # When schedule is provided, use default (will be replaced by parser later)
        return inches_to_feet(DEFAULT_WINDOW_WIDTH_INCHES)
    else:
        # No schedule: window width = 4' (48 inches)
        return inches_to_feet(DEFAULT_WINDOW_WIDTH_INCHES)


def calculate_baseboard(inputs, trim_style, finish_level):
    """
    Calculate baseboard lineal footage.
    Control Document Section 2: Baseboard Rules
    """
    int_walls = inputs['int_walls_linear_ft']
    ext_walls = inputs['ext_walls_linear_ft']
    
    # Raw base = interior + exterior
    raw_base = int_walls + ext_walls
    
    # Base style multipliers (Section 2.2)
    style_multipliers = {
        'craftsman': 1.15,
        'mitered': 1.05,
        'built_up': 2.00,
        'sill_apron_only': 1.00  # Standard
    }
    multiplier = style_multipliers.get(trim_style, 1.00)
    
    # Installed base: interior gets base on both sides, exterior on one side
    installed_base_raw = (2 * int_walls) + ext_walls
    
    # Apply style multiplier and waste
    installed_base = apply_running_waste(installed_base_raw * multiplier)
    
    return installed_base


def calculate_window_casing(inputs, trim_style, finish_level):
    """
    Calculate window casing lineal footage.
    Control Document Section 3.1: Window Casing
    """
    windows = inputs['windows']
    sliders = inputs['sliders']
    total_windows = windows + sliders
    
    if total_windows == 0:
        return 0.0
    
    # Get window height based on schedule availability
    window_height_ft = get_window_height_ft(inputs)
    
    # Window casing: 2 vertical legs per opening
    window_casing_raw = window_height_ft * 2 * total_windows
    
    # Style overrides (Section 5)
    if trim_style == 'sill_apron_only':
        return 0.0
    
    # For mitered style, casing absorbs sill and header (handled in main calculation)
    # For now, return baseline
    window_casing = apply_standing_waste(window_casing_raw)
    
    return window_casing


def calculate_window_header(inputs, trim_style, finish_level):
    """
    Calculate window header lineal footage.
    Control Document Section 3.2: Window Headers
    """
    windows = inputs['windows']
    sliders = inputs['sliders']
    total_windows = windows + sliders
    
    if total_windows == 0:
        return 0.0
    
    # Header = width + 1 foot extra per opening
    window_width_ft = get_window_width_ft(inputs)
    window_header_raw = (window_width_ft + 1) * total_windows
    
    # Style overrides: Mitered and Sill/Apron Only have no header
    if trim_style in ['mitered', 'sill_apron_only']:
        return 0.0
    
    window_header = apply_running_waste(window_header_raw)
    return window_header


def calculate_window_sill(inputs, trim_style, finish_level):
    """
    Calculate window sill lineal footage.
    Control Document Section 3.3: Window Sills
    """
    # Sills only apply to non-slider windows
    windows = inputs['windows']
    
    if windows == 0:
        return 0.0
    
    window_width_ft = get_window_width_ft(inputs)
    window_sill_raw = window_width_ft * windows
    
    # Style overrides: Mitered has no sill
    if trim_style == 'mitered':
        return 0.0
    
    window_sill = apply_running_waste(window_sill_raw)
    return window_sill


def calculate_window_apron(inputs, trim_style, finish_level):
    """
    Calculate window apron lineal footage.
    Control Document Section 3.4: Window Apron
    """
    # Apron always matches sill LF
    window_width_ft = get_window_width_ft(inputs)
    window_sill_raw = window_width_ft * inputs['windows']
    
    # Style overrides: Mitered has no apron
    if trim_style == 'mitered':
        return 0.0
    
    window_apron = apply_running_waste(window_sill_raw)
    return window_apron


def calculate_window_jamb(inputs, trim_style, finish_level):
    """
    Calculate window jamb lineal footage.
    Control Document Section 3.5: Window Jamb
    """
    windows = inputs['windows']
    sliders = inputs['sliders']
    total_windows = windows + sliders
    
    if total_windows == 0:
        return 0.0
    
    # Wood-wrapped toggle
    wood_wrapped = inputs.get('wood_wrapped', DEFAULT_WOOD_WRAPPED)
    if not wood_wrapped:
        return 0.0
    
    window_height_ft = get_window_height_ft(inputs)
    window_width_ft = get_window_width_ft(inputs)
    
    # Style overrides
    if trim_style == 'sill_apron_only':
        return 0.0
    elif trim_style == 'mitered':
        # Mitered: full perimeter (4 sides)
        window_jamb_raw = ((2 * window_height_ft) + (2 * window_width_ft)) * total_windows
    else:
        # Craftsman/Built-Up: 3 sides (2 vertical + 1 head, sill covers bottom)
        window_jamb_raw = ((2 * window_height_ft) + window_width_ft) * total_windows
    
    window_jamb = apply_standing_waste(window_jamb_raw)
    return window_jamb


def calculate_door_casing(inputs, trim_style, finish_level):
    """
    Calculate door casing lineal footage.
    Control Document Section 4.1: Door Casing
    """
    ext_doors = inputs['ext_doors']
    int_doors = inputs['int_doors']
    
    door_height_ft = DOOR_HEIGHTS.get(inputs['door_height'], 7.0)
    
    # Exterior doors: 1 leg, Interior doors: 2 legs
    ext_casing_raw = door_height_ft * 1 * ext_doors
    int_casing_raw = door_height_ft * 2 * int_doors
    
    door_casing_raw = ext_casing_raw + int_casing_raw
    door_casing = apply_standing_waste(door_casing_raw)
    
    return door_casing


def calculate_door_header(inputs, trim_style, finish_level):
    """
    Calculate door header lineal footage.
    Control Document Section 4.2: Door Headers
    """
    ext_doors = inputs['ext_doors']
    int_doors = inputs['int_doors']
    
    door_width_ft = inches_to_feet(DEFAULT_DOOR_WIDTH_INCHES)
    door_height_ft = DOOR_HEIGHTS.get(inputs['door_height'], 7.0)
    
    # Exterior: 1 leg, Interior: 2 legs, plus 1-foot filler per opening
    ext_header_raw = (door_width_ft * 1 + 1) * ext_doors
    int_header_raw = (door_width_ft * 2 + 1) * int_doors
    
    door_header_raw = ext_header_raw + int_header_raw
    door_header = apply_running_waste(door_header_raw)
    
    return door_header


def calculate_door_jamb(inputs, trim_style, finish_level):
    """
    Calculate door jamb lineal footage.
    Control Document Section 4.3: Door Jamb
    Only barn and pocket doors receive jamb.
    For now, we'll use trimmed_openings as barn/pocket doors.
    """
    # Only barn and pocket doors get jamb
    # Using trimmed_openings as proxy for barn/pocket doors
    barn_pocket_doors = inputs.get('trimmed_openings', 0)
    
    if barn_pocket_doors == 0:
        return 0.0
    
    wood_wrapped = inputs.get('wood_wrapped', DEFAULT_WOOD_WRAPPED)
    if not wood_wrapped:
        return 0.0
    
    door_height_ft = DOOR_HEIGHTS.get(inputs['door_height'], 7.0)
    
    # Jamb: 2 vertical legs per opening
    door_jamb_raw = door_height_ft * 2 * barn_pocket_doors
    door_jamb = apply_standing_waste(door_jamb_raw)
    
    return door_jamb


def calculate_dentil(inputs, trim_style, finish_level):
    """
    Calculate dentil lineal footage.
    Control Document Section 5.2: Built-Up Style
    """
    # Dentil only applies to Built-Up style
    if trim_style != 'built_up':
        return 0.0
    
    windows = inputs['windows']
    sliders = inputs['sliders']
    total_windows = windows + sliders
    
    if total_windows == 0:
        return 0.0
    
    # Dentil LF = 2 × window_header_raw
    window_width_ft = get_window_width_ft(inputs)
    window_header_raw = (window_width_ft + 1) * total_windows
    dentil_raw = 2 * window_header_raw
    
    dentil = apply_running_waste(dentil_raw)
    return dentil


def calculate_trim(inputs, trim_style, finish_level):
    """
    Calculate total lineal footage for a given trim style and finish level.
    Implements the complete TRIM TAKEOFF CONTROL DOCUMENT specification.
    
    Args:
        inputs: Dictionary with form inputs:
            - int_walls_linear_ft: float
            - ext_walls_linear_ft: float
            - ext_doors: int
            - int_doors: int
            - trimmed_openings: int (barn/pocket doors)
            - windows: int
            - sliders: int
            - door_height: str (e.g., '6/8', '7/0', '8/0')
            - wood_wrapped: bool (optional, defaults to True)
        trim_style: str (one of TRIM_STYLES)
        finish_level: str (one of FINISH_LEVELS)
    
    Returns:
        Dictionary with trim type as key and lineal footage as value
    """
    # Ensure wood_wrapped is set (use value from UI or default)
    if 'wood_wrapped' not in inputs:
        inputs['wood_wrapped'] = DEFAULT_WOOD_WRAPPED
    
    # Ensure has_schedule is set (defaults to False)
    if 'has_schedule' not in inputs:
        inputs['has_schedule'] = False
    
    # Calculate baseline (Craftsman) for all trim types
    results = {
        'base': calculate_baseboard(inputs, trim_style, finish_level),
        'casing': 0.0,  # Will be calculated below
        'headers': 0.0,  # Will be calculated below
        'sills': calculate_window_sill(inputs, trim_style, finish_level),
        'apron': calculate_window_apron(inputs, trim_style, finish_level),
        'jambs': 0.0,  # Will be calculated below
        'dentils': calculate_dentil(inputs, trim_style, finish_level)
    }
    
    # Calculate window and door components
    window_casing_raw = 0.0
    window_header_raw = 0.0
    window_sill_raw = 0.0
    
    # Calculate raw values for style overrides
    windows = inputs['windows']
    sliders = inputs['sliders']
    total_windows = windows + sliders
    
    if total_windows > 0:
        window_height_ft = get_window_height_ft(inputs)
        window_width_ft = get_window_width_ft(inputs)
        
        window_casing_raw = window_height_ft * 2 * total_windows
        window_header_raw = (window_width_ft + 1) * total_windows
        window_sill_raw = window_width_ft * windows
    
    # Apply style overrides (Section 5)
    if trim_style == 'mitered':
        # Mitered: No sill, apron, or separate header
        # Move their LF into casing (apron matches sill, so 2x sill)
        removed_sill = window_sill_raw
        removed_apron = window_sill_raw  # Apron matches sill
        removed_header = window_header_raw
        
        window_casing_raw += removed_sill + removed_apron + removed_header
        results['sills'] = 0.0
        results['apron'] = 0.0
        results['headers'] = calculate_door_header(inputs, trim_style, finish_level)  # Only door headers
        results['casing'] = apply_standing_waste(window_casing_raw) + calculate_door_casing(inputs, trim_style, finish_level)
    elif trim_style == 'sill_apron_only':
        # Sill/Apron Only: Only sill and apron for windows
        results['casing'] = calculate_door_casing(inputs, trim_style, finish_level)  # Only door casing
        results['headers'] = calculate_door_header(inputs, trim_style, finish_level)  # Only door headers
    else:
        # Craftsman and Built-Up: Normal calculations
        results['casing'] = apply_standing_waste(window_casing_raw) + calculate_door_casing(inputs, trim_style, finish_level)
        results['headers'] = apply_running_waste(window_header_raw) + calculate_door_header(inputs, trim_style, finish_level)
    
    # Calculate jambs (window + door)
    results['jambs'] = calculate_window_jamb(inputs, trim_style, finish_level) + calculate_door_jamb(inputs, trim_style, finish_level)
    
    return results

