"""
CLI front end for residential automation tools.
"""

import typer
from typing import Optional
from systems.trim.models import TrimJobInput, TrimRoomInput
from systems.trim.pricing_engine import price_job

app = typer.Typer()


@app.command()
def hello():
    """Simple hello command."""
    typer.echo("Hello from Residential Automation CLI!")


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
    # Build a basic TrimJobInput with one TrimRoomInput
    room = TrimRoomInput(
        name="Main Floor",
        base_lf=100.0,
        window_openings=4,
        case_openings=6
    )
    
    job_input = TrimJobInput(
        job_name=job_name,
        job_number=job_number,
        rooms=[room],
        spec_level=spec_level
    )
    
    # Call price_job
    result = price_job(job_input)
    
    # Print header
    typer.echo("=" * 60)
    summary = result.summary_lines()
    for line in summary:
        typer.echo(line)
    typer.echo("=" * 60)
    
    # Print line items
    typer.echo("\nLine Items:")
    typer.echo("-" * 60)
    for item in result.items:
        typer.echo(
            f"{item.code:12} | {item.description[:35]:35} | "
            f"{item.quantity_lf:8.2f} LF | ${item.extended_price:10,.2f}"
        )
    
    # Print totals
    typer.echo("-" * 60)
    typer.echo(f"Subtotal: ${result.totals.subtotal:,.2f}")
    if result.totals.tax:
        typer.echo(f"Tax: ${result.totals.tax:,.2f}")
    typer.echo(f"TOTAL: ${result.totals.total:,.2f}")
    typer.echo("=" * 60)


if __name__ == "__main__":
    app()
