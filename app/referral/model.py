from sqlalchemy import TIMESTAMP, Column, ForeignKey, PrimaryKeyConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.settings import Base


class Referral(Base):
    __tablename__ = 'referrals'
    __table_args__ = (
        PrimaryKeyConstraint('referrer_id', 'referral_id', name='pk_referral_referrer'),
    )

    referrer_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    referral_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    referrer = relationship('User', back_populates='referrals', foreign_keys=[referrer_id])
    referral = relationship('User', foreign_keys=[referral_id])
