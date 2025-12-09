"""
Trim system module: Data models for trim takeoff and pricing.
"""

from pydantic import BaseModel
from typing import Optional


class TrimRoomInput(BaseModel):
    """Input model for a single room's trim requirements."""
    name: str
    notes: Optional[str] = None
    
    # Optional numeric hints (even if some aren't used yet)
    base_lf: Optional[float] = None
    case_openings: Optional[int] = None
    window_openings: Optional[int] = None
    crown_lf: Optional[float] = None
    shoe_lf: Optional[float] = None


class TrimJobInput(BaseModel):
    """Input model for a complete trim job."""
    job_name: str
    job_number: Optional[str] = None
    rooms: list[TrimRoomInput]
    spec_level: Optional[str] = None  # e.g. "economy", "standard", "premium"
    notes: Optional[str] = None


class TrimLineItem(BaseModel):
    """A single line item in a trim quote."""
    code: str  # internal code or rule key
    description: str
    quantity_lf: float
    unit_price: float
    extended_price: float


class TrimJobTotals(BaseModel):
    """Totals for a trim job quote."""
    subtotal: float
    tax: Optional[float] = None
    total: float


class TrimJobResult(BaseModel):
    """Complete result of a trim job quote."""
    job: TrimJobInput
    items: list[TrimLineItem]
    totals: TrimJobTotals
    
    def summary_lines(self) -> list[str]:
        """
        Returns human-readable summary lines.
        
        Returns:
            List of strings, e.g.:
            - "Job {job_number or ''} – {job_name}"
            - One line per room if per-room totals can be inferred (otherwise just total)
        """
        lines = []
        
        # First line: Job info
        job_id = self.job.job_number or ""
        if job_id:
            lines.append(f"Job {job_id} – {self.job.job_name}")
        else:
            lines.append(f"Job – {self.job.job_name}")
        
        # For now, just show total (per-room breakdown would require more complex logic)
        lines.append(f"Total: ${self.totals.total:,.2f}")
        
        return lines
