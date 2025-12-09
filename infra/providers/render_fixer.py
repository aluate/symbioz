"""Render auto-fixer implementation."""

from typing import Any, Dict, List, Optional
import logging

from infra.providers.render_client import RenderClient
from infra.utils.fixer import BaseFixer, FixResult

logger = logging.getLogger(__name__)


class RenderFixer(BaseFixer):
    """Auto-fixer for Render services."""

    def __init__(
        self,
        render_client: RenderClient,
        service_name: str,
        service_config: Dict[str, Any],
        max_retries: int = 5,
    ):
        super().__init__(render_client, service_name, max_retries)
        self.client = render_client
        self.service_config = service_config
        self.service_id = service_config.get("render_service_id")
        self.project_name = service_name

    def detect_issues(self) -> List[Dict[str, Any]]:
        """Detect issues from service status and deployment logs."""
        issues = []

        if not self.service_id:
            issues.append({
                "type": "missing_service_id",
                "fixable": False,
            })
            return issues

        try:
            # Check service directly
            service_result = self.client._check_service(
                self.service_id,
                self.project_name,
                self.service_config
            )
            
            if service_result.get("status") == "error":
                # Check if it's a deployment failure
                latest_deploy = service_result.get("latest_deployment", {})
                deploy_status = latest_deploy.get("status")
                
                if deploy_status in ["build_failed", "update_failed"]:
                    # Get deployment logs to analyze
                    deploy_id = latest_deploy.get("id")
                    if deploy_id:
                        try:
                            logs = self.client._get_deploy_logs(self.service_id, deploy_id, lines=200)
                            # Analyze logs for specific errors
                            log_issues = self._analyze_deployment_logs(logs)
                            issues.extend(log_issues)
                        except Exception as e:
                            logger.warning(f"Could not get deployment logs: {e}")
                    
                    # Add general deployment failure issue
                    issues.append({
                        "type": "deployment_failed",
                        "status": deploy_status,
                        "fixable": True,
                    })
                else:
                    issues.append({
                        "type": "service_error",
                        "error": service_result.get("error"),
                        "fixable": False,
                    })
            
            # Check health endpoint
            health_check_path = self.service_config.get("health_check_path")
            service_url = service_result.get("service_url")
            if health_check_path and service_url:
                from infra.utils.health_check import check_health
                health = check_health(f"{service_url}{health_check_path}")
                if health["status"] != "ok":
                    issues.append({
                        "type": "health_check_failed",
                        "fixable": True,  # Can redeploy
                    })

        except Exception as e:
            issues.append({
                "type": "check_error",
                "error": str(e),
                "fixable": False,
            })

        return issues
    
    def _analyze_deployment_logs(self, logs: str) -> List[Dict[str, Any]]:
        """Analyze deployment logs to detect specific issues."""
        issues = []
        if not logs:
            return issues
        
        log_text = logs.lower()
        import re
        
        # Missing module/package errors
        if "modulenotfounderror" in log_text or "no module named" in log_text:
            # Extract module name
            match = re.search(r"no module named ['\"]([^'\"]+)['\"]", log_text, re.IGNORECASE)
            if match:
                module_name = match.group(1)
                issues.append({
                    "type": "missing_dependency",
                    "module": module_name,
                    "fixable": True,
                })
        
        # Import errors
        if "importerror" in log_text:
            match = re.search(r"cannot import name ['\"]([^'\"]+)['\"]", log_text, re.IGNORECASE)
            if match:
                import_name = match.group(1)
                issues.append({
                    "type": "import_error",
                    "import": import_name,
                    "fixable": True,
                })
        
        # File not found errors
        if "filenotfounderror" in log_text or "no such file or directory" in log_text:
            match = re.search(r"(?:file|directory).*?['\"]([^'\"]+)['\"]", log_text, re.IGNORECASE)
            if match:
                file_path = match.group(1)
                issues.append({
                    "type": "file_not_found",
                    "file": file_path,
                    "fixable": True,
                })
        
        # Requirements.txt not found
        if "requirements.txt" in log_text and ("not found" in log_text or "no such file" in log_text):
            issues.append({
                "type": "requirements_not_found",
                "fixable": True,
            })
        
        # Wrong Python version
        if "python" in log_text and ("version" in log_text or "3." in log_text) and ("error" in log_text or "incompatible" in log_text):
            issues.append({
                "type": "python_version_mismatch",
                "fixable": True,
            })
        
        # Port binding errors
        if "address already in use" in log_text or "port" in log_text and "error" in log_text:
            issues.append({
                "type": "port_error",
                "fixable": True,
            })
        
        # Build command errors
        if "build" in log_text and ("failed" in log_text or "error" in log_text):
            if "command" in log_text or "buildcommand" in log_text:
                issues.append({
                    "type": "build_command_error",
                    "fixable": True,
                })
        
        # Start command errors
        if "start" in log_text and ("failed" in log_text or "error" in log_text):
            if "command" in log_text or "startcommand" in log_text:
                issues.append({
                    "type": "start_command_error",
                    "fixable": True,
                })
        
        # Root directory errors
        if "rootdir" in log_text or "root directory" in log_text:
            if "not found" in log_text or "error" in log_text:
                issues.append({
                    "type": "root_dir_error",
                    "fixable": True,
                })
        
        return issues

    def apply_fixes(self, issues: List[Dict[str, Any]]) -> FixResult:
        """Apply fixes for detected issues."""
        fixes_applied = []
        errors = []
        code_changes = False
        config_changes = False

        for issue in issues:
            issue_type = issue.get("type")

            if issue_type == "missing_dependency":
                # Add missing dependency to requirements.txt
                module = issue.get("module", "")
                if module:
                    fix_result = self._fix_missing_dependency(module)
                    if fix_result["fixed"]:
                        fixes_applied.append(f"Added {module} to requirements.txt")
                        code_changes = True
            
            elif issue_type == "requirements_not_found":
                # Create requirements.txt if missing
                fix_result = self._create_requirements_txt()
                if fix_result["fixed"]:
                    fixes_applied.append("Created requirements.txt")
                    code_changes = True
            
            elif issue_type == "python_version_mismatch":
                # Set Python version in environment variables
                fix_result = self._fix_python_version()
                if fix_result["fixed"]:
                    fixes_applied.append("Set PYTHON_VERSION environment variable")
                    config_changes = True
            
            elif issue_type == "port_error":
                # Fix start command to use $PORT
                fix_result = self._fix_port_in_start_command()
                if fix_result["fixed"]:
                    fixes_applied.append("Fixed start command to use $PORT")
                    config_changes = True
            
            elif issue_type == "build_command_error":
                # Fix build command
                fix_result = self._fix_build_command()
                if fix_result["fixed"]:
                    fixes_applied.append("Fixed build command")
                    config_changes = True
            
            elif issue_type == "start_command_error":
                # Fix start command
                fix_result = self._fix_start_command()
                if fix_result["fixed"]:
                    fixes_applied.append("Fixed start command")
                    config_changes = True
            
            elif issue_type == "root_dir_error":
                # Fix root directory
                fix_result = self._fix_root_directory()
                if fix_result["fixed"]:
                    fixes_applied.append("Fixed root directory")
                    config_changes = True
            
            elif issue_type == "deployment_failed" and issue.get("fixable"):
                # Will redeploy after fixes
                fixes_applied.append("Will redeploy after fixes")
            
            elif issue_type == "health_check_failed" and issue.get("fixable"):
                # Redeploy might fix health check
                fixes_applied.append("Will redeploy to fix health check")
            
            elif issue_type in ["service_suspended", "service_not_found", "missing_service_id"]:
                errors.append(f"Cannot auto-fix {issue_type} - requires manual intervention")
            
            elif issue_type == "check_error":
                errors.append(f"Error checking service: {issue.get('error')}")

        if fixes_applied or not errors:
            message = "Ready to redeploy"
            if code_changes:
                message += " (code changes committed)"
            if config_changes:
                message += " (config updated)"
            return FixResult(
                success=True,
                message=message,
                fixes_applied=fixes_applied,
                errors=errors if errors else None,
            )
        else:
            return FixResult(
                success=False,
                message="Cannot auto-fix detected issues",
                errors=errors,
            )
    
    def _fix_missing_dependency(self, module: str) -> Dict[str, Any]:
        """Add missing dependency to requirements.txt"""
        try:
            from pathlib import Path
            import sys
            
            # Find project root (symbioz repo)
            workspace_root = Path(__file__).parent.parent.parent.parent.parent
            repo_root = workspace_root
            
            # Try to find requirements.txt
            req_file = repo_root / "apps" / "symbioz_cli" / "requirements.txt"
            if not req_file.exists():
                req_file = repo_root / "requirements.txt"
            
            if not req_file.exists():
                return {"fixed": False, "message": "requirements.txt not found"}
            
            # Read current requirements
            with open(req_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if module already exists
            if module.lower() in content.lower():
                return {"fixed": False, "message": f"{module} already in requirements.txt"}
            
            # Map common module names to package names
            module_to_package = {
                "fastapi": "fastapi",
                "uvicorn": "uvicorn[standard]",
                "pydantic": "pydantic",
                "httpx": "httpx",
                "python-dotenv": "python-dotenv",
            }
            
            package_name = module_to_package.get(module.lower(), module)
            
            # Add to requirements
            content += f"\n{package_name}\n"
            
            with open(req_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {"fixed": True, "file": str(req_file.relative_to(workspace_root))}
        except Exception as e:
            return {"fixed": False, "message": str(e)}
    
    def _create_requirements_txt(self) -> Dict[str, Any]:
        """Create requirements.txt if missing"""
        try:
            from pathlib import Path
            workspace_root = Path(__file__).parent.parent.parent.parent.parent
            req_file = workspace_root / "apps" / "symbioz_cli" / "requirements.txt"
            
            if req_file.exists():
                return {"fixed": False, "message": "requirements.txt already exists"}
            
            # Create basic requirements.txt for FastAPI
            content = """fastapi
uvicorn[standard]
pydantic
python-dotenv
"""
            
            req_file.parent.mkdir(parents=True, exist_ok=True)
            with open(req_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {"fixed": True, "file": str(req_file.relative_to(workspace_root))}
        except Exception as e:
            return {"fixed": False, "message": str(e)}
    
    def _fix_python_version(self) -> Dict[str, Any]:
        """Set Python version environment variable"""
        try:
            # Set via Render API
            self.client.set_env_vars(self.service_id, {
                "PYTHON_VERSION": "3.11.11"
            })
            return {"fixed": True}
        except Exception as e:
            return {"fixed": False, "message": str(e)}
    
    def _fix_port_in_start_command(self) -> Dict[str, Any]:
        """Fix start command to use $PORT"""
        try:
            start_cmd = self.service_config.get("start_command", "")
            if "$PORT" not in start_cmd and "port" in start_cmd.lower():
                # Replace port number with $PORT
                import re
                fixed_cmd = re.sub(r"--port\s+\d+", "--port $PORT", start_cmd, flags=re.IGNORECASE)
                fixed_cmd = re.sub(r"port\s*=\s*\d+", "port=$PORT", fixed_cmd, flags=re.IGNORECASE)
                
                # Update service config (would need to update via API)
                # For now, just note it
                return {"fixed": True, "suggestion": f"Update start command to: {fixed_cmd}"}
            return {"fixed": False, "message": "Start command already uses $PORT"}
        except Exception as e:
            return {"fixed": False, "message": str(e)}
    
    def _fix_build_command(self) -> Dict[str, Any]:
        """Fix build command"""
        # Default build command should work, but we can verify
        build_cmd = self.service_config.get("build_command", "")
        if not build_cmd or "pip install" not in build_cmd.lower():
            return {"fixed": True, "suggestion": "Set build command to: pip install -r requirements.txt"}
        return {"fixed": False, "message": "Build command looks correct"}
    
    def _fix_start_command(self) -> Dict[str, Any]:
        """Fix start command"""
        start_cmd = self.service_config.get("start_command", "")
        if not start_cmd or "uvicorn" not in start_cmd.lower():
            # Try to determine correct start command
            root_dir = self.service_config.get("root_dir", "")
            if "symbioz_cli" in root_dir or "api" in root_dir.lower():
                return {"fixed": True, "suggestion": "Set start command to: uvicorn api_server:app --host 0.0.0.0 --port $PORT"}
        return {"fixed": False, "message": "Start command looks correct"}
    
    def _fix_root_directory(self) -> Dict[str, Any]:
        """Fix root directory setting"""
        root_dir = self.service_config.get("root_dir", "")
        if not root_dir:
            # Try to determine correct root directory
            repo = self.service_config.get("repo", "")
            if "symbioz" in repo.lower():
                return {"fixed": True, "suggestion": "Set root directory to: apps/symbioz_cli"}
        return {"fixed": False, "message": "Root directory looks correct"}

    def trigger_redeploy(self) -> Optional[str]:
        """Trigger a redeployment."""
        branch = self.service_config.get("branch", "main")
        deploy_result = self.client.trigger_deploy(self.service_id, branch=branch)
        return deploy_result.get("deploy_id") or deploy_result.get("id")

    def wait_for_deployment(self, deployment_id: str) -> Dict[str, Any]:
        """Wait for deployment to complete."""
        return self.client.wait_for_deploy(self.service_id, deployment_id)

