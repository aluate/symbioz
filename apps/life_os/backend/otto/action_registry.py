"""
Action Schema Registry - Single source of truth for all Otto actions
Phase 2.5 — CONTROL_OTTO_PHASE2_5_FOUNDATIONS.md
"""

from typing import Callable, Dict, Any, Optional
from pydantic import BaseModel
from dataclasses import dataclass

from otto.actions import (
    _handle_life_os_create_task,
    _handle_life_os_update_task_status,
    _handle_life_os_list_tasks,
    _handle_bills_create,
    _handle_bills_update,
    _handle_bills_mark_paid,
    _handle_bills_list,
    _handle_calendar_create_event,
    _handle_calendar_update_event,
    _handle_calendar_list_events,
    _handle_income_create_income,
    _handle_income_update_income,
    _handle_transactions_create_transaction,
    _handle_transactions_update_transaction,
    _handle_transactions_categorize_transaction,
    _handle_tax_propose_category,
    _handle_memory_create,
    _handle_memory_update,
    _handle_memory_delete,
    _handle_memory_mark_stale,
    _handle_memory_set_expiration,
    _handle_memory_link,
    _handle_otto_log,
)


@dataclass
class ActionSchema:
    """Schema for an action type"""
    type: str
    description: str
    safety_tier: int  # 0-3, as defined in META_RULES
    handler: Callable[[Any, Dict[str, Any], Dict[str, Any]], Any]
    payload_model: Optional[type[BaseModel]] = None
    allow_in_worker: bool = True


