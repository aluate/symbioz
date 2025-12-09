# Trim API Summary

This document shows the final API signatures and examples for the trim system.

## Final Signatures

### `systems.trim.takeoff_engine.run_takeoff`

```python
def run_takeoff(job_input: TrimJobInput) -> dict:
    """
    High-level entry point for the trim takeoff.
    Calls the existing legacy functions to compute quantities / BF, etc.
    
    Args:
        job_input: TrimJobInput model
        
    Returns:
        dict with keys:
            - 'lf': dict of trim_type -> lineal feet (from calculate_trim)
            - 'bf': dict with BF calculations (from calculate_bf_with_waste)
                - 'bf_raw': dict of trim_type -> board feet
                - 'bf_with_waste': dict of trim_type -> board feet with waste
                - 'waste_factors': dict of trim_type -> waste factor
                - 'dimensions': dict of trim_type -> (width, thickness)
                - 'nominal_thickness': dict of trim_type -> nominal thickness
                - 'thickness_category': dict of trim_type -> thickness category
            - 'trim_style': str
            - 'finish_level': str
            - 'inputs': dict (original inputs passed to calculate_trim)
    """
```

### `systems.trim.pricing_engine.price_job`

```python
def price_job(
    job_input: TrimJobInput, 
    species: str = "Poplar", 
    lf_cost_per_ft: float = 0.0,
    bf_markup_pct: float = 30.0, 
    is_finishing: bool = False,
    finish_type: str = "Primed", 
    sales_tax_rate: float = 0.06
) -> TrimJobResult:
    """
    High-level API:
    - Runs the takeoff for the job_input.
    - Looks up rates (BF cost, finish rates, etc.) using the existing code.
    - Builds a TrimJobResult with line items and totals.
    
    Args:
        job_input: TrimJobInput model
        species: Wood species (default: "Poplar")
        lf_cost_per_ft: Cost per linear foot (default: 0.0)
        bf_markup_pct: BF markup percentage (default: 30.0)
        is_finishing: Whether finishing is required (default: False)
        finish_type: Finish type - "Stain", "Paint", "Primed" (default: "Primed")
        sales_tax_rate: Sales tax rate (default: 0.06 = 6%)
        
    Returns:
        TrimJobResult with line items and totals
    """
```

### CLI Command: `trim`

```python
@app.command()
def trim(
    job_name: str = typer.Option("Sample Job", help="Name of the job."),
    spec_level: str = typer.Option("standard", help="Spec level: economy / standard / premium."),
    job_number: Optional[str] = typer.Option(None, help="Job number (optional)."),
):
    """
    Run a quick trim quote using default/sample inputs.
    
    For now this just:
    - builds a very simple TrimJobInput with one sample room,
    - calls price_job(),
    - and prints a human-readable summary.
    """
```

## Example: `TrimJobResult.summary_lines()`

```python
from systems.trim.models import TrimJobInput, TrimRoomInput, TrimJobTotals, TrimJobResult

# Create a simple example
room = TrimRoomInput(name="Main Floor", base_lf=100.0)
job = TrimJobInput(job_name="Sample House", job_number="2024-001", rooms=[room])
totals = TrimJobTotals(subtotal=5000.00, tax=300.00, total=5300.00)
result = TrimJobResult(job=job, items=[], totals=totals)

# Call summary_lines()
summary = result.summary_lines()
print(summary)
```

**Output:**
```
['Job 2024-001 – Sample House', 'Total: $5,300.00']
```

Or without job number:
```python
job = TrimJobInput(job_name="Sample House", rooms=[room])
# ... create result ...
summary = result.summary_lines()
```

**Output:**
```
['Job – Sample House', 'Total: $5,300.00']
```

