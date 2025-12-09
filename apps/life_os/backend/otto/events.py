"""
Otto Event System - Event emission and processing
Phase 2.5 — CONTROL_OTTO_PHASE2_5_FOUNDATIONS.md
"""

from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from models import OttoEvent


def emit_event(
    db: Session,
    household_id: int,
    event_type: str,
    source_model: str,
    source_id: int,
    payload: Optional[Dict[str, Any]] = None
) -> OttoEvent:
    """
    Emit an OttoEvent after a domain model change.
    
    Args:
        db: Database session
        household_id: Household ID
        event_type: Event type (e.g., "bill.created", "transaction.created")
        source_model: Source model name (e.g., "Bill", "Transaction")
        source_id: ID of the source record
        payload: Optional payload data
    
    Returns:
        Created OttoEvent
    """
    event = OttoEvent(
        household_id=household_id,
        type=event_type,
        source_model=source_model,
        source_id=source_id,
        payload=payload or {},
        status="pending"
    )
    
    db.add(event)
    db.flush()  # Don't commit here - let caller commit
    
    return event


def process_event(db: Session, event: OttoEvent) -> None:
    """
    Process an event by creating appropriate OttoTasks.
    
    For Phase 2.5, this is a simple mapping:
    - bill.created → create reminder/scheduling tasks
    - transaction.created → create categorization task
    - income.created → create categorization task
    - task.created → (no action for now)
    - calendar.created → (no action for now)
    """
    from models import OttoTask
    
    event.status = "processing"
    db.flush()
    
    try:
        # Map event types to OttoTask creation
        if event.type == "bill.created":
            # Create bill reminder task
            otto_task = OttoTask(
                household_id=event.household_id,
                type="bill_reminder",
                description=f"Process bill reminder for bill #{event.source_id}",
                payload={"bill_id": event.source_id},
                status="pending"
            )
            db.add(otto_task)
        
        elif event.type == "transaction.created":
            # Create transaction categorization task
            otto_task = OttoTask(
                household_id=event.household_id,
                type="tax.categorize_transaction",
                description=f"Categorize transaction #{event.source_id}",
                payload={"transaction_id": event.source_id},
                status="pending"
            )
            db.add(otto_task)
        
        elif event.type == "income.created":
            # Create income categorization task (if needed)
            # For now, just log
            pass
        
        # Mark event as done
        event.status = "done"
        event.processed_at = datetime.utcnow()
        db.commit()
    
    except Exception as e:
        event.status = "error"
        event.error = str(e)
        db.commit()
        raise

