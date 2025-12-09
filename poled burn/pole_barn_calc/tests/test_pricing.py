"""Tests for pricing calculations."""

import pytest
from pathlib import Path
from systems.pole_barn.model import (
    MaterialTakeoff,
    AssemblyQuantity,
    PricingInputs,
    PricedLineItem,
    PricingSummary,
)
from systems.pole_barn import pricing


def test_load_parts():
    """Test loading parts CSV."""
    parts_df = pricing.load_parts()
    
    assert len(parts_df) > 0
    assert "part_id" in parts_df.columns
    assert "part_name" in parts_df.columns
    
    # Check for expected parts
    part_ids = parts_df["part_id"].tolist()
    assert "POST_6X6_PT" in part_ids
    assert "METAL_PANEL_29_SQFT" in part_ids


def test_load_pricing():
    """Test loading pricing CSV."""
    pricing_df = pricing.load_pricing()
    
    assert len(pricing_df) > 0
    assert "part_id" in pricing_df.columns
    assert "unit_price" in pricing_df.columns
    
    # Check for expected pricing
    pricing_dict = dict(zip(pricing_df["part_id"], pricing_df["unit_price"]))
    assert "POST_6X6_PT" in pricing_dict
    assert pricing_dict["POST_6X6_PT"] > 0


def test_load_assemblies():
    """Test loading assemblies CSV."""
    assemblies_df = pricing.load_assemblies()
    
    assert len(assemblies_df) > 0
    assert "assembly_name" in assemblies_df.columns


def test_find_assembly_mapping():
    """Test finding assembly mapping."""
    assemblies_df = pricing.load_assemblies()
    
    # Test finding an existing assembly
    mapping = pricing.find_assembly_mapping(assemblies_df, "ROOF-STANDARD")
    assert mapping is not None
    assert "part_id" in mapping
    assert "waste_factor" in mapping
    
    # Test non-existent assembly
    mapping = pricing.find_assembly_mapping(assemblies_df, "NONEXISTENT")
    assert mapping is None


def test_find_part_record():
    """Test finding part record."""
    parts_df = pricing.load_parts()
    
    part_record = pricing.find_part_record(parts_df, "POST_6X6_PT")
    assert part_record is not None
    assert part_record["part_id"] == "POST_6X6_PT"
    assert "part_name" in part_record
    
    # Test non-existent part
    part_record = pricing.find_part_record(parts_df, "NONEXISTENT")
    assert part_record is None


def test_find_unit_price():
    """Test finding unit price."""
    pricing_df = pricing.load_pricing()
    
    unit_price = pricing.find_unit_price(pricing_df, "POST_6X6_PT")
    assert unit_price is not None
    assert unit_price > 0
    
    # Test non-existent part
    unit_price = pricing.find_unit_price(pricing_df, "NONEXISTENT")
    assert unit_price is None


def test_price_material_takeoff():
    """Test pricing a material takeoff."""
    # Create a simple takeoff
    takeoff = MaterialTakeoff(items=[
        AssemblyQuantity(
            name="posts",
            description="Structural posts",
            category="framing",
            quantity=10.0,
            unit="ea",
        ),
        AssemblyQuantity(
            name="roof_panels",
            description="Roof panels",
            category="roof",
            quantity=1000.0,
            unit="sqft",
        ),
    ])
    
    pricing_inputs = PricingInputs(
        material_markup=1.15,  # 15% markup
        tax_rate=0.08,  # 8% tax
        labor_rate=50.0,  # Default labor rate
    )
    
    parts_df = pricing.load_parts()
    pricing_df = pricing.load_pricing()
    assemblies_df = pricing.load_assemblies()
    
    priced_items, summary = pricing.price_material_takeoff(
        takeoff, pricing_inputs, parts_df, pricing_df, assemblies_df
    )
    
    # Should have priced items
    assert len(priced_items) == 2
    
    # Check posts item
    posts_item = next((item for item in priced_items if item.name == "posts"), None)
    assert posts_item is not None
    # Posts have waste_factor 1.0, so effective quantity = 10.0
    assert posts_item.quantity == pytest.approx(10.0)
    assert posts_item.unit == "ea"
    assert posts_item.material_cost > 0
    assert posts_item.total_cost > 0
    
    # Check roof panels item
    roof_item = next((item for item in priced_items if item.name == "roof_panels"), None)
    assert roof_item is not None
    # Roof panels have waste_factor 1.05, so effective quantity = 1000 * 1.05 = 1050
    assert roof_item.quantity == pytest.approx(1050.0)
    assert roof_item.unit == "sqft"
    assert roof_item.material_cost > 0
    assert roof_item.total_cost > 0
    
    # Check summary
    assert summary.material_subtotal > 0
    assert summary.markup_total > 0
    assert summary.tax_total > 0
    assert summary.grand_total > 0
    
    # Verify totals match
    calculated_material = sum(item.material_cost for item in priced_items)
    calculated_markup = sum(item.markup_amount for item in priced_items)
    assert summary.material_subtotal == pytest.approx(calculated_material)
    assert summary.markup_total == pytest.approx(calculated_markup)


