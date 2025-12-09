# Pole Barn Calculator

A Python calculator for pole barn construction materials, quantities, and costs.

## Project Status

**Current Phase: First Pass - Structure and Data Models**

This is the initial structure of the project. All calculation functions are currently stubbed with `NotImplementedError`. The focus of this phase is:

- ✅ Project structure and organization
- ✅ Data model definitions (dataclasses)
- ✅ CLI interface for accepting inputs
- ✅ Function stubs for all calculations
- ✅ Control document listing all variables
- ⏳ **Next**: Implement actual calculation logic

## Project Structure

```
pole_barn_calc/
├── README.md
├── pyproject.toml
├── config/
│   ├── parts.example.csv
│   ├── pricing.example.csv
│   └── assemblies.example.csv
├── systems/
│   ├── __init__.py
│   └── pole_barn/
│       ├── __init__.py
│       ├── model.py          # Data models (dataclasses)
│       ├── geometry.py       # Geometry calculations (stubbed)
│       ├── assemblies.py     # Material quantity calculations (stubbed)
│       ├── pricing.py        # Cost calculations (stubbed)
│       └── calculator.py     # Main calculator class (stubbed)
├── apps/
│   ├── __init__.py
│   └── cli.py                # Command-line interface
├── control/
│   └── pole_barn_calculator.md  # Control document with all variables
└── tests/
    ├── test_geometry.py
    ├── test_assemblies.py
    └── test_end_to_end.py
```

## Installation

```bash
# Install in development mode
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"
```

## Usage

### Command Line Interface

The CLI accepts all input variables as command-line options. Example:

```bash
pole-barn-calc \
  --project-name "My Barn" \
  --length 40 \
  --width 30 \
  --eave-height 12 \
  --peak-height 16 \
  --roof-pitch 0.333 \
  --pole-spacing-length 8 \
  --pole-spacing-width 8 \
  --pole-diameter 6 \
  --pole-depth 4 \
  --roof-material metal \
  --roof-gauge 29 \
  --wall-material metal \
  --wall-gauge 29 \
  --truss-type standard \
  --truss-spacing 2 \
  --purlin-spacing 2 \
  --girt-spacing 2 \
  --foundation-type concrete_pad \
  --labor-rate 50 \
  --material-markup 1.15 \
  --tax-rate 0.08 \
  --assembly-method standard \
  --fastening-type screws
```

### Python API

```python
from systems.pole_barn import PoleBarnInputs, GeometryInputs, MaterialInputs, PricingInputs, AssemblyInputs
from systems.pole_barn import PoleBarnCalculator

# Create inputs
geometry = GeometryInputs(
    length=40.0,
    width=30.0,
    eave_height=12.0,
    peak_height=16.0,
    # ... other geometry inputs
)

materials = MaterialInputs(
    roof_material_type="metal",
    wall_material_type="metal",
    # ... other material inputs
)

pricing = PricingInputs(
    labor_rate=50.0,
    material_markup=1.15,
    tax_rate=0.08,
)

assemblies = AssemblyInputs(
    assembly_method="standard",
    fastening_type="screws",
)

inputs = PoleBarnInputs(
    geometry=geometry,
    materials=materials,
    pricing=pricing,
    assemblies=assemblies,
)

# Create calculator (calculations not yet implemented)
calculator = PoleBarnCalculator(inputs)
```

## Data Models

The project uses dataclasses to define input structures:

- `GeometryInputs` - Physical dimensions and layout
- `MaterialInputs` - Material specifications
- `PricingInputs` - Cost parameters
- `AssemblyInputs` - Construction method details
- `PoleBarnInputs` - Complete input set

See `control/pole_barn_calculator.md` for a complete list of all variables.

## Configuration Files

Example CSV files in `config/` demonstrate the structure for:
- **parts.example.csv** - Part catalog with IDs and descriptions
- **pricing.example.csv** - Pricing data for parts
- **assemblies.example.csv** - Assembly definitions

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black .
ruff check .
```

## Next Steps

See the summary section below for recommended next steps in development.

## License

MIT

