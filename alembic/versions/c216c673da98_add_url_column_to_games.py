"""add url column to games

Revision ID: c216c673da98
Revises: accc10800deb
Create Date: 2025-04-20 11:27:23.803629

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c216c673da98'
down_revision: Union[str, None] = 'accc10800deb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('games', sa.Column('url', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('games', 'url')