def test_price_material_takeoff_with_markup():
    """Test that markup is applied correctly (ONLY to material, not labor - per changelog entry [4])."""
    takeoff = MaterialTakeoff(items=[
        AssemblyQuantity(
            name="roof_panels",
            description="Roof panels",
            category="roof",
            quantity=100.0,
            unit="sqft",
        ),
    ])
    
    # 20% markup
    pricing_inputs = PricingInputs(
        material_markup=1.20,
        tax_rate=0.0,
        labor_rate=50.0,  # Non-zero labor rate to verify markup doesn't apply to labor
    )
    
    parts_df = pricing.load_parts()
    pricing_df = pricing.load_pricing()
    assemblies_df = pricing.load_assemblies()
    
    priced_items, summary = pricing.price_material_takeoff(
        takeoff, pricing_inputs, parts_df, pricing_df, assemblies_df
    )
    
    item = priced_items[0]
    # Markup should be 20% of material cost ONLY, not labor
    expected_markup = item.material_cost * 0.20
    assert item.markup_percent == pytest.approx(20.0)
    assert item.markup_amount == pytest.approx(expected_markup)
    # Total cost = material + labor + markup (markup does NOT include labor)
    assert item.total_cost == pytest.approx(item.material_cost + item.labor_cost + item.markup_amount)
    
    # Verify markup is NOT applied to labor
    # If markup included labor, it would be: (material + labor) * 0.20
    # But it should be: material * 0.20
    markup_with_labor = (item.material_cost + item.labor_cost) * 0.20
    assert item.markup_amount < markup_with_labor  # Should be less if labor > 0


def test_price_material_takeoff_with_waste_factor():
    """Test that waste_factor is applied to quantities."""
    takeoff = MaterialTakeoff(items=[
        AssemblyQuantity(
            name="roof_panels",
            description="Roof panels",
            category="roof",
            quantity=100.0,  # Base quantity
            unit="sqft",
        ),
    ])
    
    pricing_inputs = PricingInputs(
        material_markup=1.0,  # No markup for simplicity
        tax_rate=0.0,
        labor_rate=0.0,  # No labor for this test
    )
    
    parts_df = pricing.load_parts()
    pricing_df = pricing.load_pricing()
    assemblies_df = pricing.load_assemblies()
    
    priced_items, summary = pricing.price_material_takeoff(
        takeoff, pricing_inputs, parts_df, pricing_df, assemblies_df
    )
    
    item = priced_items[0]
    # Waste factor for roof_panels should be 1.05 (5% waste)
    # So effective quantity should be 100 * 1.05 = 105
    assert item.quantity == pytest.approx(105.0)  # 100 * 1.05
    # Unit price is 1.16, so material cost should be 105 * 1.16 = 121.80
    assert item.material_cost == pytest.approx(105.0 * 1.16)


def test_price_material_takeoff_with_labor():
    """Test that labor_per_unit is used to calculate labor costs."""
    takeoff = MaterialTakeoff(items=[
        AssemblyQuantity(
            name="posts",
            description="Posts",
            category="framing",
            quantity=10.0,
            unit="ea",
        ),
    ])
    
    pricing_inputs = PricingInputs(
        material_markup=1.0,
        tax_rate=0.0,
        labor_rate=50.0,  # $50/hour
    )
    
    parts_df = pricing.load_parts()
    pricing_df = pricing.load_pricing()
    assemblies_df = pricing.load_assemblies()
    
    priced_items, summary = pricing.price_material_takeoff(
        takeoff, pricing_inputs, parts_df, pricing_df, assemblies_df
    )
    
    item = priced_items[0]
    # Labor per unit for posts is 0.25 hours/post
    # Waste factor is 1.0, so effective quantity = 10
    # Labor hours = 10 * 0.25 = 2.5 hours
    # Labor cost = 2.5 * 50 = $125
    assert item.labor_hours == pytest.approx(2.5)
    assert item.labor_cost == pytest.approx(125.0)
    assert item.labor_rate == 50.0


