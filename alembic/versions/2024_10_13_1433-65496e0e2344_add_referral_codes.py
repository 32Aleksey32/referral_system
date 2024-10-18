"""add referral_codes

Revision ID: 65496e0e2344
Revises: dd2223b6ce62
Create Date: 2024-10-13 14:33:30.073734

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '65496e0e2344'
down_revision: Union[str, None] = 'dd2223b6ce62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('referral_codes',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('expires_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code'),
    sa.UniqueConstraint('user_id')
    )


def downgrade() -> None:
    op.drop_table('referral_codes')
