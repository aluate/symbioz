"""
FastAPI server for ACC Prime Order cabinet ordering tool.
Allows contractors/clients to order cabinets via webform and download CSV order file.
"""

from __future__ import annotations

from pathlib import Path
import json
import csv
import zipfile
from io import StringIO, BytesIO
from functools import lru_cache
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from pydantic import BaseModel, ValidationError
from typing import Optional, List, Literal, Dict, Any
import traceback
import logging

app = FastAPI(title="ACC Prime Order API")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mount static files directory for logos and assets
STATIC_DIR = Path(__file__).resolve().parent / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Load catalog at startup
CATALOG_PATH = Path(__file__).resolve().parents[2] / "config" / "cabinets_catalog.json"
FINISHES_PATH = Path(__file__).resolve().parents[2] / "config" / "finish_colors.csv"
PRICING_PATH = Path(__file__).resolve().parents[2] / "config" / "express_pricing.csv"
PRESETS_PATH = Path(__file__).resolve().parents[2] / "config" / "express_presets.json"

def load_catalog():
    """Load the cabinets catalog JSON."""
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# Cache catalog
_catalog = None

def get_catalog():
    """Get cached catalog or load it."""
    global _catalog
    if _catalog is None:
        _catalog = load_catalog()
    return _catalog


