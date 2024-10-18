from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    referral_code: Optional[str] = None


class UserRead(BaseModel):
    id: UUID
    username: str
    email: EmailStr


class UserMe(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    referral_code: Optional[str]

    @field_validator('referral_code', mode='before')
    def get_referral_code(cls, referral_code):
        return referral_code.code if referral_code else None


class Token(BaseModel):
    access_token: str
    token_type: str
