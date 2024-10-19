from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth import get_current_user
from app.errors import CustomError
from app.session import get_db
from app.user import User, UserService

from .schema import ReferralCodeCreate, ReferralCodeDetail, ReferralCodeRead
from .service import ReferralCodeService

referral_code_router = APIRouter()


@referral_code_router.post('',  response_model=ReferralCodeRead, summary='Создать реферальный код')
async def create_referral_code(
    code_data: ReferralCodeCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    ref_code_service = ReferralCodeService(session)
    try:
        return await ref_code_service.add_referral_code(current_user.id, code_data.expires_at)
    except CustomError as err:
        raise HTTPException(status_code=err.status_code, detail=err.message)


@referral_code_router.get(
    '/{email}',
    response_model=ReferralCodeDetail,
    summary='Получить реферальный код по email пользователя'
)
async def get_referral_code_by_user_email(email: EmailStr, session: AsyncSession = Depends(get_db)):
    ref_code_service = ReferralCodeService(session)
    user_service = UserService(session)
    try:
        return await ref_code_service.get_referral_code_by_user_email(user_service.get_user_by_email, email)
    except CustomError as err:
        raise HTTPException(status_code=err.status_code, detail=err.message)


@referral_code_router.delete('', summary='Удалить реферальный код')
async def delete_referral_code(
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_db)
):
    ref_code_service = ReferralCodeService(session)
    try:
        await ref_code_service.delete_referral_code(current_user.id)
        return {"detail": "Реферальный код успешно удален."}
    except CustomError as err:
        raise HTTPException(status_code=err.status_code, detail=err.message)
