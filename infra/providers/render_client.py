"""Render API client for diagnostics and provisioning."""

import json
import time
from typing import Any, Dict, List, Optional

import httpx

from infra.providers.base import BaseProvider, ProviderCheckResult


class RenderClient(BaseProvider):
    """Client for Render API operations."""

    API_BASE_URL = "https://api.render.com/v1"

    def __init__(self, config: Dict[str, Any], env: str = "prod", dry_run: bool = False):
        super().__init__(config, env, dry_run)
        self.api_key = self._require_env_var("RENDER_API_KEY")
        self.services = config.get("services", {})

    def validate_config(self) -> bool:
        """Validate Render configuration."""
        if not self.services:
            return False
        return True

    def _get_headers(self) -> Dict[str, str]:
        """Get API request headers."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def check_health(self) -> ProviderCheckResult:
        """Check health of all configured Render services."""
        if self.dry_run:
            return {
                "provider": "render",
                "status": "ok",
                "human_summary": "[DRY RUN] Would check Render services",
                "details": {"dry_run": True},
            }

        service_results = []
        overall_status = "ok"

        for service_name, service_config in self.services.items():
            if service_config.get("env") != self.env:
                continue

            service_id = service_config.get("render_service_id")
            if not service_id:
                continue

            try:
                result = self._check_service(service_id, service_name, service_config)
                service_results.append(result)

                if result["status"] == "error":
                    overall_status = "error"
                elif result["status"] == "warn" and overall_status == "ok":
                    overall_status = "warn"

            except Exception as e:
                service_results.append({
                    "service": service_name,
                    "status": "error",
                    "error": str(e),
                })
                overall_status = "error"

        # Build summary
        error_count = sum(1 for r in service_results if r.get("status") == "error")
        warn_count = sum(1 for r in service_results if r.get("status") == "warn")

        if error_count > 0:
            summary = f"❌ {error_count} service(s) have errors"
        elif warn_count > 0:
            summary = f"⚠️ {warn_count} service(s) have warnings"
        else:
            summary = f"✅ All {len(service_results)} service(s) healthy"

        return {
            "provider": "render",
            "status": overall_status,
            "human_summary": summary,
            "details": {
                "services": service_results,
                "total_services": len(service_results),
            },
        }

    def _check_service(
        self, service_id: str, service_name: str, service_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Check a single Render service."""
        result = {
            "service": service_name,
            "service_id": service_id,
            "status": "ok",
        }

        # Get service info
        try:
            service_info = self._get_service(service_id)
            result["service_url"] = service_info.get("service", {}).get("serviceDetails", {}).get("url")
            result["deploy_status"] = service_info.get("service", {}).get("deployStatus")
        except Exception as e:
            result["status"] = "error"
            result["error"] = f"Failed to get service info: {e}"
            return result

        # Get latest deployment
        try:
            deployments = self._get_deployments(service_id, limit=1)
            if deployments:
                latest_deploy = deployments[0]
                result["latest_deployment"] = {
                    "id": latest_deploy.get("deploy", {}).get("id"),
                    "status": latest_deploy.get("deploy", {}).get("status"),
                    "commit": latest_deploy.get("deploy", {}).get("commit", {}).get("id"),
                    "created_at": latest_deploy.get("deploy", {}).get("createdAt"),
                }

                deploy_status = result["latest_deployment"]["status"]
                if deploy_status in ["live", "update_recommended"]:
                    result["status"] = "ok"
                elif deploy_status == "build_failed":
                    result["status"] = "error"
                    # Try to get error logs
                    try:
                        deploy_id = result["latest_deployment"]["id"]
                        logs = self._get_deploy_logs(service_id, deploy_id, lines=50)
                        result["error_logs"] = logs[-500:] if logs else "No logs available"
                    except Exception:
                        pass
                else:
                    result["status"] = "warn"
        except Exception as e:
            result["status"] = "warn"
            result["warning"] = f"Could not check deployments: {e}"

        # Health check if URL available
        health_path = service_config.get("health_check_path")
        if health_path and result.get("service_url"):
            try:
                from infra.utils.health_check import check_health

                health_url = f"{result['service_url']}{health_path}"
                health_result = check_health(health_url, timeout=5)
                result["health_check"] = health_result

                if health_result["status"] == "error":
                    result["status"] = "error"
                elif health_result["status"] == "warn" and result["status"] == "ok":
                    result["status"] = "warn"
            except Exception as e:
                result["warning"] = f"Health check failed: {e}"

        return result

    def _get_service(self, service_id: str) -> Dict[str, Any]:
        """Get service details from Render API."""
        url = f"{self.API_BASE_URL}/services/{service_id}"
        with httpx.Client() as client:
            response = client.get(url, headers=self._get_headers(), timeout=30)
            response.raise_for_status()
            return response.json()

    def _get_deployments(self, service_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get deployments for a service."""
        url = f"{self.API_BASE_URL}/services/{service_id}/deploys"
        params = {"limit": limit}
        with httpx.Client() as client:
            response = client.get(url, headers=self._get_headers(), params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            # Handle both list and dict responses from Render API
            if isinstance(data, list):
                return data
            else:
                return data.get("deploys", [])

    def _get_deploy_logs(self, service_id: str, deploy_id: str, lines: int = 100) -> str:
        """Get deployment logs."""
        # Try different log endpoints
        endpoints = [
            f"{self.API_BASE_URL}/services/{service_id}/deploys/{deploy_id}/logs",
            f"{self.API_BASE_URL}/services/{service_id}/deploys/{deploy_id}/events",
        ]
        
        for url in endpoints:
            try:
                params = {"lines": lines} if "logs" in url else {}
                with httpx.Client() as client:
                    response = client.get(url, headers=self._get_headers(), params=params, timeout=30)
                    response.raise_for_status()
                    data = response.json()
                    # Handle different response formats
                    if isinstance(data, str):
                        return data
                    elif isinstance(data, dict):
                        return data.get("logs", data.get("message", ""))
                    elif isinstance(data, list):
                        # Events format
                        return "\n".join([str(event) for event in data[-lines:]])
                    return str(data)
            except Exception:
                continue
        
        # If all endpoints fail, try getting deploy details which might have error info
        try:
            deploy = self._get_deploy(service_id, deploy_id)
            if isinstance(deploy, dict):
                deploy_data = deploy.get("deploy", deploy)
                if isinstance(deploy_data, dict):
                    return deploy_data.get("message", deploy_data.get("error", "No error details available"))
        except Exception:
            pass
        
        return "Could not retrieve logs"

    # Provisioning methods

    def ensure_service(self, service_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Create or update a Render service."""
        if self.dry_run:
            self._log_if_dry_run("create/update Render service", service_spec)
            return {"service_id": "mock-service-id", "url": "https://mock.onrender.com"}

        service_id = service_spec.get("service_id")
        if service_id:
            # Update existing service
            return self._update_service(service_id, service_spec)
        else:
            # Create new service
            return self._create_service(service_spec)

    def _create_service(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new Render service."""
        payload = {
            "type": "web_service",
            "name": spec["name"],
            "repo": spec.get("repo"),
            "branch": spec.get("branch", "main"),
            "buildCommand": spec.get("build_command"),
            "startCommand": spec.get("start_command"),
            "envVars": spec.get("env_vars", {}),
        }

        url = f"{self.API_BASE_URL}/services"
        with httpx.Client() as client:
            response = client.post(url, headers=self._get_headers(), json=payload, timeout=60)
            response.raise_for_status()
            return response.json()

    def _update_service(self, service_id: str, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing Render service."""
        payload = {}
        if "build_command" in spec:
            payload["buildCommand"] = spec["build_command"]
        if "start_command" in spec:
            payload["startCommand"] = spec["start_command"]

        url = f"{self.API_BASE_URL}/services/{service_id}"
        with httpx.Client() as client:
            response = client.patch(url, headers=self._get_headers(), json=payload, timeout=60)
            response.raise_for_status()
            return response.json()

    def set_env_vars(self, service_id: str, env_vars: Dict[str, str]) -> None:
        """Set environment variables for a service."""
        if self.dry_run:
            self._log_if_dry_run("set environment variables", {"service_id": service_id, "count": len(env_vars)})
            return

        # Render API: set env vars one at a time or batch
        url = f"{self.API_BASE_URL}/services/{service_id}/env-vars"
        
        # Get existing env vars first
        with httpx.Client() as client:
            response = client.get(url, headers=self._get_headers(), timeout=30)
            response.raise_for_status()
            data = response.json()
            # Handle both list and dict responses from Render API
            if isinstance(data, list):
                env_vars_list = data
            else:
                env_vars_list = data.get("envVars", [])
            existing = {item["key"]: item.get("id") for item in env_vars_list if isinstance(item, dict) and "key" in item}

        # Update/create each env var
        with httpx.Client() as client:
            for key, value in env_vars.items():
                if key in existing:
                    # Update existing
                    var_id = existing[key]
                    patch_url = f"{url}/{var_id}"
                    payload = {"value": value}
                    client.patch(patch_url, headers=self._get_headers(), json=payload, timeout=30)
                else:
                    # Create new
                    payload = {"key": key, "value": value}
                    client.post(url, headers=self._get_headers(), json=payload, timeout=30)

    def trigger_deploy(self, service_id: str, branch: Optional[str] = None) -> Dict[str, Any]:
        """Trigger a deployment."""
        if self.dry_run:
            self._log_if_dry_run("trigger deployment", {"service_id": service_id, "branch": branch})
            return {"deploy_id": "mock-deploy-id", "status": "queued"}

        url = f"{self.API_BASE_URL}/services/{service_id}/deploys"
        payload = {}
        if branch:
            payload["clearCache"] = "do_not_clear"

        with httpx.Client() as client:
            response = client.post(url, headers=self._get_headers(), json=payload, timeout=60)
            response.raise_for_status()
            return response.json()

    def wait_for_deploy(
        self, service_id: str, deploy_id: str, timeout: int = 600, poll_interval: int = 5
    ) -> Dict[str, Any]:
        """Wait for a deployment to complete."""
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                deploy = self._get_deploy(service_id, deploy_id)
                status = deploy.get("deploy", {}).get("status")

                if status in ["live", "build_failed", "update_failed"]:
                    return deploy

                time.sleep(poll_interval)
            except Exception as e:
                # Continue polling on transient errors
                time.sleep(poll_interval)

        raise TimeoutError(f"Deployment {deploy_id} did not complete within {timeout}s")

    def _get_deploy(self, service_id: str, deploy_id: str) -> Dict[str, Any]:
        """Get deployment details."""
        url = f"{self.API_BASE_URL}/services/{service_id}/deploys/{deploy_id}"
        with httpx.Client() as client:
            response = client.get(url, headers=self._get_headers(), timeout=30)
            response.raise_for_status()
            return response.json()

