import asyncio
from datetime import timedelta
from uuid import UUID

import asyncpg
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.auth.security import create_access_token
from app.main import app
from app.referral_code.model import ReferralCode
from app.session import get_db
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES, DATABASE_URL
from app.user.model import User

test_engine = create_async_engine(DATABASE_URL, future=True, echo=True)
test_async_session = sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def _get_test_db():
    async with test_async_session() as session:
        yield session


@pytest.fixture(scope="session")
async def client() -> AsyncClient:
    app.dependency_overrides[get_db] = _get_test_db
    async with AsyncClient(transport=ASGITransport(app), base_url="http://testserver") as client:
        yield client


def create_test_auth_headers_for_user(email: str):
    access_token = create_access_token(
        data={"sub": email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool("".join(DATABASE_URL.split("+asyncpg")))
    try:
        yield pool
    finally:
        await pool.close()


@pytest.fixture
async def create_user_in_database(asyncpg_pool):

    async def create_user_in_database(user_id: UUID, username: str, email: str, password: str):
        async with test_async_session() as session:
            new_user = User(id=user_id, username=username, hashed_password=password, email=email)
            session.add(new_user)
            await session.commit()
            return new_user

    return create_user_in_database


@pytest.fixture
async def get_user_from_database(asyncpg_pool):
    async def get_user_from_database_by_uuid(user_id: UUID):
        async with test_async_session() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            return result.scalars().first()
    return get_user_from_database_by_uuid


@pytest.fixture
async def get_referral_code_from_database(asyncpg_pool):
    async def get_referral_code_from_database_by_code(code: str):
        async with test_async_session() as session:
            result = await session.execute(select(ReferralCode).where(ReferralCode.code == code))
            return result.scalars().first()
    return get_referral_code_from_database_by_code
