"""
RepoAuditSkill - Audits the Otto repository and writes reports
"""

from pathlib import Path
from typing import List
from datetime import datetime
import uuid

from ..core.models import Task, TaskResult
from ..core.skill_base import Skill, SkillHealthIssue, SkillContext
from ..core.logging_utils import get_logger

logger = get_logger(__name__)


class RepoAuditSkill:
    """Skill that audits the Otto repository"""
    
    name = "repo_audit"
    
    def can_handle(self, task: Task) -> bool:
        """Check if this skill can handle the task"""
        return task.type == "repo_audit"
    
    def run(self, task: Task, context: SkillContext) -> TaskResult:
        """Execute the repo audit task"""
        target_repo = task.payload.get("target_repo", "apps/otto")
        output_path = task.payload.get("output_path")
        
        repo_path = Path(target_repo).resolve()
        
        if not repo_path.exists():
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Repository path does not exist: {repo_path}"
            )
        
        # Generate output path if not provided
        if not output_path:
            reports_dir = Path(context.config.storage.reports_dir) / "audits"
            reports_dir.mkdir(parents=True, exist_ok=True)
            date_str = datetime.now().strftime("%Y-%m-%d")
            output_path = reports_dir / f"otto_audit_{date_str}.md"
        else:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Perform audit
        findings = self._audit_repo(repo_path)
        
        # Write report
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# Otto Repository Audit\n\n")
            f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")
            f.write(f"**Target:** `{repo_path}`\n\n")
            
            f.write("## Summary\n\n")
            f.write(f"- **Total Issues Found:** {len(findings['issues'])}\n")
            f.write(f"- **Empty Directories:** {len(findings['empty_dirs'])}\n")
            f.write(f"- **Large Files:** {len(findings['large_files'])}\n")
            f.write(f"- **Missing __init__.py:** {len(findings['missing_init'])}\n\n")
            
            if findings['empty_dirs']:
                f.write("## Empty or Suspicious Directories\n\n")
                for dir_path in findings['empty_dirs']:
                    f.write(f"- `{dir_path}`\n")
                f.write("\n")
            
            if findings['large_files']:
                f.write("## Large Files (>1000 lines estimated)\n\n")
                for file_path, size in findings['large_files']:
                    f.write(f"- `{file_path}` ({size} bytes)\n")
                f.write("\n")
            
            if findings['missing_init']:
                f.write("## Missing __init__.py Files\n\n")
                for dir_path in findings['missing_init']:
                    f.write(f"- `{dir_path}` (Python package directory missing __init__.py)\n")
                f.write("\n")
            
            f.write("## Proposed Changes (Advisory Only)\n\n")
            f.write("The following changes are suggested but will not be applied automatically:\n\n")
            
            if findings['empty_dirs']:
                f.write("- Consider removing empty directories or adding placeholder files\n")
            
            if findings['large_files']:
                f.write("- Review large files for potential refactoring or splitting\n")
            
            if findings['missing_init']:
                f.write("- Add `__init__.py` files to Python package directories\n")
            
            if not findings['issues']:
                f.write("- No issues detected. Repository structure looks good!\n")
        
        logger.info(f"Audit report written to {output_path}")
        
        return TaskResult(
            task_id=task.id,
            success=True,
            message=f"Audit report written to {output_path}",
            data={
                "output_path": str(output_path),
                "findings": findings
            }
        )
    
    def _audit_repo(self, repo_path: Path) -> dict:
        """Perform audit on repository"""
        findings = {
            "issues": [],
            "empty_dirs": [],
            "large_files": [],
            "missing_init": []
        }
        
        # Walk the directory tree
        for root, dirs, files in repo_path.rglob("*"):
            root_path = Path(root)
            
            # Check for empty directories (or only __init__.py)
            if root_path.is_dir():
                dir_contents = list(root_path.iterdir())
                if not dir_contents or (len(dir_contents) == 1 and dir_contents[0].name == "__init__.py"):
                    rel_path = root_path.relative_to(repo_path)
                    findings["empty_dirs"].append(str(rel_path))
            
            # Check for large files
            for file in root_path.iterdir():
                if file.is_file():
                    try:
                        size = file.stat().st_size
                        # Estimate lines (rough: ~50 bytes per line)
                        estimated_lines = size / 50
                        if estimated_lines > 1000:
                            rel_path = file.relative_to(repo_path)
                            findings["large_files"].append((str(rel_path), size))
                    except (OSError, PermissionError):
                        pass
            
            # Check for missing __init__.py in Python package directories
            if root_path.is_dir() and root_path.name not in ["__pycache__", ".git", "node_modules"]:
                # Check if this looks like a Python package (has .py files)
                has_py_files = any(f.suffix == ".py" for f in root_path.iterdir() if f.is_file())
                if has_py_files:
                    init_file = root_path / "__init__.py"
                    if not init_file.exists():
                        rel_path = root_path.relative_to(repo_path)
                        findings["missing_init"].append(str(rel_path))
        
        findings["issues"] = (
            findings["empty_dirs"] +
            [f[0] for f in findings["large_files"]] +
            findings["missing_init"]
        )
        
        return findings
    
    def self_test(self, context: SkillContext) -> List[SkillHealthIssue]:
        """Run health checks on this skill"""
        issues = []
        
        default_repo = Path("apps/otto")
        if not default_repo.exists():
            issues.append(SkillHealthIssue(
                code="otto_repo_missing",
                message=f"Otto repo path does not exist: {default_repo}",
                suggestion="Ensure apps/otto directory exists"
            ))
        
        return issues

