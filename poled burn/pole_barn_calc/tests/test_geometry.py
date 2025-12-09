"""Tests for geometry calculations."""

import pytest
import math
from systems.pole_barn.model import GeometryInputs, GeometryModel
from systems.pole_barn import geometry


def test_geometry_inputs_creation():
    """Test that GeometryInputs can be created with required fields."""
    geometry_inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=2.0,
        overhang_rear=2.0,
        overhang_sides=1.0,
        door_count=2,
        door_width=12.0,
        door_height=10.0,
        window_count=4,
        window_width=3.0,
        window_height=2.0,
        pole_spacing_length=8.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    assert geometry_inputs.length == 40.0
    assert geometry_inputs.width == 30.0
    assert geometry_inputs.eave_height == 12.0
    assert geometry_inputs.peak_height == 16.0  # Can still be provided explicitly


def test_peak_height_derivation():
    """Test that peak height is derived when not provided."""
    geometry_inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=None,  # Not provided - should be derived
        roof_pitch=0.333,  # 4:12 pitch
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
    
    model = geometry.build_geometry_model(geometry_inputs)
    
    # For 30ft width, 4:12 pitch, centered ridge:
    # run = 30 / 2 = 15ft
    # rise = 15 * 0.333 = 5ft
    # peak_height = 12 + 5 = 17ft
    expected_peak = 12.0 + (30.0 / 2.0) * 0.333
    assert model.peak_height_ft == pytest.approx(expected_peak, rel=1e-2)
    assert model.peak_height_ft > geometry_inputs.eave_height


