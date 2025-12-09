"""
Trim system module: Pricing engine - use Finish Rates & material prices for pricing.
"""

from .models import TrimJobInput, TrimJobResult, TrimLineItem, TrimJobTotals
from .takeoff_engine import run_takeoff
from .exporters import (
    calculate_pricing,
    format_description,
    get_setup_cost,
    load_bf_cost
)


def price_job(job_input: TrimJobInput, species: str = "Poplar", lf_cost_per_ft: float = 0.0,
              bf_markup_pct: float = 30.0, is_finishing: bool = False,
              finish_type: str = "Primed", sales_tax_rate: float = 0.06) -> TrimJobResult:
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
    # Run takeoff
    takeoff_result = run_takeoff(job_input)
    
    lf_results = takeoff_result['lf']
    bf_data = takeoff_result['bf']
    finish_level = takeoff_result['finish_level']
    
    # Calculate pricing using legacy function
    pricing_dict = calculate_pricing(
        lf_results,
        bf_data,
        species,
        lf_cost_per_ft,
        bf_markup_pct,
        is_finishing,
        finish_type
    )
    
    # Build line items from pricing dict
    line_items = []
    trim_type_order = ['base', 'casing', 'headers', 'sills', 'apron', 'jambs', 'dentils']
    
    for trim_type in trim_type_order:
        if trim_type in pricing_dict:
            p = pricing_dict[trim_type]
            if p['linear_ft'] > 0:
                # Format description
                description = format_description(
                    species,
                    trim_type,
                    p['width'],
                    p['thickness'],
                    finish_level,
                    is_finishing,
                    finish_type,
                    p['linear_ft'],
                    p['bf_required']
                )
                
                # Create line item
                line_item = TrimLineItem(
                    code=trim_type,
                    description=description,
                    quantity_lf=round(p['linear_ft'], 2),
                    unit_price=round(p['price_per_lf'], 2),
                    extended_price=round(p['line_total'], 2)
                )
                line_items.append(line_item)
    
    # Calculate totals
    subtotal = sum(item.extended_price for item in line_items)
    tax = subtotal * sales_tax_rate
    total = subtotal + tax
    
    totals = TrimJobTotals(
        subtotal=round(subtotal, 2),
        tax=round(tax, 2),
        total=round(total, 2)
    )
    
    # Build result
    result = TrimJobResult(
        job=job_input,
        items=line_items,
        totals=totals
    )
    
    return result
