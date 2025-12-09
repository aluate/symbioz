"""
Health check runner for Otto skills
"""

from typing import List, Dict
from dataclasses import dataclass
from .skill_base import Skill, SkillHealthIssue, SkillContext


@dataclass
class HealthReport:
    """Report of health checks across all skills"""
    issues: Dict[str, List[SkillHealthIssue]]
    
    def has_issues(self) -> bool:
        """Check if any skills have issues"""
        return any(len(issues) > 0 for issues in self.issues.values())
    
    def total_issues(self) -> int:
        """Get total number of issues"""
        return sum(len(issues) for issues in self.issues.values())


def run_skill_health_checks(
    skills: List[Skill],
    context: SkillContext
) -> HealthReport:
    """
    Run health checks on all skills and return a report.
    """
    issues: Dict[str, List[SkillHealthIssue]] = {}
    
    for skill in skills:
        skill_issues = skill.self_test(context)
        if skill_issues:
            issues[skill.name] = skill_issues
    
    return HealthReport(issues=issues)

