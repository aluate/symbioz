"""
Tax Brain data models
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from .enums import FilingStatusEnum, TaxBucketEnum, TaxDocumentTypeEnum


class TaxProfile(BaseModel):
    """Tax profile for a user"""
    id: Optional[int] = None
    user_id: int
    filing_status: FilingStatusEnum
    
    primary_state: str  # e.g. "ID", "MT"
    additional_states: Optional[List[str]] = None
    
    has_home_mortgage: bool = False
    has_property_tax: bool = False
    has_business_income: bool = False
    has_hsa: bool = False
    has_fsa: bool = False
    has_student_loans: bool = False
    has_529: bool = False
    has_charitable_giving: bool = False
    
    dependents: Optional[List[Dict[str, Any]]] = None
    # Example: [{"name": "Audrey", "dob": "2012-05-01", "relationship": "daughter"}]
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class TaxCategory(BaseModel):
    """Tax category for categorizing transactions"""
    id: Optional[int] = None
    name: str  # e.g., "Business: Tools & Equipment"
    bucket: TaxBucketEnum
    schedule_hint: Optional[str] = None  # e.g., "Schedule C, Line 22"
    description: Optional[str] = None
    is_active: bool = True


class TaxRule(BaseModel):
    """Rule for auto-categorizing transactions"""
    id: Optional[int] = None
    user_id: int
    
    # Simple string matching
    vendor_contains: Optional[str] = None  # e.g., "HOME DEPOT"
    description_contains: Optional[str] = None
    
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    
    default_tax_category_id: int
    
    applies_to_business: bool = False
    applies_to_personal: bool = True
    
    priority: int = 100  # lower = higher priority


class Transaction(BaseModel):
    """Financial transaction with tax categorization"""
    id: Optional[int] = None
    user_id: int
    
    date: datetime
    amount: float  # + for income, - for expense
    account: Optional[str] = None  # "Checking", "Visa 1234"
    vendor: Optional[str] = None
    description: Optional[str] = None
    source: Optional[str] = None  # "plaid", "csv", "manual"
    
    # Basic general category
    category: Optional[str] = None
    
    # Tax brain overlay
    tax_category_id: Optional[int] = None
    bucket: TaxBucketEnum = TaxBucketEnum.NONE
    schedule_hint: Optional[str] = None
    is_business: bool = False
    is_tax_relevant: bool = False


class TaxYearSummary(BaseModel):
    """Year-end tax summary"""
    id: Optional[int] = None
    user_id: int
    year: int
    
    # Totals (stored as JSON to keep schema flexible)
    bucket_totals: Dict[str, float] = Field(default_factory=dict)
    category_totals: Dict[str, float] = Field(default_factory=dict)
    
    generated_at: Optional[datetime] = None
    notes: Optional[str] = None


class TaxDocument(BaseModel):
    """Tax document tracking"""
    id: Optional[int] = None
    user_id: int
    year: int
    
    doc_type: TaxDocumentTypeEnum
    issuer_name: str  # "ACC", "Chase", "Mortgage Co."
    expected: bool = True
    received: bool = False
    received_at: Optional[datetime] = None
    
    storage_url: Optional[str] = None  # link to GDrive / S3
    raw_metadata: Optional[Dict[str, Any]] = None

