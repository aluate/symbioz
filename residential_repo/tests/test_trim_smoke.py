"""
Smoke test for trim system.
"""

from systems.trim.models import TrimJobInput, TrimRoomInput
from systems.trim.pricing_engine import price_job


def test_trim_smoke():
    """Basic smoke test to ensure imports and basic functionality work."""
    room = TrimRoomInput(name="Test Room", base_lf=100.0)
    job = TrimJobInput(job_name="Test Job", rooms=[room], spec_level="standard")
    result = price_job(job)
    assert result.totals.total >= 0
    assert len(result.items) >= 0
    assert result.job.job_name == "Test Job"