# Finish library loading
@lru_cache()
def load_finish_library() -> Dict[str, List[Dict[str, Any]]]:
    """
    Load finish colors library from CSV and organize by medium.
    Returns dict with keys: "Paint", "Stain", "Melamine"
    """
    library = {"Paint": [], "Stain": [], "Melamine": []}
    
    if not FINISHES_PATH.exists():
        return library
    
    with open(FINISHES_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Filter to active only
            if row.get("active", "").upper() != "TRUE":
                continue
            
            # Normalize medium (strip, title case, handle variations)
            medium_raw = row.get("medium", "").strip()
            medium = medium_raw.title() if medium_raw else ""
            
            # Map common variations to canonical names
            medium_map = {
                "Paint": "Paint",
                "Stain": "Stain", 
                "Melamine": "Melamine"
            }
            
            # Normalize to canonical form
            if medium in medium_map:
                medium = medium_map[medium]
            else:
                # Try case-insensitive match
                medium_lower = medium.lower()
                if medium_lower == "paint":
                    medium = "Paint"
                elif medium_lower == "stain":
                    medium = "Stain"
                elif medium_lower == "melamine":
                    medium = "Melamine"
                else:
                    continue  # Skip unknown mediums
            
            if medium not in library:
                continue
            
            # Build finish record
            finish_record = {
                "finish_id": row.get("finish_id", ""),
                "color_brand": row.get("color_brand", ""),
                "color_collection": row.get("color_collection", ""),
                "color_name": row.get("color_name", ""),
                "color_code": row.get("color_code", ""),
                "color_chip_url": row.get("color_chip_url", ""),
                "medium": medium,
                "substrate": row.get("substrate", ""),
                "shop_product_line": row.get("shop_product_line", ""),
                "shop_sku": row.get("shop_sku", ""),
                "vendor": row.get("vendor", ""),
                "vendor_sku": row.get("vendor_sku", ""),
                "cost_per_unit": row.get("cost_per_unit", ""),
                "cost_unit": row.get("cost_unit", ""),
                "waste_factor": row.get("waste_factor", ""),
                "eligible_for_prime": row.get("eligible_for_prime", "").upper() == "TRUE",
                "recommended_slot": row.get("recommended_slot", ""),
                "max_sheen": row.get("max_sheen", ""),
                "notes": row.get("notes", ""),
            }
            
            # Build UI label
            brand = finish_record["color_brand"]
            code = finish_record["color_code"]
            name = finish_record["color_name"]
            substrate = finish_record["substrate"]
            
            if substrate:
                label = f"{brand} {code} – {name} ({medium} on {substrate})"
            else:
                label = f"{brand} {code} – {name} ({medium})"
            
            finish_record["label"] = label
            library[medium].append(finish_record)
    
    return library


def get_finish_by_id(finish_id: str) -> Optional[Dict[str, Any]]:
    """Look up a finish record by finish_id across all mediums."""
    library = load_finish_library()
    for medium_list in library.values():
        for finish in medium_list:
            if finish.get("finish_id") == finish_id:
                return finish
    return None


def load_pricing_config() -> Dict[str, Dict[str, Any]]:
    """
    Load pricing configuration from CSV.
    Returns a dict organized by key_type -> key -> pricing data.
    Structure: {
        'family': {'B_2D': {...}, ...},
        'finish': {'PAINT_SW_ALABASTER': {...}, ...},
        'option': {'rollout_tray': {...}, ...}
    }
    """
    pricing_config = {
        'family': {},
        'finish': {},
        'option': {}
    }
    
    if not PRICING_PATH.exists():
        logger.warning(f"Pricing config not found at {PRICING_PATH}. Pricing will be disabled.")
        return pricing_config
    
    try:
        with open(PRICING_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('active', '').upper() != 'TRUE':
                    continue
                
                key_type = row.get('key_type', '').strip().lower()
                key = row.get('key', '').strip()
                
                if not key_type or not key:
                    continue
                
                try:
                    price_per_unit = float(row.get('price_per_unit', 0))
                except (ValueError, TypeError):
                    logger.warning(f"Invalid price_per_unit for {key_type}/{key}: {row.get('price_per_unit')}")
                    continue
                
                unit = row.get('unit', '').strip()
                description = row.get('description', '').strip()
                
                if key_type in pricing_config:
                    pricing_config[key_type][key] = {
                        'price_per_unit': price_per_unit,
                        'unit': unit,
                        'description': description
                    }
    except Exception as e:
        logger.error(f"Error loading pricing config: {e}")
        logger.error(traceback.format_exc())
    
    return pricing_config


def calculate_cabinet_price(
    cabinet: CabinetLineItem,
    room: RoomInfo,
    finish_slot: Optional[FinishSlot],
    pricing: Dict[str, Dict[str, Any]]
) -> float:
    """
    Calculate price for a single cabinet line item (before quantity multiplier).
    
    Rules:
    1. Base price: family_rate * width_in (if per_inch_width)
    2. Finish adder: finish_id rate (if per_cabinet)
    3. Options: rollout_trays_qty * rate, trash_kit rate, applied_panels * rate
    4. Plywood upgrade: per_cabinet rate if box_material == "Plywood"
    
    Returns: unit_price (price for one cabinet of this type)
    """
    total = 0.0
    
    # 1. Base price from family
    family_pricing = pricing.get('family', {}).get(cabinet.family_code)
    if family_pricing:
        if family_pricing['unit'] == 'per_inch_width':
            total += family_pricing['price_per_unit'] * cabinet.width_in
        elif family_pricing['unit'] == 'per_cabinet':
            total += family_pricing['price_per_unit']
    
    # 2. Finish adder
    if finish_slot and finish_slot.finish_id:
        finish_pricing = pricing.get('finish', {}).get(finish_slot.finish_id)
        if finish_pricing and finish_pricing['unit'] == 'per_cabinet':
            total += finish_pricing['price_per_unit']
    
    # 3. Options
    option_pricing = pricing.get('option', {})
    
    # Rollout trays
    if cabinet.rollout_trays_qty > 0:
        rollout_rate = option_pricing.get('rollout_tray', {}).get('price_per_unit', 0)
        if option_pricing.get('rollout_tray', {}).get('unit') == 'per_rollout':
            total += rollout_rate * cabinet.rollout_trays_qty
    
    # Trash kit
    if cabinet.trash_kit:
        trash_rate = option_pricing.get('trash_kit', {}).get('price_per_unit', 0)
        if option_pricing.get('trash_kit', {}).get('unit') == 'per_trash_kit':
            total += trash_rate
    
    # Applied panels
    if cabinet.applied_panels > 0:
        panel_rate = option_pricing.get('applied_panel', {}).get('price_per_unit', 0)
        if option_pricing.get('applied_panel', {}).get('unit') == 'per_applied_panel':
            total += panel_rate * cabinet.applied_panels
    
    # 4. Plywood upgrade (per cabinet)
    if room.box_material == "Plywood":
        plywood_rate = option_pricing.get('plywood_upgrade', {}).get('price_per_unit', 0)
        if option_pricing.get('plywood_upgrade', {}).get('unit') == 'per_cabinet':
            total += plywood_rate
    
    return round(total, 2)


# Pydantic models for request validation
class JobInfo(BaseModel):
    job_name: str
    job_number: Optional[str] = None
    client_name: str
    client_email: Optional[str] = None
    site_address: Optional[str] = None
    designer: Optional[str] = None
    delivery_or_pickup: Optional[str] = None
    requested_delivery_date: Optional[str] = None
    notes: Optional[str] = None


class FinishSlot(BaseModel):
    index: int
    finish_id: Optional[str] = None
    label: str
    other_brand: Optional[str] = None  # For "Other" finishes
    other_name: Optional[str] = None   # For "Other" finishes
    other_code: Optional[str] = None   # For "Other" finishes


class FinishesInfo(BaseModel):
    paint: Optional[List[FinishSlot]] = []
    stain: List[FinishSlot]
    melamine: List[FinishSlot]


class RoomInfo(BaseModel):
    name: str
    number: Optional[str] = None
    has_crown: bool = False
    has_light_valance: bool = False
    finish_type: Literal["Paint", "Stain", "Melamine"]
    finish_number: int  # 1-3
    pull: Literal["Black", "Satin Nickel", "None"] = "None"
    door_style: Optional[str] = None  # "Shaker", "Slim Shaker", "Slab MDF", "Slab"
    grain_direction: Optional[str] = None  # "Vertical Grain", "Horizontal Grain" (only for Melamine)
    box_material: str = "Melamine"  # "Melamine" or "Plywood"


class CabinetLineItem(BaseModel):
    line_id: int
    room: str
    family_code: str
    width_in: float
    height_in: Optional[float] = None
    depth_in: Optional[float] = None
    quantity: int = 1
    hinge_side: Optional[str] = None
    rollout_trays_qty: int = 0
    trash_kit: Optional[str] = None
    applied_panels: int = 0  # 0, 1, or 2
    special_instructions: Optional[str] = None


class PrimeOrderRequest(BaseModel):
    job: JobInfo
    finishes: FinishesInfo
    rooms: List[RoomInfo]
    cabinets: List[CabinetLineItem]


@app.get("/prime-order", response_class=HTMLResponse)
def prime_order_form():
    """Serve the Prime Order HTML form (legacy route - kept for backward compatibility)."""
    template_path = Path(__file__).resolve().parent / "templates" / "prime_order.html"
    html = template_path.read_text(encoding="utf-8")
    return HTMLResponse(content=html)


@app.get("/express-order", response_class=HTMLResponse)
def express_order_form():
    """Serve the ACC Express Order HTML form."""
    try:
        template_path = Path(__file__).resolve().parent / "templates" / "prime_order.html"
        if not template_path.exists():
            raise HTTPException(status_code=404, detail="Template file not found")
        html = template_path.read_text(encoding="utf-8")
        return HTMLResponse(content=html)
    except Exception as e:
        logger.error(f"Error serving Express order form: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error loading form: {str(e)}")


@app.get("/prime-order/catalog")
def get_catalog_endpoint():
    """Return the cabinets catalog as JSON for the frontend (legacy route)."""
    catalog = get_catalog()
    # Debug logging
    family_count = len(catalog) if isinstance(catalog, dict) else 0
    print(f"Prime catalog endpoint: returning {family_count} cabinet families")
    return JSONResponse(content=catalog)


@app.get("/express-order/catalog")
def get_express_catalog_endpoint():
    """Return the cabinets catalog as JSON for the frontend."""
    try:
        catalog = get_catalog()
        # Debug logging
        family_count = len(catalog) if isinstance(catalog, dict) else 0
        logger.info(f"Express catalog endpoint: returning {family_count} cabinet families")
        return JSONResponse(content=catalog)
    except Exception as e:
        logger.error(f"Error loading catalog: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error loading catalog: {str(e)}")


@app.get("/prime-order/finish-library")
def get_finish_library_endpoint():
    """Return the finish colors library organized by medium for the frontend (legacy route)."""
    library = load_finish_library()
    # Ensure we return the exact structure expected
    response = {
        "Paint": library.get("Paint", []),
        "Stain": library.get("Stain", []),
        "Melamine": library.get("Melamine", [])
    }
    return JSONResponse(content=response)


@app.get("/express-order/finish-library")
def get_express_finish_library_endpoint():
    """Return the finish colors library organized by medium for the frontend."""
    try:
        library = load_finish_library()
        # Ensure we return the exact structure expected
        response = {
            "Paint": library.get("Paint", []),
            "Stain": library.get("Stain", []),
            "Melamine": library.get("Melamine", [])
        }
        logger.info(f"Finish library endpoint: Paint={len(response['Paint'])}, "
                   f"Stain={len(response['Stain'])}, Melamine={len(response['Melamine'])}")
        return JSONResponse(content=response)
    except Exception as e:
        logger.error(f"Error loading finish library: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error loading finish library: {str(e)}")


def load_presets_config() -> Dict[str, Any]:
    """Load presets configuration from JSON file."""
    try:
        if not PRESETS_PATH.exists():
            logger.warning(f"Presets file not found at {PRESETS_PATH}")
            return {}
        with open(PRESETS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading presets config: {e}")
        logger.error(traceback.format_exc())
        return {}


@app.get("/express-order/presets")
def get_express_presets_endpoint():
    """Return the preset configurations for the frontend (read-only)."""
    try:
        presets = load_presets_config()
        logger.info(f"Presets endpoint: {len(presets)} presets loaded")
        return JSONResponse(content=presets)
    except Exception as e:
        logger.error(f"Error loading presets: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error loading presets: {str(e)}")


def resolve_finish_label(finishes: FinishesInfo, finish_type: str, finish_number: int) -> str:
    """Resolve finish label from finishes info."""
    try:
        slot_list = None
        if finish_type == "Paint":
            slot_list = finishes.paint or []
        elif finish_type == "Stain":
            slot_list = finishes.stain or []
        elif finish_type == "Melamine":
            slot_list = finishes.melamine or []
        
        if slot_list:
            for slot in slot_list:
                if slot.index == finish_number:
                    return slot.label if slot.label else "UNKNOWN"
        return "UNKNOWN"
    except Exception as e:
        logger.warning(f"Error resolving finish label: {e}")
        return "UNKNOWN"


def resolve_finish_id(finishes: FinishesInfo, finish_type: str, finish_number: int) -> Optional[str]:
    """Resolve finish_id from finishes info."""
    try:
        slot_list = None
        if finish_type == "Paint":
            slot_list = finishes.paint or []
        elif finish_type == "Stain":
            slot_list = finishes.stain or []
        elif finish_type == "Melamine":
            slot_list = finishes.melamine or []
        
        if slot_list:
            for slot in slot_list:
                if slot.index == finish_number:
                    return slot.finish_id
        return None
    except Exception as e:
        logger.warning(f"Error resolving finish_id: {e}")
        return None


@app.post("/prime-order/submit")
def prime_order_submit(request: PrimeOrderRequest):
    """Legacy route - kept for backward compatibility."""
    return express_order_submit(request)


@app.post("/express-order/submit")
def express_order_submit(request: PrimeOrderRequest):
    """
    Accept order JSON and generate two CSV files (order + room schedule) in a ZIP bundle.
    
    For each cabinet line item:
    - Looks up family_code in catalog
    - Validates width/height are in allowed ranges
    - Derives cabinet_code from code_pattern
    - Uses display_name as cabinet_type
    - Resolves finish_label from finishes block
    """
    try:
        # Log incoming request structure for debugging
        logger.info("=== Express Order Submit Request ===")
        logger.info(f"Job: {request.job.job_name if request.job else 'None'}")
        logger.info(f"Rooms count: {len(request.rooms)}")
        logger.info(f"Cabinets count: {len(request.cabinets)}")
        logger.info(f"Finishes - Paint: {len(request.finishes.paint) if request.finishes.paint else 0}, "
                   f"Stain: {len(request.finishes.stain) if request.finishes.stain else 0}, "
                   f"Melamine: {len(request.finishes.melamine) if request.finishes.melamine else 0}")
        
        # Validate request structure
        if not request.job:
            raise HTTPException(status_code=400, detail="Job information is required")
        if not request.rooms:
            raise HTTPException(status_code=400, detail="At least one room is required")
        if not request.cabinets:
            raise HTTPException(status_code=400, detail="At least one cabinet is required")
        
        catalog = get_catalog()
        job = request.job
        finishes = request.finishes
        rooms = request.rooms
        cabinets = request.cabinets
        
        # Load pricing config (optional - if missing, prices will be 0.0)
        pricing_config = load_pricing_config()
        pricing_enabled = any(
            pricing_config.get('family', {}) or
            pricing_config.get('finish', {}) or
            pricing_config.get('option', {})
        )
        
        # Track pricing totals
        room_totals = {room.name: 0.0 for room in rooms}
        job_total = 0.0
        
        # Validate room data
        for idx, room in enumerate(rooms):
            if not hasattr(room, 'box_material') or not room.box_material:
                room.box_material = "Melamine"  # Set default if missing
            logger.info(f"Room {idx}: {room.name}, box_material: {room.box_material}")
        
        # Validate cabinet data
        for idx, cabinet in enumerate(cabinets):
            if not hasattr(cabinet, 'applied_panels'):
                cabinet.applied_panels = 0  # Set default if missing
            logger.info(f"Cabinet {idx}: {cabinet.family_code}, applied_panels: {getattr(cabinet, 'applied_panels', 0)}")
        
        # Build room lookup dict (name -> room object)
        room_lookup = {room.name: room for room in rooms}
        
        # Create order CSV in memory
        order_output = StringIO()
        order_writer = csv.writer(order_output)
    
        # Order CSV Header row
        order_writer.writerow([
        "job_name", "job_number", "client_name", "client_email", "site_address",
        "designer", "delivery_or_pickup", "requested_delivery_date",
        "room", "cabinet_type", "cabinet_code", "family_code",
        "width_in", "height_in", "depth_in", "quantity",
        "finish_type", "finish_number", "finish_label", "finish_id",
        "color_brand", "color_name", "color_code", "medium",
        "shop_product_line", "shop_sku", "vendor",
        "door_style", "grain_direction", "box_material",
        "hinge_side", "rollout_trays_qty", "trash_kit", "applied_panels",
        "special_instructions"
        ])
        
        # Track counts for room schedule
        room_finish_counts = {}  # room_name -> {cabinet_count, accessory_count}
        
        # Process each cabinet line item
        for line in cabinets:
            family_code = line.family_code
            
            # Look up family in catalog
            if family_code not in catalog:
                continue  # Skip invalid families
            
            family_data = catalog[family_code]
            is_accessory = family_data.get("is_accessory", False) or family_data.get("category") == "Accessory"
            
            # Set default depth if not provided
            if line.depth_in is None:
                line.depth_in = family_data.get("default_depth_in", 24.0)
            
            # Set default height if not provided
            if line.height_in is None:
                allowed_heights = family_data.get("allowed_heights_in", [])
                if allowed_heights:
                    line.height_in = allowed_heights[0]  # Use first allowed height
                else:
                    line.height_in = family_data.get("default_height_in", 34.5)
            
            # Validate width/height (basic check - frontend should prevent this)
            if family_data.get("allowed_widths_in"):
                if line.width_in not in family_data["allowed_widths_in"]:
                    allowed = family_data["allowed_widths_in"]
                    if allowed:
                        line.width_in = min(allowed, key=lambda x: abs(x - line.width_in))
            
            if "allowed_heights_in" in family_data and family_data["allowed_heights_in"]:
                if line.height_in not in family_data["allowed_heights_in"]:
                    allowed = family_data["allowed_heights_in"]
                    if allowed:
                        line.height_in = min(allowed, key=lambda x: abs(x - line.height_in))
            
            # Handle special cases for accessories (e.g., floating shelves with depth)
            if is_accessory and "allowed_depths_in" in family_data:
                if line.depth_in not in family_data.get("allowed_depths_in", []):
                    allowed = family_data["allowed_depths_in"]
                    if allowed:
                        line.depth_in = min(allowed, key=lambda x: abs(x - line.depth_in))
            
            # Derive cabinet_code from code_pattern
            code_pattern = family_data.get("code_pattern", "")
            try:
                if "{depth}" in code_pattern:
                    cabinet_code = code_pattern.format(
                        width=int(line.width_in),
                        depth=int(line.depth_in)
                    )
                elif "{height}" in code_pattern:
                    cabinet_code = code_pattern.format(
                        width=int(line.width_in),
                        height=int(line.height_in)
                    )
                else:
                    cabinet_code = code_pattern.format(width=int(line.width_in))
                cabinet_code = cabinet_code.replace("--", "-").strip("-")
            except (KeyError, ValueError, AttributeError) as e:
                logger.warning(f"Error formatting cabinet code for {family_code}: {e}. Using fallback.")
                cabinet_code = f"{family_code}-{int(line.width_in)}"
            
            # Get display name as cabinet_type
            cabinet_type = family_data.get("display_name", family_code)
            
            # Derive finish from room
            room_obj = room_lookup.get(line.room)
            finish_id = None
            color_brand = ""
            color_name = ""
            color_code = ""
            medium = ""
            shop_product_line = ""
            shop_sku = ""
            vendor = ""
            door_style = ""
            grain_direction = ""
            
            if room_obj:
                finish_type = room_obj.finish_type
                finish_number = room_obj.finish_number
                finish_label = resolve_finish_label(finishes, finish_type, finish_number)
                finish_id = resolve_finish_id(finishes, finish_type, finish_number)
                door_style = room_obj.door_style or ""
                grain_direction = room_obj.grain_direction or ""
                box_material = room_obj.box_material or "Melamine"
                
                # Get finish slot to check for "Other" metadata
                finish_slot = None
                if finish_type == "Paint":
                    slot_list = finishes.paint or []
                elif finish_type == "Stain":
                    slot_list = finishes.stain or []
                elif finish_type == "Melamine":
                    slot_list = finishes.melamine or []
                else:
                    slot_list = []
                
                for slot in slot_list:
                    if slot.index == finish_number:
                        finish_slot = slot
                        break
                
                # Look up library metadata if finish_id exists
                if finish_id:
                    finish_record = get_finish_by_id(finish_id)
                    if finish_record:
                        color_brand = finish_record.get("color_brand", "")
                        color_name = finish_record.get("color_name", "")
                        color_code = finish_record.get("color_code", "")
                        medium = finish_record.get("medium", "")
                        shop_product_line = finish_record.get("shop_product_line", "")
                        shop_sku = finish_record.get("shop_sku", "")
                        vendor = finish_record.get("vendor", "")
                elif finish_slot and finish_slot.other_brand:
                    # Handle "Other" manual finishes - use metadata from slot
                    color_brand = finish_slot.other_brand or ""
                    color_name = finish_slot.other_name or ""
                    color_code = finish_slot.other_code or ""
                    medium = finish_type  # Use finish_type as medium for "Other"
                    shop_product_line = ""
                    shop_sku = ""
                    vendor = ""
            else:
                # Room not found - use defaults
                finish_type = ""
                finish_number = 0
                finish_label = ""
                box_material = "Melamine"  # Default when room not found
                finish_slot = None
            
            # Calculate pricing
            unit_price = 0.0
            line_total = 0.0
            if pricing_enabled and room_obj:
                unit_price = calculate_cabinet_price(line, room_obj, finish_slot, pricing_config)
                line_total = unit_price * line.quantity
                room_totals[line.room] = room_totals.get(line.room, 0.0) + line_total
                job_total += line_total
            
            # Write order CSV row
            order_writer.writerow([
                job.job_name or "",
                job.job_number or "",
                job.client_name or "",
                job.client_email or "",
                job.site_address or "",
                job.designer or "",
                job.delivery_or_pickup or "",
                job.requested_delivery_date or "",
                line.room or "",
                cabinet_type,
                cabinet_code,
                family_code,
                line.width_in,
                line.height_in,
                line.depth_in,
                line.quantity,
                finish_type,
                finish_number,
                finish_label,
                finish_id or "",
                color_brand,
                color_name,
                color_code,
                medium,
                shop_product_line,
                shop_sku,
                vendor,
                door_style,
                grain_direction,
                box_material,
                line.hinge_side or "",
                line.rollout_trays_qty or 0,
                line.trash_kit or "",
                line.applied_panels or 0,
                line.special_instructions or "",
                unit_price,
                line_total
            ])
            
            # Track counts per room for room schedule
            if line.room not in room_finish_counts:
                room_finish_counts[line.room] = {"cabinet_count": 0, "accessory_count": 0}
            
            if is_accessory:
                room_finish_counts[line.room]["accessory_count"] += line.quantity
            else:
                room_finish_counts[line.room]["cabinet_count"] += line.quantity
        
        # Build room schedule CSV
        schedule_output = StringIO()
        schedule_writer = csv.writer(schedule_output)
        
        # Room schedule CSV Header
        schedule_writer.writerow([
        "room_name", "room_number", "finish_code", "finish_label", "finish_id",
        "color_brand", "color_name", "color_code", "medium", "pull",
        "door_style", "grain_direction", "box_material",
        "has_crown", "has_light_valance", "cabinet_count", "accessory_count",
        "room_total"
    ])
        
        # Write room schedule rows (one per room)
        for room in rooms:
            # Derive finish_code
            if room.finish_type == "Paint":
                finish_code = f"PAINT {room.finish_number}"
            elif room.finish_type == "Melamine":
                finish_code = f"MEL {room.finish_number}"
            else:
                finish_code = f"STAIN {room.finish_number}"
            
            finish_label = resolve_finish_label(finishes, room.finish_type, room.finish_number)
            finish_id = resolve_finish_id(finishes, room.finish_type, room.finish_number)
            
            # Look up library metadata
            color_brand = ""
            color_name = ""
            color_code = ""
            medium = ""
            
            if finish_id:
                finish_record = get_finish_by_id(finish_id)
                if finish_record:
                    color_brand = finish_record.get("color_brand", "")
                    color_name = finish_record.get("color_name", "")
                    color_code = finish_record.get("color_code", "")
                    medium = finish_record.get("medium", "")
            
            # Get counts for this room
            counts = room_finish_counts.get(room.name, {"cabinet_count": 0, "accessory_count": 0})
            
            # Get room total from pricing
            room_total = room_totals.get(room.name, 0.0) if pricing_enabled else 0.0
            
            schedule_writer.writerow([
                room.name,
                room.number or "",
                finish_code,
                finish_label,
                finish_id or "",
                color_brand,
                color_name,
                color_code,
                medium,
                room.pull,
                room.door_style or "",
                room.grain_direction or "",
                room.box_material or "Melamine",
                "Yes" if room.has_crown else "No",
                "Yes" if room.has_light_valance else "No",
                counts["cabinet_count"],
                counts["accessory_count"],
                room_total
            ])
        
        # Create ZIP file in memory
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add order CSV
            order_output.seek(0)
            zip_file.writestr("order.csv", order_output.getvalue())
            
            # Add room schedule CSV
            schedule_output.seek(0)
            zip_file.writestr("room_schedule.csv", schedule_output.getvalue())
        
        zip_buffer.seek(0)
        filename = f"ACC_Express_Order_{job.job_name.replace(' ', '_')}.zip"
        
        logger.info(f"ZIP file generated successfully: {filename}")
        
        return StreamingResponse(
            iter([zip_buffer.getvalue()]),
            media_type="application/zip",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )
    
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=400, detail=f"Invalid request data: {str(e)}")
    except KeyError as e:
        logger.error(f"Missing key error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=400, detail=f"Missing required field: {str(e)}")
    except AttributeError as e:
        logger.error(f"Attribute error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=400, detail=f"Invalid attribute access: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in express_order_submit: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

