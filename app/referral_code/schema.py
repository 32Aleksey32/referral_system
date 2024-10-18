from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ReferralCodeCreate(BaseModel):
    expires_at: datetime


class ReferralCodeRead(BaseModel):
    id: UUID
    code: str
    expires_at: datetime


class ReferralCodeDetail(BaseModel):
    code: str
