"""JSON export for full project state."""

import json
from pathlib import Path
from typing import Any, Dict
from datetime import datetime
from .model import (
    PoleBarnInputs,
    GeometryModel,
    MaterialTakeoff,
    PartQuantity,
    PricedLineItem,
    PricingSummary,
)


def export_project_to_json(
    inputs: PoleBarnInputs,
    geometry: GeometryModel,
    takeoff: MaterialTakeoff,
    bom: list[PartQuantity],
    priced_items: list[PricedLineItem],
    summary: PricingSummary,
    output_path: Path,
) -> None:
    """
    Export full project state to JSON.
    
    Args:
        inputs: Original inputs
        geometry: Derived geometry
        takeoff: Material takeoff
        bom: Bill of materials
        priced_items: Priced line items
        summary: Pricing summary
        output_path: Path to save JSON file
    """
    # Convert dataclasses to dicts
    def dataclass_to_dict(obj: Any) -> Dict[str, Any]:
        if hasattr(obj, "__dict__"):
            result = {}
            for key, value in obj.__dict__.items():
                if hasattr(value, "__dict__"):
                    result[key] = dataclass_to_dict(value)
                elif isinstance(value, list):
                    result[key] = [dataclass_to_dict(item) if hasattr(item, "__dict__") else item for item in value]
                else:
                    result[key] = value
            return result
        return obj
    
    project_data = {
        "metadata": {
            "export_date": datetime.now().isoformat(),
            "project_name": inputs.project_name,
            "version": "1.0",
        },
        "inputs": {
            "geometry": dataclass_to_dict(inputs.geometry),
            "materials": dataclass_to_dict(inputs.materials),
            "pricing": dataclass_to_dict(inputs.pricing),
            "assemblies": dataclass_to_dict(inputs.assemblies),
            "project_name": inputs.project_name,
            "notes": inputs.notes,
            "build_type": inputs.build_type,
            "construction_type": inputs.construction_type,
            "building_type": inputs.building_type,
            "building_use": inputs.building_use,
            "permitting_agency": inputs.permitting_agency,
            "required_snow_load_psf": inputs.required_snow_load_psf,
            "requested_snow_load_psf": inputs.requested_snow_load_psf,
            "snow_load_unknown": inputs.snow_load_unknown,
        },
        "geometry": dataclass_to_dict(geometry),
        "material_takeoff": {
            "items": [dataclass_to_dict(item) for item in takeoff.items],
        },
        "bom": [dataclass_to_dict(item) for item in bom],
        "priced_items": [dataclass_to_dict(item) for item in priced_items],
        "pricing_summary": dataclass_to_dict(summary),
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(project_data, f, indent=2, default=str)


def generate_json_filename(project_name: str | None = None) -> str:
    """Generate filename for JSON export."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if project_name:
        safe_name = "".join(c for c in project_name if c.isalnum() or c in (" ", "-", "_")).strip()
        safe_name = safe_name.replace(" ", "_")
        return f"project_{safe_name}_{timestamp}.json"
    return f"project_{timestamp}.json"

