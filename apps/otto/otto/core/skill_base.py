"""
Base classes and interfaces for Otto skills
"""

from typing import Protocol, List, Optional, Any
from dataclasses import dataclass
from .models import Task, TaskResult


@dataclass
class SkillHealthIssue:
    """Represents a health issue found in a skill"""
    code: str
    message: str
    suggestion: Optional[str] = None


@dataclass
class SkillContext:
    """Context passed to skills when executing"""
    config: Any  # AppConfig
    logger: Any  # logging.Logger (will be added later)


class Skill(Protocol):
    """Protocol that all Otto skills must implement"""
    
    name: str
    
    def can_handle(self, task: Task) -> bool:
        """Check if this skill can handle the given task"""
        ...
    
    def run(self, task: Task, context: SkillContext) -> TaskResult:
        """Execute the task"""
        ...
    
    def self_test(self, context: SkillContext) -> List[SkillHealthIssue]:
        """Run health checks on this skill"""
        ...

