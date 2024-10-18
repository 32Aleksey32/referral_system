from typing import Callable, Union
from uuid import UUID

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import CustomError
from app.user.utils.email_verification import verify_email_via_hunter

from .model import User
from .repository import UserRepository
from .schema import UserCreate


class UserService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def authenticate_user(self, username: str, password: str) -> Union[User, bool]:
        user = await self.get_user_by_username(username)
        if not user:
            return False
        if not self.pwd_context.verify(password, user.hashed_password):
            return False
        return user

    async def add_user(self, user: UserCreate, get_referral_code_by_code: Callable, add_referral: Callable) -> User:
        # Проверяем, существует ли уже пользователя с такими данными
        await self.check_existing_user(user.email, user.username)

        # Проверяем email через Hunter.io (не проверяет домен ".ru")
        await verify_email_via_hunter(user.email)

        if user.referral_code:
            referral_code = await get_referral_code_by_code(user.referral_code)

        new_user = User(
            username=user.username,
            email=user.email,
            hashed_password=self.pwd_context.hash(user.password)
        )

        await self.repo.add_user(new_user)

        if user.referral_code:
            await add_referral(referrer_id=referral_code.user_id, referral_id=new_user.id)

        return new_user

    async def get_user_by_email(self, email: str) -> User:
        return await self.repo.get_user_by_email(email)

    async def get_user_by_username(self, username: str) -> User:
        return await self.repo.get_user_by_username(username)

    async def get_user_by_id(self, user_id: UUID) -> User:
        return await self.repo.get_user_by_id(user_id)

    async def check_existing_user(self, email: str, username: str) -> None:
        user = await self.repo.check_existing_user(email, username)
        if user:
            if user.email == email:
                raise CustomError('Пользователь с таким email уже существует.', status_code=409)
            if user.username == username:
                raise CustomError('Пользователь с таким username уже существует.', status_code=409)
