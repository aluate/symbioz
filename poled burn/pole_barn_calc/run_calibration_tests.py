"""Script to run pricing calibration test cases."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from systems.pole_barn.model import (
    PoleBarnInputs,
    GeometryInputs,
    MaterialInputs,
    PricingInputs,
    AssemblyInputs,
)
from systems.pole_barn.calculator import PoleBarnCalculator


def create_test_a():
    """TEST A — Basic 30x40 Shop"""
    geometry = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=None,  # Will be derived
        roof_pitch=4/12,  # 4/12 = 0.333
        roof_style="gable",
        ridge_position_ft_from_left=20.0,  # Centered
        overhang_front=1.0,
        overhang_rear=1.0,
        overhang_sides=1.0,
        door_count=1,
        door_width=3.0,  # 3/0 = 36"
        door_height=6.67,  # 6/8 = 80" = 6.67'
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=10.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
        overhead_door_count=1,
        overhead_door_type="steel_rollup",
    )
    
    materials = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="gravel",
        exterior_finish_type="metal_29ga",
        wall_insulation_type="none",
        roof_insulation_type="none",
        floor_type="gravel",
        girt_type="standard",
        wall_sheathing_type="none",
        roof_sheathing_type="none",
    )
    
    pricing = PricingInputs(
        material_markup=1.15,  # 15% markup
        tax_rate=0.08,  # 8% tax
        labor_rate=50.0,
        include_electrical=False,
        electrical_allowance=0.0,
        include_plumbing=False,
        plumbing_allowance=0.0,
        include_mechanical=False,
        mechanical_allowance=0.0,
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
        project_name="TEST A - Basic 30x40 Shop",
        build_type="pole",
        construction_type="new",
        building_type="residential",
    )


def create_test_b():
    """TEST B — Standard 40x60 Shop"""
    geometry = GeometryInputs(
        length=60.0,
        width=40.0,
        eave_height=12.0,
        peak_height=None,
        roof_pitch=4/12,
        roof_style="gable",
        ridge_position_ft_from_left=30.0,  # Centered
        overhang_front=1.0,
        overhang_rear=1.0,
        overhang_sides=1.0,
        door_count=2,
        door_width=3.0,
        door_height=6.67,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=10.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
        overhead_door_count=2,
        overhead_door_type="steel_rollup",
    )
    
    materials = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="gravel",
        exterior_finish_type="metal_29ga",
        wall_insulation_type="none",
        roof_insulation_type="none",
        floor_type="gravel",
        girt_type="standard",
        wall_sheathing_type="none",
        roof_sheathing_type="none",
    )
    
    pricing = PricingInputs(
        material_markup=1.15,
        tax_rate=0.08,
        labor_rate=50.0,
        include_electrical=False,
        electrical_allowance=0.0,
        include_plumbing=False,
        plumbing_allowance=0.0,
        include_mechanical=False,
        mechanical_allowance=0.0,
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
        project_name="TEST B - Standard 40x60 Shop",
        build_type="pole",
        construction_type="new",
        building_type="residential",
    )


def create_test_c():
    """TEST C — Insulated 40x60"""
    geometry = GeometryInputs(
        length=60.0,
        width=40.0,
        eave_height=12.0,
        peak_height=None,
        roof_pitch=4/12,
        roof_style="gable",
        ridge_position_ft_from_left=30.0,
        overhang_front=1.0,
        overhang_rear=1.0,
        overhang_sides=1.0,
        door_count=2,
        door_width=3.0,
        door_height=6.67,
        window_count=3,
        window_width=3.0,
        window_height=2.0,
        pole_spacing_length=10.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
        overhead_door_count=2,
        overhead_door_type="steel_rollup",
    )
    
    materials = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="gravel",
        exterior_finish_type="metal_29ga",
        wall_insulation_type="fiberglass_batts",
        roof_insulation_type="fiberglass_batts",
        floor_type="gravel",
        girt_type="standard",
        wall_sheathing_type="none",
        roof_sheathing_type="none",
    )
    
    pricing = PricingInputs(
        material_markup=1.15,
        tax_rate=0.08,
        labor_rate=50.0,
        include_electrical=False,
        electrical_allowance=0.0,
        include_plumbing=False,
        plumbing_allowance=0.0,
        include_mechanical=False,
        mechanical_allowance=0.0,
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
        project_name="TEST C - Insulated 40x60",
        build_type="pole",
        construction_type="new",
        building_type="residential",
    )


def create_test_d():
    """TEST D — Large 40x80 Shop"""
    geometry = GeometryInputs(
        length=80.0,
        width=40.0,
        eave_height=12.0,
        peak_height=None,
        roof_pitch=4/12,
        roof_style="gable",
        ridge_position_ft_from_left=40.0,
        overhang_front=1.0,
        overhang_rear=1.0,
        overhang_sides=1.0,
        door_count=3,
        door_width=3.0,
        door_height=6.67,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=10.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
        overhead_door_count=3,
        overhead_door_type="steel_rollup",
    )
    
    materials = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="gravel",
        exterior_finish_type="metal_29ga",
        wall_insulation_type="none",
        roof_insulation_type="none",
        floor_type="gravel",
        girt_type="standard",
        wall_sheathing_type="none",
        roof_sheathing_type="none",
    )
    
    pricing = PricingInputs(
        material_markup=1.15,
        tax_rate=0.08,
        labor_rate=50.0,
        include_electrical=False,
        electrical_allowance=0.0,
        include_plumbing=False,
        plumbing_allowance=0.0,
        include_mechanical=False,
        mechanical_allowance=0.0,
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
        project_name="TEST D - Large 40x80 Shop",
        build_type="pole",
        construction_type="new",
        building_type="residential",
    )


def run_test(test_name, inputs):
    """Run a test case and return results."""
    print(f"\n{'='*60}")
    print(f"Running {test_name}")
    print(f"{'='*60}")
    
    config_dir = Path(__file__).parent / "config"
    calculator = PoleBarnCalculator(config_dir=config_dir)
    
    try:
        calculator.load_config()
        geom_model, takeoff, priced_items, summary = calculator.calculate(inputs)
        
        footprint = geom_model.footprint_area_sqft
        cost_per_sqft = summary.grand_total / footprint if footprint > 0 else 0
        
        print(f"Dimensions: {inputs.geometry.length}ft × {inputs.geometry.width}ft")
        print(f"Footprint: {footprint:.1f} sq ft")
        print(f"Total Cost: ${summary.grand_total:,.2f}")
        print(f"Cost per sq ft: ${cost_per_sqft:.2f}")
        print(f"\nBreakdown:")
        print(f"  Material: ${summary.material_subtotal:,.2f}")
        print(f"  Labor: ${summary.labor_subtotal:,.2f}")
        print(f"  Markup: ${summary.markup_total:,.2f}")
        print(f"  Tax: ${summary.tax_total:,.2f}")
        
        return {
            'test_name': test_name,
            'dimensions': f"{int(inputs.geometry.length)}×{int(inputs.geometry.width)}",
            'footprint_sqft': footprint,
            'total_cost': summary.grand_total,
            'cost_per_sqft': cost_per_sqft,
            'material_subtotal': summary.material_subtotal,
            'labor_subtotal': summary.labor_subtotal,
            'markup_total': summary.markup_total,
            'tax_total': summary.tax_total,
        }
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Run all calibration tests."""
    print("Pricing Calibration Test Runner")
    print("="*60)
    
    results = []
    
    # Run all tests
    test_a = create_test_a()
    result_a = run_test("TEST A - Basic 30x40 Shop", test_a)
    if result_a:
        results.append(result_a)
    
    test_b = create_test_b()
    result_b = run_test("TEST B - Standard 40x60 Shop", test_b)
    if result_b:
        results.append(result_b)
    
    test_c = create_test_c()
    result_c = run_test("TEST C - Insulated 40x60", test_c)
    if result_c:
        results.append(result_c)
    
    test_d = create_test_d()
    result_d = run_test("TEST D - Large 40x80 Shop", test_d)
    if result_d:
        results.append(result_d)
    
    # Summary table
    print(f"\n{'='*60}")
    print("SUMMARY TABLE")
    print(f"{'='*60}")
    print(f"{'Test':<25} {'Dimensions':<12} {'Sq Ft':<8} {'Total Cost':<12} {'$/sqft':<10}")
    print("-"*60)
    for r in results:
        print(f"{r['test_name']:<25} {r['dimensions']:<12} {r['footprint_sqft']:>7.0f} "
              f"${r['total_cost']:>10,.0f} ${r['cost_per_sqft']:>8.2f}")
    
    print(f"\n{'='*60}")
    print("Copy the results above into PRICING_CALIBRATION.md")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()

