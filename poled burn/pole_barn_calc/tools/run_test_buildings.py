"""Test runner for 4 representative buildings with BOM/JSON exports."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from systems.pole_barn.calculator import PoleBarnCalculator
from systems.pole_barn.model import (
    PoleBarnInputs,
    GeometryInputs,
    MaterialInputs,
    PricingInputs,
    AssemblyInputs,
)
from systems.pole_barn.export_excel import export_bom_to_excel, generate_bom_filename
from systems.pole_barn.export_json import export_project_to_json, generate_json_filename
from systems.pole_barn.export_csv import export_bom_to_flat_csv, generate_flat_csv_filename


def create_test_building_a():
    """Test A - Small Basic Shop: 24×30, 10' eave, 4/12 pitch, Metal 29ga, No insulation, 1 man door, 0 windows."""
    geometry = GeometryInputs(
        length=30.0,
        width=24.0,
        eave_height=10.0,
        peak_height=None,  # Will be derived
        roof_pitch=4.0 / 12.0,  # 4/12
        roof_style="gable",
        ridge_position_ft_from_left=15.0,  # Centered
        overhang_front=1.0,
        overhang_rear=1.0,
        overhang_sides=1.0,
        door_count=1,
        door_width=3.0,
        door_height=6.67,  # 6/8
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=10.0,
        pole_spacing_width=12.0,
        pole_diameter=6.0,
        pole_depth=4.0,
        overhead_door_count=0,
        overhead_door_type="none",
    )
    
    materials = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
        exterior_finish_type="metal_29ga",
        wall_insulation_type="none",
        roof_insulation_type="none",
        girt_type="standard",
        wall_sheathing_type="none",
        roof_sheathing_type="none",
        floor_type="none",
    )
    
    pricing = PricingInputs(
        material_markup=1.15,
        tax_rate=0.08,
        material_markup_pct=15.0,
        labor_markup_pct=10.0,
        subcontractor_markup_pct=10.0,
        overhead_pct=0.0,
    )
    
    assemblies = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
        weather_sealing=False,
        post_type="pt_solid",
        post_truss_connection_type="notched",
    )
    
    return PoleBarnInputs(
        geometry=geometry,
        materials=materials,
        pricing=pricing,
        assemblies=assemblies,
        project_name="Test_A_SmallShop",
        build_type="pole",
        construction_type="new",
        building_type="residential",
    )


def create_test_building_b():
    """Test B - Standard 40×60 Shop: 40×60, 12' eave, 4/12 pitch, Metal 29ga, Wall batts, 2 man doors, 4 windows."""
    geometry = GeometryInputs(
        length=60.0,
        width=40.0,
        eave_height=12.0,
        peak_height=None,
        roof_pitch=4.0 / 12.0,
        roof_style="gable",
        ridge_position_ft_from_left=30.0,
        overhang_front=1.0,
        overhang_rear=1.0,
        overhang_sides=1.0,
        door_count=2,
        door_width=3.0,
        door_height=6.67,
        window_count=4,
        window_width=2.0,
        window_height=2.0,
        pole_spacing_length=10.0,
        pole_spacing_width=10.0,
        pole_diameter=6.0,
        pole_depth=4.0,
        overhead_door_count=0,
        overhead_door_type="none",
    )
    
    materials = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
        exterior_finish_type="metal_29ga",
        wall_insulation_type="fiberglass_batts",
        roof_insulation_type="none",
        girt_type="standard",
        wall_sheathing_type="none",
        roof_sheathing_type="none",
        floor_type="none",
    )
    
    pricing = PricingInputs(
        material_markup=1.15,
        tax_rate=0.08,
        material_markup_pct=15.0,
        labor_markup_pct=10.0,
        subcontractor_markup_pct=10.0,
        overhead_pct=0.0,
    )
    
    assemblies = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
        weather_sealing=False,
        post_type="pt_solid",
        post_truss_connection_type="notched",
    )
    
    return PoleBarnInputs(
        geometry=geometry,
        materials=materials,
        pricing=pricing,
        assemblies=assemblies,
        project_name="Test_B_40x60",
        build_type="pole",
        construction_type="new",
        building_type="residential",
    )


def create_test_building_c():
    """Test C - Large Commercial 50×80: 50×80, 16' eave, 3/12 pitch, Metal 26ga, Roof + wall insulation, 3 man doors, 6 windows."""
    geometry = GeometryInputs(
        length=80.0,
        width=50.0,
        eave_height=16.0,
        peak_height=None,
        roof_pitch=3.0 / 12.0,
        roof_style="gable",
        ridge_position_ft_from_left=40.0,
        overhang_front=2.0,
        overhang_rear=2.0,
        overhang_sides=2.0,
        door_count=3,
        door_width=3.0,
        door_height=6.67,
        window_count=6,
        window_width=3.0,
        window_height=4.0,
        pole_spacing_length=10.0,
        pole_spacing_width=10.0,
        pole_diameter=8.0,
        pole_depth=5.0,
        overhead_door_count=0,
        overhead_door_type="none",
    )
    
    materials = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
        exterior_finish_type="metal_26ga",
        wall_insulation_type="fiberglass_batts",
        roof_insulation_type="fiberglass_batts",
        girt_type="commercial",
        wall_sheathing_type="none",
        roof_sheathing_type="none",
        floor_type="none",
    )
    
    pricing = PricingInputs(
        material_markup=1.15,
        tax_rate=0.08,
        material_markup_pct=15.0,
        labor_markup_pct=10.0,
        subcontractor_markup_pct=10.0,
        overhead_pct=5.0,
    )
    
    assemblies = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
        weather_sealing=False,
        post_type="pt_solid",
        post_truss_connection_type="notched",
    )
    
    return PoleBarnInputs(
        geometry=geometry,
        materials=materials,
        pricing=pricing,
        assemblies=assemblies,
        project_name="Test_C_50x80_Commercial",
        build_type="pole",
        construction_type="new",
        building_type="commercial",
    )


