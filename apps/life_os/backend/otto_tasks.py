"""
Otto Tasks API - Endpoints for managing Otto tasks
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models import OttoTask

router = APIRouter(prefix="/otto/tasks", tags=["otto-tasks"])


class CreateTaskRequest(BaseModel):
    """Request to create a new Otto task"""
    type: str  # e.g. "life_os.create_task", "infra.deploy", etc.
    description: str
    payload: Optional[Dict[str, Any]] = None
    next_run_at: Optional[datetime] = None  # For scheduled tasks


class TaskResponse(BaseModel):
    """Response model for Otto task"""
    id: int
    created_at: datetime
    updated_at: datetime
    status: str
    type: str
    description: str
    payload: Optional[Dict[str, Any]] = None
    next_run_at: Optional[datetime] = None
    last_run_at: Optional[datetime] = None
    last_error: Optional[str] = None

    class Config:
        from_attributes = True


@router.post("", response_model=TaskResponse)
async def create_task(request: CreateTaskRequest, db: Session = Depends(get_db)):
    """
    Create a new Otto task.
    
    Tasks represent work that Otto should do. The worker loop will
    process pending tasks and create OttoRun records.
    """
    task = OttoTask(
        status="pending",
        type=request.type,
        description=request.description,
        payload=request.payload,
        next_run_at=request.next_run_at
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("", response_model=List[TaskResponse])
async def list_tasks(
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(50, ge=1, le=200, description="Maximum number of tasks to return"),
    db: Session = Depends(get_db)
):
    """List Otto tasks, optionally filtered by status"""
    query = db.query(OttoTask)
    
    if status:
        query = query.filter(OttoTask.status == status)
    
    tasks = query.order_by(OttoTask.created_at.desc()).limit(limit).all()
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get details of a specific Otto task"""
    task = db.query(OttoTask).filter(OttoTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

