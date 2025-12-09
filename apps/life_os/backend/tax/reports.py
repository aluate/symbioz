"""
Tax year-end report generation
"""

from collections import defaultdict
from datetime import datetime
from typing import List
from .models import Transaction, TaxYearSummary
from .enums import TaxBucketEnum


def generate_tax_year_summary(
    transactions: List[Transaction],
    user_id: int,
    year: int
) -> TaxYearSummary:
    """
    Generate a tax year summary from transactions.
    """
    start = datetime(year, 1, 1)
    end = datetime(year + 1, 1, 1)
    
    # Filter transactions for the year and tax-relevant
    relevant_txs = [
        tx for tx in transactions
        if start <= tx.date < end and tx.is_tax_relevant
    ]
    
    bucket_totals = defaultdict(float)
    category_totals = defaultdict(float)
    
    for tx in relevant_txs:
        # Add to bucket totals
        key_bucket = tx.bucket.value if isinstance(tx.bucket, TaxBucketEnum) else str(tx.bucket)
        bucket_totals[key_bucket] += tx.amount
        
        # Add to category totals (if we have category info)
        if tx.tax_category_id:
            # We'd need to look up category name, but for now use ID
            key_cat = f"category_{tx.tax_category_id}"
        else:
            key_cat = "Uncategorized"
        category_totals[key_cat] += tx.amount
    
    summary = TaxYearSummary(
        user_id=user_id,
        year=year,
        bucket_totals=dict(bucket_totals),
        category_totals=dict(category_totals),
        generated_at=datetime.now()
    )
    
    return summary

