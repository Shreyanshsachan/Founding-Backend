"""Initial migration

Revision ID: 7130b41e5a21
Revises: af9cef12264c
Create Date: 2025-01-22 21:03:20.035337

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7130b41e5a21'
down_revision: Union[str, None] = 'af9cef12264c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
