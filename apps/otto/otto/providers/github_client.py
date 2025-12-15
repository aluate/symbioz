"""
Lightweight GitHub client for Otto monitor/repair loop
"""

import os
import subprocess
from typing import Any, Dict, List, Optional
from pathlib import Path
from ..core.logging_utils import get_logger

logger = get_logger(__name__)


class GitHubClient:
    """Client for GitHub operations needed for committing fixes"""
    
    def __init__(self, token: Optional[str] = None, repo_path: Optional[str] = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        
        # Find git root
        current = self.repo_path
        while current != current.parent:
            if (current / ".git").exists():
                self.repo_path = current
                break
            current = current.parent
    
    def create_branch(self, branch_name: str) -> bool:
        """Create a new git branch"""
        try:
            result = subprocess.run(
                ["git", "checkout", "-b", branch_name],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Error creating branch: {e}")
            return False
    
    def commit_changes(self, message: str, files: Optional[List[str]] = None) -> bool:
        """Commit changes to git"""
        try:
            # Stage files
            if files:
                for file in files:
                    subprocess.run(
                        ["git", "add", file],
                        cwd=self.repo_path,
                        capture_output=True,
                        timeout=30
                    )
            else:
                subprocess.run(
                    ["git", "add", "."],
                    cwd=self.repo_path,
                    capture_output=True,
                    timeout=30
                )
            
            # Commit
            result = subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Error committing changes: {e}")
            return False
    
    def push(self, branch: str = "main", remote: str = "origin") -> Dict[str, Any]:
        """Push commits to remote"""
        try:
            result = subprocess.run(
                ["git", "push", remote, branch],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return {"success": True, "message": f"Pushed to {remote}/{branch}"}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            logger.error(f"Error pushing: {e}")
            return {"success": False, "error": str(e)}
    
    def create_pr(self, title: str, body: str, base: str = "main", head: str = None) -> Optional[Dict[str, Any]]:
        """Create a pull request (requires GitHub CLI or API)"""
        # For now, return None - PR creation can be done via GitHub CLI if available
        # or via GitHub API if token is provided
        logger.info(f"PR creation not implemented yet. Branch {head} should be pushed for manual PR creation.")
        return None
    
    def get_current_branch(self) -> str:
        """Get current git branch"""
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return "main"
        except Exception as e:
            logger.warning(f"Error getting current branch: {e}")
            return "main"

