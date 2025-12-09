"""Vercel client for diagnostics, provisioning, and auto-fixing deployments."""

import logging
import time
from typing import Any, Dict, List, Optional

import httpx

from infra.providers.base import BaseProvider, ProviderCheckResult

logger = logging.getLogger(__name__)


class VercelClient(BaseProvider):
    """Client for Vercel API operations."""

    API_BASE_URL = "https://api.vercel.com"

    def __init__(self, config: Dict[str, Any], env: str = "prod", dry_run: bool = False):
        super().__init__(config, env, dry_run)
        self.token = self._require_env_var("VERCEL_TOKEN")
        self.team_id = config.get("team_id")
        self.projects = config.get("projects", {})

    def validate_config(self) -> bool:
        """Validate Vercel configuration."""
        return True  # Vercel config is optional

    def _get_headers(self) -> Dict[str, str]:
        """Get API request headers."""
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        if self.team_id:
            headers["x-vercel-team-id"] = self.team_id
        return headers

    def check_health(self) -> ProviderCheckResult:
        """Check health of Vercel deployments."""
        if self.dry_run:
            return {
                "provider": "vercel",
                "status": "ok",
                "human_summary": "[DRY RUN] Would check Vercel deployments",
                "details": {"dry_run": True},
            }

        if not self.projects:
            return {
                "provider": "vercel",
                "status": "warn",
                "human_summary": "⚠️ No Vercel projects configured",
                "details": {"note": "Add projects to infra/providers/vercel.yaml"},
            }

        project_results = []
        overall_status = "ok"

        for project_name, project_config in self.projects.items():
            try:
                result = self._check_project(project_name, project_config)
                project_results.append(result)

                if result["status"] == "error":
                    overall_status = "error"
                elif result["status"] == "warn" and overall_status == "ok":
                    overall_status = "warn"

            except Exception as e:
                project_results.append({
                    "project": project_name,
                    "status": "error",
                    "error": str(e),
                })
                overall_status = "error"

        error_count = sum(1 for r in project_results if r.get("status") == "error")
        warn_count = sum(1 for r in project_results if r.get("status") == "warn")

        if error_count > 0:
            summary = f"❌ {error_count} project(s) have errors"
        elif warn_count > 0:
            summary = f"⚠️ {warn_count} project(s) have warnings"
        elif project_results:
            summary = f"✅ All {len(project_results)} project(s) healthy"
        else:
            summary = "⚠️ No projects configured"

        return {
            "provider": "vercel",
            "status": overall_status,
            "human_summary": summary,
            "details": {
                "projects": project_results,
                "total_projects": len(project_results),
            },
        }

    def _check_project(self, project_name: str, project_config: Dict[str, Any]) -> Dict[str, Any]:
        """Check a single Vercel project."""
        result = {
            "project": project_name,
            "status": "ok",
        }

        try:
            # Get project
            project_id = project_config.get("project_id") or project_name
            project = self._get_project(project_id)
            
            if not project:
                result["status"] = "error"
                result["error"] = f"Project '{project_id}' not found"
                return result

            result["project_id"] = project.get("id")
            result["name"] = project.get("name")
            result["url"] = project.get("link", {}).get("url")

            # Get latest deployment
            deployments = self._list_deployments(project_id, limit=1)
            if deployments:
                latest = deployments[0]
                result["latest_deployment"] = {
                    "id": latest.get("uid"),
                    "url": latest.get("url"),
                    "state": latest.get("state"),
                    "created_at": latest.get("createdAt"),
                }

                state = latest.get("state")
                if state in ["ERROR", "CANCELED"]:
                    result["status"] = "error"
                    result["error"] = f"Deployment {state.lower()}"
                elif state == "BUILDING":
                    result["status"] = "warn"
                    result["warning"] = "Deployment in progress"
            else:
                result["status"] = "warn"
                result["warning"] = "No deployments found"

        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)

        return result

    def _get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get project details."""
        if self.dry_run:
            return {"id": project_id, "name": project_id}

        url = f"{self.API_BASE_URL}/v9/projects/{project_id}"
        with httpx.Client() as client:
            try:
                response = client.get(url, headers=self._get_headers(), timeout=30)
                if response.status_code == 404:
                    return None
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError:
                return None

    def _list_deployments(
        self, project_id: str, limit: int = 10, state: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List deployments for a project."""
        if self.dry_run:
            return []

        url = f"{self.API_BASE_URL}/v6/deployments"
        params = {"projectId": project_id, "limit": limit}
        if state:
            params["state"] = state

        with httpx.Client() as client:
            response = client.get(url, headers=self._get_headers(), params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get("deployments", [])

    def get_deployment_logs(self, deployment_id: str) -> List[str]:
        """Get build logs for a deployment."""
        if self.dry_run:
            return ["[DRY RUN] Would fetch deployment logs"]

        url = f"{self.API_BASE_URL}/v2/deployments/{deployment_id}/events"
        logs = []

        with httpx.Client() as client:
            try:
                response = client.get(url, headers=self._get_headers(), timeout=60)
                response.raise_for_status()
                events = response.json()
                
                for event in events:
                    if "payload" in event:
                        payload = event["payload"]
                        if isinstance(payload, dict) and "text" in payload:
                            logs.append(payload["text"])
                        elif isinstance(payload, str):
                            logs.append(payload)
            except Exception as e:
                logs.append(f"Error fetching logs: {e}")

        return logs

    def get_deployment(self, deployment_id: str) -> Optional[Dict[str, Any]]:
        """Get deployment details."""
        if self.dry_run:
            return {"uid": deployment_id, "state": "READY"}

        url = f"{self.API_BASE_URL}/v13/deployments/{deployment_id}"
        with httpx.Client() as client:
            try:
                response = client.get(url, headers=self._get_headers(), timeout=30)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError:
                return None

    def trigger_redeploy(self, deployment_id: str) -> Optional[Dict[str, Any]]:
        """Redeploy a specific deployment."""
        if self.dry_run:
            self._log_if_dry_run("redeploy", {"deployment_id": deployment_id})
            return {"uid": "mock-deploy-id", "state": "QUEUED"}

        # Get original deployment to get project info
        deployment = self.get_deployment(deployment_id)
        if not deployment:
            return None

        # Create new deployment from same source
        url = f"{self.API_BASE_URL}/v13/deployments"
        payload = {
            "name": deployment.get("name"),
            "project": deployment.get("projectId"),
        }

        with httpx.Client() as client:
            response = client.post(url, headers=self._get_headers(), json=payload, timeout=60)
            response.raise_for_status()
            return response.json()

    def set_environment_variable(
        self, project_id: str, key: str, value: str, environments: List[str] = None
    ) -> bool:
        """Set an environment variable for a project."""
        if self.dry_run:
            self._log_if_dry_run("set environment variable", {"project": project_id, "key": key})
            return True

        if environments is None:
            environments = ["production", "preview", "development"]

        url = f"{self.API_BASE_URL}/v10/projects/{project_id}/env"
        payload = {
            "key": key,
            "value": value,
            "type": "encrypted",
            "target": environments,
        }

        with httpx.Client() as client:
            try:
                response = client.post(url, headers=self._get_headers(), json=payload, timeout=30)
                response.raise_for_status()
                return True
            except httpx.HTTPStatusError:
                # Try updating existing
                try:
                    # Get existing env vars
                    list_url = f"{self.API_BASE_URL}/v10/projects/{project_id}/env"
                    list_response = client.get(list_url, headers=self._get_headers(), timeout=30)
                    list_response.raise_for_status()
                    env_vars = list_response.json().get("envs", [])
                    
                    # Find and update
                    for env_var in env_vars:
                        if env_var.get("key") == key:
                            update_url = f"{self.API_BASE_URL}/v10/projects/{project_id}/env/{env_var['id']}"
                            update_payload = {"value": value, "target": environments}
                            update_response = client.patch(
                                update_url, headers=self._get_headers(), json=update_payload, timeout=30
                            )
                            update_response.raise_for_status()
                            return True
                except Exception:
                    pass
                return False

    def wait_for_deployment(
        self, deployment_id: str, timeout: int = 600, poll_interval: int = 5
    ) -> Dict[str, Any]:
        """Wait for a deployment to complete."""
        start_time = time.time()

        while time.time() - start_time < timeout:
            deployment = self.get_deployment(deployment_id)
            if not deployment:
                break

            state = deployment.get("readyState")
            if state in ["READY", "ERROR", "CANCELED"]:
                return deployment

            time.sleep(poll_interval)

        raise TimeoutError(f"Deployment {deployment_id} did not complete within {timeout}s")

    def detect_errors_from_logs(self, logs: List[str]) -> List[Dict[str, Any]]:
        """Detect common errors from build logs."""
        errors = []
        log_text = "\n".join(logs).lower()

        # Missing environment variable
        if "environment variable" in log_text or "env" in log_text and "undefined" in log_text:
            # Try to extract variable name
            import re
            matches = re.findall(r"([A-Z_][A-Z0-9_]*).*?(?:undefined|not defined|missing)", log_text, re.IGNORECASE)
            for var_name in matches:
                errors.append({
                    "type": "missing_env_var",
                    "variable": var_name,
                    "fixable": True,
                })

        # Build errors
        if "error" in log_text and ("build" in log_text or "failed" in log_text):
            errors.append({
                "type": "build_error",
                "fixable": False,  # Usually requires code changes
            })

        # Module not found
        if "module not found" in log_text or "cannot find module" in log_text:
            errors.append({
                "type": "missing_dependency",
                "fixable": False,  # Requires package.json update
            })

        # TypeScript errors
        if "typescript" in log_text and "error" in log_text:
            errors.append({
                "type": "typescript_error",
                "fixable": False,  # Requires code fixes
            })

        return errors

    def create_project(
        self, name: str, git_repo: Optional[str] = None, root_directory: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Create a new Vercel project."""
        if self.dry_run:
            self._log_if_dry_run("create Vercel project", {"name": name, "git_repo": git_repo})
            return {"id": f"prj_mock_{name}", "name": name}

        url = f"{self.API_BASE_URL}/v10/projects"
        payload = {"name": name}
        
        if git_repo:
            # Parse git_repo format: "owner/repo"
            parts = git_repo.split("/")
            if len(parts) == 2:
                payload["gitRepository"] = {
                    "type": "github",
                    "repo": parts[1],
                    "org": parts[0],
                }
        
        if root_directory:
            payload["rootDirectory"] = root_directory

        with httpx.Client() as client:
            try:
                response = client.post(url, headers=self._get_headers(), json=payload, timeout=30)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 409:
                    # Project already exists, return existing
                    return self._get_project(name)
                raise

    def add_domain(self, project_id: str, domain: str) -> Dict[str, Any]:
        """Add a custom domain to a Vercel project."""
        if self.dry_run:
            self._log_if_dry_run("add domain", {"project": project_id, "domain": domain})
            return {"domain": domain, "status": "pending"}

        url = f"{self.API_BASE_URL}/v9/projects/{project_id}/domains"
        payload = {"name": domain}

        with httpx.Client() as client:
            try:
                response = client.post(url, headers=self._get_headers(), json=payload, timeout=30)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError:
                # Domain might already exist, get existing domain config
                try:
                    list_url = f"{self.API_BASE_URL}/v9/projects/{project_id}/domains"
                    list_response = client.get(list_url, headers=self._get_headers(), timeout=30)
                    list_response.raise_for_status()
                    domains = list_response.json().get("domains", [])
                    for d in domains:
                        if d.get("name") == domain:
                            return d
                except Exception:
                    pass
                raise

    def get_domain_config(self, domain: str) -> Optional[Dict[str, Any]]:
        """Get DNS configuration for a domain."""
        if self.dry_run:
            return {"domain": domain, "dns_records": []}

        url = f"{self.API_BASE_URL}/v4/domains/{domain}/config"
        with httpx.Client() as client:
            try:
                response = client.get(url, headers=self._get_headers(), timeout=30)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError:
                return None

    def update_project_settings(
        self, project_id: str, root_directory: Optional[str] = None, **kwargs
    ) -> bool:
        """Update project settings (root directory, etc.)."""
        if self.dry_run:
            self._log_if_dry_run("update project settings", {"project": project_id, "root_directory": root_directory})
            return True

        url = f"{self.API_BASE_URL}/v9/projects/{project_id}"
        payload = {}
        
        if root_directory is not None:
            payload["rootDirectory"] = root_directory
        
        # Add any other settings from kwargs
        payload.update(kwargs)
        
        if not payload:
            return True  # Nothing to update

        with httpx.Client() as client:
            try:
                response = client.patch(url, headers=self._get_headers(), json=payload, timeout=30)
                response.raise_for_status()
                return True
            except httpx.HTTPStatusError as e:
                logger.error(f"Failed to update project settings: {e.response.text}")
                return False
