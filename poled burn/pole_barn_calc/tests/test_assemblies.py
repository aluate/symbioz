"""Tests for assembly and material quantity calculations."""

import pytest
from systems.pole_barn.model import (
    PoleBarnInputs,
    GeometryInputs,
    MaterialInputs,
    PricingInputs,
    AssemblyInputs,
    AssemblyQuantity,
    MaterialTakeoff,
)
from systems.pole_barn import assemblies
from systems.pole_barn import geometry


def test_calculate_material_quantities():
    """Test the main material quantities calculation function."""
    # Build geometry model
    geometry_inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,  # 4:12
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
    
    geom_model = geometry.build_geometry_model(geometry_inputs)
    
    material_inputs = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,  # Same as bay spacing
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
    )
    
    assembly_inputs = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    quantities = assemblies.calculate_material_quantities(
        geom_model, material_inputs, assembly_inputs
    )
    
    # Should have multiple items
    assert len(quantities) > 0
    
    # Check for key categories
    categories = {item.category for item in quantities}
    assert "framing" in categories
    assert "roof" in categories
    assert "wall" in categories
    assert "trim" in categories
    
    # Check for specific items
    names = {item.name for item in quantities}
    assert "posts" in names
    assert "trusses" in names
    assert "sidewall_girts" in names
    assert "roof_purlins" in names
    assert "roof_panels" in names
    assert "sidewall_panels" in names
    assert "endwall_panels" in names
    assert "eave_trim" in names
    assert "rake_trim" in names
    assert "base_trim" in names
    assert "corner_trim" in names


def test_post_count_calculation():
    """Test post count calculation."""
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
        pole_spacing_length=10.0,  # 40/10 = 4 bays, 5 frame lines
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    geom_model = geometry.build_geometry_model(geometry_inputs)
    material_inputs = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
    )
    assembly_inputs = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    quantities = assemblies.calculate_material_quantities(
        geom_model, material_inputs, assembly_inputs
    )
    
    posts_item = next((item for item in quantities if item.name == "posts"), None)
    assert posts_item is not None
    assert posts_item.quantity == 10  # 5 frame lines × 2 sidewalls
    assert posts_item.unit == "ea"
    assert posts_item.category == "framing"


def test_truss_count_calculation():
    """Test truss count calculation."""
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
        pole_spacing_length=10.0,  # 4 bays, 5 frame lines
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    geom_model = geometry.build_geometry_model(geometry_inputs)
    material_inputs = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,  # Same as bay spacing
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
    )
    assembly_inputs = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    quantities = assemblies.calculate_material_quantities(
        geom_model, material_inputs, assembly_inputs
    )
    
    trusses_item = next((item for item in quantities if item.name == "trusses"), None)
    assert trusses_item is not None
    assert trusses_item.quantity == 5  # One per frame line
    assert trusses_item.unit == "ea"


def test_girt_calculation():
    """Test girt quantity calculation."""
    geometry_inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,  # 12ft height
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
    
    geom_model = geometry.build_geometry_model(geometry_inputs)
    material_inputs = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,  # 12ft / 2ft = 6 rows
        foundation_type="concrete_pad",
    )
    assembly_inputs = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    quantities = assemblies.calculate_material_quantities(
        geom_model, material_inputs, assembly_inputs
    )
    
    sidewall_girts_item = next(
        (item for item in quantities if item.name == "sidewall_girts"), None
    )
    assert sidewall_girts_item is not None
    # 6 rows × 40ft × 2 sidewalls = 480 LF
    assert sidewall_girts_item.quantity == pytest.approx(480.0)
    assert sidewall_girts_item.unit == "lf"


def test_roof_panel_calculation():
    """Test roof panel quantity calculation."""
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
    
    geom_model = geometry.build_geometry_model(geometry_inputs)
    material_inputs = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
    )
    assembly_inputs = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    quantities = assemblies.calculate_material_quantities(
        geom_model, material_inputs, assembly_inputs
    )
    
    roof_panels_item = next(
        (item for item in quantities if item.name == "roof_panels"), None
    )
    assert roof_panels_item is not None
    assert roof_panels_item.quantity == pytest.approx(geom_model.roof_area_sqft)
    assert roof_panels_item.unit == "sqft"
    assert roof_panels_item.category == "roof"


