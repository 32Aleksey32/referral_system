import secrets
from datetime import datetime, timezone
from typing import Callable
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import CustomError

from .model import ReferralCode
from .repository import ReferralCodeRepository


class ReferralCodeService:
    def __init__(self, session: AsyncSession):
        self.repo = ReferralCodeRepository(session)

    async def add_referral_code(self, user_id: UUID, expires_at: datetime) -> ReferralCode:
        existing_referral_code = await self.repo.get_referral_code_by_user_id(user_id)
        if existing_referral_code:
            raise CustomError('У Вас уже есть активный реферальный код.', status_code=409)

        code = await self.generate_referral_code()

        referral_code = ReferralCode(user_id=user_id, expires_at=expires_at, code=code)
        await self.repo.add_referral_code(referral_code)
        return referral_code

    async def delete_referral_code(self, user_id: UUID) -> None:
        referral_code = await self.repo.get_referral_code_by_user_id(user_id)
        if not referral_code:
            raise CustomError('Реферальный код отсутствует.', status_code=404)
        await self.repo.delete_referral_code(referral_code)

    async def get_referral_code_by_user_email(self, get_user_by_email: Callable, email: str) -> ReferralCode:
        user = await get_user_by_email(email)
        if not user:
            raise CustomError('Пользователя с таким с таким email не существует.', status_code=404)

        referral_code = user.referral_code
        if not referral_code:
            raise CustomError('Реферальный код у пользователя с таким email отсутствует.', status_code=404)

        return referral_code

    async def get_referral_code_by_code(self, code: str) -> ReferralCode:
        referral_code = await self.repo.get_referral_code_by_code(code)
        if referral_code is None:
            raise CustomError('Неверный реферальный код.', status_code=409)
        if referral_code.expires_at < datetime.now(timezone.utc):
            raise CustomError('Срок действия реферального кода истек.', status_code=410)
        return referral_code

    async def generate_referral_code(self) -> str:
        while True:
            code = secrets.token_urlsafe(10)
            existing_code = await self.repo.get_referral_code_by_code(code)
            if existing_code is None:
                return code
