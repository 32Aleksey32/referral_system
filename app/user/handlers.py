from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth import get_current_user
from app.auth.security import create_access_token
from app.errors import CustomError
from app.referral.service import ReferralService
from app.referral_code.service import ReferralCodeService
from app.session import get_db
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES

from .model import User
from .schema import Token, UserCreate, UserMe, UserRead
from .service import UserService

user_router = APIRouter()


@user_router.post('/register', response_model=UserRead, summary='Регистрация пользователя')
async def register(user: UserCreate, session: AsyncSession = Depends(get_db)):
    user_service = UserService(session)
    ref_code_service = ReferralCodeService(session)
    referral_service = ReferralService(session)
    try:
        return await user_service.add_user(
            user, ref_code_service.get_referral_code_by_code, referral_service.add_referral
        )
    except CustomError as err:
        raise HTTPException(status_code=err.status_code, detail=err.message)


@user_router.get('/me', response_model=UserMe, summary='Получить информацию о текущем пользователе')
async def get_user(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)):
    user_service = UserService(session)
    return await user_service.get_user_by_email(user.email)


@user_router.post('/login', response_model=Token, summary='Аутентификация пользователя')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_db)):
    user_service = UserService(session)
    user = await user_service.authenticate_user(username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверные учетные данные.')
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub': user.email}, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}
