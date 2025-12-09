"""
Otto Event Worker - Processes pending events
Phase 2.5 — CONTROL_OTTO_PHASE2_5_FOUNDATIONS.md
"""

import time
from sqlalchemy.orm import Session
from datetime import datetime

from models import OttoEvent
from otto.events import process_event
from database import SessionLocal


def run_event_worker(interval_seconds: int = 5, max_iterations: Optional[int] = None):
    """
    Run the event worker loop.
    
    Fetches pending events and processes them.
    
    Args:
        interval_seconds: Seconds to wait between checks
        max_iterations: Maximum iterations (None = run forever)
    """
    iteration = 0
    
    while max_iterations is None or iteration < max_iterations:
        db: Session = SessionLocal()
        try:
            # Fetch pending events
            pending_events = db.query(OttoEvent).filter(
                OttoEvent.status == "pending"
            ).limit(10).all()
            
            for event in pending_events:
                try:
                    process_event(db, event)
                except Exception as e:
                    print(f"Error processing event {event.id}: {e}")
                    # Event status already set to "error" in process_event
                    db.rollback()
                    continue
            
            db.commit()
        
        except Exception as e:
            print(f"Error in event worker: {e}")
            db.rollback()
        
        finally:
            db.close()
        
        if pending_events:
            # If we processed events, check again immediately
            time.sleep(1)
        else:
            # No events, wait longer
            time.sleep(interval_seconds)
        
        iteration += 1


if __name__ == "__main__":
    # Run worker
    print("Starting Otto Event Worker...")
    run_event_worker()

