"""some updates

Revision ID: 8a064488aeab
Revises: 3f0837e02fdf
Create Date: 2024-10-06 01:26:31.126780

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a064488aeab'
down_revision: Union[str, None] = '3f0837e02fdf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
