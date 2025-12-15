"""
Lightweight Render API client for Otto monitor/repair loop
"""

import os
import time
from typing import Any, Dict, List, Optional
import httpx
from ..core.logging_utils import get_logger

logger = get_logger(__name__)


class RenderClient:
    """Client for Render API operations needed for monitoring and repair"""
    
    API_BASE_URL = "https://api.render.com/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("RENDER_API_KEY")
        if not self.api_key:
            raise ValueError("RENDER_API_KEY environment variable required")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get API request headers"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
    
    def list_deploys(self, service_id: str, limit: int = 1) -> List[Dict[str, Any]]:
        """List deploys for a Render service"""
        try:
            url = f"{self.API_BASE_URL}/services/{service_id}/deploys"
            params = {"limit": limit}
            
            with httpx.Client() as client:
                response = client.get(url, headers=self._get_headers(), params=params, timeout=30)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error listing Render deploys: {e}")
            return []
    
    def get_deploy_status(self, service_id: str, deploy_id: str) -> Dict[str, Any]:
        """Get deploy status"""
        try:
            url = f"{self.API_BASE_URL}/services/{service_id}/deploys/{deploy_id}"
            
            with httpx.Client() as client:
                response = client.get(url, headers=self._get_headers(), timeout=30)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error getting Render deploy status: {e}")
            return {"status": "error", "error": str(e)}
    
    def get_deploy_logs(self, service_id: str, deploy_id: str, lines: int = 100) -> str:
        """Fetch deploy logs"""
        try:
            # Render logs endpoint
            url = f"{self.API_BASE_URL}/logs"
            params = {
                "resource": f"deploy:{deploy_id}",
                "lines": lines
            }
            
            with httpx.Client() as client:
                response = client.get(url, headers=self._get_headers(), params=params, timeout=60)
                response.raise_for_status()
                data = response.json()
                # Render returns logs as a list of log entries
                log_entries = data.get("logs", [])
                return "\n".join(entry.get("message", "") for entry in log_entries)
        except Exception as e:
            logger.error(f"Error fetching Render deploy logs: {e}")
            return f"Error fetching logs: {str(e)}"
    
    def parse_errors_from_logs(self, logs: str) -> List[str]:
        """Parse errors from log text"""
        errors = []
        lines = logs.split("\n")
        for line in lines:
            if any(keyword in line.lower() for keyword in ["error", "failed", "failure", "exception"]):
                errors.append(line.strip())
        return errors[:20]  # Limit to 20 errors
    
    def get_service(self, service_id: str) -> Dict[str, Any]:
        """Get service details"""
        try:
            url = f"{self.API_BASE_URL}/services/{service_id}"
            
            with httpx.Client() as client:
                response = client.get(url, headers=self._get_headers(), timeout=30)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error getting Render service: {e}")
            return {}
    
    def update_service(self, service_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update Render service configuration.
        
        Args:
            service_id: Render service ID
            updates: Dictionary with serviceDetails to update, e.g.:
                {
                    "serviceDetails": {
                        "runtime": "docker",  # or "python", "node", etc.
                        "rootDir": "apps/otto",  # root directory for monorepos
                        "buildCommand": "pip install -r requirements.txt",
                        "startCommand": "python -m uvicorn otto.api:app --host 0.0.0.0 --port $PORT"
                    }
                }
        
        Returns:
            Updated service details or error dict
        """
        try:
            url = f"{self.API_BASE_URL}/services/{service_id}"
            
            with httpx.Client() as client:
                response = client.patch(url, headers=self._get_headers(), json=updates, timeout=30)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error updating Render service: {e}")
            return {"error": str(e), "success": False}
    
    def update_service_runtime(self, service_id: str, runtime: str, root_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Convenience method to update service runtime and optionally root directory.
        
        Args:
            service_id: Render service ID
            runtime: "docker", "python", "node", etc.
            root_dir: Optional root directory (e.g., "apps/otto")
        
        Returns:
            Update result
        """
        service_details = {"runtime": runtime}
        if root_dir:
            service_details["rootDir"] = root_dir
        
        return self.update_service(service_id, {"serviceDetails": service_details})
    
    def trigger_manual_deploy(self, service_id: str) -> Dict[str, Any]:
        """Trigger a manual deploy for a service"""
        try:
            url = f"{self.API_BASE_URL}/services/{service_id}/deploys"
            
            with httpx.Client() as client:
                response = client.post(url, headers=self._get_headers(), json={}, timeout=30)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error triggering Render deploy: {e}")
            return {"error": str(e), "success": False}

