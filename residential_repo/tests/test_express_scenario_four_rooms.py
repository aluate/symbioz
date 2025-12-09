"""
Four-Room Scenario Test for ACC Express Order App

Tests a realistic 4-room job (Wilson Residence) to validate:
- Hinge logic (1-door vs 2-door)
- Tall cabinet widths (15" support)
- Pricing integration
- Multiple finish types
- Room-level attributes
- End-to-end CSV generation
"""

import sys
from pathlib import Path

# Add repo root to path
repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))

try:
    from fastapi.testclient import TestClient
    HAS_TEST_CLIENT = True
except (ImportError, RuntimeError):
    HAS_TEST_CLIENT = False
    print("WARNING: TestClient not available (httpx not installed). Skipping scenario test.")
    print("  Install with: pip install httpx")

from apps.web.prime_order_api import app
import zipfile
import io
import csv
import json

if HAS_TEST_CLIENT:
    client = TestClient(app)


def build_four_room_payload():
    """Build a realistic 4-room payload using live catalog and finish library."""
    # Fetch catalog and finish library to build valid payload
    catalog_response = client.get("/express-order/catalog")
    assert catalog_response.status_code == 200
    catalog = catalog_response.json()
    
    finish_lib_response = client.get("/express-order/finish-library")
    assert finish_lib_response.status_code == 200
    finish_library = finish_lib_response.json()
    
    # Pick valid finish IDs from library
    paint_finish = finish_library.get("Paint", [{}])[0] if finish_library.get("Paint") else {}
    stain_finish = finish_library.get("Stain", [{}])[0] if finish_library.get("Stain") else {}
    melamine_finish = finish_library.get("Melamine", [{}])[0] if finish_library.get("Melamine") else {}
    
    # Build payload
    payload = {
        "job": {
            "job_name": "Wilson Residence – Express Test",
            "job_number": "EXP-TEST-004",
            "client_name": "Jordan Wilson",
            "client_email": "test+express@acc.local",
            "site_address": "123 Test Ridge, Coeur d'Alene, ID",
            "designer": "ACC Express",
            "delivery_or_pickup": "Delivery",
            "requested_delivery_date": "2025-01-15"
        },
        "finishes": {
            "paint": [
                {
                    "index": 1,
                    "finish_id": paint_finish.get("finish_id"),
                    "label": paint_finish.get("label", "Paint 1")
                }
            ] if paint_finish.get("finish_id") else [],
            "stain": [
                {
                    "index": 1,
                    "finish_id": stain_finish.get("finish_id"),
                    "label": stain_finish.get("label", "Stain 1")
                }
            ] if stain_finish.get("finish_id") else [],
            "melamine": [
                {
                    "index": 1,
                    "finish_id": melamine_finish.get("finish_id"),
                    "label": melamine_finish.get("label", "Melamine 1")
                }
            ] if melamine_finish.get("finish_id") else []
        },
        "rooms": [
            {
                "name": "Kitchen Perimeter",
                "number": "101",
                "has_crown": True,
                "has_light_valance": True,
                "finish_type": "Melamine",
                "finish_number": 1,
                "pull": "Black",
                "door_style": "Slab",
                "grain_direction": "Vertical Grain",
                "box_material": "Plywood"
            },
            {
                "name": "Kitchen Island",
                "number": "102",
                "has_crown": False,
                "has_light_valance": False,
                "finish_type": "Stain",
                "finish_number": 1,
                "pull": "Black",
                "door_style": "Shaker",
                "grain_direction": None,
                "box_material": "Plywood"
            },
            {
                "name": "Hall Bath",
                "number": "201",
                "has_crown": False,
                "has_light_valance": False,
                "finish_type": "Paint",
                "finish_number": 1,
                "pull": "Satin Nickel",
                "door_style": "Slim Shaker",
                "grain_direction": None,
                "box_material": "Melamine"
            },
            {
                "name": "Laundry",
                "number": "301",
                "has_crown": False,
                "has_light_valance": False,
                "finish_type": "Melamine",
                "finish_number": 1,
                "pull": "Black",
                "door_style": "Slab",
                "grain_direction": "Horizontal Grain",
                "box_material": "Melamine"
            }
        ],
        "cabinets": []
    }
    
    # Kitchen Perimeter (101) - Mix of 1-door and 2-door, with tall
    # B_2D 30" (2-door, no hinge)
    if "B_2D" in catalog:
        payload["cabinets"].extend([
            {
                "line_id": len(payload["cabinets"]) + 1,
                "room": "Kitchen Perimeter",
                "family_code": "B_2D",
                "width_in": 30.0,
                "height_in": 34.5,
                "depth_in": 24.0,
                "quantity": 2,
                "hinge_side": None,  # 2-door doesn't require hinge
                "rollout_trays_qty": 2,
                "trash_kit": None,
                "applied_panels": 0,
                "special_instructions": None
            }
        ])
    
    # B_1D 15" (1-door, requires hinge)
    if "B_1D" in catalog:
        payload["cabinets"].append({
            "line_id": len(payload["cabinets"]) + 1,
            "room": "Kitchen Perimeter",
            "family_code": "B_1D",
            "width_in": 15.0,
            "height_in": 34.5,
            "depth_in": 24.0,
            "quantity": 1,
            "hinge_side": "L",  # 1-door requires hinge
            "rollout_trays_qty": 1,
            "trash_kit": None,
            "applied_panels": 0,
            "special_instructions": None
        })
    
    # W_2D 30" wall (2-door, no hinge)
    if "W_2D" in catalog:
        payload["cabinets"].extend([
            {
                "line_id": len(payload["cabinets"]) + 1,
                "room": "Kitchen Perimeter",
                "family_code": "W_2D",
                "width_in": 30.0,
                "height_in": 30.0,
                "depth_in": 12.0,
                "quantity": 2,
                "hinge_side": None,
                "rollout_trays_qty": 0,
                "trash_kit": None,
                "applied_panels": 0,
                "special_instructions": None
            }
        ])
    
    # W_1D 15" wall (1-door, requires hinge)
    if "W_1D" in catalog:
        payload["cabinets"].append({
            "line_id": len(payload["cabinets"]) + 1,
            "room": "Kitchen Perimeter",
            "family_code": "W_1D",
            "width_in": 15.0,
            "height_in": 30.0,
            "depth_in": 12.0,
            "quantity": 1,
            "hinge_side": "R",  # 1-door requires hinge
            "rollout_trays_qty": 0,
            "trash_kit": None,
            "applied_panels": 0,
            "special_instructions": None
        })
    
    # T_PANTRY 15" tall (tests 15" width support)
    if "T_PANTRY" in catalog:
        pantry_family = catalog["T_PANTRY"]
        if 15 in pantry_family.get("allowed_widths_in", []):
            payload["cabinets"].append({
                "line_id": len(payload["cabinets"]) + 1,
                "room": "Kitchen Perimeter",
                "family_code": "T_PANTRY",
                "width_in": 15.0,
                "height_in": 90.0,
                "depth_in": 24.0,
                "quantity": 1,
                "hinge_side": None,  # Tall doesn't require hinge
                "rollout_trays_qty": 3,
                "trash_kit": None,
                "applied_panels": 1,
                "special_instructions": None
            })
    
    # Kitchen Island (102)
    # B_3DR 24" (drawer, no hinge)
    if "B_3DR" in catalog:
        payload["cabinets"].extend([
            {
                "line_id": len(payload["cabinets"]) + 1,
                "room": "Kitchen Island",
                "family_code": "B_3DR",
                "width_in": 24.0,
                "height_in": 34.5,
                "depth_in": 24.0,
                "quantity": 2,
                "hinge_side": None,
                "rollout_trays_qty": 0,
                "trash_kit": None,
                "applied_panels": 1,  # Test applied panels
                "special_instructions": None
            }
        ])
    
    # B_TRASH 18" (trash pullout, no hinge)
    if "B_TRASH" in catalog:
        payload["cabinets"].append({
            "line_id": len(payload["cabinets"]) + 1,
            "room": "Kitchen Island",
            "family_code": "B_TRASH",
            "width_in": 18.0,
            "height_in": 34.5,
            "depth_in": 24.0,
            "quantity": 1,
            "hinge_side": None,
            "rollout_trays_qty": 0,
            "trash_kit": "Single",
            "applied_panels": 0,
            "special_instructions": None
        })
    
    # Hall Bath (201)
    # V_SINK_CENTER 30"
    if "V_SINK_CENTER" in catalog:
        payload["cabinets"].append({
            "line_id": len(payload["cabinets"]) + 1,
            "room": "Hall Bath",
            "family_code": "V_SINK_CENTER",
            "width_in": 30.0,
            "height_in": 34.5,
            "depth_in": 21.0,
            "quantity": 1,
            "hinge_side": None,
            "rollout_trays_qty": 0,
            "trash_kit": None,
            "applied_panels": 0,
            "special_instructions": None
        })
    
    # V_3DR 15"
    if "V_3DR" in catalog:
        payload["cabinets"].append({
            "line_id": len(payload["cabinets"]) + 1,
            "room": "Hall Bath",
            "family_code": "V_3DR",
            "width_in": 15.0,
            "height_in": 34.5,
            "depth_in": 21.0,
            "quantity": 1,
            "hinge_side": None,
            "rollout_trays_qty": 0,
            "trash_kit": None,
            "applied_panels": 0,
            "special_instructions": None
        })
    
    # Laundry (301)
    # B_2D 30" (2-door, no hinge)
    if "B_2D" in catalog:
        payload["cabinets"].extend([
            {
                "line_id": len(payload["cabinets"]) + 1,
                "room": "Laundry",
                "family_code": "B_2D",
                "width_in": 30.0,
                "height_in": 34.5,
                "depth_in": 24.0,
                "quantity": 2,
                "hinge_side": None,
                "rollout_trays_qty": 0,
                "trash_kit": None,
                "applied_panels": 0,
                "special_instructions": None
            }
        ])
    
    # W_2D 30" wall
    if "W_2D" in catalog:
        payload["cabinets"].extend([
            {
                "line_id": len(payload["cabinets"]) + 1,
                "room": "Laundry",
                "family_code": "W_2D",
                "width_in": 30.0,
                "height_in": 30.0,
                "depth_in": 12.0,
                "quantity": 2,
                "hinge_side": None,
                "rollout_trays_qty": 0,
                "trash_kit": None,
                "applied_panels": 0,
                "special_instructions": None
            }
        ])
    
    return payload


