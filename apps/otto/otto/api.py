"""
Otto API Server - HTTP interface for receiving prompts from anywhere
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uuid
import os
from datetime import datetime

from .config import load_config
from .core.models import Task, TaskStatus, TaskResult
from .core.skill_base import SkillContext
from .core.runner import run_tasks
from .core.logging_utils import get_logger
from .skills import get_all_skills

logger = get_logger(__name__)

app = FastAPI(
    title="Otto API",
    description="HTTP API for sending prompts and tasks to Otto",
    version="0.1.0"
)

# CORS configuration - allow requests from anywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
_config = None
_context = None
_skills = None


def get_context():
    """Get or create Otto context"""
    global _config, _context, _skills
    if _config is None:
        _config = load_config()
        _context = SkillContext(config=_config, logger=logger)
        _skills = get_all_skills()
    return _context, _skills


class PromptRequest(BaseModel):
    """Request model for sending a prompt"""
    prompt: str
    task_type: Optional[str] = None  # If not provided, will try to infer
    payload: Optional[Dict[str, Any]] = None
    source: str = "api"


class TaskRequest(BaseModel):
    """Request model for sending a structured task"""
    type: str
    payload: Dict[str, Any]
    source: str = "api"


class PromptResponse(BaseModel):
    """Response model for prompt submission"""
    task_id: str
    status: str
    message: str
    result: Optional[Dict[str, Any]] = None
    actions: Optional[List[Dict[str, Any]]] = None  # Structured actions for executor
    reasoning: Optional[Dict[str, Any]] = None  # Phase 2.5: Structured reasoning steps
    evidence: Optional[Dict[str, Any]] = None  # Phase 2.5: IDs of entities consulted


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Otto API",
        "status": "running",
        "version": "0.1.0"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/capabilities")
async def capabilities():
    """Check which API tokens are available (without exposing values)"""
    import os
    
    return {
        "github_token": bool(os.getenv("GITHUB_TOKEN")),
        "vercel_token": bool(os.getenv("VERCEL_TOKEN")),
        "render_api_key": bool(os.getenv("RENDER_API_KEY")),
    }


@app.post("/prompt", response_model=PromptResponse)
async def submit_prompt(request: PromptRequest):
    """
    Submit a text prompt to Otto.
    
    Otto will try to understand the prompt and execute it using available skills.
    """
    context, skills = get_context()
    
    # For now, we'll create a generic "prompt" task type
    # In the future, this could use LLM to parse the prompt and route to skills
    task_id = str(uuid.uuid4())
    
    # Create a task with the prompt
    task = Task(
        id=task_id,
        type=request.task_type or "prompt",
        payload={
            "prompt": request.prompt,
            **(request.payload or {})
        },
        source=request.source,
        status=TaskStatus.PENDING
    )
    
    # Try to find a skill that can handle this
    # For now, if it's a generic prompt, we'll create a simple response
    # In Phase 2, this will use LLM to route to appropriate skills
    
    # Check if any skill can handle it
    handler = None
    for skill in skills:
        if skill.can_handle(task):
            handler = skill
            break
    
    if handler:
        # Execute with the skill
        results = run_tasks([task], skills, context)
        result = results[0]
        
        return PromptResponse(
            task_id=task_id,
            status="success" if result.success else "failed",
            message=result.message,
            result=result.data,
            actions=result.actions,
            reasoning=result.reasoning,
            evidence=result.evidence
        )
    else:
        # No skill can handle it - return a message that it will be processed later
        # In Phase 2, this will queue for LLM processing
        return PromptResponse(
            task_id=task_id,
            status="queued",
            message=f"Prompt received: '{request.prompt[:100]}...'. Will be processed when LLM integration is available.",
            result={"note": "LLM integration coming in Phase 2"}
        )


@app.post("/task", response_model=PromptResponse)
async def submit_task(request: TaskRequest):
    """
    Submit a structured task to Otto.
    
    Use this when you know the exact task type and payload.
    """
    context, skills = get_context()
    
    task_id = str(uuid.uuid4())
    
    task = Task(
        id=task_id,
        type=request.type,
        payload=request.payload,
        source=request.source,
        status=TaskStatus.PENDING
    )
    
    # Execute the task
    results = run_tasks([task], skills, context)
    result = results[0]
    
    # Extract actions from result.data if present
    actions = None
    if result.data and isinstance(result.data, dict):
        actions = result.data.get("actions")
        # If actions were extracted, remove them from result.data
        if actions:
            result_data = {k: v for k, v in result.data.items() if k != "actions"}
        else:
            result_data = result.data
    else:
        result_data = result.data
    
    return PromptResponse(
        task_id=task_id,
        status="success" if result.success else "failed",
        message=result.message,
        result=result_data,
        actions=actions or result.actions,
        reasoning=result.reasoning,
        evidence=result.evidence
    )


@app.get("/skills")
async def list_skills():
    """List all available Otto skills"""
    context, skills = get_context()
    
    return {
        "skills": [
            {
                "name": skill.name,
                "description": getattr(skill, "description", "No description available")
            }
            for skill in skills
        ]
    }


class MonitorRepairRequest(BaseModel):
    """Request model for monitor/repair/redeploy"""
    mode: str = "pr"  # "pr" or "main"
    targets: Dict[str, Any]
    maxIterations: int = 5


@app.post("/skills/monitor_repair_redeploy")
async def monitor_repair_redeploy(request: MonitorRepairRequest):
    """Trigger monitor/repair/redeploy loop"""
    context, skills = get_context()
    
    task_id = str(uuid.uuid4())
    task = Task(
        id=task_id,
        type="monitor_repair_redeploy",
        payload={
            "mode": request.mode,
            "targets": request.targets,
            "maxIterations": request.maxIterations
        },
        source="api",
        status=TaskStatus.PENDING
    )
    
    # Find the skill
    skill = None
    for s in skills:
        if hasattr(s, "can_handle") and s.can_handle(task):
            skill = s
            break
    
    if not skill:
        raise HTTPException(status_code=404, detail="Monitor repair skill not found")
    
    # Execute
    result = skill.run(task, context)
    
    return {
        "task_id": task_id,
        "status": "success" if result.success else "failed",
        "message": result.message,
        "data": result.data
    }


class DeployMonitorRequest(BaseModel):
    """Request model for deploy monitor with defaults"""
    mode: str = "pr"
    maxIterations: int = 5


@app.post("/actions/run_deploy_monitor")
async def run_deploy_monitor(request: DeployMonitorRequest):
    """Run deploy monitor with saved config defaults"""
    # Default targets - read from environment variables
    default_targets = {}
    
    # Vercel target
    vercel_project = os.getenv("VERCEL_PROJECT_ID") or os.getenv("VERCEL_PROJECT_NAME")
    if vercel_project:
        default_targets["vercel"] = {
            "projectNameOrId": vercel_project,
            "teamId": os.getenv("VERCEL_TEAM_ID")
        }
    
    # Render targets - can monitor multiple services
    render_services = []
    if os.getenv("RENDER_SERVICE_ID_OTTO"):
        render_services.append({
            "name": "otto",
            "serviceId": os.getenv("RENDER_SERVICE_ID_OTTO")
        })
    if os.getenv("RENDER_SERVICE_ID_SYMBIOZ"):
        render_services.append({
            "name": "symbioz",
            "serviceId": os.getenv("RENDER_SERVICE_ID_SYMBIOZ")
        })
    
    # Use first Render service if available, or allow multiple
    if render_services:
        # For now, monitor the first one (can be extended to monitor all)
        default_targets["render"] = {
            "serviceId": render_services[0]["serviceId"]
        }
    
    if not default_targets:
        raise HTTPException(
            status_code=400,
            detail="No monitoring targets configured. Set VERCEL_PROJECT_ID/NAME and/or RENDER_SERVICE_ID_* environment variables."
        )
    
    monitor_request = MonitorRepairRequest(
        mode=request.mode,
        targets=default_targets,
        maxIterations=request.maxIterations
    )
    
    return await monitor_repair_redeploy(monitor_request)


def run_server(host: str = "0.0.0.0", port: int = 8001):
    """Run the Otto API server"""
    import uvicorn
    logger.info(f"Starting Otto API server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run_server()

