"""
Safety Tier Registry and Permission Checking
"""

from typing import Dict, Any, Optional
from enum import IntEnum


class SafetyTier(IntEnum):
    """Privilege tiers for task types"""
    TIER_0_SAFE = 0  # Read-only, no side effects
    TIER_1_LIMITED = 1  # Limited writes, non-sensitive
    TIER_2_SENSITIVE = 2  # Sensitive actions, may require approval
    TIER_3_FINANCIAL = 3  # Financial/legal, requires approval
    TIER_4_CRITICAL = 4  # System-critical, requires explicit signature


# Registry of task types and their safety tiers
TASK_TIER_REGISTRY: Dict[str, SafetyTier] = {
    # Tier 0 - Safe/Read-only
    "otto.log": SafetyTier.TIER_0_SAFE,
    "env_status": SafetyTier.TIER_0_SAFE,
    "otto_doctor": SafetyTier.TIER_0_SAFE,
    "check_dependencies": SafetyTier.TIER_0_SAFE,
    "otto_runs": SafetyTier.TIER_0_SAFE,
    "list_otto_runs": SafetyTier.TIER_0_SAFE,
    "get_otto_run": SafetyTier.TIER_0_SAFE,
    "self_test": SafetyTier.TIER_0_SAFE,
    "test_otto": SafetyTier.TIER_0_SAFE,
    "repo_list": SafetyTier.TIER_0_SAFE,
    "repo_audit": SafetyTier.TIER_0_SAFE,
    
    # Tier 1 - Limited writes
    "life_os.create_task": SafetyTier.TIER_1_LIMITED,
    "life_os.log_note": SafetyTier.TIER_1_LIMITED,
    "life_os.list_tasks": SafetyTier.TIER_0_SAFE,  # Read-only
    "bills.create": SafetyTier.TIER_1_LIMITED,
    "bills.update": SafetyTier.TIER_1_LIMITED,
    "bills.list": SafetyTier.TIER_0_SAFE,  # Read-only
    "calendar.create_event": SafetyTier.TIER_1_LIMITED,
    "calendar.update_event": SafetyTier.TIER_1_LIMITED,
    "calendar.list_events": SafetyTier.TIER_0_SAFE,  # Read-only
    
    # Tier 2 - Sensitive actions
    "life_os.update_task_status": SafetyTier.TIER_2_SENSITIVE,
    "calendar.create_event": SafetyTier.TIER_2_SENSITIVE,
    
    # Tier 3 - Financial/Legal (requires approval)
    "bills.mark_paid": SafetyTier.TIER_3_FINANCIAL,
    "tax.categorize_transaction": SafetyTier.TIER_3_FINANCIAL,
    "financial.transfer": SafetyTier.TIER_3_FINANCIAL,
    
    # Tier 4 - System/Critical (requires signature)
    "infra.deploy": SafetyTier.TIER_4_CRITICAL,
    "schema.migrate": SafetyTier.TIER_4_CRITICAL,
    "config.update": SafetyTier.TIER_4_CRITICAL,
}


def get_task_tier(task_type: str) -> SafetyTier:
    """
    Get the safety tier for a task type.
    
    Returns TIER_2_SENSITIVE as default for unknown types (fail-safe).
    """
    # Check exact match first
    if task_type in TASK_TIER_REGISTRY:
        return TASK_TIER_REGISTRY[task_type]
    
    # Check prefix matches (e.g., "life_os.*" -> TIER_1)
    for registered_type, tier in TASK_TIER_REGISTRY.items():
        if task_type.startswith(registered_type.split('.')[0] + '.'):
            return tier
    
    # Default to TIER_2 for unknown types (fail-safe)
    return SafetyTier.TIER_2_SENSITIVE


def requires_approval(task_type: str) -> bool:
    """Check if a task type requires approval before execution"""
    tier = get_task_tier(task_type)
    return tier >= SafetyTier.TIER_3_FINANCIAL


def requires_signature(task_type: str) -> bool:
    """Check if a task type requires explicit signature"""
    tier = get_task_tier(task_type)
    return tier >= SafetyTier.TIER_4_CRITICAL


def is_test_artifact(description: str, payload: Optional[Dict[str, Any]] = None) -> bool:
    """
    Check if a task/run is a test artifact.
    
    Test artifacts are identified by:
    - Description contains [OTTO_SELF_TEST] or [TEST]
    - Payload contains meta.source = "test" or "otto_self_test"
    """
    if description and ("[OTTO_SELF_TEST]" in description or "[TEST]" in description):
        return True
    
    if payload:
        meta = payload.get("meta", {})
        source = meta.get("source", "")
        if source in ["test", "otto_self_test", "test_script", "manual_test"]:
            return True
    
    return False


def should_auto_hide(description: str, payload: Optional[Dict[str, Any]] = None) -> bool:
    """Check if a task/run should be auto-hidden from production UI"""
    return is_test_artifact(description, payload)


# Rate limits (configurable via env vars)
import os

MAX_ACTIONS_PER_RUN = int(os.getenv("OTTO_MAX_ACTIONS_PER_RUN", "10"))
MAX_RUNS_PER_HOUR = int(os.getenv("OTTO_MAX_RUNS_PER_HOUR", "100"))
MAX_TASKS_PER_MINUTE = int(os.getenv("OTTO_MAX_TASKS_PER_MINUTE", "5"))

# Kill switch
OTTO_ENABLED = os.getenv("OTTO_ENABLED", "true").lower() == "true"