# Registry of all action types
ACTION_REGISTRY: Dict[str, ActionSchema] = {
    "otto.log": ActionSchema(
        type="otto.log",
        description="Log a message (no-op for debugging)",
        safety_tier=0,
        handler=_handle_otto_log,
        allow_in_worker=True,
    ),
    
    "life_os.create_task": ActionSchema(
        type="life_os.create_task",
        description="Create a Life OS task",
        safety_tier=1,
        handler=_handle_life_os_create_task,
        allow_in_worker=True,
    ),
    
    "life_os.update_task_status": ActionSchema(
        type="life_os.update_task_status",
        description="Update Life OS task status and fields",
        safety_tier=1,
        handler=_handle_life_os_update_task_status,
        allow_in_worker=True,
    ),
    
    "life_os.list_tasks": ActionSchema(
        type="life_os.list_tasks",
        description="List Life OS tasks with optional filters",
        safety_tier=0,  # Read-only
        handler=_handle_life_os_list_tasks,
        allow_in_worker=True,
    ),
    
    "bills.create": ActionSchema(
        type="bills.create",
        description="Create a bill",
        safety_tier=2,  # Financial state
        handler=_handle_bills_create,
        allow_in_worker=True,
    ),
    
    "bills.update": ActionSchema(
        type="bills.update",
        description="Update a bill",
        safety_tier=2,  # Financial state
        handler=_handle_bills_update,
        allow_in_worker=True,
    ),
    
    "bills.mark_paid": ActionSchema(
        type="bills.mark_paid",
        description="Mark a bill as paid",
        safety_tier=2,  # Financial state
        handler=_handle_bills_mark_paid,
        allow_in_worker=True,
    ),
    
    "bills.list": ActionSchema(
        type="bills.list",
        description="List bills with optional filters",
        safety_tier=0,  # Read-only
        handler=_handle_bills_list,
        allow_in_worker=True,
    ),
    
    "calendar.create_event": ActionSchema(
        type="calendar.create_event",
        description="Create a calendar event",
        safety_tier=2,  # Schedule commitments
        handler=_handle_calendar_create_event,
        allow_in_worker=True,
    ),
    
    "calendar.update_event": ActionSchema(
        type="calendar.update_event",
        description="Update a calendar event",
        safety_tier=2,  # Schedule commitments
        handler=_handle_calendar_update_event,
        allow_in_worker=True,
    ),
    
    "calendar.list_events": ActionSchema(
        type="calendar.list_events",
        description="List calendar events with optional filters",
        safety_tier=0,  # Read-only
        handler=_handle_calendar_list_events,
        allow_in_worker=True,
    ),
    
    "income.create_income": ActionSchema(
        type="income.create_income",
        description="Create an income entry",
        safety_tier=2,  # Financial state
        handler=_handle_income_create_income,
        allow_in_worker=True,
    ),
    
    "income.update_income": ActionSchema(
        type="income.update_income",
        description="Update an income entry",
        safety_tier=2,  # Financial state
        handler=_handle_income_update_income,
        allow_in_worker=True,
    ),
    
    "transactions.create_transaction": ActionSchema(
        type="transactions.create_transaction",
        description="Create a transaction",
        safety_tier=2,  # Tax-critical
        handler=_handle_transactions_create_transaction,
        allow_in_worker=True,
    ),
    
    "transactions.update_transaction": ActionSchema(
        type="transactions.update_transaction",
        description="Update a transaction",
        safety_tier=2,  # Tax-critical
        handler=_handle_transactions_update_transaction,
        allow_in_worker=True,
    ),
    
    "transactions.categorize_transaction": ActionSchema(
        type="transactions.categorize_transaction",
        description="Categorize a transaction for tax/reporting",
        safety_tier=2,  # Tax-critical
        handler=_handle_transactions_categorize_transaction,
        allow_in_worker=True,
    ),
    
    "tax.propose_category": ActionSchema(
        type="tax.propose_category",
        description="Propose a new tax/expense category for approval",
        safety_tier=2,  # Financial state
        handler=_handle_tax_propose_category,
        allow_in_worker=True,
    ),
    
    "memory.create": ActionSchema(
        type="memory.create",
        description="Create a new memory entry",
        safety_tier=2,  # Requires approval if source is "otto_inference"
        handler=_handle_memory_create,
        allow_in_worker=True,
    ),
    
    "memory.update": ActionSchema(
        type="memory.update",
        description="Update an existing memory entry",
        safety_tier=2,  # Requires approval
        handler=_handle_memory_update,
        allow_in_worker=True,
    ),
    
    "memory.delete": ActionSchema(
        type="memory.delete",
        description="Delete a memory entry",
        safety_tier=2,  # Requires approval
        handler=_handle_memory_delete,
        allow_in_worker=True,
    ),
    
    "memory.mark_stale": ActionSchema(
        type="memory.mark_stale",
        description="Mark a memory as stale (non-destructive)",
        safety_tier=1,  # Non-destructive
        handler=_handle_memory_mark_stale,
        allow_in_worker=True,
    ),
    
    "memory.set_expiration": ActionSchema(
        type="memory.set_expiration",
        description="Set expiration date for a memory",
        safety_tier=1,  # Non-destructive
        handler=_handle_memory_set_expiration,
        allow_in_worker=True,
    ),
    
    "memory.link": ActionSchema(
        type="memory.link",
        description="Create a link from a memory to another memory or domain object",
        safety_tier=1,  # Non-destructive, just creates relationships
        handler=_handle_memory_link,
        allow_in_worker=True,
    ),
}


def get_action_schema(action_type: str) -> Optional[ActionSchema]:
    """Get action schema by type, or None if not found"""
    return ACTION_REGISTRY.get(action_type)


def validate_action(action: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    Validate an action against the registry.
    
    Returns:
        (is_valid, error_message)
    """
    action_type = action.get("type")
    if not action_type:
        return False, "Action missing 'type' field"
    
    schema = get_action_schema(action_type)
    if not schema:
        return False, f"Unknown action type: {action_type}"
    
    # Check for tier
    tier = action.get("tier")
    if tier is None:
        return False, f"Action missing 'tier' field (required for {action_type})"
    
    if tier != schema.safety_tier:
        return False, f"Action tier {tier} does not match schema tier {schema.safety_tier} for {action_type}"
    
    # TODO: Validate payload against payload_model if provided
    # For now, just check that payload exists
    if "payload" not in action:
        return False, f"Action missing 'payload' field"
    
    return True, None

