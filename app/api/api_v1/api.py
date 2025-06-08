from fastapi import APIRouter
from app.api.api_v1.endpoints import stocks, news, ai

api_router = APIRouter()

api_router.include_router(stocks.router, prefix="/stocks", tags=["stocks"])
api_router.include_router(news.router, prefix="/news", tags=["news"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"]) 