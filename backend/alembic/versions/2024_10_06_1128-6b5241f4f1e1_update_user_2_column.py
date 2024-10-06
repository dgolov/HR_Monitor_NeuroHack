"""update User 2 column

Revision ID: 6b5241f4f1e1
Revises: ba07a7d1a019
Create Date: 2024-10-06 11:28:55.683822

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b5241f4f1e1'
down_revision: Union[str, None] = 'ba07a7d1a019'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('grade', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('efficiently', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'efficiently')
    op.drop_column('user', 'grade')
    # ### end Alembic commands ###
