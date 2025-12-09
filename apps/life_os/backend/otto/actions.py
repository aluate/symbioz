"""
Action Executor - Safely executes structured actions returned by Otto
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from sqlalchemy.orm import Session
import json
from datetime import datetime
from enum import IntEnum

from models import OttoTask, LifeOSTask, Bill, CalendarEvent, Income, Transaction
from otto.context import OttoContext, get_default_context
from otto.action_registry import ACTION_REGISTRY, validate_action, get_action_schema


class ActionSeverity(IntEnum):
    """Severity levels for action execution"""
    LOW = 1  # Failure doesn't affect other actions
    MEDIUM = 2  # Failure logged, execution continues
    HIGH = 3  # Failure halts execution
    CRITICAL = 4  # Failure is catastrophic, rollback if possible


# Registry of action severities
ACTION_SEVERITY_REGISTRY: Dict[str, ActionSeverity] = {
    "otto.log": ActionSeverity.LOW,
    "life_os.create_task": ActionSeverity.MEDIUM,
    "life_os.update_task_status": ActionSeverity.MEDIUM,
    "life_os.list_tasks": ActionSeverity.LOW,  # Read-only
    "life_os.log_note": ActionSeverity.LOW,
    "bills.create": ActionSeverity.MEDIUM,  # Tier 2 - financial state
    "bills.update": ActionSeverity.MEDIUM,  # Tier 2 - financial state
    "bills.mark_paid": ActionSeverity.MEDIUM,  # Tier 2 - financial state
    "bills.list": ActionSeverity.LOW,  # Read-only
    "calendar.create_event": ActionSeverity.MEDIUM,  # Tier 2 - schedule commitments
    "calendar.update_event": ActionSeverity.MEDIUM,  # Tier 2 - schedule commitments
    "calendar.list_events": ActionSeverity.LOW,  # Read-only
    "income.create_income": ActionSeverity.MEDIUM,  # Tier 2 - financial state
    "income.update_income": ActionSeverity.MEDIUM,  # Tier 2 - financial state
    "transactions.create_transaction": ActionSeverity.MEDIUM,  # Tier 2 - tax-critical
    "transactions.update_transaction": ActionSeverity.MEDIUM,  # Tier 2 - tax-critical
    "transactions.categorize_transaction": ActionSeverity.MEDIUM,  # Tier 2 - tax-critical
    "schema.migrate": ActionSeverity.HIGH,
    "config.update": ActionSeverity.HIGH,
    "financial.transfer": ActionSeverity.CRITICAL,
    "legal.sign_document": ActionSeverity.CRITICAL,
}


def get_action_severity(action_type: str) -> ActionSeverity:
    """Get severity for an action type, default to MEDIUM"""
    return ACTION_SEVERITY_REGISTRY.get(action_type, ActionSeverity.MEDIUM)


@dataclass
class ActionResult:
    """Result of executing a single action"""
    action_type: str
    success: bool
    message: str
    error: Optional[str] = None


@dataclass
class ExecutionResult:
    """Result of executing a batch of actions"""
    summary: str
    total: int
    succeeded: int
    failed: int
    results: List[ActionResult]


def execute_actions(
    db: Session, 
    actions: List[Dict[str, Any]], 
    otto_context: Optional[OttoContext] = None,
    context: Optional[Dict[str, Any]] = None
) -> ExecutionResult:
    """
    Execute a list of actions returned by Otto.
    
    Respects action severity - HIGH/CRITICAL failures halt execution.
    
    Args:
        db: Database session
        actions: List of action dicts with 'type' and 'payload'
        otto_context: OttoContext with household/user info (required)
        context: Optional context dict (e.g., task_id, run_id)
    
    Returns:
        ExecutionResult with summary and per-action results
    """
    # Get default context if not provided
    if otto_context is None:
        otto_context = get_default_context(db)
    
    if context is None:
        context = {}
    
    # Add otto_context to context dict for handlers
    context["otto_context"] = otto_context
    
    results = []
    succeeded = 0
    failed = 0
    halted = False
    
    for action in actions:
        action_type = action.get("type")
        payload = action.get("payload", {})
        
        # Validate action against registry
        is_valid, error_msg = validate_action(action)
        if not is_valid:
            results.append(ActionResult(
                action_type=action_type or "unknown",
                success=False,
                message=error_msg or "Action validation failed",
                error=error_msg or "Action validation failed"
            ))
            failed += 1
            continue
        
        # Get schema from registry
        schema = get_action_schema(action_type)
        if not schema:
            # Should not happen if validate_action passed, but double-check
            results.append(ActionResult(
                action_type=action_type,
                success=False,
                message=f"Action schema not found for: {action_type}",
                error=f"Action schema not found"
            ))
            failed += 1
            continue
        
        try:
            # Dispatch to handler from registry
            result = schema.handler(db, payload, context)
            
            results.append(result)
            if result.success:
                succeeded += 1
            else:
                failed += 1
                # Check severity - HIGH/CRITICAL failures halt execution
                severity = get_action_severity(action_type)
                if severity >= ActionSeverity.HIGH:
                    halted = True
                    results.append(ActionResult(
                        action_type="execution_halted",
                        success=False,
                        message=f"Execution halted due to {action_type} failure (severity: {severity.name})",
                        error=f"High-severity action failed, remaining actions skipped"
                    ))
                    break
                
        except Exception as e:
            # Catch any exceptions and mark as failed
            severity = get_action_severity(action_type)
            result = ActionResult(
                action_type=action_type,
                success=False,
                message=f"Error executing action: {str(e)}",
                error=str(e)
            )
            results.append(result)
            failed += 1
            
            # HIGH/CRITICAL exceptions halt execution
            if severity >= ActionSeverity.HIGH:
                halted = True
                results.append(ActionResult(
                    action_type="execution_halted",
                    success=False,
                    message=f"Execution halted due to exception in {action_type} (severity: {severity.name})",
                    error=f"Exception in high-severity action: {str(e)}"
                ))
                break
    
    total = len(actions)
    if halted:
        summary = f"{succeeded} succeeded, {failed} failed, execution halted"
    else:
        summary = f"{succeeded} actions succeeded, {failed} failed"
    
    return ExecutionResult(
        summary=summary,
        total=total,
        succeeded=succeeded,
        failed=failed,
        results=results
    )


def _handle_life_os_create_task(db: Session, payload: Dict[str, Any], context: Dict[str, Any]) -> ActionResult:
    """
    Handle life_os.create_task action.
    
    Creates a new LifeOSTask in the database.
    
    Payload should contain:
    - title: str (required)
    - description: str (optional)
    - assignee: str (optional)
    - due_date: datetime (optional)
    - priority: str (optional: low, medium, high)
    - category: str (optional)
    """
    try:
        title = payload.get("title")
        
        if not title:
            return ActionResult(
                action_type="life_os.create_task",
                success=False,
                message="Missing required field: 'title'",
                error="Missing required field: 'title'"
            )
        
        # Get OttoContext from context
        otto_context: OttoContext = context.get("otto_context")
        if not otto_context:
            return ActionResult(
                action_type="life_os.create_task",
                success=False,
                message="Missing OttoContext",
                error="OttoContext required"
            )
        
        task = LifeOSTask(
            household_id=otto_context.household_id,
            user_id=otto_context.user_id,
            title=title,
            description=payload.get("description"),
            assignee=payload.get("assignee"),
            due_date=payload.get("due_date"),
            priority=payload.get("priority"),
            category=payload.get("category"),
            status="todo"
        )
        
        db.add(task)
        db.commit()
        db.refresh(task)
        
        return ActionResult(
            action_type="life_os.create_task",
            success=True,
            message=f"Created Life OS task #{task.id}: {title}"
        )
    except Exception as e:
        db.rollback()
        return ActionResult(
            action_type="life_os.create_task",
            success=False,
            message=f"Failed to create task: {str(e)}",
            error=str(e)
        )


def _handle_life_os_update_task_status(db: Session, payload: Dict[str, Any], context: Dict[str, Any]) -> ActionResult:
    """
    Handle life_os.update_task_status action.
    
    Updates the status of an existing LifeOSTask.
    
    Payload should contain:
    - task_id: int
    - status: str (todo, in_progress, done, blocked)
    - Other fields can also be updated: title, description, assignee, due_date, priority, category
    """
    try:
        task_id = payload.get("task_id")
        new_status = payload.get("status")
        
        if not task_id:
            return ActionResult(
                action_type="life_os.update_task_status",
                success=False,
                message="Missing required field: 'task_id'",
                error="Missing required field: 'task_id'"
            )
        
        task = db.query(LifeOSTask).filter(LifeOSTask.id == task_id).first()
        if not task:
            return ActionResult(
                action_type="life_os.update_task_status",
                success=False,
                message=f"Life OS task #{task_id} not found",
                error=f"Life OS task #{task_id} not found"
            )
        
        # Update status if provided
        if new_status:
            task.status = new_status
            if new_status == "done" and task.completed_at is None:
                task.completed_at = datetime.utcnow()
            elif new_status != "done":
                task.completed_at = None
        
        # Update other fields if provided
        if payload.get("title") is not None:
            task.title = payload.get("title")
        if payload.get("description") is not None:
            task.description = payload.get("description")
        if payload.get("assignee") is not None:
            task.assignee = payload.get("assignee")
        if payload.get("due_date") is not None:
            task.due_date = payload.get("due_date")
        if payload.get("priority") is not None:
            task.priority = payload.get("priority")
        if payload.get("category") is not None:
            task.category = payload.get("category")
        
        db.commit()
        
        status_msg = f" to status: {new_status}" if new_status else ""
        return ActionResult(
            action_type="life_os.update_task_status",
            success=True,
            message=f"Updated Life OS task #{task_id}{status_msg}"
        )
    except Exception as e:
        db.rollback()
        return ActionResult(
            action_type="life_os.update_task_status",
            success=False,
            message=f"Failed to update task status: {str(e)}",
            error=str(e)
        )


def _handle_life_os_list_tasks(db: Session, payload: Dict[str, Any], context: Dict[str, Any]) -> ActionResult:
    """
    Handle life_os.list_tasks action.
    
    Lists Life OS tasks with optional filters.
    
    Payload can contain:
    - status: str (optional filter)
    - assignee: str (optional filter)
    - category: str (optional filter)
    - limit: int (optional, default 20)
    """
    try:
        query = db.query(LifeOSTask)
        
        if payload.get("status"):
            query = query.filter(LifeOSTask.status == payload.get("status"))
        if payload.get("assignee"):
            query = query.filter(LifeOSTask.assignee == payload.get("assignee"))
        if payload.get("category"):
            query = query.filter(LifeOSTask.category == payload.get("category"))
        
        limit = payload.get("limit", 20)
        tasks = query.order_by(LifeOSTask.due_date.asc().nulls_last(), LifeOSTask.created_at.desc()).limit(limit).all()
        
        task_list = [
            {
                "id": t.id,
                "title": t.title,
                "status": t.status,
                "assignee": t.assignee,
                "due_date": t.due_date.isoformat() if t.due_date else None,
                "priority": t.priority,
                "category": t.category
            }
            for t in tasks
        ]
        
        return ActionResult(
            action_type="life_os.list_tasks",
            success=True,
            message=f"Found {len(tasks)} task(s)"
        )
    except Exception as e:
        return ActionResult(
            action_type="life_os.list_tasks",
            success=False,
            message=f"Failed to list tasks: {str(e)}",
            error=str(e)
        )


def _handle_calendar_create_event(db: Session, payload: Dict[str, Any], context: Dict[str, Any]) -> ActionResult:
    """
    Handle calendar.create_event action.
    
    Creates a new CalendarEvent in the database.
    
    Payload should contain:
    - title: str (required)
    - start_time: datetime (required)
    - description: str (optional)
    - end_time: datetime (optional)
    - location: str (optional)
    - attendees: str (optional)
    - category: str (optional)
    - is_recurring: str (optional: yes, no)
    - recurrence_frequency: str (optional: daily, weekly, monthly, yearly)
    - reminders: list (optional: [{"minutes": 15}])
    """
    try:
        title = payload.get("title")
        start_time = payload.get("start_time")
        
        if not title or not start_time:
            return ActionResult(
                action_type="calendar.create_event",
                success=False,
                message="Missing required fields: 'title' and 'start_time'",
                error="Missing required fields"
            )
        
        # Parse start_time if it's a string
        if isinstance(start_time, str):
            try:
                start_time = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
            except:
                return ActionResult(
                    action_type="calendar.create_event",
                    success=False,
                    message=f"Invalid start_time format: {start_time}",
                    error="Invalid start_time format"
                )
        
        # Parse end_time if provided
        end_time = payload.get("end_time")
        if end_time and isinstance(end_time, str):
            try:
                end_time = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
            except:
                return ActionResult(
                    action_type="calendar.create_event",
                    success=False,
                    message=f"Invalid end_time format: {end_time}",
                    error="Invalid end_time format"
                )
        
        # Get OttoContext from context
        otto_context: OttoContext = context.get("otto_context")
        if not otto_context:
            return ActionResult(
                action_type="calendar.create_event",
                success=False,
                message="Missing OttoContext",
                error="OttoContext required"
            )
        
        event = CalendarEvent(
            household_id=otto_context.household_id,
            user_id=otto_context.user_id,
            title=title,
            description=payload.get("description"),
            start_time=start_time,
            end_time=end_time,
            location=payload.get("location"),
            attendees=payload.get("attendees"),
            category=payload.get("category"),
            is_recurring=payload.get("is_recurring", "no"),
            recurrence_frequency=payload.get("recurrence_frequency"),
            reminders=payload.get("reminders")
        )
        
        db.add(event)
        db.commit()
        db.refresh(event)
        
        return ActionResult(
            action_type="calendar.create_event",
            success=True,
            message=f"Created calendar event #{event.id}: {title}"
        )
    except Exception as e:
        db.rollback()
        return ActionResult(
            action_type="calendar.create_event",
            success=False,
            message=f"Failed to create event: {str(e)}",
            error=str(e)
        )


def _handle_calendar_update_event(db: Session, payload: Dict[str, Any], context: Dict[str, Any]) -> ActionResult:
    """
    Handle calendar.update_event action.
    
    Updates an existing CalendarEvent.
    
    Payload should contain:
    - event_id: int (required)
    - Other fields can also be updated
    """
    try:
        event_id = payload.get("event_id")
        if not event_id:
            return ActionResult(
                action_type="calendar.update_event",
                success=False,
                message="Missing required field: 'event_id'",
                error="Missing required field: 'event_id'"
            )
        
        event = db.query(CalendarEvent).filter(CalendarEvent.id == event_id).first()
        if not event:
            return ActionResult(
                action_type="calendar.update_event",
                success=False,
                message=f"Calendar event #{event_id} not found",
                error=f"Calendar event #{event_id} not found"
            )
        
        # Update fields
        if payload.get("title") is not None:
            event.title = payload.get("title")
        if payload.get("description") is not None:
            event.description = payload.get("description")
        if payload.get("start_time") is not None:
            start_time = payload.get("start_time")
            if isinstance(start_time, str):
                start_time = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
            event.start_time = start_time
        if payload.get("end_time") is not None:
            end_time = payload.get("end_time")
            if isinstance(end_time, str):
                end_time = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
            event.end_time = end_time
        if payload.get("location") is not None:
            event.location = payload.get("location")
        if payload.get("attendees") is not None:
            event.attendees = payload.get("attendees")
        if payload.get("category") is not None:
            event.category = payload.get("category")
        if payload.get("status") is not None:
            event.status = payload.get("status")
        if payload.get("reminders") is not None:
            event.reminders = payload.get("reminders")
        
        db.commit()
        
        return ActionResult(
            action_type="calendar.update_event",
            success=True,
            message=f"Updated calendar event #{event_id}"
        )
    except Exception as e:
        db.rollback()
        return ActionResult(
            action_type="calendar.update_event",
            success=False,
            message=f"Failed to update event: {str(e)}",
            error=str(e)
        )


def _handle_calendar_list_events(db: Session, payload: Dict[str, Any], context: Dict[str, Any]) -> ActionResult:
    """
    Handle calendar.list_events action.
    
    Lists calendar events with optional filters.
    
    Payload can contain:
    - start_date: datetime (optional)
    - end_date: datetime (optional)
    - category: str (optional)
    - status: str (optional)
    """
    try:
        from datetime import timedelta
        
        query = db.query(CalendarEvent)
        
        if payload.get("start_date"):
            start_date = payload.get("start_date")
            if isinstance(start_date, str):
                start_date = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
            query = query.filter(CalendarEvent.start_time >= start_date)
        if payload.get("end_date"):
            end_date = payload.get("end_date")
            if isinstance(end_date, str):
                end_date = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
            query = query.filter(CalendarEvent.start_time <= end_date)
        if payload.get("category"):
            query = query.filter(CalendarEvent.category == payload.get("category"))
        if payload.get("status"):
            query = query.filter(CalendarEvent.status == payload.get("status"))
        
        limit = payload.get("limit", 20)
        events = query.order_by(CalendarEvent.start_time.asc()).limit(limit).all()
        
        return ActionResult(
            action_type="calendar.list_events",
            success=True,
            message=f"Found {len(events)} event(s)"
        )
    except Exception as e:
        return ActionResult(
            action_type="calendar.list_events",
            success=False,
            message=f"Failed to list events: {str(e)}",
            error=str(e)
        )


def _handle_bills_create(db: Session, payload: Dict[str, Any], context: Dict[str, Any]) -> ActionResult:
    """
    Handle bills.create action.
    
    Creates a new Bill in the database.
    
    Payload should contain:
    - name: str (required)
    - amount: str (required)
    - due_date: datetime (required)
    - category: str (optional)
    - payee: str (optional)
    - account_number: str (optional)
    - notes: str (optional)
    - is_recurring: str (optional: yes, no)
    - recurrence_frequency: str (optional: monthly, quarterly, yearly)
    """
    try:
        name = payload.get("name")
        amount = payload.get("amount")
        due_date = payload.get("due_date")
        
        if not name or not amount or not due_date:
            return ActionResult(
                action_type="bills.create",
                success=False,
                message="Missing required fields: 'name', 'amount', 'due_date'",
                error="Missing required fields"
            )
        
        # Parse due_date if it's a string
        if isinstance(due_date, str):
            try:
                due_date = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
            except:
                return ActionResult(
                    action_type="bills.create",
                    success=False,
                    message=f"Invalid due_date format: {due_date}",
                    error="Invalid due_date format"
                )
        
        # Get OttoContext from context
        otto_context: OttoContext = context.get("otto_context")
        if not otto_context:
            return ActionResult(
                action_type="bills.create",
                success=False,
                message="Missing OttoContext",
                error="OttoContext required"
            )
        
        bill = Bill(
            household_id=otto_context.household_id,
            name=name,
            amount=amount,
            due_date=due_date,
            category=payload.get("category"),
            payee=payload.get("payee"),
            account_number=payload.get("account_number"),
            notes=payload.get("notes"),
            is_recurring=payload.get("is_recurring", "no"),
            recurrence_frequency=payload.get("recurrence_frequency")
        )
        
        # Calculate next_due_date for recurring bills
        if bill.is_recurring == "yes" and bill.recurrence_frequency:
            from datetime import timedelta
            if bill.recurrence_frequency == "monthly":
                bill.next_due_date = due_date + timedelta(days=30)
            elif bill.recurrence_frequency == "quarterly":
                bill.next_due_date = due_date + timedelta(days=90)
            elif bill.recurrence_frequency == "yearly":
                bill.next_due_date = due_date + timedelta(days=365)
        
        db.add(bill)
        db.commit()
        db.refresh(bill)
        
        return ActionResult(
            action_type="bills.create",
            success=True,
            message=f"Created bill #{bill.id}: {name}"
        )
    except Exception as e:
        db.rollback()
        return ActionResult(
            action_type="bills.create",
            success=False,
            message=f"Failed to create bill: {str(e)}",
            error=str(e)
        )


def _handle_bills_update(db: Session, payload: Dict[str, Any], context: Dict[str, Any]) -> ActionResult:
    """
    Handle bills.update action.
    
    Updates an existing Bill.
    
    Payload should contain:
    - bill_id: int (required)
    - Other fields can also be updated
    """
    try:
        bill_id = payload.get("bill_id")
        if not bill_id:
            return ActionResult(
                action_type="bills.update",
                success=False,
                message="Missing required field: 'bill_id'",
                error="Missing required field: 'bill_id'"
            )
        
        bill = db.query(Bill).filter(Bill.id == bill_id).first()
        if not bill:
            return ActionResult(
                action_type="bills.update",
                success=False,
                message=f"Bill #{bill_id} not found",
                error=f"Bill #{bill_id} not found"
            )
        
        # Update fields
        if payload.get("name") is not None:
            bill.name = payload.get("name")
        if payload.get("amount") is not None:
            bill.amount = payload.get("amount")
        if payload.get("due_date") is not None:
            due_date = payload.get("due_date")
            if isinstance(due_date, str):
                due_date = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
            bill.due_date = due_date
        if payload.get("paid") is not None:
            bill.paid = payload.get("paid")
            if payload.get("paid") == "yes" and bill.paid_at is None:
                bill.paid_at = datetime.utcnow()
            elif payload.get("paid") != "yes":
                bill.paid_at = None
        if payload.get("category") is not None:
            bill.category = payload.get("category")
        if payload.get("payee") is not None:
            bill.payee = payload.get("payee")
        if payload.get("account_number") is not None:
            bill.account_number = payload.get("account_number")
        if payload.get("notes") is not None:
            bill.notes = payload.get("notes")
        if payload.get("is_recurring") is not None:
            bill.is_recurring = payload.get("is_recurring")
        if payload.get("recurrence_frequency") is not None:
            bill.recurrence_frequency = payload.get("recurrence_frequency")
        
        db.commit()
        
        return ActionResult(
            action_type="bills.update",
            success=True,
            message=f"Updated bill #{bill_id}"
        )
    except Exception as e:
        db.rollback()
        return ActionResult(
            action_type="bills.update",
            success=False,
            message=f"Failed to update bill: {str(e)}",
            error=str(e)
        )


def _handle_bills_mark_paid(db: Session, payload: Dict[str, Any], context: Dict[str, Any]) -> ActionResult:
    """
    Handle bills.mark_paid action.
    
    Marks a bill as paid.
    
    Payload should contain:
    - bill_id: int (required)
    - paid: str (optional: yes, no, partial, default: yes)
    """
    try:
        bill_id = payload.get("bill_id")
        if not bill_id:
            return ActionResult(
                action_type="bills.mark_paid",
                success=False,
                message="Missing required field: 'bill_id'",
                error="Missing required field: 'bill_id'"
            )
        
        bill = db.query(Bill).filter(Bill.id == bill_id).first()
        if not bill:
            return ActionResult(
                action_type="bills.mark_paid",
                success=False,
                message=f"Bill #{bill_id} not found",
                error=f"Bill #{bill_id} not found"
            )
        
        paid_status = payload.get("paid", "yes")
        bill.paid = paid_status
        
        if paid_status == "yes" and bill.paid_at is None:
            bill.paid_at = datetime.utcnow()
        elif paid_status != "yes":
            bill.paid_at = None
        
        db.commit()
        
        return ActionResult(
            action_type="bills.mark_paid",
            success=True,
            message=f"Marked bill #{bill_id} as {paid_status}"
        )
    except Exception as e:
        db.rollback()
        return ActionResult(
            action_type="bills.mark_paid",
            success=False,
            message=f"Failed to mark bill as paid: {str(e)}",
            error=str(e)
        )


def _handle_bills_list(db: Session, payload: Dict[str, Any], context: Dict[str, Any]) -> ActionResult:
    """
    Handle bills.list action.
    
    Lists bills with optional filters.
    
    Payload can contain:
    - paid: str (optional filter: yes, no, partial)
    - category: str (optional filter)
    - upcoming: bool (optional: show only upcoming)
    - overdue: bool (optional: show only overdue)
    - limit: int (optional, default 20)
    """
    try:
        from datetime import timedelta
        
        query = db.query(Bill)
        
        if payload.get("paid"):
            query = query.filter(Bill.paid == payload.get("paid"))
        if payload.get("category"):
            query = query.filter(Bill.category == payload.get("category"))
        
        now = datetime.utcnow()
        if payload.get("upcoming"):
            future_date = now + timedelta(days=30)
            query = query.filter(Bill.due_date >= now, Bill.due_date <= future_date)
        if payload.get("overdue"):
            query = query.filter(Bill.due_date < now, Bill.paid == "no")
        
        limit = payload.get("limit", 20)
        bills = query.order_by(Bill.due_date.asc()).limit(limit).all()
        
        return ActionResult(
            action_type="bills.list",
            success=True,
            message=f"Found {len(bills)} bill(s)"
        )
    except Exception as e:
        return ActionResult(
            action_type="bills.list",
            success=False,
            message=f"Failed to list bills: {str(e)}",
            error=str(e)
        )


def _handle_income_create_income(db: Session, payload: Dict[str, Any], context: Dict[str, Any]) -> ActionResult:
    """
    Handle income.create_income action.
    
    Creates a new Income entry in the database.
    
    Payload should contain:
    - source: str (required)
    - amount: str (required)
    - received_date: datetime (required)
    - category: str (optional)
    - notes: str (optional)
    - is_recurring: str (optional: yes, no)
    - recurrence_frequency: str (optional: monthly, quarterly, yearly)
    """
    try:
        source = payload.get("source")
        amount = payload.get("amount")
        received_date = payload.get("received_date")
        
        if not source or not amount or not received_date:
            return ActionResult(
                action_type="income.create_income",
                success=False,
                message="Missing required fields: 'source', 'amount', 'received_date'",
                error="Missing required fields"
            )
        
        # Parse received_date if it's a string
        if isinstance(received_date, str):
            try:
                received_date = datetime.fromisoformat(received_date.replace("Z", "+00:00"))
            except:
                return ActionResult(
                    action_type="income.create_income",
                    success=False,
                    message=f"Invalid received_date format: {received_date}",
                    error="Invalid received_date format"
                )
        
        # Get OttoContext from context
        otto_context: OttoContext = context.get("otto_context")
        if not otto_context:
            return ActionResult(
                action_type="income.create_income",
                success=False,
                message="Missing OttoContext",
                error="OttoContext required"
            )
        
        income = Income(
            household_id=otto_context.household_id,
            user_id=otto_context.user_id,
            source=source,
            amount=amount,
            received_date=received_date,
            category=payload.get("category"),
            notes=payload.get("notes"),
            is_recurring=payload.get("is_recurring", "no"),
            recurrence_frequency=payload.get("recurrence_frequency")
        )
        
        # Calculate next_expected_date for recurring income
        if income.is_recurring == "yes" and income.recurrence_frequency:
            from datetime import timedelta
            if income.recurrence_frequency == "monthly":
                income.next_expected_date = received_date + timedelta(days=30)
            elif income.recurrence_frequency == "quarterly":
                income.next_expected_date = received_date + timedelta(days=90)
            elif income.recurrence_frequency == "yearly":
                income.next_expected_date = received_date + timedelta(days=365)
        
        db.add(income)
        db.commit()
        db.refresh(income)
        
        return ActionResult(
            action_type="income.create_income",
            success=True,
            message=f"Created income entry #{income.id}: {source}"
        )
    except Exception as e:
        db.rollback()
        return ActionResult(
            action_type="income.create_income",
            success=False,
            message=f"Failed to create income: {str(e)}",
            error=str(e)
        )


def _handle_income_update_income(db: Session, payload: Dict[str, Any], context: Dict[str, Any]) -> ActionResult:
    """
    Handle income.update_income action.
    
    Updates an existing Income entry.
    
    Payload should contain:
    - income_id: int (required)
    - Other fields can also be updated
    """
    try:
        income_id = payload.get("income_id")
        if not income_id:
            return ActionResult(
                action_type="income.update_income",
                success=False,
                message="Missing required field: 'income_id'",
                error="Missing required field: 'income_id'"
            )
        
        income = db.query(Income).filter(Income.id == income_id).first()
        if not income:
            return ActionResult(
                action_type="income.update_income",
                success=False,
                message=f"Income entry #{income_id} not found",
                error=f"Income entry #{income_id} not found"
            )
        
        # Update fields
        if payload.get("source") is not None:
            income.source = payload.get("source")
        if payload.get("amount") is not None:
            income.amount = payload.get("amount")
        if payload.get("received_date") is not None:
            received_date = payload.get("received_date")
            if isinstance(received_date, str):
                received_date = datetime.fromisoformat(received_date.replace("Z", "+00:00"))
            income.received_date = received_date
        if payload.get("category") is not None:
            income.category = payload.get("category")
        if payload.get("notes") is not None:
            income.notes = payload.get("notes")
        if payload.get("is_recurring") is not None:
            income.is_recurring = payload.get("is_recurring")
        if payload.get("recurrence_frequency") is not None:
            income.recurrence_frequency = payload.get("recurrence_frequency")
        if payload.get("next_expected_date") is not None:
            next_date = payload.get("next_expected_date")
            if isinstance(next_date, str):
                next_date = datetime.fromisoformat(next_date.replace("Z", "+00:00"))
            income.next_expected_date = next_date
        
        db.commit()
        
        return ActionResult(
            action_type="income.update_income",
            success=True,
            message=f"Updated income entry #{income_id}"
        )
    except Exception as e:
        db.rollback()
        return ActionResult(
            action_type="income.update_income",
            success=False,
            message=f"Failed to update income: {str(e)}",
            error=str(e)
        )


def _handle_transactions_create_transaction(db: Session, payload: Dict[str, Any], context: Dict[str, Any]) -> ActionResult:
    """
    Handle transactions.create_transaction action.
    
    Creates a new Transaction in the database.
    
    Payload should contain:
    - date: datetime (required)
    - amount: str (required)
    - vendor: str (optional)
    - description: str (optional)
    - tax_category: str (optional)
    - source: str (optional, default: "manual")
    - source_id: str (optional)
    - notes: str (optional)
    - tags: list (optional)
    """
    try:
        date = payload.get("date")
        amount = payload.get("amount")
        
        if not date or not amount:
            return ActionResult(
                action_type="transactions.create_transaction",
                success=False,
                message="Missing required fields: 'date', 'amount'",
                error="Missing required fields"
            )
        
        # Parse date if it's a string
        if isinstance(date, str):
            try:
                date = datetime.fromisoformat(date.replace("Z", "+00:00"))
            except:
                return ActionResult(
                    action_type="transactions.create_transaction",
                    success=False,
                    message=f"Invalid date format: {date}",
                    error="Invalid date format"
                )
        
        transaction = Transaction(
            date=date,
            amount=amount,
            vendor=payload.get("vendor"),
            description=payload.get("description"),
            tax_category=payload.get("tax_category"),
            source=payload.get("source", "manual"),
            source_id=payload.get("source_id"),
            notes=payload.get("notes"),
            tags=payload.get("tags")
        )
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        
        return ActionResult(
            action_type="transactions.create_transaction",
            success=True,
            message=f"Created transaction #{transaction.id}"
        )
    except Exception as e:
        db.rollback()
        return ActionResult(
            action_type="transactions.create_transaction",
            success=False,
            message=f"Failed to create transaction: {str(e)}",
            error=str(e)
        )


def _handle_transactions_update_transaction(db: Session, payload: Dict[str, Any], context: Dict[str, Any]) -> ActionResult:
    """
    Handle transactions.update_transaction action.
    
    Updates an existing Transaction.
    
    Payload should contain:
    - transaction_id: int (required)
    - Other fields can also be updated
    """
    try:
        transaction_id = payload.get("transaction_id")
        if not transaction_id:
            return ActionResult(
                action_type="transactions.update_transaction",
                success=False,
                message="Missing required field: 'transaction_id'",
                error="Missing required field: 'transaction_id'"
            )
        
        transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if not transaction:
            return ActionResult(
                action_type="transactions.update_transaction",
                success=False,
                message=f"Transaction #{transaction_id} not found",
                error=f"Transaction #{transaction_id} not found"
            )
        
        # Update fields
        if payload.get("date") is not None:
            date = payload.get("date")
            if isinstance(date, str):
                date = datetime.fromisoformat(date.replace("Z", "+00:00"))
            transaction.date = date
        if payload.get("amount") is not None:
            transaction.amount = payload.get("amount")
        if payload.get("vendor") is not None:
            transaction.vendor = payload.get("vendor")
        if payload.get("description") is not None:
            transaction.description = payload.get("description")
        if payload.get("tax_category") is not None:
            transaction.tax_category = payload.get("tax_category")
        if payload.get("notes") is not None:
            transaction.notes = payload.get("notes")
        if payload.get("tags") is not None:
            transaction.tags = payload.get("tags")
        
        db.commit()
        
        return ActionResult(
            action_type="transactions.update_transaction",
            success=True,
            message=f"Updated transaction #{transaction_id}"
        )
    except Exception as e:
        db.rollback()
        return ActionResult(
            action_type="transactions.update_transaction",
            success=False,
            message=f"Failed to update transaction: {str(e)}",
            error=str(e)
        )


def _handle_transactions_categorize_transaction(db: Session, payload: Dict[str, Any], context: Dict[str, Any]) -> ActionResult:
    """
    Handle transactions.categorize_transaction action.
    
    Categorizes a transaction (updates tax_category).
    
    Payload should contain:
    - transaction_id: int (required)
    - tax_category: str (required)
    """
    try:
        transaction_id = payload.get("transaction_id")
        tax_category = payload.get("tax_category")
        
        if not transaction_id or not tax_category:
            return ActionResult(
                action_type="transactions.categorize_transaction",
                success=False,
                message="Missing required fields: 'transaction_id', 'tax_category'",
                error="Missing required fields"
            )
        
        # Use update_transaction handler
        return _handle_transactions_update_transaction(
            db,
            {
                "transaction_id": transaction_id,
                "tax_category": tax_category
            },
            context
        )
    except Exception as e:
        return ActionResult(
            action_type="transactions.categorize_transaction",
            success=False,
            message=f"Failed to categorize transaction: {str(e)}",
            error=str(e)
        )


def _handle_tax_propose_category(db: Session, payload: Dict[str, Any], context: Dict[str, Any]) -> ActionResult:
    """
    Handle tax.propose_category action.
    
    Proposes a new category for approval. This is a Tier 2 action that requires approval.
    
    Payload should contain:
    - code: str (required) - Category code (e.g., "TOOLS_HAND")
    - label: str (required) - Display name (e.g., "Hand Tools")
    - type: str (required) - "income", "expense", "transfer", "other"
    - reason: str (optional) - Why this category is needed
    """
    try:
        from models import Category, CategoryVersion
        from otto.context import get_default_context
        from datetime import date
        
        code = payload.get("code")
        label = payload.get("label")
        category_type = payload.get("type", "expense")
        reason = payload.get("reason", "")
        
        if not code or not label:
            return ActionResult(
                action_type="tax.propose_category",
                success=False,
                message="Missing required fields: 'code', 'label'",
                error="Missing required fields"
            )
        
        otto_context = get_default_context(db)
        
        # Check if category already exists
        existing = db.query(Category).filter(
            Category.code == code,
            Category.household_id == otto_context.household_id
        ).first()
        
        if existing:
            return ActionResult(
                action_type="tax.propose_category",
                success=False,
                message=f"Category with code '{code}' already exists (ID: {existing.id})",
                error="Category already exists"
            )
        
        # Create the category (for now, auto-approve; in future this could require approval)
        new_category = Category(
            household_id=otto_context.household_id,
            code=code,
            label=label,
            type=category_type,
            is_active=True
        )
        
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        
        # Create initial version
        version = CategoryVersion(
            category_id=new_category.id,
            version=1,
            effective_from=date.today(),
            notes=reason or "Created via tax.propose_category action"
        )
        db.add(version)
        db.commit()
        
        return ActionResult(
            action_type="tax.propose_category",
            success=True,
            message=f"Category '{label}' (code: {code}) created with ID {new_category.id}",
        )
    except Exception as e:
        db.rollback()
        return ActionResult(
            action_type="tax.propose_category",
            success=False,
            message=f"Failed to create category: {str(e)}",
            error=str(e)
        )


def _handle_memory_create(db: Session, payload: Dict[str, Any], context: Dict[str, Any]) -> ActionResult:
    """
    Handle memory.create action.
    
    Creates a new memory entry.
    
    Payload should contain:
    - category: str (required)
    - content: str (required)
    - tags: List[str] (optional)
    - source: str (optional, default="user")
    - confidence_score: float (optional, default=1.0)
    """
    try:
        from models import OttoMemory
        from otto.context import get_default_context
        
        category = payload.get("category")
        content = payload.get("content")
        tags = payload.get("tags")
        source = payload.get("source", "user")
        confidence_score = payload.get("confidence_score", 1.0)
        
        if not category or not content:
            return ActionResult(
                action_type="memory.create",
                success=False,
                message="Missing required fields: 'category', 'content'",
                error="Missing required fields"
            )
        
        otto_context = get_default_context(db)
        
        new_memory = OttoMemory(
            household_id=otto_context.household_id,
            category=category,
            content=content,
            tags=tags,
            source=source,
            confidence_score=confidence_score,
            version=1
        )
        
        db.add(new_memory)
        db.commit()
        db.refresh(new_memory)
        
        return ActionResult(
            action_type="memory.create",
            success=True,
            message=f"Memory created: {category} - {content[:50]}... (ID: {new_memory.id})",
        )
    except Exception as e:
        db.rollback()
        return ActionResult(
            action_type="memory.create",
            success=False,
            message=f"Failed to create memory: {str(e)}",
            error=str(e)
        )


def _handle_memory_update(db: Session, payload: Dict[str, Any], context: Dict[str, Any]) -> ActionResult:
    """
    Handle memory.update action.
    
    Updates an existing memory entry.
    
    Phase 4: Creates history entry before updating.
    
    Payload should contain:
    - id: int (required)
    - content: str (optional)
    - tags: List[str] (optional)
    - confidence_score: float (optional)
    - expires_at: str (optional, ISO8601 datetime)
    - is_stale: bool (optional)
    - stale_reason: str (optional)
    """
    try:
        from models import OttoMemory, OttoMemoryHistory
        from otto.context import get_default_context
        
        memory_id = payload.get("id")
        if not memory_id:
            return ActionResult(
                action_type="memory.update",
                success=False,
                message="Missing required field: 'id'",
                error="Missing required field"
            )
        
        otto_context = get_default_context(db)
        
        memory = db.query(OttoMemory).filter(
            OttoMemory.id == memory_id,
            OttoMemory.household_id == otto_context.household_id
        ).first()
        
        if not memory:
            return ActionResult(
                action_type="memory.update",
                success=False,
                message=f"Memory {memory_id} not found",
                error=f"Memory {memory_id} not found"
            )
        
        # Phase 4: Create history entry before updating
        history_entry = OttoMemoryHistory(
            memory_id=memory.id,
            household_id=memory.household_id,
            version=memory.version,
            category=memory.category,
            content=memory.content,
            tags=memory.tags,
            source=memory.source,
            changed_by="Otto"  # Could be enhanced with user context
        )
        db.add(history_entry)
        
        # Update fields
        if payload.get("content") is not None:
            memory.content = payload["content"]
        if payload.get("tags") is not None:
            memory.tags = payload["tags"]
        if payload.get("confidence_score") is not None:
            memory.confidence_score = payload["confidence_score"]
        if payload.get("expires_at") is not None:
            expires_at_str = payload["expires_at"]
            if isinstance(expires_at_str, str):
                memory.expires_at = datetime.fromisoformat(expires_at_str.replace("Z", "+00:00"))
            else:
                memory.expires_at = expires_at_str
        if payload.get("is_stale") is not None:
            memory.is_stale = payload["is_stale"]
        if payload.get("stale_reason") is not None:
            memory.stale_reason = payload["stale_reason"]
        
        # Increment version
        memory.version += 1
        memory.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(memory)
        
        return ActionResult(
            action_type="memory.update",
            success=True,
            message=f"Memory {memory_id} updated (version {memory.version})",
        )
    except Exception as e:
        db.rollback()
        return ActionResult(
            action_type="memory.update",
            success=False,
            message=f"Failed to update memory: {str(e)}",
            error=str(e)
        )


def _handle_memory_mark_stale(db: Session, payload: Dict[str, Any], context: Dict[str, Any]) -> ActionResult:
    """
    Handle memory.mark_stale action.
    
    Marks a memory as stale without deleting it.
    
    Payload should contain:
    - memory_id: int (required)
    - reason: str (required)
    """
    try:
        from models import OttoMemory
        from otto.context import get_default_context
        
        memory_id = payload.get("memory_id")
        reason = payload.get("reason", "")
        
        if not memory_id:
            return ActionResult(
                action_type="memory.mark_stale",
                success=False,
                message="Missing required field: 'memory_id'",
                error="Missing required field"
            )
        
        otto_context = get_default_context(db)
        
        memory = db.query(OttoMemory).filter(
            OttoMemory.id == memory_id,
            OttoMemory.household_id == otto_context.household_id
        ).first()
        
        if not memory:
            return ActionResult(
                action_type="memory.mark_stale",
                success=False,
                message=f"Memory {memory_id} not found",
                error=f"Memory {memory_id} not found"
            )
        
        memory.is_stale = True
        memory.stale_reason = reason
        memory.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(memory)
        
        return ActionResult(
            action_type="memory.mark_stale",
            success=True,
            message=f"Memory {memory_id} marked as stale: {reason}",
        )
    except Exception as e:
        db.rollback()
        return ActionResult(
            action_type="memory.mark_stale",
            success=False,
            message=f"Failed to mark memory stale: {str(e)}",
            error=str(e)
        )


def _handle_memory_set_expiration(db: Session, payload: Dict[str, Any], context: Dict[str, Any]) -> ActionResult:
    """
    Handle memory.set_expiration action.
    
    Sets expiration date for a memory.
    
    Payload should contain:
    - memory_id: int (required)
    - expires_at: str (ISO8601 datetime, required)
    """
    try:
        from models import OttoMemory
        from otto.context import get_default_context
        
        memory_id = payload.get("memory_id")
        expires_at_str = payload.get("expires_at")
        
        if not memory_id or not expires_at_str:
            return ActionResult(
                action_type="memory.set_expiration",
                success=False,
                message="Missing required fields: 'memory_id', 'expires_at'",
                error="Missing required fields"
            )
        
        otto_context = get_default_context(db)
        
        memory = db.query(OttoMemory).filter(
            OttoMemory.id == memory_id,
            OttoMemory.household_id == otto_context.household_id
        ).first()
        
        if not memory:
            return ActionResult(
                action_type="memory.set_expiration",
                success=False,
                message=f"Memory {memory_id} not found",
                error=f"Memory {memory_id} not found"
            )
        
        # Parse datetime - handle various ISO formats
        expires_at = None
        if isinstance(expires_at_str, str):
            try:
                # Handle ISO format with 'Z' timezone
                if expires_at_str.endswith("Z"):
                    expires_at = datetime.fromisoformat(expires_at_str.replace("Z", "+00:00"))
                # Handle ISO format with timezone offset
                elif "+" in expires_at_str or expires_at_str.count("-") > 2:
                    expires_at = datetime.fromisoformat(expires_at_str)
                # Handle ISO format without timezone (assume naive datetime)
                else:
                    # Try parsing as-is first
                    try:
                        expires_at = datetime.fromisoformat(expires_at_str)
                    except ValueError:
                        # If that fails, try removing microseconds
                        if "." in expires_at_str:
                            clean_str = expires_at_str.split(".")[0]
                            expires_at = datetime.fromisoformat(clean_str)
                        else:
                            raise ValueError(f"Invalid datetime format: {expires_at_str}")
            except (ValueError, AttributeError) as e:
                return ActionResult(
                    action_type="memory.set_expiration",
                    success=False,
                    message=f"Invalid datetime format: {expires_at_str}",
                    error=f"Datetime parsing failed: {str(e)}"
                )
        elif isinstance(expires_at_str, datetime):
            expires_at = expires_at_str
        else:
            return ActionResult(
                action_type="memory.set_expiration",
                success=False,
                message=f"Invalid expires_at type: {type(expires_at_str)}",
                error="expires_at must be a string or datetime object"
            )
        
        if expires_at is None:
            return ActionResult(
                action_type="memory.set_expiration",
                success=False,
                message="Failed to parse expiration date",
                error="expires_at could not be parsed"
            )
        
        # Set expiration
        memory.expires_at = expires_at
        memory.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(memory)
        
        return ActionResult(
            action_type="memory.set_expiration",
            success=True,
            message=f"Memory {memory_id} expiration set to {expires_at_str}",
        )
    except Exception as e:
        db.rollback()
        import traceback
        error_details = traceback.format_exc()
        return ActionResult(
            action_type="memory.set_expiration",
            success=False,
            message=f"Failed to set expiration: {str(e)}",
            error=f"{str(e)}\n{error_details}"
        )


def _handle_memory_link(db: Session, payload: Dict[str, Any], context: Dict[str, Any]) -> ActionResult:
    """
    Handle memory.link action.
    
    Creates a link from a memory to another memory or domain object.
    
    Payload should contain:
    - from_memory_id: int (required)
    - to_memory_id: int (optional, if target_type is "memory")
    - target_type: str (required) - "task", "bill", "transaction", "event", "memory"
    - target_id: int (required)
    - relationship_type: str (required) - "supports", "contradicts", "refines", "applies_to", etc.
    - notes: str (optional)
    """
    try:
        from models import OttoMemory, OttoMemoryLink
        from otto.context import get_default_context
        
        from_memory_id = payload.get("from_memory_id")
        target_type = payload.get("target_type")
        target_id = payload.get("target_id")
        relationship_type = payload.get("relationship_type")
        to_memory_id = payload.get("to_memory_id")
        notes = payload.get("notes")
        
        if not from_memory_id or not target_type or not target_id or not relationship_type:
            return ActionResult(
                action_type="memory.link",
                success=False,
                message="Missing required fields: 'from_memory_id', 'target_type', 'target_id', 'relationship_type'",
                error="Missing required fields"
            )
        
        otto_context = get_default_context(db)
        
        # Verify memory exists and belongs to household
        memory = db.query(OttoMemory).filter(
            OttoMemory.id == from_memory_id,
            OttoMemory.household_id == otto_context.household_id
        ).first()
        
        if not memory:
            return ActionResult(
                action_type="memory.link",
                success=False,
                message=f"Memory {from_memory_id} not found",
                error=f"Memory {from_memory_id} not found"
            )
        
        # If linking to another memory, set to_memory_id
        if target_type == "memory":
            to_memory_id = target_id
        
        new_link = OttoMemoryLink(
            from_memory_id=from_memory_id,
            to_memory_id=to_memory_id,
            target_type=target_type,
            target_id=target_id,
            relationship_type=relationship_type,
            notes=notes
        )
        
        db.add(new_link)
        db.commit()
        db.refresh(new_link)
        
        return ActionResult(
            action_type="memory.link",
            success=True,
            message=f"Link created: memory {from_memory_id} -> {target_type} {target_id} ({relationship_type})",
        )
    except Exception as e:
        db.rollback()
        return ActionResult(
            action_type="memory.link",
            success=False,
            message=f"Failed to create link: {str(e)}",
            error=str(e)
        )


def _handle_memory_delete(db: Session, payload: Dict[str, Any], context: Dict[str, Any]) -> ActionResult:
    """
    Handle memory.delete action.
    
    Deletes a memory entry.
    
    Phase 4: Creates final history entry before deletion.
    
    Payload should contain:
    - id: int (required)
    """
    try:
        from models import OttoMemory, OttoMemoryHistory
        from otto.context import get_default_context
        
        memory_id = payload.get("id")
        if not memory_id:
            return ActionResult(
                action_type="memory.delete",
                success=False,
                message="Missing required field: 'id'",
                error="Missing required field"
            )
        
        otto_context = get_default_context(db)
        
        memory = db.query(OttoMemory).filter(
            OttoMemory.id == memory_id,
            OttoMemory.household_id == otto_context.household_id
        ).first()
        
        if not memory:
            return ActionResult(
                action_type="memory.delete",
                success=False,
                message=f"Memory {memory_id} not found",
                error=f"Memory {memory_id} not found"
            )
        
        # Phase 4: Create final history entry before deletion
        history_entry = OttoMemoryHistory(
            memory_id=memory.id,
            household_id=memory.household_id,
            version=memory.version,
            category=memory.category,
            content=memory.content,
            tags=memory.tags,
            source=memory.source,
            changed_by="Otto"
        )
        db.add(history_entry)
        
        db.delete(memory)
        db.commit()
        
        return ActionResult(
            action_type="memory.delete",
            success=True,
            message=f"Memory {memory_id} deleted",
        )
    except Exception as e:
        db.rollback()
        return ActionResult(
            action_type="memory.delete",
            success=False,
            message=f"Failed to delete memory: {str(e)}",
            error=str(e)
        )


def _handle_otto_log(payload: Dict[str, Any], context: Dict[str, Any]) -> ActionResult:
    """
    Handle otto.log action.
    
    This is a no-op action for logging/debugging purposes.
    The log message is returned in the result.
    
    Payload should contain:
    - message: str
    - level: str (optional, e.g. "info", "warning", "error")
    """
    message = payload.get("message", "No message provided")
    level = payload.get("level", "info")
    
    # For now, just return success - in the future this could write to a log file
    return ActionResult(
        action_type="otto.log",
        success=True,
        message=f"[{level.upper()}] {message}"
    )

