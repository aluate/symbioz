"""
TaxBrainSkill - Integrates with Tax Brain module for tax categorization and reporting
Phase 3 — CONTROL_OTTO_PHASE3.md
Implements:
- Transaction categorization
- Tax report generation
- Deduction finding
- Category summarization
- Integration with Tax Brain module
"""

from typing import List, Dict, Any, Optional
import os
import httpx
from datetime import datetime

from ..core.models import Task, TaskResult, TaskStatus
from ..core.skill_base import Skill, SkillHealthIssue, SkillContext
from ..core.logging_utils import get_logger
from .memory_helpers import get_vendor_hint

logger = get_logger(__name__)


class TaxBrainSkill:
    """Skill that integrates with Tax Brain module"""
    
    name = "tax_brain"
    description = "Integrates with Tax Brain: categorize transactions, generate reports, find deductions"
    
    def __init__(self):
        # Life OS backend API URL
        self.life_os_api_url = os.getenv("LIFE_OS_API_URL", "http://localhost:8000")
    
    def can_handle(self, task: Task) -> bool:
        """Check if this skill can handle the task"""
        return task.type in [
            "tax.categorize_transaction",
            "tax.generate_report",
            "tax.find_deductions",
            "tax.summarize_by_category",
            "tax.update_category",
            "tax.get_categories",
        ]
    
    def run(self, task: Task, context: SkillContext) -> TaskResult:
        """Execute the tax brain operation"""
        try:
            task_type = task.type
            
            if task_type == "tax.categorize_transaction":
                return self._handle_categorize_transaction(task, context)
            elif task_type == "tax.generate_report":
                return self._handle_generate_report(task, context)
            elif task_type == "tax.find_deductions":
                return self._handle_find_deductions(task, context)
            elif task_type == "tax.summarize_by_category":
                return self._handle_summarize_by_category(task, context)
            elif task_type == "tax.update_category":
                return self._handle_update_category(task, context)
            elif task_type == "tax.get_categories":
                return self._handle_get_categories(task, context)
            else:
                return TaskResult(
                    task_id=task.id,
                    success=False,
                    message=f"Unknown task type: {task_type}"
                )
        except Exception as e:
            logger.error(f"Error in TaxBrainSkill: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error with tax brain: {str(e)}"
            )
    
    def _handle_categorize_transaction(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle transaction categorization"""
        payload = task.payload or {}
        transaction_id = payload.get("transaction_id")
        
        if not transaction_id:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required field: 'transaction_id'"
            )
        
        # Track reasoning and evidence
        reasoning_steps = []
        evidence = {
            "transactions": [transaction_id],
            "categories": [],
            "rules": [],
            "memory_ids": []
        }
        
        # First get the transaction
        try:
            with httpx.Client(timeout=10.0) as client:
                # Get transaction
                txn_response = client.get(
                    f"{self.life_os_api_url}/transactions/{transaction_id}"
                )
                
                if txn_response.status_code != 200:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Transaction #{transaction_id} not found"
                    )
                
                transaction = txn_response.json()
                reasoning_steps.append({
                    "id": "step1",
                    "type": "fetch",
                    "summary": f"Retrieved transaction #{transaction_id}",
                    "evidence": [{"kind": "transaction", "id": transaction_id}]
                })
                
                # Get available categories
                categories_response = client.get(
                    f"{self.life_os_api_url}/categories",
                    params={"limit": 100}
                )
                
                available_categories = []
                if categories_response.status_code == 200:
                    available_categories = categories_response.json()
                    evidence["categories"] = [c.get("id") for c in available_categories]
                
                # Phase 3B: Lookup vendor hint from memory
                vendor_name = transaction.get("vendor", "")
                vendor_hint_category, vendor_hint_memory_id, vendor_hint_memory = None, None, None
                if vendor_name:
                    vendor_hint_category, vendor_hint_memory_id, vendor_hint_memory = get_vendor_hint(
                        self.life_os_api_url,
                        vendor_name
                    )
                    if vendor_hint_memory_id:
                        reasoning_steps.append({
                            "id": "step1b",
                            "type": "lookup",
                            "summary": f"Found vendor hint for '{vendor_name}': category {vendor_hint_category} (Memory ID: {vendor_hint_memory_id})",
                            "evidence": [{"kind": "memory", "id": vendor_hint_memory_id, "vendor": vendor_name, "category": vendor_hint_category}]
                        })
                        evidence["memory_ids"] = evidence.get("memory_ids", []) + [vendor_hint_memory_id]
                
                # Categorize using Tax Brain
                categorize_response = client.post(
                    f"{self.life_os_api_url}/tax/transactions/categorize",
                    json={
                        "date": transaction.get("date"),
                        "amount": transaction.get("amount"),
                        "vendor": transaction.get("vendor"),
                        "description": transaction.get("description"),
                        "user_id": context.config.get("user_id", 1) if hasattr(context, "config") else 1
                    }
                )
                
                if categorize_response.status_code == 200:
                    categorized = categorize_response.json()
                    tax_category_code = categorized.get("tax_category") or categorized.get("category")
                    
                    # Phase 3B: Use vendor hint if available, otherwise use Tax Brain suggestion
                    if vendor_hint_category:
                        # Verify vendor hint category exists in database
                        matching_category = None
                        for cat in available_categories:
                            if cat.get("code") == vendor_hint_category:
                                matching_category = cat
                                break
                        
                        if matching_category:
                            tax_category_code = vendor_hint_category
                            reasoning_steps.append({
                                "id": "step2",
                                "type": "hint_application",
                                "summary": f"Applied vendor hint category: {tax_category_code} (from memory)",
                                "evidence": [{"kind": "vendor_hint", "category": tax_category_code, "memory_id": vendor_hint_memory_id}]
                            })
                        else:
                            reasoning_steps.append({
                                "id": "step2",
                                "type": "hint_validation",
                                "summary": f"Vendor hint category {vendor_hint_category} not found in database, using Tax Brain suggestion",
                                "evidence": [{"kind": "hint_invalid", "category": vendor_hint_category}]
                            })
                            reasoning_steps.append({
                                "id": "step2b",
                                "type": "categorization",
                                "summary": f"Tax Brain suggested category: {tax_category_code}",
                                "evidence": [{"kind": "tax_brain_result", "category": tax_category_code}]
                            })
                    else:
                        reasoning_steps.append({
                            "id": "step2",
                            "type": "categorization",
                            "summary": f"Tax Brain suggested category: {tax_category_code}",
                            "evidence": [{"kind": "tax_brain_result", "category": tax_category_code}]
                        })
                    
                    # Look up category in Category table by code
                    category_id = None
                    category_version = None
                    
                    if tax_category_code:
                        # Find matching category
                        matching_category = None
                        for cat in available_categories:
                            if cat.get("code") == tax_category_code:
                                matching_category = cat
                                break
                        
                        if matching_category:
                            category_id = matching_category.get("id")
                            category_version = 1  # Default version for now
                            reasoning_steps.append({
                                "id": "step3",
                                "type": "lookup",
                                "summary": f"Found category in database: {matching_category.get('label')} (ID: {category_id})",
                                "evidence": [{"kind": "category", "id": category_id, "code": tax_category_code}]
                            })
                        else:
                            # Category doesn't exist - propose it
                            reasoning_steps.append({
                                "id": "step3",
                                "type": "proposal",
                                "summary": f"Category '{tax_category_code}' not found in database - proposing creation",
                                "evidence": [{"kind": "proposed_category", "code": tax_category_code}]
                            })
                            
                            # Create action to propose category
                            actions = [{
                                "type": "tax.propose_category",
                                "tier": 2,
                                "payload": {
                                    "code": tax_category_code,
                                    "label": tax_category_code.replace("_", " ").title(),
                                    "type": "expense",  # Default, could be inferred
                                    "reason": f"Suggested by Tax Brain for transaction #{transaction_id}"
                                }
                            }]
                            
                            return TaskResult(
                                task_id=task.id,
                                success=True,
                                message=f"Category '{tax_category_code}' not found - proposal created",
                                data={
                                    "tax_category": tax_category_code,
                                    "category_proposed": True
                                },
                                actions=actions,
                                reasoning={"steps": reasoning_steps},
                                evidence=evidence
                            )
                    
                    # Update transaction with category (using category_id if found, otherwise legacy tax_category)
                    update_payload = {}
                    if category_id:
                        update_payload["category_id"] = category_id
                        update_payload["category_version"] = category_version
                    else:
                        # Fallback to legacy field
                        update_payload["tax_category"] = tax_category_code
                    
                    if update_payload:
                        update_response = client.patch(
                            f"{self.life_os_api_url}/transactions/{transaction_id}",
                            json=update_payload
                        )
                        
                        if update_response.status_code == 200:
                            reasoning_steps.append({
                                "id": "step4",
                                "type": "update",
                                "summary": f"Updated transaction #{transaction_id} with category",
                                "evidence": [{"kind": "transaction", "id": transaction_id}]
                            })
                            
                            # Phase 4: Create memory link if vendor hint was used
                            actions = []
                            if vendor_hint_memory_id:
                                actions.append({
                                    "type": "memory.link",
                                    "tier": 1,
                                    "payload": {
                                        "from_memory_id": vendor_hint_memory_id,
                                        "target_type": "transaction",
                                        "target_id": transaction_id,
                                        "relationship_type": "applies_to",
                                        "notes": f"Vendor hint applied to transaction #{transaction_id}"
                                    }
                                })
                            
                            return TaskResult(
                                task_id=task.id,
                                success=True,
                                message=f"Categorized transaction #{transaction_id} as: {tax_category_code}",
                                data={
                                    "tax_category": tax_category_code,
                                    "category_id": category_id
                                },
                                actions=actions if actions else None,
                                reasoning={"steps": reasoning_steps},
                                evidence=evidence
                            )
                    
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=f"Categorized transaction #{transaction_id}",
                        data={"tax_category": tax_category_code},
                        reasoning={"steps": reasoning_steps},
                        evidence=evidence
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to categorize transaction: {categorize_response.status_code}",
                        reasoning={"steps": reasoning_steps},
                        evidence=evidence
                    )
        except Exception as e:
            logger.error(f"Error categorizing transaction: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error categorizing transaction: {str(e)}",
                reasoning={"steps": reasoning_steps},
                evidence=evidence
            )
    
    def _handle_generate_report(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle tax report generation"""
        payload = task.payload or {}
        year = payload.get("year")
        
        if not year:
            # Default to current year
            year = datetime.now().year
        
        # Generate year summary
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    f"{self.life_os_api_url}/tax/summary/{year}",
                    params={"user_id": context.config.get("user_id", 1) if hasattr(context, "config") else 1}
                )
                
                if response.status_code == 200:
                    summary = response.json()
                    message = f"Generated tax report for {year}"
                    
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
                        message=f"Failed to generate report: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error generating report: {str(e)}"
            )
    
    def _handle_find_deductions(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle finding deductions"""
        payload = task.payload or {}
        year = payload.get("year")
        
        if not year:
            year = datetime.now().year
        
        # Get transactions for the year and filter for deductions
        try:
            with httpx.Client(timeout=10.0) as client:
                # Get transactions
                start_date = f"{year}-01-01"
                end_date = f"{year + 1}-01-01"
                
                response = client.get(
                    f"{self.life_os_api_url}/transactions",
                    params={
                        "start_date": start_date,
                        "end_date": end_date,
                        "limit": 500
                    }
                )
                
                if response.status_code == 200:
                    transactions = response.json()
                    
                    # Filter for deductible transactions (negative amounts with tax categories)
                    deductions = []
                    for txn in transactions:
                        amount_str = txn.get("amount", "0")
                        tax_category = txn.get("tax_category")
                        
                        try:
                            amount = float(amount_str.replace("$", "").replace(",", ""))
                            # Deductions are typically expenses (negative amounts) with tax categories
                            if amount < 0 and tax_category:
                                deductions.append(txn)
                        except:
                            pass
                    
                    # Calculate total
                    total = sum(
                        float(txn.get("amount", "0").replace("$", "").replace(",", ""))
                        for txn in deductions
                    )
                    
                    message = f"Found {len(deductions)} deductible transaction(s) for {year}, Total: ${abs(total):.2f}"
                    
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=message,
                        data={
                            "deductions": deductions,
                            "count": len(deductions),
                            "total": f"${abs(total):.2f}",
                            "year": year
                        }
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to fetch transactions: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error finding deductions: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error finding deductions: {str(e)}"
            )
    
    def _handle_summarize_by_category(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle tax summarization by category"""
        payload = task.payload or {}
        year = payload.get("year")
        
        if not year:
            year = datetime.now().year
        
        # Use transaction summary by category
        try:
            with httpx.Client(timeout=10.0) as client:
                start_date = f"{year}-01-01"
                end_date = f"{year + 1}-01-01"
                
                response = client.get(
                    f"{self.life_os_api_url}/transactions/summary/by_category",
                    params={
                        "start_date": start_date,
                        "end_date": end_date
                    }
                )
                
                if response.status_code == 200:
                    summary = response.json()
                    message = f"Tax summary by category for {year}: {summary.get('count', 0)} transactions"
                    
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
                        message=f"Failed to get tax summary: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error summarizing by category: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error summarizing by category: {str(e)}"
            )
    
    def _handle_update_category(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle updating transaction category"""
        payload = task.payload or {}
        transaction_id = payload.get("transaction_id")
        tax_category = payload.get("tax_category")
        
        if not transaction_id or not tax_category:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required fields: 'transaction_id' and 'tax_category'"
            )
        
        # Update transaction via API
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.patch(
                    f"{self.life_os_api_url}/transactions/{transaction_id}",
                    json={"tax_category": tax_category}
                )
                
                if response.status_code == 200:
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=f"Updated transaction #{transaction_id} category to: {tax_category}"
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
                        message=f"Failed to update category: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error updating category: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error updating category: {str(e)}"
            )
    
    def _handle_get_categories(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle getting tax categories"""
        # Get categories from Tax Brain
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    f"{self.life_os_api_url}/tax/categories",
                    params={"user_id": context.config.get("user_id", 1) if hasattr(context, "config") else 1}
                )
                
                if response.status_code == 200:
                    categories = response.json()
                    message = f"Found {len(categories)} tax category/categories"
                    
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=message,
                        data={"categories": categories, "count": len(categories)}
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to fetch categories: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error fetching categories: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error fetching categories: {str(e)}"
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
        
        # Check if Tax Brain API is reachable
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"{self.life_os_api_url}/tax/categories", params={"user_id": 1})
                # 200 or 404 is OK (404 means no categories yet)
                if response.status_code not in [200, 404]:
                    issues.append(SkillHealthIssue(
                        code="tax_brain_api_unreachable",
                        message=f"Tax Brain API returned status {response.status_code}",
                        suggestion="Ensure Tax Brain module is properly integrated"
                    ))
        except Exception as e:
            issues.append(SkillHealthIssue(
                code="tax_brain_api_unreachable",
                message=f"Cannot reach Tax Brain API: {str(e)}",
                suggestion="Ensure Tax Brain module is properly integrated"
            ))
        
        return issues

