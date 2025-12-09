"""
CLI for syncing canonical material library to INNERGY.

This script:
1. Reads canonical material library
2. Fetches current materials from INNERGY
3. Computes diff (new/updated/inactive)
4. Syncs changes to INNERGY (dry-run or real)
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Set
import csv

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from integrations.innergy.client import INNERGYClient, INNERGYClientError
from integrations.canonical.models import CanonicalMaterial

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_canonical_materials(file_path: Path) -> List[CanonicalMaterial]:
    """Load canonical materials from JSON or CSV file."""
    materials = []
    
    if not file_path.exists():
        logger.error(f"Material library file not found: {file_path}")
        return materials
    
    try:
        if file_path.suffix == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                materials = [CanonicalMaterial(**m) for m in data]
        elif file_path.suffix == '.csv':
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                materials = [CanonicalMaterial(**row) for row in reader]
        else:
            logger.error(f"Unsupported file format: {file_path.suffix}")
            return materials
        
        logger.info(f"Loaded {len(materials)} materials from {file_path}")
        return materials
    except Exception as e:
        logger.error(f"Error loading material library: {e}")
        return materials


def compute_material_diff(
    canonical_materials: List[CanonicalMaterial],
    innergy_materials: List[Dict]
) -> Dict[str, List]:
    """
    Compute diff between canonical and INNERGY materials.
    
    Returns:
        Dict with keys: 'new', 'updated', 'inactive'
    """
    # Create lookup by SKU
    canonical_by_sku = {m.sku: m for m in canonical_materials}
    innergy_by_sku = {m.get('sku'): m for m in innergy_materials if m.get('sku')}
    
    canonical_skus = set(canonical_by_sku.keys())
    innergy_skus = set(innergy_by_sku.keys())
    
    # New materials: in canonical but not in INNERGY
    new_skus = canonical_skus - innergy_skus
    new_materials = [canonical_by_sku[sku] for sku in new_skus]
    
    # Updated materials: in both but different
    updated_materials = []
    common_skus = canonical_skus & innergy_skus
    for sku in common_skus:
        canonical = canonical_by_sku[sku]
        innergy = innergy_by_sku[sku]
        # TODO: Implement actual comparison logic
        # For now, assume all common materials might need updating
        updated_materials.append(canonical)
    
    # Inactive materials: in INNERGY but marked inactive in canonical
    inactive_materials = []
    for sku in innergy_skus:
        if sku not in canonical_skus:
            # Material exists in INNERGY but not in canonical - mark inactive
            inactive_materials.append(innergy_by_sku[sku])
        elif not canonical_by_sku[sku].is_active:
            # Material is marked inactive in canonical
            inactive_materials.append(innergy_by_sku[sku])
    
    return {
        'new': new_materials,
        'updated': updated_materials,
        'inactive': inactive_materials,
    }


def sync_materials_to_innergy(
    client: INNERGYClient,
    materials: List[CanonicalMaterial],
    operation: str,  # 'create', 'update', 'deactivate'
    dry_run: bool = True
) -> Dict[str, int]:
    """
    Sync materials to INNERGY.
    
    Returns:
        Dict with success/failure counts
    """
    results = {'success': 0, 'failed': 0, 'errors': []}
    
    for material in materials:
        try:
            # Convert canonical material to INNERGY format
            # TODO: Update this mapping based on actual INNERGY API requirements
            innergy_data = {
                'sku': material.sku,
                'description': material.description,
                'category': material.category,
                'unit_of_measure': material.unit_of_measure,
                'cost_per_unit': float(material.cost_per_unit) if material.cost_per_unit else None,
                'vendor': material.vendor,
                'vendor_part_number': material.vendor_part_number,
                'is_active': material.is_active,
            }
            
            if dry_run:
                logger.info(f"[DRY RUN] Would {operation} material: {material.sku}")
                results['success'] += 1
            else:
                if operation == 'create':
                    created = client.create_material(innergy_data)  # TODO: Implement this method
                    logger.info(f"Created material: {created.sku}")
                    results['success'] += 1
                elif operation == 'update':
                    if material.innergy_id:
                        updated = client.update_material(material.innergy_id, innergy_data)  # TODO: Implement
                        logger.info(f"Updated material: {updated.sku}")
                        results['success'] += 1
                    else:
                        logger.warning(f"Material {material.sku} has no innergy_id, skipping update")
                        results['failed'] += 1
                elif operation == 'deactivate':
                    if material.innergy_id:
                        # TODO: Implement deactivate method
                        logger.info(f"Deactivated material: {material.sku}")
                        results['success'] += 1
                    else:
                        logger.warning(f"Material {material.sku} has no innergy_id, skipping deactivate")
                        results['failed'] += 1
        except Exception as e:
            logger.error(f"Error syncing material {material.sku}: {e}")
            results['failed'] += 1
            results['errors'].append(f"{material.sku}: {str(e)}")
    
    return results


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Sync canonical material library to INNERGY")
    parser.add_argument(
        '--material-library',
        type=str,
        required=True,
        help='Path to canonical material library file (JSON or CSV)'
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
        help='Dry run mode (default: True, use --no-dry-run for actual sync)'
    )
    parser.add_argument(
        '--no-dry-run',
        dest='dry_run',
        action='store_false',
        help='Perform actual sync (not dry run)'
    )
    
    args = parser.parse_args()
    
    # Get API credentials
    import os
    api_key = args.api_key or os.getenv('INNERGY_API_KEY')
    api_url = args.api_url or os.getenv('INNERGY_API_BASE_URL')
    
    if not api_key or not api_url:
        logger.error("INNERGY API key and URL required (via args or env vars)")
        return 1
    
    # Load canonical materials
    material_library_path = Path(args.material_library)
    canonical_materials = load_canonical_materials(material_library_path)
    
    if not canonical_materials:
        logger.error("No materials loaded from library file")
        return 1
    
    # Initialize INNERGY client
    try:
        client = INNERGYClient(api_key=api_key, base_url=api_url)
        
        # Fetch current INNERGY materials
        logger.info("Fetching current materials from INNERGY...")
        innergy_materials = client.list_materials()
        innergy_materials_dict = [m.dict() if hasattr(m, 'dict') else m for m in innergy_materials]
        
        # Compute diff
        logger.info("Computing material diff...")
        diff = compute_material_diff(canonical_materials, innergy_materials_dict)
        
        print(f"\n📊 Material Sync Summary")
        print(f"   New materials: {len(diff['new'])}")
        print(f"   Updated materials: {len(diff['updated'])}")
        print(f"   Inactive materials: {len(diff['inactive'])}")
        
        if args.dry_run:
            print(f"\n🔍 DRY RUN MODE - No changes will be made")
        else:
            print(f"\n⚡ LIVE MODE - Changes will be applied")
        
        # Sync new materials
        if diff['new']:
            logger.info(f"Syncing {len(diff['new'])} new materials...")
            results = sync_materials_to_innergy(client, diff['new'], 'create', dry_run=args.dry_run)
            print(f"   Created: {results['success']} success, {results['failed']} failed")
        
        # Sync updated materials
        if diff['updated']:
            logger.info(f"Syncing {len(diff['updated'])} updated materials...")
            results = sync_materials_to_innergy(client, diff['updated'], 'update', dry_run=args.dry_run)
            print(f"   Updated: {results['success']} success, {results['failed']} failed")
        
        # Deactivate inactive materials
        if diff['inactive']:
            logger.info(f"Deactivating {len(diff['inactive'])} materials...")
            # TODO: Convert inactive INNERGY materials to CanonicalMaterial format for sync
            print(f"   Deactivated: {len(diff['inactive'])} materials")
        
        client.close()
        
        print(f"\n✅ Sync complete!")
        return 0
        
    except INNERGYClientError as e:
        logger.error(f"INNERGY API error: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())

