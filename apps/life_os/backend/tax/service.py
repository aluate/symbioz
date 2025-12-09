"""
TaxBrain service layer - main interface for tax operations
"""

from typing import List, Optional
from datetime import datetime

from .models import (
    TaxProfile,
    TaxCategory,
    TaxRule,
    Transaction,
    TaxYearSummary,
    TaxDocument,
)
from .enums import TaxBucketEnum
from .rules import apply_rules_to_transaction
from .reports import generate_tax_year_summary


class TaxBrain:
    """Main service class for tax operations"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        # In a real implementation, these would come from a database
        self._categories: List[TaxCategory] = []
        self._rules: List[TaxRule] = []
        self._transactions: List[Transaction] = []
        self._profile: Optional[TaxProfile] = None
    
    def get_profile(self) -> Optional[TaxProfile]:
        """Get tax profile for user"""
        return self._profile
    
    def update_profile(self, profile: TaxProfile) -> TaxProfile:
        """Update tax profile"""
        profile.user_id = self.user_id
        profile.updated_at = datetime.now()
        self._profile = profile
        return profile
    
    def get_categories(self) -> List[TaxCategory]:
        """Get all tax categories"""
        return self._categories
    
    def add_category(self, category: TaxCategory) -> TaxCategory:
        """Add a tax category"""
        self._categories.append(category)
        return category
    
    def get_rules(self) -> List[TaxRule]:
        """Get all tax rules for user"""
        return [r for r in self._rules if r.user_id == self.user_id]
    
    def add_rule(self, rule: TaxRule) -> TaxRule:
        """Add a tax rule"""
        rule.user_id = self.user_id
        self._rules.append(rule)
        return rule
    
    def categorize_transaction(self, transaction: Transaction) -> Transaction:
        """Categorize a transaction using rules"""
        transaction.user_id = self.user_id
        rules = self.get_rules()
        return apply_rules_to_transaction(transaction, rules, self._categories)
    
    def add_transaction(self, transaction: Transaction) -> Transaction:
        """Add and categorize a transaction"""
        categorized = self.categorize_transaction(transaction)
        self._transactions.append(categorized)
        return categorized
    
    def get_transactions(
        self,
        year: Optional[int] = None,
        tax_relevant_only: bool = False
    ) -> List[Transaction]:
        """Get transactions, optionally filtered by year and tax relevance"""
        txs = [t for t in self._transactions if t.user_id == self.user_id]
        
        if year:
            start = datetime(year, 1, 1)
            end = datetime(year + 1, 1, 1)
            txs = [t for t in txs if start <= t.date < end]
        
        if tax_relevant_only:
            txs = [t for t in txs if t.is_tax_relevant]
        
        return txs
    
    def generate_year_summary(self, year: int) -> TaxYearSummary:
        """Generate tax year summary"""
        transactions = self.get_transactions(year=year, tax_relevant_only=True)
        return generate_tax_year_summary(transactions, self.user_id, year)
    
    def get_documents(self, year: Optional[int] = None) -> List[TaxDocument]:
        """Get tax documents, optionally filtered by year"""
        # Placeholder - would query database in real implementation
        return []

