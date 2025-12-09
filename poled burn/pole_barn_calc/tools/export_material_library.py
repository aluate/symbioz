"""Export material library to markdown for review."""

import sys
from pathlib import Path
import pandas as pd

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def export_material_library():
    """Export parts, pricing, and assemblies to markdown."""
    config_dir = Path(__file__).parent.parent / "config"
    output_file = Path(__file__).parent.parent / "MATERIALS_LIBRARY_EXPORT.md"
    
    # Load CSVs
    parts_df = pd.read_csv(config_dir / "parts.example.csv")
    pricing_df = pd.read_csv(config_dir / "pricing.example.csv")
    assemblies_df = pd.read_csv(config_dir / "assemblies.example.csv")
    
    # Merge parts and pricing
    merged_df = parts_df.merge(
        pricing_df,
        on="part_id",
        how="left",
        suffixes=("", "_price")
    )
    
    # Group by export_category if it exists, otherwise by category
    group_col = "export_category" if "export_category" in merged_df.columns else "category"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Materials Library Export\n\n")
        f.write("This document contains a full export of all parts, pricing, and assemblies.\n")
        f.write("**Auto-generated** - Regenerate using `tools/export_material_library.py`\n\n")
        f.write("---\n\n")
        
        # Parts and Pricing by Category
        f.write("## Parts & Pricing by Category\n\n")
        
        if group_col in merged_df.columns:
            categories = sorted(merged_df[group_col].dropna().unique())
        else:
            categories = sorted(merged_df["category"].dropna().unique())
        
        for cat in categories:
            f.write(f"### {cat}\n\n")
            cat_df = merged_df[merged_df[group_col] == cat] if group_col in merged_df.columns else merged_df[merged_df["category"] == cat]
            
            f.write("| Part ID | Part Name | Description | Unit | Unit Price | Vendor | Notes |\n")
            f.write("|---------|-----------|-------------|------|------------|--------|-------|\n")
            
            for _, row in cat_df.iterrows():
                part_id = row.get("part_id", "")
                part_name = row.get("part_name", "")
                description = row.get("description", "")
                unit = row.get("unit", "")
                unit_price = row.get("unit_price", 0.0)
                vendor = row.get("vendor", "")
                notes = row.get("notes", "")
                
                f.write(f"| {part_id} | {part_name} | {description} | {unit} | ${unit_price:.2f} | {vendor} | {notes} |\n")
            
            f.write("\n")
        
        # Assemblies
        f.write("---\n\n")
        f.write("## Assembly Mappings\n\n")
        f.write("| Assembly Name | Part ID | Waste Factor | Labor/Unit | Notes |\n")
        f.write("|---------------|---------|--------------|------------|-------|\n")
        
        for _, row in assemblies_df.iterrows():
            assembly_name = row.get("assembly_name", "")
            part_id = row.get("part_id", "")
            waste_factor = row.get("waste_factor", 1.0)
            labor_per_unit = row.get("labor_per_unit", 0.0)
            notes = row.get("notes", "")
            
            f.write(f"| {assembly_name} | {part_id} | {waste_factor} | {labor_per_unit} | {notes} |\n")
        
        f.write("\n---\n\n")
        f.write(f"**Generated:** {pd.Timestamp.now()}\n")
        f.write(f"**Total Parts:** {len(parts_df)}\n")
        f.write(f"**Total Pricing Entries:** {len(pricing_df)}\n")
        f.write(f"**Total Assemblies:** {len(assemblies_df)}\n")
    
    print(f"Material library exported to: {output_file}")

if __name__ == "__main__":
    export_material_library()

