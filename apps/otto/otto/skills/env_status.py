"""
EnvStatusSkill - Diagnoses environment and dependency status
"""

from typing import List, Dict, Any
import os
import subprocess
import httpx
from pathlib import Path

from ..core.models import Task, TaskResult, TaskStatus
from ..core.skill_base import Skill, SkillHealthIssue, SkillContext
from ..core.logging_utils import get_logger

logger = get_logger(__name__)


class EnvStatusSkill:
    """Skill that checks environment and dependency status"""
    
    name = "env_status"
    description = "Diagnoses environment setup, dependencies, and service health"
    
    def __init__(self):
        # Life OS backend API URL
        self.life_os_api_url = os.getenv("LIFE_OS_API_URL", "http://localhost:8000")
        # Otto API URL
        self.otto_api_url = os.getenv("OTTO_API_URL", "http://localhost:8001")
    
    def can_handle(self, task: Task) -> bool:
        """Check if this skill can handle the task"""
        return task.type in ["env_status", "otto_doctor", "check_dependencies", "diagnose_env"]
    
    def run(self, task: Task, context: SkillContext) -> TaskResult:
        """Execute the environment status check"""
        try:
            checks = self._run_all_checks()
            report = self._format_report(checks)
            
            # Extract actions if any are needed (e.g., "run setup script")
            actions = []
            if checks.get("needs_setup"):
                actions.append({
                    "type": "otto.log",
                    "payload": {
                        "message": f"Run {checks.get('setup_script', 'setup_otto_windows.bat')} to fix missing dependencies",
                        "level": "warning"
                    }
                })
            
            return TaskResult(
                task_id=task.id,
                success=True,
                message=report,
                data={
                    "checks": checks,
                    "actions": actions if actions else None
                }
            )
        except Exception as e:
            logger.error(f"Error in EnvStatusSkill: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error checking environment: {str(e)}"
            )
    
    def _run_all_checks(self) -> Dict[str, Any]:
        """Run all environment checks"""
        checks = {
            "python": self._check_python(),
            "pip": self._check_pip(),
            "node": self._check_node(),
            "otto_api": self._check_otto_api(),
            "life_os_backend": self._check_life_os_backend(),
            "life_os_frontend": self._check_life_os_frontend(),
            "dependencies": self._check_dependencies(),
            "migrations": self._check_migrations(),  # Phase 2.5
            "needs_setup": False,
            "setup_script": self._get_setup_script()
        }
        
        # Determine if setup is needed
        checks["needs_setup"] = (
            not checks["python"]["ok"] or
            not checks["pip"]["ok"] or
            (checks["dependencies"]["missing_python"] > 0) or
            (checks["node"]["ok"] and checks["dependencies"]["missing_node"] > 0) or
            checks["migrations"].get("needs_migration", False)
        )
        
        return checks
    
    def _check_python(self) -> Dict[str, Any]:
        """Check if Python is installed"""
        try:
            result = subprocess.run(
                ["python", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return {"ok": True, "version": result.stdout.strip()}
        except:
            pass
        
        try:
            result = subprocess.run(
                ["python3", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return {"ok": True, "version": result.stdout.strip()}
        except:
            pass
        
        return {"ok": False, "message": "Python not found"}
    
    def _check_pip(self) -> Dict[str, Any]:
        """Check if pip is installed"""
        try:
            result = subprocess.run(
                ["pip", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return {"ok": True, "version": result.stdout.strip()}
        except:
            pass
        
        try:
            result = subprocess.run(
                ["pip3", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return {"ok": True, "version": result.stdout.strip()}
        except:
            pass
        
        return {"ok": False, "message": "pip not found"}
    
    def _check_node(self) -> Dict[str, Any]:
        """Check if Node.js is installed"""
        try:
            result = subprocess.run(
                ["node", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return {"ok": True, "version": result.stdout.strip()}
        except:
            pass
        
        return {"ok": False, "message": "Node.js not found (optional)"}
    
    def _check_otto_api(self) -> Dict[str, Any]:
        """Check if Otto API is running"""
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"{self.otto_api_url}/health")
                if response.status_code == 200:
                    return {"ok": True, "url": self.otto_api_url}
        except:
            pass
        
        return {"ok": False, "message": f"Otto API not reachable at {self.otto_api_url}"}
    
    def _check_life_os_backend(self) -> Dict[str, Any]:
        """Check if Life OS Backend is running"""
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"{self.life_os_api_url}/health")
                if response.status_code == 200:
                    return {"ok": True, "url": self.life_os_api_url}
        except:
            pass
        
        return {"ok": False, "message": f"Life OS Backend not reachable at {self.life_os_api_url}"}
    
    def _check_life_os_frontend(self) -> Dict[str, Any]:
        """Check if Life OS Frontend is running"""
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get("http://localhost:3000")
                if response.status_code == 200:
                    return {"ok": True, "url": "http://localhost:3000"}
        except:
            pass
        
        return {"ok": False, "message": "Life OS Frontend not reachable at http://localhost:3000"}
    
    def _check_dependencies(self) -> Dict[str, Any]:
        """Check if required dependencies are installed"""
        missing_python = 0
        missing_node = 0
        
        # Check Python dependencies
        try:
            # Try to import key packages
            import fastapi
            import sqlalchemy
            import httpx
        except ImportError as e:
            missing_python += 1
        
        # Check Node dependencies (if node is available)
        node_ok = self._check_node()["ok"]
        if node_ok:
            # Check if node_modules exists in frontend
            frontend_path = Path("apps/life_os/frontend")
            if not (frontend_path / "node_modules").exists():
                missing_node += 1
        
        return {
            "missing_python": missing_python,
            "missing_node": missing_node,
            "ok": missing_python == 0 and (not node_ok or missing_node == 0)
        }
    
    def _check_migrations(self) -> Dict[str, Any]:
        """Check for pending database migrations (Phase 2.5)"""
        try:
            # Try to import alembic
            import alembic
            from alembic.config import Config
            from alembic import script
            from alembic.runtime.migration import MigrationContext
            from sqlalchemy import create_engine
            
            # Check if alembic.ini exists
            alembic_ini_path = Path("apps/life_os/backend/alembic.ini")
            if not alembic_ini_path.exists():
                return {
                    "ok": True,  # Migrations not set up yet, not an error
                    "needs_migration": False,
                    "message": "Alembic not configured (using auto-create tables)"
                }
            
            # Try to check migration status
            alembic_cfg = Config(str(alembic_ini_path))
            script_dir = script.ScriptDirectory.from_config(alembic_cfg)
            
            # Get database URL
            database_url = alembic_cfg.get_main_option("sqlalchemy.url", "sqlite:///./life_os.db")
            engine = create_engine(database_url)
            
            with engine.connect() as connection:
                context = MigrationContext.configure(connection)
                current_rev = context.get_current_revision()
                head_rev = script_dir.get_current_head()
                
                if current_rev != head_rev:
                    return {
                        "ok": False,
                        "needs_migration": True,
                        "message": f"Pending migrations: current={current_rev}, head={head_rev}",
                        "action": "Run: alembic upgrade head"
                    }
                else:
                    return {
                        "ok": True,
                        "needs_migration": False,
                        "message": "Database migrations up to date"
                    }
        
        except ImportError:
            # Alembic not installed - that's OK for now
            return {
                "ok": True,
                "needs_migration": False,
                "message": "Alembic not installed (using auto-create tables)"
            }
        except Exception as e:
            # Migration check failed, but don't block
            return {
                "ok": True,  # Don't fail the whole check
                "needs_migration": False,
                "message": f"Could not check migrations: {str(e)}"
            }
    
    def _get_setup_script(self) -> str:
        """Determine which setup script to recommend"""
        if os.name == "nt":  # Windows
            return "setup_otto_windows.bat"
        else:  # Unix-like
            return "setup_otto_unix.sh"
    
    def _format_report(self, checks: Dict[str, Any]) -> str:
        """Format a human-readable report"""
        lines = []
        lines.append("Environment Status Report")
        lines.append("=" * 50)
        lines.append("")
        
        # Python
        if checks["python"]["ok"]:
            lines.append(f"✓ Python: {checks['python'].get('version', 'OK')}")
        else:
            lines.append(f"✗ Python: {checks['python'].get('message', 'Not found')}")
        
        # pip
        if checks["pip"]["ok"]:
            lines.append(f"✓ pip: {checks['pip'].get('version', 'OK')}")
        else:
            lines.append(f"✗ pip: {checks['pip'].get('message', 'Not found')}")
        
        # Node.js
        if checks["node"]["ok"]:
            lines.append(f"✓ Node.js: {checks['node'].get('version', 'OK')}")
        else:
            lines.append(f"○ Node.js: {checks['node'].get('message', 'Not found')} (optional)")
        
        lines.append("")
        lines.append("Services:")
        
        # Otto API
        if checks["otto_api"]["ok"]:
            lines.append(f"✓ Otto API: Running at {checks['otto_api']['url']}")
        else:
            lines.append(f"✗ Otto API: {checks['otto_api'].get('message', 'Not running')}")
        
        # Life OS Backend
        if checks["life_os_backend"]["ok"]:
            lines.append(f"✓ Life OS Backend: Running at {checks['life_os_backend']['url']}")
        else:
            lines.append(f"✗ Life OS Backend: {checks['life_os_backend'].get('message', 'Not running')}")
        
        # Life OS Frontend
        if checks["life_os_frontend"]["ok"]:
            lines.append(f"✓ Life OS Frontend: Running at {checks['life_os_frontend']['url']}")
        else:
            lines.append(f"✗ Life OS Frontend: {checks['life_os_frontend'].get('message', 'Not running')}")
        
        lines.append("")
        lines.append("Dependencies:")
        
        if checks["dependencies"]["missing_python"] > 0:
            lines.append(f"✗ Missing Python dependencies: {checks['dependencies']['missing_python']} package(s)")
        else:
            lines.append("✓ Python dependencies: OK")
        
        if checks["node"]["ok"]:
            if checks["dependencies"]["missing_node"] > 0:
                lines.append(f"✗ Missing Node dependencies: {checks['dependencies']['missing_node']} package(s)")
            else:
                lines.append("✓ Node dependencies: OK")
        
        lines.append("")
        lines.append("Database:")
        
        # Migrations
        if checks["migrations"].get("needs_migration"):
            lines.append(f"✗ Migrations: {checks['migrations'].get('message', 'Pending migrations')}")
            if checks["migrations"].get("action"):
                lines.append(f"  → {checks['migrations']['action']}")
        else:
            lines.append(f"✓ Migrations: {checks['migrations'].get('message', 'OK')}")
        
        if checks["needs_setup"]:
            lines.append("")
            lines.append(f"⚠ Setup needed! Run: {checks['setup_script']}")
        
        return "\n".join(lines)
    
    def self_test(self, context: SkillContext) -> List[SkillHealthIssue]:
        """Run health checks on this skill"""
        issues = []
        
        # Check if we can run subprocess commands
        try:
            subprocess.run(["python", "--version"], capture_output=True, timeout=2)
        except:
            issues.append(SkillHealthIssue(
                code="subprocess_unavailable",
                message="Cannot run subprocess commands for environment checks",
                suggestion="Check system permissions"
            ))
        
        return issues

