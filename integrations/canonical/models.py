"""
Canonical data models - single source of truth between PPak and INNERGY.

These models represent the intermediate format that sits between legacy (PPak)
and new (INNERGY) systems, enabling repeatable ETL pipelines.
"""

from pydantic import BaseModel, Field
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List


class CanonicalProject(BaseModel):
    """Canonical project model - single source of truth for project data."""
    
    # Core fields
    project_number: str = Field(..., description="Unique project identifier (canonical)")
    name: str = Field(..., description="Project name/title")
    customer_name: str = Field(..., description="Customer/client name")
    customer_email: Optional[str] = Field(None, description="Customer email")
    customer_phone: Optional[str] = Field(None, description="Customer phone")
    
    # Status and phase
    status: str = Field(..., description="Project status (canonical)")
    phase: str = Field(..., description="Current project phase")
    
    # Dates
    start_date: Optional[date] = Field(None, description="Project start date")
    target_completion_date: Optional[date] = Field(None, description="Target completion date")
    actual_completion_date: Optional[date] = Field(None, description="Actual completion date")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now, description="When record was created")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    
    # Identifiers (for mapping between systems)
    ppak_id: Optional[str] = Field(None, description="Original PPak project ID")
    ppak_job_number: Optional[str] = Field(None, description="PPak job number")
    innergy_id: Optional[str] = Field(None, description="INNERGY project ID (after import)")
    innergy_project_number: Optional[str] = Field(None, description="INNERGY project number")
    
    # Additional metadata
    notes: Optional[str] = Field(None, description="Project notes/description")
    address: Optional[str] = Field(None, description="Project address")
    estimated_value: Optional[Decimal] = Field(None, description="Estimated project value")
    tags: Optional[List[str]] = Field(None, description="Project tags/categories")
    
    class Config:
        """Pydantic config."""
        extra = "allow"  # Allow extra fields for future extensibility
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            Decimal: lambda v: str(v),
        }


class CanonicalMaterial(BaseModel):
    """Canonical material model - single source of truth for material data."""
    
    # Core fields
    sku: str = Field(..., description="Stock Keeping Unit (canonical)")
    description: str = Field(..., description="Material description")
    category: str = Field(..., description="Material category")
    subcategory: Optional[str] = Field(None, description="Subcategory")
    
    # Units and pricing
    unit_of_measure: str = Field(..., description="UOM (e.g., 'each', 'sqft', 'lf')")
    cost_per_unit: Optional[Decimal] = Field(None, description="Cost per unit")
    
    # Vendor information
    vendor: Optional[str] = Field(None, description="Primary vendor/supplier")
    vendor_part_number: Optional[str] = Field(None, description="Vendor's part number")
    
    # Status
    is_active: bool = Field(True, description="Whether material is active")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now, description="When record was created")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    
    # Identifiers (for mapping between systems)
    ppak_sku: Optional[str] = Field(None, description="Original PPak SKU")
    ppak_id: Optional[str] = Field(None, description="PPak material ID")
    innergy_id: Optional[str] = Field(None, description="INNERGY material ID (after sync)")
    innergy_sku: Optional[str] = Field(None, description="INNERGY SKU")
    
    # Additional metadata
    notes: Optional[str] = Field(None, description="Material notes")
    lead_time_days: Optional[int] = Field(None, description="Typical lead time in days")
    minimum_order_quantity: Optional[int] = Field(None, description="Minimum order quantity")
    tags: Optional[List[str]] = Field(None, description="Material tags")
    
    class Config:
        """Pydantic config."""
        extra = "allow"  # Allow extra fields for future extensibility
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            Decimal: lambda v: str(v),
        }

