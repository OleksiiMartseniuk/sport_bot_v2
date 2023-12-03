"""logger

Revision ID: 4ce66ee364e1
Revises: 5f9a51a9060b
Create Date: 2023-12-03 21:55:54.772747

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ce66ee364e1'
down_revision: Union[str, None] = '5f9a51a9060b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('status_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('logger_name', sa.String(length=255), nullable=False),
    sa.Column('level', sa.Enum('CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET', name='loglevel'), nullable=False),
    sa.Column('msg', sa.String(), nullable=False),
    sa.Column('trace', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('status_log')
    # ### end Alembic commands ###
