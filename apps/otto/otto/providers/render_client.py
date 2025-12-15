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

