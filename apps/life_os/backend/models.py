"""
Life OS data models
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey, Boolean, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Household(Base):
    """Model for household (multi-user support)"""
    __tablename__ = "households"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    name = Column(String, nullable=False)  # e.g., "Karl's Household"
    timezone = Column(String, nullable=False, default="America/Los_Angeles")  # e.g., "America/Los_Angeles"
    currency = Column(String, nullable=False, default="USD")  # e.g., "USD"
    locale = Column(String, nullable=False, default="en-US")  # e.g., "en-US"
    
    tax_filing_status = Column(String, nullable=True)  # e.g., "single", "married_joint", "married_separate", "head_of_household"
    tax_year_start = Column(Date, nullable=True)  # Default Jan 1, but can be customized
    
    primary_user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=True)
    
    # Relationships
    users = relationship("UserProfile", back_populates="household", foreign_keys="UserProfile.household_id")


class UserProfile(Base):
    """Model for user profiles within a household"""
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    name = Column(String, nullable=False)  # e.g., "Karl", "Brit"
    email = Column(String, nullable=True)
    role = Column(String, nullable=False, default="primary")  # e.g., "primary", "spouse", "dependent"
    is_active = Column(Boolean, nullable=False, default=True)
    
    # Relationships
    household = relationship("Household", back_populates="users", foreign_keys=[household_id])


class OttoRun(Base):
    """Model for Otto run records"""
    __tablename__ = "otto_runs"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=True)
    
    status = Column(String, nullable=False, default="pending")  # pending, running, success, error
    source = Column(String, nullable=False, default="shell")  # shell, worker, webhook
    
    input_text = Column(Text, nullable=False)
    input_payload = Column(JSON, nullable=True)
    
    output_text = Column(Text, nullable=True)
    output_payload = Column(JSON, nullable=True)
    
    logs = Column(Text, nullable=True)
    
    # Phase 2.5: Decision memory & reasoning
    reasoning = Column(JSON, nullable=True)  # Structured reasoning steps
    evidence = Column(JSON, nullable=True)  # IDs of entities consulted (bills, transactions, etc.)


class OttoTask(Base):
    """Model for Otto tasks (what should happen)"""
    __tablename__ = "otto_tasks"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=True)
    
    status = Column(String, nullable=False, default="pending")  # pending, running, success, error, blocked, pending_approval
    type = Column(String, nullable=False)  # e.g. "life_os.create_task", "infra.deploy", etc.
    
    description = Column(Text, nullable=False)
    payload = Column(JSON, nullable=True)
    
    next_run_at = Column(DateTime, nullable=True)  # For scheduled/recurring tasks
    last_run_at = Column(DateTime, nullable=True)
    last_error = Column(Text, nullable=True)
    
    # Safety fields
    retries = Column(Integer, nullable=False, default=0)
    max_retries = Column(Integer, nullable=False, default=3)
    next_retry_at = Column(DateTime, nullable=True)
    requires_approval = Column(String, nullable=True)  # approval_id if pending approval


class LifeOSTask(Base):
    """Model for Life OS household tasks"""
    __tablename__ = "life_os_tasks"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    completed_at = Column(DateTime, nullable=True)
    
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=True)  # Creator/assignee
    
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="todo")  # todo, in_progress, done, blocked
    
    assignee = Column(String, nullable=True)  # e.g., "Karl", "Brit", "Household" (legacy field, use user_id for FK)
    due_date = Column(DateTime, nullable=True)
    priority = Column(String, nullable=True)  # low, medium, high
    category = Column(String, nullable=True)  # e.g., "bills", "household", "work"


class Bill(Base):
    """Model for household bills"""
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    paid_at = Column(DateTime, nullable=True)
    
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    
    name = Column(String, nullable=False)  # e.g., "Electric Bill", "Internet"
    amount = Column(String, nullable=False)  # Store as string to handle currency formatting
    due_date = Column(DateTime, nullable=False)
    paid = Column(String, nullable=False, default="no")  # yes, no, partial
    
    category = Column(String, nullable=True)  # e.g., "utilities", "subscription", "insurance"
    payee = Column(String, nullable=True)  # Who to pay (company name)
    account_number = Column(String, nullable=True)  # Account number for payment
    notes = Column(Text, nullable=True)
    
    # Recurring bill fields
    is_recurring = Column(String, nullable=False, default="no")  # yes, no
    recurrence_frequency = Column(String, nullable=True)  # monthly, quarterly, yearly
    next_due_date = Column(DateTime, nullable=True)  # For recurring bills


class CalendarEvent(Base):
    """Model for calendar events"""
    __tablename__ = "calendar_events"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=True)  # Creator/owner
    
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)  # Optional end time
    
    location = Column(String, nullable=True)
    attendees = Column(Text, nullable=True)  # Comma-separated or JSON
    category = Column(String, nullable=True)  # e.g., "work", "personal", "family"
    
    # Recurring event fields
    is_recurring = Column(String, nullable=False, default="no")  # yes, no
    recurrence_frequency = Column(String, nullable=True)  # daily, weekly, monthly, yearly
    recurrence_end_date = Column(DateTime, nullable=True)  # When recurrence stops
    
    # External calendar sync
    external_calendar_id = Column(String, nullable=True)  # e.g., Google Calendar event ID
    external_calendar_type = Column(String, nullable=True)  # e.g., "google", "outlook"
    external_sync_enabled = Column(String, nullable=False, default="no")  # yes, no
    
    # Status
    status = Column(String, nullable=False, default="confirmed")  # confirmed, tentative, cancelled
    reminders = Column(JSON, nullable=True)  # Array of reminder times (e.g., [{"minutes": 15}, {"minutes": 60}])


class Income(Base):
    """Model for income tracking"""
    __tablename__ = "income"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=True)  # Who received the income
    
    source = Column(String, nullable=False)  # e.g., "Salary", "Freelance", "Investment"
    amount = Column(String, nullable=False)  # Store as string to handle currency formatting
    received_date = Column(DateTime, nullable=False)
    category = Column(String, nullable=True)  # For tax purposes: "wages", "self_employment", "investment", etc.
    notes = Column(Text, nullable=True)
    
    # Recurring income fields
    is_recurring = Column(String, nullable=False, default="no")  # yes, no
    recurrence_frequency = Column(String, nullable=True)  # monthly, quarterly, yearly
    next_expected_date = Column(DateTime, nullable=True)  # For recurring income


class Category(Base):
    """Model for tax/expense categories"""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    household_id = Column(Integer, ForeignKey("households.id"), nullable=True)  # NULL = global category
    code = Column(String, nullable=False)  # Stable identifier, e.g. "TOOLS_HAND"
    label = Column(String, nullable=False)  # Display name, e.g. "Hand Tools"
    type = Column(String, nullable=False)  # "income", "expense", "transfer", "other"
    tax_line = Column(String, nullable=True)  # Optional IRS line reference
    is_active = Column(Boolean, nullable=False, default=True)


class CategoryVersion(Base):
    """Model for category versioning"""
    __tablename__ = "category_versions"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    version = Column(Integer, nullable=False)
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)  # NULL = current version
    notes = Column(Text, nullable=True)


class Transaction(Base):
    """Model for tracking transactions"""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=True)  # Who made the transaction
    
    date = Column(DateTime, nullable=False)
    amount = Column(String, nullable=False)  # Store as string, negative for expenses, positive for income
    vendor = Column(String, nullable=True)  # Vendor/merchant name
    description = Column(Text, nullable=True)
    
    # Tax categorization (via Tax Brain)
    tax_category = Column(String, nullable=True)  # Legacy field - e.g., "business_expense", "personal", "deductible"
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)  # Phase 2.5: Reference to Category table
    category_version = Column(Integer, nullable=True)  # Phase 2.5: Version of category used at classification time
    
    # Source tracking
    source = Column(String, nullable=False, default="manual")  # manual, import, bank_import, etc.
    source_id = Column(String, nullable=True)  # ID from source system if imported
    
    # Additional metadata
    notes = Column(Text, nullable=True)
    tags = Column(JSON, nullable=True)  # Array of tags for filtering


class OttoEvent(Base):
    """Model for Otto events (trigger system)"""
    __tablename__ = "otto_events"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    processed_at = Column(DateTime, nullable=True)
    
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    type = Column(String, nullable=False)  # e.g., "bill.created", "transaction.created", "task.completed"
    source_model = Column(String, nullable=False)  # "Bill", "Transaction", "Task", etc.
    source_id = Column(Integer, nullable=False)
    payload = Column(JSON, nullable=True)
    
    status = Column(String, nullable=False, default="pending")  # pending, processing, done, error
    error = Column(Text, nullable=True)


class OttoMemory(Base):
    """
    Model for Otto's long-term memory
    Phase 3 Extension — CONTROL_OTTO_LONG_TERM_MEMORY.md
    
    Structured memory system that is transparent, interpretable, queryable, and versioned.
    NOT vector embeddings or generic ML approach.
    """
    __tablename__ = "otto_memory"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    
    category = Column(String, nullable=False, index=True)  # e.g., "preference", "rule", "domain_fact", "interpretation_hint", "workflow_cue", "safety_policy"
    content = Column(Text, nullable=False)  # The memory itself (human-readable)
    tags = Column(JSON, nullable=True)  # Optional metadata for filtering (e.g., ["calendar", "reminders"])
    source = Column(String, nullable=False)  # "user", "otto_inference", "task", or "system"
    
    last_used_at = Column(DateTime, nullable=True)
    usage_count = Column(Integer, default=0, nullable=False)
    confidence_score = Column(Float, default=1.0, nullable=False)  # 0.0–1.0
    version = Column(Integer, default=1, nullable=False)
    
    # Phase 4: Expiration & Maintenance
    expires_at = Column(DateTime, nullable=True)
    is_stale = Column(Boolean, default=False, nullable=False)
    stale_reason = Column(Text, nullable=True)


class OttoMemoryHistory(Base):
    """
    Model for OttoMemory version history
    Phase 4 — CONTROL_OTTO_PHASE4_MEMORY_UI_AND_MAINTENANCE.md
    
    Archives previous versions of OttoMemory entries when they are updated.
    """
    __tablename__ = "otto_memory_history"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=True)
    
    memory_id = Column(Integer, ForeignKey("otto_memory.id"), nullable=False)
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    
    version = Column(Integer, nullable=False)  # The version number this history entry represents
    category = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(JSON, nullable=True)
    source = Column(String, nullable=False)
    
    changed_by = Column(String, nullable=True)  # "user", "Otto", "API", or user ID


class OttoMemoryLink(Base):
    """
    Model for linking OttoMemory entries to each other and domain objects
    Phase 4 — CONTROL_OTTO_PHASE4_MEMORY_UI_AND_MAINTENANCE.md
    
    Enables relationships between memories and domain objects (tasks, bills, transactions, events).
    """
    __tablename__ = "otto_memory_links"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    from_memory_id = Column(Integer, ForeignKey("otto_memory.id"), nullable=False)
    to_memory_id = Column(Integer, ForeignKey("otto_memory.id"), nullable=True)  # Nullable if linking to non-memory object
    
    target_type = Column(String, nullable=False)  # "task", "bill", "transaction", "event", "memory"
    target_id = Column(Integer, nullable=False)  # ID in the relevant table
    
    relationship_type = Column(String, nullable=False)  # "supports", "contradicts", "refines", "applies_to", etc.
    notes = Column(Text, nullable=True)


class ActivityReport(Base):
    """
    Model for OTTO activity reports
    Tracks activity and changes across all systems for specified time periods
    """
    __tablename__ = "activity_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    report_type = Column(String(50), nullable=False, index=True)  # 'daily', 'custom', 'period'
    period_start = Column(DateTime, nullable=False, index=True)
    period_end = Column(DateTime, nullable=False, index=True)
    
    report_data = Column(JSON, nullable=False)  # Full report data
    summary = Column(Text, nullable=True)  # Human-readable summary
    comparison_data = Column(JSON, nullable=True)  # For daily reports: comparison to previous period
    metadata = Column(JSON, nullable=True)  # Additional metadata (generation time, etc.)