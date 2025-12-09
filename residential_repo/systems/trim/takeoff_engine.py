"""
Trim system module: Takeoff engine - turn raw counts/lengths into assemblies.
Wrapper around legacy trim calculation logic.
"""

from .models import TrimJobInput
from .trim_rules import calculate_trim, TRIM_STYLES, FINISH_LEVELS
from .trim_bf_calculator import calculate_bf_with_waste


def build_internal_job_from_input(job_input: TrimJobInput) -> dict:
    """
    Adapter from TrimJobInput into whatever internal structures the legacy
    trim calculators expect.
    
    This function:
    - Converts the Pydantic model into dicts
    - Maps spec levels to rule sets
    - Prepares arguments for trim_rules / trim_bf_calculator
    
    It does NOT touch the filesystem.
    
    Args:
        job_input: TrimJobInput model
        
    Returns:
        dict with keys:
            - 'inputs': dict for calculate_trim() (int_walls_linear_ft, ext_walls_linear_ft, etc.)
            - 'trim_style': str (defaults to 'craftsman')
            - 'finish_level': str (mapped from spec_level)
    """
    # Map spec_level to finish_level
    spec_to_finish = {
        'economy': 'Economy',
        'standard': 'Standard',
        'premium': 'Luxury',
        'luxury': 'Luxury'
    }
    finish_level = spec_to_finish.get(
        (job_input.spec_level or 'standard').lower(),
        'Standard'
    )
    
    # Default trim style (can be made configurable later)
    trim_style = 'craftsman'
    
    # Aggregate room data into job-level inputs
    # For now, we'll sum up room hints or use defaults
    total_base_lf = sum(room.base_lf or 0.0 for room in job_input.rooms)
    total_windows = sum(room.window_openings or 0 for room in job_input.rooms)
    total_case_openings = sum(room.case_openings or 0 for room in job_input.rooms)
    
    # Estimate interior/exterior walls from base LF
    # Simple heuristic: assume 50/50 split if not specified
    int_walls_linear_ft = total_base_lf * 0.5 if total_base_lf > 0 else 50.0
    ext_walls_linear_ft = total_base_lf * 0.5 if total_base_lf > 0 else 20.0
    
    # Estimate doors from case openings (rough approximation)
    # If case_openings provided, assume mix of interior/exterior
    int_doors = max(1, int(total_case_openings * 0.7)) if total_case_openings > 0 else 2
    ext_doors = max(0, int(total_case_openings * 0.3)) if total_case_openings > 0 else 1
    
    # Build inputs dict for legacy calculate_trim function
    inputs = {
        'int_walls_linear_ft': int_walls_linear_ft,
        'ext_walls_linear_ft': ext_walls_linear_ft,
        'ext_doors': ext_doors,
        'int_doors': int_doors,
        'trimmed_openings': 0,  # barn/pocket doors - not in current model
        'windows': total_windows,
        'sliders': 0,  # not in current model
        'door_height': '7/0',  # default 7'0"
        'wood_wrapped': True,  # default
        'has_schedule': False  # default
    }
    
    return {
        'inputs': inputs,
        'trim_style': trim_style,
        'finish_level': finish_level
    }


def run_takeoff(job_input: TrimJobInput) -> dict:
    """
    High-level entry point for the trim takeoff.
    Calls the existing legacy functions to compute quantities / BF, etc.
    
    Args:
        job_input: TrimJobInput model
        
    Returns:
        dict with keys:
            - 'lf': dict of trim_type -> lineal feet (from calculate_trim)
            - 'bf': dict with BF calculations (from calculate_bf_with_waste)
                - 'bf_raw': dict of trim_type -> board feet
                - 'bf_with_waste': dict of trim_type -> board feet with waste
                - 'waste_factors': dict of trim_type -> waste factor
                - 'dimensions': dict of trim_type -> (width, thickness)
                - 'nominal_thickness': dict of trim_type -> nominal thickness
                - 'thickness_category': dict of trim_type -> thickness category
            - 'trim_style': str
            - 'finish_level': str
            - 'inputs': dict (original inputs passed to calculate_trim)
    """
    # Build internal job structure
    internal = build_internal_job_from_input(job_input)
    
    # Run legacy calculate_trim
    lf_results = calculate_trim(
        internal['inputs'],
        internal['trim_style'],
        internal['finish_level']
    )
    
    # Run legacy calculate_bf_with_waste
    bf_data = calculate_bf_with_waste(
        lf_results,
        internal['trim_style'],
        internal['finish_level']
    )
    
    return {
        'lf': lf_results,
        'bf': bf_data,
        'trim_style': internal['trim_style'],
        'finish_level': internal['finish_level'],
        'inputs': internal['inputs']
    }
