"""
PPak export schemas - represents expected structure of PPak CSV exports.

TODO: Update these models once we analyze actual PPak export files.
These are reasonable assumptions based on typical project/material data.
"""

from pydantic import BaseModel, Field
from datetime import date, datetime
from decimal import Decimal
from typing import Optional


class PPakProjectRow(BaseModel):
    """
    Represents a single row from a PPak projects export CSV.
    
    TODO: Update field names to match actual PPak export columns.
    Add/remove fields based on actual PPak structure.
    """
    
    # TODO: Replace with actual PPak column names
    project_id: Optional[str] = Field(None, description="PPak project ID")
    job_number: Optional[str] = Field(None, description="PPak job number")
    project_name: Optional[str] = Field(None, description="Project name")
    customer: Optional[str] = Field(None, description="Customer name")
    customer_email: Optional[str] = Field(None, description="Customer email")
    customer_phone: Optional[str] = Field(None, description="Customer phone")
    
    # Status and phase - TODO: Verify actual column names
    status: Optional[str] = Field(None, description="PPak status value")
    phase: Optional[str] = Field(None, description="PPak phase value")
    
    # Dates - TODO: Verify date format and column names
    start_date: Optional[str] = Field(None, description="Start date (as string from CSV)")
    completion_date: Optional[str] = Field(None, description="Completion date (as string from CSV)")
    
    # Additional fields - TODO: Add more as discovered
    notes: Optional[str] = Field(None, description="Project notes")
    address: Optional[str] = Field(None, description="Project address")
    estimated_value: Optional[str] = Field(None, description="Estimated value (as string from CSV)")
    
    class Config:
        """Pydantic config."""
        extra = "allow"  # Allow extra fields from CSV that we don't know about yet


class PPakMaterialRow(BaseModel):
    """
    Represents a single row from a PPak materials export CSV.
    
    TODO: Update field names to match actual PPak export columns.
    Add/remove fields based on actual PPak structure.
    """
    
    # TODO: Replace with actual PPak column names
    material_id: Optional[str] = Field(None, description="PPak material ID")
    sku: Optional[str] = Field(None, description="PPak SKU")
    description: Optional[str] = Field(None, description="Material description")
    category: Optional[str] = Field(None, description="Material category")
    
    # Units and pricing - TODO: Verify column names
    unit_of_measure: Optional[str] = Field(None, description="Unit of measure")
    cost: Optional[str] = Field(None, description="Cost (as string from CSV)")
    
    # Vendor - TODO: Verify column names
    vendor: Optional[str] = Field(None, description="Vendor name")
    vendor_part_number: Optional[str] = Field(None, description="Vendor part number")
    
    # Status - TODO: Verify how PPak indicates active/inactive
    is_active: Optional[str] = Field(None, description="Active status (as string from CSV)")
    
    # Additional fields - TODO: Add more as discovered
    notes: Optional[str] = Field(None, description="Material notes")
    
    class Config:
        """Pydantic config."""
        extra = "allow"  # Allow extra fields from CSV that we don't know about yet

