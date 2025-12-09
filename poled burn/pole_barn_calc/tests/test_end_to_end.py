"""End-to-end tests for the pole barn calculator."""

import pytest
from systems.pole_barn.model import (
    PoleBarnInputs,
    GeometryInputs,
    MaterialInputs,
    PricingInputs,
    AssemblyInputs,
)
from systems.pole_barn.calculator import PoleBarnCalculator
from systems.pole_barn import geometry
from systems.pole_barn import assemblies
from pathlib import Path


def test_calculator_initialization():
    """Test that PoleBarnCalculator can be initialized."""
    geometry = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=0.0,
        overhang_rear=0.0,
        overhang_sides=0.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=8.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    materials = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=2.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
    )
    
    pricing = PricingInputs(
        material_markup=1.15,
        tax_rate=0.08,
        labor_rate=50.0,
    )
    
    assemblies = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    inputs = PoleBarnInputs(
        geometry=geometry,
        materials=materials,
        pricing=pricing,
        assemblies=assemblies,
        project_name="Test Barn",
    )
    
    calculator = PoleBarnCalculator(inputs)
    assert calculator.inputs == inputs
    assert calculator.inputs.project_name == "Test Barn"


def test_calculator_methods_not_implemented():
    """Test that calculator methods raise NotImplementedError."""
    geometry = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=0.0,
        overhang_rear=0.0,
        overhang_sides=0.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=8.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    materials = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=2.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
    )
    
    pricing = PricingInputs(
        material_markup=1.15,
        tax_rate=0.08,
        labor_rate=50.0,
    )
    
    assemblies = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    inputs = PoleBarnInputs(
        geometry=geometry,
        materials=materials,
        pricing=pricing,
        assemblies=assemblies,
    )
    
    calculator = PoleBarnCalculator(inputs)
    
    with pytest.raises(NotImplementedError):
        calculator.calculate_geometry()
    
    with pytest.raises(NotImplementedError):
        calculator.calculate_quantities()
    
    with pytest.raises(NotImplementedError):
        calculator.calculate_costs()
    
    with pytest.raises(NotImplementedError):
        calculator.calculate_all()
    
    with pytest.raises(NotImplementedError):
        calculator.get_summary()


def test_geometry_with_pole_barn_inputs():
    """Test that geometry calculations work with PoleBarnInputs."""
    geometry_inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,  # 4:12 pitch
        overhang_front=1.0,
        overhang_rear=1.0,
        overhang_sides=1.0,
        door_count=2,
        door_width=12.0,
        door_height=10.0,
        window_count=4,
        window_width=3.0,
        window_height=2.0,
        pole_spacing_length=10.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    materials = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=2.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
    )
    
    pricing = PricingInputs(
        material_markup=1.15,
        tax_rate=0.08,
        labor_rate=50.0,
    )
    
    assemblies = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    inputs = PoleBarnInputs(
        geometry=geometry_inputs,
        materials=materials,
        pricing=pricing,
        assemblies=assemblies,
        project_name="Test Barn",
    )
    
    # Test that we can build geometry model from PoleBarnInputs
    model = geometry.build_geometry_model(inputs.geometry)
    
    assert model.overall_length_ft == 40.0
    assert model.overall_width_ft == 30.0
    assert model.num_bays == 4  # ceil(40/10) = 4
    assert model.footprint_area_sqft == pytest.approx(1200.0)  # 40 * 30
    
    # Test that geometry summary works
    summary = geometry.get_geometry_summary(inputs.geometry)
    assert 'areas' in summary
    assert summary['areas']['footprint_sqft'] == pytest.approx(1200.0)
    
    # Test door/window openings
    openings = geometry.calculate_door_window_openings(inputs.geometry)
    assert openings['door_area'] == pytest.approx(240.0)  # 2 * 12 * 10
    assert openings['window_area'] == pytest.approx(24.0)  # 4 * 3 * 2


