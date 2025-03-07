"""empty message

Revision ID: 53f0d23c94cb
Revises: 35c0e6ad642a
Create Date: 2025-02-24 00:26:20.617793

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '53f0d23c94cb'
down_revision: Union[str, None] = '35c0e6ad642a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
