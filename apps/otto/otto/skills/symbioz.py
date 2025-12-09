"""
SymbiozSkill - Otto can launch and manage Symbioz game
"""

import os
import subprocess
import sys
from typing import List, Dict, Any

from ..core.models import Task, TaskResult, TaskStatus
from ..core.skill_base import Skill, SkillHealthIssue, SkillContext
from ..core.logging_utils import get_logger

logger = get_logger(__name__)


class SymbiozSkill:
    """Skill for managing Symbioz game"""
    
    name = "symbioz"
    description = "Launch and manage Symbioz game server and UI"
    
    def can_handle(self, task: Task) -> bool:
        """Check if this skill can handle the task"""
        return task.type in ["symbioz", "launch_symbioz", "start_symbioz", "symbioz_game"]
    
    def run(self, task: Task, context: SkillContext) -> TaskResult:
        """Execute Symbioz task"""
        try:
            action = task.payload.get("action", "launch")
            
            if action == "launch" or action == "start":
                return self._launch_game(context)
            elif action == "check":
                return self._check_status(context)
            else:
                return TaskResult(
                    task_id=task.id,
                    success=False,
                    message=f"Unknown action: {action}"
                )
        except Exception as e:
            logger.error(f"Error in SymbiozSkill: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error: {str(e)}"
            )
    
    def _launch_game(self, context: SkillContext) -> TaskResult:
        """Launch Symbioz game"""
        try:
            # Find repo root
            repo_root = self._find_repo_root()
            if not repo_root:
                return TaskResult(
                    task_id="",
                    success=False,
                    message="Could not find repository root"
                )
            
            launcher_path = os.path.join(repo_root, "LAUNCH_SYMBIOZ.bat")
            if not os.path.exists(launcher_path):
                return TaskResult(
                    task_id="",
                    success=False,
                    message=f"Launcher not found at {launcher_path}"
                )
            
            # Launch the game
            if sys.platform == "win32":
                subprocess.Popen(
                    [launcher_path],
                    cwd=repo_root,
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            else:
                # For non-Windows, would need different approach
                subprocess.Popen(
                    ["bash", launcher_path],
                    cwd=repo_root
                )
            
            return TaskResult(
                task_id="",
                success=True,
                message="Symbioz game launcher started! Check the console windows.",
                data={
                    "api_url": "http://localhost:8002",
                    "web_ui_url": "http://localhost:3001"
                }
            )
        except Exception as e:
            logger.error(f"Error launching Symbioz: {str(e)}")
            return TaskResult(
                task_id="",
                success=False,
                message=f"Failed to launch game: {str(e)}"
            )
    
    def _check_status(self, context: SkillContext) -> TaskResult:
        """Check if Symbioz services are running"""
        import httpx
        
        results = {}
        all_ok = True
        
        # Check API server
        try:
            with httpx.Client(timeout=2.0) as client:
                response = client.get("http://localhost:8002/")
                results["api_server"] = {
                    "ok": response.status_code == 200,
                    "status": response.status_code
                }
                if response.status_code != 200:
                    all_ok = False
        except Exception as e:
            results["api_server"] = {
                "ok": False,
                "status": "unreachable",
                "error": str(e)
            }
            all_ok = False
        
        # Check web UI (harder to check, just try to connect)
        try:
            with httpx.Client(timeout=2.0) as client:
                response = client.get("http://localhost:3001/")
                results["web_ui"] = {
                    "ok": response.status_code == 200,
                    "status": response.status_code
                }
                if response.status_code != 200:
                    all_ok = False
        except Exception as e:
            results["web_ui"] = {
                "ok": False,
                "status": "unreachable",
                "error": str(e)
            }
            all_ok = False
        
        return TaskResult(
            task_id="",
            success=all_ok,
            message="All services running" if all_ok else "Some services not running",
            data=results
        )
    
    def _find_repo_root(self) -> str:
        """Find the repository root by looking for LAUNCH_SYMBIOZ.bat"""
        current = os.path.abspath(__file__)
        
        # Go up from apps/otto/otto/skills/symbioz.py
        # to repo root
        for _ in range(5):
            current = os.path.dirname(current)
            launcher = os.path.join(current, "LAUNCH_SYMBIOZ.bat")
            if os.path.exists(launcher):
                return current
        
        return None
    
    def self_test(self, context: SkillContext) -> List[SkillHealthIssue]:
        """Run health checks on this skill"""
        issues = []
        
        # Check if launcher exists
        repo_root = self._find_repo_root()
        if not repo_root:
            issues.append(SkillHealthIssue(
                code="launcher_not_found",
                message="Could not find LAUNCH_SYMBIOZ.bat in repository",
                suggestion="Ensure you're running from the correct repository"
            ))
        
        return issues

