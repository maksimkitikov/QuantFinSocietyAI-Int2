from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class PredictionRequest(BaseModel):
    symbol: str = Field(..., description="Тикер акции", example="AAPL")
    days: int = Field(..., description="Количество дней для прогноза", ge=1, le=30, example=7)

class PricePoint(BaseModel):
    date: datetime = Field(..., description="Дата прогноза")
    price: float = Field(..., description="Прогнозируемая цена", ge=0)

class PricePrediction(BaseModel):
    symbol: str = Field(..., description="Тикер акции")
    predictions: List[PricePoint] = Field(..., description="Список прогнозов по дням")
    confidence: float = Field(..., description="Уровень уверенности в прогнозе", ge=0, le=1) 