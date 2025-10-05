"""create reporting tables

Revision ID: 0002_create_reporting_tables
Revises: 0001_create_documents_table
Create Date: 2025-10-05 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002_create_reporting_tables'
down_revision = '0001_create_documents_table'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create sales_performance_metrics
    op.create_table(
        'sales_performance_metrics',
        sa.Column('id', sa.String(length=36), primary_key=True, nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('revenue', sa.Float(), nullable=False),
        sa.Column('conversion_rate', sa.Float(), nullable=False),
        sa.Column('pipeline_velocity', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    )

    # Create team_productivity_metrics
    op.create_table(
        'team_productivity_metrics',
        sa.Column('id', sa.String(length=36), primary_key=True, nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('tasks_completed', sa.Integer(), nullable=False),
        sa.Column('deals_closed', sa.Integer(), nullable=False),
        sa.Column('activity_level', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    )

    # Create customer_interaction_metrics
    op.create_table(
        'customer_interaction_metrics',
        sa.Column('id', sa.String(length=36), primary_key=True, nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('total_interactions', sa.Integer(), nullable=False),
        sa.Column('avg_engagement_score', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    )

    # Create pipeline_analytics_metrics
    # Use generic JSON for cross-database compatibility; application model maps to JSONB on Postgres.
    op.create_table(
        'pipeline_analytics_metrics',
        sa.Column('id', sa.String(length=36), primary_key=True, nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('stage_conversion_rates', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('pipeline_analytics_metrics')
    op.drop_table('customer_interaction_metrics')
    op.drop_table('team_productivity_metrics')
    op.drop_table('sales_performance_metrics')
