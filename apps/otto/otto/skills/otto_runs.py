"""
OttoRunsSkill - Query and manage Otto run history
"""

from typing import List, Dict, Any
import httpx
import os

from ..core.models import Task, TaskResult, TaskStatus
from ..core.skill_base import Skill, SkillHealthIssue, SkillContext
from ..core.logging_utils import get_logger

logger = get_logger(__name__)


class OttoRunsSkill:
    """Skill that queries and manages Otto run history"""
    
    name = "otto_runs"
    description = "Query and view Otto run history from the Life OS backend"
    
    def __init__(self):
        # Life OS backend API URL - use env var or default
        self.life_os_api_url = os.getenv("LIFE_OS_API_URL", "http://localhost:8000")
    
    def can_handle(self, task: Task) -> bool:
        """Check if this skill can handle the task"""
        # Handle tasks related to Otto runs
        return task.type in ["otto_runs", "list_otto_runs", "get_otto_run", "otto_history"]
    
    def run(self, task: Task, context: SkillContext) -> TaskResult:
        """Execute the Otto runs query task"""
        try:
            action = task.payload.get("action", "list")
            run_id = task.payload.get("run_id")
            limit = task.payload.get("limit", 20)
            
            if action == "get" and run_id:
                # Get specific run details
                return self._get_run_details(run_id, task.id)
            elif action == "list" or action == "recent":
                # List recent runs
                return self._list_runs(limit, task.id)
            else:
                return TaskResult(
                    task_id=task.id,
                    success=False,
                    message=f"Unknown action: {action}. Supported actions: 'list', 'get'"
                )
        except Exception as e:
            logger.error(f"Error in OttoRunsSkill: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error querying Otto runs: {str(e)}"
            )
    
    def _list_runs(self, limit: int, task_id: str) -> TaskResult:
        """List recent Otto runs"""
        try:
            async def fetch_runs():
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.get(
                        f"{self.life_os_api_url}/otto/runs",
                        params={"limit": limit}
                    )
                    response.raise_for_status()
                    return response.json()
            
            # For now, we'll use sync httpx since Otto's runner might be sync
            # In the future, this could be made async
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    f"{self.life_os_api_url}/otto/runs",
                    params={"limit": limit}
                )
                response.raise_for_status()
                runs = response.json()
            
            # Format the response
            if not runs:
                return TaskResult(
                    task_id=task_id,
                    success=True,
                    message="No Otto runs found.",
                    data={"runs": []}
                )
            
            # Create a summary
            summary_lines = []
            summary_lines.append(f"Found {len(runs)} recent Otto run(s):\n")
            
            for run in runs:
                status_emoji = {
                    "success": "✅",
                    "error": "❌",
                    "running": "🔄",
                    "pending": "⏳"
                }.get(run.get("status"), "❓")
                
                summary_lines.append(
                    f"{status_emoji} Run #{run['id']} ({run['status']}) - "
                    f"{run['input_text'][:60]}{'...' if len(run['input_text']) > 60 else ''}"
                )
                summary_lines.append(f"   Created: {run['created_at']}")
                if run.get("source"):
                    summary_lines.append(f"   Source: {run['source']}")
                summary_lines.append("")
            
            return TaskResult(
                task_id=task_id,
                success=True,
                message="\n".join(summary_lines),
                data={"runs": runs, "count": len(runs)}
            )
            
        except httpx.RequestError as e:
            return TaskResult(
                task_id=task_id,
                success=False,
                message=f"Could not connect to Life OS API: {str(e)}"
            )
        except httpx.HTTPStatusError as e:
            return TaskResult(
                task_id=task_id,
                success=False,
                message=f"Life OS API error: {e.response.status_code} - {e.response.text}"
            )
        except Exception as e:
            return TaskResult(
                task_id=task_id,
                success=False,
                message=f"Unexpected error: {str(e)}"
            )
    
    def _get_run_details(self, run_id: int, task_id: str) -> TaskResult:
        """Get details of a specific Otto run"""
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    f"{self.life_os_api_url}/otto/runs/{run_id}"
                )
                response.raise_for_status()
                run = response.json()
            
            # Format the response
            status_emoji = {
                "success": "✅",
                "error": "❌",
                "running": "🔄",
                "pending": "⏳"
            }.get(run.get("status"), "❓")
            
            details = []
            details.append(f"{status_emoji} Run #{run['id']} - {run['status'].upper()}")
            details.append(f"Created: {run['created_at']}")
            details.append(f"Updated: {run['updated_at']}")
            details.append(f"Source: {run.get('source', 'unknown')}")
            details.append("")
            details.append("Input:")
            details.append(f"  {run['input_text']}")
            details.append("")
            
            if run.get("output_text"):
                details.append("Output:")
                details.append(f"  {run['output_text']}")
                details.append("")
            
            if run.get("logs"):
                details.append("Logs:")
                # Truncate long logs
                logs = run['logs']
                if len(logs) > 500:
                    logs = logs[:500] + "\n... (truncated)"
                details.append(f"  {logs}")
            
            return TaskResult(
                task_id=task_id,
                success=True,
                message="\n".join(details),
                data={"run": run}
            )
            
        except httpx.RequestError as e:
            return TaskResult(
                task_id=task_id,
                success=False,
                message=f"Could not connect to Life OS API: {str(e)}"
            )
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return TaskResult(
                    task_id=task_id,
                    success=False,
                    message=f"Run #{run_id} not found"
                )
            return TaskResult(
                task_id=task_id,
                success=False,
                message=f"Life OS API error: {e.response.status_code} - {e.response.text}"
            )
        except Exception as e:
            return TaskResult(
                task_id=task_id,
                success=False,
                message=f"Unexpected error: {str(e)}"
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
                        code="life_os_api_unhealthy",
                        message=f"Life OS API returned status {response.status_code}",
                        suggestion="Check if Life OS backend is running and healthy"
                    ))
        except httpx.RequestError:
            issues.append(SkillHealthIssue(
                code="life_os_api_unreachable",
                message=f"Could not reach Life OS API at {self.life_os_api_url}",
                suggestion="Ensure Life OS backend is running and LIFE_OS_API_URL is correct"
            ))
        
        return issues

