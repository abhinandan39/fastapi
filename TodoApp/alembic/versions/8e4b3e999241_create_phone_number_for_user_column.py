"""create phone number for user column

Revision ID: 8e4b3e999241
Revises: 
Create Date: 2024-12-24 12:45:36.121408

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e4b3e999241'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(),nullable=True))

def downgrade() -> None:
    op.drop_column('users', 'phone_number')
