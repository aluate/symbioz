"""
Configuration file validation module.
Validates all required Excel and CSV configuration files for the trim calculator.
"""

import os
import pandas as pd
from tkinter import messagebox


def validate_trim_dimensions(config_dir):
    """Validate trim_dimensions.xlsx schema"""
    excel_path = os.path.join(config_dir, 'trim_dimensions.xlsx')
    
    if not os.path.exists(excel_path):
        return False, f"Missing file: trim_dimensions.xlsx"
    
    try:
        df = pd.read_excel(excel_path)
        
        # Required columns
        required_cols = ['STYLE', 'PART', 'ECONOMY WIDTH', 'ECONOMY THICKNESS', 
                        'STANDARD WIDTH', 'STANDARD THICKNESS', 
                        'UPGRADE WIDTH', 'UPGRADE THICKNESS']
        
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            return False, f"trim_dimensions.xlsx missing columns: {', '.join(missing_cols)}"
        
        if df.empty:
            return False, "trim_dimensions.xlsx is empty"
        
        return True, "OK"
    except Exception as e:
        return False, f"Error reading trim_dimensions.xlsx: {str(e)}"


def validate_awi_waste_chart(config_dir):
    """Validate awi_waste_chart.xlsx schema"""
    excel_path = os.path.join(config_dir, 'awi_waste_chart.xlsx')
    
    if not os.path.exists(excel_path):
        return False, f"Missing file: awi_waste_chart.xlsx"
    
    try:
        df = pd.read_excel(excel_path)
        
        # Required columns
        required_cols = ['RIP SIZE', '4/4', '5/4', '6/4', '8/4']
        
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            return False, f"awi_waste_chart.xlsx missing columns: {', '.join(missing_cols)}"
        
        if df.empty:
            return False, "awi_waste_chart.xlsx is empty"
        
        return True, "OK"
    except Exception as e:
        return False, f"Error reading awi_waste_chart.xlsx: {str(e)}"


def validate_lumber_species(config_dir):
    """Validate lumber_species.csv schema"""
    csv_path = os.path.join(config_dir, 'lumber_species.csv')
    
    if not os.path.exists(csv_path):
        return False, f"Missing file: lumber_species.csv"
    
    try:
        df = pd.read_csv(csv_path)
        
        if df.empty:
            return False, "lumber_species.csv is empty"
        
        # Check if has 'Species' column or at least one column
        if 'Species' not in df.columns and len(df.columns) == 0:
            return False, "lumber_species.csv has no valid columns"
        
        return True, "OK"
    except Exception as e:
        return False, f"Error reading lumber_species.csv: {str(e)}"


def validate_bf_cost(config_dir):
    """Validate bf_cost.xlsx schema"""
    excel_path = os.path.join(config_dir, 'bf_cost.xlsx')
    
    if not os.path.exists(excel_path):
        return False, f"Missing file: bf_cost.xlsx"
    
    try:
        df = pd.read_excel(excel_path)
        
        # Required columns: Species and thickness categories
        required_cols = ['Species', '4/4', '5/4', '6/4', '8/4']
        
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            return False, f"bf_cost.xlsx missing columns: {', '.join(missing_cols)}"
        
        if df.empty:
            return False, "bf_cost.xlsx is empty"
        
        return True, "OK"
    except Exception as e:
        return False, f"Error reading bf_cost.xlsx: {str(e)}"


def validate_finish_rates(config_dir):
    """Validate Finish Rates.xlsx schema (if exists)"""
    excel_path = os.path.join(config_dir, 'Finish_Rates.xlsx')
    
    if not os.path.exists(excel_path):
        return None, "Finish Rates.xlsx not found (optional)"
    
    try:
        df = pd.read_excel(excel_path)
        
        if df.empty:
            return False, "Finish Rates.xlsx is empty"
        
        # Basic validation - can be expanded based on actual schema
        return True, "OK"
    except Exception as e:
        return False, f"Error reading Finish Rates.xlsx: {str(e)}"


def validate_setup_costs(config_dir):
    """Validate setup_costs.xlsx schema (if exists)"""
    excel_path = os.path.join(config_dir, 'setup_costs.xlsx')
    
    if not os.path.exists(excel_path):
        return None, "setup_costs.xlsx not found (optional - using hardcoded values)"
    
    try:
        df = pd.read_excel(excel_path)
        
        if df.empty:
            return False, "setup_costs.xlsx is empty"
        
        # Basic validation - can be expanded based on actual schema
        return True, "OK"
    except Exception as e:
        return False, f"Error reading setup_costs.xlsx: {str(e)}"


def validate_finish_pricing(config_dir):
    """Validate finish_pricing.xlsx schema (if exists)"""
    excel_path = os.path.join(config_dir, 'finish_pricing.xlsx')
    
    if not os.path.exists(excel_path):
        return None, "finish_pricing.xlsx not found (optional)"
    
    try:
        df = pd.read_excel(excel_path)
        
        if df.empty:
            return False, "finish_pricing.xlsx is empty"
        
        # Basic validation - can be expanded based on actual schema
        return True, "OK"
    except Exception as e:
        return False, f"Error reading finish_pricing.xlsx: {str(e)}"


def validate_config_files(show_dialogs=True):
    """
    Validate all configuration files.
    
    Args:
        show_dialogs: If True, show Tkinter error dialogs for critical errors
    
    Returns:
        tuple: (is_valid: bool, errors: list, warnings: list)
    """
    # Get config directory (repo root/config)
    script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    config_dir = os.path.join(script_dir, 'config')
    errors = []
    warnings = []
    
    # Required files
    validations = [
        ('trim_dimensions.xlsx', validate_trim_dimensions),
        ('awi_waste_chart.xlsx', validate_awi_waste_chart),
        ('lumber_species.csv', validate_lumber_species),
        ('bf_cost.xlsx', validate_bf_cost),
    ]
    
    # Optional files
    optional_validations = [
        ('Finish_Rates.xlsx', validate_finish_rates),
        ('setup_costs.xlsx', validate_setup_costs),
        ('finish_pricing.xlsx', validate_finish_pricing),
    ]
    
    # Validate required files
    for file_name, validation_func in validations:
        is_valid, message = validation_func(config_dir)
        if not is_valid:
            errors.append(f"{file_name}: {message}")
        elif message != "OK":
            warnings.append(f"{file_name}: {message}")
    
    # Validate optional files
    for file_name, validation_func in optional_validations:
        result, message = validation_func(config_dir)
        if result is False:  # File exists but has errors
            warnings.append(f"{file_name}: {message}")
        elif result is None:  # File doesn't exist (optional)
            warnings.append(f"{file_name}: {message}")
    
    # Show dialogs for critical errors
    if errors and show_dialogs:
        error_msg = "Critical configuration errors found:\n\n" + "\n".join(errors)
        error_msg += "\n\nPlease fix these errors before using the calculator."
        messagebox.showerror("Configuration Error", error_msg)
    
    # Show warnings if any
    if warnings and show_dialogs and not errors:
        warning_msg = "Configuration warnings:\n\n" + "\n".join(warnings)
        messagebox.showwarning("Configuration Warning", warning_msg)
    
    return len(errors) == 0, errors, warnings

