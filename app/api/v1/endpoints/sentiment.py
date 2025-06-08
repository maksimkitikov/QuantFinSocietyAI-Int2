from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.schemas.sentiment import SentimentAnalysis, SentimentRequest
from app.crud.market import get_stock_news
import numpy as np

router = APIRouter()

@router.post("/sentiment", response_model=SentimentAnalysis)
def analyze_sentiment(
    request: SentimentRequest,
    db: Session = Depends(deps.get_db)
) -> SentimentAnalysis:
    """
    Анализ тональности новостей по тикеру.
    
    - **symbol**: Тикер акции
    - **days**: Количество дней для анализа
    """
    # Получаем новости по тикеру
    news = get_stock_news(db, symbol=request.symbol, days=request.days)
    
    if not news:
        raise HTTPException(
            status_code=404,
            detail=f"No news found for symbol {request.symbol}"
        )
    
    # Имитация анализа тональности
    sentiments = []
    for article in news:
        # Генерируем случайную тональность от -1 до 1
        sentiment_score = np.random.uniform(-1, 1)
        sentiment = "positive" if sentiment_score > 0.2 else "negative" if sentiment_score < -0.2 else "neutral"
        
        sentiments.append({
            "title": article.title,
            "sentiment": sentiment,
            "score": round(sentiment_score, 2),
            "published_at": article.published_at
        })
    
    # Вычисляем общую тональность
    overall_sentiment = np.mean([s["score"] for s in sentiments])
    overall = "positive" if overall_sentiment > 0.2 else "negative" if overall_sentiment < -0.2 else "neutral"
    
    return SentimentAnalysis(
        symbol=request.symbol,
        overall_sentiment=overall,
        sentiment_score=round(overall_sentiment, 2),
        articles=sentiments
    ) 