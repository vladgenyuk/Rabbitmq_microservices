"""add: likes

Revision ID: 17ab8c84de3c
Revises: de021151bd26
Create Date: 2024-07-24 16:34:35.330028

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '17ab8c84de3c'
down_revision: Union[str, None] = 'de021151bd26'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('likes', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'likes')
    # ### end Alembic commands ###
