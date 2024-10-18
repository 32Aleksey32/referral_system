from typing import Callable, Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import CustomError

from .model import Referral
from .repository import ReferralRepository


class ReferralService:
    def __init__(self, session: AsyncSession):
        self.repo = ReferralRepository(session)

    async def add_referral(self, referral_id: int, referrer_id: int) -> None:
        referral = Referral(referrer_id=referrer_id, referral_id=referral_id)
        await self.repo.add_referral(referral)

    async def get_all_referrals(self, user_id: UUID, get_user_by_id: Callable) -> Sequence[Referral]:
        user = await get_user_by_id(user_id)
        if not user:
            raise CustomError('Пользователь с таким uuid не найден.', status_code=404)
        return await self.repo.get_all_referrals(user_id)
