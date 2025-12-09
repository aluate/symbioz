"""
ReminderSkill - Sends reminders for tasks, bills, events
Phase 3 — CONTROL_OTTO_PHASE3.md
Implements:
- Reminder creation
- Reminder sending (via tasks/logs for now)
- Upcoming reminders listing
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


class ReminderSkill:
    """Skill that sends reminders"""
    
    name = "reminder"
    description = "Sends reminders for tasks, bills, and events"
    
    def __init__(self):
        # Life OS backend API URL
        self.life_os_api_url = os.getenv("LIFE_OS_API_URL", "http://localhost:8000")
    
    def can_handle(self, task: Task) -> bool:
        """Check if this skill can handle the task"""
        return task.type in [
            "reminder.create_reminder",
            "reminder.send_reminders",
            "reminder.list_upcoming_reminders",
        ]
    
    def run(self, task: Task, context: SkillContext) -> TaskResult:
        """Execute the reminder operation"""
        try:
            task_type = task.type
            
            if task_type == "reminder.create_reminder":
                return self._handle_create_reminder(task, context)
            elif task_type == "reminder.send_reminders":
                return self._handle_send_reminders(task, context)
            elif task_type == "reminder.list_upcoming_reminders":
                return self._handle_list_upcoming_reminders(task, context)
            else:
                return TaskResult(
                    task_id=task.id,
                    success=False,
                    message=f"Unknown task type: {task_type}"
                )
        except Exception as e:
            logger.error(f"Error in ReminderSkill: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error with reminders: {str(e)}"
            )
    
    def _handle_create_reminder(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle creating a reminder"""
        payload = task.payload or {}
        reminder_type = payload.get("type")  # task, bill, event
        item_id = payload.get("item_id")
        reminder_minutes = payload.get("reminder_minutes", [15, 60])  # Default: 15 min and 1 hour
        
        if not reminder_type or not item_id:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required fields: 'type' and 'item_id'"
            )
        
        # Create reminder based on type
        if reminder_type == "task":
            # Get task and create reminder
            try:
                with httpx.Client(timeout=10.0) as client:
                    task_response = client.get(f"{self.life_os_api_url}/life_os/tasks/{item_id}")
                    
                    if task_response.status_code == 200:
                        task_data = task_response.json()
                        due_date_str = task_data.get("due_date")
                        
                        if due_date_str:
                            due_date = datetime.fromisoformat(due_date_str.replace("Z", "+00:00"))
                            
                            # Create reminder tasks for each reminder_minutes
                            actions = []
                            for minutes in reminder_minutes:
                                reminder_time = due_date - timedelta(minutes=minutes)
                                if reminder_time > datetime.utcnow():
                                    actions.append({
                                        "type": "otto.log",
                                        "tier": 0,
                                        "payload": {
                                            "message": f"Reminder: {task_data.get('title')} is due in {minutes} minutes",
                                            "level": "info"
                                        }
                                    })
                            
                            return TaskResult(
                                task_id=task.id,
                                success=True,
                                message=f"Created {len(actions)} reminder(s) for task #{item_id}",
                                actions=actions if actions else None
                            )
                        else:
                            return TaskResult(
                                task_id=task.id,
                                success=False,
                                message="Task has no due date"
                            )
                    else:
                        return TaskResult(
                            task_id=task.id,
                            success=False,
                            message=f"Task #{item_id} not found"
                        )
            except Exception as e:
                return TaskResult(
                    task_id=task.id,
                    success=False,
                    message=f"Error creating task reminder: {str(e)}"
                )
        
        elif reminder_type == "bill":
            # Bill reminders are handled by BillReminderSkill
            # This can create a log reminder
            actions = [{
                "type": "otto.log",
                "tier": 0,
                "payload": {
                    "message": f"Reminder: Bill #{item_id} is due soon",
                    "level": "info"
                }
            }]
            
            return TaskResult(
                task_id=task.id,
                success=True,
                message=f"Created reminder for bill #{item_id}",
                actions=actions
            )
        
        elif reminder_type == "event":
            # Get event and create reminder
            try:
                with httpx.Client(timeout=10.0) as client:
                    event_response = client.get(f"{self.life_os_api_url}/calendar/{item_id}")
                    
                    if event_response.status_code == 200:
                        event_data = event_response.json()
                        start_time_str = event_data.get("start_time")
                        
                        if start_time_str:
                            start_time = datetime.fromisoformat(start_time_str.replace("Z", "+00:00"))
                            
                            # Create reminder tasks
                            actions = []
                            for minutes in reminder_minutes:
                                reminder_time = start_time - timedelta(minutes=minutes)
                                if reminder_time > datetime.utcnow():
                                    actions.append({
                                        "type": "otto.log",
                                        "tier": 0,
                                        "payload": {
                                            "message": f"Reminder: {event_data.get('title')} starts in {minutes} minutes",
                                            "level": "info"
                                        }
                                    })
                            
                            return TaskResult(
                                task_id=task.id,
                                success=True,
                                message=f"Created {len(actions)} reminder(s) for event #{item_id}",
                                actions=actions if actions else None
                            )
                        else:
                            return TaskResult(
                                task_id=task.id,
                                success=False,
                                message="Event has no start time"
                            )
                    else:
                        return TaskResult(
                            task_id=task.id,
                            success=False,
                            message=f"Event #{item_id} not found"
                        )
            except Exception as e:
                return TaskResult(
                    task_id=task.id,
                    success=False,
                    message=f"Error creating event reminder: {str(e)}"
                )
        else:
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Unknown reminder type: {reminder_type}"
            )
    
    def _handle_send_reminders(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle sending reminders (checks what's due soon)"""
        payload = task.payload or {}
        minutes_ahead = payload.get("minutes_ahead", 60)  # Default: 1 hour ahead
        
        # Find items that need reminders
        reminders_sent = []
        
        try:
            now = datetime.utcnow()
            reminder_window = now + timedelta(minutes=minutes_ahead)
            
            # Check tasks due soon
            with httpx.Client(timeout=10.0) as client:
                tasks_response = client.get(
                    f"{self.life_os_api_url}/life_os/tasks",
                    params={"limit": 100}
                )
                
                if tasks_response.status_code == 200:
                    tasks = tasks_response.json()
                    for t in tasks:
                        due_date_str = t.get("due_date")
                        if due_date_str and t.get("status") != "done":
                            try:
                                due_date = datetime.fromisoformat(due_date_str.replace("Z", "+00:00"))
                                if now <= due_date <= reminder_window:
                                    reminders_sent.append({
                                        "type": "task",
                                        "id": t.get("id"),
                                        "title": t.get("title"),
                                        "due_date": due_date_str
                                    })
                            except:
                                pass
                
                # Check bills due soon
                bills_response = client.get(
                    f"{self.life_os_api_url}/bills",
                    params={"paid": "no", "limit": 100}
                )
                
                if bills_response.status_code == 200:
                    bills = bills_response.json()
                    for b in bills:
                        due_date_str = b.get("due_date")
                        if due_date_str:
                            try:
                                due_date = datetime.fromisoformat(due_date_str.replace("Z", "+00:00"))
                                if now <= due_date <= reminder_window:
                                    reminders_sent.append({
                                        "type": "bill",
                                        "id": b.get("id"),
                                        "name": b.get("name"),
                                        "due_date": due_date_str
                                    })
                            except:
                                pass
                
                # Check events starting soon
                events_response = client.get(
                    f"{self.life_os_api_url}/calendar",
                    params={"limit": 100}
                )
                
                if events_response.status_code == 200:
                    events = events_response.json()
                    for e in events:
                        start_time_str = e.get("start_time")
                        if start_time_str and e.get("status") != "cancelled":
                            try:
                                start_time = datetime.fromisoformat(start_time_str.replace("Z", "+00:00"))
                                if now <= start_time <= reminder_window:
                                    reminders_sent.append({
                                        "type": "event",
                                        "id": e.get("id"),
                                        "title": e.get("title"),
                                        "start_time": start_time_str
                                    })
                            except:
                                pass
            
            message = f"Found {len(reminders_sent)} item(s) needing reminders in next {minutes_ahead} minutes"
            
            # Create log actions for each reminder
            actions = []
            for reminder in reminders_sent:
                if reminder["type"] == "task":
                    actions.append({
                        "type": "otto.log",
                        "tier": 0,
                        "payload": {
                            "message": f"Reminder: Task '{reminder['title']}' is due soon",
                            "level": "info"
                        }
                    })
                elif reminder["type"] == "bill":
                    actions.append({
                        "type": "otto.log",
                        "tier": 0,
                        "payload": {
                            "message": f"Reminder: Bill '{reminder['name']}' is due soon",
                            "level": "info"
                        }
                    })
                elif reminder["type"] == "event":
                    actions.append({
                        "type": "otto.log",
                        "tier": 0,
                        "payload": {
                            "message": f"Reminder: Event '{reminder['title']}' starts soon",
                            "level": "info"
                        }
                    })
            
            return TaskResult(
                task_id=task.id,
                success=True,
                message=message,
                data={"reminders": reminders_sent, "count": len(reminders_sent)},
                actions=actions if actions else None
            )
        except Exception as e:
            logger.error(f"Error sending reminders: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error sending reminders: {str(e)}"
            )
    
    def _handle_list_upcoming_reminders(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle listing upcoming reminders"""
        payload = task.payload or {}
        hours_ahead = payload.get("hours_ahead", 24)  # Default: next 24 hours
        
        # Similar to send_reminders but just list, don't send
        try:
            now = datetime.utcnow()
            reminder_window = now + timedelta(hours=hours_ahead)
            
            upcoming_reminders = []
            
            with httpx.Client(timeout=10.0) as client:
                # Get tasks
                tasks_response = client.get(
                    f"{self.life_os_api_url}/life_os/tasks",
                    params={"limit": 100}
                )
                
                if tasks_response.status_code == 200:
                    tasks = tasks_response.json()
                    for t in tasks:
                        due_date_str = t.get("due_date")
                        if due_date_str and t.get("status") != "done":
                            try:
                                due_date = datetime.fromisoformat(due_date_str.replace("Z", "+00:00"))
                                if now <= due_date <= reminder_window:
                                    upcoming_reminders.append({
                                        "type": "task",
                                        "id": t.get("id"),
                                        "title": t.get("title"),
                                        "due_date": due_date_str,
                                        "priority": t.get("priority")
                                    })
                            except:
                                pass
                
                # Get bills
                bills_response = client.get(
                    f"{self.life_os_api_url}/bills",
                    params={"paid": "no", "limit": 100}
                )
                
                if bills_response.status_code == 200:
                    bills = bills_response.json()
                    for b in bills:
                        due_date_str = b.get("due_date")
                        if due_date_str:
                            try:
                                due_date = datetime.fromisoformat(due_date_str.replace("Z", "+00:00"))
                                if now <= due_date <= reminder_window:
                                    upcoming_reminders.append({
                                        "type": "bill",
                                        "id": b.get("id"),
                                        "name": b.get("name"),
                                        "due_date": due_date_str,
                                        "amount": b.get("amount")
                                    })
                            except:
                                pass
                
                # Get events
                events_response = client.get(
                    f"{self.life_os_api_url}/calendar",
                    params={"limit": 100}
                )
                
                if events_response.status_code == 200:
                    events = events_response.json()
                    for e in events:
                        start_time_str = e.get("start_time")
                        if start_time_str and e.get("status") != "cancelled":
                            try:
                                start_time = datetime.fromisoformat(start_time_str.replace("Z", "+00:00"))
                                if now <= start_time <= reminder_window:
                                    upcoming_reminders.append({
                                        "type": "event",
                                        "id": e.get("id"),
                                        "title": e.get("title"),
                                        "start_time": start_time_str,
                                        "location": e.get("location")
                                    })
                            except:
                                pass
            
            # Sort by date
            upcoming_reminders.sort(key=lambda x: x.get("due_date") or x.get("start_time", ""))
            
            message = f"Found {len(upcoming_reminders)} upcoming reminder(s) in next {hours_ahead} hours"
            
            return TaskResult(
                task_id=task.id,
                success=True,
                message=message,
                data={"reminders": upcoming_reminders, "count": len(upcoming_reminders)}
            )
        except Exception as e:
            logger.error(f"Error listing upcoming reminders: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error listing upcoming reminders: {str(e)}"
            )
    
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

