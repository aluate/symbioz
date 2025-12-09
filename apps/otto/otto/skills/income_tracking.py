"""
IncomeTrackingSkill - Tracks income sources and amounts
Phase 3 — CONTROL_OTTO_PHASE3.md
Implements:
- Income CRUD operations
- Income filtering and summarization
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


class IncomeTrackingSkill:
    """Skill that tracks income"""
    
    name = "income_tracking"
    description = "Tracks income sources: create, update, list, summarize by period"
    
    def __init__(self):
        # Life OS backend API URL
        self.life_os_api_url = os.getenv("LIFE_OS_API_URL", "http://localhost:8000")
    
    def can_handle(self, task: Task) -> bool:
        """Check if this skill can handle the task"""
        return task.type in [
            "income.create_income",
            "income.list_income",
            "income.update_income",
            "income.summarize_income",
            "income.by_period",
            "income.get_income",
        ]
    
    def run(self, task: Task, context: SkillContext) -> TaskResult:
        """Execute the income tracking operation"""
        try:
            task_type = task.type
            
            if task_type == "income.create_income":
                return self._handle_create_income(task, context)
            elif task_type == "income.list_income":
                return self._handle_list_income(task, context)
            elif task_type == "income.update_income":
                return self._handle_update_income(task, context)
            elif task_type == "income.summarize_income":
                return self._handle_summarize_income(task, context)
            elif task_type == "income.by_period":
                return self._handle_by_period(task, context)
            elif task_type == "income.get_income":
                return self._handle_get_income(task, context)
            else:
                return TaskResult(
                    task_id=task.id,
                    success=False,
                    message=f"Unknown task type: {task_type}"
                )
        except Exception as e:
            logger.error(f"Error in IncomeTrackingSkill: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error tracking income: {str(e)}"
            )
    
    def _handle_create_income(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle income creation"""
        payload = task.payload or {}
        
        # Create action for worker to execute (Tier 2 - financial state)
        actions = [{
            "type": "income.create_income",
            "tier": 2,
            "payload": {
                "source": payload.get("source"),
                "amount": payload.get("amount"),
                "received_date": payload.get("received_date"),
                "category": payload.get("category"),
                "notes": payload.get("notes"),
                "is_recurring": payload.get("is_recurring", "no"),
                "recurrence_frequency": payload.get("recurrence_frequency"),
            }
        }]
        
        return TaskResult(
            task_id=task.id,
            success=True,
            message=f"Will create income entry: {payload.get('source', 'Unknown')} - {payload.get('amount', 'N/A')}",
            actions=actions
        )
    
    def _handle_list_income(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle income listing"""
        payload = task.payload or {}
        
        # Fetch income from Life OS API
        try:
            params = {}
            if payload.get("category"):
                params["category"] = payload.get("category")
            if payload.get("source"):
                params["source"] = payload.get("source")
            if payload.get("start_date"):
                params["start_date"] = payload.get("start_date")
            if payload.get("end_date"):
                params["end_date"] = payload.get("end_date")
            params["limit"] = payload.get("limit", 50)
            
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    f"{self.life_os_api_url}/income",
                    params=params
                )
                
                if response.status_code == 200:
                    income_list = response.json()
                    message = f"Found {len(income_list)} income entry/entries"
                    if payload.get("category"):
                        message += f" in category: {payload.get('category')}"
                    
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=message,
                        data={"income": income_list, "count": len(income_list)}
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to fetch income: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error fetching income: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error fetching income: {str(e)}"
            )
    
    def _handle_update_income(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle income update"""
        payload = task.payload or {}
        income_id = payload.get("income_id")
        
        if not income_id:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required field: 'income_id'"
            )
        
        # Update via API
        try:
            update_data = {}
            if payload.get("source") is not None:
                update_data["source"] = payload.get("source")
            if payload.get("amount") is not None:
                update_data["amount"] = payload.get("amount")
            if payload.get("received_date") is not None:
                update_data["received_date"] = payload.get("received_date")
            if payload.get("category") is not None:
                update_data["category"] = payload.get("category")
            if payload.get("notes") is not None:
                update_data["notes"] = payload.get("notes")
            if payload.get("is_recurring") is not None:
                update_data["is_recurring"] = payload.get("is_recurring")
            if payload.get("recurrence_frequency") is not None:
                update_data["recurrence_frequency"] = payload.get("recurrence_frequency")
            
            with httpx.Client(timeout=10.0) as client:
                response = client.patch(
                    f"{self.life_os_api_url}/income/{income_id}",
                    json=update_data
                )
                
                if response.status_code == 200:
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=f"Updated income entry #{income_id}"
                    )
                elif response.status_code == 404:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Income entry #{income_id} not found"
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to update income: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error updating income: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error updating income: {str(e)}"
            )
    
    def _handle_summarize_income(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle income summarization"""
        payload = task.payload or {}
        start_date = payload.get("start_date")
        end_date = payload.get("end_date")
        
        # Fetch all income in range
        try:
            params = {"limit": 500}
            if start_date:
                params["start_date"] = start_date
            if end_date:
                params["end_date"] = end_date
            
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    f"{self.life_os_api_url}/income",
                    params=params
                )
                
                if response.status_code == 200:
                    income_list = response.json()
                    
                    # Calculate summary
                    total = 0
                    by_category = {}
                    by_source = {}
                    
                    for inc in income_list:
                        amount_str = inc.get("amount", "0")
                        try:
                            amount = float(amount_str.replace("$", "").replace(",", ""))
                            total += amount
                        except:
                            pass
                        
                        category = inc.get("category") or "uncategorized"
                        by_category[category] = by_category.get(category, 0) + amount
                        
                        source = inc.get("source") or "unknown"
                        by_source[source] = by_source.get(source, 0) + amount
                    
                    summary = {
                        "total": f"${total:.2f}",
                        "count": len(income_list),
                        "by_category": {k: f"${v:.2f}" for k, v in by_category.items()},
                        "by_source": {k: f"${v:.2f}" for k, v in by_source.items()},
                    }
                    
                    message = f"Income Summary: {summary['count']} entries, Total: {summary['total']}"
                    
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
                        message=f"Failed to fetch income for summary: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error summarizing income: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error summarizing income: {str(e)}"
            )
    
    def _handle_by_period(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle income by period"""
        payload = task.payload or {}
        period = payload.get("period", "monthly")
        year = payload.get("year")
        
        # Use the summary endpoint
        try:
            params = {"period": period}
            if year:
                params["year"] = year
            
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    f"{self.life_os_api_url}/income/summary/by_period",
                    params=params
                )
                
                if response.status_code == 200:
                    summary = response.json()
                    message = f"Income for {period} period: {summary.get('total_amount', 'N/A')}"
                    
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
                        message=f"Failed to fetch income by period: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error fetching income by period: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error fetching income by period: {str(e)}"
            )
    
    def _handle_get_income(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle getting a single income entry by ID"""
        payload = task.payload or {}
        income_id = payload.get("income_id")
        
        if not income_id:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required field: 'income_id'"
            )
        
        # Fetch income from API
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    f"{self.life_os_api_url}/income/{income_id}"
                )
                
                if response.status_code == 200:
                    income_data = response.json()
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=f"Retrieved income #{income_id}: {income_data.get('source')} - {income_data.get('amount')}",
                        data={"income": income_data}
                    )
                elif response.status_code == 404:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Income entry #{income_id} not found"
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to fetch income: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error fetching income: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error fetching income: {str(e)}"
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