def test_price_material_takeoff_with_tax():
    """Test that tax is calculated correctly."""
    takeoff = MaterialTakeoff(items=[
        AssemblyQuantity(
            name="roof_panels",
            description="Roof panels",
            category="roof",
            quantity=100.0,
            unit="sqft",
        ),
    ])
    
    # 10% tax
    pricing_inputs = PricingInputs(
        material_markup=1.0,  # No markup
        tax_rate=0.10,  # 10% tax
        labor_rate=0.0,
    )
    
    parts_df = pricing.load_parts()
    pricing_df = pricing.load_pricing()
    assemblies_df = pricing.load_assemblies()
    
    priced_items, summary = pricing.price_material_takeoff(
        takeoff, pricing_inputs, parts_df, pricing_df, assemblies_df
    )
    
    # Tax should be 10% of (material + markup)
    expected_tax = (summary.material_subtotal + summary.markup_total) * 0.10
    assert summary.tax_total == pytest.approx(expected_tax)
    assert summary.grand_total == pytest.approx(
        summary.material_subtotal + summary.markup_total + summary.tax_total
    )


def test_price_material_takeoff_with_labor():
    """Test that labor costs are calculated when labor_per_unit is set."""
    # Note: Current assemblies CSV doesn't have labor_per_unit,
    # so this tests the structure but labor will be 0
    takeoff = MaterialTakeoff(items=[
        AssemblyQuantity(
            name="roof_panels",
            description="Roof panels",
            category="roof",
            quantity=100.0,
            unit="sqft",
        ),
    ])
    
    pricing_inputs = PricingInputs(
        material_markup=1.0,
        tax_rate=0.0,
        labor_rate=50.0,  # $50/hour
    )
    
    parts_df = pricing.load_parts()
    pricing_df = pricing.load_pricing()
    assemblies_df = pricing.load_assemblies()
    
    priced_items, summary = pricing.price_material_takeoff(
        takeoff, pricing_inputs, parts_df, pricing_df, assemblies_df
    )
    
    # Labor should be 0 since assemblies CSV doesn't specify labor_per_unit
    assert summary.labor_subtotal == 0.0


def test_price_material_takeoff_missing_part():
    """Test handling of missing part mappings."""
    takeoff = MaterialTakeoff(items=[
        AssemblyQuantity(
            name="nonexistent_assembly",
            description="Non-existent assembly",
            category="other",
            quantity=10.0,
            unit="ea",
        ),
    ])
    
    pricing_inputs = PricingInputs(
        material_markup=1.0,
        tax_rate=0.0,
        labor_rate=0.0,
    )
    
    parts_df = pricing.load_parts()
    pricing_df = pricing.load_pricing()
    assemblies_df = pricing.load_assemblies()
    
    priced_items, summary = pricing.price_material_takeoff(
        takeoff, pricing_inputs, parts_df, pricing_df, assemblies_df
    )
    
    # Should still create a priced item, but with 0 cost
    assert len(priced_items) == 1
    item = priced_items[0]
    assert item.unit_price == 0.0
    assert item.material_cost == 0.0
    assert item.total_cost == 0.0
    assert item.notes is not None  # Should have a note about missing mapping


def test_assemblies_csv_schema():
    """Test that assemblies CSV has the expected schema."""
    assemblies_df = pricing.load_assemblies()
    
    # Check for required columns
    assert "assembly_name" in assemblies_df.columns
    assert "category" in assemblies_df.columns
    assert "part_id" in assemblies_df.columns
    assert "waste_factor" in assemblies_df.columns
    assert "labor_per_unit" in assemblies_df.columns
    
    # Check that we have mappings for key assemblies
    assembly_names = assemblies_df["assembly_name"].tolist()
    assert "posts" in assembly_names
    assert "roof_panels" in assembly_names
    assert "sidewall_panels" in assembly_names
    
    # Check that waste_factor values are reasonable
    waste_factors = assemblies_df["waste_factor"].tolist()
    assert all(1.0 <= wf <= 1.20 for wf in waste_factors)  # Waste should be 0-20%
    
    # Check that labor_per_unit values are reasonable
    labor_values = assemblies_df["labor_per_unit"].tolist()
    assert all(0.0 <= lv <= 1.0 for lv in labor_values)  # Labor should be reasonable hours

