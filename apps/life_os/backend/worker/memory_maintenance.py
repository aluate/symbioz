"""
Memory Maintenance Worker - Handles expiration and stale marking
Phase 4 — CONTROL_OTTO_PHASE4_MEMORY_UI_AND_MAINTENANCE.md
"""

import logging
from datetime import datetime
from sqlalchemy.orm import Session
from typing import List

from models import OttoMemory, OttoRun
from otto.context import get_default_context

logger = logging.getLogger(__name__)


def mark_expired_memories_stale(db: Session) -> int:
    """
    Scan for expired memories and mark them as stale.
    
    Non-destructive: Only sets is_stale=True and stale_reason="expired".
    
    Returns:
        Number of memories marked as stale
    """
    try:
        otto_context = get_default_context(db)
        now = datetime.utcnow()
        
        # Find memories that are expired but not yet marked stale
        expired_memories = db.query(OttoMemory).filter(
            OttoMemory.household_id == otto_context.household_id,
            OttoMemory.expires_at < now,
            OttoMemory.is_stale == False
        ).all()
        
        count = 0
        for memory in expired_memories:
            memory.is_stale = True
            memory.stale_reason = "expired"
            memory.updated_at = now
            count += 1
        
        if count > 0:
            db.commit()
            logger.info(f"Marked {count} expired memory(ies) as stale")
        
        # Create OttoRun record for audit trail
        if count > 0:
            run = OttoRun(
                household_id=otto_context.household_id,
                status="success",
                source="memory_maintenance",
                input_text=f"Memory maintenance: marked {count} expired memory(ies) as stale",
                input_payload={
                    "operation": "mark_expired_stale",
                    "count": count
                },
                output_text=f"Marked {count} expired memory(ies) as stale",
                output_payload={
                    "memories_marked": count,
                    "timestamp": now.isoformat()
                },
                reasoning={
                    "steps": [{
                        "id": "step1",
                        "type": "maintenance",
                        "summary": f"Scanned for expired memories (expires_at < {now.isoformat()})",
                        "evidence": [{"kind": "maintenance_scan", "timestamp": now.isoformat()}]
                    }, {
                        "id": "step2",
                        "type": "action",
                        "summary": f"Marked {count} memory(ies) as stale with reason 'expired'",
                        "evidence": [{"kind": "memories_updated", "count": count}]
                    }]
                },
                evidence={
                    "memories_marked": count,
                    "operation": "mark_expired_stale"
                }
            )
            db.add(run)
            db.commit()
        
        return count
    except Exception as e:
        logger.error(f"Error in memory maintenance: {str(e)}")
        db.rollback()
        raise


def run_memory_maintenance(db: Session) -> dict:
    """
    Run all memory maintenance tasks.
    
    Returns:
        Summary dict with counts of actions taken
    """
    summary = {
        "expired_marked_stale": 0,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    try:
        summary["expired_marked_stale"] = mark_expired_memories_stale(db)
    except Exception as e:
        logger.error(f"Memory maintenance failed: {str(e)}")
        summary["error"] = str(e)
    
    return summary

