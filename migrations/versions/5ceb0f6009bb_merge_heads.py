"""merge heads

Revision ID: 5ceb0f6009bb
Revises: 4bcbb338880d, 98c7ef4dffb2
Create Date: 2025-06-23 09:54:31.862774

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ceb0f6009bb'
down_revision: Union[str, None] = ('4bcbb338880d', '98c7ef4dffb2')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
