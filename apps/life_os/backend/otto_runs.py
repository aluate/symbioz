"""
Otto Runs API - Endpoints for managing Otto run history
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from datetime import datetime
import httpx
import os
import json

from database import get_db, init_db
from models import OttoRun

router = APIRouter(prefix="/otto/runs", tags=["otto-runs"])

# Otto API configuration - use env var or default
OTTO_API_URL = os.getenv("OTTO_API_URL", "http://localhost:8001")


class CreateRunRequest(BaseModel):
    """Request to create a new Otto run"""
    input_text: str
    input_payload: Optional[Dict[str, Any]] = None
    mode: Optional[str] = "chat"  # chat or task


class RunResponse(BaseModel):
    """Response model for Otto run"""
    id: int
    created_at: datetime
    updated_at: datetime
    status: str
    source: str
    input_text: str
    input_payload: Optional[Dict[str, Any]] = None
    output_text: Optional[str] = None
    output_payload: Optional[Dict[str, Any]] = None
    logs: Optional[str] = None

    class Config:
        from_attributes = True


async def call_otto_api(input_text: str, input_payload: Optional[Dict[str, Any]] = None, mode: str = "chat") -> Dict[str, Any]:
    """
    Call Otto API with a prompt.
    
    This function is separate from the endpoint so it can be reused
    by a background worker in the future.
    """
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            if mode == "task" and input_payload:
                # Use structured task endpoint
                response = await client.post(
                    f"{OTTO_API_URL}/task",
                    json={
                        "type": input_payload.get("type", "prompt"),
                        "payload": input_payload.get("payload", {}),
                        "source": "life_os_shell"
                    }
                )
            else:
                # Use prompt endpoint
                response = await client.post(
                    f"{OTTO_API_URL}/prompt",
                    json={
                        "prompt": input_text,
                        "payload": input_payload,
                        "source": "life_os_shell"
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


@router.post("", response_model=RunResponse)
async def create_run(request: CreateRunRequest, db: Session = Depends(get_db)):
    """
    Create a new Otto run and execute it.
    
    This endpoint:
    1. Creates a run record with status="pending"
    2. Calls Otto API
    3. Updates the run with results
    """
    # Create run record
    run = OttoRun(
        status="pending",
        source="shell",
        input_text=request.input_text,
        input_payload=request.input_payload
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    
    # Update status to running
    run.status = "running"
    db.commit()
    
    try:
        # Call Otto API
        otto_response = await call_otto_api(
            request.input_text,
            request.input_payload,
            request.mode
        )
        
        # Extract response data
        output_text = None
        output_payload = None
        
        if isinstance(otto_response, dict):
            # Try to extract meaningful text
            output_text = otto_response.get("message") or otto_response.get("result", {}).get("message")
            if not output_text and otto_response.get("result"):
                # If result is a dict, try to stringify it nicely
                result = otto_response.get("result")
                if isinstance(result, dict):
                    output_text = json.dumps(result, indent=2)
                else:
                    output_text = str(result)
            
            # Store full response as payload
            output_payload = otto_response
        
        # Update run with results
        run.status = "success" if otto_response.get("status") in ["success", "queued"] else "error"
        run.output_text = output_text
        run.output_payload = output_payload
        run.logs = json.dumps(otto_response, indent=2)
        
    except HTTPException as e:
        # HTTPException from call_otto_api
        run.status = "error"
        run.logs = f"Error: {e.detail}"
        raise
    except Exception as e:
        # Any other error
        run.status = "error"
        run.logs = f"Unexpected error: {str(e)}"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Error executing Otto run: {str(e)}")
    
    db.commit()
    db.refresh(run)
    
    return run


@router.get("", response_model=List[RunResponse])
async def list_runs(limit: int = 20, db: Session = Depends(get_db)):
    """List recent Otto runs"""
    runs = db.query(OttoRun).order_by(OttoRun.created_at.desc()).limit(limit).all()
    return runs


@router.get("/{run_id}", response_model=RunResponse)
async def get_run(run_id: int, db: Session = Depends(get_db)):
    """Get details of a specific Otto run"""
    run = db.query(OttoRun).filter(OttoRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run

