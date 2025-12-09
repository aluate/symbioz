"""
LauncherDiagnosticSkill - Otto can diagnose and fix launcher issues
"""

import os
import subprocess
import sys
import re
from typing import List, Dict, Any
from pathlib import Path

from ..core.models import Task, TaskResult, TaskStatus
from ..core.skill_base import Skill, SkillHealthIssue, SkillContext
from ..core.logging_utils import get_logger

logger = get_logger(__name__)


class LauncherDiagnosticSkill:
    """Skill for diagnosing and fixing launcher issues"""
    
    name = "launcher_diagnostic"
    description = "Diagnose and fix launcher dependency and configuration issues"
    
    def can_handle(self, task: Task) -> bool:
        """Check if this skill can handle the task"""
        return task.type in ["launcher_diagnostic", "fix_launcher", "diagnose_launcher", "test_launcher"]
    
    def run(self, task: Task, context: SkillContext) -> TaskResult:
        """Execute launcher diagnostic"""
        try:
            action = task.payload.get("action", "diagnose")
            
            if action == "diagnose":
                return self._diagnose_launcher(context)
            elif action == "fix":
                return self._fix_launcher(context)
            elif action == "test":
                return self._test_launcher(context)
            else:
                return TaskResult(
                    task_id=task.id,
                    success=False,
                    message=f"Unknown action: {action}"
                )
        except Exception as e:
            logger.error(f"Error in LauncherDiagnosticSkill: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error: {str(e)}"
            )
    
    def _find_repo_root(self) -> str:
        """Find the repository root"""
        current = os.path.abspath(__file__)
        # Go up from apps/otto/otto/skills/launcher_diagnostic.py
        for _ in range(5):
            current = os.path.dirname(current)
            launcher = os.path.join(current, "LAUNCH_SYMBIOZ.bat")
            if os.path.exists(launcher):
                return current
        return None
    
    def _diagnose_launcher(self, context: SkillContext) -> TaskResult:
        """Diagnose launcher issues"""
        issues = []
        fixes_applied = []
        
        repo_root = self._find_repo_root()
        if not repo_root:
            return TaskResult(
                task_id="",
                success=False,
                message="Could not find repository root"
            )
        
        # Check Python
        python_ok, python_issue = self._check_python()
        if not python_ok:
            issues.append(python_issue)
        
        # Check Node.js
        node_ok, node_issue = self._check_node()
        if not node_ok:
            issues.append(node_issue)
        
        # Check requirements.txt for problematic dependencies
        req_file = os.path.join(repo_root, "apps", "symbioz_cli", "requirements.txt")
        if os.path.exists(req_file):
            req_ok, req_issue, fix_applied = self._check_requirements(req_file)
            if not req_ok:
                issues.append(req_issue)
            if fix_applied:
                fixes_applied.append("Fixed requirements.txt (removed Rust dependencies)")
        
        # Check venv
        venv_path = os.path.join(repo_root, "apps", "symbioz_cli", "venv")
        venv_ok, venv_issue = self._check_venv(venv_path)
        if not venv_ok:
            issues.append(venv_issue)
        
        # Check package.json
        package_json = os.path.join(repo_root, "apps", "symbioz_web", "package.json")
        package_ok, package_issue = self._check_package_json(package_json)
        if not package_ok:
            issues.append(package_issue)
        
        all_ok = len(issues) == 0
        
        message = "Launcher diagnostic complete"
        if fixes_applied:
            message += f". Fixes applied: {', '.join(fixes_applied)}"
        if issues:
            message += f". Issues found: {len(issues)}"
        
        return TaskResult(
            task_id="",
            success=all_ok,
            message=message,
            data={
                "issues": issues,
                "fixes_applied": fixes_applied,
                "repo_root": repo_root
            }
        )
    
    def _check_python(self) -> tuple[bool, Dict[str, Any]]:
        """Check if Python is available"""
        try:
            result = subprocess.run(
                ["python", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                return True, {"type": "python", "status": "ok", "version": version}
            else:
                return False, {
                    "type": "python",
                    "status": "error",
                    "message": "Python command failed",
                    "suggestion": "Install Python or add it to PATH"
                }
        except FileNotFoundError:
            return False, {
                "type": "python",
                "status": "not_found",
                "message": "Python not found in PATH",
                "suggestion": "Install Python or add it to PATH"
            }
        except Exception as e:
            return False, {
                "type": "python",
                "status": "error",
                "message": f"Error checking Python: {str(e)}"
            }
    
    def _check_node(self) -> tuple[bool, Dict[str, Any]]:
        """Check if Node.js is available"""
        try:
            result = subprocess.run(
                ["node", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                return True, {"type": "node", "status": "ok", "version": version}
            else:
                return False, {
                    "type": "node",
                    "status": "error",
                    "message": "Node.js command failed",
                    "suggestion": "Install Node.js or add it to PATH"
                }
        except FileNotFoundError:
            return False, {
                "type": "node",
                "status": "not_found",
                "message": "Node.js not found in PATH",
                "suggestion": "Install Node.js or add it to PATH"
            }
        except Exception as e:
            return False, {
                "type": "node",
                "status": "error",
                "message": f"Error checking Node.js: {str(e)}"
            }
    
    def _check_requirements(self, req_file: str) -> tuple[bool, Dict[str, Any], bool]:
        """Check requirements.txt for problematic dependencies"""
        fix_applied = False
        try:
            with open(req_file, 'r') as f:
                content = f.read()
            
            # Check for uvicorn[standard] which requires Rust
            if 'uvicorn[standard]' in content:
                # Fix it
                new_content = content.replace('uvicorn[standard]', 'uvicorn')
                with open(req_file, 'w') as f:
                    f.write(new_content)
                fix_applied = True
                return False, {
                    "type": "requirements",
                    "status": "fixed",
                    "message": "Found uvicorn[standard] which requires Rust - fixed by removing [standard]",
                    "suggestion": "Re-run launcher"
                }, True
            
            return True, {"type": "requirements", "status": "ok"}, False
        except Exception as e:
            return False, {
                "type": "requirements",
                "status": "error",
                "message": f"Error checking requirements.txt: {str(e)}"
            }, False
    
    def _check_venv(self, venv_path: str) -> tuple[bool, Dict[str, Any]]:
        """Check if venv exists and is valid"""
        if not os.path.exists(venv_path):
            return True, {
                "type": "venv",
                "status": "not_created",
                "message": "Virtual environment not created yet (will be created by launcher)",
                "suggestion": "Run launcher to create venv"
            }
        
        # Check if venv has activation script
        if sys.platform == "win32":
            activate = os.path.join(venv_path, "Scripts", "activate.bat")
        else:
            activate = os.path.join(venv_path, "bin", "activate")
        
        if not os.path.exists(activate):
            return False, {
                "type": "venv",
                "status": "invalid",
                "message": "Virtual environment exists but is invalid",
                "suggestion": "Delete venv folder and re-run launcher"
            }
        
        return True, {"type": "venv", "status": "ok"}
    
    def _check_package_json(self, package_json: str) -> tuple[bool, Dict[str, Any]]:
        """Check if package.json exists"""
        if not os.path.exists(package_json):
            return False, {
                "type": "package_json",
                "status": "not_found",
                "message": "package.json not found",
                "suggestion": "Ensure symbioz_web directory exists"
            }
        return True, {"type": "package_json", "status": "ok"}
    
    def _fix_launcher(self, context: SkillContext) -> TaskResult:
        """Fix launcher issues"""
        # Run diagnose first
        diagnose_result = self._diagnose_launcher(context)
        
        if not diagnose_result.success:
            # Apply fixes
            fixes = []
            repo_root = self._find_repo_root()
            
            # Fix requirements.txt if needed
            req_file = os.path.join(repo_root, "apps", "symbioz_cli", "requirements.txt")
            if os.path.exists(req_file):
                with open(req_file, 'r') as f:
                    content = f.read()
                if 'uvicorn[standard]' in content:
                    new_content = content.replace('uvicorn[standard]', 'uvicorn')
                    with open(req_file, 'w') as f:
                        f.write(new_content)
                    fixes.append("Fixed requirements.txt")
            
            # Remove broken venv if it exists
            venv_path = os.path.join(repo_root, "apps", "symbioz_cli", "venv")
            if os.path.exists(venv_path):
                # Check if it's broken
                if sys.platform == "win32":
                    activate = os.path.join(venv_path, "Scripts", "activate.bat")
                else:
                    activate = os.path.join(venv_path, "bin", "activate")
                
                if not os.path.exists(activate):
                    import shutil
                    try:
                        shutil.rmtree(venv_path)
                        fixes.append("Removed broken virtual environment")
                    except Exception as e:
                        logger.warning(f"Could not remove venv: {str(e)}")
            
            return TaskResult(
                task_id="",
                success=True,
                message=f"Applied fixes: {', '.join(fixes) if fixes else 'None needed'}",
                data={
                    "fixes_applied": fixes,
                    "diagnosis": diagnose_result.data
                }
            )
        
        return TaskResult(
            task_id="",
            success=True,
            message="No fixes needed - launcher is healthy",
            data=diagnose_result.data
        )
    
    def _test_launcher(self, context: SkillContext) -> TaskResult:
        """Test if launcher can start services"""
        repo_root = self._find_repo_root()
        if not repo_root:
            return TaskResult(
                task_id="",
                success=False,
                message="Could not find repository root"
            )
        
        # First fix any issues
        fix_result = self._fix_launcher(context)
        
        # Try to install Python dependencies
        cli_dir = os.path.join(repo_root, "apps", "symbioz_cli")
        venv_path = os.path.join(cli_dir, "venv")
        
        test_results = []
        
        # Test Python dependency installation
        try:
            if not os.path.exists(venv_path):
                result = subprocess.run(
                    ["python", "-m", "venv", "venv"],
                    cwd=cli_dir,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode != 0:
                    test_results.append({
                        "test": "create_venv",
                        "ok": False,
                        "error": result.stderr
                    })
                    return TaskResult(
                        task_id="",
                        success=False,
                        message="Failed to create virtual environment",
                        data={"test_results": test_results}
                    )
            
            # Activate venv and install dependencies
            if sys.platform == "win32":
                pip_path = os.path.join(venv_path, "Scripts", "pip.exe")
                python_path = os.path.join(venv_path, "Scripts", "python.exe")
            else:
                pip_path = os.path.join(venv_path, "bin", "pip")
                python_path = os.path.join(venv_path, "bin", "python")
            
            if os.path.exists(pip_path):
                result = subprocess.run(
                    [pip_path, "install", "-q", "-r", "requirements.txt"],
                    cwd=cli_dir,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                if result.returncode == 0:
                    test_results.append({
                        "test": "install_python_deps",
                        "ok": True
                    })
                else:
                    test_results.append({
                        "test": "install_python_deps",
                        "ok": False,
                        "error": result.stderr[:500]  # First 500 chars
                    })
                    return TaskResult(
                        task_id="",
                        success=False,
                        message="Failed to install Python dependencies",
                        data={"test_results": test_results, "error": result.stderr[:500]}
                    )
            else:
                test_results.append({
                    "test": "install_python_deps",
                    "ok": False,
                    "error": "pip not found in venv"
                })
        
        except subprocess.TimeoutExpired:
            return TaskResult(
                task_id="",
                success=False,
                message="Timeout installing Python dependencies",
                data={"test_results": test_results}
            )
        except Exception as e:
            return TaskResult(
                task_id="",
                success=False,
                message=f"Error testing launcher: {str(e)}",
                data={"test_results": test_results}
            )
        
        # Test Node.js dependency check (don't actually install, just check)
        web_dir = os.path.join(repo_root, "apps", "symbioz_web")
        package_json = os.path.join(web_dir, "package.json")
        if os.path.exists(package_json):
            test_results.append({
                "test": "check_node_setup",
                "ok": True
            })
        
        return TaskResult(
            task_id="",
            success=True,
            message="Launcher test passed - dependencies can be installed",
            data={
                "test_results": test_results,
                "fixes_applied": fix_result.data.get("fixes_applied", []) if fix_result.data else []
            }
        )
    
    def self_test(self, context: SkillContext) -> List[SkillHealthIssue]:
        """Run health checks on this skill"""
        issues = []
        
        repo_root = self._find_repo_root()
        if not repo_root:
            issues.append(SkillHealthIssue(
                code="repo_root_not_found",
                message="Could not find repository root",
                suggestion="Ensure you're running from the correct repository"
            ))
        
        return issues



