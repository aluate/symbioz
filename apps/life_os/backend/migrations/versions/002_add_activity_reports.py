"""Add activity_reports table

Revision ID: 002_add_activity_reports
Revises: 001_initial_phase2_5
Create Date: 2025-01-XX

Adds activity_reports table for tracking OTTO activity reports
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey

# revision identifiers, used by Alembic.
revision: str = '002_add_activity_reports'
down_revision: Union[str, None] = '001_initial_phase2_5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create activity_reports table"""
    op.create_table(
        'activity_reports',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('report_type', sa.String(50), nullable=False),  # 'daily', 'custom', 'period'
        sa.Column('period_start', sa.DateTime(), nullable=False),
        sa.Column('period_end', sa.DateTime(), nullable=False),
        sa.Column('report_data', sa.JSON(), nullable=False),  # Full report data
        sa.Column('summary', sa.Text(), nullable=True),  # Human-readable summary
        sa.Column('comparison_data', sa.JSON(), nullable=True),  # For daily reports: comparison to previous period
        sa.Column('metadata', sa.JSON(), nullable=True),  # Additional metadata
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for efficient querying
    op.create_index('ix_activity_reports_created_at', 'activity_reports', ['created_at'])
    op.create_index('ix_activity_reports_report_type', 'activity_reports', ['report_type'])
    op.create_index('ix_activity_reports_period_start', 'activity_reports', ['period_start'])
    op.create_index('ix_activity_reports_period_end', 'activity_reports', ['period_end'])


def downgrade() -> None:
    """Drop activity_reports table"""
    op.drop_index('ix_activity_reports_period_end', table_name='activity_reports')
    op.drop_index('ix_activity_reports_period_start', table_name='activity_reports')
    op.drop_index('ix_activity_reports_report_type', table_name='activity_reports')
    op.drop_index('ix_activity_reports_created_at', table_name='activity_reports')
    op.drop_table('activity_reports')
