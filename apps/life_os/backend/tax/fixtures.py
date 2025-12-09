"""
Default tax categories and rules
"""

from .models import TaxCategory, TaxRule
from .enums import TaxBucketEnum


def get_default_categories() -> list[TaxCategory]:
    """Get default tax categories"""
    return [
        TaxCategory(
            name="W-2 Wages",
            bucket=TaxBucketEnum.W2_WAGES,
            schedule_hint="Form 1040, Line 1",
            description="Wages from employment"
        ),
        TaxCategory(
            name="Business Income",
            bucket=TaxBucketEnum.BUSINESS_INCOME,
            schedule_hint="Schedule C, Line 7",
            description="Income from business/self-employment"
        ),
        TaxCategory(
            name="Business: Tools & Equipment",
            bucket=TaxBucketEnum.BUSINESS_EXPENSE,
            schedule_hint="Schedule C, Line 22",
            description="Business equipment purchases"
        ),
        TaxCategory(
            name="Business: Office Supplies",
            bucket=TaxBucketEnum.BUSINESS_EXPENSE,
            schedule_hint="Schedule C, Line 27",
            description="Office supplies and materials"
        ),
        TaxCategory(
            name="Mortgage Interest",
            bucket=TaxBucketEnum.MORTGAGE_INTEREST,
            schedule_hint="Schedule A, Line 8",
            description="Home mortgage interest"
        ),
        TaxCategory(
            name="Property Tax",
            bucket=TaxBucketEnum.PROPERTY_TAX,
            schedule_hint="Schedule A, Line 5",
            description="Real estate property taxes"
        ),
        TaxCategory(
            name="Charitable Donations",
            bucket=TaxBucketEnum.CHARITABLE,
            schedule_hint="Schedule A, Line 11",
            description="Charitable contributions"
        ),
        TaxCategory(
            name="Medical Expenses",
            bucket=TaxBucketEnum.MEDICAL,
            schedule_hint="Schedule A, Line 1",
            description="Medical and dental expenses"
        ),
        TaxCategory(
            name="HSA Contributions",
            bucket=TaxBucketEnum.HSA,
            schedule_hint="Form 8889",
            description="Health Savings Account contributions"
        ),
    ]


def get_default_rules() -> list[TaxRule]:
    """Get default tax rules (these would be user-specific in practice)"""
    # These are examples - in practice, rules would be created per user
    return []

