"""
Core data models for Otto
"""

from typing import Any, Dict, Optional, List
from dataclasses import dataclass
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


@dataclass
class Task:
    """Represents a task for Otto to execute"""
    id: str
    type: str
    payload: Dict[str, Any]
    source: str = "cli"  # e.g., "cli", "doc", "life_os"
    status: TaskStatus = TaskStatus.PENDING


@dataclass
class TaskResult:
    """Result of executing a task"""
    task_id: str
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    actions: Optional[List[Dict[str, Any]]] = None
    reasoning: Optional[Dict[str, Any]] = None  # Phase 2.5: Structured reasoning steps
    evidence: Optional[Dict[str, Any]] = None  # Phase 2.5: IDs of entities consulted

