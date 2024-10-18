from fastapi import APIRouter, FastAPI

from app.referral.handlers import referral_router
from app.referral_code.handlers import referral_code_router
from app.user.handlers import user_router

app = FastAPI(title='Referral System API')

api_router = APIRouter()

api_router.include_router(user_router, prefix='/users', tags=['users'])
api_router.include_router(referral_code_router, prefix='/referral-codes', tags=['referral-codes'])
api_router.include_router(referral_router, prefix='/referrals', tags=['referrals'])

app.include_router(api_router)
