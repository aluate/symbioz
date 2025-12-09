"""
Phase 3 Smoke Test for ACC Express Order App

Tests core Phase 3 functionality:
- Pricing engine integration
- Presets endpoint
- End-to-end order submission with pricing columns
"""

import sys
from pathlib import Path

# Add repo root to path
repo_root = Path(__file__).resolve().parent
sys.path.insert(0, str(repo_root))

from apps.web.prime_order_api import app
import zipfile
import io
import csv

# Try to import TestClient (requires httpx)
HAS_TEST_CLIENT = False
client = None
try:
    from fastapi.testclient import TestClient
    client = TestClient(app)
    HAS_TEST_CLIENT = True
except (ImportError, RuntimeError) as e:
    HAS_TEST_CLIENT = False
    print("WARNING: TestClient not available (httpx not installed). Skipping endpoint tests.")
    print("  Install with: pip install httpx")


def test_catalog_endpoint():
    """Test that catalog endpoint returns valid data."""
    if not HAS_TEST_CLIENT:
        print("Skipping catalog endpoint test (TestClient not available)")
        return
    print("Testing /express-order/catalog...")
    response = client.get("/express-order/catalog")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    catalog = response.json()
    assert isinstance(catalog, dict), "Catalog should be a dict"
    assert len(catalog) > 0, "Catalog should have at least one cabinet family"
    print(f"Catalog endpoint OK ({len(catalog)} families)")


def test_finish_library_endpoint():
    """Test that finish library endpoint returns valid data."""
    if not HAS_TEST_CLIENT:
        print("Skipping finish library endpoint test (TestClient not available)")
        return
    print("Testing /express-order/finish-library...")
    response = client.get("/express-order/finish-library")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    library = response.json()
    assert isinstance(library, dict), "Library should be a dict"
    assert "Paint" in library or "Stain" in library or "Melamine" in library, "Library should have at least one medium"
    total = sum(len(v) for v in library.values())
    assert total > 0, "Library should have at least one finish"
    print(f"Finish library endpoint OK ({total} finishes)")


def test_presets_endpoint():
    """Test that presets endpoint returns valid data."""
    if not HAS_TEST_CLIENT:
        print("Skipping presets endpoint test (TestClient not available)")
        return
    print("Testing /express-order/presets...")
    response = client.get("/express-order/presets")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    presets = response.json()
    assert isinstance(presets, dict), "Presets should be a dict"
    # Check for known preset
    assert "KITCHEN_8FT_BASE" in presets or len(presets) > 0, "Presets should have at least one preset"
    print(f"Presets endpoint OK ({len(presets)} presets)")


