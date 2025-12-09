"""
Git History Cleaner - Removes secrets from git commit history
Uses git filter-branch to rewrite history and remove sensitive data
"""

import subprocess
import re
from pathlib import Path
from typing import List, Dict, Any


class GitHistoryCleaner:
    """Cleans secrets from git commit history"""
    
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
    
    def clean_secrets(self, secrets: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Remove secrets from git history using git filter-branch
        
        Args:
            secrets: List of dicts with 'pattern' (regex) and 'replacement' (string)
        
        Returns:
            Dict with success status and message
        """
        try:
            # Create filter script
            filter_script = self._create_filter_script(secrets)
            script_path = self.repo_path / ".git" / "filter-secrets.sh"
            
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(filter_script)
            
            # Make executable (Unix) - on Windows, git bash will handle it
            import os
            if os.name != 'nt':  # Unix-like
                os.chmod(script_path, 0o755)
            
            # Run git filter-branch
            # Use git filter-repo if available, otherwise filter-branch
            result = subprocess.run(
                ["git", "filter-branch", "--force", "--index-filter", 
                 f"bash {script_path.relative_to(self.repo_path)}", 
                 "--prune-empty", "--tag-name-filter", "cat", "--", "--all"],
                cwd=str(self.repo_path),
                capture_output=True,
                text=True,
                timeout=300
            )
            
            # Clean up script
            try:
                script_path.unlink()
            except:
                pass
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": "Successfully cleaned secrets from git history",
                    "output": result.stdout
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to clean history: {result.stderr}",
                    "output": result.stdout
                }
        
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "message": "Git filter-branch operation timed out"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error cleaning history: {str(e)}"
            }
    
    def _create_filter_script(self, secrets: List[Dict[str, str]]) -> str:
        """Create a bash script for git filter-branch"""
        replacements = []
        
        for secret in secrets:
            pattern = secret['pattern']
            replacement = secret['replacement']
            # Escape for sed
            escaped_pattern = pattern.replace('/', '\\/')
            escaped_replacement = replacement.replace('/', '\\/').replace('&', '\\&')
            replacements.append(f"s/{escaped_pattern}/{escaped_replacement}/g")
        
        script = """#!/bin/bash
git ls-files -z | while IFS= read -rd '' file; do
"""
        
        for replacement in replacements:
            script += f'  sed -i "{replacement}" "$file" 2>/dev/null || true\n'
        
        script += """done
"""
        
        return script
    
    def force_push_required(self) -> bool:
        """Check if force push will be needed after history rewrite"""
        try:
            result = subprocess.run(
                ["git", "log", "--oneline", "origin/main..HEAD"],
                cwd=str(self.repo_path),
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0 and bool(result.stdout.strip())
        except:
            return True

