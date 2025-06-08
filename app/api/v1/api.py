from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, market, predict, sentiment

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(market.router, prefix="/market", tags=["market"])
api_router.include_router(predict.router, prefix="/predict", tags=["predictions"])
api_router.include_router(sentiment.router, prefix="/sentiment", tags=["sentiment"]) 