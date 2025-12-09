"""
Life OS - Otto Integration API
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import httpx

router = APIRouter(prefix="/otto", tags=["otto"])

# Otto API configuration - use env var or default
import os
OTTO_API_URL = os.getenv("OTTO_API_URL", "http://localhost:8001")


class PromptRequest(BaseModel):
    """Request to send a prompt to Otto"""
    prompt: str
    task_type: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None


class TaskRequest(BaseModel):
    """Request to send a structured task to Otto"""
    type: str
    payload: Dict[str, Any]


@router.post("/prompt")
async def send_prompt_to_otto(request: PromptRequest):
    """
    Send a text prompt to Otto via the Otto API.
    
    This allows Life OS to forward prompts to Otto for processing.
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{OTTO_API_URL}/prompt",
                json={
                    "prompt": request.prompt,
                    "task_type": request.task_type,
                    "payload": request.payload,
                    "source": "life_os"
                }
            )
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Could not connect to Otto API: {str(e)}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Otto API error: {e.response.text}"
        )


@router.post("/task")
async def send_task_to_otto(request: TaskRequest):
    """
    Send a structured task to Otto via the Otto API.
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{OTTO_API_URL}/task",
                json={
                    "type": request.type,
                    "payload": request.payload,
                    "source": "life_os"
                }
            )
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Could not connect to Otto API: {str(e)}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Otto API error: {e.response.text}"
        )


@router.get("/skills")
async def get_otto_skills():
    """Get list of available Otto skills"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{OTTO_API_URL}/skills")
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Could not connect to Otto API: {str(e)}"
        )


@router.get("/health")
async def check_otto_health():
    """Check if Otto API is available"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{OTTO_API_URL}/health")
            response.raise_for_status()
            return {"status": "connected", "otto_status": response.json()}
    except Exception as e:
        return {"status": "disconnected", "error": str(e)}


class ActionsRequest(BaseModel):
    """Request to execute Otto actions"""
    actions: List[Dict[str, Any]]


@router.post("/actions")
async def execute_otto_actions(request: ActionsRequest):
    """
    Execute Otto actions directly.
    
    This endpoint allows direct execution of Otto actions without going through
    the Otto API. Useful for testing and direct action execution.
    """
    from database import SessionLocal
    from otto.actions import execute_actions
    from otto.context import get_default_context
    import traceback
    
    db = SessionLocal()
    try:
        otto_context = get_default_context(db)
        
        # Execute actions
        execution_result = execute_actions(
            db=db,
            actions=request.actions,
            otto_context=otto_context
        )
        
        # Only commit if all actions succeeded or if failures are non-critical
        if execution_result.failed == 0 or all(r.success for r in execution_result.results if r.action_type != "execution_halted"):
            db.commit()
        else:
            # Some actions failed, but commit anyway (actions handle their own rollback)
            db.commit()
        
        # Convert results to dict format
        results = []
        for result in execution_result.results:
            results.append({
                "action_type": result.action_type,
                "success": result.success,
                "message": result.message,
                "error": result.error
            })
        
        return {
            "summary": execution_result.summary,
            "total": execution_result.total,
            "succeeded": execution_result.succeeded,
            "failed": execution_result.failed,
            "results": results
        }
    except Exception as e:
        db.rollback()
        error_trace = traceback.format_exc()
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to execute actions: {str(e)}\n{error_trace}"
        )
    finally:
        db.close()