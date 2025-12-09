"""
Transactions API - Track and categorize transactions
Phase 3 — CONTROL_OTTO_PHASE3.md
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from database import get_db
from models import Transaction

router = APIRouter(prefix="/transactions", tags=["transactions"])


class CreateTransactionRequest(BaseModel):
    """Request to create a new transaction"""
    date: datetime
    amount: str
    vendor: Optional[str] = None
    description: Optional[str] = None
    tax_category: Optional[str] = None
    source: Optional[str] = "manual"
    source_id: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None


class UpdateTransactionRequest(BaseModel):
    """Request to update a transaction"""
    date: Optional[datetime] = None
    amount: Optional[str] = None
    vendor: Optional[str] = None
    description: Optional[str] = None
    tax_category: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None


class TransactionResponse(BaseModel):
    """Response model for transaction"""
    id: int
    created_at: datetime
    updated_at: datetime
    date: datetime
    amount: str
    vendor: Optional[str]
    description: Optional[str]
    tax_category: Optional[str]
    source: str
    source_id: Optional[str]
    notes: Optional[str]
    tags: Optional[List[str]]

    class Config:
        from_attributes = True


@router.post("", response_model=TransactionResponse)
async def create_transaction(request: CreateTransactionRequest, db: Session = Depends(get_db)):
    """Create a new transaction"""
    transaction = Transaction(
        date=request.date,
        amount=request.amount,
        vendor=request.vendor,
        description=request.description,
        tax_category=request.tax_category,
        source=request.source or "manual",
        source_id=request.source_id,
        notes=request.notes,
        tags=request.tags
    )
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    
    # Phase 2.5: Emit event
    from otto.events import emit_event
    from otto.context import get_default_context
    otto_context = get_default_context(db)
    emit_event(
        db,
        household_id=otto_context.household_id,
        event_type="transaction.created",
        source_model="Transaction",
        source_id=transaction.id,
        payload={"vendor": transaction.vendor, "amount": transaction.amount}
    )
    db.commit()
    
    return transaction


@router.get("", response_model=List[TransactionResponse])
async def list_transactions(
    start_date: Optional[datetime] = Query(None, description="Filter from this date"),
    end_date: Optional[datetime] = Query(None, description="Filter until this date"),
    tax_category: Optional[str] = Query(None, description="Filter by tax category"),
    vendor: Optional[str] = Query(None, description="Filter by vendor"),
    source: Optional[str] = Query(None, description="Filter by source"),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """List transactions with optional filters"""
    query = db.query(Transaction)
    
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    if tax_category:
        query = query.filter(Transaction.tax_category == tax_category)
    if vendor:
        query = query.filter(Transaction.vendor == vendor)
    if source:
        query = query.filter(Transaction.source == source)
    
    transactions = query.order_by(Transaction.date.desc()).limit(limit).all()
    return transactions


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Get details of a specific transaction"""
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.patch("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(transaction_id: int, request: UpdateTransactionRequest, db: Session = Depends(get_db)):
    """Update a transaction"""
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # Update fields
    if request.date is not None:
        transaction.date = request.date
    if request.amount is not None:
        transaction.amount = request.amount
    if request.vendor is not None:
        transaction.vendor = request.vendor
    if request.description is not None:
        transaction.description = request.description
    if request.tax_category is not None:
        transaction.tax_category = request.tax_category
    if request.notes is not None:
        transaction.notes = request.notes
    if request.tags is not None:
        transaction.tags = request.tags
    
    db.commit()
    db.refresh(transaction)
    return transaction


@router.delete("/{transaction_id}")
async def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Delete a transaction"""
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.delete(transaction)
    db.commit()
    return {"message": "Transaction deleted"}


@router.get("/summary/by_category", response_model=dict)
async def get_summary_by_category(
    start_date: Optional[datetime] = Query(None, description="Filter from this date"),
    end_date: Optional[datetime] = Query(None, description="Filter until this date"),
    db: Session = Depends(get_db)
):
    """Get transaction summary by tax category"""
    query = db.query(Transaction)
    
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    
    transactions = query.all()
    
    by_category = {}
    total = 0
    
    for txn in transactions:
        cat = txn.tax_category or "uncategorized"
        amount_str = txn.amount or "0"
        try:
            amount = float(amount_str.replace("$", "").replace(",", ""))
            total += amount
            by_category[cat] = by_category.get(cat, 0) + amount
        except:
            pass
    
    return {
        "total": f"${total:.2f}",
        "count": len(transactions),
        "by_category": {k: f"${v:.2f}" for k, v in by_category.items()}
    }

