"""
Tax rule engine for auto-categorization
"""

from typing import List, Optional
from .models import TaxRule, Transaction, TaxCategory
from .enums import TaxBucketEnum


def apply_rules_to_transaction(
    tx: Transaction,
    rules: List[TaxRule],
    categories: List[TaxCategory]
) -> Transaction:
    """
    Apply tax rules to a transaction.
    Mutates tx in memory; caller is responsible for persisting.
    """
    matching_rule: Optional[TaxRule] = None
    
    # Sort rules by priority (lower = higher priority)
    sorted_rules = sorted(rules, key=lambda r: r.priority)
    
    for rule in sorted_rules:
        if not rule_matches_transaction(rule, tx):
            continue
        matching_rule = rule
        break
    
    if matching_rule:
        # Find the category
        category = next(
            (c for c in categories if c.id == matching_rule.default_tax_category_id),
            None
        )
        
        if category:
            tx.tax_category_id = category.id
            tx.bucket = category.bucket
            tx.schedule_hint = category.schedule_hint
            tx.is_tax_relevant = category.bucket != TaxBucketEnum.NONE
        else:
            tx.is_tax_relevant = False
            tx.bucket = TaxBucketEnum.NONE
    else:
        tx.is_tax_relevant = False
        tx.bucket = TaxBucketEnum.NONE
    
    return tx


def rule_matches_transaction(rule: TaxRule, tx: Transaction) -> bool:
    """Check if a rule matches a transaction"""
    # Vendor matching
    if rule.vendor_contains:
        if not tx.vendor or rule.vendor_contains.upper() not in tx.vendor.upper():
            return False
    
    # Description matching
    if rule.description_contains:
        if not tx.description or rule.description_contains.upper() not in tx.description.upper():
            return False
    
    # Amount range matching
    if rule.min_amount is not None and abs(tx.amount) < rule.min_amount:
        return False
    
    if rule.max_amount is not None and abs(tx.amount) > rule.max_amount:
        return False
    
    # Business/personal matching
    if rule.applies_to_business and not tx.is_business:
        return False
    
    if not rule.applies_to_personal and not tx.is_business:
        return False
    
    return True

