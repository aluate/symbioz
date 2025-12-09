"""
BillReminderSkill - Monitors bills and creates reminders
"""

from typing import List, Dict, Any
import os
import httpx
from datetime import datetime, timedelta

from ..core.models import Task, TaskResult, TaskStatus
from ..core.skill_base import Skill, SkillHealthIssue, SkillContext
from ..core.logging_utils import get_logger
from .memory_helpers import get_reminder_pattern

logger = get_logger(__name__)


class BillReminderSkill:
    """Skill that monitors bills and creates reminders"""
    
    name = "bill_reminder"
    description = "Monitors household bills and creates reminder tasks for upcoming or overdue bills"
    
    def __init__(self):
        # Life OS backend API URL
        self.life_os_api_url = os.getenv("LIFE_OS_API_URL", "http://localhost:8000")
    
    def can_handle(self, task: Task) -> bool:
        """Check if this skill can handle the task"""
        return task.type in [
            "bill_reminder",
            "check_bills",
            "create_bill_reminders",
            "scan_bills",
            "upcoming_bills"
        ]
    
    def run(self, task: Task, context: SkillContext) -> TaskResult:
        """Execute the bill reminder check"""
        try:
            # Get upcoming and overdue bills
            bills_data = self._fetch_bills()
            
            if not bills_data:
                return TaskResult(
                    task_id=task.id,
                    success=True,
                    message="No bills found to process",
                    data={"bills_processed": 0}
                )
            
            # Analyze bills and create reminders
            reminders_created = []
            actions = []
            
            # Phase 3B: Track reasoning and evidence, lookup reminder pattern
            reasoning_steps = []
            evidence = {
                "bills": [],
                "reminders": [],
                "memory_ids": []
            }
            
            reasoning_steps.append({
                "id": "step1",
                "type": "fetch",
                "summary": f"Fetched {len(bills_data)} bill(s) from Life OS API",
                "evidence": [{"kind": "bills_fetched", "count": len(bills_data)}]
            })
            
            # Phase 3B: Lookup default reminder pattern from memory
            reminder_days, memory_id, memory_entry = get_reminder_pattern(self.life_os_api_url)
            
            if memory_id:
                reasoning_steps.append({
                    "id": "step2",
                    "type": "lookup",
                    "summary": f"Retrieved reminder pattern from OttoMemory (ID: {memory_id}): {reminder_days} days before",
                    "evidence": [{"kind": "memory", "id": memory_id, "pattern": reminder_days}]
                })
                evidence["memory_ids"].append(memory_id)
            else:
                reasoning_steps.append({
                    "id": "step2",
                    "type": "fallback",
                    "summary": f"No reminder pattern found in memory, using default: {reminder_days} days before",
                    "evidence": [{"kind": "default_pattern", "pattern": reminder_days}]
                })
            
            for bill in bills_data:
                evidence["bills"].append(bill["id"])
                reminder_info = self._analyze_bill(bill)
                if reminder_info["needs_reminder"]:
                    # Create a task reminder
                    # Note: The reminder pattern is used to determine when to create reminders
                    # For now, we create the task at the bill due date, but in future
                    # we could create multiple reminders based on the pattern
                    actions.append({
                        "type": "life_os.create_task",
                        "tier": 1,
                        "payload": {
                            "title": f"Pay {bill['name']}",
                            "description": reminder_info["description"],
                            "due_date": bill["due_date"],
                            "priority": reminder_info["priority"],
                            "category": "bills"
                        }
                    })
                    reminders_created.append({
                        "bill_id": bill["id"],
                        "bill_name": bill["name"],
                        "amount": bill["amount"],
                        "due_date": bill["due_date"]
                    })
                    evidence["reminders"].append(bill["id"])
                    
                    # Phase 4: Create memory link if pattern memory was used
                    if memory_id:
                        actions.append({
                            "type": "memory.link",
                            "tier": 1,
                            "payload": {
                                "from_memory_id": memory_id,
                                "target_type": "bill",
                                "target_id": bill["id"],
                                "relationship_type": "applies_to",
                                "notes": f"Reminder pattern applied to bill {bill['name']}"
                            }
                        })
            
            if reminders_created:
                reasoning_steps.append({
                    "id": "step3",
                    "type": "reminder_creation",
                    "summary": f"Created {len(reminders_created)} reminder(s) based on bill due dates using pattern: {reminder_days} days before",
                    "evidence": [{"kind": "reminders", "count": len(reminders_created), "bill_ids": [r["bill_id"] for r in reminders_created], "pattern_used": reminder_days}]
                })
            
            message = f"Processed {len(bills_data)} bill(s). Created {len(reminders_created)} reminder(s)."
            
            if reminders_created:
                message += "\n\nReminders created:\n"
                for r in reminders_created:
                    message += f"- {r['bill_name']} (${r['amount']}) due {r['due_date']}\n"
            
            return TaskResult(
                task_id=task.id,
                success=True,
                message=message,
                data={
                    "bills_processed": len(bills_data),
                    "reminders_created": len(reminders_created),
                    "reminders": reminders_created
                },
                actions=actions if actions else None,
                reasoning={"steps": reasoning_steps} if reasoning_steps else None,
                evidence=evidence
            )
        except Exception as e:
            logger.error(f"Error in BillReminderSkill: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error checking bills: {str(e)}"
            )
    
    def _fetch_bills(self) -> List[Dict[str, Any]]:
        """Fetch bills from Life OS API"""
        try:
            with httpx.Client(timeout=10.0) as client:
                # Get upcoming bills (next 30 days) and overdue bills
                response = client.get(
                    f"{self.life_os_api_url}/bills",
                    params={
                        "paid": "no",
                        "limit": 100
                    }
                )
                if response.status_code == 200:
                    bills = response.json()
                    # Filter to only upcoming/overdue
                    now = datetime.utcnow()
                    future_date = now + timedelta(days=30)
                    
                    filtered_bills = []
                    for bill in bills:
                        due_date_str = bill.get("due_date")
                        if due_date_str:
                            try:
                                due_date = datetime.fromisoformat(due_date_str.replace("Z", "+00:00"))
                                # Include if due within 30 days or overdue
                                if due_date <= future_date:
                                    filtered_bills.append(bill)
                            except:
                                pass
                    
                    return filtered_bills
                else:
                    logger.warning(f"Failed to fetch bills: {response.status_code}")
                    return []
        except Exception as e:
            logger.error(f"Error fetching bills: {str(e)}")
            return []
    
    def _analyze_bill(self, bill: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a bill and determine if a reminder is needed"""
        due_date_str = bill.get("due_date")
        if not due_date_str:
            return {"needs_reminder": False}
        
        try:
            due_date = datetime.fromisoformat(due_date_str.replace("Z", "+00:00"))
            now = datetime.utcnow()
            days_until_due = (due_date - now).days
            
            # Determine if reminder is needed
            # - Overdue: always remind
            # - Due within 3 days: high priority
            # - Due within 7 days: medium priority
            # - Due within 14 days: low priority
            # - Due within 30 days: low priority (optional)
            
            if days_until_due < 0:
                # Overdue
                return {
                    "needs_reminder": True,
                    "priority": "high",
                    "description": f"OVERDUE: ${bill.get('amount', 'N/A')} due {due_date_str[:10]}. {bill.get('payee', '')} - {bill.get('account_number', '')}"
                }
            elif days_until_due <= 3:
                return {
                    "needs_reminder": True,
                    "priority": "high",
                    "description": f"Due in {days_until_due} day(s): ${bill.get('amount', 'N/A')}. {bill.get('payee', '')} - {bill.get('account_number', '')}"
                }
            elif days_until_due <= 7:
                return {
                    "needs_reminder": True,
                    "priority": "medium",
                    "description": f"Due in {days_until_due} day(s): ${bill.get('amount', 'N/A')}. {bill.get('payee', '')} - {bill.get('account_number', '')}"
                }
            elif days_until_due <= 14:
                return {
                    "needs_reminder": True,
                    "priority": "medium",
                    "description": f"Due in {days_until_due} day(s): ${bill.get('amount', 'N/A')}. {bill.get('payee', '')}"
                }
            elif days_until_due <= 30:
                # Only create reminder if there isn't already a task for this bill
                # For now, we'll create it but with low priority
                return {
                    "needs_reminder": True,
                    "priority": "low",
                    "description": f"Due in {days_until_due} day(s): ${bill.get('amount', 'N/A')}. {bill.get('payee', '')}"
                }
            else:
                return {"needs_reminder": False}
        except Exception as e:
            logger.warning(f"Error analyzing bill: {str(e)}")
            return {"needs_reminder": False}
    
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

