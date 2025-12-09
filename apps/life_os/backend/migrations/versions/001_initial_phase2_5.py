"""Initial Phase 2.5 schema

Revision ID: 001_initial_phase2_5
Revises: 
Create Date: 2025-01-XX

Phase 2.5 — CONTROL_OTTO_PHASE2_5_FOUNDATIONS.md
Baseline migration for Phase 2.5 models and fields
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey

# revision identifiers, used by Alembic.
revision: str = '001_initial_phase2_5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Create all Phase 2.5 tables.
    
    This is a baseline migration that creates:
    - Household and UserProfile (context)
    - Category and CategoryVersion (taxonomy)
    - OttoEvent (events)
    - Updates to existing tables (household_id, reasoning, evidence)
    """
    # Create households table
    op.create_table(
        'households',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('timezone', sa.String(), nullable=False),
        sa.Column('currency', sa.String(), nullable=False),
        sa.Column('locale', sa.String(), nullable=False),
        sa.Column('tax_filing_status', sa.String(), nullable=True),
        sa.Column('tax_year_start', sa.Date(), nullable=True),
        sa.Column('primary_user_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create user_profiles table
    op.create_table(
        'user_profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('household_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['household_id'], ['households.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add foreign key for primary_user_id
    op.create_foreign_key(
        'fk_households_primary_user',
        'households', 'user_profiles',
        ['primary_user_id'], ['id']
    )
    
    # Create categories table
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('household_id', sa.Integer(), nullable=True),
        sa.Column('code', sa.String(), nullable=False),
        sa.Column('label', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('tax_line', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['household_id'], ['households.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create category_versions table
    op.create_table(
        'category_versions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False),
        sa.Column('effective_from', sa.Date(), nullable=False),
        sa.Column('effective_to', sa.Date(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create otto_events table
    op.create_table(
        'otto_events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('processed_at', sa.DateTime(), nullable=True),
        sa.Column('household_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('source_model', sa.String(), nullable=False),
        sa.Column('source_id', sa.Integer(), nullable=False),
        sa.Column('payload', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('error', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['household_id'], ['households.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add household_id and user_id to existing tables
    # Note: These migrations assume tables already exist from auto-create
    # In practice, you'd check if columns exist first
    
    # otto_runs
    try:
        op.add_column('otto_runs', sa.Column('household_id', sa.Integer(), nullable=True))
        op.add_column('otto_runs', sa.Column('user_id', sa.Integer(), nullable=True))
        op.add_column('otto_runs', sa.Column('reasoning', sa.JSON(), nullable=True))
        op.add_column('otto_runs', sa.Column('evidence', sa.JSON(), nullable=True))
        op.create_foreign_key('fk_otto_runs_household', 'otto_runs', 'households', ['household_id'], ['id'])
        op.create_foreign_key('fk_otto_runs_user', 'otto_runs', 'user_profiles', ['user_id'], ['id'])
    except:
        pass  # Columns may already exist
    
    # otto_tasks
    try:
        op.add_column('otto_tasks', sa.Column('household_id', sa.Integer(), nullable=True))
        op.add_column('otto_tasks', sa.Column('user_id', sa.Integer(), nullable=True))
        op.create_foreign_key('fk_otto_tasks_household', 'otto_tasks', 'households', ['household_id'], ['id'])
        op.create_foreign_key('fk_otto_tasks_user', 'otto_tasks', 'user_profiles', ['user_id'], ['id'])
    except:
        pass
    
    # life_os_tasks
    try:
        op.add_column('life_os_tasks', sa.Column('household_id', sa.Integer(), nullable=True))
        op.add_column('life_os_tasks', sa.Column('user_id', sa.Integer(), nullable=True))
        op.create_foreign_key('fk_life_os_tasks_household', 'life_os_tasks', 'households', ['household_id'], ['id'])
        op.create_foreign_key('fk_life_os_tasks_user', 'life_os_tasks', 'user_profiles', ['user_id'], ['id'])
    except:
        pass
    
    # bills
    try:
        op.add_column('bills', sa.Column('household_id', sa.Integer(), nullable=True))
        op.create_foreign_key('fk_bills_household', 'bills', 'households', ['household_id'], ['id'])
    except:
        pass
    
    # calendar_events
    try:
        op.add_column('calendar_events', sa.Column('household_id', sa.Integer(), nullable=True))
        op.add_column('calendar_events', sa.Column('user_id', sa.Integer(), nullable=True))
        op.create_foreign_key('fk_calendar_events_household', 'calendar_events', 'households', ['household_id'], ['id'])
        op.create_foreign_key('fk_calendar_events_user', 'calendar_events', 'user_profiles', ['user_id'], ['id'])
    except:
        pass
    
    # income
    try:
        op.add_column('income', sa.Column('household_id', sa.Integer(), nullable=True))
        op.add_column('income', sa.Column('user_id', sa.Integer(), nullable=True))
        op.create_foreign_key('fk_income_household', 'income', 'households', ['household_id'], ['id'])
        op.create_foreign_key('fk_income_user', 'income', 'user_profiles', ['user_id'], ['id'])
    except:
        pass
    
    # transactions
    try:
        op.add_column('transactions', sa.Column('household_id', sa.Integer(), nullable=True))
        op.add_column('transactions', sa.Column('user_id', sa.Integer(), nullable=True))
        op.add_column('transactions', sa.Column('category_id', sa.Integer(), nullable=True))
        op.add_column('transactions', sa.Column('category_version', sa.Integer(), nullable=True))
        op.create_foreign_key('fk_transactions_household', 'transactions', 'households', ['household_id'], ['id'])
        op.create_foreign_key('fk_transactions_user', 'transactions', 'user_profiles', ['user_id'], ['id'])
        op.create_foreign_key('fk_transactions_category', 'transactions', 'categories', ['category_id'], ['id'])
    except:
        pass


def downgrade() -> None:
    """
    Rollback Phase 2.5 changes.
    
    Note: This is a destructive operation that will remove all Phase 2.5 tables and columns.
    """
    # Remove foreign keys and columns from existing tables
    try:
        op.drop_constraint('fk_transactions_category', 'transactions', type_='foreignkey')
        op.drop_constraint('fk_transactions_user', 'transactions', type_='foreignkey')
        op.drop_constraint('fk_transactions_household', 'transactions', type_='foreignkey')
        op.drop_column('transactions', 'category_version')
        op.drop_column('transactions', 'category_id')
        op.drop_column('transactions', 'user_id')
        op.drop_column('transactions', 'household_id')
    except:
        pass
    
    try:
        op.drop_constraint('fk_income_user', 'income', type_='foreignkey')
        op.drop_constraint('fk_income_household', 'income', type_='foreignkey')
        op.drop_column('income', 'user_id')
        op.drop_column('income', 'household_id')
    except:
        pass
    
    try:
        op.drop_constraint('fk_calendar_events_user', 'calendar_events', type_='foreignkey')
        op.drop_constraint('fk_calendar_events_household', 'calendar_events', type_='foreignkey')
        op.drop_column('calendar_events', 'user_id')
        op.drop_column('calendar_events', 'household_id')
    except:
        pass
    
    try:
        op.drop_constraint('fk_bills_household', 'bills', type_='foreignkey')
        op.drop_column('bills', 'household_id')
    except:
        pass
    
    try:
        op.drop_constraint('fk_life_os_tasks_user', 'life_os_tasks', type_='foreignkey')
        op.drop_constraint('fk_life_os_tasks_household', 'life_os_tasks', type_='foreignkey')
        op.drop_column('life_os_tasks', 'user_id')
        op.drop_column('life_os_tasks', 'household_id')
    except:
        pass
    
    try:
        op.drop_constraint('fk_otto_tasks_user', 'otto_tasks', type_='foreignkey')
        op.drop_constraint('fk_otto_tasks_household', 'otto_tasks', type_='foreignkey')
        op.drop_column('otto_tasks', 'user_id')
        op.drop_column('otto_tasks', 'household_id')
    except:
        pass
    
    try:
        op.drop_constraint('fk_otto_runs_user', 'otto_runs', type_='foreignkey')
        op.drop_constraint('fk_otto_runs_household', 'otto_runs', type_='foreignkey')
        op.drop_column('otto_runs', 'evidence')
        op.drop_column('otto_runs', 'reasoning')
        op.drop_column('otto_runs', 'user_id')
        op.drop_column('otto_runs', 'household_id')
    except:
        pass
    
    # Drop new tables
    op.drop_table('otto_events')
    op.drop_table('category_versions')
    op.drop_table('categories')
    op.drop_constraint('fk_households_primary_user', 'households', type_='foreignkey')
    op.drop_table('user_profiles')
    op.drop_table('households')