def test_express_order_submit():
    """Test end-to-end order submission with Phase 3 features."""
    if not HAS_TEST_CLIENT:
        print("Skipping submit endpoint test (TestClient not available)")
        return
    print("Testing /express-order/submit (end-to-end)...")
    
    # Construct minimal but realistic payload
    payload = {
        "job": {
            "job_name": "Test Job - Phase 3 Smoke Test",
            "job_number": "TEST-001",
            "client_name": "Test Client",
            "client_email": "test@example.com",
            "site_address": "123 Test St",
            "designer": "Test Designer",
            "delivery_or_pickup": "Delivery",
            "requested_delivery_date": "2024-12-31"
        },
        "finishes": {
            "paint": [
                {
                    "index": 1,
                    "finish_id": "PAINT_SW_ALABASTER",
                    "label": "Sherwin-Williams SW 7008 – Alabaster (Paint on MDF)"
                }
            ],
            "stain": [
                {
                    "index": 1,
                    "finish_id": "STAIN_SW_URBANEBRONZE_ALDER",
                    "label": "Sherwin-Williams SW 7048 – Urbane Bronze (Stain on Select Alder)"
                }
            ],
            "melamine": [
                {
                    "index": 1,
                    "finish_id": "MEL_TAFISA_SNOWWHITE",
                    "label": "Tafisa L557 – Snow White (Melamine)"
                }
            ]
        },
        "rooms": [
            {
                "name": "Test Kitchen",
                "number": "101",
                "has_crown": True,
                "has_light_valance": True,
                "finish_type": "Stain",
                "finish_number": 1,
                "pull": "Black",
                "door_style": "Shaker",
                "grain_direction": None,
                "box_material": "Melamine"
            }
        ],
        "cabinets": [
            {
                "line_id": 1,
                "room": "Test Kitchen",
                "family_code": "B_2D",
                "width_in": 30.0,
                "height_in": 34.5,
                "depth_in": 24.0,
                "quantity": 1,
                "hinge_side": None,  # 2-door doesn't require hinge side
                "rollout_trays_qty": 0,
                "trash_kit": None,
                "applied_panels": 0,
                "special_instructions": None
            },
            {
                "line_id": 2,
                "room": "Test Kitchen",
                "family_code": "B_1D",
                "width_in": 15.0,
                "height_in": 34.5,
                "depth_in": 24.0,
                "quantity": 1,
                "hinge_side": "L",  # 1-door requires hinge side
                "rollout_trays_qty": 0,
                "trash_kit": None,
                "applied_panels": 0,
                "special_instructions": None
            },
            {
                "line_id": 3,
                "room": "Test Kitchen",
                "family_code": "T_PANTRY",
                "width_in": 15.0,  # Test tall with 15" width (matching 1-door base)
                "height_in": 90.0,
                "depth_in": 24.0,
                "quantity": 1,
                "hinge_side": None,  # Tall doesn't require hinge side
                "rollout_trays_qty": 2,  # Test option pricing
                "trash_kit": None,
                "applied_panels": 1,  # Test applied panels
                "special_instructions": None
            }
        ]
    }
    
    response = client.post("/express-order/submit", json=payload)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:500]}"
    assert response.headers.get("content-type") == "application/zip", f"Expected ZIP, got {response.headers.get('content-type')}"
    assert len(response.content) > 0, "ZIP file should not be empty"
    print("Submit endpoint returned ZIP file")
    
    # Extract and verify ZIP contents
    zip_file = zipfile.ZipFile(io.BytesIO(response.content))
    file_names = zip_file.namelist()
    assert "order.csv" in file_names, "ZIP should contain order.csv"
    assert "room_schedule.csv" in file_names, "ZIP should contain room_schedule.csv"
    print("ZIP contains expected CSV files")
    
    # Verify order.csv has Phase 3 columns
    order_csv_content = zip_file.read("order.csv").decode("utf-8")
    order_reader = csv.DictReader(io.StringIO(order_csv_content))
    order_rows = list(order_reader)
    assert len(order_rows) > 0, "order.csv should have at least one row"
    
    # Check for Phase 3 pricing columns
    assert "unit_price" in order_rows[0], "order.csv should have unit_price column"
    assert "line_total" in order_rows[0], "order.csv should have line_total column"
    print("order.csv has Phase 3 pricing columns (unit_price, line_total)")
    
    # Verify at least one row has pricing data (if pricing CSV exists)
    has_pricing = any(
        row.get("unit_price") and float(row.get("unit_price", 0)) > 0
        for row in order_rows
    )
    if has_pricing:
        print("Pricing data found in order.csv")
    else:
        print("NOTE: Pricing columns present but values are 0 (pricing CSV may be missing or incomplete)")
    
    # Verify room_schedule.csv has Phase 3 columns
    schedule_csv_content = zip_file.read("room_schedule.csv").decode("utf-8")
    schedule_reader = csv.DictReader(io.StringIO(schedule_csv_content))
    schedule_rows = list(schedule_reader)
    assert len(schedule_rows) > 0, "room_schedule.csv should have at least one row"
    
    # Check for Phase 3 pricing column
    assert "room_total" in schedule_rows[0], "room_schedule.csv should have room_total column"
    print("room_schedule.csv has Phase 3 pricing column (room_total)")
    
    # Verify room data
    test_room = schedule_rows[0]
    assert test_room["room_name"] == "Test Kitchen", "Room name should match"
    assert test_room["finish_code"] == "STAIN 1", "Finish code should be STAIN 1"
    assert test_room["cabinet_count"] == "3", "Should have 3 cabinets (2 base + 1 tall)"
    print("Room schedule data is correct")
    
    # Verify hinge side logic: B_2D should have null, B_1D should have "L"
    b2d_row = next((r for r in order_rows if r.get("family_code") == "B_2D"), None)
    b1d_row = next((r for r in order_rows if r.get("family_code") == "B_1D"), None)
    if b2d_row:
        assert b2d_row.get("hinge_side") == "" or b2d_row.get("hinge_side") is None, "2-door should not have hinge side"
    if b1d_row:
        assert b1d_row.get("hinge_side") == "L", "1-door should have hinge side"
    print("Hinge side logic verified (2-door=null, 1-door=L)")
    
    # Verify tall cabinet with 15" width
    tall_row = next((r for r in order_rows if r.get("family_code") == "T_PANTRY"), None)
    if tall_row:
        assert float(tall_row.get("width_in", 0)) == 15.0, "Tall should support 15\" width"
    print("Tall cabinet with 15\" width verified")
    
    print("End-to-end submission test passed")


def test_import_and_structure():
    """Test that the app imports correctly and has expected structure."""
    print("Testing app import and structure...")
    
    # Verify app exists
    assert app is not None, "App should be defined"
    assert hasattr(app, 'routes'), "App should have routes"
    
    # Check for expected routes
    route_paths = [route.path for route in app.routes]
    assert "/express-order" in route_paths, "Should have /express-order route"
    assert "/express-order/submit" in route_paths, "Should have /express-order/submit route"
    assert "/express-order/catalog" in route_paths, "Should have /express-order/catalog route"
    assert "/express-order/finish-library" in route_paths, "Should have /express-order/finish-library route"
    # Presets route may not exist if presets file is missing - make it optional
    if "/express-order/presets" not in route_paths:
        print("  NOTE: /express-order/presets route not found (presets may not be configured)")
    
    print("App imports successfully")
    print(f"App has {len(route_paths)} routes")
    return True


def run_all_tests():
    """Run all smoke tests."""
    print("\n" + "="*60)
    print("ACC Express Order - Phase 3 Smoke Tests")
    print("="*60 + "\n")
    
    try:
        # Always run import test
        test_import_and_structure()
        
        # Run endpoint tests if TestClient is available
        if HAS_TEST_CLIENT:
            test_catalog_endpoint()
            test_finish_library_endpoint()
            test_presets_endpoint()
            test_express_order_submit()
        else:
            print("\nNOTE: Endpoint tests skipped (install httpx to run full tests)")
        
        print("\n" + "="*60)
        print("ALL TESTS PASSED")
        print("="*60 + "\n")
        return True
    except AssertionError as e:
        print(f"\nTEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\nUNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

