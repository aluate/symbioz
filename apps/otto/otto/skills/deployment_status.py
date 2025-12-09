"""
DeploymentStatusSkill - Checks deployment status across Vercel, Render, Stripe, and Cloudflare
Uses existing infrastructure API clients to check deployment health
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add infra directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "infra"))

from ..core.models import Task, TaskResult, TaskStatus
from ..core.skill_base import Skill, SkillHealthIssue, SkillContext
from ..core.logging_utils import get_logger

logger = get_logger(__name__)


class DeploymentStatusSkill:
    """Skill that checks deployment status across platforms"""
    
    name = "deployment_status"
    description = "Checks deployment status across Vercel, Render, Stripe, Cloudflare, and GitHub"
    
    def __init__(self):
        """Initialize the skill with infrastructure clients"""
        self.vercel_client = None
        self.render_client = None
        self.stripe_client = None
        self.github_client = None
        
        # Try to initialize clients if API keys are available
        self._init_clients()
    
    def _init_clients(self):
        """Initialize infrastructure API clients if keys are available"""
        try:
            from infra.providers.vercel_client import VercelClient
            from infra.providers.render_client import RenderClient
            from infra.providers.stripe_client import StripeClient
            from infra.providers.github_client import GitHubClient
            from infra.utils.yaml_loader import load_provider_configs
            
            # Load provider configs
            configs = load_provider_configs()
            env = os.getenv("OTTO_ENV", "prod")
            
            # Initialize Vercel client if token available
            if os.getenv("VERCEL_TOKEN") and "vercel" in configs:
                try:
                    self.vercel_client = VercelClient(
                        configs.get("vercel", {}),
                        env=env,
                        dry_run=False
                    )
                except Exception as e:
                    logger.warning(f"Could not initialize Vercel client: {e}")
            
            # Initialize Render client if API key available
            if os.getenv("RENDER_API_KEY") and "render" in configs:
                try:
                    self.render_client = RenderClient(
                        configs.get("render", {}),
                        env=env,
                        dry_run=False
                    )
                except Exception as e:
                    logger.warning(f"Could not initialize Render client: {e}")
            
            # Initialize Stripe client if API key available
            if os.getenv("STRIPE_SECRET_KEY") and "stripe" in configs:
                try:
                    self.stripe_client = StripeClient(
                        configs.get("stripe", {}),
                        env=env,
                        dry_run=False
                    )
                except Exception as e:
                    logger.warning(f"Could not initialize Stripe client: {e}")
            
            # Initialize GitHub client if token available
            if os.getenv("GITHUB_TOKEN") and "github" in configs:
                try:
                    self.github_client = GitHubClient(
                        configs.get("github", {}),
                        env=env,
                        dry_run=False
                    )
                except Exception as e:
                    logger.warning(f"Could not initialize GitHub client: {e}")
                    
        except ImportError as e:
            logger.warning(f"Could not import infrastructure clients: {e}")
        except Exception as e:
            logger.warning(f"Error initializing clients: {e}")
    
    def can_handle(self, task: Task) -> bool:
        """Check if this skill can handle the task"""
        return task.type in [
            "deployment.check_status",
            "deployment.check_vercel",
            "deployment.check_render",
            "deployment.check_stripe",
            "deployment.check_cloudflare",
            "deployment.check_all",
            "infra.check_deployments",
            "check_deployment_status",
        ]
    
    def run(self, task: Task, context: SkillContext) -> TaskResult:
        """Execute the deployment status check"""
        try:
            task_type = task.type
            
            if task_type in ["deployment.check_all", "infra.check_deployments", "check_deployment_status"]:
                return self._check_all_platforms(task, context)
            elif task_type == "deployment.check_vercel":
                return self._check_vercel(task, context)
            elif task_type == "deployment.check_render":
                return self._check_render(task, context)
            elif task_type == "deployment.check_stripe":
                return self._check_stripe(task, context)
            elif task_type == "deployment.check_cloudflare":
                return self._check_cloudflare(task, context)
            elif task_type == "deployment.check_status":
                # Check specific platform from task payload
                platform = task.payload.get("platform", "all")
                if platform == "vercel":
                    return self._check_vercel(task, context)
                elif platform == "render":
                    return self._check_render(task, context)
                elif platform == "stripe":
                    return self._check_stripe(task, context)
                elif platform == "cloudflare":
                    return self._check_cloudflare(task, context)
                else:
                    return self._check_all_platforms(task, context)
            else:
                return TaskResult(
                    task_id=task.id,
                    success=False,
                    message=f"Unknown deployment check type: {task_type}"
                )
        except Exception as e:
            logger.error(f"Error in DeploymentStatusSkill: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error checking deployment status: {str(e)}"
            )
    
    def _check_all_platforms(self, task: Task, context: SkillContext) -> TaskResult:
        """Check status across all platforms"""
        results = {}
        summary_parts = []
        
        # Check Vercel
        if self.vercel_client:
            try:
                vercel_result = self.vercel_client.check_health()
                results["vercel"] = vercel_result
                summary_parts.append(f"Vercel: {vercel_result.get('human_summary', 'Unknown')}")
            except Exception as e:
                results["vercel"] = {"status": "error", "error": str(e)}
                summary_parts.append(f"Vercel: Error - {str(e)}")
        else:
            results["vercel"] = {"status": "warn", "message": "VERCEL_TOKEN not configured"}
            summary_parts.append("Vercel: ⚠️ Not configured (missing VERCEL_TOKEN)")
        
        # Check Render
        if self.render_client:
            try:
                render_result = self.render_client.check_health()
                results["render"] = render_result
                summary_parts.append(f"Render: {render_result.get('human_summary', 'Unknown')}")
            except Exception as e:
                results["render"] = {"status": "error", "error": str(e)}
                summary_parts.append(f"Render: Error - {str(e)}")
        else:
            results["render"] = {"status": "warn", "message": "RENDER_API_KEY not configured"}
            summary_parts.append("Render: ⚠️ Not configured (missing RENDER_API_KEY)")
        
        # Check Stripe
        if self.stripe_client:
            try:
                stripe_result = self.stripe_client.check_health()
                results["stripe"] = stripe_result
                summary_parts.append(f"Stripe: {stripe_result.get('human_summary', 'Unknown')}")
            except Exception as e:
                results["stripe"] = {"status": "error", "error": str(e)}
                summary_parts.append(f"Stripe: Error - {str(e)}")
        else:
            results["stripe"] = {"status": "warn", "message": "STRIPE_SECRET_KEY not configured"}
            summary_parts.append("Stripe: ⚠️ Not configured (missing STRIPE_SECRET_KEY)")
        
        # Check GitHub
        if self.github_client:
            try:
                github_result = self.github_client.check_health()
                results["github"] = github_result
                summary_parts.append(f"GitHub: {github_result.get('human_summary', 'Unknown')}")
            except Exception as e:
                results["github"] = {"status": "error", "error": str(e)}
                summary_parts.append(f"GitHub: Error - {str(e)}")
        else:
            results["github"] = {"status": "warn", "message": "GITHUB_TOKEN not configured"}
            summary_parts.append("GitHub: ⚠️ Not configured (missing GITHUB_TOKEN)")
        
        # Check Cloudflare (note: no client yet, so just report status)
        results["cloudflare"] = {
            "status": "warn",
            "message": "Cloudflare API client not yet implemented"
        }
        summary_parts.append("Cloudflare: ⚠️ API client not implemented")
        
        # Determine overall status
        statuses = [r.get("status") for r in results.values()]
        if "error" in statuses:
            overall_status = "error"
        elif "warn" in statuses:
            overall_status = "warn"
        else:
            overall_status = "ok"
        
        message = "\n".join(summary_parts)
        
        return TaskResult(
            task_id=task.id,
            success=overall_status != "error",
            message=message,
            data={
                "platforms": results,
                "overall_status": overall_status,
            }
        )
    
    def _check_vercel(self, task: Task, context: SkillContext) -> TaskResult:
        """Check Vercel deployment status"""
        if not self.vercel_client:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Vercel client not available. Set VERCEL_TOKEN environment variable.",
                data={"status": "not_configured"}
            )
        
        try:
            result = self.vercel_client.check_health()
            return TaskResult(
                task_id=task.id,
                success=result.get("status") != "error",
                message=result.get("human_summary", "Vercel status check completed"),
                data=result
            )
        except Exception as e:
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error checking Vercel: {str(e)}"
            )
    
    def _check_render(self, task: Task, context: SkillContext) -> TaskResult:
        """Check Render deployment status"""
        if not self.render_client:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Render client not available. Set RENDER_API_KEY environment variable.",
                data={"status": "not_configured"}
            )
        
        try:
            result = self.render_client.check_health()
            return TaskResult(
                task_id=task.id,
                success=result.get("status") != "error",
                message=result.get("human_summary", "Render status check completed"),
                data=result
            )
        except Exception as e:
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error checking Render: {str(e)}"
            )
    
    def _check_stripe(self, task: Task, context: SkillContext) -> TaskResult:
        """Check Stripe status"""
        if not self.stripe_client:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Stripe client not available. Set STRIPE_SECRET_KEY environment variable.",
                data={"status": "not_configured"}
            )
        
        try:
            result = self.stripe_client.check_health()
            return TaskResult(
                task_id=task.id,
                success=result.get("status") != "error",
                message=result.get("human_summary", "Stripe status check completed"),
                data=result
            )
        except Exception as e:
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error checking Stripe: {str(e)}"
            )
    
    def _check_cloudflare(self, task: Task, context: SkillContext) -> TaskResult:
        """Check Cloudflare status (placeholder - client not yet implemented)"""
        return TaskResult(
            task_id=task.id,
            success=False,
            message="Cloudflare API client not yet implemented. Would need CLOUDFLARE_API_TOKEN environment variable.",
            data={
                "status": "not_implemented",
                "note": "Cloudflare API client needs to be created in infra/providers/cloudflare_client.py"
            }
        )
    
    def self_test(self, context: SkillContext) -> List[SkillHealthIssue]:
        """Run health checks on this skill"""
        issues = []
        
        # Check if any clients are available
        if not any([self.vercel_client, self.render_client, self.stripe_client, self.github_client]):
            issues.append(SkillHealthIssue(
                code="no_api_keys",
                message="No API keys configured. Set VERCEL_TOKEN, RENDER_API_KEY, STRIPE_SECRET_KEY, or GITHUB_TOKEN to enable deployment checks.",
                suggestion="See infra/FINDING_YOUR_KEYS_AND_IDS.md for instructions"
            ))
        
        return issues

