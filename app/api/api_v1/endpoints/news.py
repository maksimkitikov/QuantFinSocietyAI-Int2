from fastapi import APIRouter, HTTPException
from typing import List, Dict, Optional
from app.services.news_service import NewsService
from datetime import datetime

router = APIRouter()
news_service = NewsService()

@router.get("/market")
async def get_market_news() -> List[Dict]:
    """
    Get market news
    """
    try:
        return await news_service.get_market_news()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/company/{company_name}")
async def get_company_news(company_name: str) -> List[Dict]:
    """
    Get company-specific news
    """
    try:
        return await news_service.get_company_news(company_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/calendar")
async def get_economic_calendar() -> List[Dict]:
    """
    Get economic calendar
    """
    try:
        return await news_service.get_economic_calendar()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 