"""
Life OS Tasks API - Manage household tasks
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models import LifeOSTask

router = APIRouter(prefix="/life_os/tasks", tags=["life-os-tasks"])


class CreateTaskRequest(BaseModel):
    """Request to create a new Life OS task"""
    title: str
    description: Optional[str] = None
    assignee: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None  # low, medium, high
    category: Optional[str] = None


class UpdateTaskRequest(BaseModel):
    """Request to update a Life OS task"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None  # todo, in_progress, done, blocked
    assignee: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None
    category: Optional[str] = None


class TaskResponse(BaseModel):
    """Response model for Life OS task"""
    id: int
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
    title: str
    description: Optional[str]
    status: str
    assignee: Optional[str]
    due_date: Optional[datetime]
    priority: Optional[str]
    category: Optional[str]

    class Config:
        from_attributes = True


@router.post("", response_model=TaskResponse)
async def create_task(request: CreateTaskRequest, db: Session = Depends(get_db)):
    """Create a new Life OS task"""
    task = LifeOSTask(
        title=request.title,
        description=request.description,
        assignee=request.assignee,
        due_date=request.due_date,
        priority=request.priority,
        category=request.category
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    
    # Phase 2.5: Emit event
    from otto.events import emit_event
    from otto.context import get_default_context
    otto_context = get_default_context(db)
    emit_event(
        db,
        household_id=otto_context.household_id,
        event_type="task.created",
        source_model="LifeOSTask",
        source_id=task.id,
        payload={"title": task.title, "status": task.status}
    )
    db.commit()
    
    return task


@router.get("", response_model=List[TaskResponse])
async def list_tasks(
    status: Optional[str] = Query(None, description="Filter by status"),
    assignee: Optional[str] = Query(None, description="Filter by assignee"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """List Life OS tasks with optional filters"""
    query = db.query(LifeOSTask)
    
    if status:
        query = query.filter(LifeOSTask.status == status)
    if assignee:
        query = query.filter(LifeOSTask.assignee == assignee)
    if category:
        query = query.filter(LifeOSTask.category == category)
    
    tasks = query.order_by(LifeOSTask.due_date.asc().nulls_last(), LifeOSTask.created_at.desc()).limit(limit).all()
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get details of a specific Life OS task"""
    task = db.query(LifeOSTask).filter(LifeOSTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, request: UpdateTaskRequest, db: Session = Depends(get_db)):
    """Update a Life OS task"""
    task = db.query(LifeOSTask).filter(LifeOSTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update fields
    if request.title is not None:
        task.title = request.title
    if request.description is not None:
        task.description = request.description
    if request.status is not None:
        task.status = request.status
        # Set completed_at if status is "done"
        if request.status == "done" and task.completed_at is None:
            task.completed_at = datetime.utcnow()
        elif request.status != "done":
            task.completed_at = None
    if request.assignee is not None:
        task.assignee = request.assignee
    if request.due_date is not None:
        task.due_date = request.due_date
    if request.priority is not None:
        task.priority = request.priority
    if request.category is not None:
        task.category = request.category
    
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a Life OS task"""
    task = db.query(LifeOSTask).filter(LifeOSTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}

