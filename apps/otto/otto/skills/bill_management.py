"""
BillManagementSkill - Manages bills (create, update, mark paid, track history)
Phase 3 — CONTROL_OTTO_PHASE3.md
Implements:
- Bill CRUD operations
- Bill filtering and summarization
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


class BillManagementSkill:
    """Skill that manages bills"""
    
    name = "bill_management"
    description = "Manages bills: create, update, mark paid, list, find upcoming/overdue, summarize"
    
    def __init__(self):
        # Life OS backend API URL
        self.life_os_api_url = os.getenv("LIFE_OS_API_URL", "http://localhost:8000")
    
    def can_handle(self, task: Task) -> bool:
        """Check if this skill can handle the task"""
        return task.type in [
            "bills.create_bill",
            "bills.list_bills",
            "bills.update_bill",
            "bills.mark_paid",
            "bills.find_upcoming",
            "bills.find_overdue",
            "bills.summarize_bills",
            "bills.get_bill",
        ]
    
    def run(self, task: Task, context: SkillContext) -> TaskResult:
        """Execute the bill management operation"""
        try:
            task_type = task.type
            
            if task_type == "bills.create_bill":
                return self._handle_create_bill(task, context)
            elif task_type == "bills.list_bills":
                return self._handle_list_bills(task, context)
            elif task_type == "bills.update_bill":
                return self._handle_update_bill(task, context)
            elif task_type == "bills.mark_paid":
                return self._handle_mark_paid(task, context)
            elif task_type == "bills.find_upcoming":
                return self._handle_find_upcoming(task, context)
            elif task_type == "bills.find_overdue":
                return self._handle_find_overdue(task, context)
            elif task_type == "bills.summarize_bills":
                return self._handle_summarize_bills(task, context)
            elif task_type == "bills.get_bill":
                return self._handle_get_bill(task, context)
            else:
                return TaskResult(
                    task_id=task.id,
                    success=False,
                    message=f"Unknown task type: {task_type}"
                )
        except Exception as e:
            logger.error(f"Error in BillManagementSkill: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error managing bills: {str(e)}"
            )
    
    def _handle_create_bill(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle bill creation"""
        payload = task.payload or {}
        
        # Create action for worker to execute (Tier 2 - financial state)
        actions = [{
            "type": "bills.create",
            "tier": 2,
            "payload": {
                "name": payload.get("name"),
                "amount": payload.get("amount"),
                "due_date": payload.get("due_date"),
                "category": payload.get("category"),
                "payee": payload.get("payee"),
                "account_number": payload.get("account_number"),
                "notes": payload.get("notes"),
                "is_recurring": payload.get("is_recurring", "no"),
                "recurrence_frequency": payload.get("recurrence_frequency"),
            }
        }]
        
        return TaskResult(
            task_id=task.id,
            success=True,
            message=f"Will create bill: {payload.get('name', 'Untitled')}",
            actions=actions
        )
    
    def _handle_list_bills(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle bill listing"""
        payload = task.payload or {}
        
        # Fetch bills from Life OS API
        try:
            params = {}
            if payload.get("paid"):
                params["paid"] = payload.get("paid")
            if payload.get("category"):
                params["category"] = payload.get("category")
            if payload.get("upcoming"):
                params["upcoming"] = True
            if payload.get("overdue"):
                params["overdue"] = True
            params["limit"] = payload.get("limit", 50)
            
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    f"{self.life_os_api_url}/bills",
                    params=params
                )
                
                if response.status_code == 200:
                    bills = response.json()
                    message = f"Found {len(bills)} bill(s)"
                    if payload.get("paid"):
                        message += f" with paid status: {payload.get('paid')}"
                    
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=message,
                        data={"bills": bills, "count": len(bills)}
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to fetch bills: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error fetching bills: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error fetching bills: {str(e)}"
            )
    
    def _handle_update_bill(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle bill update"""
        payload = task.payload or {}
        bill_id = payload.get("bill_id")
        
        if not bill_id:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required field: 'bill_id'"
            )
        
        # Create action for worker to execute (Tier 2 - financial state)
        actions = [{
            "type": "bills.update",
            "tier": 2,
            "payload": {
                "bill_id": bill_id,
                "name": payload.get("name"),
                "amount": payload.get("amount"),
                "due_date": payload.get("due_date"),
                "paid": payload.get("paid"),
                "category": payload.get("category"),
                "payee": payload.get("payee"),
                "account_number": payload.get("account_number"),
                "notes": payload.get("notes"),
                "is_recurring": payload.get("is_recurring"),
                "recurrence_frequency": payload.get("recurrence_frequency"),
            }
        }]
        
        return TaskResult(
            task_id=task.id,
            success=True,
            message=f"Will update bill #{bill_id}",
            actions=actions
        )
    
    def _handle_mark_paid(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle marking bill as paid"""
        payload = task.payload or {}
        bill_id = payload.get("bill_id")
        
        if not bill_id:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required field: 'bill_id'"
            )
        
        # Create action for worker to execute (Tier 2 - financial state)
        actions = [{
            "type": "bills.mark_paid",
            "tier": 2,
            "payload": {
                "bill_id": bill_id,
                "paid": payload.get("paid", "yes")
            }
        }]
        
        return TaskResult(
            task_id=task.id,
            success=True,
            message=f"Will mark bill #{bill_id} as paid",
            actions=actions
        )
    
    def _handle_find_upcoming(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle finding upcoming bills"""
        payload = task.payload or {}
        days = payload.get("days", 30)
        
        # Fetch upcoming bills
        try:
            params = {
                "upcoming": True,
                "limit": 100
            }
            
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    f"{self.life_os_api_url}/bills",
                    params=params
                )
                
                if response.status_code == 200:
                    all_bills = response.json()
                    now = datetime.utcnow()
                    future_date = now + timedelta(days=days)
                    
                    upcoming_bills = []
                    for bill in all_bills:
                        due_date_str = bill.get("due_date")
                        if due_date_str:
                            try:
                                due_date = datetime.fromisoformat(due_date_str.replace("Z", "+00:00"))
                                if now <= due_date <= future_date and bill.get("paid") != "yes":
                                    upcoming_bills.append(bill)
                            except:
                                pass
                    
                    message = f"Found {len(upcoming_bills)} upcoming bill(s) in next {days} days"
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=message,
                        data={"bills": upcoming_bills, "count": len(upcoming_bills), "days": days}
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to fetch bills: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error finding upcoming bills: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error finding upcoming bills: {str(e)}"
            )
    
    def _handle_find_overdue(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle finding overdue bills"""
        # Fetch overdue bills
        try:
            params = {
                "overdue": True,
                "limit": 100
            }
            
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    f"{self.life_os_api_url}/bills",
                    params=params
                )
                
                if response.status_code == 200:
                    bills = response.json()
                    message = f"Found {len(bills)} overdue bill(s)"
                    
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=message,
                        data={"bills": bills, "count": len(bills)}
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to fetch bills: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error finding overdue bills: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error finding overdue bills: {str(e)}"
            )
    
    def _handle_summarize_bills(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle bill summarization"""
        payload = task.payload or {}
        days = payload.get("days", 30)
        
        # Use the summary endpoint
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    f"{self.life_os_api_url}/bills/upcoming/summary",
                    params={"days": days}
                )
                
                if response.status_code == 200:
                    summary = response.json()
                    message = f"Bill Summary: {summary.get('upcoming_count', 0)} upcoming, {summary.get('overdue_count', 0)} overdue"
                    if summary.get("total_amount"):
                        message += f", Total: {summary.get('total_amount')}"
                    
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
                        message=f"Failed to fetch bill summary: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error summarizing bills: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error summarizing bills: {str(e)}"
            )
    
    def _handle_get_bill(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle getting a single bill by ID"""
        payload = task.payload or {}
        bill_id = payload.get("bill_id")
        
        if not bill_id:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required field: 'bill_id'"
            )
        
        # Fetch bill from API
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    f"{self.life_os_api_url}/bills/{bill_id}"
                )
                
                if response.status_code == 200:
                    bill_data = response.json()
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=f"Retrieved bill #{bill_id}: {bill_data.get('name')}",
                        data={"bill": bill_data}
                    )
                elif response.status_code == 404:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Bill #{bill_id} not found"
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to fetch bill: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error fetching bill: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error fetching bill: {str(e)}"
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

