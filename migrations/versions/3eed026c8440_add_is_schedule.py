"""add is_schedule

Revision ID: 3eed026c8440
Revises: 210c21d4086d
Create Date: 2024-01-20 19:09:21.608207

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3eed026c8440'
down_revision: Union[str, None] = '210c21d4086d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('telegram_user', sa.Column('is_schedule', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('telegram_user', 'is_schedule')
    # ### end Alembic commands ###
