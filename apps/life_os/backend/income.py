"""
Income API - Track income sources
Phase 3 — CONTROL_OTTO_PHASE3.md
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from database import get_db
from models import Income

router = APIRouter(prefix="/income", tags=["income"])


class CreateIncomeRequest(BaseModel):
    """Request to create a new income entry"""
    source: str
    amount: str
    received_date: datetime
    category: Optional[str] = None
    notes: Optional[str] = None
    is_recurring: Optional[str] = "no"  # yes, no
    recurrence_frequency: Optional[str] = None  # monthly, quarterly, yearly


class UpdateIncomeRequest(BaseModel):
    """Request to update an income entry"""
    source: Optional[str] = None
    amount: Optional[str] = None
    received_date: Optional[datetime] = None
    category: Optional[str] = None
    notes: Optional[str] = None
    is_recurring: Optional[str] = None
    recurrence_frequency: Optional[str] = None
    next_expected_date: Optional[datetime] = None


class IncomeResponse(BaseModel):
    """Response model for income"""
    id: int
    created_at: datetime
    updated_at: datetime
    source: str
    amount: str
    received_date: datetime
    category: Optional[str]
    notes: Optional[str]
    is_recurring: str
    recurrence_frequency: Optional[str]
    next_expected_date: Optional[datetime]

    class Config:
        from_attributes = True


@router.post("", response_model=IncomeResponse)
async def create_income(request: CreateIncomeRequest, db: Session = Depends(get_db)):
    """Create a new income entry"""
    income = Income(
        source=request.source,
        amount=request.amount,
        received_date=request.received_date,
        category=request.category,
        notes=request.notes,
        is_recurring=request.is_recurring or "no",
        recurrence_frequency=request.recurrence_frequency
    )
    
    # Calculate next_expected_date for recurring income
    if request.is_recurring == "yes" and request.recurrence_frequency:
        income.next_expected_date = _calculate_next_date(request.received_date, request.recurrence_frequency)
    
    db.add(income)
    db.commit()
    db.refresh(income)
    
    # Phase 2.5: Emit event
    from otto.events import emit_event
    from otto.context import get_default_context
    otto_context = get_default_context(db)
    emit_event(
        db,
        household_id=otto_context.household_id,
        event_type="income.created",
        source_model="Income",
        source_id=income.id,
        payload={"source": income.source, "amount": income.amount}
    )
    db.commit()
    
    return income


def _calculate_next_date(current_date: datetime, frequency: str) -> datetime:
    """Calculate the next expected date based on frequency"""
    if frequency == "monthly":
        return current_date + timedelta(days=30)
    elif frequency == "quarterly":
        return current_date + timedelta(days=90)
    elif frequency == "yearly":
        return current_date + timedelta(days=365)
    else:
        return current_date


@router.get("", response_model=List[IncomeResponse])
async def list_income(
    category: Optional[str] = Query(None, description="Filter by category"),
    source: Optional[str] = Query(None, description="Filter by source"),
    start_date: Optional[datetime] = Query(None, description="Filter from this date"),
    end_date: Optional[datetime] = Query(None, description="Filter until this date"),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """List income entries with optional filters"""
    query = db.query(Income)
    
    if category:
        query = query.filter(Income.category == category)
    if source:
        query = query.filter(Income.source == source)
    if start_date:
        query = query.filter(Income.received_date >= start_date)
    if end_date:
        query = query.filter(Income.received_date <= end_date)
    
    income_list = query.order_by(Income.received_date.desc()).limit(limit).all()
    return income_list


@router.get("/{income_id}", response_model=IncomeResponse)
async def get_income(income_id: int, db: Session = Depends(get_db)):
    """Get details of a specific income entry"""
    income = db.query(Income).filter(Income.id == income_id).first()
    if not income:
        raise HTTPException(status_code=404, detail="Income not found")
    return income


@router.patch("/{income_id}", response_model=IncomeResponse)
async def update_income(income_id: int, request: UpdateIncomeRequest, db: Session = Depends(get_db)):
    """Update an income entry"""
    income = db.query(Income).filter(Income.id == income_id).first()
    if not income:
        raise HTTPException(status_code=404, detail="Income not found")
    
    # Update fields
    if request.source is not None:
        income.source = request.source
    if request.amount is not None:
        income.amount = request.amount
    if request.received_date is not None:
        income.received_date = request.received_date
    if request.category is not None:
        income.category = request.category
    if request.notes is not None:
        income.notes = request.notes
    if request.is_recurring is not None:
        income.is_recurring = request.is_recurring
    if request.recurrence_frequency is not None:
        income.recurrence_frequency = request.recurrence_frequency
    if request.next_expected_date is not None:
        income.next_expected_date = request.next_expected_date
    
    db.commit()
    db.refresh(income)
    return income


@router.delete("/{income_id}")
async def delete_income(income_id: int, db: Session = Depends(get_db)):
    """Delete an income entry"""
    income = db.query(Income).filter(Income.id == income_id).first()
    if not income:
        raise HTTPException(status_code=404, detail="Income not found")
    
    db.delete(income)
    db.commit()
    return {"message": "Income deleted"}


@router.get("/summary/by_period", response_model=dict)
async def get_income_by_period(
    period: str = Query("monthly", description="Period: monthly, quarterly, yearly"),
    year: Optional[int] = Query(None, description="Year (defaults to current year)"),
    db: Session = Depends(get_db)
):
    """Get income summary by period"""
    now = datetime.utcnow()
    if not year:
        year = now.year
    
    # Calculate date range based on period
    if period == "monthly":
        start_date = datetime(year, now.month, 1)
        if now.month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, now.month + 1, 1)
    elif period == "quarterly":
        quarter = (now.month - 1) // 3 + 1
        start_month = (quarter - 1) * 3 + 1
        start_date = datetime(year, start_month, 1)
        if quarter == 4:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, start_month + 3, 1)
    elif period == "yearly":
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1)
    else:
        raise HTTPException(status_code=400, detail="Invalid period. Use: monthly, quarterly, yearly")
    
    income_list = db.query(Income).filter(
        Income.received_date >= start_date,
        Income.received_date < end_date
    ).all()
    
    total_amount = sum(float(inc.amount.replace("$", "").replace(",", "")) for inc in income_list if inc.amount)
    
    by_category = {}
    for inc in income_list:
        cat = inc.category or "uncategorized"
        amount = float(inc.amount.replace("$", "").replace(",", "")) if inc.amount else 0
        by_category[cat] = by_category.get(cat, 0) + amount
    
    return {
        "period": period,
        "year": year,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "total_amount": f"${total_amount:.2f}",
        "count": len(income_list),
        "by_category": {k: f"${v:.2f}" for k, v in by_category.items()}
    }

