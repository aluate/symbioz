# Tax Brain Module

Tax preparation and categorization module for Life OS.

## Features

- **Tax Profile Management** - Store filing status, dependents, state info
- **Transaction Categorization** - Auto-categorize transactions for tax purposes
- **Rule Engine** - Create rules to automatically categorize transactions
- **Year-End Summaries** - Generate tax summaries by year
- **Document Tracking** - Track tax documents (W-2s, 1099s, etc.)

## API Endpoints

### Profile
- `GET /tax/profile` - Get tax profile
- `POST /tax/profile` - Update tax profile

### Categories
- `GET /tax/categories` - List all tax categories
- `POST /tax/categories` - Create a category

### Rules
- `GET /tax/rules` - List tax rules
- `POST /tax/rules` - Create a rule

### Transactions
- `POST /tax/transactions` - Add and categorize a transaction
- `GET /tax/transactions` - List transactions (with optional filters)
- `POST /tax/transactions/categorize` - Categorize without saving

### Reports
- `GET /tax/summary/{year}` - Generate year-end summary
- `GET /tax/documents` - List tax documents

## Usage Example

```python
from tax.service import TaxBrain

# Create TaxBrain instance
brain = TaxBrain(user_id=1)

# Update profile
profile = TaxProfile(
    user_id=1,
    filing_status=FilingStatusEnum.MARRIED_FILING_JOINT,
    primary_state="ID",
    has_home_mortgage=True,
    has_business_income=True
)
brain.update_profile(profile)

# Add a transaction
transaction = Transaction(
    user_id=1,
    date=datetime.now(),
    amount=-150.00,
    vendor="HOME DEPOT",
    description="Tools for business",
    is_business=True
)
categorized = brain.add_transaction(transaction)

# Generate year summary
summary = brain.generate_year_summary(2025)
```

## Data Models

- **TaxProfile** - User's tax filing information
- **TaxCategory** - Categories for transactions (e.g., "Business: Tools")
- **TaxRule** - Rules for auto-categorization
- **Transaction** - Financial transactions with tax categorization
- **TaxYearSummary** - Year-end tax totals
- **TaxDocument** - Tax document tracking

## Integration

This module integrates with:
- **Life OS Backend** - Main API server
- **Life OS Frontend** - UI for tax management (to be built)
- **Otto** - Automation for transaction import and categorization

