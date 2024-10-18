from typing import Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from .model import Referral


class ReferralRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_referrals(self, user_id: UUID) -> Sequence[Referral]:
        query = (
            select(Referral)
            .options(selectinload(Referral.referral))
            .where(Referral.referrer_id == user_id)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def add_referral(self, referral: Referral) -> None:
        self.session.add(referral)
        await self.session.commit()
