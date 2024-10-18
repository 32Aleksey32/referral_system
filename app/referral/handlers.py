from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import CustomError
from app.session import get_db
from app.user.service import UserService

from .schema import ReferralRead
from .service import ReferralService

referral_router = APIRouter()


@referral_router.get(
    "/{user_id}",
    response_model=List[ReferralRead],
    summary="Получить информацию о рефералах"
)
async def get_referrals(user_id: UUID, session: AsyncSession = Depends(get_db)):
    referral_service = ReferralService(session)
    user_service = UserService(session)
    try:
        referrals = await referral_service.get_all_referrals(user_id, user_service.get_user_by_id)
        return [ReferralRead.model_validate(referral.referral) for referral in referrals]
    except CustomError as err:
        raise HTTPException(status_code=err.status_code, detail=err.message)
