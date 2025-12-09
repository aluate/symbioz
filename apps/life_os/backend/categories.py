"""
Categories API - Manage tax/expense categories
Phase 2.5 — CONTROL_OTTO_PHASE2_5_FOUNDATIONS.md
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from database import get_db
from models import Category, CategoryVersion
from otto.context import get_default_context

router = APIRouter(prefix="/categories", tags=["categories"])


class CategoryCreate(BaseModel):
    code: str
    label: str
    type: str  # "income", "expense", "transfer", "other"
    tax_line: Optional[str] = None


class CategoryResponse(BaseModel):
    id: int
    household_id: Optional[int]
    code: str
    label: str
    type: str
    tax_line: Optional[str]
    is_active: bool
    
    class Config:
        from_attributes = True


@router.get("", response_model=List[CategoryResponse])
def list_categories(
    household_id: Optional[int] = None,
    type: Optional[str] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List categories, optionally filtered by household and type"""
    query = db.query(Category).filter(Category.is_active == True)
    
    if household_id:
        query = query.filter(Category.household_id == household_id)
    elif household_id is None:
        # If no household_id specified, include global categories (household_id is NULL)
        query = query.filter((Category.household_id == None) | (Category.household_id == household_id))
    
    if type:
        query = query.filter(Category.type == type)
    
    categories = query.limit(limit).all()
    return categories


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Get a single category by ID"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail=f"Category {category_id} not found")
    return category


@router.post("", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Create a new category"""
    # Get default context for household_id
    otto_context = get_default_context(db)
    
    # Check if code already exists for this household
    existing = db.query(Category).filter(
        Category.code == category.code,
        Category.household_id == otto_context.household_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Category with code '{category.code}' already exists"
        )
    
    new_category = Category(
        household_id=otto_context.household_id,
        code=category.code,
        label=category.label,
        type=category.type,
        tax_line=category.tax_line,
        is_active=True
    )
    
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    # Create initial version
    version = CategoryVersion(
        category_id=new_category.id,
        version=1,
        effective_from=datetime.now().date(),
        notes="Initial version"
    )
    db.add(version)
    db.commit()
    
    return new_category


@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    updates: dict,
    db: Session = Depends(get_db)
):
    """Update a category"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail=f"Category {category_id} not found")
    
    # Update allowed fields
    if "label" in updates:
        category.label = updates["label"]
    if "tax_line" in updates:
        category.tax_line = updates["tax_line"]
    if "is_active" in updates:
        category.is_active = updates["is_active"]
    
    category.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(category)
    
    return category

