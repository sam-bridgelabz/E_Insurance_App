"""create customers table

Revision ID: d667edfd3e01
Revises: 29d1749d8870
Create Date: 2025-06-22 19:41:49.753852
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision: str = 'd667edfd3e01'
down_revision: Union[str, None] = '29d1749d8870'  # Initial base migration
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'customers',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('phone_number', sa.String(length=15), nullable=False),
        sa.Column('dob', sa.Date(), nullable=False),
        sa.Column('agent_id', sa.String(), sa.ForeignKey('agents.id', ondelete='CASCADE'), nullable=False),
        sa.Column('total_amount', sa.Integer(), nullable=False, server_default='0')
    )

def downgrade() -> None:
    op.drop_table('customers')
