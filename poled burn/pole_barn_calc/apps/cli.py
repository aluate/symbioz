"""Command-line interface for pole barn calculator."""

import click
import json
from pathlib import Path
from systems.pole_barn.model import (
    PoleBarnInputs,
    GeometryInputs,
    MaterialInputs,
    PricingInputs,
    AssemblyInputs,
)
from systems.pole_barn.calculator import PoleBarnCalculator
from systems.pole_barn import geometry as geometry_module
from systems.pole_barn import assemblies as assemblies_module


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


@click.command()
@click.option("--project-name", help="Project name or identifier")
@click.option("--length", type=float, required=True, help="Length of barn in feet")
@click.option("--width", type=float, required=True, help="Width of barn in feet")
@click.option("--eave-height", type=float, required=True, help="Eave height in feet")
@click.option("--peak-height", type=float, default=None, help="Peak height in feet (optional, will be derived if not provided)")
@click.option("--roof-pitch", type=str, required=True, help="Roof pitch (e.g., '4/12', '3/12', or 0.333)")
@click.option("--roof-style", type=click.Choice(["gable", "shed"]), default="gable", help="Roof style: gable or shed")
@click.option("--ridge-position", type=float, default=None, help="Ridge position from left eave in feet (default: centered)")
@click.option("--overhang-front", type=float, default=0.0, help="Front overhang in feet")
@click.option("--overhang-rear", type=float, default=0.0, help="Rear overhang in feet")
@click.option("--overhang-sides", type=float, default=0.0, help="Side overhangs in feet")
@click.option("--door-count", type=int, default=0, help="Number of doors")
@click.option("--door-width", type=float, default=0.0, help="Door width in feet")
@click.option("--door-height", type=float, default=0.0, help="Door height in feet")
@click.option("--window-count", type=int, default=0, help="Number of windows")
@click.option("--window-width", type=float, default=0.0, help="Window width in feet")
@click.option("--window-height", type=float, default=0.0, help="Window height in feet")
@click.option("--overhead-door-count", type=int, default=0, help="Number of overhead/roll-up doors")
@click.option("--overhead-door-type", type=click.Choice(["none", "steel_rollup", "sectional"]), default="none", help="Overhead door type")
@click.option("--pole-spacing-length", type=float, required=True, help="Pole spacing along length in feet")
@click.option("--pole-spacing-width", type=float, required=True, help="Pole spacing along width in feet")
@click.option("--pole-diameter", type=float, required=True, help="Pole diameter in inches")
@click.option("--pole-depth", type=float, required=True, help="Pole depth in ground in feet")
@click.option("--roof-material", type=str, required=True, help="Roof material type (e.g., metal, shingle)")
@click.option("--roof-gauge", type=float, help="Roof gauge (for metal roofing)")
@click.option("--wall-material", type=str, required=True, help="Wall material type (e.g., metal, wood)")
@click.option("--wall-gauge", type=float, help="Wall gauge (for metal walls)")
@click.option("--truss-type", type=str, required=True, help="Truss type (e.g., scissor, standard, gambrel)")
@click.option("--truss-spacing", type=float, required=True, help="Truss spacing in feet")
@click.option("--purlin-spacing", type=float, required=True, help="Purlin spacing in feet")
@click.option("--girt-spacing", type=float, required=True, help="Girt spacing in feet")
@click.option("--foundation-type", type=str, required=True, help="Foundation type (e.g., concrete_pad, gravel)")
@click.option("--concrete-thickness", type=float, help="Concrete thickness in inches")
@click.option("--insulation-type", type=str, help="Insulation type (e.g., fiberglass, spray_foam) [deprecated]")
@click.option("--insulation-r-value", type=float, help="Insulation R-value [deprecated]")
@click.option("--exterior-finish-type", type=click.Choice(["metal_29ga", "metal_26ga", "lap_siding", "stucco"]), default="metal_29ga", help="Exterior finish type")
@click.option("--wall-insulation-type", type=click.Choice(["none", "fiberglass_batts", "rock_wool", "rigid_board", "spray_foam"]), default="none", help="Wall insulation type")
@click.option("--roof-insulation-type", type=click.Choice(["none", "fiberglass_batts", "rock_wool", "rigid_board", "spray_foam"]), default="none", help="Roof insulation type")
@click.option("--girt-type", type=click.Choice(["standard", "commercial"]), default="standard", help="Girt type: standard or commercial")
@click.option("--wall-sheathing-type", type=click.Choice(["none", "osb", "plywood"]), default="none", help="Wall sheathing type")
@click.option("--roof-sheathing-type", type=click.Choice(["none", "osb", "plywood"]), default="none", help="Roof sheathing type")
@click.option("--floor-type", type=click.Choice(["none", "slab", "gravel"]), default="none", help="Floor type")
@click.option("--slab-thickness", type=float, default=None, help="Slab thickness in inches (if floor-type is slab)")
@click.option("--slab-reinforcement", type=click.Choice(["none", "mesh", "rebar"]), default="none", help="Slab reinforcement type")
@click.option("--post-type", type=click.Choice(["pt_solid", "laminated"]), default="pt_solid", help="Post type: pt_solid or laminated")
@click.option("--post-truss-connection", type=click.Choice(["notched", "cleated"]), default="notched", help="Truss/post connection type")
@click.option("--labor-rate", type=float, default=None, help="Labor rate per hour (optional, defaults to 50.0)")
@click.option("--material-markup", type=float, default=None, help="Material markup multiplier (e.g., 1.15 for 15%%) - legacy, use --material-markup-pct instead")
@click.option("--material-markup-pct", type=float, default=None, help="Material markup as percentage (e.g., 15.0 for 15%%)")
@click.option("--labor-markup-pct", type=float, default=None, help="Labor markup as percentage (e.g., 10.0 for 10%%)")
@click.option("--subcontractor-markup-pct", type=float, default=None, help="Subcontractor markup as percentage (e.g., 10.0 for 10%%)")
@click.option("--overhead-pct", type=float, default=None, help="Overhead as percentage of (material + labor) (e.g., 5.0 for 5%%)")
@click.option("--tax-rate", type=float, required=True, help="Tax rate as decimal (e.g., 0.08 for 8%%)")
@click.option("--delivery-cost", type=float, help="Delivery cost")
@click.option("--permit-cost", type=float, help="Permit cost")
@click.option("--site-prep-cost", type=float, help="Site preparation cost")
@click.option("--include-electrical", is_flag=True, help="Include basic electrical")
@click.option("--electrical-allowance", type=float, default=0.0, help="Electrical allowance in dollars")
@click.option("--include-plumbing", is_flag=True, help="Include plumbing")
@click.option("--plumbing-allowance", type=float, default=0.0, help="Plumbing allowance in dollars")
@click.option("--include-mechanical", is_flag=True, help="Include mechanical (heat/vent)")
@click.option("--mechanical-allowance", type=float, default=0.0, help="Mechanical allowance in dollars")
@click.option("--build-type", type=click.Choice(["pole", "stick_frame"]), default="pole", help="Build type: pole or stick_frame")
@click.option("--construction-type", type=click.Choice(["new", "addition"]), default="new", help="Construction type: new or addition")
@click.option("--building-type", type=click.Choice(["residential", "commercial"]), default="residential", help="Building type: residential or commercial")
@click.option("--building-use", type=str, default=None, help="Building use/description")
@click.option("--permitting-agency", type=str, default=None, help="Permitting agency")
@click.option("--required-snow-load", type=float, default=None, help="Required snow load in psf")
@click.option("--requested-snow-load", type=float, default=None, help="Requested snow load in psf")
@click.option("--snow-load-unknown", is_flag=True, help="Flag if snow load needs lookup")
@click.option("--assembly-method", type=str, required=True, help="Assembly method (e.g., standard, prefab)")
@click.option("--fastening-type", type=str, required=True, help="Fastening type (e.g., screws, nails)")
@click.option("--weather-sealing", is_flag=True, help="Include weather sealing")
@click.option("--ventilation-type", type=str, help="Ventilation type (e.g., ridge_vent, gable_vent)")
@click.option("--ventilation-count", type=int, help="Number of ventilation units")
@click.option("--skylight-count", type=int, help="Number of skylights")
@click.option("--skylight-size", type=float, help="Skylight size in square feet")
@click.option("--notes", type=str, help="Additional notes or special requirements")
@click.option("--output-format", type=click.Choice(["summary", "json", "detailed"]), default="summary", help="Output format")
@click.option("--export-bom-excel", is_flag=True, help="Export BOM to Excel file")
@click.option("--export-bom-csv", type=click.Path(), default=None, help="Export BOM to flat CSV file (provide path or directory)")
@click.option("--export-json", is_flag=True, help="Export full project to JSON file")
def main(
    project_name,
    length,
    width,
    eave_height,
    peak_height,
    roof_pitch,
    roof_style,
    ridge_position,
    overhang_front,
    overhang_rear,
    overhang_sides,
    door_count,
    door_width,
    door_height,
    window_count,
    window_width,
    window_height,
    overhead_door_count,
    overhead_door_type,
    pole_spacing_length,
    pole_spacing_width,
    pole_diameter,
    pole_depth,
    roof_material,
    roof_gauge,
    wall_material,
    wall_gauge,
    truss_type,
    truss_spacing,
    purlin_spacing,
    girt_spacing,
    foundation_type,
    concrete_thickness,
    insulation_type,
    insulation_r_value,
    exterior_finish_type,
    wall_insulation_type,
    roof_insulation_type,
    girt_type,
    wall_sheathing_type,
    roof_sheathing_type,
    floor_type,
    slab_thickness,
    slab_reinforcement,
    post_type,
    post_truss_connection,
    labor_rate,
    material_markup,
    material_markup_pct,
    labor_markup_pct,
    subcontractor_markup_pct,
    overhead_pct,
    tax_rate,
    delivery_cost,
    permit_cost,
    site_prep_cost,
    include_electrical,
    electrical_allowance,
    include_plumbing,
    plumbing_allowance,
    include_mechanical,
    mechanical_allowance,
    build_type,
    construction_type,
    building_type,
    building_use,
    permitting_agency,
    required_snow_load,
    requested_snow_load,
    snow_load_unknown,
    assembly_method,
    fastening_type,
    weather_sealing,
    ventilation_type,
    ventilation_count,
    skylight_count,
    skylight_size,
    notes,
    output_format,
    export_bom_csv,
):
    """Pole Barn Calculator - Calculate materials and costs for pole barn construction."""
    
    # Parse roof pitch (can be "4/12", "3/12", or "0.333")
    try:
        roof_pitch_ratio = parse_roof_pitch(roof_pitch)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        return
    
    # Determine ridge position (default to centered if not provided for gable roofs)
    ridge_pos = ridge_position
    if roof_style == "gable" and ridge_pos is None:
        ridge_pos = length / 2.0
    
    # Build geometry inputs
    # Peak height is optional - will be derived if not provided (per changelog entry [4])
    geometry = GeometryInputs(
        length=length,
        width=width,
        eave_height=eave_height,
        peak_height=peak_height,  # None if not provided, will be derived
        roof_pitch=roof_pitch_ratio,
        roof_style=roof_style,
        ridge_position_ft_from_left=ridge_pos if roof_style == "gable" else None,
        overhang_front=overhang_front,
        overhang_rear=overhang_rear,
        overhang_sides=overhang_sides,
        door_count=door_count,
        door_width=door_width,
        door_height=door_height,
        window_count=window_count,
        window_width=window_width,
        window_height=window_height,
        pole_spacing_length=pole_spacing_length,
        pole_spacing_width=pole_spacing_width,
        pole_diameter=pole_diameter,
        pole_depth=pole_depth,
        overhead_door_count=overhead_door_count,
        overhead_door_type=overhead_door_type,
    )
    
    # Build material inputs
    materials = MaterialInputs(
        roof_material_type=roof_material,
        roof_gauge=roof_gauge,
        wall_material_type=wall_material,
        wall_gauge=wall_gauge,
        truss_type=truss_type,
        truss_spacing=truss_spacing,
        purlin_spacing=purlin_spacing,
        girt_spacing=girt_spacing,
        foundation_type=foundation_type if floor_type == "none" else floor_type,
        concrete_thickness=concrete_thickness if slab_thickness is None else slab_thickness,
        insulation_type=insulation_type,
        insulation_r_value=insulation_r_value,
        exterior_finish_type=exterior_finish_type,
        wall_insulation_type=wall_insulation_type,
        roof_insulation_type=roof_insulation_type,
        girt_type=girt_type,
        wall_sheathing_type=wall_sheathing_type,
        roof_sheathing_type=roof_sheathing_type,
        floor_type=floor_type,
        slab_thickness_in=slab_thickness,
        slab_reinforcement=slab_reinforcement,
    )
    
    # Build pricing inputs
    # Labor rate uses default if not provided (per changelog entry [4])
    # Handle material_markup: use material_markup_pct if provided, otherwise use legacy material_markup
    if material_markup_pct is not None:
        # New percentage-based markup
        material_markup_value = 1.0 + (material_markup_pct / 100.0)  # Convert 15% to 1.15 for backward compat
    elif material_markup is not None:
        # Legacy multiplier format
        material_markup_value = material_markup
    else:
        # Default to 15% if neither provided
        material_markup_value = 1.15
    
    pricing = PricingInputs(
        material_markup=material_markup_value,  # Legacy field for backward compatibility
        tax_rate=tax_rate,
        labor_rate=labor_rate if labor_rate is not None else 50.0,  # Default 50.0 if not provided
        delivery_cost=delivery_cost,
        permit_cost=permit_cost,
        site_prep_cost=site_prep_cost,
        include_electrical=include_electrical,
        electrical_allowance=electrical_allowance,
        include_plumbing=include_plumbing,
        plumbing_allowance=plumbing_allowance,
        include_mechanical=include_mechanical,
        mechanical_allowance=mechanical_allowance,
        material_markup_pct=material_markup_pct if material_markup_pct is not None else 15.0,
        labor_markup_pct=labor_markup_pct if labor_markup_pct is not None else 10.0,
        subcontractor_markup_pct=subcontractor_markup_pct if subcontractor_markup_pct is not None else 10.0,
        overhead_pct=overhead_pct if overhead_pct is not None else 0.0,
    )
    
    # Build assembly inputs
    assemblies = AssemblyInputs(
        assembly_method=assembly_method,
        fastening_type=fastening_type,
        weather_sealing=weather_sealing,
        ventilation_type=ventilation_type,
        ventilation_count=ventilation_count,
        skylight_count=skylight_count,
        skylight_size=skylight_size,
        post_type=post_type,
        post_truss_connection_type=post_truss_connection,
    )
    
    # Build complete inputs
    inputs = PoleBarnInputs(
        geometry=geometry,
        materials=materials,
        pricing=pricing,
        assemblies=assemblies,
        project_name=project_name,
        notes=notes,
        build_type=build_type,
        construction_type=construction_type,
        building_type=building_type,
        building_use=building_use,
        permitting_agency=permitting_agency,
        required_snow_load_psf=required_snow_load,
        requested_snow_load_psf=requested_snow_load,
        snow_load_unknown=snow_load_unknown,
    )
    
    # Create calculator and run full calculation
    # Use explicit config_dir for consistency
    config_dir = Path(__file__).parent.parent / "config"
    calculator = PoleBarnCalculator(config_dir=config_dir)
    
    try:
        calculator.load_config()
        geom_model, takeoff, priced_items, pricing_summary, bom_items = calculator.calculate(inputs)
        openings = geometry_module.calculate_door_window_openings(geometry)
    except Exception as e:
        click.echo(f"Error during calculation: {e}", err=True)
        import traceback
        if output_format == "detailed":
            click.echo(traceback.format_exc(), err=True)
        return
    
    # Display input summary
    click.echo("=" * 60)
    click.echo("POLE BARN CALCULATOR")
    click.echo("=" * 60)
    
    if project_name:
        click.echo(f"\nProject: {project_name}")
    
    click.echo(f"\nDimensions: {length}ft x {width}ft")
    # Peak height is derived - get it from the geometry model
    click.echo(f"Height: Eave {eave_height}ft, Peak {geom_model.peak_height_ft:.2f}ft (derived)")
    click.echo(f"Roof Pitch: {roof_pitch} ({roof_pitch_ratio:.4f} ratio)")
    click.echo(f"Roof Style: {roof_style}")
    click.echo(f"Pole Spacing: {pole_spacing_length}ft x {pole_spacing_width}ft")
    click.echo(f"Materials: {roof_material} roof, {wall_material} walls")
    click.echo(f"Truss Type: {truss_type}")
    
    # Display geometry results (Phase 1)
    click.echo("\n" + "=" * 60)
    click.echo("GEOMETRY CALCULATIONS (Phase 1 - Implemented)")
    click.echo("=" * 60)
    click.echo(f"\nBays & Frames:")
    click.echo(f"  Bay Spacing: {geom_model.bay_spacing_ft}ft")
    click.echo(f"  Number of Bays: {geom_model.num_bays}")
    click.echo(f"  Number of Frame Lines: {geom_model.num_frame_lines}")
    
    click.echo(f"\nAreas:")
    click.echo(f"  Footprint: {geom_model.footprint_area_sqft:.2f} sq ft")
    click.echo(f"  Sidewalls: {geom_model.sidewall_area_sqft:.2f} sq ft")
    click.echo(f"  Endwalls: {geom_model.endwall_area_sqft:.2f} sq ft")
    click.echo(f"  Total Walls: {geom_model.total_wall_area_sqft:.2f} sq ft")
    click.echo(f"  Roof: {geom_model.roof_area_sqft:.2f} sq ft")
    
    if geom_model.building_volume_cuft:
        click.echo(f"\nVolume:")
        click.echo(f"  Building Volume: {geom_model.building_volume_cuft:.2f} cu ft")
    
    if openings['door_area'] > 0 or openings['window_area'] > 0:
        click.echo(f"\nOpenings:")
        if openings['door_area'] > 0:
            click.echo(f"  Door Area: {openings['door_area']:.2f} sq ft")
        if openings['window_area'] > 0:
            click.echo(f"  Window Area: {openings['window_area']:.2f} sq ft")
    
    # Display material quantities (Phase 2)
    if takeoff.items:
        click.echo("\n" + "=" * 60)
        click.echo("MATERIAL QUANTITIES (Phase 2 - Implemented)")
        click.echo("=" * 60)
        
        # Group by category
        by_category = {}
        for item in takeoff.items:
            if item.category not in by_category:
                by_category[item.category] = []
            by_category[item.category].append(item)
        
        # Display framing
        if "framing" in by_category:
            click.echo(f"\nFraming:")
            for item in by_category["framing"]:
                click.echo(f"  {item.description}: {item.quantity:.1f} {item.unit}")
        
        # Display roof
        if "roof" in by_category:
            click.echo(f"\nRoof:")
            for item in by_category["roof"]:
                click.echo(f"  {item.description}: {item.quantity:.1f} {item.unit}")
        
        # Display walls
        if "wall" in by_category:
            click.echo(f"\nWalls:")
            for item in by_category["wall"]:
                click.echo(f"  {item.description}: {item.quantity:.1f} {item.unit}")
        
        # Display trim
        if "trim" in by_category:
            click.echo(f"\nTrim:")
            for item in by_category["trim"]:
                click.echo(f"  {item.description}: {item.quantity:.1f} {item.unit}")
    
    # Display pricing (Phase 3)
    if priced_items:
        click.echo("\n" + "=" * 60)
        click.echo("COST BREAKDOWN (Phase 3 - Implemented)")
        click.echo("=" * 60)
        
        # Group priced items by category
        priced_by_category = {}
        for item in priced_items:
            if item.category not in priced_by_category:
                priced_by_category[item.category] = []
            priced_by_category[item.category].append(item)
        
        # Display major line items
        click.echo("\nMajor Line Items:")
        for category in ["framing", "roof", "wall", "trim"]:
            if category in priced_by_category:
                click.echo(f"\n{category.title()}:")
                for item in priced_by_category[category]:
                    if item.total_cost > 0:
                        click.echo(
                            f"  {item.description}: "
                            f"{item.quantity:.1f} {item.unit} @ ${item.unit_price:.2f}/{item.unit} = "
                            f"${item.total_cost:.2f}"
                        )
        
        # Display summary
        click.echo("\n" + "-" * 60)
        click.echo("COST SUMMARY")
        click.echo("-" * 60)
        click.echo(f"Material Subtotal: ${pricing_summary.material_subtotal:,.2f}")
        click.echo(f"Labor Subtotal:    ${pricing_summary.labor_subtotal:,.2f}")
        click.echo(f"Markup Total:      ${pricing_summary.markup_total:,.2f}")
        if pricing_summary.overhead_total > 0:
            click.echo(f"Overhead Total:    ${pricing_summary.overhead_total:,.2f}")
        click.echo(f"Tax Total:         ${pricing_summary.tax_total:,.2f}")
        click.echo("-" * 60)
        click.echo(f"GRAND TOTAL:       ${pricing_summary.grand_total:,.2f}")
        click.echo("=" * 60)
    
    # Handle exports
    if export_bom_excel:
        from systems.pole_barn.export_excel import export_bom_to_excel, generate_bom_filename
        excel_filename = generate_bom_filename(project_name)
        excel_path = Path.cwd() / excel_filename
        export_bom_to_excel(bom_items, excel_path, project_name)
        click.echo(f"\nBOM exported to: {excel_path}")
    
    if export_bom_csv:
        from systems.pole_barn.export_csv import export_bom_to_flat_csv
        
        csv_path = Path(export_bom_csv)
        export_bom_to_flat_csv(bom_items, csv_path, project_name=project_name, building_id="CLI")
        click.echo(f"\nBOM (CSV) exported to: {csv_path}")
    
    if export_json:
        from systems.pole_barn.export_json import export_project_to_json, generate_json_filename
        json_filename = generate_json_filename(project_name)
        json_path = Path.cwd() / json_filename
        export_project_to_json(
            inputs,
            geom_model,
            takeoff,
            bom_items,
            priced_items,
            pricing_summary,
            json_path,
        )
        click.echo(f"\nProject exported to: {json_path}")
    
    if output_format == "json":
        # Convert to dictionaries for JSON
        quantities_dict = [
            {
                "name": item.name,
                "description": item.description,
                "category": item.category,
                "quantity": item.quantity,
                "unit": item.unit,
                "notes": item.notes,
            }
            for item in takeoff.items
        ]
        
        priced_items_dict = [
            {
                "name": item.name,
                "description": item.description,
                "category": item.category,
                "quantity": item.quantity,
                "unit": item.unit,
                "part_id": item.part_id,
                "unit_price": item.unit_price,
                "material_cost": item.material_cost,
                "labor_hours": item.labor_hours,
                "labor_cost": item.labor_cost,
                "markup_percent": item.markup_percent,
                "markup_amount": item.markup_amount,
                "total_cost": item.total_cost,
                "notes": item.notes,
            }
            for item in priced_items
        ]
        
        click.echo("\n" + json.dumps({
            "project_name": project_name,
            "geometry": {
                "dimensions": {
                    "length_ft": length,
                    "width_ft": width,
                    "eave_height_ft": eave_height,
                    "peak_height_ft": peak_height,
                },
                "bays": {
                    "bay_spacing_ft": geom_model.bay_spacing_ft,
                    "num_bays": geom_model.num_bays,
                    "num_frame_lines": geom_model.num_frame_lines,
                },
                "areas": {
                    "footprint_sqft": geom_model.footprint_area_sqft,
                    "sidewall_sqft": geom_model.sidewall_area_sqft,
                    "endwall_sqft": geom_model.endwall_area_sqft,
                    "total_wall_sqft": geom_model.total_wall_area_sqft,
                    "roof_sqft": geom_model.roof_area_sqft,
                },
                "volume_cuft": geom_model.building_volume_cuft,
                "openings": openings,
            },
            "material_quantities": quantities_dict,
            "priced_items": priced_items_dict,
            "pricing_summary": {
                "material_subtotal": pricing_summary.material_subtotal,
                "labor_subtotal": pricing_summary.labor_subtotal,
                "markup_total": pricing_summary.markup_total,
                "tax_total": pricing_summary.tax_total,
                "grand_total": pricing_summary.grand_total,
            },
            "status": "all_phases_implemented",
        }, indent=2))
    elif output_format == "detailed":
        click.echo("\n" + "=" * 60)
        click.echo("DETAILED GEOMETRY SUMMARY")
        click.echo("=" * 60)
        click.echo(json.dumps(geom_summary, indent=2))


if __name__ == "__main__":
    main()

