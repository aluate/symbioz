"""
RepoListerSkill - Lists repository structure and writes to Markdown
"""

from pathlib import Path
from typing import List
from datetime import datetime
import uuid

from ..core.models import Task, TaskResult, TaskStatus
from ..core.skill_base import Skill, SkillHealthIssue, SkillContext
from ..core.logging_utils import get_logger

logger = get_logger(__name__)


class RepoListerSkill:
    """Skill that lists repository structure"""
    
    name = "repo_lister"
    
    def can_handle(self, task: Task) -> bool:
        """Check if this skill can handle the task"""
        return task.type == "repo_list"
    
    def run(self, task: Task, context: SkillContext) -> TaskResult:
        """Execute the repo listing task"""
        target_repo = task.payload.get("target_repo")
        output_path = task.payload.get("output_path")
        
        if not target_repo:
            target_repo = context.config.storage.default_repo_root
        
        repo_path = Path(target_repo).resolve()
        
        if not repo_path.exists():
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Repository path does not exist: {repo_path}"
            )
        
        # Generate output path if not provided
        if not output_path:
            reports_dir = Path(context.config.storage.reports_dir)
            reports_dir.mkdir(parents=True, exist_ok=True)
            output_path = reports_dir / "repo_tree.md"
        else:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Walk the directory tree and generate markdown
        tree_lines = self._generate_tree(repo_path, repo_path)
        
        # Write to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# Repository Tree: {repo_path.name}\n\n")
            f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")
            f.write(f"**Root Path:** `{repo_path}`\n\n")
            f.write("## Directory Structure\n\n")
            f.write("```\n")
            f.write("\n".join(tree_lines))
            f.write("\n```\n")
        
        logger.info(f"Repository tree written to {output_path}")
        
        return TaskResult(
            task_id=task.id,
            success=True,
            message=f"Repository tree written to {output_path}",
            data={"output_path": str(output_path)}
        )
    
    def _generate_tree(self, root: Path, current: Path, prefix: str = "") -> List[str]:
        """Generate tree structure lines"""
        lines = []
        
        try:
            items = sorted(current.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
            
            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                current_prefix = "└── " if is_last else "├── "
                lines.append(f"{prefix}{current_prefix}{item.name}")
                
                if item.is_dir():
                    extension = "    " if is_last else "│   "
                    lines.extend(self._generate_tree(root, item, prefix + extension))
        except PermissionError:
            lines.append(f"{prefix}└── [Permission Denied]")
        
        return lines
    
    def self_test(self, context: SkillContext) -> List[SkillHealthIssue]:
        """Run health checks on this skill"""
        issues = []
        
        default_repo = Path(context.config.storage.default_repo_root)
        if not default_repo.exists():
            issues.append(SkillHealthIssue(
                code="default_repo_missing",
                message=f"Default repo root does not exist: {default_repo}",
                suggestion="Update otto_config.yaml with a valid default_repo_root"
            ))
        
        return issues

