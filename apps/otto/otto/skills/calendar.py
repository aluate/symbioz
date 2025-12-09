"""
CalendarSkill - Manages calendar events and reminders
Phase 3 — CONTROL_OTTO_PHASE3.md
Implements:
- Calendar event CRUD operations
- Upcoming events and conflict detection
- Reminder creation
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


class CalendarSkill:
    """Skill that manages calendar events"""
    
    name = "calendar"
    description = "Manages calendar events: create, update, list, find upcoming, detect conflicts"
    
    def __init__(self):
        # Life OS backend API URL
        self.life_os_api_url = os.getenv("LIFE_OS_API_URL", "http://localhost:8000")
    
    def can_handle(self, task: Task) -> bool:
        """Check if this skill can handle the task"""
        return task.type in [
            "calendar.create_event",
            "calendar.list_events",
            "calendar.update_event",
            "calendar.delete_event",
            "calendar.find_upcoming",
            "calendar.find_conflicts",
            "calendar.create_reminder",
            "calendar.get_event",
        ]
    
    def run(self, task: Task, context: SkillContext) -> TaskResult:
        """Execute the calendar operation"""
        try:
            task_type = task.type
            
            if task_type == "calendar.create_event":
                return self._handle_create_event(task, context)
            elif task_type == "calendar.list_events":
                return self._handle_list_events(task, context)
            elif task_type == "calendar.update_event":
                return self._handle_update_event(task, context)
            elif task_type == "calendar.delete_event":
                return self._handle_delete_event(task, context)
            elif task_type == "calendar.find_upcoming":
                return self._handle_find_upcoming(task, context)
            elif task_type == "calendar.find_conflicts":
                return self._handle_find_conflicts(task, context)
            elif task_type == "calendar.create_reminder":
                return self._handle_create_reminder(task, context)
            elif task_type == "calendar.get_event":
                return self._handle_get_event(task, context)
            else:
                return TaskResult(
                    task_id=task.id,
                    success=False,
                    message=f"Unknown task type: {task_type}"
                )
        except Exception as e:
            logger.error(f"Error in CalendarSkill: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error managing calendar: {str(e)}"
            )
    
    def _handle_create_event(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle event creation"""
        payload = task.payload or {}
        
        # Create action for worker to execute (Tier 2 - affects scheduling)
        actions = [{
            "type": "calendar.create_event",
            "tier": 2,
            "payload": {
                "title": payload.get("title"),
                "description": payload.get("description"),
                "start_time": payload.get("start_time"),
                "end_time": payload.get("end_time"),
                "location": payload.get("location"),
                "attendees": payload.get("attendees"),
                "category": payload.get("category"),
                "is_recurring": payload.get("is_recurring", "no"),
                "recurrence_frequency": payload.get("recurrence_frequency"),
                "reminders": payload.get("reminders"),
            }
        }]
        
        return TaskResult(
            task_id=task.id,
            success=True,
            message=f"Will create calendar event: {payload.get('title', 'Untitled')}",
            actions=actions
        )
    
    def _handle_list_events(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle event listing"""
        payload = task.payload or {}
        
        # Fetch events from Life OS API
        try:
            params = {}
            if payload.get("start_date"):
                params["start_date"] = payload.get("start_date")
            if payload.get("end_date"):
                params["end_date"] = payload.get("end_date")
            if payload.get("category"):
                params["category"] = payload.get("category")
            if payload.get("status"):
                params["status"] = payload.get("status")
            params["limit"] = payload.get("limit", 50)
            
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    f"{self.life_os_api_url}/calendar",
                    params=params
                )
                
                if response.status_code == 200:
                    events = response.json()
                    message = f"Found {len(events)} event(s)"
                    if payload.get("start_date"):
                        message += f" from {payload.get('start_date')}"
                    
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=message,
                        data={"events": events, "count": len(events)}
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to fetch events: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error fetching events: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error fetching events: {str(e)}"
            )
    
    def _handle_update_event(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle event update"""
        payload = task.payload or {}
        event_id = payload.get("event_id")
        
        if not event_id:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required field: 'event_id'"
            )
        
        # Create action for worker to execute (Tier 2)
        actions = [{
            "type": "calendar.update_event",
            "tier": 2,
            "payload": {
                "event_id": event_id,
                "title": payload.get("title"),
                "description": payload.get("description"),
                "start_time": payload.get("start_time"),
                "end_time": payload.get("end_time"),
                "location": payload.get("location"),
                "attendees": payload.get("attendees"),
                "category": payload.get("category"),
                "status": payload.get("status"),
                "reminders": payload.get("reminders"),
            }
        }]
        
        return TaskResult(
            task_id=task.id,
            success=True,
            message=f"Will update calendar event #{event_id}",
            actions=actions
        )
    
    def _handle_delete_event(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle event deletion"""
        payload = task.payload or {}
        event_id = payload.get("event_id")
        
        if not event_id:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required field: 'event_id'"
            )
        
        # Delete via API (Tier 2 - affects scheduling)
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.delete(
                    f"{self.life_os_api_url}/calendar/{event_id}"
                )
                
                if response.status_code == 200:
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=f"Deleted calendar event #{event_id}"
                    )
                elif response.status_code == 404:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Event #{event_id} not found"
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to delete event: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error deleting event: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error deleting event: {str(e)}"
            )
    
    def _handle_find_upcoming(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle finding upcoming events"""
        payload = task.payload or {}
        days = payload.get("days", 7)
        
        # Use the upcoming endpoint
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    f"{self.life_os_api_url}/calendar/upcoming",
                    params={"days": days}
                )
                
                if response.status_code == 200:
                    events = response.json()
                    message = f"Found {len(events)} upcoming event(s) in next {days} days"
                    
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=message,
                        data={"events": events, "count": len(events), "days": days}
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to fetch upcoming events: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error fetching upcoming events: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error fetching upcoming events: {str(e)}"
            )
    
    def _handle_find_conflicts(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle finding scheduling conflicts"""
        payload = task.payload or {}
        start_time = payload.get("start_time")
        end_time = payload.get("end_time")
        
        if not start_time or not end_time:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required fields: 'start_time' and 'end_time'"
            )
        
        # Parse times
        try:
            if isinstance(start_time, str):
                start_time = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
            if isinstance(end_time, str):
                end_time = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
        except Exception as e:
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Invalid time format: {str(e)}"
            )
        
        # Fetch events in the time range
        try:
            params = {
                "start_date": start_time.isoformat(),
                "end_date": end_time.isoformat(),
                "limit": 100
            }
            
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    f"{self.life_os_api_url}/calendar",
                    params=params
                )
                
                if response.status_code == 200:
                    all_events = response.json()
                    
                    # Find conflicts (events that overlap)
                    conflicts = []
                    for event in all_events:
                        event_start_str = event.get("start_time")
                        event_end_str = event.get("end_time")
                        
                        if event_start_str:
                            try:
                                event_start = datetime.fromisoformat(event_start_str.replace("Z", "+00:00"))
                                event_end = event_end_str
                                if event_end:
                                    event_end = datetime.fromisoformat(event_end.replace("Z", "+00:00"))
                                else:
                                    # Default 1 hour if no end time
                                    event_end = event_start + timedelta(hours=1)
                                
                                # Check for overlap
                                if not (event_end < start_time or event_start > end_time):
                                    conflicts.append(event)
                            except:
                                pass
                    
                    message = f"Found {len(conflicts)} conflicting event(s)"
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=message,
                        data={"conflicts": conflicts, "count": len(conflicts)}
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to check conflicts: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error finding conflicts: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error finding conflicts: {str(e)}"
            )
    
    def _handle_create_reminder(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle creating a reminder (creates event with reminder)"""
        payload = task.payload or {}
        
        # Create a calendar event with reminders
        reminder_minutes = payload.get("reminder_minutes", [15, 60])  # Default: 15 min and 1 hour
        if isinstance(reminder_minutes, int):
            reminder_minutes = [reminder_minutes]
        
        reminders = [{"minutes": m} for m in reminder_minutes]
        
        # Use create_event with reminders
        return self._handle_create_event(
            Task(
                id=task.id,
                type="calendar.create_event",
                payload={
                    **payload,
                    "reminders": reminders,
                    "title": payload.get("title", "Reminder")
                }
            ),
            context
        )
    
    def _handle_get_event(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle getting a single event by ID"""
        payload = task.payload or {}
        event_id = payload.get("event_id")
        
        if not event_id:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required field: 'event_id'"
            )
        
        # Fetch event from API
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    f"{self.life_os_api_url}/calendar/{event_id}"
                )
                
                if response.status_code == 200:
                    event_data = response.json()
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=f"Retrieved event #{event_id}: {event_data.get('title')}",
                        data={"event": event_data}
                    )
                elif response.status_code == 404:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Event #{event_id} not found"
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to fetch event: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error fetching event: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error fetching event: {str(e)}"
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