def test_build_geometry_model():
    """Test building a complete geometry model."""
    inputs = GeometryInputs(
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
    
    model = geometry.build_geometry_model(inputs)
    
    # Check dimensions
    assert model.overall_length_ft == 40.0
    assert model.overall_width_ft == 30.0
    assert model.eave_height_ft == 12.0
    assert model.peak_height_ft == 16.0
    
    # Check overhangs
    assert model.sidewall_overhang_ft == 1.0
    assert model.endwall_overhang_front_ft == 1.0
    assert model.endwall_overhang_rear_ft == 1.0
    
    # Check bays
    assert model.bay_spacing_ft == 10.0
    assert model.num_bays == 4  # ceil(40 / 10) = 4
    assert model.num_frame_lines == 5  # bays + 1
    
    # Check footprint area
    assert model.footprint_area_sqft == pytest.approx(1200.0)  # 40 * 30
    
    # Check wall areas
    sidewall_area_expected = 2 * 40.0 * 12.0  # 2 sidewalls
    endwall_area_expected = 2 * 30.0 * 12.0  # 2 endwalls
    assert model.sidewall_area_sqft == pytest.approx(sidewall_area_expected)
    assert model.endwall_area_sqft == pytest.approx(endwall_area_expected)
    assert model.total_wall_area_sqft == pytest.approx(
        sidewall_area_expected + endwall_area_expected
    )
    
    # Check roof area (with pitch and overhangs)
    # Effective length: 40 + 1 + 1 = 42
    # Effective width: 30 + 2*1 = 32
    # Plan area: 42 * 32 = 1344
    # Slope factor for 4:12 (0.333): sqrt(1 + 0.333^2) = sqrt(1.111) ≈ 1.054
    # Roof area: 1344 * 1.054 ≈ 1416.6
    L_eff = 40.0 + 1.0 + 1.0
    W_eff = 30.0 + 2 * 1.0
    plan_area = L_eff * W_eff
    slope_factor = math.sqrt(1 + 0.333 ** 2)
    expected_roof_area = plan_area * slope_factor
    assert model.roof_area_sqft == pytest.approx(expected_roof_area, rel=1e-3)
    
    # Check volume
    expected_volume = 40.0 * 30.0 * 12.0
    assert model.building_volume_cuft == pytest.approx(expected_volume)


def test_calculate_roof_area():
    """Test roof area calculation."""
    inputs = GeometryInputs(
        length=60.0,
        width=40.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,  # 4:12
        overhang_front=2.0,
        overhang_rear=2.0,
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
    
    roof_area = geometry.calculate_roof_area(inputs)
    
    # Manual calculation
    L_eff = 60.0 + 2.0 + 2.0  # 64
    W_eff = 40.0 + 2 * 1.0  # 42
    plan_area = L_eff * W_eff  # 2688
    slope_factor = math.sqrt(1 + 0.333 ** 2)
    expected = plan_area * slope_factor
    
    assert roof_area == pytest.approx(expected, rel=1e-3)
    assert roof_area > plan_area  # Roof area should be larger than plan area


def test_calculate_wall_area():
    """Test wall area calculation."""
    inputs = GeometryInputs(
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
    
    wall_areas = geometry.calculate_wall_area(inputs)
    
    assert wall_areas['front'] == pytest.approx(30.0 * 12.0)
    assert wall_areas['rear'] == pytest.approx(30.0 * 12.0)
    assert wall_areas['left'] == pytest.approx(40.0 * 12.0)
    assert wall_areas['right'] == pytest.approx(40.0 * 12.0)


def test_calculate_floor_area():
    """Test floor area calculation."""
    inputs = GeometryInputs(
        length=50.0,
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
    
    floor_area = geometry.calculate_floor_area(inputs)
    assert floor_area == pytest.approx(50.0 * 30.0)


def test_calculate_door_window_openings():
    """Test door and window opening calculations."""
    inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=0.0,
        overhang_rear=0.0,
        overhang_sides=0.0,
        door_count=2,
        door_width=12.0,
        door_height=10.0,
        window_count=4,
        window_width=3.0,
        window_height=2.0,
        pole_spacing_length=8.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    openings = geometry.calculate_door_window_openings(inputs)
    
    expected_door_area = 2 * 12.0 * 10.0  # 240
    expected_window_area = 4 * 3.0 * 2.0  # 24
    
    assert openings['door_area'] == pytest.approx(expected_door_area)
    assert openings['window_area'] == pytest.approx(expected_window_area)


def test_calculate_roof_volume():
    """Test roof volume calculation."""
    inputs = GeometryInputs(
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
    
    volume = geometry.calculate_roof_volume(inputs)
    expected = 40.0 * 30.0 * 12.0
    assert volume == pytest.approx(expected)


def test_get_geometry_summary():
    """Test geometry summary function."""
    inputs = GeometryInputs(
        length=40.0,
        width=30.0,
        eave_height=12.0,
        peak_height=16.0,
        roof_pitch=0.333,
        overhang_front=1.0,
        overhang_rear=1.0,
        overhang_sides=1.0,
        door_count=1,
        door_width=10.0,
        door_height=8.0,
        window_count=2,
        window_width=2.0,
        window_height=2.0,
        pole_spacing_length=10.0,
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    summary = geometry.get_geometry_summary(inputs)
    
    assert 'dimensions' in summary
    assert 'overhangs' in summary
    assert 'bays' in summary
    assert 'areas' in summary
    assert 'volume' in summary
    assert 'openings' in summary
    
    assert summary['dimensions']['length_ft'] == 40.0
    assert summary['bays']['num_bays'] == 4
    assert summary['openings']['door_area'] == pytest.approx(80.0)


def test_pole_count_raises_not_implemented():
    """Test that pole count calculation still raises NotImplementedError."""
    inputs = GeometryInputs(
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
    
    with pytest.raises(NotImplementedError):
        geometry.calculate_pole_count(inputs)


def test_bay_calculation_edge_cases():
    """Test bay calculations with edge cases."""
    # Test exact division
    inputs = GeometryInputs(
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
        pole_spacing_length=10.0,  # Exactly divides 40
        pole_spacing_width=8.0,
        pole_diameter=6.0,
        pole_depth=4.0,
    )
    
    model = geometry.build_geometry_model(inputs)
    assert model.num_bays == 4
    assert model.num_frame_lines == 5
    
    # Test non-exact division (should round up)
    inputs.pole_spacing_length = 7.0  # 40/7 = 5.71, should round up to 6
    model = geometry.build_geometry_model(inputs)
    assert model.num_bays == 6
    assert model.num_frame_lines == 7
