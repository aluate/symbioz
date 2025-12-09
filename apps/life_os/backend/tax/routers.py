"""
Tax Brain API routes
"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime

from .models import (
    TaxProfile,
    TaxCategory,
    TaxRule,
    Transaction,
    TaxYearSummary,
    TaxDocument,
)
from .service import TaxBrain
from .fixtures import get_default_categories

router = APIRouter(prefix="/tax", tags=["tax"])

# In-memory storage for demo (would be database in production)
_tax_brain_instances: dict[int, TaxBrain] = {}


def get_tax_brain(user_id: int) -> TaxBrain:
    """Get or create TaxBrain instance for user"""
    if user_id not in _tax_brain_instances:
        brain = TaxBrain(user_id)
        # Initialize with default categories
        for category in get_default_categories():
            brain.add_category(category)
        _tax_brain_instances[user_id] = brain
    return _tax_brain_instances[user_id]


@router.get("/profile")
async def get_profile(user_id: int = 1):
    """Get tax profile"""
    brain = get_tax_brain(user_id)
    profile = brain.get_profile()
    if not profile:
        raise HTTPException(status_code=404, detail="Tax profile not found")
    return profile


@router.post("/profile")
async def update_profile(profile: TaxProfile, user_id: int = 1):
    """Update tax profile"""
    brain = get_tax_brain(user_id)
    return brain.update_profile(profile)


@router.get("/categories")
async def list_categories(user_id: int = 1):
    """List all tax categories"""
    brain = get_tax_brain(user_id)
    return brain.get_categories()


@router.post("/categories")
async def create_category(category: TaxCategory, user_id: int = 1):
    """Create a tax category"""
    brain = get_tax_brain(user_id)
    return brain.add_category(category)


@router.get("/rules")
async def list_rules(user_id: int = 1):
    """List tax rules for user"""
    brain = get_tax_brain(user_id)
    return brain.get_rules()


@router.post("/rules")
async def create_rule(rule: TaxRule, user_id: int = 1):
    """Create a tax rule"""
    brain = get_tax_brain(user_id)
    return brain.add_rule(rule)


@router.post("/transactions")
async def add_transaction(transaction: Transaction, user_id: int = 1):
    """Add and categorize a transaction"""
    brain = get_tax_brain(user_id)
    return brain.add_transaction(transaction)


@router.get("/transactions")
async def list_transactions(
    user_id: int = 1,
    year: Optional[int] = None,
    tax_relevant_only: bool = False
):
    """List transactions"""
    brain = get_tax_brain(user_id)
    return brain.get_transactions(year=year, tax_relevant_only=tax_relevant_only)


@router.post("/transactions/categorize")
async def categorize_transaction(transaction: Transaction, user_id: int = 1):
    """Categorize a transaction without saving"""
    brain = get_tax_brain(user_id)
    return brain.categorize_transaction(transaction)


@router.get("/summary/{year}")
async def get_year_summary(year: int, user_id: int = 1):
    """Generate tax year summary"""
    brain = get_tax_brain(user_id)
    return brain.generate_year_summary(year)


@router.get("/documents")
async def list_documents(user_id: int = 1, year: Optional[int] = None):
    """List tax documents"""
    brain = get_tax_brain(user_id)
    return brain.get_documents(year=year)

