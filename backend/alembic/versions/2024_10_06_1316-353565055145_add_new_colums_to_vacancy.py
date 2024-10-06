"""add new colums to Vacancy

Revision ID: 353565055145
Revises: 6b5241f4f1e1
Create Date: 2024-10-06 13:16:20.687751

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '353565055145'
down_revision: Union[str, None] = '6b5241f4f1e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vacancy', sa.Column('closing_cost', sa.Integer(), nullable=True))
    op.add_column('vacancy', sa.Column('is_referral', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('vacancy', 'is_referral')
    op.drop_column('vacancy', 'closing_cost')
    # ### end Alembic commands ###
