"""create referrals

Revision ID: 8154377a89f0
Revises: 65496e0e2344
Create Date: 2024-10-14 20:33:17.172794

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8154377a89f0'
down_revision: Union[str, None] = '65496e0e2344'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('referrals',
    sa.Column('referrer_id', sa.UUID(), nullable=False),
    sa.Column('referral_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['referrer_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['referral_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('referral_id', 'referrer_id', name='pk_referral_referrer')
    )


def downgrade() -> None:
    op.drop_table('referrals')
