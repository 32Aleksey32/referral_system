import uuid

from sqlalchemy import TIMESTAMP, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.settings import Base


class ReferralCode(Base):
    __tablename__ = 'referral_codes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, unique=True, nullable=False)
    expires_at = Column(TIMESTAMP(timezone=True), nullable=False)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        unique=True
    )

    user = relationship("User", back_populates='referral_code')
