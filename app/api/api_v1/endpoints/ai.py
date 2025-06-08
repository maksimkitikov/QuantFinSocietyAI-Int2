from fastapi import APIRouter, HTTPException
from typing import List, Dict
from app.services.ai_service import AIService
from pydantic import BaseModel
import pandas as pd

router = APIRouter()
ai_service = AIService()

class NewsAnalysisRequest(BaseModel):
    text: str

class StockPredictionRequest(BaseModel):
    symbol: str
    period: str = "1y"

@router.post("/analyze-news")
async def analyze_news_sentiment(request: NewsAnalysisRequest) -> Dict:
    """
    Analyze news sentiment
    """
    try:
        return await ai_service.analyze_news_sentiment(request.text)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/predict-stock")
async def predict_stock_movement(request: StockPredictionRequest) -> Dict:
    """
    Predict stock price movement
    """
    try:
        # Get stock data and pass to service
        # Using placeholder for now
        stock_data = pd.DataFrame()
        return await ai_service.predict_stock_movement(stock_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/market-insight")
async def generate_market_insight(symbol: str) -> Dict:
    """
    Generate market analysis insight
    """
    try:
        # Get stock data and news
        # Using placeholder for now
        stock_data = pd.DataFrame()
        news_data = []
        return await ai_service.generate_market_insight(stock_data, news_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 