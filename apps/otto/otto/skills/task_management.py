"""
TaskManagementSkill - Manages Life OS tasks (create, update, list, filter, summarize)
Phase 3 — CONTROL_OTTO_PHASE3.md
Implements:
- Task CRUD operations
- Task filtering and summarization
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


class TaskManagementSkill:
    """Skill that manages Life OS tasks"""
    
    name = "task_management"
    description = "Manages Life OS tasks: create, update, list, filter, and summarize tasks"
    
    def __init__(self):
        # Life OS backend API URL
        self.life_os_api_url = os.getenv("LIFE_OS_API_URL", "http://localhost:8000")
    
    def can_handle(self, task: Task) -> bool:
        """Check if this skill can handle the task"""
        return task.type in [
            "life_os.create_task",
            "life_os.list_tasks",
            "life_os.update_task",
            "life_os.delete_task",
            "life_os.summarize_tasks",
            "life_os.find_overdue",
            "life_os.find_by_category",
            "life_os.find_by_assignee",
            "life_os.get_task",
        ]
    
    def run(self, task: Task, context: SkillContext) -> TaskResult:
        """Execute the task management operation"""
        try:
            task_type = task.type
            
            if task_type == "life_os.create_task":
                return self._handle_create_task(task, context)
            elif task_type == "life_os.list_tasks":
                return self._handle_list_tasks(task, context)
            elif task_type == "life_os.update_task":
                return self._handle_update_task(task, context)
            elif task_type == "life_os.delete_task":
                return self._handle_delete_task(task, context)
            elif task_type == "life_os.summarize_tasks":
                return self._handle_summarize_tasks(task, context)
            elif task_type == "life_os.find_overdue":
                return self._handle_find_overdue(task, context)
            elif task_type == "life_os.find_by_category":
                return self._handle_find_by_category(task, context)
            elif task_type == "life_os.find_by_assignee":
                return self._handle_find_by_assignee(task, context)
            elif task_type == "life_os.get_task":
                return self._handle_get_task(task, context)
            else:
                return TaskResult(
                    task_id=task.id,
                    success=False,
                    message=f"Unknown task type: {task_type}"
                )
        except Exception as e:
            logger.error(f"Error in TaskManagementSkill: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error managing tasks: {str(e)}"
            )
    
    def _handle_create_task(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle task creation"""
        payload = task.payload or {}
        
        # Create action for worker to execute
        actions = [{
            "type": "life_os.create_task",
            "tier": 1,
            "payload": {
                "title": payload.get("title"),
                "description": payload.get("description"),
                "assignee": payload.get("assignee"),
                "due_date": payload.get("due_date"),
                "priority": payload.get("priority", "medium"),
                "category": payload.get("category"),
            }
        }]
        
        return TaskResult(
            task_id=task.id,
            success=True,
            message=f"Will create task: {payload.get('title', 'Untitled')}",
            actions=actions
        )
    
    def _handle_list_tasks(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle task listing"""
        payload = task.payload or {}
        
        # Fetch tasks from Life OS API
        try:
            params = {}
            if payload.get("status"):
                params["status"] = payload.get("status")
            if payload.get("assignee"):
                params["assignee"] = payload.get("assignee")
            if payload.get("category"):
                params["category"] = payload.get("category")
            params["limit"] = payload.get("limit", 50)
            
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    f"{self.life_os_api_url}/life_os/tasks",
                    params=params
                )
                
                if response.status_code == 200:
                    tasks = response.json()
                    message = f"Found {len(tasks)} task(s)"
                    if payload.get("status"):
                        message += f" with status: {payload.get('status')}"
                    
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=message,
                        data={"tasks": tasks, "count": len(tasks)}
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to fetch tasks: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error fetching tasks: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error fetching tasks: {str(e)}"
            )
    
    def _handle_update_task(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle task update"""
        payload = task.payload or {}
        task_id = payload.get("task_id")
        
        if not task_id:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required field: 'task_id'"
            )
        
        # Create action for worker to execute
        actions = [{
            "type": "life_os.update_task_status",
            "tier": 1,
            "payload": {
                "task_id": task_id,
                "title": payload.get("title"),
                "description": payload.get("description"),
                "status": payload.get("status"),
                "assignee": payload.get("assignee"),
                "due_date": payload.get("due_date"),
                "priority": payload.get("priority"),
                "category": payload.get("category"),
            }
        }]
        
        return TaskResult(
            task_id=task.id,
            success=True,
            message=f"Will update task #{task_id}",
            actions=actions
        )
    
    def _handle_delete_task(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle task deletion"""
        payload = task.payload or {}
        task_id = payload.get("task_id")
        
        if not task_id:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required field: 'task_id'"
            )
        
        # Delete via API
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.delete(
                    f"{self.life_os_api_url}/life_os/tasks/{task_id}"
                )
                
                if response.status_code == 200:
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=f"Deleted task #{task_id}"
                    )
                elif response.status_code == 404:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Task #{task_id} not found"
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to delete task: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error deleting task: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error deleting task: {str(e)}"
            )
    
    def _handle_summarize_tasks(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle task summarization"""
        payload = task.payload or {}
        
        # Fetch all tasks
        try:
            params = {"limit": 500}  # Get more for summary
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    f"{self.life_os_api_url}/life_os/tasks",
                    params=params
                )
                
                if response.status_code == 200:
                    tasks = response.json()
                    
                    # Calculate summary
                    total = len(tasks)
                    by_status = {}
                    by_assignee = {}
                    by_category = {}
                    overdue = 0
                    due_today = 0
                    due_this_week = 0
                    
                    now = datetime.utcnow()
                    week_from_now = now + timedelta(days=7)
                    
                    for t in tasks:
                        # By status
                        status = t.get("status", "unknown")
                        by_status[status] = by_status.get(status, 0) + 1
                        
                        # By assignee
                        assignee = t.get("assignee") or "unassigned"
                        by_assignee[assignee] = by_assignee.get(assignee, 0) + 1
                        
                        # By category
                        category = t.get("category") or "uncategorized"
                        by_category[category] = by_category.get(category, 0) + 1
                        
                        # Due date analysis
                        due_date_str = t.get("due_date")
                        if due_date_str:
                            try:
                                due_date = datetime.fromisoformat(due_date_str.replace("Z", "+00:00"))
                                if due_date < now:
                                    overdue += 1
                                elif due_date.date() == now.date():
                                    due_today += 1
                                elif due_date <= week_from_now:
                                    due_this_week += 1
                            except:
                                pass
                    
                    summary = {
                        "total": total,
                        "by_status": by_status,
                        "by_assignee": by_assignee,
                        "by_category": by_category,
                        "overdue": overdue,
                        "due_today": due_today,
                        "due_this_week": due_this_week,
                    }
                    
                    message = f"Task Summary: {total} total tasks"
                    if overdue > 0:
                        message += f", {overdue} overdue"
                    if due_today > 0:
                        message += f", {due_today} due today"
                    if due_this_week > 0:
                        message += f", {due_this_week} due this week"
                    
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=message,
                        data=summary
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to fetch tasks for summary: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error summarizing tasks: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error summarizing tasks: {str(e)}"
            )
    
    def _handle_find_overdue(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle finding overdue tasks"""
        # Fetch all tasks and filter
        try:
            params = {"limit": 500}
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    f"{self.life_os_api_url}/life_os/tasks",
                    params=params
                )
                
                if response.status_code == 200:
                    all_tasks = response.json()
                    now = datetime.utcnow()
                    
                    overdue_tasks = []
                    for t in all_tasks:
                        due_date_str = t.get("due_date")
                        if due_date_str:
                            try:
                                due_date = datetime.fromisoformat(due_date_str.replace("Z", "+00:00"))
                                if due_date < now and t.get("status") != "done":
                                    overdue_tasks.append(t)
                            except:
                                pass
                    
                    message = f"Found {len(overdue_tasks)} overdue task(s)"
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=message,
                        data={"tasks": overdue_tasks, "count": len(overdue_tasks)}
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to fetch tasks: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error finding overdue tasks: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error finding overdue tasks: {str(e)}"
            )
    
    def _handle_find_by_category(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle finding tasks by category"""
        payload = task.payload or {}
        category = payload.get("category")
        
        if not category:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required field: 'category'"
            )
        
        # Use list_tasks with category filter
        return self._handle_list_tasks(
            Task(
                id=task.id,
                type="life_os.list_tasks",
                payload={"category": category}
            ),
            context
        )
    
    def _handle_find_by_assignee(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle finding tasks by assignee"""
        payload = task.payload or {}
        assignee = payload.get("assignee")
        
        if not assignee:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required field: 'assignee'"
            )
        
        # Use list_tasks with assignee filter
        return self._handle_list_tasks(
            Task(
                id=task.id,
                type="life_os.list_tasks",
                payload={"assignee": assignee}
            ),
            context
        )
    
    def _handle_get_task(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle getting a single task by ID"""
        payload = task.payload or {}
        task_id = payload.get("task_id")
        
        if not task_id:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required field: 'task_id'"
            )
        
        # Fetch task from API
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    f"{self.life_os_api_url}/life_os/tasks/{task_id}"
                )
                
                if response.status_code == 200:
                    task_data = response.json()
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=f"Retrieved task #{task_id}: {task_data.get('title')}",
                        data={"task": task_data}
                    )
                elif response.status_code == 404:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Task #{task_id} not found"
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to fetch task: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error fetching task: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error fetching task: {str(e)}"
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

