"""GUI application for Pole Barn Calculator using tkinter."""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
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
        
        geom_model, takeoff, priced_items, summary, bom_items = calculator.calculate(inputs)
        
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
        if summary.overhead_total > 0:
            output_text.insert(tk.END, f"  Overhead Total:    ${summary.overhead_total:,.2f}\n")
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
        
        # Store BOM items for export (attach to output_text widget)
        output_text.bom_items = bom_items
        output_text.inputs = inputs
        output_text.geom_model = geom_model
        output_text.takeoff = takeoff
        output_text.priced_items = priced_items
        output_text.summary = summary
        
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
    output_frame.rowconfigure(1, weight=1)
    root.columnconfigure(2, weight=2)
    
    # Export buttons frame
    export_frame = ttk.Frame(output_frame)
    export_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
    export_frame.columnconfigure(0, weight=1)
    export_frame.columnconfigure(1, weight=1)
    
    def export_excel():
        """Export BOM to Excel."""
        if not hasattr(output_text, 'bom_items'):
            messagebox.showwarning("No Data", "Please run a calculation first.")
            return
        
        from systems.pole_barn.export_excel import export_bom_to_excel, generate_bom_filename
        
        filename = generate_bom_filename(output_text.inputs.project_name if hasattr(output_text, 'inputs') else None)
        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile=filename,
        )
        
        if filepath:
            try:
                export_bom_to_excel(output_text.bom_items, Path(filepath), output_text.inputs.project_name if hasattr(output_text, 'inputs') else None)
                messagebox.showinfo("Success", f"BOM exported to:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export BOM:\n{str(e)}")
    
    def export_json():
        """Export project to JSON."""
        if not hasattr(output_text, 'bom_items'):
            messagebox.showwarning("No Data", "Please run a calculation first.")
            return
        
        from systems.pole_barn.export_json import export_project_to_json, generate_json_filename
        
        filename = generate_json_filename(output_text.inputs.project_name if hasattr(output_text, 'inputs') else None)
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=filename,
        )
        
        if filepath:
            try:
                export_project_to_json(
                    output_text.inputs,
                    output_text.geom_model,
                    output_text.takeoff,
                    output_text.bom_items,
                    output_text.priced_items,
                    output_text.summary,
                    Path(filepath),
                )
                messagebox.showinfo("Success", f"Project exported to:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export project:\n{str(e)}")
    
    excel_button = ttk.Button(export_frame, text="Export BOM (Excel)", command=export_excel)
    excel_button.grid(row=0, column=0, padx=5, sticky="ew")
    
    csv_button = ttk.Button(export_frame, text="Export BOM (CSV - Flat)", command=export_csv)
    csv_button.grid(row=0, column=1, padx=5, sticky="ew")
    
    json_button = ttk.Button(export_frame, text="Export Project (JSON)", command=export_json)
    json_button.grid(row=0, column=2, padx=5, sticky="ew")
    
    # Output text area with scrollbar
    output_text = scrolledtext.ScrolledText(
        output_frame,
        width=60,
        height=40,
        wrap=tk.WORD,
        font=("Consolas", 9),
    )
    output_text.grid(row=1, column=0, sticky="nsew")
    
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
