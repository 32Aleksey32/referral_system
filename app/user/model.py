import uuid

from sqlalchemy import UUID, Column, String
from sqlalchemy.orm import relationship

from app.settings import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    referral_code = relationship('ReferralCode', back_populates='user', uselist=False)
    referrals = relationship('Referral', back_populates='referrer', foreign_keys='Referral.referrer_id')
