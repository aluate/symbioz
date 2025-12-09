"""
TransactionSkill - Tracks and categorizes transactions
Phase 3 — CONTROL_OTTO_PHASE3.md
Implements:
- Transaction CRUD operations
- Transaction categorization
- Transaction filtering and summarization
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


class TransactionSkill:
    """Skill that tracks and categorizes transactions"""
    
    name = "transaction"
    description = "Tracks transactions: create, update, categorize, list, summarize by category"
    
    def __init__(self):
        # Life OS backend API URL
        self.life_os_api_url = os.getenv("LIFE_OS_API_URL", "http://localhost:8000")
    
    def can_handle(self, task: Task) -> bool:
        """Check if this skill can handle the task"""
        return task.type in [
            "transactions.create_transaction",
            "transactions.list_transactions",
            "transactions.update_transaction",
            "transactions.categorize_transaction",
            "transactions.summarize_by_category",
            "transactions.get_transaction",
        ]
    
    def run(self, task: Task, context: SkillContext) -> TaskResult:
        """Execute the transaction operation"""
        try:
            task_type = task.type
            
            if task_type == "transactions.create_transaction":
                return self._handle_create_transaction(task, context)
            elif task_type == "transactions.list_transactions":
                return self._handle_list_transactions(task, context)
            elif task_type == "transactions.update_transaction":
                return self._handle_update_transaction(task, context)
            elif task_type == "transactions.categorize_transaction":
                return self._handle_categorize_transaction(task, context)
            elif task_type == "transactions.summarize_by_category":
                return self._handle_summarize_by_category(task, context)
            elif task_type == "transactions.get_transaction":
                return self._handle_get_transaction(task, context)
            else:
                return TaskResult(
                    task_id=task.id,
                    success=False,
                    message=f"Unknown task type: {task_type}"
                )
        except Exception as e:
            logger.error(f"Error in TransactionSkill: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error managing transactions: {str(e)}"
            )
    
    def _handle_create_transaction(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle transaction creation"""
        payload = task.payload or {}
        
        # Create action for worker to execute (Tier 2 - tax-critical)
        actions = [{
            "type": "transactions.create_transaction",
            "tier": 2,
            "payload": {
                "date": payload.get("date"),
                "amount": payload.get("amount"),
                "vendor": payload.get("vendor"),
                "description": payload.get("description"),
                "tax_category": payload.get("tax_category"),
                "source": payload.get("source", "manual"),
                "source_id": payload.get("source_id"),
                "notes": payload.get("notes"),
                "tags": payload.get("tags"),
            }
        }]
        
        return TaskResult(
            task_id=task.id,
            success=True,
            message=f"Will create transaction: {payload.get('vendor', 'Unknown')} - {payload.get('amount', 'N/A')}",
            actions=actions
        )
    
    def _handle_list_transactions(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle transaction listing"""
        payload = task.payload or {}
        
        # Fetch transactions from Life OS API
        try:
            params = {}
            if payload.get("start_date"):
                params["start_date"] = payload.get("start_date")
            if payload.get("end_date"):
                params["end_date"] = payload.get("end_date")
            if payload.get("tax_category"):
                params["tax_category"] = payload.get("tax_category")
            if payload.get("vendor"):
                params["vendor"] = payload.get("vendor")
            if payload.get("source"):
                params["source"] = payload.get("source")
            params["limit"] = payload.get("limit", 50)
            
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    f"{self.life_os_api_url}/transactions",
                    params=params
                )
                
                if response.status_code == 200:
                    transactions = response.json()
                    message = f"Found {len(transactions)} transaction(s)"
                    if payload.get("tax_category"):
                        message += f" in category: {payload.get('tax_category')}"
                    
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=message,
                        data={"transactions": transactions, "count": len(transactions)}
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to fetch transactions: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error fetching transactions: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error fetching transactions: {str(e)}"
            )
    
    def _handle_update_transaction(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle transaction update"""
        payload = task.payload or {}
        transaction_id = payload.get("transaction_id")
        
        if not transaction_id:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required field: 'transaction_id'"
            )
        
        # Update via API
        try:
            update_data = {}
            if payload.get("date") is not None:
                update_data["date"] = payload.get("date")
            if payload.get("amount") is not None:
                update_data["amount"] = payload.get("amount")
            if payload.get("vendor") is not None:
                update_data["vendor"] = payload.get("vendor")
            if payload.get("description") is not None:
                update_data["description"] = payload.get("description")
            if payload.get("tax_category") is not None:
                update_data["tax_category"] = payload.get("tax_category")
            if payload.get("notes") is not None:
                update_data["notes"] = payload.get("notes")
            if payload.get("tags") is not None:
                update_data["tags"] = payload.get("tags")
            
            with httpx.Client(timeout=10.0) as client:
                response = client.patch(
                    f"{self.life_os_api_url}/transactions/{transaction_id}",
                    json=update_data
                )
                
                if response.status_code == 200:
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=f"Updated transaction #{transaction_id}"
                    )
                elif response.status_code == 404:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Transaction #{transaction_id} not found"
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to update transaction: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error updating transaction: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error updating transaction: {str(e)}"
            )
    
    def _handle_categorize_transaction(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle transaction categorization"""
        payload = task.payload or {}
        transaction_id = payload.get("transaction_id")
        tax_category = payload.get("tax_category")
        
        if not transaction_id or not tax_category:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required fields: 'transaction_id' and 'tax_category'"
            )
        
        # Use update_transaction with tax_category
        return self._handle_update_transaction(
            Task(
                id=task.id,
                type="transactions.update_transaction",
                payload={
                    "transaction_id": transaction_id,
                    "tax_category": tax_category
                }
            ),
            context
        )
    
    def _handle_summarize_by_category(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle transaction summarization by category"""
        payload = task.payload or {}
        start_date = payload.get("start_date")
        end_date = payload.get("end_date")
        
        # Use the summary endpoint
        try:
            params = {}
            if start_date:
                params["start_date"] = start_date
            if end_date:
                params["end_date"] = end_date
            
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    f"{self.life_os_api_url}/transactions/summary/by_category",
                    params=params
                )
                
                if response.status_code == 200:
                    summary = response.json()
                    message = f"Transaction Summary: {summary.get('count', 0)} transactions, Total: {summary.get('total', 'N/A')}"
                    
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
                        message=f"Failed to fetch transaction summary: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error summarizing transactions: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error summarizing transactions: {str(e)}"
            )
    
    def _handle_get_transaction(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle getting a single transaction by ID"""
        payload = task.payload or {}
        transaction_id = payload.get("transaction_id")
        
        if not transaction_id:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required field: 'transaction_id'"
            )
        
        # Fetch transaction from API
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    f"{self.life_os_api_url}/transactions/{transaction_id}"
                )
                
                if response.status_code == 200:
                    transaction_data = response.json()
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=f"Retrieved transaction #{transaction_id}: {transaction_data.get('vendor', 'Unknown')} - {transaction_data.get('amount', 'N/A')}",
                        data={"transaction": transaction_data}
                    )
                elif response.status_code == 404:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Transaction #{transaction_id} not found"
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to fetch transaction: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error fetching transaction: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error fetching transaction: {str(e)}"
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

