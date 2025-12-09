"""
OttoMemorySkill - Long-term memory management for Otto
Phase 3 Extension — CONTROL_OTTO_LONG_TERM_MEMORY.md
"""

from typing import List, Dict, Any, Optional
import os
import httpx
from datetime import datetime

from ..core.models import Task, TaskResult, TaskStatus
from ..core.skill_base import Skill, SkillHealthIssue, SkillContext
from ..core.logging_utils import get_logger

logger = get_logger(__name__)


class OttoMemorySkill:
    """Skill for managing Otto's long-term memory"""
    
    name = "memory"
    description = "Manages Otto's structured long-term memory (preferences, rules, facts, workflow cues)"
    
    def __init__(self):
        # Life OS backend API URL
        self.life_os_api_url = os.getenv("LIFE_OS_API_URL", "http://localhost:8000")
    
    def can_handle(self, task: Task) -> bool:
        """Check if this skill can handle the task"""
        return task.type in [
            "memory.remember",
            "memory.recall",
            "memory.lookup",
            "memory.search",
            "memory.update",
            "memory.propose",
            "memory.delete"
        ]
    
    def run(self, task: Task, context: SkillContext) -> TaskResult:
        """Execute the memory operation"""
        try:
            if task.type == "memory.remember":
                return self._handle_remember(task, context)
            elif task.type == "memory.recall":
                return self._handle_recall(task, context)
            elif task.type == "memory.lookup":
                return self._handle_lookup(task, context)
            elif task.type == "memory.search":
                return self._handle_search(task, context)
            elif task.type == "memory.update":
                return self._handle_update(task, context)
            elif task.type == "memory.propose":
                return self._handle_propose(task, context)
            elif task.type == "memory.delete":
                return self._handle_delete(task, context)
            else:
                return TaskResult(
                    task_id=task.id,
                    success=False,
                    message=f"Unknown memory operation: {task.type}"
                )
        except Exception as e:
            logger.error(f"Error in OttoMemorySkill: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error in memory operation: {str(e)}"
            )
    
    def _handle_remember(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle memory.remember - Add new memory"""
        payload = task.payload or {}
        
        category = payload.get("category")
        content = payload.get("content")
        tags = payload.get("tags", [])
        source = payload.get("source", "user")
        confidence_score = payload.get("confidence_score", 1.0)
        
        if not category or not content:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required fields: 'category', 'content'"
            )
        
        # Create action to add memory
        actions = [{
            "type": "memory.create",
            "tier": 2,
            "payload": {
                "category": category,
                "content": content,
                "tags": tags,
                "source": source,
                "confidence_score": confidence_score
            }
        }]
        
        return TaskResult(
            task_id=task.id,
            success=True,
            message=f"Memory proposal created: {category} - {content[:50]}...",
            data={"action_created": True},
            actions=actions,
            reasoning={
                "steps": [{
                    "id": "step1",
                    "type": "proposal",
                    "summary": f"Proposed memory: {category} - {content[:50]}...",
                    "evidence": [{"kind": "memory_proposal", "category": category, "source": source}]
                }]
            },
            evidence={"category": category, "source": source}
        )
    
    def _handle_recall(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle memory.recall - Retrieve specific memory by ID"""
        payload = task.payload or {}
        memory_id = payload.get("id")
        
        if not memory_id:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required field: 'id'"
            )
        
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(f"{self.life_os_api_url}/otto/memory/{memory_id}")
                
                if response.status_code == 200:
                    memory = response.json()
                    
                    # Mark as used
                    client.post(
                        f"{self.life_os_api_url}/otto/memory/use",
                        json={"id": memory_id}
                    )
                    
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=f"Recalled memory: {memory.get('content', '')[:50]}...",
                        data={"memory": memory},
                        reasoning={
                            "steps": [{
                                "id": "step1",
                                "type": "recall",
                                "summary": f"Retrieved memory ID {memory_id}",
                                "evidence": [{"kind": "memory", "id": memory_id}]
                            }]
                        },
                        evidence={"memory_id": memory_id}
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Memory {memory_id} not found"
                    )
        except Exception as e:
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error recalling memory: {str(e)}"
            )
    
    def _handle_search(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle memory.search - Search memories with filters"""
        payload = task.payload or {}
        
        q = payload.get("q")
        category = payload.get("category")
        tag = payload.get("tag")
        source = payload.get("source")
        is_stale = payload.get("is_stale")
        limit = payload.get("limit", 50)
        
        try:
            with httpx.Client(timeout=10.0) as client:
                params = {"limit": limit}
                if q:
                    params["q"] = q
                if category:
                    params["category"] = category
                if tag:
                    params["tag"] = tag
                if source:
                    params["source"] = source
                if is_stale is not None:
                    params["is_stale"] = is_stale
                
                response = client.get(
                    f"{self.life_os_api_url}/otto/memory/search",
                    params=params
                )
                
                if response.status_code == 200:
                    memories = response.json()
                    
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=f"Found {len(memories)} memory(ies) matching search",
                        data={"memories": memories, "count": len(memories)},
                        reasoning={
                            "steps": [{
                                "id": "step1",
                                "type": "search",
                                "summary": f"Searched memories with query: {q or 'none'}",
                                "evidence": [{"kind": "memory_search", "query": q, "filters": {"category": category, "tag": tag}}]
                            }]
                        },
                        evidence={"query": q, "matched_memory_ids": [m.get("id") for m in memories]}
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Error searching memories: {response.status_code}"
                    )
        except Exception as e:
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error searching memories: {str(e)}"
            )
    
    def _handle_lookup(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle memory.lookup - Query memory with filters"""
        payload = task.payload or {}
        
        category = payload.get("category")
        tags = payload.get("tags", [])
        source = payload.get("source")
        limit = payload.get("limit", 50)
        
        try:
            with httpx.Client(timeout=10.0) as client:
                params = {"limit": limit}
                if category:
                    params["category"] = category
                if tags:
                    params["tags"] = ",".join(tags) if isinstance(tags, list) else tags
                if source:
                    params["source"] = source
                
                response = client.get(
                    f"{self.life_os_api_url}/otto/memory",
                    params=params
                )
                
                if response.status_code == 200:
                    memories = response.json()
                    
                    # Mark all as used
                    if memories:
                        use_request = {}
                        if category:
                            use_request["category"] = category
                        if tags:
                            use_request["tags"] = tags
                        
                        if use_request:
                            client.post(
                                f"{self.life_os_api_url}/otto/memory/use",
                                json=use_request
                            )
                    
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=f"Found {len(memories)} memory(ies)",
                        data={"memories": memories, "count": len(memories)},
                        reasoning={
                            "steps": [{
                                "id": "step1",
                                "type": "lookup",
                                "summary": f"Queried memories with filters: category={category}, tags={tags}",
                                "evidence": [{"kind": "memory_query", "filters": {"category": category, "tags": tags}}]
                            }]
                        },
                        evidence={"query_filters": {"category": category, "tags": tags}}
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Error querying memories: {response.status_code}"
                    )
        except Exception as e:
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error looking up memories: {str(e)}"
            )
    
    def _handle_update(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle memory.update - Update existing memory"""
        payload = task.payload or {}
        memory_id = payload.get("id")
        
        if not memory_id:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required field: 'id'"
            )
        
        # Create action to update memory
        actions = [{
            "type": "memory.update",
            "tier": 2,
            "payload": {
                "id": memory_id,
                "content": payload.get("content"),
                "tags": payload.get("tags"),
                "confidence_score": payload.get("confidence_score")
            }
        }]
        
        return TaskResult(
            task_id=task.id,
            success=True,
            message=f"Memory update proposal created for ID {memory_id}",
            data={"action_created": True},
            actions=actions,
            reasoning={
                "steps": [{
                    "id": "step1",
                    "type": "update_proposal",
                    "summary": f"Proposed update for memory ID {memory_id}",
                    "evidence": [{"kind": "memory_update", "id": memory_id}]
                }]
            },
            evidence={"memory_id": memory_id}
        )
    
    def _handle_propose(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle memory.propose - Propose new memory (requires approval)"""
        # This creates a task that requires approval
        payload = task.payload or {}
        
        category = payload.get("category")
        content = payload.get("content")
        tags = payload.get("tags", [])
        source = payload.get("source", "otto_inference")
        confidence_score = payload.get("confidence_score", 0.8)
        reason = payload.get("reason", "")
        
        if not category or not content:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required fields: 'category', 'content'"
            )
        
        # Create action that will require approval
        actions = [{
            "type": "memory.create",
            "tier": 2,  # Requires approval
            "payload": {
                "category": category,
                "content": content,
                "tags": tags,
                "source": source,
                "confidence_score": confidence_score
            },
            "requires_approval": True,
            "reason": reason
        }]
        
        return TaskResult(
            task_id=task.id,
            success=True,
            message=f"Memory proposal created (requires approval): {category} - {content[:50]}...",
            data={
                "action_created": True,
                "requires_approval": True,
                "reason": reason
            },
            actions=actions,
            reasoning={
                "steps": [{
                    "id": "step1",
                    "type": "proposal",
                    "summary": f"Proposed memory requiring approval: {category} - {content[:50]}...",
                    "evidence": [{"kind": "memory_proposal", "category": category, "source": source, "reason": reason}]
                }]
            },
            evidence={"category": category, "source": source, "requires_approval": True}
        )
    
    def _handle_delete(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle memory.delete - Delete memory entry"""
        payload = task.payload or {}
        memory_id = payload.get("id")
        
        if not memory_id:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required field: 'id'"
            )
        
        # Create action to delete memory
        actions = [{
            "type": "memory.delete",
            "tier": 2,  # Requires approval
            "payload": {
                "id": memory_id
            }
        }]
        
        return TaskResult(
            task_id=task.id,
            success=True,
            message=f"Memory deletion proposal created for ID {memory_id}",
            data={"action_created": True},
            actions=actions,
            reasoning={
                "steps": [{
                    "id": "step1",
                    "type": "delete_proposal",
                    "summary": f"Proposed deletion for memory ID {memory_id}",
                    "evidence": [{"kind": "memory_delete", "id": memory_id}]
                }]
            },
            evidence={"memory_id": memory_id}
        )
    
    def self_test(self, context: SkillContext) -> List[SkillHealthIssue]:
        """Run health checks on this skill"""
        issues = []
        
        # Check if Life OS API is reachable
        try:
            life_os_url = os.getenv("LIFE_OS_API_URL", "http://localhost:8000")
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"{life_os_url}/health")
                if response.status_code != 200:
                    issues.append(SkillHealthIssue(
                        code="api_unreachable",
                        message=f"Life OS API not reachable at {life_os_url}",
                        suggestion="Check if Life OS backend is running"
                    ))
        except Exception as e:
            issues.append(SkillHealthIssue(
                code="api_error",
                message=f"Error checking Life OS API: {str(e)}",
                suggestion="Check network connectivity and API URL"
            ))
        
        return issues

