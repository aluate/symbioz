"""Vercel auto-fixer implementation."""

from typing import Any, Dict, List, Optional

from infra.providers.vercel_client import VercelClient
from infra.utils.fixer import BaseFixer, FixResult


class VercelFixer(BaseFixer):
    """Auto-fixer for Vercel deployments."""

    def __init__(
        self,
        vercel_client: VercelClient,
        project_name: str,
        project_config: Dict[str, Any],
        max_retries: int = 5,
    ):
        super().__init__(vercel_client, project_name, max_retries)
        self.client = vercel_client
        self.project_config = project_config
        self.project_id = project_config.get("project_id") or project_name

    def detect_issues(self) -> List[Dict[str, Any]]:
        """Detect issues from latest deployment."""
        issues = []

        # Get project details to check root directory
        project = self.client._get_project(self.project_id)
        if project:
            expected_root = self.project_config.get("root_directory")
            current_root = project.get("rootDirectory")
            
            if expected_root and current_root != expected_root:
                issues.append({
                    "type": "wrong_root_directory",
                    "current": current_root,
                    "expected": expected_root,
                    "fixable": True,
                })

        # Get latest deployment
        deployments = self.client._list_deployments(self.project_id, limit=1)
        if not deployments:
            return issues

        latest = deployments[0]
        state = latest.get("state")
        deployment_id = latest.get("uid")

        # Check if deployment succeeded but site returns 404 (root directory issue)
        if state == "READY":
            # Check if site is accessible (basic check)
            url = latest.get("url")
            if url:
                import httpx
                try:
                    response = httpx.get(f"https://{url}", timeout=10, follow_redirects=True)
                    if response.status_code == 404:
                        # Site is deployed but returns 404 - likely root directory issue
                        if not any(i.get("type") == "wrong_root_directory" for i in issues):
                            expected_root = self.project_config.get("root_directory")
                            if expected_root:
                                issues.append({
                                    "type": "wrong_root_directory",
                                    "current": current_root if project else None,
                                    "expected": expected_root,
                                    "fixable": True,
                                    "detected_from": "404_response",
                                })
                except Exception:
                    pass  # Can't check, skip

        if state not in ["ERROR", "CANCELED"]:
            return issues  # No build errors if deployment is successful

        # Get logs
        logs = self.client.get_deployment_logs(deployment_id)
        
        # Detect errors from logs
        detected_errors = self.client.detect_errors_from_logs(logs)
        issues.extend(detected_errors)

        # Check for missing env vars from project spec
        if self.project_config.get("required_env_vars"):
            deployment = self.client.get_deployment(deployment_id)
            if deployment:
                # Check if env vars are set (we'd need to get env vars from API)
                # For now, we'll detect from logs
                pass

        return issues

    def apply_fixes(self, issues: List[Dict[str, Any]]) -> FixResult:
        """Apply fixes for detected issues."""
        fixes_applied = []
        errors = []

        for issue in issues:
            issue_type = issue.get("type")

            if issue_type == "wrong_root_directory" and issue.get("fixable"):
                expected_root = issue.get("expected")
                if expected_root:
                    try:
                        success = self.client.update_project_settings(
                            self.project_id, root_directory=expected_root
                        )
                        if success:
                            fixes_applied.append(f"Updated root directory to: {expected_root}")
                        else:
                            errors.append(f"Failed to update root directory to {expected_root}")
                    except Exception as e:
                        errors.append(f"Error updating root directory: {e}")

            elif issue_type == "missing_env_var" and issue.get("fixable"):
                var_name = issue.get("variable")
                # Try to get value from project config or env
                var_value = self._get_env_var_value(var_name)
                
                if var_value:
                    try:
                        success = self.client.set_environment_variable(
                            self.project_id, var_name, var_value
                        )
                        if success:
                            fixes_applied.append(f"Set environment variable: {var_name}")
                        else:
                            errors.append(f"Failed to set {var_name}")
                    except Exception as e:
                        errors.append(f"Error setting {var_name}: {e}")
                else:
                    errors.append(f"Could not find value for {var_name}")

            elif issue_type in ["build_error", "missing_dependency", "typescript_error"]:
                # These require code changes, can't auto-fix
                errors.append(f"Cannot auto-fix {issue_type} - requires code changes")

        if fixes_applied:
            return FixResult(
                success=True,
                message=f"Applied {len(fixes_applied)} fix(es)",
                fixes_applied=fixes_applied,
                errors=errors if errors else None,
            )
        else:
            return FixResult(
                success=len(errors) == 0,
                message="No fixes could be applied automatically" if errors else "No fixes needed",
                errors=errors if errors else None,
            )

    def _get_env_var_value(self, var_name: str) -> Optional[str]:
        """Get environment variable value from config or environment."""
        import os

        # Check project config first
        env_vars = self.project_config.get("env_vars", {})
        if var_name in env_vars:
            return str(env_vars[var_name])

        # Check environment
        return os.environ.get(var_name)

    def trigger_redeploy(self) -> Optional[str]:
        """Trigger a redeployment."""
        deployments = self.client._list_deployments(self.project_id, limit=1)
        if not deployments:
            return None

        latest = deployments[0]
        deployment_id = latest.get("uid")
        
        new_deployment = self.client.trigger_redeploy(deployment_id)
        if new_deployment:
            return new_deployment.get("uid") or new_deployment.get("id")
        return None

    def wait_for_deployment(self, deployment_id: str) -> Dict[str, Any]:
        """Wait for deployment to complete."""
        return self.client.wait_for_deployment(deployment_id)

