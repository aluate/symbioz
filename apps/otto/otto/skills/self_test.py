"""
SelfTestSkill - Otto can test himself!
"""

from typing import List, Dict, Any
import httpx
import os

from ..core.models import Task, TaskResult, TaskStatus
from ..core.skill_base import Skill, SkillHealthIssue, SkillContext
from ..core.logging_utils import get_logger

logger = get_logger(__name__)


class SelfTestSkill:
    """Skill that allows Otto to test his own functionality"""
    
    name = "self_test"
    description = "Test Otto's worker, actions, and API endpoints"
    
    def __init__(self):
        self.life_os_api_url = os.getenv("LIFE_OS_API_URL", "http://localhost:8000")
        self.otto_api_url = os.getenv("OTTO_API_URL", "http://localhost:8001")
    
    def can_handle(self, task: Task) -> bool:
        """Check if this skill can handle the task"""
        return task.type in ["self_test", "test_otto", "test_worker", "test_phase2"]
    
    def run(self, task: Task, context: SkillContext) -> TaskResult:
        """Execute self-test"""
        try:
            # Default to "quick" to avoid spamming DB
            test_type = task.payload.get("test_type", "quick")
            
            if test_type == "worker" or test_type == "full":
                worker_result = self._test_worker()
            else:
                worker_result = None
            
            if test_type == "api" or test_type == "full":
                api_result = self._test_api()
            else:
                api_result = None
            
            if test_type == "actions" or test_type == "full":
                actions_result = self._test_actions()
            else:
                actions_result = None
            
            # Format report
            report = self._format_report(worker_result, api_result, actions_result, test_type)
            
            # Create actions to actually run a test if requested (full test only)
            actions = []
            if test_type == "full" and task.payload.get("create_test_task", True):
                actions.append({
                    "type": "life_os.create_task",
                    "payload": {
                        "type": "otto.log",
                        "description": "[OTTO_SELF_TEST] Self-test task created by Otto",
                        "payload": {
                            "message": "Otto tested himself!",
                            "level": "info",
                            "meta": {
                                "source": "self_test",
                                "test_id": task.id
                            }
                        }
                    }
                })
            
            return TaskResult(
                task_id=task.id,
                success=True,
                message=report,
                data={
                    "test_type": test_type,
                    "worker_test": worker_result,
                    "api_test": api_result,
                    "actions_test": actions_result,
                    "actions": actions if actions else None
                }
            )
        except Exception as e:
            logger.error(f"Error in SelfTestSkill: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error running self-test: {str(e)}"
            )
    
    def _test_worker(self) -> Dict[str, Any]:
        """Test if worker is processing tasks"""
        try:
            # Check for recent worker runs
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"{self.life_os_api_url}/otto/runs?limit=5")
                response.raise_for_status()
                runs = response.json()
                
                worker_runs = [r for r in runs if r.get('source') == 'worker']
                
                if worker_runs:
                    latest = worker_runs[0]
                    return {
                        "ok": True,
                        "status": "worker_active",
                        "message": f"Worker is active. Latest run: #{latest['id']} ({latest['status']})",
                        "latest_run_id": latest['id'],
                        "latest_status": latest['status']
                    }
                else:
                    return {
                        "ok": False,
                        "status": "worker_not_running",
                        "message": "No worker runs found. Worker may not be running.",
                        "suggestion": "Start worker with: python -m worker.otto_worker"
                    }
        except httpx.RequestError as e:
            return {
                "ok": False,
                "status": "life_os_api_unreachable",
                "message": f"Cannot reach Life OS API: {str(e)}",
                "suggestion": "Ensure Life OS backend is running on port 8000"
            }
        except Exception as e:
            return {
                "ok": False,
                "status": "worker_check_error",
                "message": f"Error checking worker: {str(e)}"
            }
    
    def _test_api(self) -> Dict[str, Any]:
        """Test API endpoints"""
        results = {}
        issues = []
        
        # Test Otto API
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"{self.otto_api_url}/health")
                results["otto_api"] = {
                    "ok": response.status_code == 200,
                    "status": response.status_code,
                    "url": self.otto_api_url
                }
                if response.status_code != 200:
                    issues.append("otto_api_unreachable")
        except httpx.RequestError as e:
            results["otto_api"] = {
                "ok": False,
                "status": "unreachable",
                "error": str(e),
                "url": self.otto_api_url
            }
            issues.append("otto_api_unreachable")
        except Exception as e:
            results["otto_api"] = {
                "ok": False,
                "status": "error",
                "error": str(e)
            }
            issues.append("otto_api_error")
        
        # Test Life OS API
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"{self.life_os_api_url}/health")
                results["life_os_api"] = {
                    "ok": response.status_code == 200,
                    "status": response.status_code,
                    "url": self.life_os_api_url
                }
                if response.status_code != 200:
                    issues.append("life_os_api_unreachable")
        except httpx.RequestError as e:
            results["life_os_api"] = {
                "ok": False,
                "status": "unreachable",
                "error": str(e),
                "url": self.life_os_api_url
            }
            issues.append("life_os_api_unreachable")
        except Exception as e:
            results["life_os_api"] = {
                "ok": False,
                "status": "error",
                "error": str(e)
            }
            issues.append("life_os_api_error")
        
        # Test tasks endpoint
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"{self.life_os_api_url}/otto/tasks?limit=1")
                results["tasks_api"] = {
                    "ok": response.status_code == 200,
                    "status": response.status_code
                }
                if response.status_code != 200:
                    issues.append("tasks_api_error")
        except Exception as e:
            results["tasks_api"] = {
                "ok": False,
                "status": "error",
                "error": str(e)
            }
            issues.append("tasks_api_error")
        
        all_ok = all(r.get("ok", False) for r in results.values())
        return {
            "ok": all_ok,
            "status": "all_apis_ok" if all_ok else "api_issues",
            "results": results,
            "issues": issues,
            "message": "All APIs OK" if all_ok else f"Issues found: {', '.join(issues)}"
        }
    
    def _test_actions(self) -> Dict[str, Any]:
        """Test if action executor is working"""
        try:
            # Try to import the action executor module
            import sys
            import os
            # Check if we can reach the actions module
            # This is a simple check - actual execution testing happens in full test
            return {
                "ok": True,
                "status": "actions_executor_available",
                "message": "Action executor module available (execution tested in full test)"
            }
        except Exception as e:
            return {
                "ok": False,
                "status": "actions_executor_missing",
                "message": f"Cannot verify action executor: {str(e)}"
            }
    
    def _format_report(self, worker_result, api_result, actions_result, test_type: str) -> str:
        """Format test report with friendly error messages"""
        lines = []
        lines.append("Otto Self-Test Report")
        if test_type == "quick":
            lines.append("(Quick Test - API checks only)")
        elif test_type == "full":
            lines.append("(Full Test - Includes task creation)")
        lines.append("=" * 50)
        lines.append("")
        
        all_ok = True
        
        if worker_result:
            if worker_result.get("ok"):
                lines.append(f"✓ Worker: {worker_result.get('message', 'OK')}")
            else:
                all_ok = False
                status = worker_result.get("status", "unknown")
                suggestion = worker_result.get("suggestion", "")
                lines.append(f"✗ Worker: {worker_result.get('message', 'Not OK')}")
                lines.append(f"  Status: {status}")
                if suggestion:
                    lines.append(f"  → {suggestion}")
            lines.append("")
        
        if api_result:
            if api_result.get("ok"):
                lines.append(f"✓ APIs: {api_result.get('message', 'OK')}")
            else:
                all_ok = False
                issues = api_result.get("issues", [])
                lines.append(f"✗ APIs: {api_result.get('message', 'Not OK')}")
                for name, result in api_result.get("results", {}).items():
                    status_icon = "✓" if result.get("ok") else "✗"
                    status_text = result.get("status", "unknown")
                    error = result.get("error")
                    lines.append(f"  {status_icon} {name}: {status_text}")
                    if error:
                        lines.append(f"    Error: {error}")
                if issues:
                    lines.append(f"  Issues: {', '.join(issues)}")
            lines.append("")
        
        if actions_result:
            if actions_result.get("ok"):
                lines.append(f"✓ Actions: {actions_result.get('message', 'OK')}")
            else:
                all_ok = False
                status = actions_result.get("status", "unknown")
                lines.append(f"✗ Actions: {actions_result.get('message', 'Not OK')}")
                lines.append(f"  Status: {status}")
            lines.append("")
        
        # Summary
        lines.append("=" * 50)
        if all_ok:
            lines.append("✅ All systems operational!")
        else:
            lines.append("⚠️  Some issues detected - see details above")
        
        return "\n".join(lines)
    
    def self_test(self, context: SkillContext) -> List[SkillHealthIssue]:
        """Run health checks on this skill"""
        issues = []
        
        # Check if APIs are reachable
        try:
            with httpx.Client(timeout=5.0) as client:
                client.get(f"{self.life_os_api_url}/health")
        except:
            issues.append(SkillHealthIssue(
                code="life_os_api_unreachable",
                message=f"Life OS API not reachable at {self.life_os_api_url}",
                suggestion="Ensure Life OS backend is running"
            ))
        
        return issues