def test_assemblies_with_pole_barn_inputs():
    """Test that assembly calculations work with PoleBarnInputs."""
    geometry_inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,  # 4:12 pitch
        overhang_front=1.0,
        overhang_rear=1.0,
        overhang_sides=1.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=10.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    materials = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
    )
    
    pricing = PricingInputs(
        material_markup=1.15,
        tax_rate=0.08,
        labor_rate=50.0,
    )
    
    assemblies_input = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    inputs = PoleBarnInputs(
        geometry=geometry_inputs,
        materials=materials,
        pricing=pricing,
        assemblies=assemblies_input,
        project_name="Test Barn",
    )
    
    # Build geometry model
    geom_model = geometry.build_geometry_model(inputs.geometry)
    
    # Calculate material quantities
    quantities = assemblies.calculate_material_quantities(
        geom_model, inputs.materials, inputs.assemblies
    )
    
    # Should have multiple items
    assert len(quantities) > 0
    
    # Check for key items
    names = {item.name for item in quantities}
    assert "posts" in names
    assert "trusses" in names
    assert "roof_panels" in names
    assert "sidewall_panels" in names
    
    # Test assembly summary
    summary = assemblies.get_assembly_summary(inputs)
    assert summary["total_items"] > 0
    assert "by_category" in summary
    
    # Test that quantities are reasonable
    posts_item = next((item for item in quantities if item.name == "posts"), None)
    assert posts_item is not None
    assert posts_item.quantity > 0
    assert posts_item.unit == "ea"


def test_full_calculator_pipeline():
    """Test the complete calculator pipeline from inputs to costs."""
    geometry_inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=1.0,
        overhang_rear=1.0,
        overhang_sides=1.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=10.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    materials = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
    )
    
    pricing_inputs = PricingInputs(
        labor_rate=50.0,
        material_markup=1.15,  # 15% markup
        tax_rate=0.08,  # 8% tax
    )
    
    assemblies_input = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    inputs = PoleBarnInputs(
        geometry=geometry_inputs,
        materials=materials,
        pricing=pricing_inputs,
        assemblies=assemblies_input,
        project_name="Test Barn",
    )
    
    # Create calculator and run full calculation
    calculator = PoleBarnCalculator(inputs)
    calculator.load_config()
    
    geom_model, takeoff, priced_items, summary = calculator.calculate()
    
    # Verify geometry
    assert geom_model is not None
    assert geom_model.overall_length_ft == 40.0
    assert geom_model.overall_width_ft == 30.0
    
    # Verify quantities
    assert len(takeoff.items) > 0
    assert any(item.name == "posts" for item in takeoff.items)
    assert any(item.name == "roof_panels" for item in takeoff.items)
    
    # Verify pricing
    assert len(priced_items) > 0
    assert summary.material_subtotal > 0
    assert summary.grand_total > 0
    
    # Verify totals are consistent
    calculated_material = sum(item.material_cost for item in priced_items)
    assert summary.material_subtotal == pytest.approx(calculated_material)
    
    # Verify grand total includes all components
    expected_total = (
        summary.material_subtotal +
        summary.labor_subtotal +
        summary.markup_total +
        summary.tax_total
    )
    assert summary.grand_total == pytest.approx(expected_total)


def test_calculator_summary():
    """Test calculator summary method."""
    geometry_inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=0.0,
        overhang_rear=0.0,
        overhang_sides=0.0,
        door_count=0,
        door_width=0.0,
        door_height=0.0,
        window_count=0,
        window_width=0.0,
        window_height=0.0,
        pole_spacing_length=10.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    materials = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
    )
    
    pricing_inputs = PricingInputs(
        labor_rate=50.0,
        material_markup=1.15,
        tax_rate=0.08,
    )
    
    assemblies_input = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    inputs = PoleBarnInputs(
        geometry=geometry_inputs,
        materials=materials,
        pricing=pricing_inputs,
        assemblies=assemblies_input,
        project_name="Summary Test",
    )
    
    calculator = PoleBarnCalculator(inputs)
    calculator.load_config()
    
    summary = calculator.get_summary()
    
    assert "geometry" in summary
    assert "quantities" in summary
    assert "costs" in summary
    assert summary["costs"]["grand_total"] > 0
    assert summary["project_name"] == "Summary Test"

