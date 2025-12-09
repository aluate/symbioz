"""
Calendar API - Manage calendar events
Renamed from calendar.py to avoid conflict with Python's standard library calendar module
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from database import get_db
from models import CalendarEvent

router = APIRouter(prefix="/calendar", tags=["calendar"])


class CreateEventRequest(BaseModel):
    """Request to create a new calendar event"""
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    attendees: Optional[str] = None
    category: Optional[str] = None
    is_recurring: Optional[str] = "no"  # yes, no
    recurrence_frequency: Optional[str] = None  # daily, weekly, monthly, yearly
    recurrence_end_date: Optional[datetime] = None
    external_calendar_type: Optional[str] = None  # google, outlook, etc.
    reminders: Optional[List[dict]] = None  # [{"minutes": 15}, {"minutes": 60}]


class UpdateEventRequest(BaseModel):
    """Request to update a calendar event"""
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    attendees: Optional[str] = None
    category: Optional[str] = None
    is_recurring: Optional[str] = None
    recurrence_frequency: Optional[str] = None
    recurrence_end_date: Optional[datetime] = None
    status: Optional[str] = None  # confirmed, tentative, cancelled
    reminders: Optional[List[dict]] = None


class EventResponse(BaseModel):
    """Response model for a calendar event"""
    id: int
    created_at: datetime
    updated_at: datetime
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: Optional[datetime]
    location: Optional[str]
    attendees: Optional[str]
    category: Optional[str]
    is_recurring: str
    recurrence_frequency: Optional[str]
    recurrence_end_date: Optional[datetime]
    external_calendar_id: Optional[str]
    external_calendar_type: Optional[str]
    external_sync_enabled: str
    status: str
    reminders: Optional[List[dict]]

    class Config:
        from_attributes = True


@router.post("", response_model=dict)
def create_event(
    request: CreateEventRequest,
    db: Session = Depends(get_db)
):
    """Create a new calendar event"""
    try:
        from otto.context import get_default_context
        from otto.events import emit_event
        
        otto_context = get_default_context(db)
        
        # Create event
        event = CalendarEvent(
            household_id=otto_context.household_id,
            title=request.title,
            description=request.description,
            start_time=request.start_time,
            end_time=request.end_time or request.start_time,
            location=request.location,
            attendees=request.attendees,
            category=request.category,
            is_recurring=request.is_recurring == "yes",
            recurrence_frequency=request.recurrence_frequency,
            recurrence_end_date=request.recurrence_end_date,
            external_calendar_type=request.external_calendar_type,
            reminders=request.reminders
        )
        
        db.add(event)
        db.commit()
        db.refresh(event)
        
        # Emit event for Otto
        emit_event(
            db=db,
            event_type="calendar.created",
            entity_type="calendar_event",
            entity_id=event.id,
            household_id=otto_context.household_id,
            payload={
                "title": event.title,
                "start_time": event.start_time.isoformat(),
                "category": event.category
            }
        )
        
        return {
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "start_time": event.start_time.isoformat(),
            "end_time": event.end_time.isoformat() if event.end_time else None,
            "location": event.location,
            "category": event.category,
            "created_at": event.created_at.isoformat()
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create event: {str(e)}")


@router.get("", response_model=List[EventResponse])
async def list_events(
    start_date: Optional[datetime] = Query(None, description="Filter events starting from this date"),
    end_date: Optional[datetime] = Query(None, description="Filter events ending before this date"),
    category: Optional[str] = Query(None, description="Filter by category"),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """List calendar events with optional filters"""
    from otto.context import get_default_context
    
    otto_context = get_default_context(db)
    query = db.query(CalendarEvent).filter(
        CalendarEvent.household_id == otto_context.household_id
    )
    
    if start_date:
        query = query.filter(CalendarEvent.start_time >= start_date)
    if end_date:
        query = query.filter(CalendarEvent.start_time <= end_date)
    if category:
        query = query.filter(CalendarEvent.category == category)
    if status:
        query = query.filter(CalendarEvent.status == status)
    
    events = query.order_by(CalendarEvent.start_time.asc()).limit(limit).all()
    return events


@router.get("/{event_id}", response_model=dict)
def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific calendar event"""
    try:
        from otto.context import get_default_context
        
        otto_context = get_default_context(db)
        
        event = db.query(CalendarEvent).filter(
            CalendarEvent.id == event_id,
            CalendarEvent.household_id == otto_context.household_id
        ).first()
        
        if not event:
            raise HTTPException(status_code=404, detail=f"Event {event_id} not found")
        
        return {
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "start_time": event.start_time.isoformat(),
            "end_time": event.end_time.isoformat() if event.end_time else None,
            "location": event.location,
            "category": event.category,
            "is_recurring": event.is_recurring,
            "recurrence_frequency": event.recurrence_frequency,
            "recurrence_end_date": event.recurrence_end_date.isoformat() if event.recurrence_end_date else None,
            "external_calendar_type": event.external_calendar_type,
            "reminders": event.reminders,
            "created_at": event.created_at.isoformat(),
            "updated_at": event.updated_at.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get event: {str(e)}")


@router.patch("/{event_id}", response_model=EventResponse)
async def update_event(event_id: int, request: UpdateEventRequest, db: Session = Depends(get_db)):
    """Update a calendar event"""
    from otto.context import get_default_context
    
    otto_context = get_default_context(db)
    event = db.query(CalendarEvent).filter(
        CalendarEvent.id == event_id,
        CalendarEvent.household_id == otto_context.household_id
    ).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Update fields
    if request.title is not None:
        event.title = request.title
    if request.description is not None:
        event.description = request.description
    if request.start_time is not None:
        event.start_time = request.start_time
    if request.end_time is not None:
        event.end_time = request.end_time
    if request.location is not None:
        event.location = request.location
    if request.attendees is not None:
        event.attendees = request.attendees
    if request.category is not None:
        event.category = request.category
    if request.is_recurring is not None:
        event.is_recurring = request.is_recurring
    if request.recurrence_frequency is not None:
        event.recurrence_frequency = request.recurrence_frequency
    if request.recurrence_end_date is not None:
        event.recurrence_end_date = request.recurrence_end_date
    if request.status is not None:
        event.status = request.status
    if request.reminders is not None:
        event.reminders = request.reminders
    
    db.commit()
    db.refresh(event)
    return event


@router.delete("/{event_id}")
async def delete_event(event_id: int, db: Session = Depends(get_db)):
    """Delete a calendar event"""
    from otto.context import get_default_context
    
    otto_context = get_default_context(db)
    event = db.query(CalendarEvent).filter(
        CalendarEvent.id == event_id,
        CalendarEvent.household_id == otto_context.household_id
    ).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db.delete(event)
    db.commit()
    return {"message": "Event deleted"}


@router.get("/today/summary", response_model=dict)
async def get_today_summary(db: Session = Depends(get_db)):
    """Get summary of today's events"""
    from otto.context import get_default_context
    
    otto_context = get_default_context(db)
    now = datetime.utcnow()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    
    today_events = db.query(CalendarEvent).filter(
        CalendarEvent.household_id == otto_context.household_id,
        CalendarEvent.start_time >= start_of_day,
        CalendarEvent.start_time < end_of_day,
        CalendarEvent.status != "cancelled"
    ).order_by(CalendarEvent.start_time.asc()).all()
    
    # Get upcoming events (next 7 days)
    future_date = now + timedelta(days=7)
    upcoming_events = db.query(CalendarEvent).filter(
        CalendarEvent.household_id == otto_context.household_id,
        CalendarEvent.start_time >= now,
        CalendarEvent.start_time <= future_date,
        CalendarEvent.status != "cancelled"
    ).order_by(CalendarEvent.start_time.asc()).limit(10).all()
    
    return {
        "today_count": len(today_events),
        "today_events": [EventResponse.from_orm(e).dict() for e in today_events],
        "upcoming_count": len(upcoming_events),
        "upcoming_events": [EventResponse.from_orm(e).dict() for e in upcoming_events]
    }

