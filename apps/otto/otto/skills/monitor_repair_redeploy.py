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
from .repair_classifiers import parse_vercel_failure, parse_render_failure
from .repair_applicators import apply_patch_vercel, apply_patch_render

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
            dry_run = payload.get("dryRun", False) or os.getenv("DRY_RUN", "false").lower() == "true"
            
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
                    fix_result = self._apply_fix(failing_target[0], failing_target[1], failing_target[2], mode, dry_run)
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
    
    def _apply_fix(self, target: str, status: Dict[str, Any], config: Dict[str, Any], mode: str, dry_run: bool = False) -> Dict[str, Any]:
        """Apply minimal fix based on error logs"""
        errors = status.get("errors", [])
        logs_summary = status.get("logs_summary", "")
        
        if not errors and not logs_summary:
            return {"success": False, "error": "No errors or logs found to fix"}
        
        # Combine errors and logs for classification
        log_text = "\n".join(errors) + "\n" + logs_summary
        
        # Classify the failure
        if target == "vercel":
            classification = parse_vercel_failure(log_text, status.get("logs", []))
        elif target == "render":
            classification = parse_render_failure(log_text)
        else:
            return {"success": False, "error": f"Unknown target: {target}"}
        
        category = classification.get("category", "unknown")
        confidence = classification.get("confidence", 0.0)
        
        logger.info(f"Classified {target} failure: {category} (confidence: {confidence:.2f})")
        
        # Only apply fix if confidence is high enough
        if confidence < 0.85:
            # Low confidence - create PR with diagnosis only
            logger.info(f"Confidence too low ({confidence:.2f} < 0.85), creating diagnosis PR only")
            return self._create_diagnosis_pr(target, status, classification, mode)
        
        # Apply the patch
        repo_root = Path.cwd()
        if target == "vercel":
            patch_result = apply_patch_vercel(category, classification, repo_root, dry_run=dry_run)
        elif target == "render":
            patch_result = apply_patch_render(category, classification, repo_root, dry_run=dry_run)
        else:
            return {"success": False, "error": f"Unknown target: {target}"}
        
        if not patch_result.get("success"):
            # Patch application failed - create diagnosis PR instead
            logger.warning(f"Patch application failed: {patch_result.get('error')}")
            return self._create_diagnosis_pr(target, status, classification, mode)
        
        files_changed = patch_result.get("files_changed", [])
        
        # Run minimal local check if applicable
        if files_changed and target == "vercel":
            # Check if we modified package.json - try a quick validation
            for file_path in files_changed:
                if "package.json" in file_path:
                    try:
                        import json
                        with open(file_path, "r") as f:
                            json.load(f)  # Validate JSON
                    except Exception as e:
                        logger.warning(f"package.json validation failed: {e}")
                        return {
                            "success": False,
                            "error": f"Generated package.json is invalid: {e}"
                        }
        
        # In dry-run mode, return without committing
        if dry_run:
            return {
                "success": True,
                "files_changed": files_changed,
                "commit_message": f"Would commit: Fix: {target} {category} (auto-repair confidence: {confidence:.0%})",
                "category": category,
                "confidence": confidence,
                "dry_run": True,
                "diff": patch_result.get("diff", "")
            }
        
        # Commit and push
        if not self.github_client:
            return {"success": False, "error": "GitHub client not available"}
        
        if mode == "pr":
            branch_name = f"fix/{target}-{category}-{int(time.time())}"
            if not self.github_client.create_branch(branch_name):
                return {"success": False, "error": "Failed to create branch"}
        
        commit_msg = f"Fix: {target} {category} (auto-repair confidence: {confidence:.0%})"
        if not self.github_client.commit_changes(commit_msg, files_changed):
            return {"success": False, "error": "Failed to commit changes"}
        
        push_result = self.github_client.push(
            branch=self.github_client.get_current_branch(),
            remote="origin"
        )
        
        if push_result.get("success"):
            return {
                "success": True,
                "files_changed": files_changed,
                "commit_message": commit_msg,
                "category": category,
                "confidence": confidence,
                "classification": classification
            }
        else:
            return {
                "success": False,
                "error": f"Failed to push: {push_result.get('error')}"
            }
    
    def _create_diagnosis_pr(self, target: str, status: Dict[str, Any], classification: Dict[str, Any], mode: str) -> Dict[str, Any]:
        """Create a PR with diagnosis only (low confidence or patch failed)"""
        if not self.github_client:
            return {"success": False, "error": "GitHub client not available"}
        
        # Create diagnosis document
        diagnosis_file = Path("docs/deploy_failures_latest.md")
        diagnosis_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(diagnosis_file, "w") as f:
            f.write(f"# Deployment Failure Diagnosis - {target}\n\n")
            f.write(f"**Target:** {target}\n")
            f.write(f"**Category:** {classification.get('category', 'unknown')}\n")
            f.write(f"**Confidence:** {classification.get('confidence', 0):.0%}\n\n")
            
            patch_info = classification.get("suggested_patch", {})
            f.write(f"**Recommended Action:**\n")
            f.write(f"{patch_info.get('message', 'Manual review required')}\n\n")
            
            f.write(f"**Key Errors:**\n")
            for error in classification.get("key_errors", [])[:10]:
                f.write(f"- {error}\n")
            
            f.write(f"\n**Full Log Summary:**\n")
            f.write(f"```\n{status.get('logs_summary', '')[:2000]}\n```\n")
        
        if mode == "pr":
            branch_name = f"diagnosis/{target}-{int(time.time())}"
            if not self.github_client.create_branch(branch_name):
                return {"success": False, "error": "Failed to create branch"}
        
        commit_msg = f"Diagnosis: {target} deployment failure ({classification.get('category', 'unknown')})"
        if not self.github_client.commit_changes(commit_msg, [str(diagnosis_file)]):
            return {"success": False, "error": "Failed to commit diagnosis"}
        
        push_result = self.github_client.push(
            branch=self.github_client.get_current_branch(),
            remote="origin"
        )
        
        if push_result.get("success"):
            return {
                "success": True,
                "files_changed": [str(diagnosis_file)],
                "commit_message": commit_msg,
                "diagnosis_only": True,
                "category": classification.get("category"),
                "confidence": classification.get("confidence", 0)
            }
        else:
            return {
                "success": False,
                "error": f"Failed to push diagnosis: {push_result.get('error')}"
            }

