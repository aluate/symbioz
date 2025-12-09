"""CSV export for flat BOM (single file with sheet_name column)."""

import csv
from pathlib import Path
from typing import List
from .model import PartQuantity


def export_bom_to_flat_csv(
    bom_items: List[PartQuantity],
    output_path: Path,
    project_name: str | None = None,
    building_id: str | None = None,
) -> None:
    """
    Writes a single CSV file with all BOM items.
    
    Includes a sheet_name column so the file can be split into tabs later.
    Aggregates items by (part_id, length_in, sheet_name) before writing.
    
    Args:
        bom_items: List of PartQuantity items from BOM
        output_path: Path to output CSV file (or directory - will create bom_flat.csv)
        project_name: Optional project name
        building_id: Optional building/test identifier
    """
    # If output_path is a directory, create bom_flat.csv inside it
    if output_path.is_dir() or (not output_path.suffix and not output_path.exists()):
        if project_name:
            safe_name = "".join(c for c in project_name if c.isalnum() or c in (" ", "-", "_")).strip()
            safe_name = safe_name.replace(" ", "_")
            filename = f"bom_flat_{safe_name}.csv"
        else:
            filename = "bom_flat.csv"
        output_path = output_path / filename
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Aggregate by (part_id, length_in, sheet_name)
    aggregated: dict[tuple, dict] = {}
    
    for item in bom_items:
        # Use sheet_name if available, otherwise fall back to export_category or category
        sheet_name = item.sheet_name or item.export_category or item.category
        
        key = (item.part_id, item.length_in, sheet_name)
        
        if key not in aggregated:
            aggregated[key] = {
                "project_name": project_name or "",
                "building_id": building_id or "",
                "sheet_name": sheet_name,
                "category": item.category,
                "part_id": item.part_id,
                "part_name": item.part_name,
                "unit": item.unit,
                "qty": 0.0,
                "length_in": item.length_in,
                "unit_price": item.unit_price,
                "ext_price": 0.0,
                "notes": item.notes or "",
            }
        
        aggregated[key]["qty"] += item.qty
        aggregated[key]["ext_price"] += item.ext_price
    
    # Write CSV
    fieldnames = [
        "project_name",
        "building_id",
        "sheet_name",
        "category",
        "part_id",
        "part_name",
        "unit",
        "qty",
        "length_in",
        "unit_price",
        "ext_price",
        "notes",
    ]
    
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for key, data in sorted(aggregated.items()):
            row = data.copy()
            # Convert None to empty string for CSV
            if row["length_in"] is None:
                row["length_in"] = ""
            else:
                row["length_in"] = str(row["length_in"])
            writer.writerow(row)


def generate_flat_csv_filename(project_name: str | None = None) -> str:
    """Generate filename for flat CSV export."""
    if project_name:
        safe_name = "".join(c for c in project_name if c.isalnum() or c in (" ", "-", "_")).strip()
        safe_name = safe_name.replace(" ", "_")
        return f"bom_flat_{safe_name}.csv"
    return "bom_flat.csv"