def test_four_room_scenario():
    """Test a realistic 4-room job end-to-end."""
    if not HAS_TEST_CLIENT:
        print("Skipping 4-room scenario test (TestClient not available)")
        return
    
    print("Testing 4-room scenario (Wilson Residence)...")
    
    # Build payload dynamically from catalog/library
    payload = build_four_room_payload()
    
    # Verify we have cabinets
    assert len(payload["cabinets"]) > 0, "Should have at least one cabinet"
    print(f"  Built payload with {len(payload['rooms'])} rooms and {len(payload['cabinets'])} cabinets")
    
    # Submit order
    response = client.post("/express-order/submit", json=payload)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text[:500]}"
    assert response.headers.get("content-type") == "application/zip", f"Expected ZIP, got {response.headers.get('content-type')}"
    assert len(response.content) > 0, "ZIP file should not be empty"
    print("  Submit endpoint returned ZIP file")
    
    # Extract and verify ZIP
    zip_file = zipfile.ZipFile(io.BytesIO(response.content))
    file_names = zip_file.namelist()
    assert "order.csv" in file_names, "ZIP should contain order.csv"
    assert "room_schedule.csv" in file_names, "ZIP should contain room_schedule.csv"
    print("  ZIP contains expected CSV files")
    
    # Verify order.csv
    order_csv_content = zip_file.read("order.csv").decode("utf-8")
    order_reader = csv.DictReader(io.StringIO(order_csv_content))
    order_rows = list(order_reader)
    assert len(order_rows) > 0, "order.csv should have at least one row"
    
    # Check for Phase 3 columns
    assert "unit_price" in order_rows[0], "order.csv should have unit_price column"
    assert "line_total" in order_rows[0], "order.csv should have line_total column"
    assert "hinge_side" in order_rows[0], "order.csv should have hinge_side column"
    assert "box_material" in order_rows[0], "order.csv should have box_material column"
    assert "applied_panels" in order_rows[0], "order.csv should have applied_panels column"
    print("  order.csv has all required columns")
    
    # Verify hinge logic
    b1d_rows = [r for r in order_rows if r.get("family_code") == "B_1D"]
    b2d_rows = [r for r in order_rows if r.get("family_code") == "B_2D"]
    w1d_rows = [r for r in order_rows if r.get("family_code") == "W_1D"]
    
    if b1d_rows:
        assert b1d_rows[0].get("hinge_side") in ["L", "R"], "1-door base should have hinge side"
        print("  Hinge logic: 1-door base has hinge side")
    
    if b2d_rows:
        assert b2d_rows[0].get("hinge_side") == "" or b2d_rows[0].get("hinge_side") is None, "2-door base should not have hinge side"
        print("  Hinge logic: 2-door base has no hinge side")
    
    if w1d_rows:
        assert w1d_rows[0].get("hinge_side") in ["L", "R"], "1-door wall should have hinge side"
        print("  Hinge logic: 1-door wall has hinge side")
    
    # Verify tall 15" width
    tall_rows = [r for r in order_rows if r.get("family_code") == "T_PANTRY"]
    if tall_rows:
        assert float(tall_rows[0].get("width_in", 0)) == 15.0, "Tall pantry should support 15\" width"
        print("  Tall cabinet: 15\" width verified")
    
    # Verify pricing
    has_pricing = any(
        row.get("unit_price") and float(row.get("unit_price", 0)) > 0
        for row in order_rows
    )
    if has_pricing:
        print("  Pricing: Active (non-zero prices found)")
    else:
        print("  Pricing: Columns present but values are 0 (pricing CSV may be missing)")
    
    # Verify room_schedule.csv
    schedule_csv_content = zip_file.read("room_schedule.csv").decode("utf-8")
    schedule_reader = csv.DictReader(io.StringIO(schedule_csv_content))
    schedule_rows = list(schedule_reader)
    assert len(schedule_rows) == 4, f"room_schedule.csv should have 4 rows (one per room), got {len(schedule_rows)}"
    
    # Check for Phase 3 columns
    assert "room_total" in schedule_rows[0], "room_schedule.csv should have room_total column"
    assert "box_material" in schedule_rows[0], "room_schedule.csv should have box_material column"
    assert "door_style" in schedule_rows[0], "room_schedule.csv should have door_style column"
    assert "grain_direction" in schedule_rows[0], "room_schedule.csv should have grain_direction column"
    print("  room_schedule.csv has all required columns")
    
    # Verify room data
    room_names = {row["room_name"] for row in schedule_rows}
    assert "Kitchen Perimeter" in room_names, "Should have Kitchen Perimeter room"
    assert "Kitchen Island" in room_names, "Should have Kitchen Island room"
    assert "Hall Bath" in room_names, "Should have Hall Bath room"
    assert "Laundry" in room_names, "Should have Laundry room"
    print("  All 4 rooms present in room_schedule.csv")
    
    # Verify room attributes
    kitchen_perim = next((r for r in schedule_rows if r["room_name"] == "Kitchen Perimeter"), None)
    if kitchen_perim:
        assert kitchen_perim["box_material"] == "Plywood", "Kitchen Perimeter should have Plywood boxes"
        assert kitchen_perim["door_style"] == "Slab", "Kitchen Perimeter should have Slab doors"
        assert kitchen_perim["grain_direction"] == "Vertical Grain", "Kitchen Perimeter should have Vertical Grain"
        print("  Room attributes verified (Plywood, Slab, Vertical Grain)")
    
    print("  4-room scenario test PASSED")


def run_test():
    """Run the 4-room scenario test."""
    print("\n" + "="*60)
    print("ACC Express - Four-Room Scenario Test")
    print("="*60 + "\n")
    
    if not HAS_TEST_CLIENT:
        print("WARNING: TestClient not available (httpx not installed).")
        print("  Install with: pip install httpx")
        print("  Skipping scenario test.\n")
        return False
    
    try:
        test_four_room_scenario()
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
    success = run_test()
    sys.exit(0 if success else 1)

