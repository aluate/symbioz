"""
Otto Context - Global household/user context for Otto operations
Phase 2.5 — CONTROL_OTTO_PHASE2_5_FOUNDATIONS.md
"""

from typing import Optional
from pydantic import BaseModel
from datetime import date
from sqlalchemy.orm import Session

from models import Household, UserProfile


class OttoContext(BaseModel):
    """Canonical context object used everywhere Otto runs"""
    
    household_id: int
    user_id: int
    timezone: str
    currency: str
    locale: str
    tax_year_start: date
    tax_filing_status: str
    
    class Config:
        frozen = True  # Immutable context


def get_default_context(db: Session) -> OttoContext:
    """
    Get or create default household/user context.
    
    For Phase 2.5, creates a single default household and user if they don't exist.
    In the future, this will load from request/auth context.
    """
    # Try to get first household
    household = db.query(Household).first()
    
    if not household:
        # Create default household
        household = Household(
            name="Default Household",
            timezone="America/Los_Angeles",
            currency="USD",
            locale="en-US",
            tax_filing_status="married_joint",
            tax_year_start=date(2025, 1, 1)
        )
        db.add(household)
        db.flush()  # Get ID without committing
    
    # Try to get first user
    user = db.query(UserProfile).filter(UserProfile.household_id == household.id).first()
    
    if not user:
        # Create default user
        user = UserProfile(
            household_id=household.id,
            name="Primary User",
            email=None,
            role="primary",
            is_active=True
        )
        db.add(user)
        db.flush()
        
        # Set as primary user
        household.primary_user_id = user.id
        db.flush()
    
    return OttoContext(
        household_id=household.id,
        user_id=user.id,
        timezone=household.timezone,
        currency=household.currency,
        locale=household.locale,
        tax_year_start=household.tax_year_start or date(2025, 1, 1),
        tax_filing_status=household.tax_filing_status or "married_joint"
    )


def load_context_from_household(db: Session, household_id: int, user_id: Optional[int] = None) -> OttoContext:
    """Load context from specific household and user"""
    household = db.query(Household).filter(Household.id == household_id).first()
    if not household:
        raise ValueError(f"Household {household_id} not found")
    
    if user_id:
        user = db.query(UserProfile).filter(
            UserProfile.id == user_id,
            UserProfile.household_id == household_id
        ).first()
        if not user:
            raise ValueError(f"User {user_id} not found in household {household_id}")
    else:
        # Use primary user
        user = db.query(UserProfile).filter(
            UserProfile.id == household.primary_user_id,
            UserProfile.household_id == household_id
        ).first()
        if not user:
            raise ValueError(f"Primary user not found for household {household_id}")
    
    return OttoContext(
        household_id=household.id,
        user_id=user.id,
        timezone=household.timezone,
        currency=household.currency,
        locale=household.locale,
        tax_year_start=household.tax_year_start or date(2025, 1, 1),
        tax_filing_status=household.tax_filing_status or "married_joint"
    )

