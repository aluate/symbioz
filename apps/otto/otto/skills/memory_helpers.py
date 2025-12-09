"""
Memory Helpers - Shared utilities for skills to interact with OttoMemory
Phase 3B — Memory Integration

Provides helper functions for skills to:
- Lookup reminder patterns from memory
- Lookup vendor hints for tax categorization
- Track memory usage
"""

from typing import List, Dict, Any, Optional, Tuple
import os
import httpx
import re
from datetime import datetime

logger = None  # Will be set by importing skill


def get_reminder_pattern(life_os_api_url: str) -> Tuple[List[int], Optional[int], Optional[Dict]]:
    """
    Lookup default reminder pattern from OttoMemory.
    
    Phase 4: Prefers non-stale memories.
    
    Returns:
        (days_list, memory_id, memory_entry)
        - days_list: List of days before due date (e.g., [7, 1, 0] for 7 days, 1 day, day-of)
        - memory_id: ID of the memory entry used (None if not found)
        - memory_entry: Full memory entry (None if not found)
    
    Falls back to [7, 1, 0] if no memory found.
    """
    default_pattern = [7, 1, 0]  # Fallback
    
    try:
        with httpx.Client(timeout=5.0) as client:
            # Phase 4: Lookup memory, prefer non-stale
            # First try non-stale
            response = client.get(
                f"{life_os_api_url}/otto/memory",
                params={
                    "category": "preference",
                    "tags": "reminder_pattern",
                    "is_stale": False,
                    "limit": 1
                }
            )
            
            memories = []
            if response.status_code == 200:
                memories = response.json()
            
            # If no non-stale found, try any (including stale)
            if not memories:
                response = client.get(
                    f"{life_os_api_url}/otto/memory",
                    params={
                        "category": "preference",
                        "tags": "reminder_pattern",
                        "limit": 1
                    }
                )
                if response.status_code == 200:
                    memories = response.json()
            
            if memories:
                memory = memories[0]
                is_stale = memory.get("is_stale", False)
                content = memory.get("content", "")
                
                # Parse pattern from content
                days = _parse_reminder_pattern(content)
                if days:
                    # Mark as used
                    try:
                        client.post(
                            f"{life_os_api_url}/otto/memory/use",
                            json={"id": memory.get("id")}
                        )
                    except:
                        pass
                    
                    # Phase 4: Warn if using stale memory
                    if is_stale and logger:
                        logger.warning(f"Using stale reminder pattern memory (ID: {memory.get('id')})")
                    
                    return days, memory.get("id"), memory
            
            # Not found, return default
            return default_pattern, None, None
    except Exception as e:
        if logger:
            logger.warning(f"Error looking up reminder pattern: {str(e)}")
        return default_pattern, None, None


def _parse_reminder_pattern(content: str) -> Optional[List[int]]:
    """
    Parse reminder pattern from natural language content.
    
    Examples:
    - "7 days before, 1 day before, and day-of" -> [7, 1, 0]
    - "Default reminder pattern is 7 days before, 1 day before, and day-of." -> [7, 1, 0]
    - "7/1/0 days" -> [7, 1, 0]
    """
    # Try to extract numbers
    # Look for patterns like "7 days", "1 day", "day-of" or "0 days"
    numbers = re.findall(r'(\d+)\s*(?:day|days)', content.lower())
    
    if numbers:
        days = [int(n) for n in numbers]
        # Check for "day-of" or "0" which means same day
        if "day-of" in content.lower() or "day of" in content.lower():
            if 0 not in days:
                days.append(0)
        days.sort(reverse=True)  # Sort descending (7, 1, 0)
        return days if days else None
    
    # Try slash-separated format: "7/1/0"
    slash_match = re.search(r'(\d+)/(\d+)/(\d+)', content)
    if slash_match:
        return [int(slash_match.group(1)), int(slash_match.group(2)), int(slash_match.group(3))]
    
    return None


def get_vendor_hint(life_os_api_url: str, vendor_name: str) -> Tuple[Optional[str], Optional[int], Optional[Dict]]:
    """
    Lookup vendor hint from OttoMemory for tax categorization.
    
    Phase 4: Prefers non-stale memories.
    
    Args:
        life_os_api_url: Life OS backend API URL
        vendor_name: Vendor name to lookup (normalized)
    
    Returns:
        (category_code, memory_id, memory_entry)
        - category_code: Category code to use (e.g., "TOOLS_HAND")
        - memory_id: ID of the memory entry used (None if not found)
        - memory_entry: Full memory entry (None if not found)
    """
    try:
        normalized_vendor = vendor_name.upper().strip()
        
        with httpx.Client(timeout=5.0) as client:
            # Phase 4: First try non-stale memories
            response = client.get(
                f"{life_os_api_url}/otto/memory",
                params={
                    "category": "tax_hint",
                    "tags": f"vendor:{normalized_vendor}",
                    "is_stale": False,
                    "limit": 10
                }
            )
            
            memories = []
            if response.status_code == 200:
                memories = response.json()
            
            # If no non-stale found, try any (including stale)
            if not memories:
                response = client.get(
                    f"{life_os_api_url}/otto/memory",
                    params={
                        "category": "tax_hint",
                        "tags": f"vendor:{normalized_vendor}",
                        "limit": 10
                    }
                )
                if response.status_code == 200:
                    memories = response.json()
            
            # Find exact match
            for memory in memories:
                tags = memory.get("tags", [])
                is_stale = memory.get("is_stale", False)
                
                if any(f"vendor:{normalized_vendor}" in str(tag).upper() for tag in tags):
                    content = memory.get("content", "")
                    category_code = _parse_category_code_from_hint(content)
                    
                    if category_code:
                        # Mark as used
                        try:
                            client.post(
                                f"{life_os_api_url}/otto/memory/use",
                                json={"id": memory.get("id")}
                            )
                        except:
                            pass
                        
                        # Phase 4: Warn if using stale memory
                        if is_stale and logger:
                            logger.warning(f"Using stale vendor hint memory (ID: {memory.get('id')}) for vendor {vendor_name}")
                        
                        return category_code, memory.get("id"), memory
            
            return None, None, None
    except Exception as e:
        if logger:
            logger.warning(f"Error looking up vendor hint: {str(e)}")
        return None, None, None


def _parse_category_code_from_hint(content: str) -> Optional[str]:
    """
    Parse category code from vendor hint content.
    
    Examples:
    - "Vendor 'TKS' usually maps to category TOOLS_HAND" -> "TOOLS_HAND"
    - "TKS -> TOOLS_HAND" -> "TOOLS_HAND"
    """
    # Look for "category <CODE>" or "maps to category <CODE>"
    match = re.search(r'category\s+([A-Z_]+)', content, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    
    # Look for "-> CODE" or "CODE" at end
    match = re.search(r'->\s*([A-Z_]+)', content, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    
    # Look for all-caps code at end
    match = re.search(r'([A-Z_]{3,})$', content)
    if match:
        return match.group(1)
    
    return None

