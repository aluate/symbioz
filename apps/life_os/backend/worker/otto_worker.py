"""
Otto Worker - Processes OttoTask records and executes them via Otto
"""

import asyncio
import os
import httpx
import json
import logging
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

logger = logging.getLogger(__name__)

from database import SessionLocal, init_db
from models import OttoTask, OttoRun
from otto.actions import execute_actions
from otto.safety import (
    get_task_tier, requires_approval, is_test_artifact,
    MAX_ACTIONS_PER_RUN, OTTO_ENABLED
)


# Otto API configuration
OTTO_API_URL = os.getenv("OTTO_API_URL", "http://localhost:8001")

# Worker configuration
POLL_INTERVAL = int(os.getenv("OTTO_WORKER_POLL_INTERVAL", "30"))  # seconds


async def call_otto_for_task(task: OttoTask) -> dict:
    """
    Call Otto API with a structured task payload.
    
    This function is separate so it can be reused and tested independently.
    """
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            # Use /task endpoint for structured tasks
            response = await client.post(
                f"{OTTO_API_URL}/task",
                json={
                    "type": task.type,
                    "payload": task.payload or {},
                    "source": "life_os_worker",
                    "task_id": task.id,
                    "description": task.description
                }
            )
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        raise Exception(f"Could not connect to Otto API: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise Exception(f"Otto API error: {e.response.status_code} - {e.response.text}")


def process_task(db: Session, task: OttoTask) -> None:
    """
    Process a single OttoTask:
    1. Check safety tier and approval requirements
    2. Lock it (set status to "running")
    3. Create OttoRun record
    4. Call Otto API
    5. Execute returned actions (with rate limiting)
    6. Update task and run records
    """
    # Check kill switch
    if not OTTO_ENABLED:
        logger.warning("Otto is disabled via OTTO_ENABLED=false")
        return
    
    # Check if task requires approval
    if requires_approval(task.type) and task.status != "approved":
        task.status = "pending_approval"
        task.last_error = f"Task type '{task.type}' requires approval (Tier {get_task_tier(task.type).value})"
        db.commit()
        logger.info(f"Task #{task.id} requires approval - set to pending_approval")
        return
    
    # Check retry limit
    if task.retries >= task.max_retries:
        task.status = "blocked"
        task.last_error = f"Max retries ({task.max_retries}) exceeded"
        db.commit()
        logger.warning(f"Task #{task.id} blocked - max retries exceeded")
        return
    
    # Lock the task by setting status to "running" and committing
    task.status = "running"
    task.last_run_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    
    # Create OttoRun record
    run = OttoRun(
        status="pending",
        source="worker",
        input_text=f"Task #{task.id}: {task.description}",
        input_payload={
            "task_id": task.id,
            "task_type": task.type,
            "task_payload": task.payload
        }
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    
    try:
        # Update run status to running
        run.status = "running"
        db.commit()
        
        # Call Otto API (using asyncio.run since we're in a sync context)
        try:
            otto_response = asyncio.run(call_otto_for_task(task))
        except Exception as e:
            # If async call fails, wrap it
            raise Exception(f"Error calling Otto: {str(e)}")
        
        # Extract response - support both old format (actions in result) and new format (actions at top level)
        message = otto_response.get("message", "")
        actions = otto_response.get("actions", [])
        result_data = otto_response.get("result", {})
        reasoning = otto_response.get("reasoning")  # Phase 2.5
        evidence = otto_response.get("evidence")  # Phase 2.5
        
        # If actions are in result.data, extract them
        if not actions and result_data and isinstance(result_data, dict):
            actions = result_data.get("actions", [])
        
        # Execute actions if any (with rate limiting)
        execution_result = None
        if actions:
            # Enforce rate limit
            if len(actions) > MAX_ACTIONS_PER_RUN:
                logger.warning(f"Task #{task.id} has {len(actions)} actions, limiting to {MAX_ACTIONS_PER_RUN}")
                actions = actions[:MAX_ACTIONS_PER_RUN]
                run.logs = json.dumps({
                    "warning": f"Actions limited to {MAX_ACTIONS_PER_RUN}",
                    "original_count": len(actions)
                }, indent=2)
            
            execution_result = execute_actions(
                db,
                actions,
                context={"task_id": task.id, "run_id": run.id}
            )
        
        # Update run with results
        run.output_text = message
        run.output_payload = {
            "otto_response": otto_response,
            "actions_executed": execution_result.summary if execution_result else None,
            "action_results": [
                {
                    "type": r.action_type,
                    "success": r.success,
                    "message": r.message
                }
                for r in (execution_result.results if execution_result else [])
            ]
        }
        # Phase 2.5: Populate reasoning and evidence
        if reasoning:
            run.reasoning = reasoning
        if evidence:
            run.evidence = evidence
        run.logs = json.dumps({
            "otto_response": otto_response,
            "execution_result": {
                "summary": execution_result.summary if execution_result else None,
                "total": execution_result.total if execution_result else 0,
                "succeeded": execution_result.succeeded if execution_result else 0,
                "failed": execution_result.failed if execution_result else 0
            } if execution_result else None
        }, indent=2)
        
        # Determine final status
        if execution_result and execution_result.failed > 0:
            run.status = "error"
            task.status = "error"
            task.last_error = f"Some actions failed: {execution_result.summary}"
        else:
            run.status = "success"
            task.status = "success"
            task.last_error = None
        
        db.commit()
        
    except Exception as e:
        # Mark both task and run as error
        error_msg = str(e)
        run.status = "error"
        run.logs = json.dumps({"error": error_msg}, indent=2)
        run.output_text = f"Error: {error_msg}"
        
        # Increment retry count and set backoff
        task.retries += 1
        task.last_error = error_msg
        
        if task.retries < task.max_retries:
            # Calculate backoff delay
            if task.retries == 1:
                delay_minutes = 1
            elif task.retries == 2:
                delay_minutes = 5
            else:
                delay_minutes = 15
            
            from datetime import timedelta
            task.next_run_at = datetime.utcnow() + timedelta(minutes=delay_minutes)
            task.status = "pending"  # Will retry later
            logger.info(f"Task #{task.id} will retry in {delay_minutes} minutes (attempt {task.retries}/{task.max_retries})")
        else:
            task.status = "blocked"
            logger.warning(f"Task #{task.id} blocked after {task.retries} retries")
        
        db.commit()


def find_ready_tasks(db: Session) -> list:
    """
    Find tasks that are ready to run:
    - status = "pending" or "approved"
    - next_run_at is None or <= now
    - retries < max_retries (if failed before)
    - Not a test artifact (unless in dev mode)
    """
    import os
    otto_mode = os.getenv("OTTO_MODE", "dev").lower()
    
    now = datetime.utcnow()
    query = db.query(OttoTask).filter(
        and_(
            OttoTask.status.in_(["pending", "approved"]),
            (OttoTask.next_run_at.is_(None)) | (OttoTask.next_run_at <= now),
            OttoTask.retries < OttoTask.max_retries
        )
    )
    
    # In production mode, exclude test artifacts
    if otto_mode == "prod":
        # Filter out test tasks by checking description
        tasks = query.all()
        return [
            t for t in tasks
            if not is_test_artifact(t.description, t.payload)
        ]
    
    return query.all()


def run_worker_cycle(db: Session) -> int:
    """
    Run one cycle of the worker:
    1. Find ready tasks
    2. Process each one
    
    Returns number of tasks processed.
    """
    ready_tasks = find_ready_tasks(db)
    
    for task in ready_tasks:
        try:
            process_task(db, task)
        except Exception as e:
            # Log error but continue with other tasks
            print(f"Error processing task #{task.id}: {str(e)}")
            # Mark task as error
            task.status = "error"
            task.last_error = str(e)
            db.commit()
    
    return len(ready_tasks)


def run_worker_forever():
    """
    Main worker loop - runs forever, polling for tasks.
    """
    print("Starting Otto Worker...")
    print(f"Otto API URL: {OTTO_API_URL}")
    print(f"Poll interval: {POLL_INTERVAL} seconds")
    print(f"Otto Enabled: {OTTO_ENABLED}")
    print(f"Max actions per run: {MAX_ACTIONS_PER_RUN}")
    print("Press Ctrl+C to stop")
    print()
    
    # Check kill switch
    if not OTTO_ENABLED:
        print("⚠️  Otto is DISABLED via OTTO_ENABLED=false")
        print("   Set OTTO_ENABLED=true to enable processing")
        return
    
    # Initialize database
    init_db()
    
    while True:
        # Re-check kill switch each cycle
        if not OTTO_ENABLED:
            print("Otto disabled - pausing worker")
            import time
            time.sleep(POLL_INTERVAL)
            continue
        try:
            db = SessionLocal()
            try:
                processed = run_worker_cycle(db)
                if processed > 0:
                    print(f"[{datetime.now().isoformat()}] Processed {processed} task(s)")
            finally:
                db.close()
            
            # Sleep before next cycle
            import time
            time.sleep(POLL_INTERVAL)
            
        except KeyboardInterrupt:
            print("\nStopping worker...")
            break
        except Exception as e:
            print(f"Error in worker cycle: {str(e)}")
            # Continue running even if there's an error
            import time
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    run_worker_forever()