def test_wall_panel_calculation():
    """Test wall panel quantity calculation."""
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
    
    geom_model = geometry.build_geometry_model(geometry_inputs)
    material_inputs = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
    )
    assembly_inputs = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    quantities = assemblies.calculate_material_quantities(
        geom_model, material_inputs, assembly_inputs
    )
    
    sidewall_panels_item = next(
        (item for item in quantities if item.name == "sidewall_panels"), None
    )
    assert sidewall_panels_item is not None
    assert sidewall_panels_item.quantity == pytest.approx(960.0)  # 2 × 40 × 12
    assert sidewall_panels_item.unit == "sqft"
    
    endwall_panels_item = next(
        (item for item in quantities if item.name == "endwall_panels"), None
    )
    assert endwall_panels_item is not None
    assert endwall_panels_item.quantity == pytest.approx(720.0)  # 2 × 30 × 12
    assert endwall_panels_item.unit == "sqft"


def test_trim_calculation():
    """Test trim quantity calculations."""
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
    
    geom_model = geometry.build_geometry_model(geometry_inputs)
    material_inputs = MaterialInputs(
        roof_material_type="metal",
        wall_material_type="metal",
        truss_type="standard",
        truss_spacing=10.0,
        purlin_spacing=2.0,
        girt_spacing=2.0,
        foundation_type="concrete_pad",
    )
    assembly_inputs = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
    )
    
    quantities = assemblies.calculate_material_quantities(
        geom_model, material_inputs, assembly_inputs
    )
    
    # Check trim items
    eave_trim = next((item for item in quantities if item.name == "eave_trim"), None)
    assert eave_trim is not None
    assert eave_trim.quantity == pytest.approx(80.0)  # 2 × 40
    assert eave_trim.unit == "lf"
    
    rake_trim = next((item for item in quantities if item.name == "rake_trim"), None)
    assert rake_trim is not None
    assert rake_trim.quantity == pytest.approx(60.0)  # 2 × 30
    assert rake_trim.unit == "lf"
    
    base_trim = next((item for item in quantities if item.name == "base_trim"), None)
    assert base_trim is not None
    assert base_trim.quantity == pytest.approx(140.0)  # 2 × (40 + 30)
    assert base_trim.unit == "lf"
    
    corner_trim = next((item for item in quantities if item.name == "corner_trim"), None)
    assert corner_trim is not None
    assert corner_trim.quantity == pytest.approx(48.0)  # 4 × 12
    assert corner_trim.unit == "lf"


def test_legacy_functions():
    """Test that legacy function signatures still work."""
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
    )
    
    # Test legacy functions
    truss_count = assemblies.calculate_truss_quantity(inputs)
    assert truss_count == 5
    
    purlin_result = assemblies.calculate_purlin_quantity(inputs)
    assert "total_length_lf" in purlin_result
    assert purlin_result["total_length_lf"] > 0
    
    girt_result = assemblies.calculate_girt_quantity(inputs)
    assert "total_length_lf" in girt_result
    assert girt_result["total_length_lf"] > 0
    
    roofing_result = assemblies.calculate_roofing_material(inputs)
    assert "quantity" in roofing_result
    assert roofing_result["quantity"] > 0
    
    wall_result = assemblies.calculate_wall_material(inputs)
    assert "total_quantity" in wall_result
    assert wall_result["total_quantity"] > 0


def test_insulation_calculation():
    """Test insulation quantity calculation."""
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
        insulation_type="fiberglass",
        insulation_r_value=19.0,
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
    )
    
    insulation_result = assemblies.calculate_insulation_quantity(inputs)
    assert insulation_result["insulation_type"] == "fiberglass"
    assert insulation_result["quantity"] > 0
    assert insulation_result["r_value"] == 19.0


def test_ventilation_calculation():
    """Test ventilation quantity calculation."""
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
    
    pricing = PricingInputs(
        material_markup=1.15,
        tax_rate=0.08,
        labor_rate=50.0,
    )
    
    assemblies_input = AssemblyInputs(
        assembly_method="standard",
        fastening_type="screws",
        ventilation_type="ridge_vent",
        ventilation_count=2,
    )
    
    inputs = PoleBarnInputs(
        geometry=geometry_inputs,
        materials=materials,
        pricing=pricing,
        assemblies=assemblies_input,
    )
    
    ventilation_result = assemblies.calculate_ventilation_quantity(inputs)
    assert ventilation_result["ventilation_type"] == "ridge_vent"
    assert ventilation_result["count"] == 2


def test_get_assembly_summary():
    """Test assembly summary function."""
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
    )
    
    summary = assemblies.get_assembly_summary(inputs)
    
    assert "total_items" in summary
    assert "by_category" in summary
    assert summary["total_items"] > 0
    assert "framing" in summary["by_category"]
    assert "roof" in summary["by_category"]
    assert "wall" in summary["by_category"]
    assert "trim" in summary["by_category"]
