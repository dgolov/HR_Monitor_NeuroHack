"""add employee

Revision ID: 3f0837e02fdf
Revises: 6c378094dcbe
Create Date: 2024-10-05 16:33:28.121873

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f0837e02fdf'
down_revision: Union[str, None] = '6c378094dcbe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employee',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('date_started', sa.Date(), nullable=True),
    sa.Column('date_fired', sa.Date(), nullable=True),
    sa.Column('position', sa.String(), nullable=True),
    sa.Column('cost_of_hiring', sa.Integer(), nullable=True),
    sa.Column('manager_rating', sa.Integer(), nullable=True),
    sa.Column('recruiter_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['recruiter_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('employee')
    # ### end Alembic commands ###
