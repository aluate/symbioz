"""
CLI for importing canonical projects into INNERGY.

This script:
1. Reads canonical project file
2. Validates projects against INNERGY API requirements
3. Creates/updates projects in INNERGY (dry-run or real)
4. Updates canonical file with innergy_id values
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from integrations.innergy.client import INNERGYClient, INNERGYClientError
from integrations.canonical.models import CanonicalProject

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


def validate_project_for_innergy(project: CanonicalProject) -> List[str]:
    """
    Validate a canonical project against INNERGY API requirements.
    
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    # TODO: Update validation rules based on actual INNERGY API requirements
    if not project.project_number:
        errors.append("Missing project_number")
    if not project.name:
        errors.append("Missing name")
    if not project.customer_name:
        errors.append("Missing customer_name")
    
    return errors


def import_project_to_innergy(
    client: INNERGYClient,
    project: CanonicalProject,
    dry_run: bool = True
) -> Dict[str, any]:
    """
    Import a single project to INNERGY.
    
    Returns:
        Dict with 'success', 'innergy_id', 'error'
    """
    # Validate project
    validation_errors = validate_project_for_innergy(project)
    if validation_errors:
        return {
            'success': False,
            'error': f"Validation failed: {', '.join(validation_errors)}"
        }
    
    # Convert canonical project to INNERGY format
    # TODO: Update this mapping based on actual INNERGY API requirements
    innergy_data = {
        'project_number': project.project_number,
        'name': project.name,
        'customer_name': project.customer_name,
        'customer_email': project.customer_email,
        'customer_phone': project.customer_phone,
        'status': project.status,
        'phase': project.phase,
        'start_date': project.start_date.isoformat() if project.start_date else None,
        'target_completion_date': project.target_completion_date.isoformat() if project.target_completion_date else None,
        'notes': project.notes,
        'address': project.address,
    }
    
    try:
        if dry_run:
            logger.info(f"[DRY RUN] Would import project: {project.project_number}")
            return {
                'success': True,
                'innergy_id': f"dry_run_{project.project_number}",
                'error': None
            }
        else:
            if project.innergy_id:
                # Update existing project
                updated = client.update_project(project.innergy_id, innergy_data)
                logger.info(f"Updated project: {updated.id}")
                return {
                    'success': True,
                    'innergy_id': updated.id,
                    'error': None
                }
            else:
                # Create new project
                created = client.create_project(innergy_data)
                logger.info(f"Created project: {created.id}")
                return {
                    'success': True,
                    'innergy_id': created.id,
                    'error': None
                }
    except INNERGYClientError as e:
        logger.error(f"Error importing project {project.project_number}: {e}")
        return {
            'success': False,
            'error': str(e)
        }


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Import canonical projects into INNERGY")
    parser.add_argument(
        '--canonical-file',
        type=str,
        required=True,
        help='Path to canonical projects JSON file'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        help='INNERGY API key (or use INNERGY_API_KEY env var)'
    )
    parser.add_argument(
        '--api-url',
        type=str,
        help='INNERGY API base URL (or use INNERGY_API_BASE_URL env var)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        default=True,
        help='Dry run mode (default: True, use --no-dry-run for actual import)'
    )
    parser.add_argument(
        '--no-dry-run',
        dest='dry_run',
        action='store_false',
        help='Perform actual import (not dry run)'
    )
    parser.add_argument(
        '--update-canonical',
        action='store_true',
        help='Update canonical file with innergy_id values after import'
    )
    
    args = parser.parse_args()
    
    # Get API credentials
    import os
    api_key = args.api_key or os.getenv('INNERGY_API_KEY')
    api_url = args.api_url or os.getenv('INNERGY_API_BASE_URL')
    
    if not api_key or not api_url:
        logger.error("INNERGY API key and URL required (via args or env vars)")
        return 1
    
    # Load canonical projects
    canonical_file = Path(args.canonical_file)
    projects = load_canonical_projects(canonical_file)
    
    if not projects:
        logger.error("No projects loaded from canonical file")
        return 1
    
    # Initialize INNERGY client
    try:
        client = INNERGYClient(api_key=api_key, base_url=api_url)
        
        # Import projects
        results = {
            'created': 0,
            'updated': 0,
            'skipped': 0,
            'failed': 0,
            'errors': []
        }
        
        updated_projects = []
        
        for project in projects:
            result = import_project_to_innergy(client, project, dry_run=args.dry_run)
            
            if result['success']:
                if project.innergy_id:
                    results['updated'] += 1
                else:
                    results['created'] += 1
                
                # Update project with innergy_id
                if result['innergy_id']:
                    project.innergy_id = result['innergy_id']
                    updated_projects.append(project)
            else:
                results['failed'] += 1
                results['errors'].append(f"{project.project_number}: {result['error']}")
                logger.warning(f"Failed to import project {project.project_number}: {result['error']}")
        
        # Update canonical file if requested
        if args.update_canonical and updated_projects:
            # Write updated projects back to file
            all_projects_dict = [p.dict() for p in projects]
            with open(canonical_file, 'w', encoding='utf-8') as f:
                json.dump(all_projects_dict, f, indent=2, default=str)
            logger.info(f"Updated canonical file with innergy_id values")
        
        # Print summary
        print(f"\n📊 Import Summary")
        print(f"   Created: {results['created']}")
        print(f"   Updated: {results['updated']}")
        print(f"   Failed: {results['failed']}")
        
        if args.dry_run:
            print(f"\n🔍 DRY RUN MODE - No changes were made")
        else:
            print(f"\n✅ Import complete!")
        
        if results['errors']:
            print(f"\n⚠️  Errors:")
            for error in results['errors'][:10]:
                print(f"   - {error}")
            if len(results['errors']) > 10:
                print(f"   ... and {len(results['errors']) - 10} more")
        
        client.close()
        return 0 if results['failed'] == 0 else 1
        
    except INNERGYClientError as e:
        logger.error(f"INNERGY API error: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())

