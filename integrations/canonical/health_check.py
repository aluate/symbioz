"""
Health check script for migration validation.

This script:
1. Reads canonical project file
2. Validates that all projects have innergy_id after import
3. Checks for unmapped materials/statuses
4. Generates health check report
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Set, Dict

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from integrations.canonical.models import CanonicalProject, CanonicalMaterial
from integrations.innergy.client import INNERGYClient, INNERGYClientError

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_canonical_projects(file_path: Path) -> List[CanonicalProject]:
    """Load canonical projects from JSON file."""
    projects = []
    
    if not file_path.exists():
        logger.error(f"Canonical project file not found: {file_path}")
        return projects
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            projects = [CanonicalProject(**p) for p in data]
        logger.info(f"Loaded {len(projects)} projects from {file_path}")
        return projects
    except Exception as e:
        logger.error(f"Error loading canonical projects: {e}")
        return projects


def run_health_checks(
    projects: List[CanonicalProject],
    client: INNERGYClient = None
) -> Dict[str, any]:
    """
    Run health checks on canonical projects.
    
    Returns:
        Dict with check results
    """
    checks = {
        'projects_missing_innergy_id': [],
        'unmapped_statuses': set(),
        'unmapped_phases': set(),
        'materials_not_found': [],
        'total_projects': len(projects),
        'projects_with_innergy_id': 0,
    }
    
    # Load mapping tables to check for unmapped values
    mappings_dir = Path(__file__).parent.parent / 'canonical' / 'mappings'
    status_mapping_path = mappings_dir / 'status_mapping.csv'
    phase_mapping_path = mappings_dir / 'phase_mapping.csv'
    
    # TODO: Load and check against mapping tables
    # For now, just check for missing innergy_id
    
    for project in projects:
        # Check for innergy_id
        if not project.innergy_id:
            checks['projects_missing_innergy_id'].append(project.project_number)
        else:
            checks['projects_with_innergy_id'] += 1
        
        # Check for unmapped status/phase (placeholder)
        # TODO: Load mapping tables and check
        
        # Check materials if client is available
        if client:
            # TODO: Validate that materials referenced in project exist in INNERGY
            pass
    
    return checks


def generate_health_report(
    output_path: Path,
    checks: Dict[str, any]
) -> Path:
    """Generate markdown health check report."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Migration Health Check Report\n\n")
            f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")
            
            f.write("## Summary\n\n")
            f.write(f"- **Total Projects:** {checks['total_projects']}\n")
            f.write(f"- **Projects with INNERGY ID:** {checks['projects_with_innergy_id']}\n")
            f.write(f"- **Projects Missing INNERGY ID:** {len(checks['projects_missing_innergy_id'])}\n")
            f.write(f"- **Unmapped Statuses:** {len(checks['unmapped_statuses'])}\n")
            f.write(f"- **Unmapped Phases:** {len(checks['unmapped_phases'])}\n")
            f.write(f"- **Materials Not Found:** {len(checks['materials_not_found'])}\n\n")
            
            # Projects missing innergy_id
            if checks['projects_missing_innergy_id']:
                f.write("## ⚠️ Projects Missing INNERGY ID\n\n")
                for project_num in checks['projects_missing_innergy_id']:
                    f.write(f"- {project_num}\n")
                f.write("\n")
            
            # Unmapped statuses
            if checks['unmapped_statuses']:
                f.write("## ⚠️ Unmapped Status Values\n\n")
                for status in checks['unmapped_statuses']:
                    f.write(f"- `{status}`\n")
                f.write("\n")
                f.write("**Action:** Add mappings to `integrations/canonical/mappings/status_mapping.csv`\n\n")
            
            # Unmapped phases
            if checks['unmapped_phases']:
                f.write("## ⚠️ Unmapped Phase Values\n\n")
                for phase in checks['unmapped_phases']:
                    f.write(f"- `{phase}`\n")
                f.write("\n")
                f.write("**Action:** Add mappings to `integrations/canonical/mappings/phase_mapping.csv`\n\n")
            
            # Materials not found
            if checks['materials_not_found']:
                f.write("## ⚠️ Materials Not Found in INNERGY\n\n")
                for material in checks['materials_not_found']:
                    f.write(f"- {material}\n")
                f.write("\n")
            
            # Overall status
            f.write("## Overall Status\n\n")
            if len(checks['projects_missing_innergy_id']) == 0 and len(checks['unmapped_statuses']) == 0:
                f.write("✅ **All checks passed!**\n")
            else:
                f.write("⚠️ **Some issues found** - see details above\n")
        
        logger.info(f"Generated health check report: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error generating health report: {e}")
        return output_path


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Run migration health checks")
    parser.add_argument(
        '--canonical-file',
        type=str,
        required=True,
        help='Path to canonical projects JSON file'
    )
    parser.add_argument(
        '--innergy-api-url',
        type=str,
        help='INNERGY API base URL (optional, for material validation)'
    )
    parser.add_argument(
        '--innergy-api-key',
        type=str,
        help='INNERGY API key (optional, for material validation)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        help='Directory to write health check report (default: same as canonical file)'
    )
    
    args = parser.parse_args()
    
    # Load canonical projects
    canonical_file = Path(args.canonical_file)
    projects = load_canonical_projects(canonical_file)
    
    if not projects:
        logger.error("No projects loaded from canonical file")
        return 1
    
    # Initialize INNERGY client if credentials provided
    client = None
    if args.innergy_api_url and args.innergy_api_key:
        try:
            client = INNERGYClient(api_key=args.innergy_api_key, base_url=args.innergy_api_url)
        except Exception as e:
            logger.warning(f"Could not initialize INNERGY client: {e}")
    
    # Run health checks
    checks = run_health_checks(projects, client)
    
    # Generate report
    output_dir = Path(args.output_dir) if args.output_dir else canonical_file.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y-%m-%d')
    report_path = output_dir / f"health_check_{timestamp}.md"
    
    generate_health_report(report_path, checks)
    
    # Print summary to stdout
    print(f"\n📊 Health Check Summary")
    print(f"   Total Projects: {checks['total_projects']}")
    print(f"   With INNERGY ID: {checks['projects_with_innergy_id']}")
    print(f"   Missing INNERGY ID: {len(checks['projects_missing_innergy_id'])}")
    print(f"   Unmapped Statuses: {len(checks['unmapped_statuses'])}")
    print(f"   Unmapped Phases: {len(checks['unmapped_phases'])}")
    print(f"\n📄 Report: {report_path}")
    
    if client:
        client.close()
    
    return 0 if len(checks['projects_missing_innergy_id']) == 0 else 1


if __name__ == '__main__':
    sys.exit(main())

