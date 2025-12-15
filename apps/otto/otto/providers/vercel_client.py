"""
Lightweight Vercel API client for Otto monitor/repair loop
"""

import os
import time
from typing import Any, Dict, List, Optional
import httpx
from ..core.logging_utils import get_logger

logger = get_logger(__name__)


class VercelClient:
    """Client for Vercel API operations needed for monitoring and repair"""
    
    API_BASE_URL = "https://api.vercel.com"
    
    def __init__(self, token: Optional[str] = None, team_id: Optional[str] = None):
        self.token = token or os.getenv("VERCEL_TOKEN")
        self.team_id = team_id
        if not self.token:
            raise ValueError("VERCEL_TOKEN environment variable required")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get API request headers"""
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        if self.team_id:
            headers["x-vercel-team-id"] = self.team_id
        return headers
    
    def list_latest_deployment(self, project_name_or_id: str) -> Optional[Dict[str, Any]]:
        """Get the latest deployment for a project"""
        try:
            # First, get project ID if we have a name
            project_id = self._get_project_id(project_name_or_id)
            if not project_id:
                return None
            
            # List deployments
            url = f"{self.API_BASE_URL}/v6/deployments"
            params = {"projectId": project_id, "limit": 1}
            
            with httpx.Client() as client:
                response = client.get(url, headers=self._get_headers(), params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                deployments = data.get("deployments", [])
                if deployments:
                    return deployments[0]
                return None
        except Exception as e:
            logger.error(f"Error listing Vercel deployment: {e}")
            return None
    
    def get_deployment_status(self, deployment_id: str) -> Dict[str, Any]:
        """Get deployment status"""
        try:
            url = f"{self.API_BASE_URL}/v13/deployments/{deployment_id}"
            
            with httpx.Client() as client:
                response = client.get(url, headers=self._get_headers(), timeout=30)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error getting Vercel deployment status: {e}")
            return {"state": "ERROR", "error": str(e)}
    
    def get_deployment_logs(self, deployment_id: str) -> List[Dict[str, Any]]:
        """Fetch deployment build events/logs"""
        try:
            url = f"{self.API_BASE_URL}/v2/deployments/{deployment_id}/events"
            
            with httpx.Client() as client:
                response = client.get(url, headers=self._get_headers(), timeout=60)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Error fetching Vercel deployment logs: {e}")
            return []
    
    def parse_errors_from_logs(self, logs: List[Dict[str, Any]]) -> List[str]:
        """Parse errors and warnings from build logs"""
        errors = []
        for event in logs:
            if event.get("type") == "command" and event.get("payload", {}).get("exitCode", 0) != 0:
                errors.append(event.get("payload", {}).get("text", ""))
            elif event.get("type") == "stdout" and "error" in event.get("payload", {}).get("text", "").lower():
                errors.append(event.get("payload", {}).get("text", ""))
        return errors
    
    def _get_project_id(self, project_name_or_id: str) -> Optional[str]:
        """Get project ID from name or return ID if already an ID"""
        try:
            # Try to list projects to find by name
            url = f"{self.API_BASE_URL}/v9/projects"
            
            with httpx.Client() as client:
                response = client.get(url, headers=self._get_headers(), timeout=30)
                response.raise_for_status()
                data = response.json()
                
                projects = data.get("projects", [])
                for project in projects:
                    if project.get("name") == project_name_or_id or project.get("id") == project_name_or_id:
                        return project.get("id")
                
                # If not found, assume it's already an ID
                return project_name_or_id
        except Exception as e:
            logger.warning(f"Error getting project ID: {e}, assuming it's already an ID")
            return project_name_or_id

