"""
Task runner for Otto
"""

from typing import List
from .models import Task, TaskResult
from .skill_base import Skill, SkillContext


def run_tasks(
    tasks: List[Task],
    skills: List[Skill],
    context: SkillContext
) -> List[TaskResult]:
    """
    Run a list of tasks using available skills.
    
    For each task, finds the first skill that can handle it,
    then executes the task.
    """
    results: List[TaskResult] = []
    
    for task in tasks:
        # Find a skill that can handle this task
        handler: Skill | None = None
        for skill in skills:
            if skill.can_handle(task):
                handler = skill
                break
        
        if handler is None:
            results.append(TaskResult(
                task_id=task.id,
                success=False,
                message=f"No skill found to handle task type: {task.type}"
            ))
            continue
        
        # Execute the task
        try:
            result = handler.run(task, context)
            results.append(result)
        except Exception as e:
            results.append(TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error executing task: {str(e)}"
            ))
    
    return results

