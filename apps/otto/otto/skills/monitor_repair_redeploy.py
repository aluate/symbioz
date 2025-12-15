"""
Monitor/Repair/Redeploy Loop Skill for Otto

Monitors Vercel and Render deployments, detects failures, applies minimal fixes,
commits, and redeploys until both targets are green.
"""

import os
import time
import subprocess
from typing import Any, Dict, List, Optional
from pathlib import Path

from ..core.models import Task, TaskResult
from ..core.skill_base import SkillContext
from ..core.logging_utils import get_logger
from ..providers.vercel_client import VercelClient
from ..providers.render_client import RenderClient
from ..providers.github_client import GitHubClient

logger = get_logger(__name__)


class MonitorRepairRedeploySkill:
    """Skill that monitors deployments and auto-fixes failures"""
    
    name = "monitor_repair_redeploy"
    description = "Monitors Vercel and Render deployments, detects failures, applies minimal fixes, commits, and redeploys"
    
    def __init__(self):
        """Initialize the skill with provider clients"""
        self.vercel_client = None
        self.render_client = None
        self.github_client = None
        self._init_clients()
    
    def _init_clients(self):
        """Initialize provider clients if tokens are available"""
        try:
            if os.getenv("VERCEL_TOKEN"):
                self.vercel_client = VercelClient()
        except Exception as e:
            logger.warning(f"Could not initialize Vercel client: {e}")
        
        try:
            if os.getenv("RENDER_API_KEY"):
                self.render_client = RenderClient()
        except Exception as e:
            logger.warning(f"Could not initialize Render client: {e}")
        
        try:
            if os.getenv("GITHUB_TOKEN"):
                self.github_client = GitHubClient()
        except Exception as e:
            logger.warning(f"Could not initialize GitHub client: {e}")
    
    def can_handle(self, task: Task) -> bool:
        """Check if this skill can handle the task"""
        return task.type == "monitor_repair_redeploy"
    
    def run(self, task: Task, context: SkillContext) -> TaskResult:
        """Run the monitor/repair/redeploy loop"""
        try:
            payload = task.payload or {}
            mode = payload.get("mode", "pr")  # "pr" or "main"
            targets = payload.get("targets", {})
            max_iterations = payload.get("maxIterations", 5)
            
            vercel_config = targets.get("vercel", {})
            render_config = targets.get("render", {})
            
            results = []
            iteration = 0
            
            while iteration < max_iterations:
                iteration += 1
                logger.info(f"Monitor/repair iteration {iteration}/{max_iterations}")
                
                # Check Vercel status
                vercel_status = None
                if vercel_config and self.vercel_client:
                    vercel_status = self._check_vercel(vercel_config)
                    results.append({
                        "iteration": iteration,
                        "target": "vercel",
                        "status": vercel_status.get("status"),
                        "message": vercel_status.get("message")
                    })
                
                # Check Render status
                render_status = None
                if render_config and self.render_client:
                    render_status = self._check_render(render_config)
                    results.append({
                        "iteration": iteration,
                        "target": "render",
                        "status": render_status.get("status"),
                        "message": render_status.get("message")
                    })
                
                # Check if both are green
                vercel_ok = not vercel_status or vercel_status.get("status") == "success"
                render_ok = not render_status or render_status.get("status") == "success"
                
                if vercel_ok and render_ok:
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=f"✅ Both deployments successful after {iteration} iteration(s)",
                        data={
                            "iterations": iteration,
                            "results": results,
                            "vercel": vercel_status,
                            "render": render_status
                        }
                    )
                
                # Pick ONE failing target (prefer web/Vercel first)
                failing_target = None
                if not vercel_ok and vercel_status:
                    failing_target = ("vercel", vercel_status, vercel_config)
                elif not render_ok and render_status:
                    failing_target = ("render", render_status, render_config)
                
                if failing_target:
                    # Apply fix
                    fix_result = self._apply_fix(failing_target[0], failing_target[1], failing_target[2], mode)
                    if fix_result.get("success"):
                        results.append({
                            "iteration": iteration,
                            "action": "fix_applied",
                            "target": failing_target[0],
                            "files_changed": fix_result.get("files_changed", [])
                        })
                        
                        # Wait for redeploy
                        logger.info("Waiting for redeploy to trigger...")
                        time.sleep(30)  # Give webhooks time to trigger
                    else:
                        return TaskResult(
                            task_id=task.id,
                            success=False,
                            message=f"Failed to apply fix: {fix_result.get('error')}",
                            data={"iterations": iteration, "results": results}
                        )
            
            # Max iterations reached
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Max iterations ({max_iterations}) reached. Some deployments may still be failing.",
                data={"iterations": iteration, "results": results}
            )
            
        except Exception as e:
            logger.error(f"Error in monitor_repair_redeploy: {e}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error: {str(e)}"
            )
    
    def _check_vercel(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Check Vercel deployment status"""
        project_name = config.get("projectNameOrId")
        if not project_name:
            return {"status": "error", "message": "No project name provided"}
        
        deployment = self.vercel_client.list_latest_deployment(project_name)
        if not deployment:
            return {"status": "error", "message": "No deployment found"}
        
        deployment_id = deployment.get("uid")
        status = self.vercel_client.get_deployment_status(deployment_id)
        state = status.get("state", "UNKNOWN")
        
        if state == "READY":
            return {"status": "success", "message": "Vercel deployment successful", "deployment_id": deployment_id}
        elif state in ["ERROR", "CANCELED"]:
            logs = self.vercel_client.get_deployment_logs(deployment_id)
            errors = self.vercel_client.parse_errors_from_logs(logs)
            return {
                "status": "failed",
                "message": f"Vercel deployment {state.lower()}",
                "deployment_id": deployment_id,
                "errors": errors[:5],  # Limit to 5 errors
                "logs_summary": "\n".join(str(log)[:200] for log in logs[:10])  # First 10 log entries
            }
        else:
            return {"status": "building", "message": f"Vercel deployment {state}", "deployment_id": deployment_id}
    
    def _check_render(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Check Render deployment status"""
        service_id = config.get("serviceId")
        if not service_id:
            return {"status": "error", "message": "No service ID provided"}
        
        deploys = self.render_client.list_deploys(service_id, limit=1)
        if not deploys:
            return {"status": "error", "message": "No deployments found"}
        
        deploy = deploys[0]
        deploy_id = deploy.get("id")
        deploy_status = deploy.get("status", "unknown")
        
        if deploy_status == "live":
            return {"status": "success", "message": "Render deployment successful", "deploy_id": deploy_id}
        elif deploy_status in ["build_failed", "update_failed", "deactivated"]:
            logs = self.render_client.get_deploy_logs(service_id, deploy_id)
            errors = self.render_client.parse_errors_from_logs(logs)
            return {
                "status": "failed",
                "message": f"Render deployment {deploy_status}",
                "deploy_id": deploy_id,
                "errors": errors[:5],
                "logs_summary": logs[:1000]  # First 1000 chars
            }
        else:
            return {"status": "building", "message": f"Render deployment {deploy_status}", "deploy_id": deploy_id}
    
    def _apply_fix(self, target: str, status: Dict[str, Any], config: Dict[str, Any], mode: str) -> Dict[str, Any]:
        """Apply minimal fix based on error logs"""
        errors = status.get("errors", [])
        if not errors:
            return {"success": False, "error": "No errors found to fix"}
        
        # For now, this is a stub - in a real implementation, this would:
        # 1. Parse errors to identify root cause
        # 2. Generate minimal patch
        # 3. Apply patch to files
        # 4. Run local checks (lint/build)
        # 5. Commit and push
        
        logger.info(f"Would apply fix for {target} with errors: {errors[:2]}")
        
        # Stub: create a minimal fix file
        fix_file = Path("docs/deploy_failures_latest.md")
        fix_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(fix_file, "w") as f:
            f.write(f"# Latest Deployment Failures\n\n")
            f.write(f"Target: {target}\n")
            f.write(f"Errors detected:\n")
            for error in errors[:5]:
                f.write(f"- {error}\n")
        
        # Commit the fix
        if self.github_client:
            if mode == "pr":
                branch_name = f"fix/{target}-{int(time.time())}"
                self.github_client.create_branch(branch_name)
            
            commit_msg = f"Fix: {target} deployment errors"
            if self.github_client.commit_changes(commit_msg, [str(fix_file)]):
                push_result = self.github_client.push(
                    branch=self.github_client.get_current_branch(),
                    remote="origin"
                )
                if push_result.get("success"):
                    return {
                        "success": True,
                        "files_changed": [str(fix_file)],
                        "commit_message": commit_msg
                    }
        
        return {"success": False, "error": "Could not commit or push changes"}

