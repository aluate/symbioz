"""
CLI entry point for running PPak ETL migration.

This script:
1. Reads PPak export CSVs from a directory
2. Transforms them to canonical format
3. Writes canonical JSON/CSV files to output directory
4. Generates a summary report
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import csv

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from integrations.ppak.schemas import PPakProjectRow, PPakMaterialRow
from integrations.ppak.etl.transform import (
    transform_ppak_project_to_canonical,
    transform_ppak_material_to_canonical,
    load_mapping_table,
)
from integrations.canonical.models import CanonicalProject, CanonicalMaterial

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def read_ppak_csv(file_path: Path, row_class) -> List:
    """
    Read a PPak CSV file and return list of parsed rows.
    
    Args:
        file_path: Path to CSV file
        row_class: Pydantic model class for rows
    
    Returns:
        List of parsed row instances
    """
    rows = []
    
    if not file_path.exists():
        logger.warning(f"File not found: {file_path}")
        return rows
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for csv_row in reader:
                try:
                    # Create Pydantic model from CSV row
                    row = row_class(**csv_row)
                    rows.append(row)
                except Exception as e:
                    logger.warning(f"Error parsing row in {file_path}: {e}")
                    continue
    except Exception as e:
        logger.error(f"Error reading CSV file {file_path}: {e}")
    
    return rows


def write_canonical_json(output_path: Path, canonical_objects: List):
    """Write canonical objects to JSON file."""
    try:
        data = [obj.dict() for obj in canonical_objects]
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        logger.info(f"Wrote {len(canonical_objects)} objects to {output_path}")
    except Exception as e:
        logger.error(f"Error writing JSON file {output_path}: {e}")


def generate_summary_report(
    output_dir: Path,
    projects: List[CanonicalProject],
    materials: List[CanonicalMaterial],
    errors: List[str]
) -> Path:
    """Generate a markdown summary report."""
    report_path = output_dir / f"migration_summary_{datetime.now().strftime('%Y-%m-%d')}.md"
    
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# PPak ETL Migration Summary\n\n")
            f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")
            
            f.write("## Statistics\n\n")
            f.write(f"- **Projects processed:** {len(projects)}\n")
            f.write(f"- **Materials processed:** {len(materials)}\n")
            f.write(f"- **Errors/Warnings:** {len(errors)}\n\n")
            
            if errors:
                f.write("## Errors and Warnings\n\n")
                for error in errors:
                    f.write(f"- {error}\n")
                f.write("\n")
            
            f.write("## Sample Projects\n\n")
            for i, project in enumerate(projects[:5], 1):
                f.write(f"### Project {i}\n")
                f.write(f"- **Number:** {project.project_number}\n")
                f.write(f"- **Name:** {project.name}\n")
                f.write(f"- **Status:** {project.status}\n")
                f.write(f"- **Phase:** {project.phase}\n")
                f.write(f"- **Customer:** {project.customer_name}\n\n")
            
            if len(projects) > 5:
                f.write(f"*... and {len(projects) - 5} more projects*\n\n")
        
        logger.info(f"Generated summary report: {report_path}")
        return report_path
        
    except Exception as e:
        logger.error(f"Error generating summary report: {e}")
        return report_path


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Run PPak ETL migration")
    parser.add_argument(
        '--ppak-export-dir',
        type=str,
        required=True,
        help='Directory containing PPak export CSV files'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        required=True,
        help='Directory to write canonical output files'
    )
    parser.add_argument(
        '--date-range',
        type=str,
        help='Optional date range filter (format: YYYY-MM-DD,YYYY-MM-DD)'
    )
    parser.add_argument(
        '--mappings-dir',
        type=str,
        default='integrations/canonical/mappings',
        help='Directory containing mapping CSV files'
    )
    
    args = parser.parse_args()
    
    # Setup paths
    ppak_dir = Path(args.ppak_export_dir)
    output_dir = Path(args.output_dir)
    mappings_dir = Path(args.mappings_dir)
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load mapping tables
    logger.info("Loading mapping tables...")
    status_mapping = load_mapping_table(mappings_dir / 'status_mapping.csv')
    phase_mapping = load_mapping_table(mappings_dir / 'phase_mapping.csv')
    material_mapping = load_mapping_table(mappings_dir / 'material_mapping.csv')
    
    # Find PPak export files
    project_files = list(ppak_dir.glob('*project*.csv')) + list(ppak_dir.glob('*job*.csv'))
    material_files = list(ppak_dir.glob('*material*.csv'))
    
    logger.info(f"Found {len(project_files)} project files and {len(material_files)} material files")
    
    # Process projects
    all_projects = []
    all_materials = []
    errors = []
    
    for project_file in project_files:
        logger.info(f"Processing project file: {project_file}")
        ppak_projects = read_ppak_csv(project_file, PPakProjectRow)
        
        for ppak_project in ppak_projects:
            canonical = transform_ppak_project_to_canonical(
                ppak_project,
                status_mapping,
                phase_mapping,
                mappings_dir
            )
            if canonical:
                all_projects.append(canonical)
            else:
                errors.append(f"Failed to transform project: {ppak_project.project_id or 'unknown'}")
    
    # Process materials
    for material_file in material_files:
        logger.info(f"Processing material file: {material_file}")
        ppak_materials = read_ppak_csv(material_file, PPakMaterialRow)
        
        for ppak_material in ppak_materials:
            canonical = transform_ppak_material_to_canonical(
                ppak_material,
                material_mapping,
                mappings_dir
            )
            if canonical:
                all_materials.append(canonical)
            else:
                errors.append(f"Failed to transform material: {ppak_material.sku or 'unknown'}")
    
    # Write canonical files
    timestamp = datetime.now().strftime('%Y-%m-%d')
    
    if all_projects:
        projects_output = output_dir / f"canonical_projects_{timestamp}.json"
        write_canonical_json(projects_output, all_projects)
        logger.info(f"Wrote {len(all_projects)} projects to {projects_output}")
    
    if all_materials:
        materials_output = output_dir / f"canonical_materials_{timestamp}.json"
        write_canonical_json(materials_output, all_materials)
        logger.info(f"Wrote {len(all_materials)} materials to {materials_output}")
    
    # Generate summary report
    report_path = generate_summary_report(output_dir, all_projects, all_materials, errors)
    
    # Print summary to stdout (for Otto to parse)
    print(f"✅ Migration complete!")
    print(f"   Projects: {len(all_projects)}")
    print(f"   Materials: {len(all_materials)}")
    print(f"   Errors: {len(errors)}")
    print(f"   Report: {report_path}")
    
    if errors:
        print(f"\n⚠️  Warnings/Errors:")
        for error in errors[:10]:  # Show first 10
            print(f"   - {error}")
        if len(errors) > 10:
            print(f"   ... and {len(errors) - 10} more (see report)")
    
    return 0 if len(errors) == 0 else 1


if __name__ == '__main__':
    sys.exit(main())

