"""Merge branches from teammate and me

Revision ID: e6fcfe1727fe
Revises: 4bcbb338880d, 98c7ef4dffb2
Create Date: 2025-06-22 20:12:51.388605

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6fcfe1727fe'
down_revision: Union[str, None] = ('4bcbb338880d', '98c7ef4dffb2')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
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
    """Downgrade schema."""
    pass
