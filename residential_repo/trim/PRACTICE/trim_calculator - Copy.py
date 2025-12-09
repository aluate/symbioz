"""
Trim Take-Off Calculator
Desktop application for calculating lineal footage of trim materials.
"""

import tkinter as tk
import os
import csv
from datetime import datetime
from tkinter import ttk, messagebox, filedialog
from trim_rules import TRIM_STYLES, FINISH_LEVELS, DOOR_HEIGHTS, calculate_trim
from trim_bf_calculator import calculate_bf_with_waste, load_lumber_species
from invoice_generator import generate_invoice_excel

class TrimCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trim Take-Off Calculator")
        self.root.geometry("800x700")
        
        # Create main frame with padding
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for resizing
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Form inputs dictionary
        self.inputs = {}
        
        # Store calculation results for export
        self.all_results = {}
        
        # Create form fields
        self.create_form_fields(main_frame)
        
        # Create results area
        self.create_results_area(main_frame)
        
        # Create calculate and export buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=15, column=0, columnspan=2, pady=20)
        
        calculate_btn = ttk.Button(button_frame, text="Calculate Trim", command=self.calculate)
        calculate_btn.grid(row=0, column=0, padx=5)
        
        export_btn = ttk.Button(button_frame, text="Export to CSV", command=self.export_to_csv)
        export_btn.grid(row=0, column=1, padx=5)
        
        invoice_btn = ttk.Button(button_frame, text="Generate Invoice", command=self.generate_invoice)
        invoice_btn.grid(row=0, column=2, padx=5)
        
        # Pricing settings frame
        pricing_frame = ttk.LabelFrame(main_frame, text="Pricing Settings", padding="5")
        pricing_frame.grid(row=16, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(pricing_frame, text="LF Cost per Foot:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.inputs['lf_cost_per_ft'] = ttk.Entry(pricing_frame, width=10)
        self.inputs['lf_cost_per_ft'].insert(0, '0.85')  # Default
        self.inputs['lf_cost_per_ft'].grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(pricing_frame, text="BF Markup %:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.inputs['bf_markup_pct'] = ttk.Entry(pricing_frame, width=10)
        self.inputs['bf_markup_pct'].insert(0, '20')  # Default 20%
        self.inputs['bf_markup_pct'].grid(row=0, column=3, sticky=tk.W, padx=5, pady=2)
        
        # Invoice info frame
        invoice_frame = ttk.LabelFrame(main_frame, text="Invoice Information", padding="5")
        invoice_frame.grid(row=17, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(invoice_frame, text="Job Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.inputs['job_name'] = ttk.Entry(invoice_frame, width=20)
        self.inputs['job_name'].grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        
        ttk.Label(invoice_frame, text="Customer:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.inputs['customer_name'] = ttk.Entry(invoice_frame, width=20)
        self.inputs['customer_name'].grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        
        ttk.Label(invoice_frame, text="Sales Tax Rate:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.inputs['sales_tax_rate'] = ttk.Entry(invoice_frame, width=10)
        self.inputs['sales_tax_rate'].insert(0, '0.06')  # Default 6%
        self.inputs['sales_tax_rate'].grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        
        invoice_frame.columnconfigure(1, weight=1)
    
    def validate_numeric_input(self, value, is_float=False):
        """Validate numeric input between 0 and 10000"""
        if not value:
            return True  # Allow empty for now
        try:
            if is_float:
                num = float(value)
            else:
                num = int(value)
            return 0 <= num <= 10000
        except ValueError:
            return False
    
    def on_numeric_validate(self, P, is_float=False):
        """Validation callback for numeric entries"""
        if P == "":
            return True  # Allow empty
        if self.validate_numeric_input(P, is_float):
            return True
        return False
    
    def create_form_fields(self, parent):
        """Create all form input fields"""
        row = 0
        
        # Register validation function
        vcmd_float = (self.root.register(lambda P: self.on_numeric_validate(P, True)), '%P')
        vcmd_int = (self.root.register(lambda P: self.on_numeric_validate(P, False)), '%P')
        
        # Toggle for manual LF input
        self.inputs['has_lf_takeoffs'] = tk.BooleanVar(value=False)
        lf_toggle_check = ttk.Checkbutton(
            parent,
            text="I already have LF takeoffs for each trim type",
            variable=self.inputs['has_lf_takeoffs'],
            command=self.toggle_lf_input_mode
        )
        lf_toggle_check.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        # Manual LF input frame (initially hidden)
        self.manual_lf_frame = ttk.LabelFrame(parent, text="Manual LF Input by Trim Type", padding="5")
        self.manual_lf_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        self.manual_lf_frame.grid_remove()  # Hidden by default
        
        manual_row = 0
        trim_types_manual = ['base', 'casing', 'headers', 'sills', 'apron', 'jambs', 'dentils']
        self.manual_lf_inputs = {}
        for trim_type in trim_types_manual:
            ttk.Label(self.manual_lf_frame, text=f"{trim_type.replace('_', ' ').title()} (LF):").grid(
                row=manual_row, column=0, sticky=tk.W, padx=5, pady=2)
            self.manual_lf_inputs[trim_type] = ttk.Entry(self.manual_lf_frame, width=15, validate='key', validatecommand=vcmd_float)
            self.manual_lf_inputs[trim_type].grid(row=manual_row, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
            manual_row += 1
        self.manual_lf_frame.columnconfigure(1, weight=1)
        row += 1
        
        # Standard input frame (shown by default)
        self.standard_input_frame = ttk.LabelFrame(parent, text="Project Measurements", padding="5")
        self.standard_input_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        standard_row = 0
        # Linear feet inputs
        ttk.Label(self.standard_input_frame, text="Interior Walls (linear ft):").grid(row=standard_row, column=0, sticky=tk.W, pady=5)
        self.inputs['int_walls_linear_ft'] = ttk.Entry(self.standard_input_frame, width=20, validate='key', validatecommand=vcmd_float)
        self.inputs['int_walls_linear_ft'].grid(row=standard_row, column=1, sticky=(tk.W, tk.E), pady=5)
        standard_row += 1
        
        ttk.Label(self.standard_input_frame, text="Exterior Walls (linear ft):").grid(row=standard_row, column=0, sticky=tk.W, pady=5)
        self.inputs['ext_walls_linear_ft'] = ttk.Entry(self.standard_input_frame, width=20, validate='key', validatecommand=vcmd_float)
        self.inputs['ext_walls_linear_ft'].grid(row=standard_row, column=1, sticky=(tk.W, tk.E), pady=5)
        standard_row += 1
        
        # Count inputs
        ttk.Label(self.standard_input_frame, text="Exterior Doors:").grid(row=standard_row, column=0, sticky=tk.W, pady=5)
        self.inputs['ext_doors'] = ttk.Entry(self.standard_input_frame, width=20, validate='key', validatecommand=vcmd_int)
        self.inputs['ext_doors'].grid(row=standard_row, column=1, sticky=(tk.W, tk.E), pady=5)
        standard_row += 1
        
        ttk.Label(self.standard_input_frame, text="Interior Doors:").grid(row=standard_row, column=0, sticky=tk.W, pady=5)
        self.inputs['int_doors'] = ttk.Entry(self.standard_input_frame, width=20, validate='key', validatecommand=vcmd_int)
        self.inputs['int_doors'].grid(row=standard_row, column=1, sticky=(tk.W, tk.E), pady=5)
        standard_row += 1
        
        ttk.Label(self.standard_input_frame, text="Trimmed Openings:").grid(row=standard_row, column=0, sticky=tk.W, pady=5)
        self.inputs['trimmed_openings'] = ttk.Entry(self.standard_input_frame, width=20, validate='key', validatecommand=vcmd_int)
        self.inputs['trimmed_openings'].grid(row=standard_row, column=1, sticky=(tk.W, tk.E), pady=5)
        standard_row += 1
        
        ttk.Label(self.standard_input_frame, text="Windows:").grid(row=standard_row, column=0, sticky=tk.W, pady=5)
        self.inputs['windows'] = ttk.Entry(self.standard_input_frame, width=20, validate='key', validatecommand=vcmd_int)
        self.inputs['windows'].grid(row=standard_row, column=1, sticky=(tk.W, tk.E), pady=5)
        standard_row += 1
        
        ttk.Label(self.standard_input_frame, text="Sliders:").grid(row=standard_row, column=0, sticky=tk.W, pady=5)
        self.inputs['sliders'] = ttk.Entry(self.standard_input_frame, width=20, validate='key', validatecommand=vcmd_int)
        self.inputs['sliders'].grid(row=standard_row, column=1, sticky=(tk.W, tk.E), pady=5)
        standard_row += 1
        
        self.standard_input_frame.columnconfigure(1, weight=1)
        row += 1
        
        # Door height dropdown
        ttk.Label(parent, text="Door Height:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.inputs['door_height'] = ttk.Combobox(parent, values=list(DOOR_HEIGHTS.keys()), width=17, state="readonly")
        self.inputs['door_height'].set('6/8')  # Default value
        self.inputs['door_height'].grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Finish level dropdown
        ttk.Label(parent, text="Finish Level:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.inputs['finish_level'] = ttk.Combobox(parent, values=FINISH_LEVELS, width=17, state="readonly")
        self.inputs['finish_level'].set('Standard')  # Default value
        self.inputs['finish_level'].grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Species dropdown
        ttk.Label(parent, text="Lumber Species:").grid(row=row, column=0, sticky=tk.W, pady=5)
        species_list = load_lumber_species()
        self.inputs['species'] = ttk.Combobox(parent, values=species_list, width=17, state="readonly")
        if species_list:
            self.inputs['species'].set(species_list[0])  # Default to first species
        self.inputs['species'].grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Wood-wrapped toggle
        self.inputs['wood_wrapped'] = tk.BooleanVar(value=True)
        wood_wrapped_check = ttk.Checkbutton(
            parent, 
            text="Wood-wrapped windows/doors", 
            variable=self.inputs['wood_wrapped']
        )
        wood_wrapped_check.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        # Finishing toggle
        self.inputs['is_finishing'] = tk.BooleanVar(value=False)
        finishing_check = ttk.Checkbutton(
            parent,
            text="Finishing required",
            variable=self.inputs['is_finishing'],
            command=self.toggle_finish_type
        )
        finishing_check.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        # Finish type dropdown (initially hidden)
        self.finish_type_frame = ttk.Frame(parent)
        self.finish_type_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        self.finish_type_frame.grid_remove()  # Hidden by default
        
        ttk.Label(self.finish_type_frame, text="Finish Type:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.inputs['finish_type'] = ttk.Combobox(self.finish_type_frame, values=['Stain', 'Paint', 'Other'], width=15, state="readonly")
        self.inputs['finish_type'].set('Stain')  # Default
        self.inputs['finish_type'].grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        self.finish_type_frame.columnconfigure(1, weight=1)
        row += 1
        
        # Door/Window schedule toggle
        ttk.Label(parent, text="Do you have a door and window schedule?").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.inputs['has_schedule'] = tk.BooleanVar(value=False)
        schedule_frame = ttk.Frame(parent)
        schedule_frame.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        
        schedule_yes = ttk.Radiobutton(schedule_frame, text="Yes", variable=self.inputs['has_schedule'], value=True, command=self.toggle_schedule_fields)
        schedule_yes.grid(row=0, column=0, padx=5)
        
        schedule_no = ttk.Radiobutton(schedule_frame, text="No", variable=self.inputs['has_schedule'], value=False, command=self.toggle_schedule_fields)
        schedule_no.grid(row=0, column=1, padx=5)
        row += 1
        
        # File upload field (initially hidden)
        self.schedule_file_frame = ttk.Frame(parent)
        self.schedule_file_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        self.schedule_file_frame.grid_remove()  # Hidden by default
        
        ttk.Label(self.schedule_file_frame, text="Schedule File:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.inputs['schedule_file_path'] = tk.StringVar()
        schedule_file_entry = ttk.Entry(self.schedule_file_frame, textvariable=self.inputs['schedule_file_path'], width=40, state='readonly')
        schedule_file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        self.schedule_file_frame.columnconfigure(1, weight=1)
        
        browse_btn = ttk.Button(self.schedule_file_frame, text="Browse...", command=self.browse_schedule_file)
        browse_btn.grid(row=0, column=2, padx=5)
        row += 1
    
    def toggle_schedule_fields(self):
        """Show/hide schedule file upload field based on toggle"""
        if self.inputs['has_schedule'].get():
            self.schedule_file_frame.grid()
        else:
            self.schedule_file_frame.grid_remove()
            self.inputs['schedule_file_path'].set('')
    
    def toggle_finish_type(self):
        """Show/hide finish type dropdown based on finishing toggle"""
        if self.inputs['is_finishing'].get():
            self.finish_type_frame.grid()
        else:
            self.finish_type_frame.grid_remove()
    
    def toggle_lf_input_mode(self):
        """Show/hide manual LF input or standard measurement inputs"""
        if self.inputs['has_lf_takeoffs'].get():
            # Show manual LF inputs, hide standard inputs
            self.manual_lf_frame.grid()
            self.standard_input_frame.grid_remove()
        else:
            # Show standard inputs, hide manual LF inputs
            self.manual_lf_frame.grid_remove()
            self.standard_input_frame.grid()
    
    def browse_schedule_file(self):
        """Open file dialog to select schedule file"""
        # Start in the same directory as the script (for template portability)
        initial_dir = os.path.dirname(os.path.abspath(__file__))
        filename = filedialog.askopenfilename(
            title="Select Door and Window Schedule",
            initialdir=initial_dir,
            filetypes=[
                ("PDF files", "*.pdf"),
                ("Excel files", "*.xlsx *.xls"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )
        if filename:
            # Store as relative path if in same directory, otherwise absolute
            try:
                rel_path = os.path.relpath(filename, initial_dir)
                if not rel_path.startswith('..'):
                    self.inputs['schedule_file_path'].set(rel_path)
                else:
                    self.inputs['schedule_file_path'].set(filename)
            except ValueError:
                # If relative path fails (different drives on Windows), use absolute
                self.inputs['schedule_file_path'].set(filename)
    
    def create_results_area(self, parent):
        """Create results display area"""
        # Results frame
        results_frame = ttk.LabelFrame(parent, text="Results", padding="10")
        results_frame.grid(row=18, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        results_frame.columnconfigure(0, weight=1)
        parent.rowconfigure(18, weight=1)
        
        # Create notebook for tabbed results (one tab per trim style)
        self.results_notebook = ttk.Notebook(results_frame)
        self.results_notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_frame.rowconfigure(0, weight=1)
        
        # Create text widgets for each trim style
        self.result_texts = {}
        style_labels = {
            'craftsman': 'Craftsman',
            'mitered': 'Mitered',
            'built_up': 'Built-Up',
            'sill_apron_only': 'Sill/Apron Only'
        }
        for style in TRIM_STYLES:
            frame = ttk.Frame(self.results_notebook)
            label = style_labels.get(style, style.replace('_', ' ').title())
            self.results_notebook.add(frame, text=label)
            
            text_widget = tk.Text(frame, wrap=tk.WORD, height=15, width=70)
            scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
            
            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(0, weight=1)
            
            self.result_texts[style] = text_widget
    
    def validate_inputs(self):
        """Validate and convert form inputs"""
        validated = {}
        validated['has_lf_takeoffs'] = self.inputs['has_lf_takeoffs'].get()
        
        # Check if using manual LF input mode
        if validated['has_lf_takeoffs']:
            # Validate manual LF inputs
            try:
                manual_lf = {}
                for trim_type, entry in self.manual_lf_inputs.items():
                    value = float(entry.get() or 0)
                    if not (0 <= value <= 10000):
                        messagebox.showerror("Invalid Input", f"{trim_type.replace('_', ' ').title()} LF must be between 0 and 10,000")
                        return None
                    manual_lf[trim_type] = value
                validated['manual_lf'] = manual_lf
            except ValueError:
                messagebox.showerror("Invalid Input", "LF values must be numbers")
                return None
        else:
            # Validate standard measurement inputs
            # Validate linear feet (float) - must be between 0 and 10000
            try:
                int_walls = float(self.inputs['int_walls_linear_ft'].get() or 0)
                ext_walls = float(self.inputs['ext_walls_linear_ft'].get() or 0)
                if not (0 <= int_walls <= 10000):
                    messagebox.showerror("Invalid Input", "Interior Walls must be between 0 and 10,000")
                    return None
                if not (0 <= ext_walls <= 10000):
                    messagebox.showerror("Invalid Input", "Exterior Walls must be between 0 and 10,000")
                    return None
                validated['int_walls_linear_ft'] = int_walls
                validated['ext_walls_linear_ft'] = ext_walls
            except ValueError:
                messagebox.showerror("Invalid Input", "Linear feet must be numbers")
                return None
            
            # Validate counts (integers) - must be between 0 and 10000
            try:
                ext_doors = int(self.inputs['ext_doors'].get() or 0)
                int_doors = int(self.inputs['int_doors'].get() or 0)
                trimmed_openings = int(self.inputs['trimmed_openings'].get() or 0)
                windows = int(self.inputs['windows'].get() or 0)
                sliders = int(self.inputs['sliders'].get() or 0)
                
                for name, value in [('Exterior Doors', ext_doors), ('Interior Doors', int_doors), 
                                   ('Trimmed Openings', trimmed_openings), ('Windows', windows), 
                                   ('Sliders', sliders)]:
                    if not (0 <= value <= 10000):
                        messagebox.showerror("Invalid Input", f"{name} must be between 0 and 10,000")
                        return None
                
                validated['ext_doors'] = ext_doors
                validated['int_doors'] = int_doors
                validated['trimmed_openings'] = trimmed_openings
                validated['windows'] = windows
                validated['sliders'] = sliders
            except ValueError:
                messagebox.showerror("Invalid Input", "Count fields must be whole numbers")
                return None
        
        # Get dropdown values
        validated['door_height'] = self.inputs['door_height'].get()
        validated['finish_level'] = self.inputs['finish_level'].get()
        validated['species'] = self.inputs['species'].get()
        
        # Get toggle values
        validated['wood_wrapped'] = self.inputs['wood_wrapped'].get()
        validated['has_schedule'] = self.inputs['has_schedule'].get()
        validated['schedule_file_path'] = self.inputs['schedule_file_path'].get()
        validated['is_finishing'] = self.inputs['is_finishing'].get()
        validated['finish_type'] = self.inputs['finish_type'].get() if self.inputs['is_finishing'].get() else ''
        
        return validated
    
    def calculate(self):
        """Calculate trim for all styles and display results"""
        # Validate inputs
        inputs = self.validate_inputs()
        if inputs is None:
            return
        
        # Get finish level from inputs
        finish_level = inputs['finish_level']
        
        # Store all results for export
        self.all_results = {
            'inputs': inputs,
            'styles': {}
        }
        
        # Check if using manual LF input
        if inputs.get('has_lf_takeoffs', False):
            # Use manual LF values directly (same for all styles)
            manual_lf = inputs.get('manual_lf', {})
            
            for style in TRIM_STYLES:
                # Use manual LF values
                lf_results = manual_lf.copy()
                
                # Still need to calculate BF - need dimensions from trim style
                # For manual mode, we'll use a default style (Craftsman) for dimensions
                bf_data = calculate_bf_with_waste(lf_results, 'craftsman', finish_level)
                
                # Store results
                self.all_results['styles'][style] = {
                    'lf': lf_results,
                    'bf': bf_data
                }
                
                # Display results
                self.display_results(style, lf_results, bf_data, inputs)
        else:
            # Standard calculation mode
            # Calculate for each trim style
            for style in TRIM_STYLES:
                # Calculate LF
                lf_results = calculate_trim(inputs, style, finish_level)
                
                # Calculate BF with waste
                bf_data = calculate_bf_with_waste(lf_results, style, finish_level)
                
                # Store results
                self.all_results['styles'][style] = {
                    'lf': lf_results,
                    'bf': bf_data
                }
                
                # Display results
                self.display_results(style, lf_results, bf_data, inputs)
    
    def display_results(self, style, lf_results, bf_data, inputs):
        """Display calculation results for a trim style"""
        text_widget = self.result_texts[style]
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        
        # Format results
        style_labels = {
            'craftsman': 'Craftsman',
            'mitered': 'Mitered',
            'built_up': 'Built-Up',
            'sill_apron_only': 'Sill/Apron Only'
        }
        style_label = style_labels.get(style, style.replace('_', ' ').title())
        
        output = f"Trim Style: {style_label}\n"
        output += f"Finish Level: {inputs['finish_level']}\n"
        output += f"Door Height: {inputs['door_height']}\n"
        output += "=" * 70 + "\n\n"
        
        # Display breakdown by trim type - showing BF required (after waste)
        output += "Breakdown by Trim Type:\n"
        output += "-" * 90 + "\n"
        output += f"{'Trim Type':<20} {'LF Needed':>12} {'BF Required':>15} {'Thickness (Stock)':>20} {'Width':>12}\n"
        output += "-" * 90 + "\n"
        
        # Order trim types for display
        trim_type_order = ['base', 'casing', 'headers', 'sills', 'apron', 'jambs', 'dentils']
        for trim_type in trim_type_order:
            if trim_type in lf_results:
                linear_ft = lf_results[trim_type]
                bf_required = bf_data['bf_with_waste'].get(trim_type, 0.0)
                width, finished_thickness = bf_data['dimensions'].get(trim_type, (0.0, 0.0))
                nominal_thickness = bf_data['nominal_thickness'].get(trim_type, 0.0)
                thickness_category = bf_data['thickness_category'].get(trim_type, '')
                
                if linear_ft > 0 or trim_type in ['base', 'casing']:  # Always show base and casing
                    # Show nominal stock thickness (what we order) and category
                    if nominal_thickness > 0:
                        thickness_str = f"{nominal_thickness:.2f}\" ({thickness_category})"
                    else:
                        thickness_str = ""
                    width_str = f"{width:.2f}\"" if width > 0 else ""
                    output += f"{trim_type.replace('_', ' ').title():<20} {linear_ft:>12.2f} {bf_required:>15.2f} {thickness_str:>20} {width_str:>12}\n"
        
        output += "-" * 90 + "\n"
        
        # Totals
        total_lf = sum(lf for lf in lf_results.values() if lf > 0)
        total_bf_required = sum(bf for bf in bf_data['bf_with_waste'].values())
        
        output += f"{'TOTALS':<20} {total_lf:>12.2f} {total_bf_required:>15.2f}\n"
        
        text_widget.insert(1.0, output)
        text_widget.config(state=tk.DISABLED)
    
    def export_to_csv(self):
        """Export all calculation results to CSV file"""
        if not self.all_results:
            messagebox.showwarning("No Data", "Please calculate trim first before exporting.")
            return
        
        # Generate filename: script_name_YYYYMMDD_HHMMSS.csv
        script_path = os.path.abspath(__file__)
        script_name = os.path.splitext(os.path.basename(script_path))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{script_name}_{timestamp}.csv"
        
        # Save in same directory as script
        script_dir = os.path.dirname(script_path)
        filepath = os.path.join(script_dir, filename)
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(['Trim Take-Off Calculator Results'])
                writer.writerow(['Generated:', datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
                writer.writerow([])
                
                # Write inputs section
                writer.writerow(['INPUTS'])
                inputs = self.all_results['inputs']
                writer.writerow(['Interior Walls (linear ft)', inputs.get('int_walls_linear_ft', 0)])
                writer.writerow(['Exterior Walls (linear ft)', inputs.get('ext_walls_linear_ft', 0)])
                writer.writerow(['Exterior Doors', inputs.get('ext_doors', 0)])
                writer.writerow(['Interior Doors', inputs.get('int_doors', 0)])
                writer.writerow(['Trimmed Openings', inputs.get('trimmed_openings', 0)])
                writer.writerow(['Windows', inputs.get('windows', 0)])
                writer.writerow(['Sliders', inputs.get('sliders', 0)])
                writer.writerow(['Door Height', inputs.get('door_height', '')])
                writer.writerow(['Finish Level', inputs.get('finish_level', '')])
                writer.writerow(['Species', inputs.get('species', '')])
                writer.writerow(['Wood Wrapped', inputs.get('wood_wrapped', False)])
                writer.writerow(['Has Schedule', inputs.get('has_schedule', False)])
                writer.writerow([])
                
                # Write results for each style
                style_labels = {
                    'craftsman': 'Craftsman',
                    'mitered': 'Mitered',
                    'built_up': 'Built-Up',
                    'sill_apron_only': 'Sill/Apron Only'
                }
                
                for style, data in self.all_results['styles'].items():
                    style_label = style_labels.get(style, style.replace('_', ' ').title())
                    writer.writerow([])
                    writer.writerow([f'STYLE: {style_label}'])
                    writer.writerow(['Trim Type', 'LF Needed', 'BF Required', 'Thickness Required (in)', 'Thickness Category'])
                    
                    lf_results = data['lf']
                    bf_data = data['bf']
                    trim_type_order = ['base', 'casing', 'headers', 'sills', 'apron', 'jambs', 'dentils']
                    
                    for trim_type in trim_type_order:
                        if trim_type in lf_results:
                            linear_ft = lf_results[trim_type]
                            bf_required = bf_data['bf_with_waste'].get(trim_type, 0.0)
                            nominal_thickness = bf_data['nominal_thickness'].get(trim_type, 0.0)
                            thickness_category = bf_data['thickness_category'].get(trim_type, '')
                            
                            if linear_ft > 0 or trim_type in ['base', 'casing']:
                                thickness_str = f'{nominal_thickness:.3f}' if nominal_thickness > 0 else ''
                                writer.writerow([
                                    trim_type.replace('_', ' ').title(),
                                    f'{linear_ft:.2f}',
                                    f'{bf_required:.2f}',
                                    thickness_str,
                                    thickness_category
                                ])
                    
                    # Style totals
                    total_lf = sum(lf for lf in lf_results.values() if lf > 0)
                    total_bf_required = sum(bf for bf in bf_data['bf_with_waste'].values())
                    writer.writerow(['TOTALS', f'{total_lf:.2f}', f'{total_bf_required:.2f}', '', ''])
            
            messagebox.showinfo("Export Successful", f"Results exported to:\n{filename}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export CSV:\n{str(e)}")
    
    def generate_invoice(self):
        """Generate Excel invoice with pricing"""
        if not self.all_results:
            messagebox.showwarning("No Data", "Please calculate trim first before generating invoice.")
            return
        
        # Validate pricing inputs
        try:
            lf_cost_per_ft = float(self.inputs['lf_cost_per_ft'].get() or 0.85)
            bf_markup_pct = float(self.inputs['bf_markup_pct'].get() or 20)
        except ValueError:
            messagebox.showerror("Invalid Input", "Pricing values must be numbers")
            return
        
        inputs = self.all_results['inputs']
        species = inputs.get('species', '')
        is_finishing = inputs.get('is_finishing', False)
        finish_type = inputs.get('finish_type', '')
        
        # Get invoice info
        job_name = self.inputs['job_name'].get() or ''
        customer_name = self.inputs['customer_name'].get() or ''
        try:
            sales_tax_rate = float(self.inputs['sales_tax_rate'].get() or 0.06)
        except ValueError:
            sales_tax_rate = 0.06
        
        try:
            # Generate invoice (will save to Output folder automatically)
            generate_invoice_excel(
                self.all_results,
                species,
                lf_cost_per_ft,
                bf_markup_pct,
                is_finishing,
                finish_type,
                job_name,
                customer_name,
                sales_tax_rate,
                None  # None = auto-generate path in Output folder
            )
            
            # Get the filename that was created
            script_path = os.path.abspath(__file__)
            script_dir = os.path.dirname(script_path)
            output_dir = os.path.join(script_dir, 'Output')
            
            # Find the most recent file
            if os.path.exists(output_dir):
                files = [f for f in os.listdir(output_dir) if f.endswith('.xlsx')]
                if files:
                    files.sort(key=lambda x: os.path.getmtime(os.path.join(output_dir, x)), reverse=True)
                    filename = files[0]
                else:
                    filename = "invoice.xlsx"
            else:
                filename = "invoice.xlsx"
            
            messagebox.showinfo("Invoice Generated", f"Invoice saved to:\nOutput/{filename}\n\nOld invoices moved to Output/archive")
        except Exception as e:
            import traceback
            error_msg = f"Failed to generate invoice:\n{str(e)}\n\n{traceback.format_exc()}"
            messagebox.showerror("Invoice Error", error_msg)

def main():
    try:
        root = tk.Tk()
        app = TrimCalculatorApp(root)
        root.mainloop()
    except Exception as e:
        # Show error dialog if GUI fails to start
        import traceback
        error_msg = f"Error starting application:\n\n{str(e)}\n\n{traceback.format_exc()}"
        try:
            messagebox.showerror("Startup Error", error_msg)
        except:
            # If messagebox fails, print to console
            print(error_msg)
            input("Press Enter to exit...")

if __name__ == "__main__":
    main()

