"""Main calculator class that orchestrates all calculations."""

import sys
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List
import pandas as pd
from .model import (
    PoleBarnInputs,
    GeometryModel,
    MaterialTakeoff,
    PricedLineItem,
    PricingSummary,
    PartQuantity,
)
from . import geometry
from . import assemblies
from . import pricing
from . import bom


def _get_default_config_dir() -> Path:
    """
    Get default config directory, handling both script and bundled exe modes.
    
    Returns:
        Path to config directory
    """
    if getattr(sys, 'frozen', False):
        # Running as bundled exe - config is next to exe
        return Path(sys.executable).parent / "config"
    else:
        # Running as script - config is in project root
        return Path(__file__).parent.parent.parent / "config"


class PoleBarnCalculator:
    """Main calculator for pole barn construction."""
    
    def __init__(
        self,
        inputs: Optional[PoleBarnInputs] = None,
        config_dir: Optional[Path] = None,
    ):
        """
        Initialize calculator with inputs and config directory.
        
        Args:
            inputs: Complete pole barn inputs (optional, can be set later)
            config_dir: Directory containing CSV config files. If None, uses default.
        """
        self.inputs = inputs
        self.config_dir = config_dir or _get_default_config_dir()
        
        # DataFrames for config data (loaded lazily)
        self.parts_df: Optional[pd.DataFrame] = None
        self.pricing_df: Optional[pd.DataFrame] = None
        self.assemblies_df: Optional[pd.DataFrame] = None
        self._config_loaded = False
    
    def load_config(self) -> None:
        """
        Load configuration data from CSV files.
        
        Raises:
            FileNotFoundError: If config files are not found
            ValueError: If config files are malformed
        """
        # Try parts.example.csv first, fall back to parts.csv
        parts_path = self.config_dir / "parts.example.csv"
        if not parts_path.exists():
            parts_path = self.config_dir / "parts.csv"
        
        pricing_path = self.config_dir / "pricing.example.csv"
        if not pricing_path.exists():
            pricing_path = self.config_dir / "pricing.csv"
        
        assemblies_path = self.config_dir / "assemblies.example.csv"
        if not assemblies_path.exists():
            assemblies_path = self.config_dir / "assemblies.csv"
        
        self.parts_df = pricing.load_parts(parts_path)
        self.pricing_df = pricing.load_pricing(pricing_path)
        self.assemblies_df = pricing.load_assemblies(assemblies_path)
        self._config_loaded = True
    
    def calculate(
        self,
        inputs: Optional[PoleBarnInputs] = None,
    ) -> Tuple[GeometryModel, MaterialTakeoff, List[PricedLineItem], PricingSummary, List[PartQuantity]]:
        """
        Run complete calculation pipeline: geometry → quantities → pricing → BOM.
        
        Args:
            inputs: Pole barn inputs. If None, uses self.inputs.
            
        Returns:
            Tuple of (GeometryModel, MaterialTakeoff, list of PricedLineItem, PricingSummary, list of PartQuantity)
            
        Raises:
            ValueError: If inputs are not provided and self.inputs is None
            RuntimeError: If config is not loaded
        """
        if inputs is None:
            inputs = self.inputs
        
        if inputs is None:
            raise ValueError("PoleBarnInputs must be provided either in __init__ or calculate()")
        
        if not self._config_loaded:
            self.load_config()
        
        if self.parts_df is None or self.pricing_df is None or self.assemblies_df is None:
            raise RuntimeError("Configuration data not loaded. Call load_config() first.")
        
        # 1. Build geometry
        geom_model = geometry.build_geometry_model(inputs.geometry)
        
        # 2. Calculate quantities
        # Pass geometry_inputs for door/window counts (per changelog entry [14])
        quantities = assemblies.calculate_material_quantities(
            geom_model,
            inputs.materials,
            inputs.assemblies,
            geometry_inputs=inputs.geometry,  # For door/window assemblies
        )
        takeoff = MaterialTakeoff(items=quantities)
        
        # 3. Price the takeoff
        priced_items, summary = pricing.price_material_takeoff(
            takeoff,
            inputs.pricing,
            self.parts_df,
            self.pricing_df,
            self.assemblies_df,
        )
        
        # 4. Generate BOM (expand assemblies to parts)
        bom_items = bom.expand_to_parts(
            takeoff,
            self.assemblies_df,
            self.parts_df,
            self.pricing_df,
            geometry_model=geom_model,
            geometry_inputs=inputs.geometry,
        )
        
        # 5. Override material_takeoff to match BOM (PHASE 2 fix)
        # This ensures material_takeoff uses packed quantities (sticks, sheets, stock lengths)
        # instead of raw inches/sqft
        takeoff = bom.create_material_takeoff_from_bom(bom_items)
        
        return geom_model, takeoff, priced_items, summary, bom_items
    
    def calculate_geometry(self) -> Dict[str, Any]:
        """
        Calculate all geometry-related values.
        
        Returns:
            Dictionary with geometry calculations
        """
        if self.inputs is None:
            raise ValueError("PoleBarnInputs must be set")
        
        geom_model = geometry.build_geometry_model(self.inputs.geometry)
        geom_summary = geometry.get_geometry_summary(self.inputs.geometry)
        
        return {
            "model": geom_model,
            "summary": geom_summary,
        }
    
    def calculate_quantities(self) -> Dict[str, Any]:
        """
        Calculate all material quantities.
        
        Returns:
            Dictionary with quantity calculations
        """
        if self.inputs is None:
            raise ValueError("PoleBarnInputs must be set")
        
        geom_model = geometry.build_geometry_model(self.inputs.geometry)
        quantities = assemblies.calculate_material_quantities(
            geom_model,
            self.inputs.materials,
            self.inputs.assemblies,
        )
        takeoff = MaterialTakeoff(items=quantities)
        
        return {
            "takeoff": takeoff,
            "summary": assemblies.get_assembly_summary(self.inputs),
        }
    
    def calculate_costs(self) -> Dict[str, Any]:
        """
        Calculate all costs.
        
        Returns:
            Dictionary with cost calculations
        """
        if self.inputs is None:
            raise ValueError("PoleBarnInputs must be set")
        
        if not self._config_loaded:
            self.load_config()
        
        if self.parts_df is None or self.pricing_df is None or self.assemblies_df is None:
            raise RuntimeError("Configuration data not loaded. Call load_config() first.")
        
        # Get quantities first
        geom_model = geometry.build_geometry_model(self.inputs.geometry)
        quantities = assemblies.calculate_material_quantities(
            geom_model,
            self.inputs.materials,
            self.inputs.assemblies,
        )
        takeoff = MaterialTakeoff(items=quantities)
        
        # Price them
        priced_items, summary = pricing.price_material_takeoff(
            takeoff,
            self.inputs.pricing,
            self.parts_df,
            self.pricing_df,
            self.assemblies_df,
        )
        
        return {
            "priced_items": priced_items,
            "summary": summary,
        }
    
    def calculate_all(self) -> Dict[str, Any]:
        """
        Run all calculations and return complete results.
        
        Returns:
            Dictionary with all calculations including geometry, quantities, and costs
        """
        geom_model, takeoff, priced_items, summary = self.calculate()
        
        return {
            "geometry": {
                "model": geom_model,
                "summary": geometry.get_geometry_summary(self.inputs.geometry),
            },
            "quantities": {
                "takeoff": takeoff,
                "summary": assemblies.get_assembly_summary(self.inputs),
            },
            "pricing": {
                "priced_items": priced_items,
                "summary": summary,
            },
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a human-readable summary of all calculations.
        
        Returns:
            Dictionary with formatted summary information
        """
        geom_model, takeoff, priced_items, summary = self.calculate()
        
        # Organize priced items by category
        by_category: Dict[str, List[PricedLineItem]] = {}
        for item in priced_items:
            if item.category not in by_category:
                by_category[item.category] = []
            by_category[item.category].append(item)
        
        return {
            "project_name": self.inputs.project_name if self.inputs else None,
            "geometry": {
                "dimensions": {
                    "length_ft": geom_model.overall_length_ft,
                    "width_ft": geom_model.overall_width_ft,
                    "eave_height_ft": geom_model.eave_height_ft,
                },
                "areas": {
                    "footprint_sqft": geom_model.footprint_area_sqft,
                    "roof_sqft": geom_model.roof_area_sqft,
                    "wall_sqft": geom_model.total_wall_area_sqft,
                },
            },
            "quantities": {
                "total_items": len(takeoff.items),
                "by_category": {
                    cat: len(items) for cat, items in by_category.items()
                },
            },
            "costs": {
                "material_subtotal": summary.material_subtotal,
                "labor_subtotal": summary.labor_subtotal,
                "markup_total": summary.markup_total,
                "tax_total": summary.tax_total,
                "grand_total": summary.grand_total,
            },
            "priced_items_by_category": {
                cat: [
                    {
                        "name": item.name,
                        "description": item.description,
                        "quantity": item.quantity,
                        "unit": item.unit,
                        "unit_price": item.unit_price,
                        "total_cost": item.total_cost,
                    }
                    for item in items
                ]
                for cat, items in by_category.items()
            },
        }
