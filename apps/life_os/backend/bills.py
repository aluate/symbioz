"""
Bills API - Manage household bills
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from database import get_db
from models import Bill

router = APIRouter(prefix="/bills", tags=["bills"])


class CreateBillRequest(BaseModel):
    """Request to create a new bill"""
    name: str
    amount: str
    due_date: datetime
    category: Optional[str] = None
    payee: Optional[str] = None
    account_number: Optional[str] = None
    notes: Optional[str] = None
    is_recurring: Optional[str] = "no"  # yes, no
    recurrence_frequency: Optional[str] = None  # monthly, quarterly, yearly


class UpdateBillRequest(BaseModel):
    """Request to update a bill"""
    name: Optional[str] = None
    amount: Optional[str] = None
    due_date: Optional[datetime] = None
    paid: Optional[str] = None  # yes, no, partial
    category: Optional[str] = None
    payee: Optional[str] = None
    account_number: Optional[str] = None
    notes: Optional[str] = None
    is_recurring: Optional[str] = None
    recurrence_frequency: Optional[str] = None
    next_due_date: Optional[datetime] = None


class BillResponse(BaseModel):
    """Response model for a bill"""
    id: int
    created_at: datetime
    updated_at: datetime
    paid_at: Optional[datetime]
    name: str
    amount: str
    due_date: datetime
    paid: str
    category: Optional[str]
    payee: Optional[str]
    account_number: Optional[str]
    notes: Optional[str]
    is_recurring: str
    recurrence_frequency: Optional[str]
    next_due_date: Optional[datetime]

    class Config:
        from_attributes = True


@router.post("", response_model=BillResponse)
async def create_bill(request: CreateBillRequest, db: Session = Depends(get_db)):
    """Create a new bill"""
    bill = Bill(
        name=request.name,
        amount=request.amount,
        due_date=request.due_date,
        category=request.category,
        payee=request.payee,
        account_number=request.account_number,
        notes=request.notes,
        is_recurring=request.is_recurring or "no",
        recurrence_frequency=request.recurrence_frequency
    )
    
    # Calculate next_due_date for recurring bills
    if request.is_recurring == "yes" and request.recurrence_frequency:
        bill.next_due_date = _calculate_next_due_date(request.due_date, request.recurrence_frequency)
    
    db.add(bill)
    db.commit()
    db.refresh(bill)
    
    # Phase 2.5: Emit event
    from otto.events import emit_event
    from otto.context import get_default_context
    otto_context = get_default_context(db)
    emit_event(
        db,
        household_id=otto_context.household_id,
        event_type="bill.created",
        source_model="Bill",
        source_id=bill.id,
        payload={"name": bill.name, "amount": bill.amount, "due_date": bill.due_date.isoformat()}
    )
    db.commit()
    
    return bill


def _calculate_next_due_date(current_due_date: datetime, frequency: str) -> datetime:
    """Calculate the next due date based on frequency"""
    if frequency == "monthly":
        # Add approximately 1 month (30 days)
        return current_due_date + timedelta(days=30)
    elif frequency == "quarterly":
        return current_due_date + timedelta(days=90)
    elif frequency == "yearly":
        return current_due_date + timedelta(days=365)
    else:
        return current_due_date


@router.get("", response_model=List[BillResponse])
async def list_bills(
    paid: Optional[str] = Query(None, description="Filter by paid status: yes, no, partial"),
    category: Optional[str] = Query(None, description="Filter by category"),
    upcoming: Optional[bool] = Query(None, description="Show only upcoming bills (due in next 30 days)"),
    overdue: Optional[bool] = Query(None, description="Show only overdue bills"),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """List bills with optional filters"""
    query = db.query(Bill)
    
    if paid:
        query = query.filter(Bill.paid == paid)
    if category:
        query = query.filter(Bill.category == category)
    
    now = datetime.utcnow()
    if upcoming:
        future_date = now + timedelta(days=30)
        query = query.filter(Bill.due_date >= now, Bill.due_date <= future_date)
    if overdue:
        query = query.filter(Bill.due_date < now, Bill.paid == "no")
    
    bills = query.order_by(Bill.due_date.asc()).limit(limit).all()
    return bills


@router.get("/{bill_id}", response_model=BillResponse)
async def get_bill(bill_id: int, db: Session = Depends(get_db)):
    """Get details of a specific bill"""
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill


@router.patch("/{bill_id}", response_model=BillResponse)
async def update_bill(bill_id: int, request: UpdateBillRequest, db: Session = Depends(get_db)):
    """Update a bill"""
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    # Update fields
    if request.name is not None:
        bill.name = request.name
    if request.amount is not None:
        bill.amount = request.amount
    if request.due_date is not None:
        bill.due_date = request.due_date
    if request.paid is not None:
        bill.paid = request.paid
        # Set paid_at if marking as paid
        if request.paid == "yes" and bill.paid_at is None:
            bill.paid_at = datetime.utcnow()
        elif request.paid != "yes":
            bill.paid_at = None
    if request.category is not None:
        bill.category = request.category
    if request.payee is not None:
        bill.payee = request.payee
    if request.account_number is not None:
        bill.account_number = request.account_number
    if request.notes is not None:
        bill.notes = request.notes
    if request.is_recurring is not None:
        bill.is_recurring = request.is_recurring
    if request.recurrence_frequency is not None:
        bill.recurrence_frequency = request.recurrence_frequency
    if request.next_due_date is not None:
        bill.next_due_date = request.next_due_date
    
    # If marking as paid and it's recurring, create next bill
    if request.paid == "yes" and bill.is_recurring == "yes" and bill.next_due_date:
        # Create next occurrence
        next_bill = Bill(
            name=bill.name,
            amount=bill.amount,
            due_date=bill.next_due_date,
            category=bill.category,
            payee=bill.payee,
            account_number=bill.account_number,
            notes=bill.notes,
            is_recurring="yes",
            recurrence_frequency=bill.recurrence_frequency
        )
        if bill.recurrence_frequency:
            next_bill.next_due_date = _calculate_next_due_date(bill.next_due_date, bill.recurrence_frequency)
        db.add(next_bill)
    
    db.commit()
    db.refresh(bill)
    return bill


@router.delete("/{bill_id}")
async def delete_bill(bill_id: int, db: Session = Depends(get_db)):
    """Delete a bill"""
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    db.delete(bill)
    db.commit()
    return {"message": "Bill deleted"}


@router.get("/upcoming/summary", response_model=dict)
async def get_upcoming_summary(
    days: int = Query(30, ge=1, le=365, description="Number of days to look ahead"),
    db: Session = Depends(get_db)
):
    """Get summary of upcoming bills"""
    now = datetime.utcnow()
    future_date = now + timedelta(days=days)
    
    upcoming_bills = db.query(Bill).filter(
        Bill.due_date >= now,
        Bill.due_date <= future_date,
        Bill.paid == "no"
    ).order_by(Bill.due_date.asc()).all()
    
    total_amount = sum(float(bill.amount.replace("$", "").replace(",", "")) for bill in upcoming_bills if bill.amount)
    overdue_bills = db.query(Bill).filter(
        Bill.due_date < now,
        Bill.paid == "no"
    ).count()
    
    return {
        "upcoming_count": len(upcoming_bills),
        "total_amount": f"${total_amount:.2f}",
        "overdue_count": overdue_bills,
        "bills": [BillResponse.from_orm(bill).dict() for bill in upcoming_bills]
    }

