"""
SchedulingSkill - Automatically schedules recurring tasks and reminders
Phase 3 — CONTROL_OTTO_PHASE3.md
Implements:
- Recurring task creation
- Recurring bill reminder creation
- Recurring event creation
- Recurring item management
- Integration with Life OS backend
"""

from typing import List, Dict, Any, Optional
import os
import httpx
from datetime import datetime, timedelta

from ..core.models import Task, TaskResult, TaskStatus
from ..core.skill_base import Skill, SkillHealthIssue, SkillContext
from ..core.logging_utils import get_logger

logger = get_logger(__name__)


class SchedulingSkill:
    """Skill that handles recurring scheduling"""
    
    name = "scheduling"
    description = "Schedules recurring tasks, bill reminders, and events"
    
    def __init__(self):
        # Life OS backend API URL
        self.life_os_api_url = os.getenv("LIFE_OS_API_URL", "http://localhost:8000")
        # Otto API URL for creating OttoTasks
        self.otto_api_url = os.getenv("OTTO_API_URL", "http://localhost:8001")
    
    def can_handle(self, task: Task) -> bool:
        """Check if this skill can handle the task"""
        return task.type in [
            "schedule.create_recurring_task",
            "schedule.create_recurring_bill_reminder",
            "schedule.create_recurring_event",
            "schedule.list_recurring_items",
            "schedule.update_recurring_item",
        ]
    
    def run(self, task: Task, context: SkillContext) -> TaskResult:
        """Execute the scheduling operation"""
        try:
            task_type = task.type
            
            if task_type == "schedule.create_recurring_task":
                return self._handle_create_recurring_task(task, context)
            elif task_type == "schedule.create_recurring_bill_reminder":
                return self._handle_create_recurring_bill_reminder(task, context)
            elif task_type == "schedule.create_recurring_event":
                return self._handle_create_recurring_event(task, context)
            elif task_type == "schedule.list_recurring_items":
                return self._handle_list_recurring_items(task, context)
            elif task_type == "schedule.update_recurring_item":
                return self._handle_update_recurring_item(task, context)
            else:
                return TaskResult(
                    task_id=task.id,
                    success=False,
                    message=f"Unknown task type: {task_type}"
                )
        except Exception as e:
            logger.error(f"Error in SchedulingSkill: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error scheduling: {str(e)}"
            )
    
    def _handle_create_recurring_task(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle creating a recurring task"""
        payload = task.payload or {}
        
        # Calculate next_run_at based on frequency
        frequency = payload.get("frequency", "weekly")  # daily, weekly, monthly, yearly
        start_date = payload.get("start_date")
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
        elif not start_date:
            start_date = datetime.utcnow()
        
        next_run_at = self._calculate_next_run(start_date, frequency)
        
        # Create OttoTask that will create the LifeOSTask
        actions = [{
            "type": "otto.create_recurring_task",
            "tier": 1,
            "payload": {
                "type": "life_os.create_task",
                "description": f"Recurring task: {payload.get('title', 'Untitled')}",
                "payload": {
                    "title": payload.get("title"),
                    "description": payload.get("description"),
                    "assignee": payload.get("assignee"),
                    "priority": payload.get("priority", "medium"),
                    "category": payload.get("category"),
                },
                "next_run_at": next_run_at.isoformat(),
                "frequency": frequency
            }
        }]
        
        return TaskResult(
            task_id=task.id,
            success=True,
            message=f"Will create recurring task: {payload.get('title', 'Untitled')} ({frequency})",
            actions=actions
        )
    
    def _handle_create_recurring_bill_reminder(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle creating a recurring bill reminder"""
        payload = task.payload or {}
        bill_id = payload.get("bill_id")
        
        if not bill_id:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required field: 'bill_id'"
            )
        
        # Get bill to determine frequency
        try:
            with httpx.Client(timeout=10.0) as client:
                bill_response = client.get(f"{self.life_os_api_url}/bills/{bill_id}")
                
                if bill_response.status_code != 200:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Bill #{bill_id} not found"
                    )
                
                bill = bill_response.json()
                frequency = bill.get("recurrence_frequency", "monthly")
                due_date_str = bill.get("due_date")
                
                if due_date_str:
                    due_date = datetime.fromisoformat(due_date_str.replace("Z", "+00:00"))
                    # Create reminder 7 days before due date
                    reminder_date = due_date - timedelta(days=7)
                    
                    # Create OttoTask for recurring reminder
                    actions = [{
                        "type": "otto.create_recurring_task",
                        "tier": 1,
                        "payload": {
                            "type": "bill_reminder",
                            "description": f"Recurring reminder for bill: {bill.get('name')}",
                            "payload": {
                                "bill_id": bill_id
                            },
                            "next_run_at": reminder_date.isoformat(),
                            "frequency": frequency
                        }
                    }]
                    
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=f"Will create recurring bill reminder for bill #{bill_id}",
                        actions=actions
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message="Bill has no due date"
                    )
        except Exception as e:
            logger.error(f"Error creating recurring bill reminder: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error creating recurring bill reminder: {str(e)}"
            )
    
    def _handle_create_recurring_event(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle creating a recurring event"""
        payload = task.payload or {}
        
        # Create calendar event with recurrence
        actions = [{
            "type": "calendar.create_event",
            "tier": 2,
            "payload": {
                "title": payload.get("title"),
                "description": payload.get("description"),
                "start_time": payload.get("start_time"),
                "end_time": payload.get("end_time"),
                "location": payload.get("location"),
                "category": payload.get("category"),
                "is_recurring": "yes",
                "recurrence_frequency": payload.get("frequency", "weekly"),
            }
        }]
        
        return TaskResult(
            task_id=task.id,
            success=True,
            message=f"Will create recurring event: {payload.get('title', 'Untitled')}",
            actions=actions
        )
    
    def _handle_list_recurring_items(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle listing recurring items"""
        # List recurring tasks, bills, and events
        try:
            recurring_items = []
            
            # Get recurring tasks (OttoTasks with next_run_at)
            with httpx.Client(timeout=10.0) as client:
                # Get recurring OttoTasks
                otto_tasks_response = client.get(
                    f"{self.life_os_api_url}/otto/tasks",
                    params={"limit": 100}
                )
                
                if otto_tasks_response.status_code == 200:
                    otto_tasks = otto_tasks_response.json()
                    for otto_task in otto_tasks:
                        if otto_task.get("next_run_at"):
                            recurring_items.append({
                                "type": "task",
                                "id": otto_task.get("id"),
                                "description": otto_task.get("description"),
                                "next_run_at": otto_task.get("next_run_at"),
                                "frequency": "unknown"  # Would need to store this
                            })
                
                # Get recurring bills
                bills_response = client.get(
                    f"{self.life_os_api_url}/bills",
                    params={"limit": 100}
                )
                
                if bills_response.status_code == 200:
                    bills = bills_response.json()
                    for bill in bills:
                        if bill.get("is_recurring") == "yes":
                            recurring_items.append({
                                "type": "bill",
                                "id": bill.get("id"),
                                "name": bill.get("name"),
                                "next_due_date": bill.get("next_due_date"),
                                "frequency": bill.get("recurrence_frequency")
                            })
                
                # Get recurring events
                events_response = client.get(
                    f"{self.life_os_api_url}/calendar",
                    params={"limit": 100}
                )
                
                if events_response.status_code == 200:
                    events = events_response.json()
                    for event in events:
                        if event.get("is_recurring") == "yes":
                            recurring_items.append({
                                "type": "event",
                                "id": event.get("id"),
                                "title": event.get("title"),
                                "start_time": event.get("start_time"),
                                "frequency": event.get("recurrence_frequency")
                            })
            
            message = f"Found {len(recurring_items)} recurring item(s)"
            return TaskResult(
                task_id=task.id,
                success=True,
                message=message,
                data={"items": recurring_items, "count": len(recurring_items)}
            )
        except Exception as e:
            logger.error(f"Error listing recurring items: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error listing recurring items: {str(e)}"
            )
    
    def _handle_update_recurring_item(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle updating a recurring item"""
        payload = task.payload or {}
        item_type = payload.get("item_type")  # task, bill, event
        item_id = payload.get("item_id")
        
        if not item_type or not item_id:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required fields: 'item_type' and 'item_id'"
            )
        
        # Update based on type
        if item_type == "task":
            # Update OttoTask
            try:
                with httpx.Client(timeout=10.0) as client:
                    update_data = {}
                    if payload.get("next_run_at"):
                        update_data["next_run_at"] = payload.get("next_run_at")
                    if payload.get("frequency"):
                        update_data["frequency"] = payload.get("frequency")
                    
                    # Would need PATCH endpoint for OttoTask
                    # For now, return success with note
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=f"Recurring task #{item_id} update requested (endpoint may need implementation)"
                    )
            except Exception as e:
                return TaskResult(
                    task_id=task.id,
                    success=False,
                    message=f"Error updating recurring task: {str(e)}"
                )
        elif item_type == "bill":
            # Update bill recurrence
            try:
                with httpx.Client(timeout=10.0) as client:
                    update_data = {}
                    if payload.get("recurrence_frequency"):
                        update_data["recurrence_frequency"] = payload.get("recurrence_frequency")
                    if payload.get("next_due_date"):
                        update_data["next_due_date"] = payload.get("next_due_date")
                    
                    response = client.patch(
                        f"{self.life_os_api_url}/bills/{item_id}",
                        json=update_data
                    )
                    
                    if response.status_code == 200:
                        return TaskResult(
                            task_id=task.id,
                            success=True,
                            message=f"Updated recurring bill #{item_id}"
                        )
                    else:
                        return TaskResult(
                            task_id=task.id,
                            success=False,
                            message=f"Failed to update bill: {response.status_code}"
                        )
            except Exception as e:
                return TaskResult(
                    task_id=task.id,
                    success=False,
                    message=f"Error updating recurring bill: {str(e)}"
                )
        elif item_type == "event":
            # Update event recurrence
            try:
                with httpx.Client(timeout=10.0) as client:
                    update_data = {}
                    if payload.get("recurrence_frequency"):
                        update_data["recurrence_frequency"] = payload.get("recurrence_frequency")
                    if payload.get("recurrence_end_date"):
                        update_data["recurrence_end_date"] = payload.get("recurrence_end_date")
                    
                    response = client.patch(
                        f"{self.life_os_api_url}/calendar/{item_id}",
                        json=update_data
                    )
                    
                    if response.status_code == 200:
                        return TaskResult(
                            task_id=task.id,
                            success=True,
                            message=f"Updated recurring event #{item_id}"
                        )
                    else:
                        return TaskResult(
                            task_id=task.id,
                            success=False,
                            message=f"Failed to update event: {response.status_code}"
                        )
            except Exception as e:
                return TaskResult(
                    task_id=task.id,
                    success=False,
                    message=f"Error updating recurring event: {str(e)}"
                )
        else:
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Unknown item type: {item_type}"
            )
    
    def _calculate_next_run(self, start_date: datetime, frequency: str) -> datetime:
        """Calculate next run date based on frequency"""
        if frequency == "daily":
            return start_date + timedelta(days=1)
        elif frequency == "weekly":
            return start_date + timedelta(days=7)
        elif frequency == "monthly":
            return start_date + timedelta(days=30)
        elif frequency == "yearly":
            return start_date + timedelta(days=365)
        else:
            # Default to weekly
            return start_date + timedelta(days=7)
    
    def self_test(self, context: SkillContext) -> List[SkillHealthIssue]:
        """Run health checks on this skill"""
        issues = []
        
        # Check if Life OS API is reachable
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"{self.life_os_api_url}/health")
                if response.status_code != 200:
                    issues.append(SkillHealthIssue(
                        code="life_os_api_unreachable",
                        message=f"Life OS API returned status {response.status_code}",
                        suggestion="Ensure Life OS backend is running and LIFE_OS_API_URL is correct"
                    ))
        except Exception as e:
            issues.append(SkillHealthIssue(
                code="life_os_api_unreachable",
                message=f"Cannot reach Life OS API: {str(e)}",
                suggestion="Ensure Life OS backend is running and LIFE_OS_API_URL is correct"
            ))
        
        return issues

