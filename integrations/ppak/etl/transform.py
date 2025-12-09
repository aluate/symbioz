"""
Transform PPak data to canonical format.

This module contains functions to convert PPak export rows into
CanonicalProject and CanonicalMaterial instances.
"""

import logging
from datetime import datetime
from decimal import Decimal
from typing import List, Dict, Optional
import csv
from pathlib import Path

from integrations.ppak.schemas import PPakProjectRow, PPakMaterialRow
from integrations.canonical.models import CanonicalProject, CanonicalMaterial

logger = logging.getLogger(__name__)


def load_mapping_table(mapping_file: Path) -> Dict[str, Dict[str, str]]:
    """
    Load a mapping CSV file and return as dictionary.
    
    Expected CSV format: ppak_value,canonical_value,innergy_value,notes
    
    Returns: Dict mapping ppak_value -> {canonical: ..., innergy: ...}
    """
    mapping = {}
    
    if not mapping_file.exists():
        logger.warning(f"Mapping file not found: {mapping_file}")
        return mapping
    
    try:
        with open(mapping_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ppak_key = row.get('ppak_status') or row.get('ppak_phase') or row.get('ppak_sku', '')
                if ppak_key:
                    mapping[ppak_key] = {
                        'canonical': row.get('canonical_status') or row.get('canonical_phase') or row.get('canonical_sku', ''),
                        'innergy': row.get('innergy_status') or row.get('innergy_phase') or row.get('innergy_sku', ''),
                    }
    except Exception as e:
        logger.error(f"Error loading mapping file {mapping_file}: {e}")
    
    return mapping


def parse_date(date_str: Optional[str]) -> Optional[datetime]:
    """Parse date string from PPak CSV into date object."""
    if not date_str:
        return None
    
    # TODO: Update date parsing based on actual PPak date format
    # Common formats: "2024-01-15", "01/15/2024", "2024-01-15 10:00:00"
    try:
        # Try ISO format first
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except:
        try:
            # Try common US format
            return datetime.strptime(date_str, "%m/%d/%Y")
        except:
            logger.warning(f"Could not parse date: {date_str}")
            return None


def parse_decimal(value_str: Optional[str]) -> Optional[Decimal]:
    """Parse decimal string from PPak CSV."""
    if not value_str:
        return None
    
    try:
        # Remove currency symbols, commas
        cleaned = value_str.replace('$', '').replace(',', '').strip()
        return Decimal(cleaned)
    except:
        logger.warning(f"Could not parse decimal: {value_str}")
        return None


def transform_ppak_project_to_canonical(
    ppak_row: PPakProjectRow,
    status_mapping: Dict[str, Dict[str, str]],
    phase_mapping: Dict[str, Dict[str, str]],
    mappings_dir: Path
) -> Optional[CanonicalProject]:
    """
    Transform a PPak project row into a CanonicalProject.
    
    Args:
        ppak_row: PPak project row from CSV
        status_mapping: Status mapping dictionary
        phase_mapping: Phase mapping dictionary
        mappings_dir: Directory containing mapping CSV files
    
    Returns:
        CanonicalProject instance, or None if transformation fails
    """
    try:
        # Map status
        ppak_status = ppak_row.status or "Unknown"
        canonical_status = status_mapping.get(ppak_status, {}).get('canonical', ppak_status.lower().replace(' ', '_'))
        
        if ppak_status not in status_mapping:
            logger.warning(f"Unknown PPak status: {ppak_status}, using '{canonical_status}'")
        
        # Map phase
        ppak_phase = ppak_row.phase or "Unknown"
        canonical_phase = phase_mapping.get(ppak_phase, {}).get('canonical', ppak_phase.lower().replace(' ', '_'))
        
        if ppak_phase not in phase_mapping:
            logger.warning(f"Unknown PPak phase: {ppak_phase}, using '{canonical_phase}'")
        
        # Generate project number (use job_number if available, otherwise project_id)
        project_number = ppak_row.job_number or ppak_row.project_id or f"PROJ-{ppak_row.project_id or 'UNKNOWN'}"
        
        # Parse dates
        start_date = parse_date(ppak_row.start_date)
        completion_date = parse_date(ppak_row.completion_date)
        
        # Parse estimated value
        estimated_value = parse_decimal(ppak_row.estimated_value)
        
        # Create canonical project
        canonical = CanonicalProject(
            project_number=project_number,
            name=ppak_row.project_name or "Unnamed Project",
            customer_name=ppak_row.customer or "Unknown Customer",
            customer_email=ppak_row.customer_email,
            customer_phone=ppak_row.customer_phone,
            status=canonical_status,
            phase=canonical_phase,
            start_date=start_date.date() if start_date else None,
            target_completion_date=completion_date.date() if completion_date else None,
            ppak_id=ppak_row.project_id,
            ppak_job_number=ppak_row.job_number,
            notes=ppak_row.notes,
            address=ppak_row.address,
            estimated_value=estimated_value,
        )
        
        return canonical
        
    except Exception as e:
        logger.error(f"Error transforming PPak project row: {e}")
        return None


def transform_ppak_material_to_canonical(
    ppak_row: PPakMaterialRow,
    material_mapping: Dict[str, Dict[str, str]],
    mappings_dir: Path
) -> Optional[CanonicalMaterial]:
    """
    Transform a PPak material row into a CanonicalMaterial.
    
    Args:
        ppak_row: PPak material row from CSV
        material_mapping: Material SKU mapping dictionary
        mappings_dir: Directory containing mapping CSV files
    
    Returns:
        CanonicalMaterial instance, or None if transformation fails
    """
    try:
        # Map SKU
        ppak_sku = ppak_row.sku or "UNKNOWN"
        canonical_sku = material_mapping.get(ppak_sku, {}).get('canonical', ppak_sku)
        
        if ppak_sku not in material_mapping:
            logger.warning(f"Unknown PPak SKU: {ppak_sku}, using '{canonical_sku}'")
        
        # Parse cost
        cost_per_unit = parse_decimal(ppak_row.cost)
        
        # Parse active status
        is_active = True
        if ppak_row.is_active:
            active_str = str(ppak_row.is_active).lower()
            is_active = active_str in ('true', '1', 'yes', 'active', 'y')
        
        # Create canonical material
        canonical = CanonicalMaterial(
            sku=canonical_sku,
            description=ppak_row.description or "No description",
            category=ppak_row.category or "other",
            unit_of_measure=ppak_row.unit_of_measure or "each",
            cost_per_unit=cost_per_unit,
            vendor=ppak_row.vendor,
            vendor_part_number=ppak_row.vendor_part_number,
            is_active=is_active,
            ppak_sku=ppak_row.sku,
            ppak_id=ppak_row.material_id,
            notes=ppak_row.notes,
        )
        
        return canonical
        
    except Exception as e:
        logger.error(f"Error transforming PPak material row: {e}")
        return None

