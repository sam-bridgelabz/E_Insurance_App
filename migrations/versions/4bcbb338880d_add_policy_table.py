"""add policy table

Revision ID: 4bcbb338880d
Revises: d667edfd3e01  # ✅ Depends on customer table now
Create Date: 2025-06-22 14:04:10.564914
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision: str = '4bcbb338880d'
down_revision: Union[str, None] = 'd667edfd3e01'  # now points to customer
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'policies',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('scheme_id', sa.String(), sa.ForeignKey('schemes.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('customer_id', sa.String(), sa.ForeignKey('customers.id', ondelete='CASCADE'), nullable=False),
        sa.Column('premium_amount', sa.Integer(), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('expiry_date', sa.Date(), nullable=False),
        sa.Column('agent_id', sa.String(), sa.ForeignKey('agents.id', ondelete='CASCADE'), nullable=False)
    )

def downgrade() -> None:
    op.drop_table('policies')