def create_test_building_d():
    """Test D - Deluxe Hobby Barn 36×48: 36×48, 12' eave, 6/12 pitch, Roof sheathing + wall sheathing (plywood), Full insulation, 2 overhead doors, 3 man doors, 4 windows."""
    geometry = GeometryInputs(
        length=48.0,
        width=36.0,
        eave_height=12.0,
        peak_height=None,
        roof_pitch=6.0 / 12.0,
        roof_style="gable",
        ridge_position_ft_from_left=24.0,
        overhang_front=2.0,
        overhang_rear=2.0,
        overhang_sides=2.0,
        door_count=3,
        door_width=3.0,
        door_height=6.67,
        window_count=4,
        window_width=2.0,
        window_height=3.0,
        pole_spacing_length=12.0,
        pole_spacing_width=12.0,
        pole_diameter=6.0,
        pole_depth=4.0,
        overhead_door_count=2,
        overhead_door_type="steel_rollup",
    )
    
    materials = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=12.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
        exterior_finish_type="metal_29ga",
        wall_insulation_type="fiberglass_batts",
        roof_insulation_type="fiberglass_batts",
        girt_type="standard",
        wall_sheathing_type="plywood",
        roof_sheathing_type="plywood",
        floor_type="slab",
        slab_thickness_in=4.0,
        slab_reinforcement="mesh",
    )
    
    pricing = PricingInputs(
        material_markup=1.15,
        tax_rate=0.08,
        material_markup_pct=15.0,
        labor_markup_pct=10.0,
        subcontractor_markup_pct=10.0,
        overhead_pct=0.0,
    )
    
    assemblies = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
        weather_sealing=True,
        post_type="pt_solid",
        post_truss_connection_type="notched",
    )
    
    return PoleBarnInputs(
        geometry=geometry,
        materials=materials,
        pricing=pricing,
        assemblies=assemblies,
        project_name="Test_D_36x48_Deluxe",
        build_type="pole",
        construction_type="new",
        building_type="residential",
    )


def main():
    """Run all test buildings and generate exports."""
    # Create test exports directory
    project_root = Path(__file__).parent.parent
    test_dir = project_root / "test_exports"
    test_dir.mkdir(exist_ok=True)
    
    print("=" * 70)
    print("POLE BARN CALCULATOR - TEST BUILDING EXPORTS")
    print("=" * 70)
    print()
    
    # Initialize calculator
    config_dir = project_root / "config"
    calculator = PoleBarnCalculator(config_dir=config_dir)
    calculator.load_config()
    
    # Define test buildings
    test_buildings = [
        ("Test_A_SmallShop", create_test_building_a),
        ("Test_B_40x60", create_test_building_b),
        ("Test_C_50x80_Commercial", create_test_building_c),
        ("Test_D_36x48_Deluxe", create_test_building_d),
    ]
    
    results = []
    
    # Process each test building
    for test_name, create_func in test_buildings:
        print(f"Processing {test_name}...")
        
        try:
            # Create inputs
            inputs = create_func()
            
            # Run calculation
            geom_model, takeoff, priced_items, summary, bom_items = calculator.calculate(inputs)
            
            # Generate filenames
            excel_filename = f"{test_name}_bom.xlsx"
            json_filename = f"{test_name}_project.json"
            
            excel_path = test_dir / excel_filename
            json_path = test_dir / json_filename
            
            # Export Excel BOM
            export_bom_to_excel(bom_items, excel_path, inputs.project_name)
            
            # Export CSV BOM (flat)
            csv_filename = f"{test_name}_bom_flat.csv"
            csv_path = test_dir / csv_filename
            export_bom_to_flat_csv(bom_items, csv_path, project_name=inputs.project_name, building_id=test_name)
            
            # Export JSON project
            export_project_to_json(
                inputs,
                geom_model,
                takeoff,
                bom_items,
                priced_items,
                summary,
                json_path,
            )
            
            results.append({
                "name": test_name,
                "excel": excel_path,
                "csv": csv_path,
                "json": json_path,
            })
            
            print(f"  [OK] Excel: {excel_path}")
            print(f"  [OK] CSV:   {csv_path}")
            print(f"  [OK] JSON:  {json_path}")
            print()
            
        except Exception as e:
            print(f"  [ERROR] {e}")
            import traceback
            traceback.print_exc()
            print()
    
    # Print final summary
    print("=" * 70)
    print("TEST EXPORTS COMPLETE")
    print("=" * 70)
    print()
    print("Files generated:")
    print()
    
    for result in results:
        print(f"{result['name']}:")
        print(f"  - Excel: {result['excel']}")
        print(f"  - CSV:   {result['csv']}")
        print(f"  - JSON:  {result['json']}")
        print()
    
    print(f"All files saved in: {test_dir}")
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()

