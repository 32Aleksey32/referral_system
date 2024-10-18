from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .model import ReferralCode


class ReferralCodeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_referral_code(self, referral_code: ReferralCode) -> None:
        self.session.add(referral_code)
        await self.session.commit()

    async def delete_referral_code(self, referral_code: ReferralCode) -> None:
        await self.session.delete(referral_code)
        await self.session.commit()

    async def get_referral_code_by_user_id(self, user_id: UUID) -> ReferralCode:
        query = select(ReferralCode).where(ReferralCode.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_referral_code_by_code(self, code: str) -> ReferralCode:
        query = select(ReferralCode).where(ReferralCode.code == code)
        result = await self.session.execute(query)
        return result.scalars().first()
