from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class SentimentRequest(BaseModel):
    symbol: str = Field(..., description="Тикер акции", example="AAPL")
    days: int = Field(..., description="Количество дней для анализа", ge=1, le=30, example=7)

class ArticleSentiment(BaseModel):
    title: str = Field(..., description="Заголовок новости")
    sentiment: str = Field(..., description="Тональность (positive/negative/neutral)")
    score: float = Field(..., description="Оценка тональности от -1 до 1")
    published_at: datetime = Field(..., description="Дата публикации")

class SentimentAnalysis(BaseModel):
    symbol: str = Field(..., description="Тикер акции")
    overall_sentiment: str = Field(..., description="Общая тональность (positive/negative/neutral)")
    sentiment_score: float = Field(..., description="Общая оценка тональности от -1 до 1")
    articles: List[ArticleSentiment] = Field(..., description="Список проанализированных новостей") 